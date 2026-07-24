"""Shared utilities: HTTP helpers, parsing, time, paths, constants, dataclasses."""

from __future__ import annotations

import csv
import io
import json
import math
import os
import time
import urllib.parse
import urllib.request
import requests
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# ─── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
LATEST_DIR = OUTPUT_DIR / "latest"
PROMPT_PATH = ROOT / "prompts" / "usd_liquidity_prompt.md"
INTRO_PATH = ROOT / "prompts" / "usd_liquidity_intro.md"
FRED_API_KEY_PATH = ROOT / ".workbuddy" / "secrets" / "fred_api_key"
TGA_CACHE_PATH = ROOT / ".workbuddy" / "cache" / "tga_cache.json"

# ─── Timezones ─────────────────────────────────────────────────────────────────
BJT = timezone(timedelta(hours=8))
UTC = timezone.utc

USER_AGENT = "WorkBuddy USD Liquidity Monitor/1.0"

# ─── Constants ─────────────────────────────────────────────────────────────────

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
    "SOFR_VOLUME": "SOFR Volume（SOFR交易量）",
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
    "TBILL_AUCTION_SIZE": "T-bill Auction Size（短期国债拍卖规模）",
    "TBILL_AUCTION_BTC": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
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
    "DGS5": "5Y Treasury Yield（5年期美国国债收益率）",
    "DGS7": "7Y Treasury Yield（7年期美国国债收益率）",
    "DGS10": "10Y Treasury Yield（10年期美国国债收益率）",
    "DFII10": "10Y Real Yield（10年期TIPS实际收益率）",
    "T10Y2Y": "10Y-2Y Treasury Spread（10年-2年美债利差）",
    "T10Y3M": "10Y-3M Treasury Spread（10年-3个月美债利差）",
    "VIXCLS": "VIX（标普500隐含波动率指数）",
    "NFCI": "NFCI（芝加哥联储全国金融条件指数）",
}

RATE_MEANINGS = {
    "EFFR": "银行间无抵押隔夜资金价格，最能观察准备金边际是否稀缺。",
    "SOFR": "以美国国债为抵押的隔夜融资价格，反映回购市场和抵押品融资压力。",
    "SOFR_VOLUME": "SOFR对应的隔夜回购交易量，用于把利率偏离转化为价格×规模的实际资金成本量级。",
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
    "TBILL_AUCTION_SIZE": "短期国债拍卖发行规模，观察货币基金、银行和交易商需要吸收的新增/滚续短债供给量级。",
    "TBILL_AUCTION_BTC": "短期国债拍卖投标覆盖倍数，和拍卖规模一起观察T-bill供给吸收压力。",
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
    "DGS5": "5年期美国国债收益率，处于曲线腹部，观察短端政策预期向长端传导的中段再定价。",
    "DGS7": "7年期美国国债收益率，处于曲线腹部偏长端，衔接腹部再定价与长端折现率。",
    "DGS10": "10年期美国国债收益率，是全球资产折现率和长期美元资金价格的重要锚，本简报仅作曲线/折现率背景观察。",
    "DFII10": "10年期TIPS实际收益率，剔除通胀补偿后观察真实无风险回报，对成长股、黄金和长期资产估值更敏感。",
    "T10Y2Y": "10年减2年美债利差，观察收益率曲线是否倒挂以及增长/降息预期。",
    "T10Y3M": "10年减3个月美债利差，观察政策短端与长期增长预期的差异。",
    "VIXCLS": "标普500隐含波动率指数，作为证券市场风险偏好和避险需求的确认指标。",
    "NFCI": "芝加哥联储全国金融条件指数，公开金融条件代理；正值偏紧，负值偏松。",
}

