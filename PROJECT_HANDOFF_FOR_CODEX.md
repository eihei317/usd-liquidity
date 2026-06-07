# 美元流动性监测项目交接文档（Codex 可直接接手）

最后更新：2026-05-27 10:45 BJT

本文档用于让新的工程同学或 Codex 打开项目后，可以快速理解、运行、验证和继续迭代这个「美元流动性监测」项目。

注意：本文档不包含任何 API Key。FRED API Key 已通过工作区私密文件读取，不能写入代码、Markdown、JSON 产物或 Git。

---

## 1. 项目一句话说明

这是一个美元流动性日度监测系统：

1. Python 脚本从官方 / 权威公开 API 抓取美元流动性相关指标。
2. 脚本生成结构化数据快照、模型输入包、兜底分析结果、图表数据和 Markdown 简报。
3. 前端读取 `output/latest/dashboard_data.json` 和 `output/latest/analysis.json`，用稳定模板确定性渲染仪表盘。
4. 模型只负责产出结构化 `analysis.json`，日常运行不让模型修改前端代码。

核心原则：

- 能用 API 抓的数据全部用 API。
- 日频、周频、事件驱动、政策阶梯型数据不能混比。
- 缺失数据必须显式标注，不能当作中性。
- 判断不能只看单一指标，必须看完整传导链。
- 利率是价格信号，必须结合市场规模/交易量做“价格 × 规模”判断；SOFR 看 `SOFR_VOLUME` / `SOFR_VOLUME_IMPACT`，T-bill 看 `TBILL_AUCTION_SIZE` + `TBILL_AUCTION_BTC` / `TBILL_AUCTION_ABSORPTION`。
- 人读简报不附带模型 context 或完整 prompt；这些只存在于 model_input JSON。

---

## 2. 当前项目目录

项目根目录：

```text
/Users/eiheisun/WorkBuddy/2026-05-04-task-1
```

主要结构：

```text
.
├── scripts/
│   ├── run.py                ← 主入口（调度器）
│   ├── utils.py              ← 公共函数、常量、dataclass
│   ├── fetchers.py           ← 数据抓取（NY Fed/FRED/Treasury/OFR/CFTC）
│   ├── signals.py            ← 信号计算 + 评分 + stance 判定
│   ├── dashboard.py          ← 前端 JSON 构建 + 传导链
│   ├── analysis.py           ← fallback 分析 + 报告 + model_input
│   ├── charts.py             ← SVG 图表生成
│   ├── db.py                 ← SQLite 历史库（init + ingest）
│   ├── jpy_carry.py          ← 日元 Carry Trade 数据
│   └── _archive/             ← 重构前旧文件备份
├── prompts/
│   ├── usd_liquidity_intro.md
│   ├── usd_liquidity_prompt.md
│   └── jpy_usd_carry_liquidity_prompt.md
├── frontend/
│   └── usd-liquidity-monitor/
│       ├── index.html
│       ├── styles.css
│       ├── app.js
│       └── chart.min.js
├── output/
│   ├── latest/
│   │   ├── snapshot.json
│   │   ├── model_input.json
│   │   ├── dashboard_data.json
│   │   ├── analysis.json
│   │   ├── charts.json
│   │   ├── jpy_carry_history.json
│   │   ├── jpy_carry_analysis.json
│   │   └── jpy_carry_model_input.json
│   ├── usd_liquidity_*_YYYYMMDD_HHMMSS.*   ← 历史归档
│   ├── jpy_carry_*_YYYYMMDD_HHMMSS.json    ← JPY 历史归档
│   └── usd_liquidity.db                     ← SQLite 历史库
├── .gitignore
├── requirements.txt
├── PROJECT_HANDOFF_FOR_CODEX.md
└── .workbuddy/
    ├── memory/
    ├── cache/
    └── secrets/
        └── fred_api_key
```

重要说明：

- `.workbuddy/secrets/fred_api_key` 是私密配置文件，不应提交、不应展示、不应写入文档。
- `output/latest/` 是前端稳定读取目录。
- `output/usd_liquidity_*_timestamp.*` 是每次运行的历史归档产物，超过 10 份自动清理。

