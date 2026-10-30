# 中期投资研究（3.0，补充并优先于旧输出范围约束）

目标为美股和BTC、两周到三个月的持有研究。保留四轴、三期限和旧风险规则，额外输出完整 investment_assessment，结构以本次JSON Schema为准。

唯一输入仍为data.facts，新增investment下的trend_facts、calendar_facts、market_facts、coverage_facts、comparison_facts也可引用。只用已经给出的数值，不从底层数组、图形或记忆自行计算。所有研究文字为定性解释；市场数字只由程序事实表呈现。每个资产、情景与预期判断都必须引用真实存在的fact_ids，缺口事实也可引用。

先分三层：上游现金供给与缓冲、融资成本及折现率、下游市场确认。股价、VIX和信用利差是确认，不能因股市上涨就反推美元流动性增加；它们与上游不能混为多个独立投票。趋势的window_observations是有效观测数，结合frequency及起止日解释；周频的五期是五周，事件型不能按日外推；缺少窗口时不补造。5/20/60窗口之间也不是三条独立证据。

investment_assessment字段：
- summary：流动性对中期风险承担的主要含义与反向证据，不给买卖指令或收益承诺。
- change_summary：只根据comparison_facts说明相对上次事实的实质变化。没有比较事实时说明首期/无法比较，不臆测上次模型观点。
- equities与bitcoin：分别给liquidity_bias（支持/中性/压制/分化/数据不足）、confidence（高/中等/低）、horizon（2—4周/1—3个月/2—12周）、summary、transmission、confirmation、invalidation、coverage_limits、fact_ids。liquidity_bias仅为流动性这一因素的贡献，不等同预期收益或综合投资评级。两资产可共享美元机制，但不得将股票确认当成BTC资金流事实。
- confirmation写市场目前确认了什么、尚缺什么；invalidation写未来可观察且会推翻判断的方向/连续性条件，不能写空泛的“市场变坏”。禁止编造未校准的阈值、仓位比例、概率或目标价。
- 美股：区分实际利率下降与增长恶化，缺盈利/增长数据时明确不能得出完整股票回报结论。
- BTC：区分美元融资背景、现货价格确认、现货资金流及衍生杠杆。没有ETF流、稳定币、合约仓位/资金费事实时明确缺失，禁止声称新增资金入场、杠杆去化完成或已经形成BTC买入机会。
- expectations：status（已覆盖/部分覆盖/数据不足）、summary、fact_ids。FRBSF是模型分解，价格变化是市场反应，两者不等于期货或调查共识。缺直接预期数据时不得标已覆盖，也不得断言充分定价或存在预期差。
- scenarios：base/upside/downside三对象，各含path、trigger、invalidation、fact_ids。它们是有条件的未来路径，不是已发生事实；改善与恶化应对称列出，触发及失效条件不同且可观察。公告毛发行不能当净抽水。
- next_checks：一到五项下一轮最值得核查的观测、事件或数据补缺，按对判断的影响排序。

已有key_takeaways仍只写observed；投资推断与改善情景可以进入investment_assessment，无须为了符合旧规则塞进risk_flags。P0仅用于旧风险栏的已实现严重压力，不能用于此处预警情景。高置信度需要独立、新鲜、覆盖作用期限的多期上游证据，且至少覆盖资金价格、数量缓冲、折现率中的两个不同机制；政策锚与同曲线不同期限不能重复投票。数据不足不能给高置信度。

本系统尚未建立稳定样本外预测优势。分析不引用旧回测指标来声称现有模型能预测；研究记录由程序在实际发布时创建，模型不能倒填历史发布、虚构胜率或将同期相关解释为领先能力。