RATE_CHANGE_IMPLICATIONS = {
    "EFFR": ("银行间无抵押融资边际变贵，准备金稀缺压力上升", "银行间无抵押融资边际变便宜，准备金仍较充裕"),
    "SOFR": ("回购融资边际变贵，抵押融资压力上升", "回购融资边际变便宜，资金面不紧"),
    "SOFR_VOLUME": ("SOFR交易量上升，同样的利率偏离会作用在更大的回购融资量上", "SOFR交易量下降，同样的利率偏离对应的总成本冲击变小"),
    "IORB": ("政策锚上移，整体短端利率中枢抬升", "政策锚下移，整体短端利率中枢回落"),
    "POLICY_UPPER_NYFED": ("政策上限上移，短端利率中枢抬升", "政策上限下移，短端利率中枢回落"),
    "DFEDTARU": ("政策上限上移，短端利率中枢抬升", "政策上限下移，短端利率中枢回落"),
    "OBFR": ("银行隔夜融资边际变贵，压力可能扩散到更广义融资市场", "银行隔夜融资边际变便宜，广义银行融资压力缓和"),
    "TGCR": ("三方回购融资边际变贵，抵押融资压力上升", "三方回购融资边际变便宜，抵押融资压力缓和"),
    "BGCR": ("广义回购融资边际变贵，回购链条压力上升", "广义回购融资边际变便宜，回购链条压力缓和"),
    "TBILL_AUCTION_SIZE": ("T-bill拍卖规模上升，短债供给吸收量级变大，需要结合认购倍数判断压力", "T-bill拍卖规模下降，短债供给吸收压力边际减轻"),
    "TBILL_AUCTION_BTC": ("T-bill认购倍数上升，说明在当前发行量下需求更强", "T-bill认购倍数下降，说明在当前发行量下吸收能力边际转弱"),
}

