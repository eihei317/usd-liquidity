#!/usr/bin/env python3
"""Fetch recent USD liquidity data and generate a daily briefing.

The script intentionally uses public official/authoritative endpoints only.
It is designed for on-demand natural-language triggering from WorkBuddy.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import io
import json
import math
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
LATEST_DIR = OUTPUT_DIR / "latest"
PROMPT_PATH = ROOT / "prompts" / "usd_liquidity_prompt.md"
INTRO_PATH = ROOT / "prompts" / "usd_liquidity_intro.md"
FRED_API_KEY_PATH = ROOT / ".workbuddy" / "secrets" / "fred_api_key"
TGA_CACHE_PATH = ROOT / ".workbuddy" / "cache" / "tga_cache.json"

BJT = timezone(timedelta(hours=8))
UTC = timezone.utc

USER_AGENT = "WorkBuddy USD Liquidity Monitor/1.0"

UNAVAILABLE_SOURCES = [
    {
        "name": "MOVE Index",
        "reason": "ICE/BofA proprietary index; no free official real-time API found",
        "proxy": "Use Treasury/repo rates, HY spread and auction signals as substitutes",
    },
    {
        "name": "FRA-OIS",
        "reason": "No free official daily API found; usually Bloomberg/Refinitiv",
        "proxy": "Use CP-Fed target proxy and SOFR/EFFR/IORB spreads",
    },
    {
        "name": "True cross-currency basis",
        "reason": "CME/market vendor access generally requires onboarding or paid data",
        "proxy": "Use Fed broad dollar index DTWEXBGS as an offshore USD stress proxy",
    },
    {
        "name": "Real-time Treasury order book depth",
        "reason": "BrokerTec/ICAP depth is proprietary; no free official API",
        "proxy": "Use auction bid-to-cover, repo fails and volatility/funding proxies",
    },
    {
        "name": "Goldman Sachs Financial Conditions Index",
        "reason": "Goldman Sachs FCI is proprietary; no free official public API found",
        "proxy": "Use Chicago Fed NFCI plus rates, credit spreads, dollar index and equity/credit proxies",
    },
]

RATE_LABELS = {
    "EFFR": "EFFR（有效联邦基金利率）",
    "SOFR": "SOFR（担保隔夜融资利率）",
    "IORB": "IORB（准备金余额利率）",
    "POLICY_UPPER_NYFED": "POLICY_UPPER_NYFED（纽约联储政策上限）",
    "DFEDTARU": "DFEDTARU（联邦基金目标区间上限）",
    "OBFR": "OBFR（隔夜银行融资利率）",
    "TGCR": "TGCR（三方一般抵押品利率）",
    "BGCR": "BGCR（广义一般抵押品利率）",
    "TGA": "TGA（财政部一般账户）",
    "RRPONTSYD": "RRP（隔夜逆回购）",
    "SOMA": "SOMA（系统公开市场账户持仓）",
    "WRESBAL": "WRESBAL（银行准备金余额）",
    "UST_AUCTION_BTC": "UST Auction BTC（国债拍卖投标覆盖倍数）",
    "REPO_FAILS_UST": "Repo Fails（美国国债回购交割失败）",
    "DTWEXBGS": "DTWEXBGS（广义美元指数）",
    "DCPN3M": "CP Rate（90天AA非金融商业票据利率）",
    "BAMLH0A0HYM2": "HY OAS（高收益债期权调整利差）",
    "BAMLC0A0CM": "IG OAS（投资级公司债期权调整利差）",
    "DTB3": "3M T-bill Rate（3个月美国国库券二级市场利率）",
    "DGS3MO": "3M Treasury Yield（3个月美国国债收益率）",
    "DGS1": "1Y Treasury Yield（1年期美国国债收益率）",
    "DGS2": "2Y Treasury Yield（2年期美国国债收益率）",
    "DGS3": "3Y Treasury Yield（3年期美国国债收益率）",
    "DGS10": "10Y Treasury Yield（10年期美国国债收益率）",
    "DFII10": "10Y Real Yield（10年期TIPS实际收益率）",
    "DGS30": "30Y Treasury Yield（30年期美国国债收益率）",
    "T10Y2Y": "10Y-2Y Treasury Spread（10年-2年美债利差）",
    "T10Y3M": "10Y-3M Treasury Spread（10年-3个月美债利差）",
    "VIXCLS": "VIX（标普500隐含波动率指数）",
    "NFCI": "NFCI（芝加哥联储全国金融条件指数）",
}

RATE_MEANINGS = {
    "EFFR": "银行间无抵押隔夜资金价格，最能观察准备金边际是否稀缺。",
    "SOFR": "以美国国债为抵押的隔夜融资价格，反映回购市场和抵押品融资压力。",
    "IORB": "美联储支付给银行准备金的利率，是银行持有准备金的政策锚。",
    "POLICY_UPPER_NYFED": "纽约联储记录中的政策利率上限；当 IORB/FRED 不可用时，用作临时政策锚。",
    "DFEDTARU": "联邦基金目标区间上限，是政策利率走廊的上沿参考。",
    "OBFR": "更广义的银行隔夜融资成本，观察压力是否从联邦基金市场扩散。",
    "TGCR": "三方回购市场的一般抵押品融资成本，反映机构化回购资金价格。",
    "BGCR": "覆盖更广的一般抵押品回购利率，观察回购市场结构性扰动。",
    "TGA": "财政部现金余额，余额上升通常抽走银行体系准备金，下降通常释放准备金。",
    "RRPONTSYD": "货币基金等机构停放在美联储的隔夜逆回购余额，是准备金压力前的缓冲垫。",
    "SOMA": "美联储公开市场账户持仓，反映QT和资产端收缩的结构背景。",
    "WRESBAL": "银行体系准备金余额，是美元流动性水位的核心变量，但发布频率较低。",
    "UST_AUCTION_BTC": "国债拍卖需求强弱代理指标，观察国债供给吸收能力。",
    "REPO_FAILS_UST": "回购和证券交割失败规模，观察抵押品链条和交割压力。",
    "DTWEXBGS": "广义美元指数，作为离岸美元融资压力的替代观察。",
    "DCPN3M": "企业短期融资价格，观察货币市场压力是否传导到商业票据。",
    "BAMLH0A0HYM2": "高收益债信用利差，观察压力是否外溢到风险信用资产。",
    "BAMLC0A0CM": "投资级公司债信用利差，观察高等级企业融资成本和信用风险溢价。",
    "DTB3": "3个月国库券二级市场利率，代表现金/货币基金可获得的短端无风险替代收益。",
    "DGS3MO": "3个月美国国债收益率，主要受当前政策利率和短端美元资金价格影响。",
    "DGS1": "1年期美国国债收益率，主要反映未来一年政策利率路径和短端再定价。",
    "DGS2": "2年期美国国债收益率，主要反映未来数年美联储政策路径预期。",
    "DGS3": "3年期美国国债收益率，观察政策路径从短端向中段扩散的再定价。",
    "DGS10": "10年期美国国债收益率，是全球资产折现率和长期美元资金价格的重要锚。",
    "DFII10": "10年期TIPS实际收益率，剔除通胀补偿后观察真实无风险回报，对成长股、黄金和长期资产估值更敏感。",
    "DGS30": "30年期美国国债收益率，反映长期通胀、财政供给和期限溢价。",
    "T10Y2Y": "10年减2年美债利差，观察收益率曲线是否倒挂以及增长/降息预期。",
    "T10Y3M": "10年减3个月美债利差，观察政策短端与长期增长预期的差异。",
    "VIXCLS": "标普500隐含波动率指数，作为证券市场风险偏好和避险需求的确认指标。",
    "NFCI": "芝加哥联储全国金融条件指数，公开金融条件代理；正值偏紧，负值偏松。",
}

RATE_CHANGE_IMPLICATIONS = {
    "EFFR": ("银行间无抵押融资边际变贵，准备金稀缺压力上升", "银行间无抵押融资边际变便宜，准备金仍较充裕"),
    "SOFR": ("回购融资边际变贵，抵押融资压力上升", "回购融资边际变便宜，资金面不紧"),
    "IORB": ("政策锚上移，整体短端利率中枢抬升", "政策锚下移，整体短端利率中枢回落"),
    "POLICY_UPPER_NYFED": ("政策上限上移，短端利率中枢抬升", "政策上限下移，短端利率中枢回落"),
    "DFEDTARU": ("政策上限上移，短端利率中枢抬升", "政策上限下移，短端利率中枢回落"),
    "OBFR": ("银行隔夜融资边际变贵，压力可能扩散到更广义融资市场", "银行隔夜融资边际变便宜，广义银行融资压力缓和"),
    "TGCR": ("三方回购融资边际变贵，抵押融资压力上升", "三方回购融资边际变便宜，抵押融资压力缓和"),
    "BGCR": ("广义回购融资边际变贵，回购链条压力上升", "广义回购融资边际变便宜，回购链条压力缓和"),
}

DATA_FREQUENCY_RULES = {
    "EFFR": ("日频，纽约联储约 9:00 ET 发布", "反映上一工作日交易", "与上一条有效工作日观测比较，不按自然日补零。"),
    "OBFR": ("日频，纽约联储参考利率", "通常反映上一工作日交易", "与上一条有效工作日观测比较。"),
    "SOFR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日回购交易，约 14:30 ET 可能同日修订", "与上一条有效工作日观测比较。"),
    "TGCR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日三方回购交易，可能同日修订", "与上一条有效工作日观测比较。"),
    "BGCR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日广义一般抵押品回购交易，可能同日修订", "与上一条有效工作日观测比较。"),
    "TGA": ("日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布", "覆盖上一工作日财政现金和债务操作", "与上一条有效工作日观测比较，不能与当天市场利率强行同日对齐。"),
    "RRPONTSYD": ("日频，纽约联储每日操作结果", "同日操作结果，工作日/操作日口径", "与上一条操作日观测比较。"),
    "SOMA": ("周频，纽约联储/Fed资产负债表背景数据", "周度持仓或H.4.1口径", "只与上一周比较，不能当作昨日边际变化。"),
    "WRESBAL": ("周频，H.4.1 通常周四 16:30 ET 发布", "反映周度准备金余额", "只与上一周比较，作为结构背景。"),
    "REPO_FAILS_UST": ("周频，OFR/STFM 或一级交易商口径", "交割失败周度背景", "只看周度趋势，不参与日度环比。"),
    "UST_AUCTION_BTC": ("事件驱动，财政部拍卖后公布", "只在拍卖发生时更新", "与上一场可比拍卖比较，不能日度环比。"),
    "DTWEXBGS": ("日频，FRED/美联储美元指数口径", "通常随源数据滞后更新", "与上一条有效观测比较，注意可能比资金利率更滞后。"),
    "DCPN3M": ("日频，商业票据利率", "通常T+1或随源数据更新", "与上一条有效观测比较。"),
    "BAMLH0A0HYM2": ("日频，高收益债OAS", "通常随ICE/BofA数据更新", "与上一条有效观测比较，作为信用传导而非银行间流动性核心。"),
    "BAMLC0A0CM": ("日频，投资级公司债OAS", "通常随ICE/BofA数据更新", "与上一条有效观测比较，作为高等级信用融资条件确认。"),
    "DTB3": ("日频，3个月国库券二级市场利率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看现金替代收益。"),
    "DGS3MO": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看政策短端。"),
    "DGS1": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看未来一年政策路径。"),
    "DGS2": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看政策路径预期。"),
    "DGS3": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看中段政策路径再定价。"),
    "DGS10": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看长期折现率。"),
    "DFII10": ("日频，FRED/H.15 10年期TIPS实际收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看真实贴现率。"),
    "DGS30": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看长期期限溢价。"),
    "T10Y2Y": ("日频，FRED曲线利差", "由10年和2年国债收益率差计算", "与上一条有效观测比较；倒挂或加深倒挂反映增长/降息预期。"),
    "T10Y3M": ("日频，FRED曲线利差", "由10年和3个月国债收益率差计算", "与上一条有效观测比较；常用于观察衰退预期。"),
    "VIXCLS": ("日频，标普500隐含波动率", "通常随CBOE/FRED数据更新", "与上一条有效观测比较，作为证券市场风险偏好确认。"),
    "NFCI": ("周频，芝加哥联储全国金融条件指数", "通常每周更新", "只与上一周比较；正值偏紧，负值偏松。"),
    "IORB": ("政策阶梯型，美联储政策利率", "只有政策调整时变化", "不做普通日度环比；用于锚定EFFR和SOFR。"),
    "DFEDTARU": ("政策阶梯型，联邦基金目标上限", "只有政策调整时变化", "不做普通日度环比；用于政策锚。"),
    "POLICY_UPPER_NYFED": ("政策阶梯型，纽约联储记录中的目标上限", "来自EFFR记录，作为IORB缺失时的临时锚", "只用于锚定，不代表市场日度变化。"),
}

CORE_INDICATOR_IMPACTS = [
    # EFFR-IORB 已移除：GSE结构性压低，SOFR-IORB 是更优指标
    # SOFR_EFFR 已移除：日常监测价值有限
    ("SOFR-IORB / SOFR-政策锚", "高", "观察回购和抵押品融资是否紧张；SOFR高于政策锚通常比单纯上升更重要。"),
    ("TGA", "高", "财政部现金余额上升会抽走准备金，下降会释放准备金，是Fed负债端最重要的日频水位之一。"),
    ("RRP", "高", "RRP下降可释放缓冲，但余额过低后，QT和TGA补库更容易直接冲击准备金。"),
    ("WRESBAL", "高但周频", "银行准备金本身是核心水位，但周频发布，适合看趋势而非日内或日度拐点。"),
    ("TGCR/BGCR", "中高", "帮助确认SOFR变化是否是广泛回购市场压力，而非单点噪音。"),
    ("国债拍卖 bid-to-cover / repo fails", "中", "观察国债供给吸收和交割压力，通常作为抵押品链条背景。"),
    ("1Y / 3Y / 10Y国债收益率", "中高", "1年期看近端政策路径，3年期看中段再定价，10年期是全球折现率锚。"),
    ("10Y实际收益率", "高", "真实无风险回报直接影响成长股、黄金和长期资产估值，是证券市场贴现率压力的核心代理。"),
    ("美元指数 / CP利差 / IG OAS / HY OAS", "中高", "观察压力是否向离岸美元和信用市场扩散，属于传导确认指标。"),
    ("10Y-2Y / 10Y-3M曲线利差", "中高", "长短端利差观察当前政策短端与增长、降息和衰退预期的相对关系。"),
    ("VIX / NFCI / FCI代理", "中", "观察利率、信用、杠杆和风险资产综合后的证券市场风险偏好与金融条件。"),
]


@dataclass
class Metric:
    id: str
    name: str
    category: str
    value: Optional[float]
    previous: Optional[float]
    change: Optional[float]
    unit: str
    as_of: Optional[str]
    previous_as_of: Optional[str]
    frequency: str
    source: str
    source_url: str
    status: str = "ok"
    notes: str = ""
    stale_days: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DerivedSignal:
    id: str
    name: str
    value: Optional[float]
    unit: str
    interpretation: str
    severity: str
    previous: Optional[float] = None
    change: Optional[float] = None


def now_bjt() -> datetime:
    return datetime.now(BJT)


def get_fred_api_key() -> str:
    env_key = os.getenv("FRED_API_KEY", "").strip()
    if env_key:
        return env_key
    if FRED_API_KEY_PATH.exists():
        return FRED_API_KEY_PATH.read_text(encoding="utf-8").strip()
    return ""


def http_get_text(url: str, timeout: int = 10, retries: int = 0) -> str:
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, errors="replace")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < retries:
                time.sleep(1.0 + attempt)
    raise RuntimeError(f"GET failed: {url} | {last_error}")


def http_get_json(url: str, timeout: int = 10, retries: int = 0) -> Any:
    text = http_get_text(url, timeout=timeout, retries=retries)
    return json.loads(text)


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return float(value)
    s = str(value).strip()
    if not s or s == "." or s.lower() in {"nan", "n/a", "null", "none"}:
        return None
    s = s.replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


def redact_url_secret(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    redacted_query = urllib.parse.urlencode([(key, "REDACTED" if key.lower() == "api_key" else value) for key, value in query])
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, redacted_query, parsed.fragment))


def normalize_fred_value(series_id: str, value: float, unit: str) -> float:
    if unit == "USD bn" and abs(value) > 100_000:
        return value / 1_000.0
    return value


def parse_date_guess(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s[:19], fmt).date().isoformat()
        except ValueError:
            pass
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    return s


def stale_days(as_of: Optional[str]) -> Optional[int]:
    if not as_of:
        return None
    try:
        d = datetime.strptime(as_of[:10], "%Y-%m-%d").date()
    except ValueError:
        return None
    return (datetime.now(UTC).date() - d).days


def make_metric(
    metric_id: str,
    name: str,
    category: str,
    latest: Optional[Tuple[str, float]],
    previous: Optional[Tuple[str, float]],
    unit: str,
    frequency: str,
    source: str,
    source_url: str,
    status: str = "ok",
    notes: str = "",
    extra: Optional[Dict[str, Any]] = None,
) -> Metric:
    value = latest[1] if latest else None
    prev_value = previous[1] if previous else None
    change = value - prev_value if value is not None and prev_value is not None else None
    as_of = latest[0] if latest else None
    prev_as_of = previous[0] if previous else None
    return Metric(
        id=metric_id,
        name=name,
        category=category,
        value=value,
        previous=prev_value,
        change=change,
        unit=unit,
        as_of=as_of,
        previous_as_of=prev_as_of,
        frequency=frequency,
        source=source,
        source_url=source_url,
        status=status,
        notes=notes,
        stale_days=stale_days(as_of),
        extra=extra or {},
    )


def error_metric(metric_id: str, name: str, category: str, unit: str, frequency: str, source: str, source_url: str, error: Exception) -> Metric:
    return Metric(
        id=metric_id,
        name=name,
        category=category,
        value=None,
        previous=None,
        change=None,
        unit=unit,
        as_of=None,
        previous_as_of=None,
        frequency=frequency,
        source=source,
        source_url=source_url,
        status="error",
        notes=str(error),
    )


def walk_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_dicts(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_dicts(item)


def extract_nyfed_observations(payload: Any) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for d in walk_dicts(payload):
        keys = set(d.keys())
        has_date = bool(keys & {"effectiveDate", "date", "businessDate", "referenceDate"})
        has_rate = bool(keys & {"percentRate", "rate", "averageRate", "ratePercent"})
        if has_date and has_rate:
            candidates.append(d)
    return candidates


def fetch_nyfed_rate(metric_id: str, name: str, secured: bool) -> Metric:
    market = "secured" if secured else "unsecured"
    url = f"https://markets.newyorkfed.org/api/rates/{market}/{metric_id}/last/2.json"
    try:
        payload = http_get_json(url)
        records = extract_nyfed_observations(payload)
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            date = parse_date_guess(rec.get("effectiveDate") or rec.get("date") or rec.get("businessDate") or rec.get("referenceDate"))
            value = safe_float(rec.get("percentRate") or rec.get("rate") or rec.get("averageRate") or rec.get("ratePercent"))
            if date and value is not None:
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2]} if parsed else {}
        return make_metric(metric_id.upper(), name, "银行间/回购融资", latest, previous, "%", "daily T+1", "NY Fed Markets API", url, extra=extra)
    except Exception as exc:  # noqa: BLE001
        return error_metric(metric_id.upper(), name, "银行间/回购融资", "%", "daily T+1", "NY Fed Markets API", url, exc)


def fetch_fred_series(series_id: str, name: str, category: str, unit: str, frequency: str) -> Metric:
    start_date = (datetime.now(UTC).date() - timedelta(days=180)).isoformat()
    source_page_url = f"https://fred.stlouisfed.org/series/{series_id}"
    api_key = get_fred_api_key()
    if api_key:
        params = urllib.parse.urlencode({"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "desc", "limit": 2, "observation_start": start_date})
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        source = "FRED API"
    else:
        params = urllib.parse.urlencode({"id": series_id, "cosd": start_date})
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
        source = "FRED CSV"
    try:
        rows: List[Tuple[str, float]] = []
        if api_key:
            payload = http_get_json(url, timeout=12, retries=2)
            observations = payload.get("observations", []) if isinstance(payload, dict) else []
            for row in observations:
                date = parse_date_guess(row.get("date"))
                value = safe_float(row.get("value"))
                if date and value is not None:
                    rows.append((date, normalize_fred_value(series_id, value, unit)))
        else:
            text = http_get_text(url, timeout=8, retries=0)
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                date = parse_date_guess(row.get("observation_date") or row.get("DATE") or row.get("date"))
                value = safe_float(row.get(series_id) or row.get("VALUE") or row.get("value"))
                if date and value is not None:
                    rows.append((date, normalize_fred_value(series_id, value, unit)))
        rows = sorted(rows, key=lambda x: x[0])
        latest = rows[-1] if rows else None
        previous = rows[-2] if len(rows) >= 2 else None
        return make_metric(series_id, name, category, latest, previous, unit, frequency, source, source_page_url, extra={"fetch_url": redact_url_secret(url)})
    except Exception as exc:  # noqa: BLE001
        safe_exc = RuntimeError(str(exc).replace(api_key, "REDACTED")) if api_key else exc
        metric = error_metric(series_id, name, category, unit, frequency, source, source_page_url, safe_exc)
        metric.extra = {"fetch_url": redact_url_secret(url)}
        return metric


def fiscal_amount_to_bn(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    abs_value = abs(value)
    if abs_value > 10_000_000:
        return value / 1_000_000_000.0
    if abs_value > 10_000:
        return value / 1_000.0
    return value


def read_tga_history(max_entries: int = 60) -> List[Tuple[str, float]]:
    """读取 TGA 本地历史记录（多条），用于计算 previous 变化值。

    兼容两种格式：
    - 新格式（列表）：[{"date": "2026-05-07", "value": 500.0}, ...]
    - 旧格式（字典）：{"date": "2026-05-07", "value": 500.0}
    """
    try:
        if not TGA_CACHE_PATH.exists():
            return []
        with open(TGA_CACHE_PATH) as f:
            raw = json.load(f)
        entries: List[Tuple[str, float]] = []
        if isinstance(raw, list):
            for item in raw:
                try:
                    entries.append((str(item["date"]), float(item["value"])))
                except Exception:
                    continue
        elif isinstance(raw, dict):
            try:
                entries.append((str(raw["date"]), float(raw["value"])))
            except Exception:
                return []
        else:
            return []
        entries = sorted(set(entries), key=lambda x: x[0])
        return entries[-max_entries:] if entries else []
    except Exception:
        return []


def append_tga_history(date_str: str, value: float, keep: int = 90) -> None:
    """将本次抓取的 TGA 追加到本地历史记录，按日期去重，保留最近 keep 条。"""
    try:
        TGA_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        history = read_tga_history(keep * 2)
        # 按日期去重，保留最新
        by_date: Dict[str, float] = {}
        for d, v in history:
            by_date[d] = v
        by_date[date_str] = value
        sorted_entries = sorted(by_date.items(), key=lambda x: x[0])
        trimmed = sorted_entries[-keep:]
        with open(TGA_CACHE_PATH, "w") as f:
            json.dump([{"date": d, "value": v} for d, v in trimmed], f, indent=2)
    except Exception:
        pass


def fetch_tga() -> Metric:
    # 拉 90 条以 bootstrap 本地历史缓存，确保 previous 有数据
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90"
    try:
        payload = http_get_json(url)
        records = payload.get("data", []) if isinstance(payload, dict) else []
        parsed: List[Tuple[str, float]] = []
        for rec in records:
            account_type = str(rec.get("account_type", ""))
            if "Closing Balance" not in account_type:
                continue
            date = parse_date_guess(rec.get("record_date"))
            raw_value = safe_float(rec.get("open_today_bal") or rec.get("close_today_bal"))
            value = fiscal_amount_to_bn(raw_value)
            if date and value is not None:
                parsed.append((date, value))
        parsed = sorted(set(parsed), key=lambda x: x[0])
        if not parsed:
            return error_metric("TGA", "Treasury General Account / operating cash balance", "Fed负债端", "USD bn", "daily T+1", "Treasury FiscalData", url, Exception("no data"))
        # 把所有历史数据点写入本地缓存
        for d, v in parsed:
            append_tga_history(d, v)
        # latest = 最新一条
        latest_date, latest_value = parsed[-1]
        # previous = 缓存中日期小于 latest_date 的最近一条
        history = read_tga_history(90)
        previous = None
        for d, v in reversed(history):
            if d < latest_date:
                previous = (d, v)
                break
        extra = {"raw_latest": records[0]} if records else {}
        metric = make_metric("TGA", "Treasury General Account closing balance", "Fed负债端",
                            (latest_date, latest_value), previous,
                            "USD bn", "daily T+1", "Treasury FiscalData", url, extra=extra)
        return metric
    except Exception as exc:  # noqa: BLE001
        return error_metric("TGA", "Treasury General Account / operating cash balance", "Fed负债端", "USD bn", "daily T+1", "Treasury FiscalData", url, exc)


def fetch_nyfed_rrp(lookback_days: int = 14) -> Metric:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=lookback_days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?{params}"
    try:
        payload = http_get_json(url)
        operations = []
        if isinstance(payload, dict):
            operations = payload.get("repo", {}).get("operations", [])
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in operations:
            date = parse_date_guess(rec.get("operationDate"))
            value = safe_float(rec.get("totalAmtAccepted"))
            if date and value is not None:
                parsed.append((date, value / 1_000_000_000.0, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2], "lookback_days": lookback_days} if parsed else {"lookback_days": lookback_days}
        status = "ok" if latest else "unavailable"
        notes = "NY Fed reverse repo accepted amount; replaces FRED RRPONTSYD when FRED is slow or unavailable"
        return make_metric("RRPONTSYD", "Overnight Reverse Repo accepted amount", "Fed负债端", latest, previous, "USD bn", "daily T+1", "NY Fed Markets API", url, status=status, notes=notes, extra=extra)
    except Exception as exc:  # noqa: BLE001
        return error_metric("RRPONTSYD", "Overnight Reverse Repo accepted amount", "Fed负债端", "USD bn", "daily T+1", "NY Fed Markets API", url, exc)


def fetch_soma_summary() -> Metric:
    url = "https://markets.newyorkfed.org/api/soma/summary.json"
    try:
        payload = http_get_json(url)
        records = list(walk_dicts(payload))
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            date = parse_date_guess(rec.get("asOfDate") or rec.get("as_of_date") or rec.get("effectiveDate") or rec.get("date"))
            value = None
            for key in ("totalParValue", "parValue", "total", "value", "amount"):
                value = safe_float(rec.get(key))
                if value is not None:
                    break
            if date and value is not None:
                if abs(value) > 1_000_000_000:
                    value = value / 1_000_000_000.0
                elif abs(value) > 10_000:
                    value = value / 1_000.0
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"raw_latest": parsed[-1][2]} if parsed else {}
        status = "ok" if latest else "unavailable"
        notes = "SOMA endpoint schema may change; use as weekly QT background" if latest else "Could not extract numeric SOMA summary from endpoint"
        return make_metric("SOMA", "SOMA holdings / QT background", "Fed负债端", latest, previous, "USD bn", "weekly", "NY Fed Markets API", url, status=status, notes=notes, extra=extra)
    except Exception as exc:  # noqa: BLE001
        return error_metric("SOMA", "SOMA holdings / QT background", "Fed负债端", "USD bn", "weekly", "NY Fed Markets API", url, exc)


def fetch_treasury_auctions(lookback_days: int) -> Metric:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=lookback_days)
    params = urllib.parse.urlencode({"format": "json", "startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://www.treasurydirect.gov/TA_WS/securities/search?{params}"
    try:
        payload = http_get_json(url)
        records = payload if isinstance(payload, list) else payload.get("data", []) if isinstance(payload, dict) else []
        parsed: List[Tuple[str, float, Dict[str, Any]]] = []
        for rec in records:
            if not isinstance(rec, dict):
                continue
            date = parse_date_guess(rec.get("auctionDate") or rec.get("auction_date"))
            value = safe_float(rec.get("bidToCoverRatio") or rec.get("bid_to_cover_ratio"))
            if date and value is not None:
                parsed.append((date, value, rec))
        parsed = sorted(parsed, key=lambda x: x[0])
        latest = (parsed[-1][0], parsed[-1][1]) if parsed else None
        previous = (parsed[-2][0], parsed[-2][1]) if len(parsed) >= 2 else None
        extra = {"latest_auction": parsed[-1][2], "lookback_days": lookback_days} if parsed else {"lookback_days": lookback_days}
        notes = "Uses bid-to-cover as free auction demand proxy; auction tail requires WI yield not available here"
        status = "ok" if latest else "unavailable"
        return make_metric("UST_AUCTION_BTC", "Treasury auction bid-to-cover", "国债/抵押品", latest, previous, "ratio", "event-based", "TreasuryDirect", url, status=status, notes=notes, extra=extra)
    except Exception as exc:  # noqa: BLE001
        return error_metric("UST_AUCTION_BTC", "Treasury auction bid-to-cover", "国债/抵押品", "ratio", "event-based", "TreasuryDirect", url, exc)


def fetch_ofr_series(mnemonic: str, metric_id: str, name: str) -> Metric:
    params = urllib.parse.urlencode({"mnemonic": mnemonic})
    url = f"https://data.financialresearch.gov/v1/series/timeseries?{params}"
    try:
        payload = http_get_json(url)
        parsed: List[Tuple[str, float]] = []
        if isinstance(payload, list):
            for row in payload:
                if isinstance(row, list) and len(row) >= 2:
                    date = parse_date_guess(row[0])
                    value = fiscal_amount_to_bn(safe_float(row[1]))
                    if date and value is not None:
                        parsed.append((date, value))
        else:
            records = list(walk_dicts(payload))
            for rec in records:
                date = parse_date_guess(rec.get("date") or rec.get("observation_date") or rec.get("time_period"))
                value = None
                for key in ("value", "obs_value", "amount"):
                    value = safe_float(rec.get(key))
                    if value is not None:
                        break
                value = fiscal_amount_to_bn(value)
                if date and value is not None:
                    parsed.append((date, value))
        parsed = sorted(set(parsed), key=lambda x: x[0])
        latest = parsed[-1] if parsed else None
        previous = parsed[-2] if len(parsed) >= 2 else None
        status = "ok" if latest else "unavailable"
        notes = "Optional OFR STFM series; if unavailable, do not block the main briefing"
        return make_metric(metric_id, name, "国债/抵押品", latest, previous, "USD bn", "weekly", "OFR STFM", url, status=status, notes=notes)
    except Exception as exc:  # noqa: BLE001
        metric = error_metric(metric_id, name, "国债/抵押品", "USD bn", "weekly", "OFR STFM", url, exc)
        metric.notes = f"Optional source failed: {metric.notes}"
        return metric


def add_synthetic_policy_anchor(metrics: List[Metric]) -> None:
    mm = metric_map(metrics)
    effr = mm.get("EFFR")
    if not effr or not effr.extra:
        return
    raw = effr.extra.get("raw_latest", {})
    prev_raw = {}
    anchor = safe_float(raw.get("targetRateTo"))
    if anchor is None:
        return
    metric = Metric(
        id="POLICY_UPPER_NYFED",
        name="Fed target upper bound from NY Fed EFFR record",
        category="政策锚",
        value=anchor,
        previous=anchor,
        change=0.0,
        unit="%",
        as_of=effr.as_of,
        previous_as_of=effr.previous_as_of,
        frequency="daily / policy step",
        source="NY Fed Markets API",
        source_url=effr.source_url,
        status="ok",
        notes="Fallback policy anchor when IORB/FRED is unavailable; not identical to IORB",
        stale_days=effr.stale_days,
        extra={"raw_latest": raw, "raw_previous": prev_raw},
    )
    metrics.append(metric)


def fetch_all_metrics(auction_lookback_days: int) -> List[Metric]:
    api_jobs = [
        lambda: fetch_nyfed_rate("sofr", "Secured Overnight Financing Rate", True),
        lambda: fetch_nyfed_rate("tgcr", "Tri-party General Collateral Rate", True),
        lambda: fetch_nyfed_rate("bgcr", "Broad General Collateral Rate", True),
        lambda: fetch_nyfed_rate("effr", "Effective Federal Funds Rate", False),
        lambda: fetch_nyfed_rate("obfr", "Overnight Bank Funding Rate", False),
        fetch_tga,
        lambda: fetch_nyfed_rrp(14),
        lambda: fetch_treasury_auctions(auction_lookback_days),
        fetch_soma_summary,
        lambda: fetch_ofr_series("NYPD-PD_AFtD_T-A", "REPO_FAILS_UST", "Primary dealer Treasury repo fails"),
    ]
    fred_jobs = [
        lambda: fetch_fred_series("IORB", "Interest on Reserve Balances", "政策锚", "%", "daily / policy step"),
        lambda: fetch_fred_series("WRESBAL", "Reserve balances with Federal Reserve Banks", "Fed负债端", "USD bn", "weekly"),
        lambda: fetch_fred_series("DTWEXBGS", "Trade-weighted broad dollar index", "离岸美元", "index", "daily T+1"),
        lambda: fetch_fred_series("DCPN3M", "90-day AA nonfinancial commercial paper", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("DFEDTARU", "Federal funds target range upper limit", "政策锚", "%", "daily / policy step"),
        lambda: fetch_fred_series("BAMLH0A0HYM2", "ICE BofA US High Yield OAS", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("BAMLC0A0CM", "ICE BofA US Corporate OAS", "信用传导", "%", "daily T+1"),
        lambda: fetch_fred_series("DTB3", "3-month Treasury bill secondary market rate", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS3MO", "3-month Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS1", "1-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS2", "2-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS3", "3-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS10", "10-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DFII10", "10-year Treasury inflation-indexed security real yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("DGS30", "30-year Treasury constant maturity yield", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("T10Y2Y", "10-year minus 2-year Treasury spread", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("T10Y3M", "10-year minus 3-month Treasury spread", "国债收益率/曲线", "%", "daily T+1"),
        lambda: fetch_fred_series("VIXCLS", "CBOE Volatility Index: VIX", "证券市场风险偏好", "index", "daily T+1"),
        lambda: fetch_fred_series("NFCI", "Chicago Fed National Financial Conditions Index", "金融条件", "index", "weekly"),
    ]
    metrics: List[Metric] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_index = {executor.submit(job): index for index, job in enumerate(api_jobs)}
        for future in concurrent.futures.as_completed(future_to_index):
            try:
                metrics.append(future.result(timeout=1))
            except Exception as exc:  # noqa: BLE001
                index = future_to_index[future]
                metrics.append(error_metric(f"JOB_{index}", "Uncaught fetch job error", "系统", "", "unknown", "internal", "", exc))
    for job in fred_jobs:
        metrics.append(job())
        time.sleep(0.15)
    add_synthetic_policy_anchor(metrics)
    metrics.sort(key=lambda m: (m.category, m.id))
    return metrics


def metric_map(metrics: List[Metric]) -> Dict[str, Metric]:
    return {m.id.upper(): m for m in metrics}


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
    effr_anchor_label = "EFFR-IORB（有效联邦基金利率-准备金余额利率）" if policy_anchor and policy_anchor.id == "IORB" else "EFFR-Policy Anchor（有效联邦基金利率-政策锚）"
    sofr_anchor_label = "SOFR-IORB（担保隔夜融资利率-准备金余额利率）" if policy_anchor and policy_anchor.id == "IORB" else "SOFR-Policy Anchor（担保隔夜融资利率-政策锚）"

    # EFFR-IORB 已移除：GSE结构性压低，信号噪声大；SOFR-IORB 是更优指标
    # 不再计算 EFFR_ANCHOR 信号和评分贡献

    sofr_anchor = spread_value(mm.get("SOFR"), policy_anchor)
    sofr_anchor_prev = previous_spread_value(mm.get("SOFR"), policy_anchor)
    sev_key, sev = classify_bp(sofr_anchor, 0.0, -8.0)
    add_signal("SOFR_ANCHOR", sofr_anchor_label, sofr_anchor, "bp", f"SOFR相对{anchor_label}的位置。" + ("回购融资高于政策锚，抵押融资压力上升" if sev_key == "tight" else "回购融资低于政策锚，说明资金面不紧" if sev_key == "loose" else "回购融资与政策锚接近"), sev, 1.5 if sev_key == "tight" else -0.5 if sev_key == "loose" else 0.0, previous=sofr_anchor_prev)

    # SOFR_EFFR 已移除：日常监测价值有限，SOFR-IORB 已足够观察回购端压力
    # 不再计算 SOFR_EFFR 信号和评分贡献

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
    # 计算前一天的 TGA 日变化，作为 TGA_FLOW 的 previous
    tga_change_prev = None
    if tga and tga.previous is not None and tga.previous_as_of:
        history = read_tga_history(90)
        # history 按日期升序排列：[(date1, val1), (date2, val2), ...]
        # 找到 tga.previous_as_of 的位置，计算它相对于再前一天的变化
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


def format_number(value: Optional[float], unit: str, precision: int = 2) -> str:
    if value is None:
        return "NA"
    if unit == "bp":
        return f"{value:.1f}bp"
    if unit == "%":
        return f"{value:.3f}%"
    if unit == "USD bn":
        return f"{value:,.1f}bn"
    if unit == "ratio":
        return f"{value:.2f}x"
    if unit == "index":
        return f"{value:.2f}"
    return f"{value:.{precision}f}{unit}"


def format_change(change: Optional[float], unit: str) -> str:
    if change is None:
        return "NA"
    sign = "+" if change > 0 else ""
    if unit == "%":
        return f"{sign}{change * 100:.1f}bp"
    if unit == "USD bn":
        return f"{sign}{change:,.1f}bn"
    if unit == "ratio":
        return f"{sign}{change:.2f}x"
    return f"{sign}{change:.2f}"


def format_signal_change(change: Optional[float], unit: str) -> str:
    if change is None:
        return "NA"
    sign = "+" if change > 0 else ""
    if unit == "bp":
        return f"{sign}{change:.1f}bp"
    if unit == "bn":
        return f"{sign}{change:,.1f}bn"
    if unit == "pt":
        return f"{sign}{change:.2f}pt"
    if unit == "x":
        return f"{sign}{change:.2f}x"
    return f"{sign}{change:.2f}{unit}"


def freshness_label(metric: Metric) -> str:
    if metric.status != "ok":
        return metric.status
    if metric.stale_days is None:
        return "unknown"
    if "weekly" in metric.frequency:
        return "ok" if metric.stale_days <= 14 else "stale"
    if "event" in metric.frequency:
        return "recent" if metric.stale_days <= 21 else "stale"
    return "ok" if metric.stale_days <= 5 else "stale"


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(out)


def load_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def load_prompt() -> str:
    return load_text(PROMPT_PATH)


def load_intro() -> str:
    return load_text(INTRO_PATH)


def rate_label(metric_id: str) -> str:
    return RATE_LABELS.get(metric_id, f"{metric_id}（未配置中文名）")


def change_direction(change: Optional[float], unit: str) -> str:
    if change is None:
        return "unknown"
    threshold = 0.0005 if unit == "%" else 0.05
    if abs(change) <= threshold:
        return "flat"
    return "up" if change > 0 else "down"


def importance_for(metric_id: str) -> str:
    if metric_id in {"EFFR", "SOFR", "TGA", "RRPONTSYD", "WRESBAL", "IORB", "POLICY_UPPER_NYFED", "DGS1", "DGS3", "DGS10", "DFII10", "BAMLH0A0HYM2"}:
        return "high"
    if metric_id in {"OBFR", "TGCR", "BGCR", "SOMA", "UST_AUCTION_BTC", "REPO_FAILS_UST", "BAMLC0A0CM", "VIXCLS", "NFCI"}:
        return "medium_high"
    return "medium"


def describe_rate_change(metric: Metric) -> str:
    if metric.status != "ok" or metric.value is None:
        return "本次未取到可用数据，不能判断边际变化。"
    if metric.change is None:
        return "缺少上一期可比数据，暂不能判断边际方向。"
    if metric.unit == "%":
        change_value = abs(metric.change * 100.0)
        change_text = f"{change_value:.1f}bp"
    elif metric.unit == "USD bn":
        change_value = abs(metric.change)
        change_text = f"{change_value:.1f}十亿美元"
    elif metric.unit == "ratio":
        change_value = abs(metric.change)
        change_text = f"{change_value:.2f}倍"
    else:
        change_value = abs(metric.change)
        change_text = f"{change_value:.2f}{metric.unit}"
    if change_value < 0.05:
        return "较上一期基本持平，说明边际资金价格没有明显变化。"
    up_text, down_text = RATE_CHANGE_IMPLICATIONS.get(metric.id, ("该指标边际上升，需要结合其他指标判断压力", "该指标边际下降，需要结合其他指标判断宽松程度"))
    if metric.change > 0:
        return f"上升 {change_text}，{up_text}。"
    return f"下降 {change_text}，{down_text}。"


def render_rate_summary_table(metrics: List[Metric]) -> str:
    mm = metric_map(metrics)
    ordered_ids = ["EFFR", "SOFR", "IORB", "POLICY_UPPER_NYFED", "OBFR", "TGCR", "BGCR"]
    rows: List[List[str]] = []
    for metric_id in ordered_ids:
        metric = mm.get(metric_id)
        if not metric:
            continue
        value_text = format_number(metric.value, metric.unit)
        rows.append([
            f"{rate_label(metric.id)}：{value_text}",
            RATE_MEANINGS.get(metric.id, metric.name),
            describe_rate_change(metric),
        ])
    if not rows:
        rows.append(["NA（未取得利率数据）", "核心利率接口本次均未返回可用数据。", "无法判断边际变化。"])
    return markdown_table(["利率", "含义", "边际变化"], rows)


def comparison_rule(metric: Metric) -> str:
    if "weekly" in metric.frequency:
        return "周度环比"
    if "event" in metric.frequency:
        return "上一事件/上一场拍卖"
    if "policy" in metric.frequency:
        return "政策阶梯变化，不做普通日环比"
    return "上一有效工作日/上一有效观测"


def build_frequency_rows(metrics: List[Metric]) -> List[List[str]]:
    rows: List[List[str]] = []
    for metric in metrics:
        update_rule, data_lag, compare_rule = DATA_FREQUENCY_RULES.get(
            metric.id,
            (metric.frequency, "以接口返回日期为准", comparison_rule(metric)),
        )
        rows.append([
            metric.id,
            metric.category,
            update_rule,
            data_lag,
            compare_rule,
            metric.as_of or "NA",
            metric.previous_as_of or "NA",
        ])
    return rows


def render_frequency_table(metrics: List[Metric]) -> str:
    priority = {"EFFR", "SOFR", "OBFR", "TGCR", "BGCR", "IORB", "POLICY_UPPER_NYFED", "TGA", "RRPONTSYD", "WRESBAL", "SOMA", "UST_AUCTION_BTC", "REPO_FAILS_UST", "DTWEXBGS", "DCPN3M", "BAMLC0A0CM", "BAMLH0A0HYM2", "DGS1", "DGS3", "DGS10", "DFII10", "DGS30", "T10Y2Y", "T10Y3M", "VIXCLS", "NFCI"}
    filtered = [m for m in metrics if m.id in priority]
    rows = build_frequency_rows(filtered)
    return markdown_table(["指标", "模块", "更新频率", "数据滞后", "环比口径", "最新日期", "上一期日期"], rows)


def render_core_indicator_impact_table() -> str:
    rows = [[name, impact, reason] for name, impact, reason in CORE_INDICATOR_IMPACTS]
    return markdown_table(["指标", "影响权重", "为什么重要"], rows)


def _format_signal_value(v: Optional[float], unit: str) -> str:
    """Format a single signal value for display."""
    if v is None:
        return "N/A"
    if unit == "bp":
        return f"{v:+.1f}bp"
    if unit == "%":
        return f"{v:.2f}%"
    if unit == "bn":
        return f"{v:.2f}bn"
    return f"{v}"


def _format_signals_table_for_prompt(signals: List[DerivedSignal]) -> str:
    """Format derived signals into a Markdown table injected into the prompt."""
    lines = [
        "| 信号ID | 信号名称 | 最新值 | 上一期值 | 边际变化 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in signals:
        vid = s.id or ""
        name = s.name or vid
        value_str = _format_signal_value(s.value, s.unit)
        prev_str = _format_signal_value(s.previous, s.unit) if s.previous is not None else "首期/无上一期"
        change_str = _format_signal_value(s.change, s.unit) if s.change is not None else "首期/无上一期"
        lines.append(f"| {vid} | {name} | {value_str} | {prev_str} | {change_str} |")
    return "\n".join(lines)


def build_model_input_package(trigger: str, generated: str, stance: str, score: float, metrics: List[Metric], signals: List[DerivedSignal], highlights: List[str], chart_paths: Optional[List[str]] = None) -> Dict[str, Any]:
    # 把 derived_signals 的正确值直接注入 prompt 最顶部，强制模型先看到硬数字
    signals_table = _format_signals_table_for_prompt(signals)
    prompt_text = load_prompt()
    injection = (
        "【衍生信号强制取值表 —— 你必须直接引用下表数值，严禁自行计算或篡改】\n"
        "以下衍生信号已由脚本精确计算完成，你在写分析时 MUST 直接使用下表中的「最新值」和「边际变化」，"
        "不得自行用原始利率相减，不得引用任何与下表不一致的数字。\n\n"
        f"{signals_table}\n\n"
        "--- 以上表数值为准，以下为分析指令 ---\n\n"
    )
    prompt_text = injection + prompt_text
    return {
        "task": "基于美元流动性介绍文档、结构化市场数据和分析prompt，输出一份可由固定前端模板渲染的结构化 analysis.json。",
        "trigger": trigger or "默认运行",
        "generated_at_bjt": generated,
        "intro_document": load_intro(),
        "analysis_prompt": prompt_text,
        "data": {
            "stance_by_rule_fallback": stance,
            "score_by_rule_fallback": score,
            "highlights_by_rule_fallback": highlights,
            "metrics": [asdict(m) for m in metrics],
            "derived_signals": [asdict(s) for s in signals],
            "jpy_carry_history": load_jpy_carry_history_payload(),
            "data_frequency_rules": DATA_FREQUENCY_RULES,
            "core_indicator_impacts": CORE_INDICATOR_IMPACTS,
            "chart_paths": chart_paths or [],
            "unavailable_sources": UNAVAILABLE_SOURCES,
        },
        "output_contract": {
            "format": "strict_json_only",
            "language": "中文",
            "style": "结论先行、字段稳定、由前端固定模板渲染",
            "forbidden_outputs": ["html", "markdown", "code_fence", "free_text_before_or_after_json"],
            "required_top_level_fields": ["meta", "stance", "key_takeaways", "risk_flags", "narrative_blocks"],
            
            
            
            "marginal_change_rule": "边际变化不能只写数值，必须说明上升/下降对融资压力或流动性的含义。",
            "dynamic_sections_rule": "key_takeaways 和 risk_flags 必须根据本次数据动态生成，数量 0-5 条，不固定为 3 条。",
            "risk_type_rule": "risk_flags.type 必须区分 market 与 data；数据缺口不能写成真实市场压力。",
            "rrp_rule": "RRP上升短期通常偏不利风险资产，RRP下降短期通常偏利好；但RRP低位继续下降代表缓冲垫耗尽。必须区分边际方向与存量缓冲垫。",
            
            "json_schema_summary": {
                "stance": ["label", "confidence", "score_text", "one_liner"],
                "risk_flag_item": ["priority", "severity", "type", "title", "text", "evidence", "related_indicators"]
            },
        },
    }


def fetch_fred_series_points(series_id: str, days: int, unit: str, use_cache: bool = True) -> List[Tuple[str, float]]:
    start_date = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    # --- DB 缓存层 ---
    if use_cache:
        try:
            import sqlite3, os
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id = ? AND as_of >= ? ORDER BY as_of", (series_id, start_date))
                rows = [(row[0], row[1]) for row in cur.fetchall() if row[1] is not None]
                conn.close()
                if len(rows) >= max(1, days // 3):
                    return rows
        except Exception:
            pass
    # --- 缓存未命中，调 API ---
    api_key = get_fred_api_key()
    if api_key:
        params = urllib.parse.urlencode({"series_id": series_id, "api_key": api_key, "file_type": "json", "sort_order": "asc", "observation_start": start_date})
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        payload = http_get_json(url, timeout=12, retries=0)
        observations = payload.get("observations", []) if isinstance(payload, dict) else []
        rows: List[Tuple[str, float]] = []
        for row in observations:
            date = parse_date_guess(row.get("date"))
            value = safe_float(row.get("value"))
            if date and value is not None:
                rows.append((date, normalize_fred_value(series_id, value, unit)))
        # 写回 DB
        try:
            import sqlite3, os
            from datetime import datetime as _dt
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
            for d, v in rows:
                cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at, snapshot_file) VALUES (?,?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", (series_id, d, v, unit, "FRED API (chart cache)", ingested, "chart_cache"))
            conn.commit()
            conn.close()
        except Exception:
            pass
        return sorted(rows)

    params = urllib.parse.urlencode({"id": series_id, "cosd": start_date})
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
    text = http_get_text(url, timeout=8, retries=0)
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        date = parse_date_guess(row.get("observation_date") or row.get("DATE") or row.get("date"))
        value = safe_float(row.get(series_id) or row.get("VALUE") or row.get("value"))
        if date and value is not None:
            rows.append((date, normalize_fred_value(series_id, value, unit)))
    return sorted(rows)


def _nyfed_series_to_db(metric_id: str, rates: List[Tuple[str, float]], policy_upper: List[Tuple[str, float]]) -> None:
    """将 NY Fed 利率序列写回本地 DB。"""
    try:
        import sqlite3, os
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rates:
            cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", (metric_id.upper(), d, v, "%", "NY Fed Markets API (chart)", ingested))
        for d, v in policy_upper:
            cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", ("POLICY_UPPER_NYFED", d, v, "%", "NY Fed Markets API (chart)", ingested))
        conn.commit()
        conn.close()
    except Exception:
        pass

def _nyfed_series_from_db(metric_id: str, days: int) -> Tuple[Optional[List[Tuple[str, float]]], Optional[List[Tuple[str, float]]]]:
    """从本地 DB 读取 NY Fed 利率序列；数据不足时返回 (None, None)。"""
    try:
        import sqlite3, os
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return None, None
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
        cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id = ? AND as_of >= ? ORDER BY as_of", (metric_id.upper(), start))
        rates = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id = ? AND as_of >= ? ORDER BY as_of", ("POLICY_UPPER_NYFED", start))
        policy = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rates) >= max(1, days // 3) and len(policy) >= max(1, days // 3):
            return rates, policy
    except Exception:
        pass
    return None, None

def fetch_nyfed_rate_series(metric_id: str, secured: bool, days: int, use_cache: bool = True) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    # --- DB 缓存层 ---
    if use_cache:
        cached_rates, cached_policy = _nyfed_series_from_db(metric_id, days)
        if cached_rates is not None:
            return cached_rates, cached_policy
    # --- 缓存未命中，调 API ---
    market = "secured" if secured else "unsecured"
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rates/{market}/{metric_id}/search.json?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload.get("refRates", []) if isinstance(payload, dict) else []
    rates: List[Tuple[str, float]] = []
    policy_upper: List[Tuple[str, float]] = []
    for rec in records:
        date = parse_date_guess(rec.get("effectiveDate") or rec.get("date"))
        rate = safe_float(rec.get("percentRate") or rec.get("rate"))
        upper = safe_float(rec.get("targetRateTo"))
        if date and rate is not None:
            rates.append((date, rate))
        if date and upper is not None:
            policy_upper.append((date, upper))
    _nyfed_series_to_db(metric_id, rates, policy_upper)
    return sorted(rates), sorted(policy_upper)


def _rrp_to_db(rows):
    """将 RRP 序列写回本地 DB。"""
    try:
        import sqlite3, os
        from datetime import datetime as _dt
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rows:
            cur.execute(
                "INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at",
                ("RRPONTSYD", d, v, "USD bn", "NY Fed Markets API (chart)", ingested)
            )
        conn.commit()
        conn.close()
    except Exception:
        pass

def _rrp_from_db(days):
    """从本地 DB 读取 RRP 序列；数据不足返回 None。"""
    try:
        import sqlite3, os
        from datetime import date as _d
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return None
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        start = (_d.today() - __import__('datetime').timedelta(days=days)).isoformat()
        cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id=? AND as_of>=? ORDER BY as_of", ("RRPONTSYD", start))
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rows) >= max(1, days // 3): return rows
    except Exception:
        pass
    return None

def fetch_rrp_series(days, use_cache=True):
    cached = _rrp_from_db(days) if use_cache else None
    if cached is not None: return cached
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days)
    params = urllib.parse.urlencode({"startDate": start.isoformat(), "endDate": end.isoformat()})
    url = f"https://markets.newyorkfed.org/api/rp/reverserepo/positions/search.json?{params}"
    payload = http_get_json(url, timeout=12, retries=0)
    operations = payload.get("repo", {}).get("operations", []) if isinstance(payload, dict) else []
    rows = []
    for rec in operations:
        date = parse_date_guess(rec.get("operationDate"))
        value = safe_float(rec.get("totalAmtAccepted"))
        if date and value is not None:
            rows.append((date, value / 1_000_000_000.0))
    rows = sorted(rows)
    _rrp_to_db(rows)
    return rows

    try:
        import sqlite3, os
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rows:
            cur.execute("INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at, snapshot_file) VALUES (?,?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at", ("TGA", d, v, "USD bn", "Treasury FiscalData API (chart)", ingested, "chart_cache"))
        conn.commit()
        conn.close()
    except Exception:
        pass

def _tga_series_from_db(days: int) -> Optional[List[Tuple[str, float]]]:
    try:
        import sqlite3, os
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return None
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        start = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
        cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id = ? AND as_of >= ? ORDER BY as_of", ("TGA", start))
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rows) >= max(1, days // 3): return rows
    except Exception:
        pass
    return None

def _tga_to_db(rows):
    """将 TGA 序列写回本地 DB。"""
    try:
        import sqlite3, os
        from datetime import datetime as _dt
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        ingested = datetime.now(BJT).strftime("%Y-%m-%d %H:%M:%S UTC+08:00")
        for d, v in rows:
            cur.execute(
                "INSERT INTO metrics_ts (metric_id, as_of, value, unit, source, ingested_at) VALUES (?,?,?,?,?,?) ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET value=excluded.value, ingested_at=excluded.ingested_at",
                ("TGA", d, v, "USD bn", "Treasury FiscalData API (chart)", ingested)
            )
        conn.commit()
        conn.close()
    except Exception:
        pass

def _tga_from_db(days):
    """从本地 DB 读取 TGA 序列；数据不足返回 None。"""
    try:
        import sqlite3, os
        from datetime import date as _d
        db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "usd_liquidity.db")
        if not os.path.exists(db): return None
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        start = (_d.today() - __import__('datetime').timedelta(days=days)).isoformat()
        cur.execute("SELECT as_of, value FROM metrics_ts WHERE metric_id=? AND as_of>=? ORDER BY as_of", ("TGA", start))
        rows = [(r[0], r[1]) for r in cur.fetchall() if r[1] is not None]
        conn.close()
        if len(rows) >= max(1, days // 3): return rows
    except Exception:
        pass
    return None

def fetch_tga_series(days, use_cache=True):
    cached = _tga_from_db(days) if use_cache else None
    if cached is not None: return cached
    page_size = max(30, min(120, days * 3))
    url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]={page_size}"
    payload = http_get_json(url, timeout=12, retries=0)
    records = payload.get("data", []) if isinstance(payload, dict) else []
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    rows = []
    for rec in records:
        if "Closing Balance" not in str(rec.get("account_type", "")): continue
        date = parse_date_guess(rec.get("record_date"))
        raw_value = safe_float(rec.get("open_today_bal"))
        if raw_value is None: raw_value = safe_float(rec.get("close_today_bal"))
        value = fiscal_amount_to_bn(raw_value)
        if date and date >= cutoff and value is not None:
            rows.append((date, value))
    history = read_tga_history(90)
    existing_dates = {d for d, v in rows}
    for d, v in history:
        if d >= cutoff and d not in existing_dates:
            rows.append((d, v))
    rows = sorted(rows)
    _tga_to_db(rows)
    return rows

    bm = {date: value for date, value in b}
    rows: List[Tuple[str, float]] = []
    for date, value in a:
        if date in bm:
            rows.append((date, (value - bm[date]) * multiplier))
    return rows


def trim_series(series: List[Tuple[str, float]], days: int) -> List[Tuple[str, float]]:
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    return [(date, value) for date, value in series if date >= cutoff]


def svg_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_polyline(points: List[Tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def render_svg_panel(title: str, series_items: List[Tuple[str, List[Tuple[str, float]], str]], x: int, y: int, width: int, height: int, unit: str) -> str:
    non_empty = [(name, rows, color) for name, rows, color in series_items if rows]
    if not non_empty:
        return f'<g><text x="{x}" y="{y + 20}" font-size="15" font-weight="600">{svg_escape(title)}</text><text x="{x}" y="{y + 50}" font-size="13" fill="#777">暂无可绘制数据</text></g>'
    all_dates = sorted({date for _, rows, _ in non_empty for date, _ in rows})
    all_values = [value for _, rows, _ in non_empty for _, value in rows]
    min_v, max_v = min(all_values), max(all_values)
    if abs(max_v - min_v) < 1e-9:
        min_v -= 1.0
        max_v += 1.0
    pad = (max_v - min_v) * 0.12
    min_v -= pad
    max_v += pad
    left, right, top, bottom = x + 58, x + width - 18, y + 36, y + height - 34
    date_index = {date: idx for idx, date in enumerate(all_dates)}
    x_span = max(1, len(all_dates) - 1)
    def px(date: str) -> float:
        return left + (right - left) * date_index[date] / x_span
    def py(value: float) -> float:
        return bottom - (bottom - top) * (value - min_v) / (max_v - min_v)
    out = [f'<g><rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" fill="#ffffff" stroke="#e5e7eb"/>']
    out.append(f'<text x="{x + 16}" y="{y + 24}" font-size="15" font-weight="700" fill="#111827">{svg_escape(title)}</text>')
    for i in range(4):
        gy = top + (bottom - top) * i / 3
        val = max_v - (max_v - min_v) * i / 3
        out.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{right}" y2="{gy:.1f}" stroke="#f3f4f6"/>')
        out.append(f'<text x="{x + 12}" y="{gy + 4:.1f}" font-size="10" fill="#6b7280">{val:.1f}{svg_escape(unit)}</text>')
    for name, rows, color in non_empty:
        pts = [(px(date), py(value)) for date, value in rows if date in date_index]
        if len(pts) == 1:
            out.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="3" fill="{color}"/>')
        elif pts:
            out.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.2" points="{svg_polyline(pts)}"/>')
        label_x = x + 16 + 110 * (len(out) % 7)
        out.append(f'<circle cx="{label_x}" cy="{y + height - 12}" r="4" fill="{color}"/><text x="{label_x + 8}" y="{y + height - 8}" font-size="11" fill="#374151">{svg_escape(name)}</text>')
    out.append(f'<text x="{left}" y="{bottom + 20}" font-size="8" fill="#a8a29e">{svg_escape(all_dates[0])}</text>')
    out.append(f'<text x="{right - 58}" y="{bottom + 20}" font-size="8" fill="#a8a29e">{svg_escape(all_dates[-1])}</text>')
    out.append("</g>")
    return "".join(out)


def render_liquidity_svg(title: str, subtitle: str, days: int, series_bundle: Dict[str, List[Tuple[str, float]]]) -> str:
    anchor_label = "IORB" if series_bundle.get("IORB") else "政策锚"
    panels = [
        ("短端资金利率", [("EFFR", trim_series(series_bundle.get("EFFR", []), days), "#2563eb"), ("SOFR", trim_series(series_bundle.get("SOFR", []), days), "#dc2626"), ("TGCR", trim_series(series_bundle.get("TGCR", []), days), "#059669"), ("BGCR", trim_series(series_bundle.get("BGCR", []), days), "#7c3aed")], "%"),
        # SOFR_EFFR 已移除：日常监测价值有限
        ("相对政策锚利差", [(f"SOFR-{anchor_label}", trim_series(series_bundle.get("SOFR_ANCHOR", []), days), "#dc2626")], "bp"),
        ("TGA财政现金余额", [("TGA", trim_series(series_bundle.get("TGA", []), days), "#0f766e")], "bn"),
        ("RRP缓冲余额", [("RRP", trim_series(series_bundle.get("RRP", []), days), "#9333ea")], "bn"),
    ]
    width, panel_h = 980, 210
    height = 90 + panel_h * len(panels)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">']
    out.append('<rect width="100%" height="100%" fill="#f8fafc"/>')
    out.append(f'<text x="28" y="34" font-size="22" font-weight="800" fill="#111827">{svg_escape(title)}</text>')
    out.append(f'<text x="28" y="58" font-size="13" fill="#64748b">{svg_escape(subtitle)}</text>')
    for idx, (panel_title, items, unit) in enumerate(panels):
        out.append(render_svg_panel(panel_title, items, 22, 78 + idx * panel_h, width - 44, panel_h - 18, unit))
    out.append('</svg>')
    return "".join(out)


def fetch_chart_series(days: int = 40) -> Dict[str, List[Tuple[str, float]]]:
    series: Dict[str, List[Tuple[str, float]]] = {}
    try:
        effr, policy = fetch_nyfed_rate_series("effr", False, days)
        series["EFFR"] = effr
        series["POLICY_UPPER_NYFED"] = policy
    except Exception:  # noqa: BLE001
        pass
    try:
        iorb = fetch_fred_series_points("IORB", days, "%")
        if iorb:
            series["IORB"] = iorb
            series["POLICY"] = iorb
        elif series.get("POLICY_UPPER_NYFED"):
            series["POLICY"] = series["POLICY_UPPER_NYFED"]
    except Exception:  # noqa: BLE001
        if series.get("POLICY_UPPER_NYFED"):
            series["POLICY"] = series["POLICY_UPPER_NYFED"]
    for metric_id in ("sofr", "tgcr", "bgcr"):
        try:
            rows, _ = fetch_nyfed_rate_series(metric_id, True, days)
            series[metric_id.upper()] = rows
        except Exception:  # noqa: BLE001
            pass
    try:
        obfr, _ = fetch_nyfed_rate_series("obfr", False, days)
        series["OBFR"] = obfr
    except Exception:  # noqa: BLE001
        pass
    try:
        series["RRP"] = fetch_rrp_series(days)
    except Exception:  # noqa: BLE001
        pass
    try:
        series["TGA"] = fetch_tga_series(days)
    except Exception:  # noqa: BLE001
        pass
    # EFFR-IORB 已移除；不再计算其时间序列
    # SOFR_EFFR 已移除；不再计算其时间序列
    if series.get("SOFR") and series.get("POLICY"):
        series["SOFR_ANCHOR"] = align_spread(series["SOFR"], series["POLICY"])
    if series.get("BGCR") and series.get("TGCR"):
        series["BGCR_TGCR"] = align_spread(series["BGCR"], series["TGCR"])
    try:
        cp = fetch_fred_series_points("DCPN3M", days, "%")
        policy_upper = fetch_fred_series_points("DFEDTARU", days, "%")
        if cp and policy_upper:
            series["CP_PROXY"] = align_spread(cp, policy_upper)
    except Exception:  # noqa: BLE001
        pass
    for series_id in ("DTB3", "DGS3MO", "DGS1", "DGS2", "DGS3", "DGS10", "DFII10", "DGS30", "T10Y2Y", "T10Y3M", "BAMLH0A0HYM2", "BAMLC0A0CM", "VIXCLS", "NFCI"):
        try:
            unit = "index" if series_id in {"NFCI", "VIXCLS"} else "%"
            rows = fetch_fred_series_points(series_id, days, unit)
            if rows:
                series[series_id] = rows
        except Exception:  # noqa: BLE001
            pass
    return series


def write_liquidity_charts(stamp: str, series_bundle: Optional[Dict[str, List[Tuple[str, float]]]] = None) -> List[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    series_bundle = series_bundle or fetch_chart_series(45)
    chart_specs = [
        ("7d", 10, "美元流动性核心指标：最近一周", "按最近10个日历日抓取，显示有效观测；日频指标按上一有效工作日比较"),
        ("30d", 35, "美元流动性核心指标：最近一月", "按最近35个日历日抓取，显示有效观测；TGA/RRP为十亿美元"),
    ]
    paths: List[Path] = []
    for suffix, days, title, subtitle in chart_specs:
        svg = render_liquidity_svg(title, subtitle, days, series_bundle)
        path = OUTPUT_DIR / f"usd_liquidity_chart_{suffix}_{stamp}.svg"
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def chart_points(series: List[Tuple[str, float]], days: int) -> List[Dict[str, Any]]:
    return [{"date": date, "value": value} for date, value in trim_series(series, days)]


def build_charts_payload(series_bundle: Dict[str, List[Tuple[str, float]]]) -> Dict[str, Any]:
    effr_anchor_label = "EFFR-IORB（有效联邦基金利率-准备金余额利率）" if series_bundle.get("IORB") else "EFFR-Policy Anchor（有效联邦基金利率-政策锚）"
    sofr_anchor_label = "SOFR-IORB（担保隔夜融资利率-准备金余额利率）" if series_bundle.get("IORB") else "SOFR-Policy Anchor（担保隔夜融资利率-政策锚）"
    specs = [
        ("short_rates_7d", "短端资金利率：最近一周", 10, "%", [("EFFR", "EFFR（有效联邦基金利率）"), ("SOFR", "SOFR（担保隔夜融资利率）"), ("TGCR", "TGCR（三方一般抵押品利率）"), ("BGCR", "BGCR（广义一般抵押品利率）")]),
        ("short_rates_30d", "短端资金利率：最近一月", 35, "%", [("EFFR", "EFFR（有效联邦基金利率）"), ("SOFR", "SOFR（担保隔夜融资利率）"), ("TGCR", "TGCR（三方一般抵押品利率）"), ("BGCR", "BGCR（广义一般抵押品利率）")]),
        # SOFR_EFFR 已移除：日常监测价值有限；SOFR-IORB 和 BGCR_TGCR 已覆盖回购端压力观察
        ("anchor_spreads_7d", "关键利差：最近一周", 10, "bp", [("SOFR_ANCHOR", sofr_anchor_label), ("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）")]),
        ("anchor_spreads_30d", "关键利差：最近一月", 35, "bp", [("SOFR_ANCHOR", sofr_anchor_label), ("BGCR_TGCR", "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）")]),
        ("cp_proxy_30d", "企业短融代理利差：最近一月", 35, "bp", [("CP_PROXY", "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）")]),
        ("credit_oas_30d", "信用利差：最近一月", 35, "%", [("BAMLH0A0HYM2", "HY OAS（高收益债期权调整利差）"), ("BAMLC0A0CM", "IG OAS（投资级公司债期权调整利差）")]),
        ("treasury_yields_30d", "美国国债收益率：1Y / 3Y / 10Y 最近一月", 35, "%", [("DGS1", "1Y Treasury Yield（1年期美国国债收益率）"), ("DGS3", "3Y Treasury Yield（3年期美国国债收益率）"), ("DGS10", "10Y Treasury Yield（10年期美国国债收益率）")]),
        ("real_yields_30d", "真实贴现率：最近一月", 35, "%", [("DFII10", "10Y Real Yield（10年期TIPS实际收益率）")]),
        ("treasury_curve_30d", "美债长短端利差：最近一月", 35, "%", [("T10Y2Y", "10Y-2Y Treasury Spread（10年-2年美债利差）"), ("T10Y3M", "10Y-3M Treasury Spread（10年-3个月美债利差）")]),
        ("risk_appetite_30d", "证券市场风险偏好：最近一月", 35, "index", [("VIXCLS", "VIX（标普500隐含波动率指数）")]),
        ("financial_conditions_30d", "公开金融条件代理：最近一月", 35, "index", [("NFCI", "NFCI（芝加哥联储全国金融条件指数）")]),
        ("fed_liability_30d", "Fed负债端水位：最近一月", 35, "USD bn", [("TGA", "TGA（财政部一般账户）", "y"), ("RRP", "RRP（隔夜逆回购）", "y1")]),
    ]
    charts = []
    for chart_id, title, days, unit, ids in specs:
        series = []
        for item in ids:
            series_id, label = item[0], item[1]
            y_axis = item[2] if len(item) >= 3 else "y"
            points = chart_points(series_bundle.get(series_id, []), days)
            if points:
                series.append({"id": series_id, "label": label, "points": points, "y_axis": y_axis})
        chart_payload = {"id": chart_id, "title": title, "chart_type": "line", "unit": unit, "series": series}
        if any(s.get("y_axis") == "y1" for s in series):
            chart_payload["dual_axis"] = True
            chart_payload["y_axes"] = {"y": "TGA（十亿美元）", "y1": "RRP（十亿美元）"}
        charts.append(chart_payload)
    return {"charts": charts}


def build_indicator_card(metric: Metric) -> Dict[str, Any]:
    update_rule, data_lag, compare_rule = DATA_FREQUENCY_RULES.get(metric.id, (metric.frequency, "以接口返回日期为准", comparison_rule(metric)))
    return {
        "id": metric.id,
        "label": rate_label(metric.id),
        "category": metric.category,
        "value": metric.value,
        "value_text": format_number(metric.value, metric.unit),
        "unit": metric.unit,
        "previous": metric.previous,
        "change": metric.change,
        "change_text": format_change(metric.change, metric.unit),
        "change_direction": change_direction(metric.change, metric.unit),
        "as_of": metric.as_of,
        "previous_as_of": metric.previous_as_of,
        "meaning": RATE_MEANINGS.get(metric.id, metric.name),
        "frequency": update_rule,
        "data_lag": data_lag,
        "comparison_basis": compare_rule,
        "freshness": freshness_label(metric),
        "importance": importance_for(metric.id),
        "interpretation_hint": describe_rate_change(metric),
        "source": metric.source,
        "source_url": metric.source_url,
        "status": metric.status,
        "notes": metric.notes,
    }


def group_indicators(metrics: List[Metric]) -> List[Dict[str, Any]]:
    group_defs = [
        ("front_end_rates", "短端资金利率", "观察银行间与回购市场资金价格是否偏离政策锚。", ["EFFR", "SOFR", "OBFR", "TGCR", "BGCR", "IORB", "POLICY_UPPER_NYFED"]),
        ("fed_liability", "Fed负债端水位", "观察TGA、RRP、SOMA与准备金水位对银行体系流动性的影响。", ["TGA", "RRPONTSYD", "SOMA", "WRESBAL"]),
        ("treasury_curve", "国债收益率与曲线", "观察1Y、3Y、10Y收益率组合、真实折现率和曲线利差的变化。", ["DGS1", "DGS3", "DGS10", "DFII10", "DGS30", "T10Y2Y", "T10Y3M", "DTB3", "DGS3MO", "DGS2"]),
        ("collateral_treasury", "抵押品与国债吸收", "观察回购抵押品链条、国债拍卖需求和交割压力。", ["UST_AUCTION_BTC", "REPO_FAILS_UST"]),
        ("offshore_credit", "离岸美元、信用与金融条件", "观察压力是否外溢到离岸美元、信用市场和综合金融条件。", ["DTWEXBGS", "DCPN3M", "BAMLC0A0CM", "BAMLH0A0HYM2", "NFCI"]),
        ("securities_risk", "证券市场风险偏好", "观察利率和信用条件是否进一步反映到股票波动率和风险偏好。", ["VIXCLS"]),
    ]
    cards = [build_indicator_card(metric) for metric in metrics]
    by_id = {card["id"]: card for card in cards}
    groups = []
    for group_id, title, description, ids in group_defs:
        indicators = [by_id[indicator_id] for indicator_id in ids if indicator_id in by_id]
        if indicators:
            groups.append({"id": group_id, "title": title, "description": description, "indicators": indicators})
    return groups


def build_trading_dashboard(metrics: List[Metric], signals: List[DerivedSignal]) -> Dict[str, Any]:
    mm = metric_map(metrics)
    sm = {s.id: s for s in signals}

    def signal_item(signal_id: str, priority: str, why: str) -> Optional[Dict[str, Any]]:
        signal = sm.get(signal_id)
        if not signal:
            return None
        return {
            "type": "signal",
            "id": signal.id,
            "label": signal.name,
            "priority": priority,
            "value_text": format_number(signal.value, signal.unit),
            "previous_text": format_number(signal.previous, signal.unit),
            "change_text": format_signal_change(signal.change, signal.unit),
            "severity": signal.severity,
            "why": why,
            "interpretation": signal.interpretation,
        }

    def metric_item(metric_id: str, priority: str, why: str) -> Optional[Dict[str, Any]]:
        metric = mm.get(metric_id)
        if not metric:
            return None
        return {
            "type": "metric",
            "id": metric.id,
            "label": rate_label(metric.id),
            "priority": priority,
            "value_text": format_number(metric.value, metric.unit),
            "previous_text": format_number(metric.previous, metric.unit),
            "change_text": format_change(metric.change, metric.unit),
            "severity": "缺失" if metric.status != "ok" else "中性",
            "why": why,
            "interpretation": RATE_MEANINGS.get(metric.id, metric.name),
            "as_of": metric.as_of,
            "frequency": DATA_FREQUENCY_RULES.get(metric.id, (metric.frequency, "", ""))[0],
        }

    def compact(items: List[Optional[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        return [item for item in items if item]

    return {
        "core": compact([
            # EFFR-IORB 已移除：GSE结构性压低，信号噪声大；SOFR-IORB 优先级更高
            # SOFR_EFFR 已移除：日常监测价值有限
            signal_item("SOFR_ANCHOR", "P0", "回购融资是否高于政策锚"),
            metric_item("TGA", "P0", "财政抽水/放水"),
            metric_item("RRPONTSYD", "P0", "非银现金缓冲垫"),
            metric_item("WRESBAL", "P1", "银行准备金水位"),
            signal_item("UST_1Y_YIELD", "P1", "近端政策路径"),
            signal_item("REAL_10Y", "P1", "真实折现率压力"),
            signal_item("HY_CHANGE", "P1", "信用压力是否扩散"),
        ]),
        "confirm": compact([
            metric_item("OBFR", "P2", "银行融资压力是否扩散"),
            metric_item("TGCR", "P2", "三方回购融资确认"),
            metric_item("BGCR", "P2", "广义回购融资确认"),
            signal_item("BGCR_TGCR", "P2", "回购内部结构扰动"),
            signal_item("NOMINAL_10Y", "P2", "长期名义折现率"),
            signal_item("IG_CHANGE", "P2", "投资级信用融资"),
            signal_item("VIX_RISK", "P2", "证券市场风险偏好"),
            metric_item("UST_AUCTION_BTC", "P2", "国债供给吸收能力"),
            metric_item("REPO_FAILS_UST", "P2", "抵押品交割链条"),
            metric_item("DTWEXBGS", "P2", "离岸美元压力"),
            signal_item("CP_PROXY", "P2", "企业短融压力代理"),
        ]),
        "background": compact([
            metric_item("SOMA", "B", "QT结构背景"),
            metric_item("DGS3", "B", "中段政策路径再定价"),
            metric_item("DGS1", "B", "近端政策路径"),
            metric_item("DGS30", "B", "长期期限溢价"),
            signal_item("UST_10Y2Y", "B", "收益率曲线斜率"),
            signal_item("UST_10Y3M", "B", "衰退/降息预期"),
            signal_item("NFCI_LEVEL", "B", "公开金融条件代理"),
        ]),
        "core_chart_ids": ["anchor_spreads_7d", "fed_liability_30d", "treasury_yields_30d", "real_yields_30d", "credit_oas_30d", "risk_appetite_30d"],
        "chart_groups": [
            {
                "id": "funding_core",
                "title": "核心资金压力",
                "description": "日常优先看：短端利差和Fed负债端水位。",
                "chart_ids": ["anchor_spreads_7d", "fed_liability_30d"],
                "default_open": True,
            },
            {
                "id": "asset_transmission",
                "title": "资产定价与传导确认",
                "description": "确认压力是否进入1Y/3Y/10Y收益率组合、长期真实折现率、曲线、信用和证券风险偏好。",
                "chart_ids": ["treasury_yields_30d", "real_yields_30d", "treasury_curve_30d", "cp_proxy_30d", "credit_oas_30d", "risk_appetite_30d"],
                "default_open": True,
            },
            {
                "id": "jpy_carry_overlay",
                "title": "日元 Carry 联动",
                "description": "观察日元融资成本、USD/JPY、JGB、CFTC仓位、NEER/REER与美日利差。",
                "chart_ids": ["jpy_usdjpy_funding_1y", "jpy_jgb_curve_1y", "jpy_cftc_position_2y", "jpy_effective_fx_3y", "us_jp_spread"],
                "default_open": True,
            },
            {
                "id": "review_background",
                "title": "背景复盘",
                "description": "复盘时再看，不占用日常交易主视图。",
                "chart_ids": ["short_rates_30d", "anchor_spreads_30d", "financial_conditions_30d"],
                "default_open": False,
            },
        ],
    }


def latest_nonfuture_date(dates: List[Optional[str]]) -> Optional[str]:
    today = now_bjt().date()
    valid: List[str] = []
    for raw in dates:
        parsed = parse_date_guess(raw)
        if not parsed:
            continue
        try:
            if datetime.fromisoformat(parsed).date() <= today:
                valid.append(parsed)
        except ValueError:
            continue
    return max(valid) if valid else None


def latest_point(rows: List[Tuple[str, float]], offset: int = 0) -> Optional[Tuple[str, float]]:
    if not rows or len(rows) <= offset:
        return None
    return rows[-1 - offset]


def first_point_before(rows: List[Tuple[str, float]], latest_date: str, lookback_days: int) -> Optional[Tuple[str, float]]:
    try:
        threshold = datetime.fromisoformat(latest_date).date() - timedelta(days=lookback_days)
    except Exception:  # noqa: BLE001
        return rows[0] if rows else None
    candidates = [(date, value) for date, value in rows if parse_date_guess(date) and datetime.fromisoformat(parse_date_guess(date)).date() <= threshold]
    return candidates[-1] if candidates else (rows[0] if rows else None)


def pct_change(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None or previous == 0:
        return None
    return (current / previous - 1.0) * 100.0


def realized_vol_from_series(rows: List[Tuple[str, float]], window: int = 20) -> Optional[float]:
    points = [value for _, value in rows[-(window + 1):] if value and value > 0]
    if len(points) < 6:
        return None
    returns = [math.log(points[i] / points[i - 1]) for i in range(1, len(points))]
    if len(returns) < 2:
        return None
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(variance) * math.sqrt(252) * 100.0


def fetch_cftc_jpy_position() -> Dict[str, Any]:
    params = urllib.parse.urlencode({
        "cftc_contract_market_code": "097741",
        "$limit": 2,
        "$order": "report_date_as_yyyy_mm_dd DESC",
    })
    url = f"https://publicreporting.cftc.gov/resource/6dca-aqww.json?{params}"
    try:
        payload = http_get_json(url, timeout=12, retries=1)
        records = payload if isinstance(payload, list) else []
        latest = records[0] if records else {}
        previous = records[1] if len(records) > 1 else {}
        long_pos = safe_float(latest.get("noncomm_positions_long_all"))
        short_pos = safe_float(latest.get("noncomm_positions_short_all"))
        open_interest = safe_float(latest.get("open_interest_all"))
        prev_long = safe_float(previous.get("noncomm_positions_long_all"))
        prev_short = safe_float(previous.get("noncomm_positions_short_all"))
        net = (long_pos - short_pos) if long_pos is not None and short_pos is not None else None
        prev_net = (prev_long - prev_short) if prev_long is not None and prev_short is not None else None
        crowded_ratio = (net / open_interest) if net is not None and open_interest else None
        return {
            "status": "ok" if net is not None else "unavailable",
            "as_of": parse_date_guess(latest.get("report_date_as_yyyy_mm_dd")),
            "value": net,
            "previous": prev_net,
            "change": (net - prev_net) if net is not None and prev_net is not None else None,
            "crowded_ratio": crowded_ratio,
            "source_url": url,
            "notes": "CFTC non-commercial JPY futures positioning; negative net means speculative JPY shorts crowded.",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "as_of": None,
            "value": None,
            "previous": None,
            "change": None,
            "crowded_ratio": None,
            "source_url": url,
            "notes": str(exc),
        }


def load_jpy_carry_history_payload() -> Optional[Dict[str, Any]]:
    path = LATEST_DIR / "jpy_carry_history.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("jpy_carry"), dict):
            return payload
    except Exception:  # noqa: BLE001
        return None
    return None


def refresh_jpy_carry_history(trigger: str) -> Optional[Dict[str, Any]]:
    script = ROOT / "scripts" / "jpy_carry_history.py"
    if not script.exists():
        return None
    try:
        subprocess.run(
            [sys.executable or "/usr/bin/python3", str(script), trigger or "更新日元carry数据", "--json"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except Exception:  # noqa: BLE001
        return load_jpy_carry_history_payload()
    return load_jpy_carry_history_payload()


def build_jpy_carry_overlay(metrics: List[Metric], signals: List[DerivedSignal]) -> Dict[str, Any]:
    history_payload = load_jpy_carry_history_payload()
    if history_payload and isinstance(history_payload.get("jpy_carry"), dict):
        jpy_carry = history_payload["jpy_carry"]
        if history_payload.get("charts") and isinstance(jpy_carry, dict):
            jpy_carry.setdefault("chart_ids", [chart.get("id") for chart in history_payload.get("charts", []) if chart.get("id")])
        return jpy_carry

    mm = metric_map(metrics)
    rows_usdjpy: List[Tuple[str, float]] = []
    rows_jgb10: List[Tuple[str, float]] = []
    rows_jpy_3m: List[Tuple[str, float]] = []
    errors: List[str] = []

    try:
        rows_usdjpy = fetch_fred_series_points("DEXJPUS", 90, "index")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"DEXJPUS unavailable: {exc}")
    try:
        rows_jgb10 = fetch_fred_series_points("IRLTLT01JPM156N", 520, "%")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"JGB10 proxy unavailable: {exc}")
    try:
        rows_jpy_3m = fetch_fred_series_points("IR3TIB01JPM156N", 520, "%")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"JPY 3M funding proxy unavailable: {exc}")

    usdjpy_latest = latest_point(rows_usdjpy)
    usdjpy_5d_base = first_point_before(rows_usdjpy, usdjpy_latest[0], 5) if usdjpy_latest else None
    usdjpy_20d_base = first_point_before(rows_usdjpy, usdjpy_latest[0], 20) if usdjpy_latest else None
    usdjpy_5d = pct_change(usdjpy_latest[1], usdjpy_5d_base[1]) if usdjpy_latest and usdjpy_5d_base else None
    usdjpy_20d = pct_change(usdjpy_latest[1], usdjpy_20d_base[1]) if usdjpy_latest and usdjpy_20d_base else None
    usdjpy_vol = realized_vol_from_series(rows_usdjpy, 20)

    us10y = mm.get("DGS10")
    us2y = mm.get("DGS2")
    vix = mm.get("VIXCLS")
    hy = mm.get("BAMLH0A0HYM2")
    jgb10_latest = latest_point(rows_jgb10)
    jgb10_prev = latest_point(rows_jgb10, 1)
    jpy3m_latest = latest_point(rows_jpy_3m)
    jpy3m_prev = latest_point(rows_jpy_3m, 1)
    cftc = fetch_cftc_jpy_position()

    us_jp_10y_spread = (us10y.value - jgb10_latest[1]) * 100.0 if us10y and us10y.value is not None and jgb10_latest else None
    us_jp_10y_prev = (us10y.previous - jgb10_prev[1]) * 100.0 if us10y and us10y.previous is not None and jgb10_prev else None
    us_jp_10y_change = (us_jp_10y_spread - us_jp_10y_prev) if us_jp_10y_spread is not None and us_jp_10y_prev is not None else None
    us_jp_short_spread = (us2y.value - jpy3m_latest[1]) * 100.0 if us2y and us2y.value is not None and jpy3m_latest else None

    score = 0.0
    reasons: List[str] = []
    if usdjpy_5d is not None:
        if usdjpy_5d <= -2.0:
            score += 2.0
            reasons.append(f"USD/JPY 5日下跌 {usdjpy_5d:.1f}%，日元快速升值，carry 平仓压力上升。")
        elif usdjpy_5d <= -1.0:
            score += 1.0
            reasons.append(f"USD/JPY 5日下跌 {usdjpy_5d:.1f}%，需要警惕日元空头回补。")
        elif usdjpy_5d >= 1.0:
            score -= 0.5
            reasons.append(f"USD/JPY 5日上涨 {usdjpy_5d:.1f}%，趋势仍支持 carry 延续。")
    if usdjpy_vol is not None:
        if usdjpy_vol >= 16.0:
            score += 2.0
            reasons.append(f"USD/JPY 20日实现波动率约 {usdjpy_vol:.1f}%，汇率波动已进入高风险区。")
        elif usdjpy_vol >= 12.0:
            score += 1.0
            reasons.append(f"USD/JPY 20日实现波动率约 {usdjpy_vol:.1f}%，波动上升会削弱 carry 风险收益。")
    if vix and vix.value is not None:
        if vix.value >= 25.0:
            score += 2.0
            reasons.append(f"VIX {vix.value:.2f}，全球风险偏好恶化，carry 去杠杆风险高。")
        elif vix.value >= 20.0:
            score += 1.0
            reasons.append(f"VIX {vix.value:.2f}，风险偏好边际转弱。")
        elif vix.value <= 17.0:
            score -= 0.5
            reasons.append(f"VIX {vix.value:.2f}，风险偏好尚可，暂未触发系统性去杠杆。")
    if us_jp_10y_change is not None and us_jp_10y_change <= -25.0:
        score += 1.0
        reasons.append(f"美日10年利差较上一期收窄 {abs(us_jp_10y_change):.0f}bp，carry 收益端吸引力下降。")
    if cftc.get("crowded_ratio") is not None and cftc["crowded_ratio"] < -0.25:
        score += 1.0
        reasons.append(f"CFTC日元投机净头寸/未平仓合约约 {cftc['crowded_ratio']:.1%}，日元空头拥挤，若汇率反转会放大回补。")
    if hy and hy.value is not None and hy.value >= 4.0:
        score += 1.0
        reasons.append(f"HY OAS {hy.value:.2f}%，信用压力上升会提高跨资产去杠杆概率。")

    score = max(0.0, min(6.0, score))
    if score >= 4.0:
        label = "偏高"
    elif score >= 2.0:
        label = "中性偏高"
    else:
        label = "中性"
    if not reasons:
        reasons.append("关键触发器未形成共振：汇率、波动率、VIX与信用利差暂未同时指向 carry unwind。")

    def card(card_id: str, label_text: str, value_text: str, change_text: str, why: str, as_of: Optional[str]) -> Dict[str, Any]:
        return {"id": card_id, "label": label_text, "value_text": value_text, "change_text": change_text, "why": why, "as_of": as_of or "NA"}

    cards = [
        card(
            "USDJPY",
            "USD/JPY（日元兑美元）",
            f"{usdjpy_latest[1]:.2f}" if usdjpy_latest else "NA",
            f"5日 {usdjpy_5d:+.1f}% / 20日 {usdjpy_20d:+.1f}%" if usdjpy_5d is not None and usdjpy_20d is not None else "NA",
            "快速下跌代表日元升值和空头回补压力；缓慢上行通常支持 carry 延续。",
            usdjpy_latest[0] if usdjpy_latest else None,
        ),
        card(
            "USDJPY_VOL",
            "USD/JPY 20日实现波动率",
            f"{usdjpy_vol:.1f}%" if usdjpy_vol is not None else "NA",
            "波动越高，carry 夏普越差",
            "carry trade 最怕汇率波动突然放大，尤其是日元升值伴随波动抬升。",
            usdjpy_latest[0] if usdjpy_latest else None,
        ),
        card(
            "US_JP_10Y_SPREAD",
            "美日10Y利差",
            f"{us_jp_10y_spread:.0f}bp" if us_jp_10y_spread is not None else "NA",
            format_signal_change(us_jp_10y_change, "bp"),
            "长端利差代表收益端吸引力；快速收窄会削弱海外持债和 carry 激励。",
            min(us10y.as_of, jgb10_latest[0]) if us10y and us10y.as_of and jgb10_latest else None,
        ),
        card(
            "US_JP_SHORT_SPREAD",
            "美日短端利差代理",
            f"{us_jp_short_spread:.0f}bp" if us_jp_short_spread is not None else "NA",
            "JPY 3M为月频代理",
            "短端利差越宽，融资日元买美元资产的收益激励越强；收窄则提高平仓风险。",
            min(us2y.as_of, jpy3m_latest[0]) if us2y and us2y.as_of and jpy3m_latest else None,
        ),
        card(
            "CFTC_JPY",
            "CFTC日元投机净头寸",
            f"{cftc['value']:,.0f}" if cftc.get("value") is not None else "NA",
            f"变化 {cftc['change']:,.0f}" if cftc.get("change") is not None else cftc.get("status", "NA"),
            "负值代表投机资金净做空日元；越拥挤，遇到日元升值时越容易踩踏回补。",
            cftc.get("as_of"),
        ),
        card(
            "GLOBAL_RISK",
            "全球风险偏好确认",
            f"VIX {vix.value:.2f}" if vix and vix.value is not None else "NA",
            f"HY OAS {hy.value:.2f}%" if hy and hy.value is not None else "HY OAS NA",
            "VIX和信用利差同步上行时，carry trade 更容易从收益策略变成融资回补风险。",
            vix.as_of if vix else None,
        ),
    ]

    sources = [
        {"name": "FRED / Federal Reserve", "items": ["DEXJPUS USD/JPY", "DGS2/DGS10 美债收益率", "VIXCLS", "HY OAS"]},
        {"name": "OECD via FRED", "items": ["IRLTLT01JPM156N 日本10年国债收益率（月频）", "IR3TIB01JPM156N 日本3个月利率代理（月频）"]},
        {"name": "CFTC Public Reporting", "items": ["JPY futures non-commercial net positions，周频背景"]},
        {"name": "缺口", "items": ["FX options implied vol", "risk reversal", "true cross-currency basis 通常为商业数据，当前未接入"]},
    ]
    if errors or cftc.get("status") != "ok":
        sources.append({"name": "本次降级", "items": errors + ([f"CFTC: {cftc.get('notes')}" ] if cftc.get("status") != "ok" else [])})

    return {
        "meta": {"lookback": "USD/JPY 90天；JGB/JPY短端代理约520天；CFTC周频最新2期", "note": "日元 carry 风险不是只看 USD/JPY，必须结合利差、波动、仓位和全球风险偏好。"},
        "risk": {"label": label, "score": round(score, 1), "reasons": reasons[:5]},
        "cards": cards,
        "sources": sources,
    }


def build_dashboard_data(trigger: str, generated: str, context: Dict[str, Any], metrics: List[Metric], signals: List[DerivedSignal], charts_payload: Dict[str, Any], chart_paths: List[str]) -> Dict[str, Any]:
    data_as_of = latest_nonfuture_date([m.as_of for m in metrics])
    jpy_history = load_jpy_carry_history_payload()
    if jpy_history and jpy_history.get("charts"):
        existing_chart_ids = {chart.get("id") for chart in charts_payload.get("charts", [])}
        charts_payload = {**charts_payload, "charts": [*charts_payload.get("charts", []), *[chart for chart in jpy_history.get("charts", []) if chart.get("id") not in existing_chart_ids]]}
    return {
        "meta": {
            "title": "美元流动性监测",
            "trigger": trigger or "默认运行",
            "generated_at_bjt": generated,
            "data_as_of": data_as_of,
            "timezone": "BJT",
            "theme": "warm_claude",
            "version": "1.0",
        },
        "status_scale": {
            "values": ["宽松", "中性偏松", "中性", "中性偏紧", "紧张"],
            "current_from_rule": context.get("stance"),
            "score_from_rule": context.get("score"),
        },
        "trading_dashboard": build_trading_dashboard(metrics, signals),
        "jpy_carry": build_jpy_carry_overlay(metrics, signals),
        "indicator_groups": group_indicators(metrics),
        "derived_signals": [
            {
                "id": s.id,
                "label": s.name,
                "value": s.value,
                "value_text": format_number(s.value, s.unit),
                "previous": s.previous,
                "previous_text": format_number(s.previous, s.unit),
                "change": s.change,
                "change_text": format_signal_change(s.change, s.unit),
                "unit": s.unit,
                "severity": s.severity,
                "meaning": s.interpretation,
            }
            for s in signals
        ],
        "core_indicator_impacts": [{"indicator": item[0], "importance": item[1], "reason": item[2]} for item in CORE_INDICATOR_IMPACTS],
        "charts": charts_payload.get("charts", []),
        "chart_paths": chart_paths,
        "data_quality": {
            "missing": [
                {"id": m.id, "label": rate_label(m.id), "reason": m.notes or m.status, "fallback": "详见缺失数据与替代指标"}
                for m in metrics
                if m.status != "ok"
            ],
            "stale": [
                {"id": m.id, "label": rate_label(m.id), "stale_days": m.stale_days}
                for m in metrics
                if freshness_label(m) == "stale"
            ],
            "degraded_sources": UNAVAILABLE_SOURCES,
        },
    }


def signal_takeaway(signal: DerivedSignal, idx: int) -> Dict[str, Any]:
    value_text = format_number(signal.value, signal.unit)
    previous_text = format_number(signal.previous, signal.unit)
    change_text = format_signal_change(signal.change, signal.unit)
    compare_text = f"当前为 {value_text}，上一期为 {previous_text}，边际变化 {change_text}。"
    titles = {
        # EFFR-IORB 已移除：GSE结构性压低，信号噪声大；SOFR-IORB 优先级更高
        # SOFR_EFFR 已移除：日常监测价值有限
        "SOFR_ANCHOR": "回购融资相对政策锚的位置",
        "RRP_LEVEL": "RRP缓冲垫是当前主要风险点",
        "TGA_FLOW": "财政现金流对准备金的边际影响",
        "CP_PROXY": "企业短融代理利差",
        "UST_10Y2Y": "10年-2年美债曲线",
        "UST_10Y3M": "10年-3个月美债曲线",
        "NFCI_LEVEL": "公开金融条件代理",
    }
    details = {
        # EFFR-IORB 已移除；SOFR-IORB 是更优的政策锚利差指标
        # SOFR_EFFR 已移除：日常监测价值有限
        "SOFR_ANCHOR": f"{signal.name} {compare_text}这个利差衡量国债抵押回购融资价格相对政策锚的位置；若持续转正或扩大，说明抵押融资压力高于政策利率锚，需要继续看TGCR/BGCR是否同步上行。{signal.interpretation}",
        "BGCR_TGCR": f"{signal.name} {compare_text}它观察广义一般抵押品利率与三方一般抵押品利率之间是否出现结构性背离；若扩大，说明回购市场内部可能有扰动。{signal.interpretation}",
        "RRP_LEVEL": f"{signal.name} {compare_text}RRP是货币基金等机构停放在美联储的缓冲垫；余额越低，后续TGA补库或QT造成的冲击越容易直接落到银行准备金。{signal.interpretation}",
        "TGA_FLOW": f"{signal.name} {compare_text}TGA上升通常抽走银行准备金，下降通常释放准备金。这个指标应和RRP、WRESBAL一起看，不应单独决定总判断。{signal.interpretation}",
        "CP_PROXY": f"{signal.name} {compare_text}这是用90天AA非金融商业票据利率减政策上限构造的企业短融压力代理；它不是FRA-OIS，也不是银行间流动性核心指标，只用于观察压力是否传导到企业短期融资。{signal.interpretation}",
        "UST_10Y2Y": f"{signal.name} {compare_text}它衡量政策路径预期和长期增长/期限溢价之间的差异；倒挂加深通常意味着短端政策偏紧且市场预期未来增长走弱或降息。{signal.interpretation}",
        "UST_10Y3M": f"{signal.name} {compare_text}它把长期利率和当前政策短端作比较，常用于观察衰退与后续降息预期。{signal.interpretation}",
        "NFCI_LEVEL": f"{signal.name} {compare_text}这是公开可取的综合金融条件代理，不是高盛FCI；正值代表金融条件紧于历史均值，负值代表偏松。{signal.interpretation}",
    }
    return {
        "title": titles.get(signal.id, f"关键变化 {idx + 1}"),
        "text": details.get(signal.id, f"{signal.name} {compare_text}状态为{signal.severity}。{signal.interpretation}"),
        "related_indicators": [signal.id],
    }


def metric_value_text_from_dict(metric: Optional[Dict[str, Any]]) -> str:
    if not metric:
        return "NA"
    return format_number(metric.get("value"), metric.get("unit", ""))


def signal_value_text(signal: Optional[DerivedSignal]) -> str:
    if not signal:
        return "NA"
    return format_number(signal.value, signal.unit)


def build_transmission_chain(context: Dict[str, Any], signals: List[DerivedSignal]) -> Dict[str, Any]:
    metrics = {str(m.get("id", "")).upper(): m for m in context.get("metrics", []) if isinstance(m, dict)}
    signal_map = {s.id: s for s in signals}

    def signal_status(signal_ids: List[str], metric_ids: Optional[List[str]] = None) -> str:
        selected = [signal_map.get(signal_id) for signal_id in signal_ids if signal_map.get(signal_id)]
        if any(s.severity in {"紧张", "偏紧"} for s in selected):
            return "偏紧"
        if any(s.severity == "缺失" for s in selected):
            return "数据缺口"
        if any(s.severity == "偏松" for s in selected):
            return "偏松"
        if metric_ids and any((metrics.get(metric_id) or {}).get("status") not in {None, "ok"} for metric_id in metric_ids):
            return "数据缺口"
        return "中性"

    def problem_type(status: str) -> str:
        if status == "数据缺口":
            return "data"
        if status in {"偏紧", "紧张"}:
            return "market"
        return "none"

    def node(node_id: str, label: str, role: str, status: str, evidence: List[str], diagnosis: str) -> Dict[str, Any]:
        ptype = problem_type(status)
        return {
            "id": node_id,
            "label": label,
            "role": role,
            "status": status,
            "is_problem_area": ptype != "none",
            "problem_type": ptype,
            "evidence": evidence,
            "diagnosis": diagnosis,
        }

    tga = metrics.get("TGA")
    rrp = metrics.get("RRPONTSYD")
    wresbal = metrics.get("WRESBAL")
    iorb = metrics.get("IORB")
    policy_upper = metrics.get("POLICY_UPPER_NYFED") or metrics.get("DFEDTARU")
    effr = metrics.get("EFFR")
    sofr = metrics.get("SOFR")
    obfr = metrics.get("OBFR")
    usd = metrics.get("DTWEXBGS")
    cp = metrics.get("DCPN3M")
    ig = metrics.get("BAMLC0A0CM")
    hy = metrics.get("BAMLH0A0HYM2")
    dgs1 = metrics.get("DGS1")
    dgs3 = metrics.get("DGS3")
    dgs10 = metrics.get("DGS10")
    real_10y = metrics.get("DFII10")
    curve_10y2y = metrics.get("T10Y2Y")
    curve_10y3m = metrics.get("T10Y3M")
    vix = metrics.get("VIXCLS")
    nfci = metrics.get("NFCI")

    nodes = [
        node(
            "fed_liability",
            "Fed负债端水位",
            "TGA/RRP/WRESBAL 决定准备金缓冲空间",
            signal_status(["TGA_FLOW", "RRP_LEVEL"], ["TGA", "RRPONTSYD", "WRESBAL"]),
            [
                f"TGA（财政部一般账户）{metric_value_text_from_dict(tga)}，变化 {format_change(tga.get('change'), tga.get('unit', '')) if tga else 'NA'}",
                f"RRP（隔夜逆回购）{metric_value_text_from_dict(rrp)}，变化 {format_change(rrp.get('change'), rrp.get('unit', '')) if rrp else 'NA'}",
                f"WRESBAL（银行准备金余额）{metric_value_text_from_dict(wresbal)}（周频背景）",
            ],
            "先看负债端是否抽走或释放准备金；若TGA快速上升或RRP缓冲过低，这一层先出问题。",
        ),
        node(
            "reserve_anchor",
            "政策锚/准备金边际",
            "IORB 是准备金报酬锚，SOFR 相对锚的位置观察准备金稀缺",
            signal_status(["SOFR_ANCHOR"], ["IORB"]),
            [
                f"IORB（准备金余额利率）{metric_value_text_from_dict(iorb)}；若缺失则降级看 {metric_value_text_from_dict(policy_upper)} 的政策上限",
                f"SOFR-IORB/Policy Anchor 当前 {signal_value_text(signal_map.get('SOFR_ANCHOR'))}",
            ],
            "如果SOFR接近或高于政策锚，说明回购融资端准备金边际开始变紧；若IORB缺失，这是数据层问题，不等同市场紧张。",
        ),
        node(
            "unsecured_funding",
            "银行间无抵押融资",
            "EFFR/OBFR 观察银行间隔夜融资是否同步抬升",
            signal_status([], ["EFFR", "OBFR"]),
            [
                f"EFFR（有效联邦基金利率）{metric_value_text_from_dict(effr)}，变化 {format_change(effr.get('change'), effr.get('unit', '')) if effr else 'NA'}",
                f"OBFR（隔夜银行融资利率）{metric_value_text_from_dict(obfr)}，变化 {format_change(obfr.get('change'), obfr.get('unit', '')) if obfr else 'NA'}",
            ],
            "这一层若与政策锚利差上行，代表准备金稀缺开始体现在银行间资金价格上。",
        ),
        node(
            "repo_collateral",
            "回购融资/抵押品链条",
            "SOFR/TGCR/BGCR 与国债拍卖、repo fails 确认抵押融资压力",
            signal_status(["SOFR_ANCHOR", "BGCR_TGCR", "AUCTION_BTC"], ["SOFR", "TGCR", "BGCR", "UST_AUCTION_BTC", "REPO_FAILS_UST"]),
            [
                f"SOFR（担保隔夜融资利率）{metric_value_text_from_dict(sofr)}，变化 {format_change(sofr.get('change'), sofr.get('unit', '')) if sofr else 'NA'}",
                f"SOFR-Policy Anchor 当前 {signal_value_text(signal_map.get('SOFR_ANCHOR'))}",
                f"BGCR-TGCR 当前 {signal_value_text(signal_map.get('BGCR_TGCR'))}",
            ],
            "若SOFR高于政策锚，问题从银行间扩散到回购/抵押品融资。",
        ),
        node(
            "bond_pricing",
            "债券定价锚/收益率曲线",
            "1年期反映近端政策路径，3年期观察中段再定价，10年期和实际利率决定长期贴现率",
            signal_status(["UST_1Y_YIELD", "NOMINAL_10Y", "REAL_10Y", "UST_10Y2Y", "UST_10Y3M"], ["DGS1", "DGS3", "DGS10", "DFII10", "T10Y2Y", "T10Y3M"]),
            [
                f"1Y Treasury Yield（1年期美国国债收益率）{metric_value_text_from_dict(dgs1)}，近端政策路径信号 {signal_value_text(signal_map.get('UST_1Y_YIELD'))}",
                f"3Y Treasury Yield（3年期美国国债收益率）{metric_value_text_from_dict(dgs3)}",
                f"10Y Treasury Yield（10年期美国国债收益率）{metric_value_text_from_dict(dgs10)}，名义折现率信号 {signal_value_text(signal_map.get('NOMINAL_10Y'))}",
                f"10Y Real Yield（10年期TIPS实际收益率）{metric_value_text_from_dict(real_10y)}，真实折现率信号 {signal_value_text(signal_map.get('REAL_10Y'))}",
                f"10Y-2Y / 10Y-3M 曲线：{metric_value_text_from_dict(curve_10y2y)} / {metric_value_text_from_dict(curve_10y3m)}",
            ],
            "若1年期和3年期收益率上行、真实收益率上行或曲线倒挂加深，压力会从政策路径和债券久期进入证券估值。"
        ),
        node(
            "offshore_usd",
            "离岸美元",
            "美元指数作为跨境美元压力的替代观察",
            signal_status(["USD_CHANGE"], ["DTWEXBGS"]),
            [
                f"DTWEXBGS（广义美元指数）{metric_value_text_from_dict(usd)}，变化 {format_change(usd.get('change'), usd.get('unit', '')) if usd else 'NA'}",
            ],
            "若美元指数明显上行且前端融资指标同步偏紧，说明压力可能外溢到海外美元融资。",
        ),
        node(
            "credit_market",
            "信用市场/金融条件",
            "CP、IG/HY OAS和NFCI确认压力是否进入企业融资和广义金融条件",
            signal_status(["CP_PROXY", "IG_CHANGE", "HY_CHANGE", "NFCI_LEVEL"], ["DCPN3M", "BAMLC0A0CM", "BAMLH0A0HYM2", "NFCI"]),
            [
                f"CP Rate-Policy Upper Proxy 当前 {signal_value_text(signal_map.get('CP_PROXY'))}",
                f"IG OAS（投资级公司债期权调整利差）{metric_value_text_from_dict(ig)}，变化 {format_change(ig.get('change'), ig.get('unit', '')) if ig else 'NA'}",
                f"HY OAS（高收益债期权调整利差）{metric_value_text_from_dict(hy)}，变化 {format_change(hy.get('change'), hy.get('unit', '')) if hy else 'NA'}",
                f"NFCI（芝加哥联储全国金融条件指数）{metric_value_text_from_dict(nfci)}",
            ],
            "若IG/HY利差扩张或NFCI转正，说明资金利率压力已经进入企业融资和广义金融条件。",
        ),
        node(
            "securities_risk",
            "证券市场风险偏好",
            "VIX观察利率和信用压力是否转化为股票波动率和避险需求",
            signal_status(["VIX_RISK"], ["VIXCLS"]),
            [
                f"VIX（标普500隐含波动率指数）{metric_value_text_from_dict(vix)}，证券风险信号 {signal_value_text(signal_map.get('VIX_RISK'))}",
            ],
            "若真实收益率、信用利差和VIX同步上行，传导已经从利率市场扩散到证券市场风险偏好。",
        ),
    ]

    market_problem = next((item for item in nodes if item["problem_type"] == "market"), None)
    data_problem = next((item for item in nodes if item["problem_type"] == "data"), None)
    focus = market_problem or data_problem
    current_layer = focus["label"] if focus else "未发现明显断点"
    return {
        "nodes": nodes,
        "problem_layer": current_layer,
        "problem_type": focus["problem_type"] if focus else "none",
        "summary": f"当前问题主要位于{current_layer}。" if focus else "完整传导链未显示明显市场断点，继续监控负债端和短端融资。",
    }






def build_fallback_risk_flags(signals: List[DerivedSignal], metrics: List[Metric]) -> List[Dict[str, Any]]:
    priority_order = ["SOFR_ANCHOR", "TGA_FLOW", "RRP_LEVEL", "REAL_10Y", "NOMINAL_10Y", "HY_CHANGE", "IG_CHANGE", "VIX_RISK", "USD_CHANGE", "NFCI_LEVEL", "CP_PROXY", "UST_10Y2Y", "UST_10Y3M"]
    priority_index = {signal_id: idx for idx, signal_id in enumerate(priority_order)}
    risky_signals = [s for s in signals if s.severity in {"偏紧", "紧张", "缺失"}]
    risky_signals = sorted(risky_signals, key=lambda s: priority_index.get(s.id, 99))
    flags: List[Dict[str, Any]] = []
    for idx, signal in enumerate(risky_signals[:5]):
        risk_type = "data" if signal.severity == "缺失" else "market"
        severity = "info" if risk_type == "data" else ("high" if idx < 2 else "medium")
        flags.append({
            "priority": "P0" if idx < 2 else ("P1" if idx < 4 else "P2"),
            "severity": severity,
            "type": risk_type,
            "title": signal.name,
            "text": signal.interpretation,
            "evidence": [
                f"最新值：{format_number(signal.value, signal.unit)}",
                f"上一期：{format_number(signal.previous, signal.unit)}",
                f"边际变化：{format_signal_change(signal.change, signal.unit)}",
            ],
            "related_indicators": [signal.id],
        })
    if len(flags) < 5:
        data_gaps = [m for m in metrics if m.status != "ok" or freshness_label(m) == "stale"]
        for metric in data_gaps[: 5 - len(flags)]:
            flags.append({
                "priority": "P2",
                "severity": "info",
                "type": "data",
                "title": f"{rate_label(metric.id)} 数据滞后或降级",
                "text": metric.notes or "该指标本次不能作为最新市场压力判断，只能作为数据风险处理。",
                "evidence": [f"as_of：{metric.as_of or 'NA'}", f"stale_days：{metric.stale_days if metric.stale_days is not None else 'NA'}"],
                "related_indicators": [metric.id],
            })
    return flags[:5]




def build_fallback_analysis(generated: str, context: Dict[str, Any], signals: List[DerivedSignal], highlights: List[str]) -> Dict[str, Any]:
    stance = context.get("stance", "中性")
    metrics = [Metric(**m) for m in context.get("metrics", [])]
    priority = {"SOFR_ANCHOR": 0, "TGA_FLOW": 1, "RRP_LEVEL": 2, "UST_1Y_YIELD": 3, "REAL_10Y": 4, "NOMINAL_10Y": 5, "HY_CHANGE": 6, "IG_CHANGE": 7, "VIX_RISK": 8, "UST_10Y2Y": 9, "UST_10Y3M": 10, "NFCI_LEVEL": 11, "CP_PROXY": 12}
    selected = sorted(signals, key=lambda s: priority.get(s.id, 99))[:5]
    data_as_of = latest_nonfuture_date([m.as_of for m in metrics])
    return {
        "meta": {
            "generated_at_bjt": generated,
            "data_as_of": data_as_of,
            "model": "rule_summary",
            "input_freshness_note": "脚本自动摘要，模型分析后更新。",
        },
        "stance": {
            "label": stance,
            "score_text": f"规则分数 {context.get('score', 0):.1f}",
            "one_liner": f"今日美元流动性整体判断为{stance}。",
            "confidence": "中等",
        },
        "key_takeaways": [signal_takeaway(signal, idx) for idx, signal in enumerate(selected)],
        "risk_flags": build_fallback_risk_flags(signals, metrics),
        "narrative_blocks": {
            "summary": f"今日美元流动性整体{stance}。",
            "rates": "短端资金利率重点看相对政策锚的位置，尤其是SOFR-IORB。",
            "balance_sheet": "TGA、RRP与准备金水位决定负债端缓冲空间，RRP需要区分边际方向和存量缓冲垫。",
            "market_transmission": "信用、离岸美元、真实收益率和VIX用于确认压力是否外溢到证券市场。",
        },
    }

def build_report(trigger: str, metrics: List[Metric], signals: List[DerivedSignal], score: float, highlights: List[str], chart_paths: Optional[List[str]] = None) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    generated = now_bjt().strftime("%Y-%m-%d %H:%M:%S %Z")
    stance = stance_from_score(score)

    metric_rows = []
    for m in metrics:
        metric_rows.append(
            [
                m.category,
                m.id,
                m.name,
                format_number(m.value, m.unit),
                format_change(m.change, m.unit),
                m.as_of or "NA",
                m.frequency,
                freshness_label(m),
            ]
        )

    signal_rows = []
    for s in signals:
        signal_rows.append([s.name, format_number(s.value, s.unit), s.severity, s.interpretation])

    unavailable_rows = [[x["name"], x["reason"], x["proxy"]] for x in UNAVAILABLE_SOURCES]

    errors = [m for m in metrics if m.status not in {"ok"}]
    error_lines = [f"- {m.id}: {m.status}; {m.notes}" for m in errors]

    top_highlights = highlights[:5] if highlights else ["未发现明显单点压力，需结合数据新鲜度继续观察。"]

    model_input = build_model_input_package(trigger, generated, stance, score, metrics, signals, highlights, chart_paths)
    context = {
        "trigger": trigger,
        "generated_at_bjt": generated,
        "stance": stance,
        "score": score,
        "metrics": [asdict(m) for m in metrics],
        "derived_signals": [asdict(s) for s in signals],
        "unavailable_sources": UNAVAILABLE_SOURCES,
        "model_prompt": load_prompt(),
        "intro_document_path": str(INTRO_PATH),
        "analysis_prompt_path": str(PROMPT_PATH),
        "data_frequency_rules": DATA_FREQUENCY_RULES,
        "core_indicator_impacts": CORE_INDICATOR_IMPACTS,
        "chart_paths": chart_paths or [],
        "model_input_schema": "See usd_liquidity_model_input_*.json generated in the same output run.",
    }

    report = f"""# 美元流动性日度简报