---

## 3. 运行环境

当前项目只依赖 Python 标准库和浏览器 CDN：

- Python：系统 `/usr/bin/python3` 可用。
- 前端：纯 HTML / CSS / JS。
- 图表：Chart.js（本地 vendor `chart.min.js`）。
- 不需要 `pip install`。
- 不需要 Node 构建步骤。

语法检查命令：

```bash
/usr/bin/python3 -m py_compile "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py"
```

前端 JS 语法检查：

```bash
/Users/eiheisun/.nvm/versions/node/v20.20.2/bin/node --check "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/frontend/usd-liquidity-monitor/app.js"
```

---

## 4. API Key 配置

FRED API Key 读取顺序：

1. 环境变量 `FRED_API_KEY`
2. 工作区私密文件 `.workbuddy/secrets/fred_api_key`

脚本实现位置：

```text
scripts/utils.py  （get_fred_api_key 函数）
```

相关函数：

```python
def get_fred_api_key() -> str:
    env_key = os.getenv("FRED_API_KEY", "").strip()
    if env_key:
        return env_key
    if FRED_API_KEY_PATH.exists():
        return FRED_API_KEY_PATH.read_text(encoding="utf-8").strip()
    return ""
```

配置方式一：环境变量

```bash
export FRED_API_KEY="你的FRED_API_KEY"
```

配置方式二：工作区私密文件

```bash
mkdir -p "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/.workbuddy/secrets"
chmod 700 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/.workbuddy/secrets"
printf '%s' "你的FRED_API_KEY" > "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/.workbuddy/secrets/fred_api_key"
chmod 600 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/.workbuddy/secrets/fred_api_key"
```

安全规则：

- 不要把 key 写入源码。
- 不要把 key 写入 Markdown。
- 不要把 key 写入 `output/*.json`。
- 如果输出中记录了 FRED API 请求 URL，必须用 `redact_url_secret()` 脱敏 `api_key` 查询参数。

---

## 5. 一键运行

在项目根目录外也可以运行，使用绝对路径：

```bash
/usr/bin/python3 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py" "今天美元流动性监测" --json
```

成功时会输出类似：

```json
{
  "report_path": ".../output/usd_liquidity_brief_YYYYMMDD_HHMMSS.md",
  "json_path": ".../output/usd_liquidity_snapshot_YYYYMMDD_HHMMSS.json",
  "model_input_path": ".../output/usd_liquidity_model_input_YYYYMMDD_HHMMSS.json",
  "dashboard_data_path": ".../output/usd_liquidity_dashboard_data_YYYYMMDD_HHMMSS.json",
  "analysis_path": ".../output/usd_liquidity_analysis_YYYYMMDD_HHMMSS.json",
  "charts_json_path": ".../output/usd_liquidity_charts_YYYYMMDD_HHMMSS.json",
  "latest_dir": ".../output/latest",
  "chart_paths": ["...7d.svg", "...30d.svg"],
  "cleanup_removed": 6,
  "stance": "中性",
  "score": 1.0
}
```

快速复用已有快照，避免重新联网抓数：

```bash
/usr/bin/python3 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py" "今天美元流动性监测" --input-json "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/output/latest/snapshot.json" --json
```

跳过 SVG 图表生成：

```bash
/usr/bin/python3 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py" "今天美元流动性监测" --no-charts --json
```

单独运行 JPY carry trade 数据：

```bash
/usr/bin/python3 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/jpy_carry.py" "更新日元carry" --json
```

---

## 6. 前端预览

启动本地 HTTP 服务：

```bash
cd "/Users/eiheisun/WorkBuddy/2026-05-04-task-1" && /usr/bin/python3 -m http.server 8787
```

打开：

```text
http://localhost:8787/frontend/usd-liquidity-monitor/index.html
```

前端读取：

```js
const DATA_URLS = {
  dashboard: "../../output/latest/dashboard_data.json",
  analysis: "../../output/latest/analysis.json"
};
```