DATA_FREQUENCY_RULES = {
    "EFFR": ("日频，纽约联储约 9:00 ET 发布", "反映上一工作日交易", "与上一条有效工作日观测比较，不按自然日补零。"),
    "OBFR": ("日频，纽约联储参考利率", "通常反映上一工作日交易", "与上一条有效工作日观测比较。"),
    "SOFR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日回购交易，约 14:30 ET 可能同日修订", "与上一条有效工作日观测比较。"),
    "SOFR_VOLUME": ("日频，纽约联储SOFR记录随利率一同发布", "反映上一工作日SOFR合格交易量", "与上一条有效工作日观测比较，并与SOFR相对政策锚利差相乘理解量级。"),
    "TGCR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日三方回购交易，可能同日修订", "与上一条有效工作日观测比较。"),
    "BGCR": ("日频，纽约联储约 8:00 ET 发布", "反映上一工作日广义一般抵押品回购交易，可能同日修订", "与上一条有效工作日观测比较。"),
    "TGA": ("日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布", "覆盖上一工作日财政现金和债务操作", "与上一条有效工作日观测比较，不能与当天市场利率强行同日对齐。"),
    "RRPONTSYD": ("日频，纽约联储每日操作结果", "同日操作结果，工作日/操作日口径", "与上一条操作日观测比较。"),
    "SOMA": ("周频，纽约联储/Fed资产负债表背景数据", "周度持仓或H.4.1口径", "只与上一周比较，不能当作昨日边际变化。"),
    "WRESBAL": ("周频，H.4.1 通常周四 16:30 ET 发布", "反映周度准备金余额", "只与上一周比较，作为结构背景。"),
    "REPO_FAILS_UST": ("周频，OFR/STFM 或一级交易商口径", "交割失败周度背景", "只看周度趋势，不参与日度环比。"),
    "UST_AUCTION_BTC": ("事件驱动，财政部拍卖后公布", "只在拍卖发生时更新", "与上一场可比拍卖比较，不能日度环比。"),
    "TBILL_AUCTION_SIZE": ("事件驱动，财政部T-bill拍卖后公布", "同一拍卖日多只Bill按发行额加总", "与上一T-bill拍卖日比较，并与认购倍数一起判断供给吸收压力。"),
    "TBILL_AUCTION_BTC": ("事件驱动，财政部T-bill拍卖后公布", "同一拍卖日多只Bill按发行额加权平均", "与上一T-bill拍卖日比较；必须结合拍卖规模，不能只看倍数。"),
    "DTWEXBGS": ("日频，FRED/美联储美元指数口径", "通常随源数据滞后更新", "与上一条有效观测比较，注意可能比资金利率更滞后。"),
    "DCPN3M": ("日频，商业票据利率", "通常T+1或随源数据更新", "与上一条有效观测比较。"),
    "BAMLH0A0HYM2": ("日频，高收益债OAS", "通常随ICE/BofA数据更新", "与上一条有效观测比较，作为信用传导而非银行间流动性核心。"),
    "BAMLC0A0CM": ("日频，投资级公司债OAS", "通常随ICE/BofA数据更新", "与上一条有效观测比较，作为高等级信用融资条件确认。"),
    "DTB3": ("日频，3个月国库券二级市场利率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看现金替代收益。"),
    "DGS3MO": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看政策短端。"),
    "DGS1": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看未来一年政策路径。"),
    "DGS2": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看政策路径预期。"),
    "DGS3": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看中段政策路径再定价。"),
    "DGS5": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看腹部中段再定价。"),
    "DGS7": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看腹部偏长端再定价。"),
    "DGS10": ("日频，FRED/H.15国债恒定期限收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，本简报仅作曲线/折现率背景观察。"),
    "DFII10": ("日频，FRED/H.15 10年期TIPS实际收益率", "通常随H.15数据发布滞后更新", "与上一条有效观测比较，主要看真实贴现率。"),
    "T10Y2Y": ("日频，FRED曲线利差", "由10年和2年国债收益率差计算", "与上一条有效观测比较；倒挂或加深倒挂反映增长/降息预期。"),
    "T10Y3M": ("日频，FRED曲线利差", "由10年和3个月国债收益率差计算", "与上一条有效观测比较；常用于观察衰退预期。"),
    "VIXCLS": ("日频，标普500隐含波动率", "通常随CBOE/FRED数据更新", "与上一条有效观测比较，作为证券市场风险偏好确认。"),
    "NFCI": ("周频，芝加哥联储全国金融条件指数", "通常每周更新", "只与上一周比较；正值偏紧，负值偏松。"),
    "IORB": ("政策阶梯型，美联储政策利率", "只有政策调整时变化", "不做普通日度环比；用于锚定EFFR和SOFR。"),
    "DFEDTARU": ("政策阶梯型，联邦基金目标上限", "只有政策调整时变化", "不做普通日度环比；用于政策锚。"),
    "POLICY_UPPER_NYFED": ("政策阶梯型，纽约联储记录中的目标上限", "来自EFFR记录，作为IORB缺失时的临时锚", "只用于锚定，不代表市场日度变化。"),
}

