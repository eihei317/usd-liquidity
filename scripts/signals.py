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

    def add_signal(signal_id: str, name: str, value: Optional[float], unit: str, interpretation: str, severity: str, score_delta: float = 0.0, previous: Optional[float] = None, as_of: Optional[str] = None) -> None:
        nonlocal score
        change = value - previous if value is not None and previous is not None else None
        signals.append(DerivedSignal(signal_id, name, value, unit, interpretation, severity, previous, change, as_of))
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
    sofr_as_of = mm.get("SOFR").as_of if mm.get("SOFR") else None  # 从底层metric继承时间
    sev_key, sev = classify_bp(sofr_anchor, 0.0, -8.0)
    add_signal("SOFR_ANCHOR", sofr_anchor_label, sofr_anchor, "bp", f"SOFR相对{anchor_label}的位置。" + ("回购融资高于政策锚，抵押融资压力上升" if sev_key == "tight" else "回购融资低于政策锚，说明资金面不紧" if sev_key == "loose" else "回购融资与政策锚接近"), sev, 1.5 if sev_key == "tight" else -0.5 if sev_key == "loose" else 0.0, previous=sofr_anchor_prev, as_of=sofr_as_of)

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
        add_signal("SOFR_VOLUME_IMPACT", "SOFR Rate-Volume Impact（SOFR价格×交易量影响）", impact_mn_day, "USD mn/day", impact_text, impact_sev, impact_score, previous=impact_prev, as_of=sofr_volume.as_of)

    bgcr_tgcr = spread_value(mm.get("BGCR"), mm.get("TGCR"))
    bgcr_tgcr_prev = previous_spread_value(mm.get("BGCR"), mm.get("TGCR"))
    bgcr_as_of = mm.get("BGCR").as_of if mm.get("BGCR") else None
    sev_key, sev = classify_bp(bgcr_tgcr, 3.0)
    add_signal("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）", bgcr_tgcr, "bp", "比较广义回购与三方回购的结构差异。" + ("一般抵押品市场结构可能有扰动" if sev_key == "tight" else "一般抵押品利率结构稳定"), sev, 0.5 if sev_key == "tight" else 0.0, previous=bgcr_tgcr_prev, as_of=bgcr_as_of)

    cp_spread = spread_value(mm.get("DCPN3M"), mm.get("DFEDTARU"))
    cp_spread_prev = previous_spread_value(mm.get("DCPN3M"), mm.get("DFEDTARU"))
    dcpn_as_of = mm.get("DCPN3M").as_of if mm.get("DCPN3M") else None
    sev_key, sev = classify_bp(cp_spread, 30.0, 0.0)
    add_signal("CP_PROXY", "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）", cp_spread, "bp", "用90天AA非金融商业票据利率减联邦基金目标上限，粗略观察企业短融相对政策利率是否变贵；这是信用传导代理指标，不是FRA-OIS。" + ("企业短期融资压力偏高" if sev_key == "tight" else "企业短融压力不明显" if sev_key == "loose" else "企业短融压力中性"), sev, 1.0 if sev_key == "tight" else -0.3 if sev_key == "loose" else 0.0, previous=cp_spread_prev, as_of=dcpn_as_of)

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
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政部现金余额上升，短期抽走准备金", "偏紧", 1.0, previous=tga_change_prev, as_of=tga.as_of)
        elif tga_change < -50:
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政部现金余额下降，短期释放准备金", "偏松", -1.0, previous=tga_change_prev, as_of=tga.as_of)
        else:
            add_signal("TGA_FLOW", "TGA Daily Change（财政部一般账户日变化）", tga_change, "bn", "财政资金流变化不大", "中性", 0.0, previous=tga_change_prev, as_of=tga.as_of)

    rrp = mm.get("RRPONTSYD")
    if rrp and rrp.value is not None:
        # RRP必须拆分为边际流量和存量缓冲垫：下降短期偏释放流动性，但低存量代表未来抗冲击能力下降。
        if rrp.change is not None:
            if rrp.change > 25:
                rrp_flow_sev = "偏紧"
                rrp_flow_score = 0.4
                rrp_flow_text = "RRP上升代表资金回到联储停车场，短期对风险资产边际偏紧。"
            elif rrp.change < -25:
                rrp_flow_sev = "偏松"
                rrp_flow_score = -0.4
                rrp_flow_text = "RRP下降代表资金从联储停车场出来，短期边际释放流动性。"
            else:
                rrp_flow_sev = "中性"
                rrp_flow_score = 0.0
                rrp_flow_text = "RRP日变化幅度有限，短期边际流量影响不大。"
            add_signal("RRP_FLOW", "RRP Flow（隔夜逆回购边际流量）", rrp.change, "bn", rrp_flow_text, rrp_flow_sev, rrp_flow_score, previous=None, as_of=rrp.as_of)

        if rrp.value < 50:
            add_signal("RRP_BUFFER", "RRP Buffer（隔夜逆回购存量缓冲垫）", rrp.value, "bn", "RRP存量缓冲垫几乎耗尽，后续TGA补库、QT或美债供给冲击更容易直接落到准备金。", "偏紧", 1.2, previous=rrp.previous, as_of=rrp.as_of)
        elif rrp.value < 200:
            add_signal("RRP_BUFFER", "RRP Buffer（隔夜逆回购存量缓冲垫）", rrp.value, "bn", "RRP缓冲垫偏低，未来冲击更容易落到准备金。", "偏紧", 0.8, previous=rrp.previous, as_of=rrp.as_of)
        else:
            add_signal("RRP_BUFFER", "RRP Buffer（隔夜逆回购存量缓冲垫）", rrp.value, "bn", "RRP仍可作为非银现金缓冲垫观察。", "中性", 0.0, previous=rrp.previous, as_of=rrp.as_of)

    dgs1 = mm.get("DGS1")
    if dgs1 and dgs1.value is not None:
        if dgs1.value >= 4.5:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "近端政策路径收益率较高，现金和短债收益对风险资产形成分流", "偏紧", 0.4, previous=dgs1.previous, as_of=dgs1.as_of)
        elif dgs1.value <= 2.0:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "近端政策路径收益率偏低，风险资产资金分流压力较小", "偏松", -0.2, previous=dgs1.previous, as_of=dgs1.as_of)
        else:
            add_signal("UST_1Y_YIELD", "1Y Treasury Yield（1年期美国国债收益率）", dgs1.value, "%", "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价", "中性", 0.0, previous=dgs1.previous, as_of=dgs1.as_of)

    dgs3 = mm.get("DGS3")
    if dgs3 and dgs3.value is not None:
        if dgs3.value >= 4.5:
            add_signal("UST_3Y_YIELD", "3Y Treasury Yield（3年期美国国债收益率）", dgs3.value, "%", "3年期收益率处于高位，说明政策路径压力向中段扩散。", "偏紧", 0.3, previous=dgs3.previous, as_of=dgs3.as_of)
        elif dgs3.value <= 3.0:
            add_signal("UST_3Y_YIELD", "3Y Treasury Yield（3年期美国国债收益率）", dgs3.value, "%", "3年期收益率处于较低区间，中段再定价压力较小。", "偏松", -0.2, previous=dgs3.previous, as_of=dgs3.as_of)
        else:
            add_signal("UST_3Y_YIELD", "3Y Treasury Yield（3年期美国国债收益率）", dgs3.value, "%", "3年期收益率处于中间区间，观察其相对1年和10年的斜率变化。", "中性", 0.0, previous=dgs3.previous, as_of=dgs3.as_of)

    dgs10 = mm.get("DGS10")
    if dgs10 and dgs10.change is not None:
        dgs10_chg_bp = dgs10.change * 100.0
        if dgs10_chg_bp > 6:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率上行，债券久期和股票估值承压", "偏紧", 0.6, previous=dgs10.previous, as_of=dgs10.as_of)
        elif dgs10_chg_bp < -6:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率下行，久期资产估值压力缓和", "偏松", -0.3, previous=dgs10.previous, as_of=dgs10.as_of)
        else:
            add_signal("NOMINAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", dgs10.value, "%", "长期名义折现率边际变化有限", "中性", 0.0, previous=dgs10.previous, as_of=dgs10.as_of)

    real_10y = mm.get("DGS10")
    if real_10y and real_10y.value is not None:
        real_chg_bp = real_10y.change * 100.0 if real_10y.change is not None else None
        if real_10y.value >= 4.5:
            add_signal("REAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", real_10y.value, "%", "10年期国债收益率处于高位，对长期资产估值有压力；这描述的是level风险，不代表边际继续恶化。", "偏紧", 0.5, previous=real_10y.previous, as_of=real_10y.as_of)
        elif real_10y.value <= 3.5:
            add_signal("REAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", real_10y.value, "%", "10年期国债收益率处于较低区间，长期资产估值压力较小。", "偏松", -0.2, previous=real_10y.previous, as_of=real_10y.as_of)
        else:
            add_signal("REAL_10Y", "10Y Treasury Yield（10年期美国国债收益率）", real_10y.value, "%", "10年期国债收益率处于中间区间。", "中性", 0.0, previous=real_10y.previous, as_of=real_10y.as_of)
        if real_chg_bp is not None:
            if real_chg_bp > 5:
                add_signal("REAL_10Y_MOMENTUM", "10Y Yield Momentum（10年期国债收益率边际变化）", real_chg_bp, "bp", "10年期国债收益率边际上行，长期资产估值压力正在增强。", "偏紧", 0.4, previous=None, as_of=real_10y.as_of)
            elif real_chg_bp < -5:
                add_signal("REAL_10Y_MOMENTUM", "10Y Yield Momentum（10年期国债收益率边际变化）", real_chg_bp, "bp", "10年期国债收益率边际下行，长期资产估值压力正在缓和。", "偏松", -0.4, previous=None, as_of=real_10y.as_of)
            else:
                add_signal("REAL_10Y_MOMENTUM", "10Y Yield Momentum（10年期国债收益率边际变化）", real_chg_bp, "bp", "10年期国债收益率边际变化有限。", "中性", 0.0, previous=None, as_of=real_10y.as_of)

    hy = mm.get("BAMLH0A0HYM2")
    if hy and hy.change is not None:
        hy_chg_bp = hy.change * 100.0
        if hy_chg_bp > 5:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用压力向风险资产扩散", "偏紧", 1.0, previous=hy.previous, as_of=hy.as_of)
        elif hy_chg_bp < -5:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用风险偏好改善", "偏松", -0.5, previous=hy.previous, as_of=hy.as_of)
        else:
            add_signal("HY_CHANGE", "HY OAS Change（高收益债期权调整利差变化）", hy.value, "%", "信用利差变化有限", "中性", 0.0, previous=hy.previous, as_of=hy.as_of)

    ig = mm.get("BAMLC0A0CM")
    if ig and ig.change is not None:
        ig_chg_bp = ig.change * 100.0
        if ig_chg_bp > 3:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "高等级企业融资风险溢价上行，信用条件边际收紧", "偏紧", 0.6, previous=ig.previous, as_of=ig.as_of)
        elif ig_chg_bp < -3:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "投资级信用利差收窄，企业融资条件边际改善", "偏松", -0.3, previous=ig.previous, as_of=ig.as_of)
        else:
            add_signal("IG_CHANGE", "IG OAS Change（投资级公司债期权调整利差变化）", ig.value, "%", "投资级信用利差变化有限", "中性", 0.0, previous=ig.previous, as_of=ig.as_of)

    vix = mm.get("VIXCLS")
    if vix and vix.value is not None:
        if vix.value >= 25:
            add_signal("VIX_RISK", "VIX Level（标普500隐含波动率水平）", vix.value, "", "证券市场避险需求处于偏高水平，风险偏好承压；这是level风险。", "偏紧", 0.5, previous=vix.previous, as_of=vix.as_of)
        elif vix.value <= 15:
            add_signal("VIX_RISK", "VIX Level（标普500隐含波动率水平）", vix.value, "", "证券市场波动率处于低位，风险偏好相对稳定。", "偏松", -0.2, previous=vix.previous, as_of=vix.as_of)
        else:
            add_signal("VIX_RISK", "VIX Level（标普500隐含波动率水平）", vix.value, "", "证券市场波动率处于中性区间。", "中性", 0.0, previous=vix.previous, as_of=vix.as_of)
        if vix.change is not None:
            if vix.change > 2.0:
                add_signal("VIX_MOMENTUM", "VIX Momentum（标普500隐含波动率边际变化）", vix.change, "pt", "VIX边际上行，说明股票风险偏好正在降温；若信用利差同步扩大才说明压力进一步传导到信用融资。", "偏紧", 0.4, previous=None, as_of=vix.as_of)
            elif vix.change < -2.0:
                add_signal("VIX_MOMENTUM", "VIX Momentum（标普500隐含波动率边际变化）", vix.change, "pt", "VIX边际回落，说明股票风险偏好改善。", "偏松", -0.3, previous=None, as_of=vix.as_of)
            else:
                add_signal("VIX_MOMENTUM", "VIX Momentum（标普500隐含波动率边际变化）", vix.change, "pt", "VIX边际变化有限。", "中性", 0.0, previous=None, as_of=vix.as_of)

    usd = mm.get("DTWEXBGS")
    if usd and usd.change is not None:
        if usd.change > 0.3:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "离岸美元融资条件可能收紧", "偏紧", 0.8, as_of=usd.as_of)
        elif usd.change < -0.3:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "外部美元压力缓和", "偏松", -0.5, as_of=usd.as_of)
        else:
            add_signal("USD_CHANGE", "Broad Dollar Index Change（广义美元指数变化）", usd.change, "pt", "离岸美元代理指标变化有限", "中性", 0.0, as_of=usd.as_of)

    curve_10y2y = mm.get("T10Y2Y")
    if curve_10y2y and curve_10y2y.value is not None:
        value_bp = curve_10y2y.value * 100.0
        previous_bp = curve_10y2y.previous * 100.0 if curve_10y2y.previous is not None else None
        if value_bp < -50:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线深度倒挂，市场隐含未来降息/增长走弱预期较强", "偏紧", 0.8, previous=previous_bp, as_of=curve_10y2y.as_of)
        elif value_bp < 0:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线仍倒挂，反映政策短端较紧和未来增长/降息预期", "中性", 0.2, previous=previous_bp, as_of=curve_10y2y.as_of)
        else:
            add_signal("UST_10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）", value_bp, "bp", "收益率曲线为正，期限结构相对正常", "中性", 0.0, previous=previous_bp, as_of=curve_10y2y.as_of)

    curve_10y3m = mm.get("T10Y3M")
    if curve_10y3m and curve_10y3m.value is not None:
        value_bp = curve_10y3m.value * 100.0
        previous_bp = curve_10y3m.previous * 100.0 if curve_10y3m.previous is not None else None
        if value_bp < -100:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线深度倒挂，衰退和后续降息预期较强", "偏紧", 0.8, previous=previous_bp, as_of=curve_10y3m.as_of)
        elif value_bp < 0:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线倒挂，短端政策利率仍高于长期增长预期", "中性", 0.2, previous=previous_bp, as_of=curve_10y3m.as_of)
        else:
            add_signal("UST_10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）", value_bp, "bp", "10年-3个月曲线为正，政策短端对长期利率压制较弱", "中性", 0.0, previous=previous_bp, as_of=curve_10y3m.as_of)

    nfci = mm.get("NFCI")
    if nfci and nfci.value is not None:
        if nfci.value > 0.25:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理显示金融条件偏紧；它不是高盛FCI，但可作为免费公开替代观察", "偏紧", 0.8, previous=nfci.previous, as_of=nfci.as_of)
        elif nfci.value < -0.25:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察", "偏松", -0.5, previous=nfci.previous, as_of=nfci.as_of)
        else:
            add_signal("NFCI_LEVEL", "NFCI（芝加哥联储全国金融条件指数）", nfci.value, "", "公开金融条件代理接近均值，金融条件整体中性", "中性", 0.0, previous=nfci.previous, as_of=nfci.as_of)

    tbill_size = mm.get("TBILL_AUCTION_SIZE")
    tbill_btc = mm.get("TBILL_AUCTION_BTC")
    if tbill_size and tbill_btc and tbill_size.value is not None and tbill_btc.value is not None:
        def tbill_stress_score(size: Optional[float], btc: Optional[float]) -> Optional[float]:
            if size is None or btc is None:
                return None
            size_score = 35.0 if size >= 180.0 else 25.0 if size >= 140.0 else 15.0 if size >= 100.0 else 5.0
            demand_score = 45.0 if btc < 2.3 else 30.0 if btc < 2.6 else 15.0 if btc < 3.0 else -10.0
            return max(0.0, min(100.0, size_score + demand_score))

        stress = tbill_stress_score(tbill_size.value, tbill_btc.value)
        stress_prev = tbill_stress_score(tbill_size.previous, tbill_btc.previous)
        btc_prev = f"，上一T-bill拍卖日认购倍数 {tbill_btc.previous:.2f}x" if tbill_btc.previous is not None else ""
        stress_text = f"最新T-bill拍卖规模约{tbill_size.value:,.1f}bn，认购倍数{tbill_btc.value:.2f}x{btc_prev}；该分数综合供给规模与需求覆盖，数值越高表示吸收压力越大。"
        if stress is not None and stress >= 55:
            add_signal("TBILL_AUCTION_STRESS", "T-bill Auction Stress Score（短债拍卖吸收压力评分）", stress, "index", stress_text + "当前为偏紧组合，可能占用货币基金/交易商资产负债表。", "偏紧", 0.7, previous=stress_prev, as_of=tbill_size.as_of)
        elif stress is not None and stress <= 15:
            add_signal("TBILL_AUCTION_STRESS", "T-bill Auction Stress Score（短债拍卖吸收压力评分）", stress, "index", stress_text + "需求覆盖较强或供给压力较低，短债吸收压力不明显。", "偏松", -0.2, previous=stress_prev, as_of=tbill_size.as_of)
        else:
            add_signal("TBILL_AUCTION_STRESS", "T-bill Auction Stress Score（短债拍卖吸收压力评分）", stress, "index", stress_text + "供给吸收处于中性区间。", "中性", 0.0, previous=stress_prev, as_of=tbill_size.as_of)

    auction = mm.get("UST_AUCTION_BTC")
    if auction and auction.value is not None:
        if auction.value < 2.2:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求偏弱，国债吸收能力需关注", "偏紧", 0.8, as_of=auction.as_of)
        elif auction.value > 2.8:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求较强，吸收压力不明显", "偏松", -0.3, as_of=auction.as_of)
        else:
            add_signal("AUCTION_BTC", "UST Auction BTC（国债拍卖投标覆盖倍数）", auction.value, "x", "拍卖需求中性", "中性", 0.0, as_of=auction.as_of)

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