注意：

- 前端必须通过 HTTP 服务打开，不能直接双击 `index.html`，否则浏览器可能因为本地文件策略拦截 JSON fetch。
- 图表由 Chart.js 渲染，鼠标悬停会显示该日期各系列的数值。
- Chart.js canvas 必须放在固定高度 `.chart-canvas-wrap` 容器里，避免 responsive resize 无限放大。

---

## 7. 数据源总览

当前要求：能用 API 的全部用 API。

| 模块 | 指标 | 来源 | 当前抓取方式 | 说明 |
|---|---|---|---|---|
| 短端资金利率 | EFFR | NY Fed Markets API | API | 无抵押银行间隔夜资金价格 |
| 短端资金利率 | SOFR | NY Fed Markets API | API | 有抵押回购融资价格 |
| 回购量级 | SOFR_VOLUME | NY Fed Markets API | API | SOFR合格交易量，单位 USD bn，用于价格×规模判断 |
| 短端资金利率 | OBFR | NY Fed Markets API | API | 更广义银行隔夜融资价格 |
| 回购 | TGCR | NY Fed Markets API | API | 三方一般抵押品利率 |
| 回购 | BGCR | NY Fed Markets API | API | 广义一般抵押品利率 |
| 政策锚 | IORB | FRED API | API | 准备金余额利率，核心政策锚 |
| 政策锚 | DFEDTARU | FRED API | API | 联邦基金目标上限，辅助政策锚 |
| Fed负债端 | TGA | Treasury FiscalData | API | 财政部一般账户 |
| Fed负债端 | RRP | NY Fed Markets API | API | 隔夜逆回购余额 |
| Fed资产端 | SOMA | NY Fed Markets API | API | 系统公开市场账户持仓 |
| 准备金 | WRESBAL | FRED API | API | 银行准备金余额，FRED 是百万美元口径，脚本转为 USD bn |
| 国债供给吸收 | UST Auction BTC | TreasuryDirect | API | 综合国债拍卖 bid-to-cover，事件驱动 |
| 短债供给吸收 | TBILL_AUCTION_SIZE | TreasuryDirect | API | 最新T-bill拍卖日多只Bill发行规模加总，单位 USD bn |
| 短债供给吸收 | TBILL_AUCTION_BTC | TreasuryDirect | API | T-bill bid-to-cover 按发行规模加权平均，必须和规模一起看 |
| 抵押品链条 | Repo Fails UST | OFR STFM | API | mnemonic: `NYPD-PD_AFtD_T-A`，周频 |
| 离岸美元 | DTWEXBGS | FRED API | API | 广义美元指数，作为离岸美元压力代理 |
| 信用传导 | DCPN3M | FRED API | API | 90天AA非金融商业票据利率 |
| 信用传导 | BAMLH0A0HYM2 | FRED API | API | 高收益债 OAS |

不可免费官方实时获取或暂用代理：

| 原始需求 | 状态 | 当前代理 |
|---|---|---|
| MOVE Index | ICE/BofA proprietary，无免费官方实时 API | 用 Treasury/repo rates、HY spread、auction signals 替代 |
| FRA-OIS | 通常 Bloomberg/Refinitiv，无免费官方日频 API | 用 CP-Fed target proxy、SOFR/EFFR/IORB spreads 替代 |
| Cross-currency basis | 通常 vendor 数据 | 用 DTWEXBGS 作为离岸美元压力代理 |
| Real-time Treasury order book depth | BrokerTec/ICAP proprietary | 用 auction bid-to-cover、repo fails 替代 |

---

## 8. 数据频率与比较口径

不要把不同频率的数据直接混做“环比”。脚本内的 `DATA_FREQUENCY_RULES` 是统一口径源。