CORE_INDICATOR_IMPACTS = [
    ("SOFR-IORB / SOFR-政策锚", "高", "观察回购和抵押品融资是否紧张；SOFR高于政策锚通常比单纯上升更重要。"),
    ("SOFR交易量", "高", "把SOFR相对政策锚的价格偏离映射到实际回购融资规模；利率冲击的影响取决于交易量。"),
    ("TGA", "高", "财政部现金余额上升会抽走准备金，下降会释放准备金，是Fed负债端最重要的日频水位之一。"),
    ("RRP", "高", "RRP下降可释放缓冲，但余额过低后，QT和TGA补库更容易直接冲击准备金。"),
    ("WRESBAL", "高但周频", "银行准备金本身是核心水位，但周频发布，适合看趋势而非日内或日度拐点。"),
    ("TGCR/BGCR", "中高", "帮助确认SOFR变化是否是广泛回购市场压力，而非单点噪音。"),
    ("T-bill拍卖规模 / bid-to-cover / repo fails", "中高", "观察短债供给吸收、货币基金现金分流和抵押品链条压力；拍卖倍数必须和发行规模一起看。"),
    ("1Y / 3Y / 5Y / 7Y国债收益率（腹部组合）", "中高", "1年期看近端政策路径，3年期看中段再定价，5Y/7Y看腹部传导，10年期仅作折现率背景锚。"),
    ("10Y名义/实际收益率", "背景", "DGS10名义收益率和DFII10实际收益率仅补充长期折现率背景，不替代1Y/3Y/5Y/7Y腹部主框架，且两者必须分开命名和解释。"),
    ("美元指数 / CP利差 / IG OAS / HY OAS", "中高", "观察压力是否向离岸美元和信用市场扩散，属于传导确认指标。"),
    ("10Y-2Y / 10Y-3M曲线利差", "中高", "长短端利差观察当前政策短端与增长、降息和衰退预期的相对关系。"),
    ("VIX / NFCI / FCI代理", "中", "观察利率、信用、杠杆和风险资产综合后的证券市场风险偏好与金融条件。"),
]


# ─── Dataclasses ───────────────────────────────────────────────────────────────

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
    as_of: Optional[str] = None  # 从底层metric继承的时间


# ─── Time helpers ──────────────────────────────────────────────────────────────

def now_bjt() -> datetime:
    return datetime.now(BJT)


# ─── FRED API key ─────────────────────────────────────────────────────────────

def get_fred_api_key() -> str:
    env_key = os.getenv("FRED_API_KEY", "").strip()
    if env_key:
        return env_key
    if FRED_API_KEY_PATH.exists():
        return FRED_API_KEY_PATH.read_text(encoding="utf-8").strip()
    return ""


# ─── HTTP helpers ──────────────────────────────────────────────────────────────

def http_get_text(url: str, timeout: int = 10, retries: int = 0) -> str:
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            # Try requests first (bundles certifi CA certs, avoids macOS/Python3.13 SSL issues)
            resp = requests.get(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"},
                timeout=timeout,
                verify=True,
            )
            resp.raise_for_status()
            return resp.text
        except Exception as exc:
            last_error = exc
            # Fallback to urllib (may hit SSL issues on some macOS/Python combos)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    raw = r.read()
                    charset = r.headers.get_content_charset() or "utf-8"
                    return raw.decode(charset, errors="replace")
            except Exception:
                pass
            if attempt < retries:
                time.sleep(1.0 + attempt)
    raise RuntimeError(f"GET failed: {url} | {last_error}")


def http_get_json(url: str, timeout: int = 10, retries: int = 0) -> Any:
    text = http_get_text(url, timeout=timeout, retries=retries)
    return json.loads(text)


# ─── Parsing helpers ───────────────────────────────────────────────────────────

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

    # Strip common timestamp suffixes before trying date-only formats.
    base = s.split("T", 1)[0].strip()
    for fmt in (
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y%m%d",
    ):
        try:
            candidate = s[:19] if "%H" in fmt or "T" in fmt else base
            return datetime.strptime(candidate, fmt).date().isoformat()
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


