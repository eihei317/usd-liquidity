"""Derive signals, scoring, and stance classification."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .utils import (
    DerivedSignal,
    Metric,
    format_number,
    metric_map,
    read_tga_history,
    safe_float,
)


def spread_value(a: Optional[Metric], b: Optional[Metric]) -> Optional[float]:
    if not a or not b or a.value is None or b.value is None:
        return None
    return (a.value - b.value) * 100.0


def previous_spread_value(a: Optional[Metric], b: Optional[Metric]) -> Optional[float]:
    if not a or not b or a.previous is None or b.previous is None:
        return None
    return (a.previous - b.previous) * 100.0


def value_change(m: Optional[Metric]) -> Optional[float]:
    if not m or m.change is None:
        return None
    return m.change


def classify_bp(value: Optional[float], tight: float, loose: Optional[float] = None) -> Tuple[str, str]:
    if value is None:
        return "missing", "缺失"
    if value >= tight:
        return "tight", "偏紧"
    if loose is not None and value <= loose:
        return "loose", "偏松"
    return "neutral", "中性"


def derive_signals(metrics: List[Metric]) -> Tuple[List[DerivedSignal], float, List[str]]:
    mm = metric_map(metrics)
    signals: List[DerivedSignal] = []
    score = 0.0
    highlights: List[str] = []

    def add_signal(signal_id: str, name: str, value: Optional[float], unit: str, interpretation: str, severity: str, score_delta: float = 0.0, previous: Optional[float] = None) -> None:
        nonlocal score
        change = value - previous if value is not None and previous is not None else None
        signals.append(DerivedSignal(signal_id, name, value, unit, interpretation, severity, previous, change))
        score += score_delta
        if severity in {"偏紧", "紧张", "偏松"}:
            val = "缺失" if value is None else f"{value:.2f}{unit}"
            prev = "NA" if previous is None else f"{previous:.2f}{unit}"
            chg = "NA" if change is None else f"{change:+.2f}{unit}"
            highlights.append(f"{name}: 当前 {val}，上一期 {prev}，边际变化 {chg}，{interpretation}")

    policy_anchor = mm.get("IORB") if mm.get("IORB") and mm.get("IORB").value is not None else mm.get("POLICY_UPPER_NYFED") or mm.get("DFEDTARU")
    anchor_label = "IORB（准备金余额利率）" if policy_anchor and policy_anchor.id == "IORB" else "Policy Anchor（政策锚）"
    sofr_anchor_label = "SOFR-IORB（担保隔夜融资利率-准备金余额利率）" if policy_anchor and policy_anchor.id == "IORB" else "SOFR-Policy Anchor（担保隔夜融资利率-政策锚）"

    sofr_anchor = spread_value(mm.get("SOFR"), policy_anchor)
    sofr_anchor_prev = previous_spread_value(mm.get("SOFR"), policy_anchor)
    sev_key, sev = classify_bp(sofr_anchor, 0.0, -8.0)
    add_signal("SOFR_ANCHOR", sofr_anchor_label, sofr_anchor, "bp", f"SOFR相对{anchor_label}的位置。" + ("回购融资高于政策锚，抵押融资压力上升" if sev_key == "tight" else "回购融资低于政策锚，说明资金面不紧" if sev_key == "loose" else "回购融资与政策锚接近"), sev, 1.5 if sev_key == "tight" else -0.5 if sev_key == "loose" else 0.0, previous=sofr_anchor_prev)

    sofr_volume = mm.get("SOFR_VOLUME")
    if sofr_volume and sofr_volume.value is not None and sofr_anchor is not None:
        impact_mn_day = sofr_volume.value * sofr_anchor / 10_000.0 / 360.0 * 1_000.0
        impact_prev = None
        if sofr_volume.previous is not None and sofr_anchor_prev is not None:
            impact_prev = sofr_volume.previous * sofr_anchor_prev / 10_000.0 / 360.0 * 1_000.0
        if impact_mn_day >= 5.0:
            impact_sev = "偏紧"
            impact_score = 0.6
            impact_text = f"SOFR交易量约{sofr_volume.value:,.0f}bn，SOFR相对政策锚为{sofr_anchor:.1f}bp，价格偏离作用在大体量回购融资上，日化额外成本约{impact_mn_day:.1f}百万美元。"
        elif impact_mn_day <= -5.0:
            impact_sev = "偏松"
            impact_score = -0.3
            impact_text = f"SOFR交易量约{sofr_volume.value:,.0f}bn，SOFR低于政策锚，按交易量估算日化融资成本低于政策锚约{abs(impact_mn_day):.1f}百万美元。"
        else:
            impact_sev = "中性"
            impact_score = 0.0
            impact_text = f"SOFR交易量约{sofr_volume.value:,.0f}bn，但SOFR相对政策锚偏离有限，价格×规模冲击不大。"
        add_signal("SOFR_VOLUME_IMPACT", "SOFR Rate-Volume Impact（SOFR价格×交易量影响）", impact_mn_day, "USD mn/day", impact_text, impact_sev, impact_score, previous=impact_prev)

    bgcr_tgcr = spread_value(mm.get("BGCR"), mm.get("TGCR"))
    bgcr_tgcr_prev = previous_spread_value(mm.get("BGCR"), mm.get("TGCR"))
    sev_key, sev = classify_bp(bgcr_tgcr, 3.0)
    add_signal("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）", bgcr_tgcr, "bp", "比较广义回购与三方回购的结构差异。" + ("一般抵押品市场结构可能有扰动" if sev_key == "tight" else "一般抵押品利率结构稳定"), sev, 0.5 if sev_key == "tight" else 0.0, previous=bgcr_tgcr_prev)

    cp_spread = spread_value(mm.get("DCPN3M"), mm.get("DFEDTARU"))
    cp_spread_prev = previous_spread_value(mm.get("DCPN3M"), mm.get("DFEDTARU"))
    sev_key, sev = classify_bp(cp_spread, 30.0, 0.0)
    add_signal("CP_PROXY", "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）", cp_spread, "bp", "用90天AA非金融商业票据利率减联邦基金目标上限，粗略观察企业短融相对政策利率是否变贵；这是信用传导代理指标，不是FRA-OIS。" + ("企业短期融资压力偏高" if sev_key == "tight" else "企业短融压力不明显" if sev_key == "loose" else "企业短融压力中性"), sev, 1.0 if sev_key == "tight" else -0.3 if sev_key == "loose" else 0.0, previous=cp_spread_prev)

    tga = mm.get("TGA")
    tga_change = value_change(tga)
    tga_change_prev = None
    if tga and tga.previous is not None and tga.previous_as_of:
        history = read_tga_history(90)
        for i, (d, v) in enumerate(history):
            if d == tga.previous_as_of and i > 0:
                tga_change_prev = tga.previous - history[i - 1][1]
                break

    if tga_change is not None:
        if tga_change > 50:
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政部现金余额上升，短期抽走准备金", "偏紧", 1.0, previous=tga_change_prev)
        elif tga_change < -50:
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政部现金余额下降，短期释放准备金", "偏松", -1.0, previous=tga_change_prev)
        else:
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政资金流变化不大", "中性", 0.0, previous=tga_change_prev)

    rrp = mm.get("RRPONTSYD")
    if rrp and rrp.value is not None:
        if rrp.value < 200:
            add_signal("RRP_LEVEL", "RRP Balance（隔夜逆回购余额）", rrp.value, "bn", "RRP缓冲垫接近低位，后续冲击更容易落到准备金", "偏紧", 1.0, previous=rrp.previous)
        elif rrp.change is not None and rrp.change < -25:
            add_signal("RRP_LEVEL", "RRP Balance（隔夜逆回购余额）", rrp.value, "bn", "RRP继续下降，缓冲释放但可用垫子减少", "中性", 0.0, previous=rrp.previous)
        else:
            add_signal("RRP_LEVEL", "RRP Balance（隔夜逆回购余额）", rrp.value, "bn", "RRP仍可作为缓冲观察", "中性", 0.0, previous=rrp.previous)

    dgs1 = mm.get("DGS1")
    if dgs1 and dgs1.value is not None:
        if dgs1.value >= 4.5:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "近端政策路径收益率较高，现金和短债收益对风险资产形成分流", "偏紧", 0.4, previous=dgs1.previous)
        elif dgs1.value <= 2.0:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "近端政策路径收益率偏低，风险资产资金分流压力较小", "偏松", -0.2, previous=dgs1.previous)
        else:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价", "中性", 0.0, previous=dgs1.previous)

    dgs10 = mm.get("DGS10")
    if dgs10 and dgs10.change is not None:
        dgs10_chg_bp = dgs10.change * 100.0
        if dgs10_chg_bp > 6:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率上行，债券久期和股票估值承压", "偏紧", 0.6, previous=dgs10.previous)
        elif dgs10_chg_bp < -6:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率下行，久期资产估值压力缓和", "偏松", -0.3, previous=dgs10.previous)
        else:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率边际变化有限", "中性", 0.0, previous=dgs10.previous)

    real_10y = mm.get("DFII10")
    if real_10y and real_10y.value is not None:
        real_chg_bp = real_10y.change * 100.0 if real_10y.change is not None else 0.0
        if real_10y.value >= 2.0 or real_chg_bp > 5:
            add_signal("REAL_10Y", "10Y Real Yield（10年期TIPS实际收益率）", real_10y.value, "%", "真实无风险回报偏高或边际上行，成长股、黄金和长期资产估值压力上升", "偏紧", 0.8, previous=real_10y.previous)
        elif real_chg_bp < -5:
            add_signal("REAL_10Y", "10Y Real Yield（10年期TIPS实际收益率）", real_10y.value, "%", "真实贴现率回落，长期资产估值压力缓和", "偏松", -0.4, previous=real_10y.previous)
        else:
            add_signal("REAL_10Y", "10Y Real Yield（10年期TIPS实际收益率）", real_10y.value, "%", "真实贴现率变化有限", "中性", 0.0, previous=real_10y.previous)

    hy = mm.get("BAMLH0A0HYM2")
    if hy and hy.change is not None:
        hy_chg_bp = hy.change * 100.0
        if hy_chg_bp > 5:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用压力向风险资产扩散", "偏紧", 1.0, previous=hy.previous)
        elif hy_chg_bp < -5:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用风险偏好改善", "偏松", -0.5, previous=hy.previous)
        else:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用利差变化有限", "中性", 0.0, previous=hy.previous)

    ig = mm.get("BAMLC0A0CM")
    if ig and ig.change is not None:
        ig_chg_bp = ig.change * 100.0
        if ig_chg_bp > 3:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "高等级企业融资风险溢价上行，信用条件边际收紧", "偏紧", 0.6, previous=ig.previous)
        elif ig_chg_bp < -3:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "投资级信用利差收窄，企业融资条件边际改善", "偏松", -0.3, previous=ig.previous)
        else:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "投资级信用利差变化有限", "中性", 0.0, previous=ig.previous)

    vix = mm.get("VIXCLS")
    if vix and vix.value is not None:
        if vix.value >= 25 or (vix.change is not None and vix.change > 2.0):
            add_signal("VIX_RISK", "VIX（标普500隐含波动率指数）", vix.value, "", "证券市场避险需求上升，风险偏好降温", "偏紧", 0.6, previous=vix.previous)
        elif vix.value <= 15 or (vix.change is not None and vix.change < -2.0):
            add_signal("VIX_RISK", "VIX（标普500隐含波动率指数）", vix.value, "", "证券市场波动率较低或回落，风险偏好相对稳定", "偏松", -0.3, previous=vix.previous)
        else:
            add_signal("VIX_RISK", "VIX（标普500隐含波动率指数）", vix.value, "", "证券市场波动率处于中性区间", "中性", 0.0, previous=vix.previous)

    usd = mm.get("DTWEXBGS")
    if usd and usd.change is not None:
        if usd.change > 0.3:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "离岸美元融资条件可能收紧", "偏紧", 0.8)
        elif usd.change < -0.3:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "外部美元压力缓和", "偏松", -0.5)
        else:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "离岸美元代理指标变化有限", "中性", 0.0)

    curve_10y2y = mm.get("T10Y2Y")
    if curve_10y2y and curve_10y2y.value is not None:
        value_bp = curve_10y2y.value * 100.0
        previous_bp = curve_10y2y.previous * 100.0 if curve_10y2y.previous is not None else None
        if value_bp < -50:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线深度倒挂，市场隐含未来降息/增长走弱预期较强", "偏紧", 0.8, previous=previous_bp)
        elif value_bp < 0:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线仍倒挂，反映政策短端较紧和未来增长/降息预期", "中性", 0.2, previous=previous_bp)
        else:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线为正，期限结构相对正常", "中性", 0.0, previous=previous_bp)

    curve_10y3m = mm.get("T10Y3M")
    if curve_10y3m and curve_10y3m.value is not None:
        value_bp = curve_10y3m.value * 100.0
        previous_bp = curve_10y3m.previous * 100.0 if curve_10y3m.previous is not None else None
        if value_bp < -100:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线深度倒挂，衰退和后续降息预期较强", "偏紧", 0.8, previous=previous_bp)
        elif value_bp < 0:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线倒挂，短端政策利率仍高于长期增长预期", "中性", 0.2, previous=previous_bp)
        else:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线为正，政策短端对长期利率压制较弱", "中性", 0.0, previous=previous_bp)

    nfci = mm.get("NFCI")
    if nfci and nfci.value is not None:
        if nfci.value > 0.25:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理显示金融条件偏紧；它不是高盛FCI，但可作为免费公开替代观察", "偏紧", 0.8, previous=nfci.previous)
        elif nfci.value < -0.25:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察", "偏松", -0.5, previous=nfci.previous)
        else:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理接近均值，金融条件整体中性", "中性", 0.0, previous=nfci.previous)

    tbill_size = mm.get("TBILL_AUCTION_SIZE")
    tbill_btc = mm.get("TBILL_AUCTION_BTC")
    if tbill_size and tbill_btc and tbill_size.value is not None and tbill_btc.value is not None:
        btc_prev = f"，上一T-bill拍卖日认购倍数 {tbill_btc.previous:.2f}x" if tbill_btc.previous is not None else ""
        if tbill_btc.value < 2.3 or (tbill_size.value >= 180.0 and tbill_btc.value < 2.6):
            add_signal("TBILL_AUCTION_ABSORPTION", "T-bill Auction Absorption（短债拍卖吸收压力）", tbill_size.value, "USD bn", f"最新T-bill拍卖规模约{tbill_size.value:,.1f}bn，认购倍数{tbill_btc.value:.2f}x{btc_prev}；规模较大且需求不强，可能占用货币基金/交易商资产负债表。", "偏紧", 0.7, previous=tbill_size.previous)
        elif tbill_btc.value >= 3.0:
            add_signal("TBILL_AUCTION_ABSORPTION", "T-bill Auction Absorption（短债拍卖吸收压力）", tbill_size.value, "USD bn", f"最新T-bill拍卖规模约{tbill_size.value:,.1f}bn，认购倍数{tbill_btc.value:.2f}x{btc_prev}；需求覆盖较强，短债吸收压力不明显。", "偏松", -0.2, previous=tbill_size.previous)
        else:
            add_signal("TBILL_AUCTION_ABSORPTION", "T-bill Auction Absorption（短债拍卖吸收压力）", tbill_size.value, "USD bn", f"最新T-bill拍卖规模约{tbill_size.value:,.1f}bn，认购倍数{tbill_btc.value:.2f}x{btc_prev}；供给吸收处于中性区间。", "中性", 0.0, previous=tbill_size.previous)

    auction = mm.get("UST_AUCTION_BTC")
    if auction and auction.value is not None:
        if auction.value < 2.2:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求偏弱，国债吸收能力需关注", "偏紧", 0.8)
        elif auction.value > 2.8:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求较强，吸收压力不明显", "偏松", -0.3)
        else:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求中性", "中性", 0.0)

    return signals, score, highlights


def stance_from_score(score: float) -> str:
    if score >= 5.0:
        return "紧张"
    if score >= 2.5:
        return "中性偏紧"
    if score <= -2.0:
        return "宽松"
    if score <= -0.8:
        return "中性偏松"
    return "中性"