| 类型 | 指标例子 | 口径 |
|---|---|---|
| 日频 | EFFR、SOFR、SOFR_VOLUME、TGCR、BGCR、OBFR、TGA、RRP、DTWEXBGS、DCPN3M、HY OAS | 与上一条有效观测比较，不按自然日补零 |
| 周频 | SOMA、WRESBAL、Repo Fails | 只与上一周比较，作为结构背景 |
| 事件驱动 | Treasury auction bid-to-cover、TBILL_AUCTION_SIZE、TBILL_AUCTION_BTC | 只与上一场/上一拍卖日比较；T-bill必须同时看规模和认购倍数 |
| 政策阶梯型 | IORB、DFEDTARU、POLICY_UPPER_NYFED | 只在政策调整时变化，不做普通日度环比 |

前端每个指标卡都展示：

- `frequency`
- `data_lag`
- `comparison_basis`
- `freshness/status`

---

## 9. 核心分析框架

### 9.1 总判断等级

`stance_from_score()` 输出五档：

```text
宽松 / 中性偏松 / 中性 / 中性偏紧 / 紧张
```

当前 fallback 规则分数只用于排序风险和兜底，不应替代模型的语义判断。

### 9.2 关键传导链

前端和模型都必须展示完整链条：

```text
Fed负债端水位
→ 政策锚/准备金边际
→ 银行间无抵押融资
→ 回购融资/抵押品链条（含SOFR交易量与T-bill供给吸收）
→ 债券定价锚/收益率曲线
→ 离岸美元
→ 信用市场/金融条件
→ 证券市场风险偏好
```

当前 `analysis.json` schema 不要求单独 `transmission` 字段；传导链判断应写入 `key_takeaways`、`risk_flags` 和 `narrative_blocks.market_transmission`。如果后续前端支持 dedicated transmission object，再扩展 schema。

`risk_flags.type` / 传导风险类型取值：

- `market`：真实市场压力或偏紧信号。
- `data`：数据缺口、接口失败、降级数据源。
- `none`：没有问题。

必须区分 `market` 和 `data`。不能把数据缺口当成市场偏紧。

### 9.3 衍生信号

脚本会生成 `derived_signals`，用于排序关键变化和风险：

| 信号 | 含义 |
|---|---|
| `SOFR_ANCHOR` | SOFR 相对 IORB / 政策锚的位置 |
| `SOFR_VOLUME_IMPACT` | SOFR相对政策锚偏离 × SOFR交易量，粗略日化资金成本量级 |
| `BGCR_TGCR` | 广义 GC 与三方 GC 的结构差异 |
| `CP_PROXY` | 商业票据利率 - 政策上限代理利差，不是 FRA-OIS |
| `TGA_FLOW` | TGA 日变化对准备金的影响 |
| `RRP_LEVEL` | RRP 缓冲垫是否过低 |
| `TBILL_AUCTION_ABSORPTION` | T-bill拍卖规模 + 认购倍数的供给吸收压力 |
| `UST_1Y_YIELD` | 1Y美债收益率对应近端政策路径 |
| `NOMINAL_10Y` | 10Y名义收益率对应长期折现率锚 |
| `REAL_10Y` | 10Y实际收益率对应真实贴现率压力 |
| `IG_CHANGE` | 投资级公司债 OAS 变化 |
| `HY_CHANGE` | 高收益债 OAS 变化 |
| `VIX_RISK` | 证券市场风险偏好 |
| `USD_CHANGE` | 广义美元指数变化 |
| `AUCTION_BTC` | 综合国债拍卖 bid-to-cover |

命名要求：

```text
英文（中文翻译）
```

示例：

```text
EFFR-IORB（有效联邦基金利率-准备金余额利率）
SOFR-EFFR（担保隔夜融资利率-有效联邦基金利率）
CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）
```

---

## 10. 三段式模型流水线

当前设计不是让模型直接改前端或直接抓数据，而是：

```text
介绍文档 + 分析 prompt
        ↓
Python 脚本抓取官方 API 数据
        ↓
保存结构化 snapshot JSON
        ↓
组装 model_input JSON
        ↓
模型只输出结构化 analysis.json
        ↓
前端稳定模板读取 dashboard_data.json + analysis.json 渲染
```

### 10.1 介绍文档