生成时间：{generated}
触发语：{trigger or "默认运行"}

## 1. 今日结论

总判断：{stance}

规则分数：{score:.1f}。该分数只用于排序风险，不是投资建议。

关键依据：
"""
    for item in top_highlights:
        report += f"- {item}\n"

    report += "\n## 2. 利率表\n\n"
    report += render_rate_summary_table(metrics)

    report += "\n\n## 3. 对流动性影响较大的指标\n\n"
    report += render_core_indicator_impact_table()

    report += "\n\n## 4. 最近一周/一月图表\n\n"
    if chart_paths:
        for path in chart_paths:
            report += f"- {Path(path).name}\n"
    else:
        report += "- 本次未生成图表，可能是时序接口暂时不可用。\n"

    report += "\n## 5. 数据频率与环比口径\n\n"
    report += "说明：环比只比较同频率的上一条有效观测；日频不和周频混比，事件型数据只和上一事件比较。\n\n"
    report += render_frequency_table(metrics)

    report += "\n\n## 6. 关键利差、核心数据与数据质量\n\n"
    report += "### 6.1 关键利差和衍生信号\n\n"
    report += markdown_table(["信号", "数值", "状态", "解释"], signal_rows)

    report += "\n\n### 6.2 数据新鲜度与核心指标\n\n"
    report += markdown_table(["模块", "代码", "指标", "最新值", "变化", "日期", "频率", "状态"], metric_rows)

    report += "\n\n### 6.3 国债/抵押品观察\n\n"
    auction = metric_map(metrics).get("UST_AUCTION_BTC")
    fails = metric_map(metrics).get("REPO_FAILS_UST")
    if auction and auction.value is not None:
        auction_desc = auction.extra.get("latest_auction", {})
        security = " ".join(str(auction_desc.get(k, "")).strip() for k in ("securityType", "securityTerm") if auction_desc.get(k))
        security_label = security or "未识别券种"
        report += f"- 最近拍卖 bid-to-cover 为 {format_number(auction.value, auction.unit)}，日期 {auction.as_of}。{security_label}。\n"
    else:
        report += "- 最近国债拍卖数据未能稳定获取，脚本已降级，不影响其他模块。\n"
    if fails and fails.value is not None:
        report += f"- Repo fails 最近值 {format_number(fails.value, fails.unit)}，日期 {fails.as_of}，周频背景信号。\n"
    else:
        report += "- Repo fails 为周频/可选源，本次未作为日度核心判断。\n"

    report += "\n### 6.4 缺失数据与接口降级\n\n"
    report += markdown_table(["缺失项", "原因", "替代观察"], unavailable_rows)
    if error_lines:
        report += "\n\n" + "\n".join(error_lines)
    else:
        report += "\n\n- 无关键接口错误。"

    return report, context, model_input


def write_outputs(
    report: str,
    context: Dict[str, Any],
    model_input: Dict[str, Any],
    dashboard_data: Dict[str, Any],
    analysis: Dict[str, Any],
    charts_payload: Dict[str, Any],
    stamp: str,
) -> Dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "report_path": OUTPUT_DIR / f"usd_liquidity_brief_{stamp}.md",
        "json_path": OUTPUT_DIR / f"usd_liquidity_snapshot_{stamp}.json",
        "model_input_path": OUTPUT_DIR / f"usd_liquidity_model_input_{stamp}.json",
        "dashboard_data_path": OUTPUT_DIR / f"usd_liquidity_dashboard_data_{stamp}.json",
        "analysis_path": OUTPUT_DIR / f"usd_liquidity_analysis_{stamp}.json",
        "charts_json_path": OUTPUT_DIR / f"usd_liquidity_charts_{stamp}.json",
    }
    paths["report_path"].write_text(report, encoding="utf-8")
    paths["json_path"].write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["model_input_path"].write_text(json.dumps(model_input, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["dashboard_data_path"].write_text(json.dumps(dashboard_data, ensure_ascii=False, indent=2), encoding="utf-8")
    if analysis is not None:
        paths["analysis_path"].write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["charts_json_path"].write_text(json.dumps(charts_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    latest_map = {
        "snapshot.json": context,
        "model_input.json": model_input,
        "dashboard_data.json": dashboard_data,
        "charts.json": charts_payload,
    }
    if analysis is not None:
        latest_map["analysis.json"] = analysis
    for filename, payload in latest_map.items():
        (LATEST_DIR / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Generate data.js for inline data (avoids fetch/CORS issues in preview panel)
    frontend_dir = ROOT / "frontend" / "usd-liquidity-monitor"
    if frontend_dir.exists() and analysis is not None:
        data_js = f"window.DASHBOARD_DATA = {json.dumps(dashboard_data, ensure_ascii=False, indent=2)};\nwindow.ANALYSIS_DATA = {json.dumps(analysis, ensure_ascii=False, indent=2)};\n"
        (frontend_dir / "data.js").write_text(data_js, encoding="utf-8")

    return paths


def cleanup_old_outputs(current_stamp: str) -> int:
    patterns = [
        "usd_liquidity_brief_*.md",
        "usd_liquidity_snapshot_*.json",
        "usd_liquidity_model_input_*.json",
        "usd_liquidity_dashboard_data_*.json",
        "usd_liquidity_analysis_*.json",
        "usd_liquidity_charts_*.json",
        "usd_liquidity_chart_*.svg",
    ]
    removed = 0
    for pattern in patterns:
        for path in OUTPUT_DIR.glob(pattern):
            if current_stamp in path.name:
                continue
            if path.is_file():
                path.unlink()
                removed += 1
    return removed


def load_snapshot(path: Path) -> Tuple[List[Metric], List[DerivedSignal], float, List[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = [Metric(**item) for item in payload.get("metrics", [])]
    if payload.get("derived_signals"):
        signals = [DerivedSignal(**item) for item in payload.get("derived_signals", [])]
        score = safe_float(payload.get("score")) or 0.0
        highlights = [f"{s.name}: {format_number(s.value, s.unit)}，{s.interpretation}" for s in signals if s.severity in {"偏紧", "紧张", "偏松"}]
    else:
        signals, score, highlights = derive_signals(metrics)
    return metrics, signals, score, highlights


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch USD liquidity data and generate a daily briefing")
    parser.add_argument("trigger", nargs="*", help="Natural-language trigger, e.g. 今天美元流动性如何")
    parser.add_argument("--auction-lookback-days", type=int, default=21, help="Lookback window for Treasury auctions")
    parser.add_argument("--input-json", help="Reuse an existing usd_liquidity_snapshot_*.json instead of fetching live data")
    parser.add_argument("--model-input-only", action="store_true", help="Still writes all files, but console output focuses on model_input_path")
    parser.add_argument("--no-charts", action="store_true", help="Skip SVG chart generation")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output paths as JSON")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    trigger = " ".join(args.trigger).strip()
    if args.input_json:
        metrics, signals, score, highlights = load_snapshot(Path(args.input_json))
    else:
        metrics = fetch_all_metrics(args.auction_lookback_days)
        signals, score, highlights = derive_signals(metrics)
    stamp = now_bjt().strftime("%Y%m%d_%H%M%S")
    chart_paths: List[str] = []
    series_bundle: Dict[str, List[Tuple[str, float]]] = {}
    if not args.no_charts:
        try:
            series_bundle = fetch_chart_series(45)
            chart_paths = [str(path) for path in write_liquidity_charts(stamp, series_bundle)]
        except Exception as exc:  # noqa: BLE001
            highlights.append(f"图表生成失败：{exc}")
    refresh_jpy_carry_history(trigger or "更新日元carry数据")
    charts_payload = build_charts_payload(series_bundle)
    report, context, model_input = build_report(trigger, metrics, signals, score, highlights, chart_paths)
    generated = context["generated_at_bjt"]
    dashboard_data = build_dashboard_data(trigger, generated, context, metrics, signals, charts_payload, chart_paths)
    analysis = build_fallback_analysis(generated, context, signals, highlights)  # 每次写入 rule_fallback，避免 latest/analysis.json 残留旧模型结果；正式模型分析可再覆盖。
    output_paths = write_outputs(report, context, model_input, dashboard_data, analysis, charts_payload, stamp)
    # 落库：将 snapshot 写入历史 SQLite DB
    try:
        import subprocess
        from pathlib import Path as Path2
        snapshot_path = output_paths["json_path"]
        ingest_script = Path2(__file__).parent / "ingest_snapshot.py"
        result = subprocess.run(
            ["python3", str(ingest_script), str(snapshot_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"[DB] 历史库已更新：{snapshot_path.name}")
        else:
            print(f"[DB] 落库警告：{result.stderr.strip()[:200]}")
    except Exception as db_exc:
        print(f"[DB] 落库失败：{db_exc}")
    cleanup_removed = cleanup_old_outputs(stamp)

    if args.json:
        print(json.dumps({**{key: str(value) for key, value in output_paths.items()}, "latest_dir": str(LATEST_DIR), "chart_paths": chart_paths, "cleanup_removed": cleanup_removed, "stance": context["stance"], "score": context["score"]}, ensure_ascii=False))
    else:
        print(f"美元流动性总判断：{context['stance']} | 分数：{context['score']:.1f}")
        print(f"Markdown简报：{output_paths['report_path']}")
        print(f"JSON快照：{output_paths['json_path']}")
        print(f"模型输入包：{output_paths['model_input_path']}")
        print(f"前端数据：{output_paths['dashboard_data_path']}")
        print(f"分析结果：{output_paths['analysis_path']}")
        print(f"最新数据目录：{LATEST_DIR}")
        print(f"清理旧产物：{cleanup_removed} 个")
        for chart_path in chart_paths:
            print(f"图表：{chart_path}")
        if args.model_input_only:
            print("提示：模型输入包已生成，可交给模型连同分析prompt进行最终分析。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
