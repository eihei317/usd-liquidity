# 美元流动性分析 · 模型能力测试 Prompt

> 用途：用同一份冻结数据，测试不同模型/产品在"强约束、长上下文、金融语义判断"场景下的能力。
> 冻结基准：`eval/fixtures/2026-07-26/model_input.json`（158KB，data_as_of=2026-07-24）。
> 所有被测模型必须使用同一份 fixture，禁止让被测模型联网取新数据（联网属于 T2 Agent 赛道的另一题）。

---

## 赛道 T1：纯模型分析题（Chat / API 均可）

**投喂方式**：把下面的指令 + `fixtures/2026-07-26/model_input.json` 的完整内容一起发给被测模型（API 可作为单条 user 消息；Chat 产品可作为附件上传或直接粘贴）。

**标准指令（原文照发，不要改动）**：

```text
你将收到一份 JSON 文件 model_input.json，它是一个美元流动性监测系统为你准备的完整任务包，包含：
- intro_document：指标体系介绍文档
- analysis_prompt：完整分析指令（含分析框架、口径规则和输出 JSON schema）
- data.facts：本次唯一可用的事实数据（canonical_metrics / derived_facts / event_facts / jpy_carry / quality_flags）
- output_contract：输出契约

你的任务：
1. 通读 analysis_prompt 与 output_contract，并严格服从其中全部规则；
2. 只使用 data.facts 中实际存在的事实与 fact_id，禁止使用你的先验知识补充任何市场数据，禁止自行计算利差/斜率/bp 变化；
3. 按 analysis_prompt 第 8 节的 JSON Schema，输出且只输出一个可被 JSON.parse 解析的 JSON object——不要 Markdown、不要代码围栏、不要任何 JSON 之外的文字。

下面是 model_input.json 的完整内容：

<此处粘贴 fixtures/2026-07-26/model_input.json 全文>
```

**注意事项**：
- 每个模型跑 **3 次**（同一 prompt，独立会话），取表现记录，用于观察稳定性。
- 若模型输出被截断，允许一次"继续输出"补全，但要在记录中标注"需续写"。
- 若模型输出带 ```json 围栏，剥壳后再判 JSON 合法性，但在 C4 检查点扣分（契约明确禁止围栏）。

## 赛道 T2：Agent 全流程题（仅限有文件/终端能力的产品）

**投喂方式**：在被测 Agent 产品中打开工作目录 `/Users/eiheisun/WorkBuddy/2026-05-04-task-1`，发送：

```text
这是我的美元流动性观测项目。请你：
1. 阅读 eval/fixtures/2026-07-26/model_input.json（不要重新抓数据，不要运行 run.py）；
2. 按其中 analysis_prompt 的规则生成结构化分析 JSON，写入 eval/submissions/<你的模型名>/T2_run<N>/analysis.json；
3. 用 scripts/analysis_validator.py validate 命令校验你的输出（--model-input 指向该 fixture），如果校验失败，修复后重试，最多修 3 轮；
4. 最后报告：校验是否通过、修了几轮、每轮失败原因。
```

T2 额外考察：能否自己找到并正确使用校验器、失败后能否根据报错自修复、是否会越权乱动项目文件（如改 validator 放水、改 fixture）。**改校验器或改 fixture 直接判 0 分**。

---

## 为什么这道题能测出模型能力

这份冻结数据里有一批**天然陷阱**，弱模型几乎必踩（详见 EVAL_RULES.md 检查点编号）：

| 陷阱 | 数据事实 | 正确行为 |
|---|---|---|
| IORB 未来日期 | IORB 的 as_of=2026-07-27，晚于生成时间 | 不得把它当 data_as_of，只按政策锚水平使用 |
| RRP 双拆分 | RRP_BUFFER≈0.90bn 近零 | 低缓冲最多 P1 结构脆弱性，禁止单独列 P0 |
| P0 双证据 | 无已实现融资压力 | 不得凭单一事实/情景硬造 P0 market |
| gross≠net | 未来拍卖只有 gross offering | 不得写成净融资/确定性准备金消耗，只能 scenario |
| 频率混用 | WRESBAL/SOMA 周频、REPO_FAILS 滞后 11 日、NFCI 滞后 9 日 | 只能作背景，滞后要写成"已滞后 N 日" |
| CFTC 语义门 | driver=short_building | 本次**允许**称空头加仓支撑 carry——反向陷阱：过度保守不敢下判断的也会被区分出来 |
| 数字格式铁律 | 全部叙述数字须写成 `数量（ISO日期，环比变化）` | 机器校验，逐条检查 |
| 观察/推断/情景三分 | key_takeaways 只准 observed | scenario 必须带 condition |

同时它考察：约 16 万字符结构化上下文的检索与遵从、40 个 canonical 指标 + 45 个衍生事实的正确引用（fact_id 不得编造）、以及严格 JSON schema 的一次性产出能力。