文件：

```text
prompts/usd_liquidity_intro.md
```

作用：

- 给模型建立美元流动性分层框架。
- 解释 TGA、RRP、SOMA、EFFR、OBFR、SOFR、TGCR、BGCR、IORB 等指标。
- 强调先看数据新鲜度，再看边际方向，最后看传导范围。

### 10.2 分析 prompt

文件：

```text
prompts/usd_liquidity_prompt.md
```

作用：

- 规定输出原则。
- 规定完整传导链。
- 规定利率表格式。
- 规定风险信号和后续观察。

### 10.3 模型输入包

文件：

```text
output/latest/model_input.json
```

必须包含顶层字段：

```json
{
  "task": "...",
  "trigger": "...",
  "generated_at_bjt": "...",
  "intro_document": "...",
  "analysis_prompt": "...",
  "data": { "...": "..." },
  "output_contract": { "...": "..." }
}
```

### 10.4 模型输出合同

日常模型只应替换：

```text
output/latest/analysis.json
```

必须包含：

```json
{
  "meta": {},
  "stance": {},
  "key_takeaways": [],
  "risk_flags": [],
  "narrative_blocks": {}
}
```

当前前端不要求 `transmission` 或 `watchlist` 顶层字段；若需要传导链说明，写入 `narrative_blocks.market_transmission` 和相关 `risk_flags`。SOFR/T-bill 相关判断必须在 evidence 或 text 中引用量级字段：`SOFR_VOLUME` / `SOFR_VOLUME_IMPACT` / `TBILL_AUCTION_SIZE` / `TBILL_AUCTION_BTC` / `TBILL_AUCTION_ABSORPTION`。

前端不依赖模型生成 HTML。

---

## 11. 输出文件说明

### 11.1 `snapshot.json`

结构化原始快照，面向机器和审计。

内容包括：

- trigger
- generated_at_bjt
- stance / score
- metrics
- derived_signals
- unavailable_sources
- data_frequency_rules
- core_indicator_impacts
- chart_paths

### 11.2 `dashboard_data.json`

前端展示骨架，确定性生成。

内容包括：

- `meta`
- `status_scale`
- `indicator_groups`
- `derived_signals`
- `core_indicator_impacts`
- `charts`
- `chart_paths`
- `data_quality`

前端指标卡主要读 `indicator_groups`。

### 11.3 `analysis.json`

模型或 fallback 规则输出的人读分析。

前端总览、关键变化、风险信号和叙事说明从这里读。当前 schema 不要求 `transmission` 或 `watchlist` 顶层字段。

### 11.4 `charts.json`

图表数据源。

图表类型目前是 line，前端用 Chart.js 渲染。

### 11.5 Markdown 简报

`output/usd_liquidity_brief_YYYYMMDD_HHMMSS.md`

给人读，不包含模型完整 context 或 prompt。

必须包含：

- 今日结论
- 利率表
- 对流动性影响较大的指标
- 最近一周 / 一月图表说明
- 数据频率与环比口径
- 关键利差、核心数据与数据质量

---

## 12. 前端设计说明

前端目录：

```text
frontend/usd-liquidity-monitor/
```

### 12.1 `index.html`

职责：

- 页面结构。
- 引入 `styles.css`。
- 引入 Chart.js CDN。
- 引入 `app.js`。

