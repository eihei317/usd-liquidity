# 测试用 Prompt：项目概括能力评估（自包含 · 从零生成版）

> 用途：把下面「测试 Prompt」整段复制给**别的模型**。该模型**没有任何文件读权限**，只能基于你粘贴进 `<project_material>` 的内容，从零生成一份结构化的项目概括。
> 目标：考察它能否把散点事实**正确组装成架构叙述**、是否**守住工程红线**、是否**不臆造**。文末附「评分卡」。

---

## 测试 Prompt（复制这一段即可）

```text
你是一名资深软件架构师。下面 <project_material> 中是某个代码库的"原始素材/笔记"——它们是零散的事实，不是成品文档，也故意没有按架构顺序组织。请你**只依据这些素材**，从零组织出一份完整、准确、结构化的项目概括。读不到依据就明说"依据不足"，不要编造或脑补文件里没写的东西。

<project_material>
【系统是什么】
- 一套"美元流动性监测 (USD Liquidity Monitor)"系统：从官方/权威公开 API 抓取美元流动性相关指标，生成结构化数据快照与模型输入，再由模型产出结构化分析 JSON，最后由纯前端按固定模板确定性渲染仪表盘。
- 人读简报不附带模型完整 context 或完整 prompt；这些只存在于 model_input JSON 内部。

【数据从哪来】
- NY Fed Markets API：EFFR、SOFR、SOFR_VOLUME（合格交易量，USD bn）、OBFR、TGCR、BGCR、RRP（隔夜逆回购余额）、SOMA。
- FRED API：IORB（准备金余额利率，核心政策锚）、DFEDTARU（联邦基金目标上限）、WRESBAL（银行准备金余额，FRED 口径为百万美元，需转 USD bn）、DTWEXBGS（广义美元指数）、DCPN3M（90天AA非金融商业票据利率）、BAMLH0A0HYM2（高收益债 OAS）。
- Treasury FiscalData：TGA（财政部一般账户）。
- TreasuryDirect：UST 综合国债拍卖 bid-to-cover、TBILL_AUCTION_SIZE（最新 T-bill 拍卖日多只 Bill 发行规模加总，USD bn）、TBILL_AUCTION_BTC（T-bill 认购倍数按规模加权）。
- OFR STFM：Repo Fails UST（mnemonic NYPD-PD_AFtD_T-A，周频）。

【数据频率与口径（核心规则）】
- 日频：EFFR、SOFR、SOFR_VOLUME、TGCR、BGCR、OBFR、TGA、RRP、DTWEXBGS、DCPN3M、HY OAS——只与上一条有效观测比，不按自然日补零。
- 周频：SOMA、WRESBAL、Repo Fails——只与上一周比，作结构背景。
- 事件驱动：Treasury auction BTC、TBILL_AUCTION_SIZE、TBILL_AUCTION_BTC——只与上一场/上一拍卖日比；T-bill 必须同时看规模和认购倍数。
- 政策阶梯型：IORB、DFEDTARU、POLICY_UPPER_NYFED——只在政策调整时变，不做普通日度环比。
- 铁律：日频/周频/事件驱动/政策阶梯型数据不可混比；缺失数据必须显式标为数据风险，不能当中性。

【处理流水线（组件）】
- run.py：主入口/调度器。
- fetchers.py：数据抓取（NY Fed / FRED / Treasury / OFR / CFTC）。
- signals.py：信号计算 + 评分 + stance 判定（五档：宽松/中性偏松/中性/中性偏紧/紧张；fallback 分数只排序风险与兜底，不替代模型语义判断）。
- dashboard.py：前端 JSON 构建 + 传导链。
- analysis.py：兜底分析 + 报告 + 生成 model_input。
- db.py：SQLite 历史库。
- charts.py：图表数据。
- jpy_carry.py：日元 Carry Trade 数据。
- 前端 frontend/usd-liquidity-monitor/：index.html + styles.css + app.js + 本地 chart.min.js（Chart.js）。米白/Claude 风格，大圆角卡片、轻阴影、oklch 变量；不同状态（中性/偏紧/偏松/数据缺口）有不同视觉；图表用固定高度容器防 Chart.js 无限放大。

【输出文件（output/latest/）】
- snapshot.json：结构化原始快照（trigger、generated_at_bjt、stance/score、metrics、derived_signals、unavailable_sources、data_frequency_rules、core_indicator_impacts、chart_paths）。
- model_input.json：含 task、trigger、generated_at_bjt、intro_document、analysis_prompt、data、output_contract。
- dashboard_data.json：前端骨架（meta、status_scale、indicator_groups、derived_signals、core_indicator_impacts、charts、chart_paths、data_quality）。
- analysis.json：模型或 fallback 输出的人读分析，含 meta、stance、key_takeaways、risk_flags、narrative_blocks。
- charts.json：图表数据源（line 类型）。
- 历史归档：output/usd_liquidity_*_时间戳.* 与 jpy_carry_*_时间戳.json；SQLite 库 usd_liquidity.db。

【模型与前端边界】
- 三段式：介绍文档 + 分析 prompt → 脚本抓官方 API → 存结构化 snapshot → 组装 model_input → 模型只输出结构化 analysis.json → 前端稳定模板读 dashboard_data.json + analysis.json 渲染。
- 日常运行：模型只替换 analysis.json，绝不让模型改前端 HTML/CSS/JS。前端只读 output/latest/*.json，不直接调用任何金融 API。
- 当前 analysis.json 由 fallback 规则生成；最终目标是由真实模型基于 model_input.json 做语义判断后覆盖。

【分析框架要点】
- 利率是价格信号，必须结合市场规模/交易量做"价格×规模"判断：SOFR 看 SOFR_VOLUME / SOFR_VOLUME_IMPACT（偏离×交易量，日化资金成本量级）；T-bill 看 TBILL_AUCTION_SIZE + TBILL_AUCTION_BTC（或 TBILL_AUCTION_ABSORPTION）。缺这些量级数据要标为 data 风险，不是中性。
- 传导链：Fed负债端水位 → 政策锚/准备金边际 → 银行间无抵押融资 → 回购融资/抵押品链条（含 SOFR 交易量与 T-bill 供给吸收）→ 债券定价锚/收益率曲线 → 离岸美元 → 信用市场/金融条件 → 证券市场风险偏好。
- 必须区分 market（真实市场压力）与 data（数据缺口/接口失败/降级源）两类风险，不能把数据缺口当市场偏紧。

【工程红线（绝对禁止）】
- API Key（FRED_API_KEY）不得写入源码、Markdown、output/*.json，输出里出现请求 URL 必须脱敏 api_key。
- 不得把 fallback 规则输出说成"模型的语义判断"。
- 不得把周频/事件型数据当成"昨日边际变化"来比较。
- 不得把"数据缺失"当作"中性/无影响"。
- 不得把 CP proxy（商业票据利率-政策上限代理利差）说成 FRA-OIS；不得把 POLICY_UPPER_NYFED（NY Fed EFFR 记录里的 targetRateTo 临时锚）说成 IORB。
- 前端只读 output/latest/*.json，绝不直接调用金融 API。
- 模型日常只输出 analysis.json，不得改前端 HTML/CSS/JS。
- 人读 Markdown 简报不得附带完整 model context 或 prompt。

【当前状态与下一步】
- 当前：fallback 规则已可用，最终应接真实模型输出 analysis.json。
- 可优化：接真实模型；增强图表（WRESBAL/SOMA 周频背景图、repo fails 与 auction BTC 单图、周期切换按钮）；增强数据质量面板（接口最近成功时间、latency、是否 fallback）；增强传导链展示；增加自动化每日定时运行并推送摘要。
</project_material>

== 任务：请按以下 8 节，从零组织出项目概括 ==
1. 一句话项目定位（解决什么问题、给谁用）。
2. 系统架构与数据流：把"抓取 → snapshot → model_input → analysis.json → 前端渲染"这条流水线讲清楚，并说明每个脚本（run/fetchers/signals/dashboard/analysis/db/charts/jpy_carry）的职责与衔接。
3. 数据源与口径：列出真实使用的官方/权威 API；强调"日频/周频/事件驱动/政策阶梯型不可混比"这条核心规则。
4. 核心分析框架：5 档总判断、完整传导链、以及"价格×规模（SOFR 交易量、T-bill 规模×认购倍数）"的要求。
5. 输出合同：列出关键 JSON（snapshot / model_input / dashboard_data / analysis / charts）及其消费者；明确"模型只输出 analysis.json、日常不改前端"的边界。
6. 前端：读取哪些文件、设计风格、确定性渲染要点（Chart.js、固定高度容器等）。
7. 工程红线：列出项目禁止的行为，并自查你的概括是否守住；market 与 data 风险必须区分。
8. 当前状态与下一步：当前是 fallback 还是已接真实模型；列出可优化方向。

== 输出与约束 ==
- 用结构化 Markdown 输出上述 8 节，术语与字段名精确。
- 严格守住红线：任何一处分辨不出"fallback≠模型判断""CP proxy≠FRA-OIS""POLICY_UPPER_NYFED≠IORB""数据缺失≠中性""前端不直连 API""模型不改前端"等，都算踩线。
- 素材读不到明确依据处，写"依据不足"，不要猜测。
- 重在准确、结构、守约，而非堆字数。
```

---

## 评分卡（给"别的模型"打分用）

| # | 维度 | 满分 | 判分要点 |
|---|---|---|---|
| 1 | 架构/数据流准确性 | 20 | 是否还原"脚本抓数→snapshot→model_input→analysis.json→前端"链路，9 个脚本职责是否分清、衔接是否对 |
| 2 | 数据源与口径 | 15 | 是否点出 NY Fed/FRED/Treasury/OFR 且强调"频率不可混比" |
| 3 | 分析框架 | 15 | 5档总判断、传导链、价格×规模是否都覆盖且正确 |
| 4 | 输出合同边界 | 15 | 是否明确"模型只输出 analysis.json、不改前端"，各 JSON 消费者是否清楚 |
| 5 | 红线零违例 | 20 | 任一红线被踩即≤10；全守住满分（重点看 fallback≠模型、CP proxy≠FRA-OIS、前端不直连、数据缺失≠中性） |
| 6 | 结构/可读/不臆造 | 15 | 8节齐全、术语精确、读不到处明说而非编造 |

> 判定：总分 ≥85 且第 5 项满分 → "能做到"；第 5 项失分或总分 <70 → "做不到/没真懂"。