# ─── Metric helpers ────────────────────────────────────────────────────────────

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
    as_of_val = latest[0] if latest else None
    prev_as_of = previous[0] if previous else None
    return Metric(
        id=metric_id,
        name=name,
        category=category,
        value=value,
        previous=prev_value,
        change=change,
        unit=unit,
        as_of=as_of_val,
        previous_as_of=prev_as_of,
        frequency=frequency,
        source=source,
        source_url=source_url,
        status=status,
        notes=notes,
        stale_days=stale_days(as_of_val),
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


def metric_map(metrics: List[Metric]) -> Dict[str, Metric]:
    return {m.id.upper(): m for m in metrics}


# ─── Generic helpers ───────────────────────────────────────────────────────────

def walk_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_dicts(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_dicts(item)


def fiscal_amount_to_bn(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    abs_value = abs(value)
    if abs_value > 10_000_000:
        return value / 1_000_000_000.0
    if abs_value > 10_000:
        return value / 1_000.0
    return value


def align_spread(a: List[Tuple[str, float]], b: List[Tuple[str, float]], multiplier: float = 100.0) -> List[Tuple[str, float]]:
    """Compute spread series (a - b) * multiplier, aligning on date."""
    bm = {date: value for date, value in b}
    rows: List[Tuple[str, float]] = []
    for date, value in a:
        if date in bm:
            rows.append((date, (value - bm[date]) * multiplier))
    return rows


def trim_series(series: List[Tuple[str, float]], days: int) -> List[Tuple[str, float]]:
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    return [(date, value) for date, value in series if date >= cutoff]


def chart_points(series: List[Tuple[str, float]], days: int) -> List[Dict[str, Any]]:
    return [{"date": date, "value": value} for date, value in trim_series(series, days)]


# ─── Formatting helpers ────────────────────────────────────────────────────────

def format_number(value: Optional[float], unit: str, precision: int = 2) -> str:
    if value is None:
        return "NA"
    if unit == "bp":
        return f"{value:.1f}bp"
    if unit == "%":
        return f"{value:.3f}%"
    if unit == "USD bn":
        return f"{value:,.1f}bn"
    if unit == "USD mn/day":
        return f"{value:+,.1f}mn/day"
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
    if unit == "USD mn/day":
        return f"{sign}{change:,.1f}mn/day"
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
    if unit == "USD mn/day":
        return f"{sign}{change:,.1f}mn/day"
    if unit == "pt":
        return f"{sign}{change:.2f}pt"
    if unit == "x":
        return f"{sign}{change:.2f}x"
    return f"{sign}{change:.2f}{unit}"


def rate_label(metric_id: str) -> str:
    return RATE_LABELS.get(metric_id, f"{metric_id}（未配置中文名）")


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


def change_direction(change: Optional[float], unit: str) -> str:
    if change is None:
        return "unknown"
    threshold = 0.0005 if unit == "%" else 0.05
    if abs(change) <= threshold:
        return "flat"
    return "up" if change > 0 else "down"


def importance_for(metric_id: str) -> str:
    if metric_id in {"EFFR", "SOFR", "SOFR_VOLUME", "TGA", "RRPONTSYD", "WRESBAL", "IORB", "POLICY_UPPER_NYFED", "DGS1", "DGS3", "DGS10", "DFII10", "BAMLH0A0HYM2"}:
        return "high"
    if metric_id in {"OBFR", "TGCR", "BGCR", "SOMA", "UST_AUCTION_BTC", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC", "REPO_FAILS_UST", "BAMLC0A0CM", "VIXCLS", "NFCI"}:
        return "medium_high"
    return "medium"


def comparison_rule(metric: Metric) -> str:
    if "weekly" in metric.frequency:
        return "周度环比"
    if "event" in metric.frequency:
        return "上一事件/上一场拍卖"
    if "policy" in metric.frequency:
        return "政策阶梯变化，不做普通日环比"
    return "上一有效工作日/上一有效观测"


def load_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def load_prompt() -> str:
    return load_text(PROMPT_PATH)


def load_intro() -> str:
    return load_text(INTRO_PATH)


# ─── TGA cache ─────────────────────────────────────────────────────────────────

def read_tga_history(max_entries: int = 60) -> List[Tuple[str, float]]:
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
    try:
        TGA_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        history = read_tga_history(keep * 2)
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


# ─── JPY carry history payload ─────────────────────────────────────────────────

def load_jpy_carry_history_payload() -> Optional[Dict[str, Any]]:
    path = LATEST_DIR / "jpy_carry_history.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("jpy_carry"), dict):
            return payload
    except Exception:
        return None
    return None