外部 CDN：

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
```

### 12.2 `styles.css`

设计风格：

- 米白 / Claude 风格。
- 大圆角卡片。
- 轻阴影。
- oklch 色彩变量。
- 中性、偏紧、偏松、数据缺口分别有不同视觉状态。

重要样式：

- `.hero-grid`：顶部三卡片。
- `.trading-radar` / radar card styles：交易雷达与关键风险卡片。
- `.indicator-grid`：指标组。
- `.chart-canvas-wrap`：固定图表高度，防止 Chart.js 无限放大。

### 12.3 `app.js`

职责：

- fetch latest JSON。
- 渲染 meta、stance、key takeaways、risk flags。
- 渲染 trading dashboard / chart groups。
- 渲染 indicator groups。
- 用 Chart.js 渲染图表。
- 渲染 data quality。

关键函数：

| 函数 | 作用 |
|---|---|
| `loadJson()` | fetch JSON |
| `renderMeta()` | 渲染更新时间和数据日期 |
| `renderStance()` | 渲染总判断 |
| `renderStack()` | 渲染关键变化 / 风险信号 |
| `renderTradingRadar()` | 渲染核心/确认/背景交易雷达 |
| `renderIndicators()` | 渲染指标组 |
| `renderCharts()` | 渲染图表容器 |
| `drawChartJS()` | Chart.js line chart |
| `renderDataQuality()` | 渲染缺失、滞后和降级数据源 |

---

## 13. 当前最新运行状态

最近 latest 数据来自：

```text
output/latest/dashboard_data.json
output/latest/analysis.json
output/latest/model_input.json
```

最新验证重点不是固定数值，而是合同是否完整：

| 检查项 | 要求 |
|---|---|
| 主入口 | `/usr/bin/python3 scripts/run.py "触发语" --json` |
| 前端稳定输入 | `output/latest/dashboard_data.json` + `output/latest/analysis.json` |
| 模型分析输入 | `output/latest/model_input.json`，含 `analysis_prompt`、`intro_document`、结构化 `metrics` / `derived_signals` |
| 量级指标 | `SOFR_VOLUME`、`TBILL_AUCTION_SIZE`、`TBILL_AUCTION_BTC` |
| 量级衍生信号 | `SOFR_VOLUME_IMPACT`、`TBILL_AUCTION_ABSORPTION` |
| 前端图表 | `sofr_volume_30d`、`tbill_auction_size_45d`、`tbill_auction_btc_45d` 应在 `charts.json` / dashboard charts 中出现 |

当前分析原则：

- SOFR 不只看利率或 SOFR-IORB，还必须看 SOFR 交易量以及 `SOFR_VOLUME_IMPACT`。
- T-bill 不只看 bid-to-cover，还必须看拍卖规模和规模加权认购倍数。
- 若缺少这些量级数据，模型应把它写成 `data` 类型风险，而不是市场中性。
- 当前 `analysis.json` 顶层合同保持：`meta`、`stance`、`key_takeaways`、`risk_flags`、`narrative_blocks`。

---

## 14. 常见坑和修复记录

### 14.1 FRED CSV 超时

问题：

`fred.stlouisfed.org/graph/fredgraph.csv` 在当前环境可能读超时。

处理：

- 配置 FRED API Key。
- 脚本优先走 `https://api.stlouisfed.org/fred/series/observations`。
- 无 key 时才降级 CSV。

### 14.2 FRED API 并发偶发 500

问题：

多个 FRED series 并发请求时，偶发 HTTP 500。

处理：

- FRED-backed metrics 改为串行抓取。
- `http_get_json(..., retries=2)`。
- 每个 FRED 请求之间短暂 sleep。

### 14.3 WRESBAL 单位错位

问题：

FRED `WRESBAL` 是百万美元，前端展示单位是 USD bn。如果不换算，会显示大 1000 倍。

处理：

- `normalize_fred_value()` 对 `unit == "USD bn"` 且值过大的 FRED 数据做 /1000。

### 14.4 OFR repo fails mnemonic 错误

问题：

旧 mnemonic `NYPD-PD_AFtD_UST-A` 返回 400。

处理：

- 正确 mnemonic 是 `NYPD-PD_AFtD_T-A`。
- OFR API 返回数组行 `[date, value]`，不是 dict。
- `fetch_ofr_series()` 已兼容 list row，并转换到 USD bn。

### 14.5 Chart.js 无限放大

问题：

canvas 直接挂在 card 内并写 inline width/height，Chart.js responsive resize 与父容器高度计算互相触发，滚动到图表区会无限放大。

处理：

- 增加固定高度容器 `.chart-canvas-wrap`。
- canvas 设置 `width: 100% !important; height: 100% !important;`。
- JS 不再直接写 `canvas.style.width/height`。

### 14.6 IORB 缺失时的 fallback

问题：

如果 FRED 不可用，IORB 会缺失。

处理：

- 用 NY Fed EFFR 记录里的 `targetRateTo` 作为临时政策上限锚。
- 必须标明是 `POLICY_UPPER_NYFED`，不是 IORB。
- 现在 FRED API 已配置，正常情况下图表和利差优先用 IORB。

---

## 15. Codex 接手建议

如果用 Codex 打开项目，可以直接给它以下任务提示。

### 15.1 快速理解项目

```text
请阅读 PROJECT_HANDOFF_FOR_CODEX.md、scripts/run.py、scripts/fetchers.py、scripts/signals.py、scripts/dashboard.py、scripts/analysis.py、prompts/usd_liquidity_intro.md、prompts/usd_liquidity_prompt.md、frontend/usd-liquidity-monitor/app.js 和 styles.css。先总结当前美元流动性监测系统的数据流、输出合同和前端渲染逻辑，不要改代码。
```

### 15.2 验证项目能跑

```text
请不要泄露 .workbuddy/secrets/fred_api_key。运行 Python 语法检查，然后执行：/usr/bin/python3 scripts/run.py "今天美元流动性监测" --json。随后检查 output/latest/dashboard_data.json、analysis.json 和 model_input.json，确认核心指标 source 来自 FRED API、NY Fed Markets API、Treasury FiscalData/TreasuryDirect 或 OFR STFM，且 SOFR_VOLUME、TBILL_AUCTION_SIZE、TBILL_AUCTION_BTC、SOFR_VOLUME_IMPACT、TBILL_AUCTION_ABSORPTION 在可用时存在。
```

### 15.3 本地预览前端

```text
请在项目根目录启动 /usr/bin/python3 -m http.server 8787，然后打开 http://localhost:8787/frontend/usd-liquidity-monitor/index.html。检查图表 hover tooltip、传导链卡片、指标卡和数据质量区域是否正常。
```

### 15.4 继续开发新功能

```text
请保持稳定前端模板原则：日常运行只更新 output/latest/*.json，不要让模型改 HTML/CSS/JS。若需要新增指标，请先在脚本里增加 API 抓取和 DATA_FREQUENCY_RULES，再更新 dashboard_data.json 数据合同，最后前端确定性渲染。新增指标必须包含英文（中文翻译）标签、frequency、data_lag、comparison_basis、source_url、status；若是利率或拍卖类指标，还要考虑是否需要对应的市场规模/交易量字段和衍生量级信号。
```

---

## 16. 新增指标开发流程

新增一个指标时，按这个顺序：

1. 确认是否有官方或权威 API。
2. 写 fetch 函数，返回 `Metric`。
3. 加入 `fetch_all_metrics()`。
4. 加入 `RATE_LABELS`。
5. 加入 `RATE_MEANINGS`。
6. 加入 `DATA_FREQUENCY_RULES`。
7. 如需参与判断，更新 `derive_signals()`。
8. 如需进入传导链，更新 `build_transmission_chain()`。
9. 如需前端展示，更新 `group_indicators()`。
10. 如需图表，更新 `fetch_chart_series()` 和 `build_charts_payload()`。
11. 运行语法检查、脚本、前端预览。
12. 检查 `output/latest/dashboard_data.json` 和 `analysis.json`。

验收标准：

- 新指标有中文名称。
- 新指标有含义。
- 新指标有频率、滞后、比较口径。
- 新指标有 source 和 source_url。
- 缺失时 status 不得伪装成 ok。
- 不把周频/事件型数据当成日频信号。

---

## 17. 模型分析替换流程

当前 `analysis.json` 由 fallback 规则生成。未来要接入真实模型时，不要改前端，流程应该是：

1. 运行脚本生成 `output/latest/model_input.json`。
2. 把 `model_input.json` 中的 intro、prompt、data、output_contract 发给模型。
3. 模型只输出符合合同的 `analysis.json`。
4. 写回 `output/latest/analysis.json`。
5. 前端刷新即可。

模型输出必须保持这些字段：

```json
{
  "meta": {
    "generated_at_bjt": "...",
    "data_as_of": "...",
    "model": "...",
    "input_freshness_note": "..."
  },
  "stance": {
    "label": "宽松|中性偏松|中性|中性偏紧|紧张",
    "score_text": "...",
    "one_liner": "...",
    "confidence": "高|中等|低"
  },
  "key_takeaways": [],
  "risk_flags": [],
  "narrative_blocks": {}
}
```

若分析涉及SOFR/回购融资，必须在 `key_takeaways` 或 `risk_flags.evidence` 中引用 `SOFR_VOLUME` 或 `SOFR_VOLUME_IMPACT`；若涉及T-bill/拍卖吸收，必须同时引用 `TBILL_AUCTION_SIZE` 和 `TBILL_AUCTION_BTC`，或直接引用 `TBILL_AUCTION_ABSORPTION`。

---

## 18. 验证清单

每次改完必须至少跑：

```bash
/usr/bin/python3 -m py_compile "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/fetchers.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/signals.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/dashboard.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/analysis.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/charts.py" "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/jpy_carry.py"
/usr/bin/python3 "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/scripts/run.py" "今天美元流动性监测" --json
/Users/eiheisun/.workbuddy/binaries/node/versions/22.12.0/bin/node --check "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/frontend/usd-liquidity-monitor/app.js"
```

再检查：

```text
output/latest/dashboard_data.json
output/latest/analysis.json
output/latest/charts.json
```

人工检查点：

- 所有可 API 抓取的数据都不是 CSV / 网页 scrape。
- FRED API Key 没出现在任何输出文件里。
- `IORB` 是 FRED API，且图表锚利差优先用 IORB。
- `WRESBAL` 单位是 USD bn，不是百万美元。
- `REPO_FAILS_UST` 使用 OFR mnemonic `NYPD-PD_AFtD_T-A`。
- `SOFR_VOLUME`、`TBILL_AUCTION_SIZE`、`TBILL_AUCTION_BTC`、`SOFR_VOLUME_IMPACT`、`TBILL_AUCTION_ABSORPTION` 在源可用时存在。
- 前端图表 hover tooltip 正常。
- 图表不会滚动后无限放大。
- 人读 Markdown 简报没有附带 raw model context 或完整 prompt。

---

## 19. 当前可继续优化的方向

1. 接入真实模型输出 `analysis.json`
   - 目前 fallback 已可用，但最终应让模型基于 `model_input.json` 做语义判断。

2. 增强图表
   - 可以增加 WRESBAL/SOMA 周频背景图。
   - 可以增加 repo fails 与 auction BTC 单独图。
   - 可以增加图表切换周期按钮。

3. 增强数据质量面板
   - 展示每个接口最近一次成功抓取时间。
   - 展示 API latency。
   - 展示是否走 fallback。

4. 增强传导链展示
   - 当前传导判断写入 `narrative_blocks.market_transmission` 和风险卡片。
   - 若未来前端需要专门传导链组件，再扩展稳定 JSON schema；规则输出保留为 sanity check。

5. 增加自动化任务
   - 每天固定时间运行脚本。
   - 生成 latest JSON 后推送摘要。

---

## 20. 最重要的工程边界

请严格遵守：

1. 不要把 API Key 写进任何可见文件。
2. 不要让模型改前端来完成日常分析。
3. 不要用规则脚本替代模型语义判断；规则只做 fallback 和 sanity check。
4. 不要把 FRED CSV 当首选；有 key 时必须走 FRED API。
5. 不要把周频数据当昨日边际变化。
6. 不要把数据缺失当中性。
7. 不要把 CP proxy 说成 FRA-OIS。
8. 不要把 `POLICY_UPPER_NYFED` 说成 IORB。
9. 不要在人读 Markdown 简报里附带完整 model context 或 prompt。
10. 前端只读 `output/latest/*.json`，不直接调用金融 API。
