# 美元流动性分析
2026-11-17 21:16:42 UTC+08:00

中性偏紧
2026-11-17 新抓取快照：核心回购与美债定价可见至 2026-11-16，无抵押融资和信用可见至 2026-11-13，离岸直接数据欠缺；低缓冲和偏高的实际贴现率令环境偏紧，尚无广泛融资失灵的确认。

## 美股与BTC中期投资研究
中期流动性对美股与BTC风险承担偏压制。上游RRP缓冲薄，但准备金短期回升、财政现金最近回落；融资端回购边际略贵，实际贴现率在多期窗口上升；下游价格走弱，但信用及波动没有持续同向确认。上游和折现率提供机制判断，下游价格只作确认。

相对上次：较 2026-11-11 的上次成功事实包，担保融资报价上移且SOFR成交量增加，无抵押融资持平，常备回购用量较上次包减少。准备金、SOMA与TGA均高于上次包，RRP余额略回升；腹部名义与实际收益率更高，广义美元更强，而投资级、高收益利差及VIX低于上次包。对比只反映各序列新增观测，不等同于上一交易日变化；上次政策锚比较日期异常，未用于归纳。

### 美股：压制（2—4周，中等置信度）
判断：实际利率多期上移使美股估值承压，久期较长的股票更敏感；较松的周频金融条件水平和近月高收益利差收窄提供反向证据。
传导：低现金缓冲会提高股票对资金价格扰动的敏感度，较高实际贴现率压低远期盈利的现值。实际利率若因通胀降温而下行且增长企稳，估值压力可缓和；若源于增长恶化，盈利下修可能抵消贴现率改善。
市场确认：标普和纳斯达克综合指数在各自近月窗口下跌，纳斯达克综合指数相对更弱，符合估值受压的表现，但不确立因果。信用和VIX尚未确认持续收紧。
失效条件：若腹部实际利率在后续有效观测中持续回落，信用利差没有同步走阔，且股票回撤趋稳，则当前的流动性压制判断应下修。
覆盖边界：缺增长与盈利修正，无法区分贴现率冲击与盈利预期变化，也不能得出完整股票回报结论。
事实引用：derived:RRP_BUFFER, trend:DFII5:20obs, trend:DFII7:20obs, market:SP500:20obs, market:NASDAQCOM:20obs, trend:BAMLH0A0HYM2:20obs, trend:VIXCLS:20obs, metric:NFCI, coverage:growth_earnings

### BTC：压制（2—12周，低置信度）
判断：偏强美元与偏高实际利率构成美元流动性逆风，Coinbase现货价格在多期窗口下跌；无法识别加密市场内部的卖压来源。
传导：较高的美元安全资产收益提高持有BTC的机会成本，担保融资边际涨价若延续，也可能压低融资型风险承担。本土融资变化不足以直接推断加密市场的杠杆状态。
市场确认：BTC自身现货价格走弱，确认的是价格变化；现货净流量和衍生品杠杆变化没有得到确认。
失效条件：若广义美元持续转弱、实际利率回落且担保融资溢价收窄，BTC现货趋稳，则美元流动性压制判断应下修；是否形成持久支持仍需资金流和杠杆数据验证。
覆盖边界：BTC观测涵盖周末，不能按美股交易日对齐。缺ETF流、稳定币、合约仓位与资金费，不能判断新增资金入场或杠杆出清。
事实引用：trend:DTWEXBGS:20obs, trend:DFII5:20obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：1Y和3Y名义收益率反映近端与中段价格变化；FRBSF提供较早的模型平均预期短率与期限溢价分解。二者均不能替代SOFR期货或调查共识，无法判断事件是否充分计价或存在预期差。

### 基准情景
资金市场继续运转，但实际贴现率偏高、缓冲偏薄，美股和BTC的风险承担仍受约束。
触发：后续担保融资维持小幅溢价且常备回购用量有限，无抵押融资继续平稳，实际利率没有持续回落。
失效：若实际利率与融资溢价同步持续回落，或融资溢价持续走阔并出现无抵押端上行，则离开基准路径。
事实引用：derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:SRP_ACCEPTED, metric:EFFR, derived:RRP_BUFFER, trend:DFII5:20obs

### 改善情景
现金压力与贴现率同步缓解，风险资产获得较一致的流动性支持；BTC仍需独立的资金流验证。
触发：准备金在后续周度观测中企稳或回升，担保融资溢价持续收窄，腹部实际利率回落，信用利差未伴随走阔。
失效：若实际利率下降同时信用利差持续走阔，或资金溢价重新走阔并伴随准备金下滑，则改善路径失效。
事实引用：metric:WRESBAL, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII7:20obs, trend:BAMLH0A0HYM2:20obs, coverage:btc_flows_leverage

### 恶化情景
若现金净流向财政账户并压低准备金，薄缓冲会放大融资端冲击，估值和高波动资产可能承受进一步压力。
触发：实际结算与到期净额确认净筹资，TGA回补、准备金持续下降，同时放量回购溢价扩大，并获无抵押利率上行或信用走阔确认。
失效：若结算净额未形成现金抽离，或TGA回补后准备金保持稳定且回购溢价回落，则财政冲击路径失效。
事实引用：calendar:28d, metric:TGA, metric:WRESBAL, derived:RRP_BUFFER, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:EFFR, metric:BAMLH0A0HYM2

### 下一轮核查
- 对齐最新SOFR溢价、成交量、成交上尾、常备工具使用与EFFR及OBFR，确认压力是否持续并扩散。
- 核对快照公告所列结算与到期的净额，以及相应的TGA和随后公布的周度准备金。
- 跟踪腹部实际利率、通胀补偿、信用和盈利修正，区分贴现率改善与增长转弱；补直接政策预期。
- 补同日美日利差、跨币种基差及外汇隐含波动，核对日元变化是否与资金压力共振。
- 补BTC ETF净流量、稳定币供应和衍生品仓位及资金费，用BTC自身数据复核价格变化。

### 中期趋势（有效观测数，日频与周频分开）
- ICE BofA US Corporate OAS：5个有效日频观测间隔变化：2026-11-06 至 2026-11-13；5期；变化 -0.040000000000000036 %；状态 ok；trend:BAMLC0A0CM:5obs
- ICE BofA US Corporate OAS：20个有效日频观测间隔变化：2026-10-16 至 2026-11-13；20期；变化 0.040000000000000036 %；状态 ok；trend:BAMLC0A0CM:20obs
- ICE BofA US Corporate OAS：60个有效日频观测间隔变化：2026-08-21 至 2026-11-13；60期；变化 0.07999999999999996 %；状态 ok；trend:BAMLC0A0CM:60obs
- ICE BofA US High Yield OAS：5个有效日频观测间隔变化：2026-11-06 至 2026-11-13；5期；变化 -0.18999999999999995 %；状态 ok；trend:BAMLH0A0HYM2:5obs
- ICE BofA US High Yield OAS：20个有效日频观测间隔变化：2026-10-16 至 2026-11-13；20期；变化 -0.08000000000000007 %；状态 ok；trend:BAMLH0A0HYM2:20obs
- ICE BofA US High Yield OAS：60个有效日频观测间隔变化：2026-08-21 至 2026-11-13；60期；变化 0.5299999999999998 %；状态 ok；trend:BAMLH0A0HYM2:60obs
- Broad General Collateral Rate：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.029999999999999805 %；状态 ok；trend:BGCR:5obs
- Broad General Collateral Rate：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.04999999999999982 %；状态 ok；trend:BGCR:20obs
- Broad General Collateral Rate：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.2999999999999998 %；状态 ok；trend:BGCR:60obs
- 10-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.29000000000000004 %；状态 ok；trend:DFII10:5obs
- 10-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.17999999999999972 %；状态 ok；trend:DFII10:20obs
- 10-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.5699999999999998 %；状态 ok；trend:DFII10:60obs
- 5-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.33000000000000007 %；状态 ok；trend:DFII5:5obs
- 5-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.16000000000000014 %；状态 ok；trend:DFII5:20obs
- 5-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.6100000000000003 %；状态 ok；trend:DFII5:60obs
- 7-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.31000000000000005 %；状态 ok；trend:DFII7:5obs
- 7-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.16999999999999993 %；状态 ok；trend:DFII7:20obs
- 7-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.6000000000000001 %；状态 ok；trend:DFII7:60obs
- 1年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.29000000000000004 %；状态 ok；trend:DGS1:5obs
- 1年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.16000000000000014 %；状态 ok；trend:DGS1:20obs
- 1年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.6200000000000001 %；状态 ok；trend:DGS1:60obs
- 10年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.2599999999999998 %；状态 ok；trend:DGS10:5obs
- 10年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.03000000000000025 %；状态 ok；trend:DGS10:20obs
- 10年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.46999999999999975 %；状态 ok；trend:DGS10:60obs
- 2年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.3200000000000003 %；状态 ok；trend:DGS2:5obs
- 2年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.08999999999999986 %；状态 ok；trend:DGS2:20obs
- 2年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.6399999999999997 %；状态 ok；trend:DGS2:60obs
- 3年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.28000000000000025 %；状态 ok；trend:DGS3:5obs
- 3年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.04999999999999982 %；状态 ok；trend:DGS3:20obs
- 3年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.6200000000000001 %；状态 ok；trend:DGS3:60obs
- 5年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.29000000000000004 %；状态 ok；trend:DGS5:5obs
- 5年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.040000000000000036 %；状态 ok；trend:DGS5:20obs
- 5年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.5800000000000001 %；状态 ok；trend:DGS5:60obs
- 7年期国债收益率：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.2699999999999996 %；状态 ok；trend:DGS7:5obs
- 7年期国债收益率：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.02999999999999936 %；状态 ok；trend:DGS7:20obs
- 7年期国债收益率：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.5299999999999994 %；状态 ok；trend:DGS7:60obs
- Trade-weighted broad dollar index：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 1.1441999999999979 index；状态 ok；trend:DTWEXBGS:5obs
- Trade-weighted broad dollar index：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 1.081000000000003 index；状态 ok；trend:DTWEXBGS:20obs
- Trade-weighted broad dollar index：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 3.6672000000000082 index；状态 ok；trend:DTWEXBGS:60obs
- Effective Federal Funds Rate：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 0.0 %；状态 ok；trend:EFFR:5obs
- Effective Federal Funds Rate：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 0.0 %；状态 ok；trend:EFFR:20obs
- Effective Federal Funds Rate：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 0.25 %；状态 ok；trend:EFFR:60obs
- FRBSF average expected overnight rate over next 10 years：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 0.21100999999999992 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:5obs
- FRBSF average expected overnight rate over next 10 years：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 0.024221999999999966 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:20obs
- FRBSF average expected overnight rate over next 10 years：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 0.35330499999999976 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:60obs
- FRBSF average expected overnight rate over next 2 years：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 0.3723010000000002 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:5obs
- FRBSF average expected overnight rate over next 2 years：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 0.11858400000000024 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:20obs
- FRBSF average expected overnight rate over next 2 years：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 0.6925860000000004 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:60obs
- FRBSF 10-year Treasury term premium：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 0.04028999999999994 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:5obs
- FRBSF 10-year Treasury term premium：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 0.012777999999999956 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:20obs
- FRBSF 10-year Treasury term premium：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 -0.01020500000000002 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:60obs
- Interest on Reserve Balances：5个有效日频观测间隔变化：2026-11-12 至 2026-11-17；5期；变化 0.0 %；状态 ok；trend:IORB:5obs
- Interest on Reserve Balances：20个有效日频观测间隔变化：2026-10-28 至 2026-11-17；20期；变化 0.0 %；状态 ok；trend:IORB:20obs
- Interest on Reserve Balances：60个有效日频观测间隔变化：2026-09-18 至 2026-11-17；60期；变化 0.0 %；状态 ok；trend:IORB:60obs
- Chicago Fed National Financial Conditions Index：5个有效周频观测间隔变化：2026-10-02 至 2026-11-06；5期；变化 0.034999999999999976 index；状态 ok；trend:NFCI:5obs
- Chicago Fed National Financial Conditions Index：20个有效周频观测间隔变化：2026-06-19 至 2026-11-06；20期；变化 0.046999999999999986 index；状态 ok；trend:NFCI:20obs
- Chicago Fed National Financial Conditions Index：60个有效周频观测间隔变化：2025-09-12 至 2026-11-06；60期；变化 0.066 index；状态 ok；trend:NFCI:60obs
- Overnight Bank Funding Rate：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 0.0 %；状态 ok；trend:OBFR:5obs
- Overnight Bank Funding Rate：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 0.0 %；状态 ok；trend:OBFR:20obs
- Overnight Bank Funding Rate：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 0.25 %；状态 ok；trend:OBFR:60obs
- Overnight Reverse Repo accepted amount：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.032 USD bn；状态 ok；trend:RRPONTSYD:5obs
- Overnight Reverse Repo accepted amount：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.08199999999999999 USD bn；状态 ok；trend:RRPONTSYD:20obs
- Overnight Reverse Repo accepted amount：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 -0.135 USD bn；状态 ok；trend:RRPONTSYD:60obs
- Secured Overnight Financing Rate：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.040000000000000036 %；状态 ok；trend:SOFR:5obs
- Secured Overnight Financing Rate：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.050000000000000266 %；状态 ok；trend:SOFR:20obs
- Secured Overnight Financing Rate：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.31000000000000005 %；状态 ok；trend:SOFR:60obs
- SOFR transaction volume：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 -4.0 USD bn；状态 ok；trend:SOFR_VOLUME:5obs
- SOFR transaction volume：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 245.0 USD bn；状态 ok；trend:SOFR_VOLUME:20obs
- SOFR transaction volume：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 247.0 USD bn；状态 ok；trend:SOFR_VOLUME:60obs
- SOMA holdings / QT background：5个有效周频观测间隔变化：2026-10-07 至 2026-11-10；5期；变化 4.402128980999805 USD bn；状态 ok；trend:SOMA:5obs
- SOMA holdings / QT background：20个有效周频观测间隔变化：2026-06-24 至 2026-11-10；20期；变化 20.576559415500014 USD bn；状态 ok；trend:SOMA:20obs
- SOMA holdings / QT background：60个有效周频观测间隔变化：2025-09-17 至 2026-11-10；60期；变化 170.12253188510022 USD bn；状态 ok；trend:SOMA:60obs
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.002 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.002 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.001 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
- Treasury General Account closing balance：5个有效日频观测间隔变化：2026-11-05 至 2026-11-13；5期；变化 1.8660000000000991 USD bn；状态 ok；trend:TGA:5obs
- Treasury General Account closing balance：20个有效日频观测间隔变化：2026-10-15 至 2026-11-13；20期；变化 -10.072000000000003 USD bn；状态 ok；trend:TGA:20obs
- Treasury General Account closing balance：60个有效日频观测间隔变化：2026-08-18 至 2026-11-13；60期；变化 -37.333999999999946 USD bn；状态 ok；trend:TGA:60obs
- Tri-party General Collateral Rate：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 0.040000000000000036 %；状态 ok；trend:TGCR:5obs
- Tri-party General Collateral Rate：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 0.04999999999999982 %；状态 ok；trend:TGCR:20obs
- Tri-party General Collateral Rate：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 0.2999999999999998 %；状态 ok；trend:TGCR:60obs
- CBOE Volatility Index: VIX：5个有效日频观测间隔变化：2026-11-06 至 2026-11-13；5期；变化 -6.34 index；状态 ok；trend:VIXCLS:5obs
- CBOE Volatility Index: VIX：20个有效日频观测间隔变化：2026-10-16 至 2026-11-13；20期；变化 -0.6899999999999977 index；状态 ok；trend:VIXCLS:20obs
- CBOE Volatility Index: VIX：60个有效日频观测间隔变化：2026-08-21 至 2026-11-13；60期；变化 4.17 index；状态 ok；trend:VIXCLS:60obs
- Reserve balances with Federal Reserve Banks：5个有效周频观测间隔变化：2026-10-07 至 2026-11-11；5期；变化 -69.05600000000004 USD bn；状态 ok；trend:WRESBAL:5obs
- Reserve balances with Federal Reserve Banks：20个有效周频观测间隔变化：2026-06-24 至 2026-11-11；20期；变化 9.186999999999898 USD bn；状态 ok；trend:WRESBAL:20obs
- Reserve balances with Federal Reserve Banks：60个有效周频观测间隔变化：2025-09-17 至 2026-11-11；60期；变化 -112.75199999999995 USD bn；状态 ok；trend:WRESBAL:60obs
- 同日SOFR减IORB：5个有效日频观测间隔变化：2026-11-06 至 2026-11-16；5期；变化 4.0000000000000036 bp；状态 ok；trend:SOFR_IORB:5obs
- 同日SOFR减IORB：20个有效日频观测间隔变化：2026-10-16 至 2026-11-16；20期；变化 5.000000000000027 bp；状态 ok；trend:SOFR_IORB:20obs
- 同日SOFR减IORB：60个有效日频观测间隔变化：2026-08-19 至 2026-11-16；60期；变化 6.000000000000005 bp；状态 ok；trend:SOFR_IORB:60obs

### 已公告结算日历（毛额，不等于净融资）
- {"fact_id": "calendar:7d", "id": "ANNOUNCED_SETTLEMENTS_7D", "name": "未来7日已公告结算毛发行（含快照日）", "value": 100.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-17", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 7, "window_start": "2026-11-17", "window_end": "2026-11-23", "event_count": 1, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 100.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-17:Bill:6-Week:912797VJ3"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:28d", "id": "ANNOUNCED_SETTLEMENTS_28D", "name": "未来28日已公告结算毛发行（含快照日）", "value": 135.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-17", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 28, "window_start": "2026-11-17", "window_end": "2026-12-14", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 135.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-17:Bill:6-Week:912797VJ3", "event:auction:2026-11-18:Bond:20-Year:912810UZ9", "event:auction:2026-11-19:Note:9-Year 8-Month:91282CRE3"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:84d", "id": "ANNOUNCED_SETTLEMENTS_84D", "name": "未来84日已公告结算毛发行（含快照日）", "value": 135.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-17", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 84, "window_start": "2026-11-17", "window_end": "2027-02-08", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 135.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-17:Bill:6-Week:912797VJ3", "event:auction:2026-11-18:Bond:20-Year:912810UZ9", "event:auction:2026-11-19:Note:9-Year 8-Month:91282CRE3"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}

### 判断验证记录
这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，从其日期往后两日开始寻找首个有效收盘作为观察起点；评估只使用截至评估时刻UTC日期往前两日的价格。美股按10／20／60个后续有效收盘观察（约2／4／12周），BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。同一快照与方法版本仅首次发布算一个样本。去重后的持有窗口仍可能重叠，不能当作统计独立样本；历史价格截断或起点缺价时不把观察起点向后漂移。收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。所有已成熟样本均保留；分组不足十个样本时明确标为积累中，样本充足时仍只提供描述统计，预测能力需要另行样本外检验。早期研究归档不完整，缺失运行 20261030_135123_15fc84aa 及其更早链路。当前统计覆盖通过清单校验的记录。
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "available", "status_note": "窗口已成熟；数值为观察期价格表现，不是策略收益。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": "2026-11-15", "exit_price": 64787.64, "elapsed_calendar_days": 14, "return_pct": -17.0569, "max_drawdown_pct": -21.7973, "max_adverse_excursion_pct": -19.4855, "benchmark_return_pct": -17.0569, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 9}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "available", "status_note": "窗口已成熟；数值为观察期价格表现，不是策略收益。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": "2026-11-15", "exit_price": 64787.64, "elapsed_calendar_days": 14, "return_pct": -17.0569, "max_drawdown_pct": -21.7973, "max_adverse_excursion_pct": -19.4855, "benchmark_return_pct": -17.0569, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-11-18"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-12-02"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2027-01-27"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 7}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-11-18"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-12-02"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2027-01-27"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 6}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 6}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 6}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2026-11-19"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2026-12-03"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2027-01-28"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 7561.67, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "observations_available": 0}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 7561.67, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "observations_available": 0}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 7561.67, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "observations_available": 0}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 68178.05, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "target_exit_date": "2026-11-27"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 68178.05, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "target_exit_date": "2026-12-11"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": "2026-11-13", "entry_price": 68178.05, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13", "target_exit_date": "2027-02-05"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}
- {"run_id": "20261117_211355_45c66f73", "published_at_bjt": "2026-11-17T21:22:09.124601+08:00", "source_generated_at_bjt": "2026-11-17T21:16:42+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-15", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-19"}

## 担保融资涨价伴随放量
SOFR相对IORB的溢价较上期扩大，成交量同步增加，假设性价量影响代理上升；常备工具用量仍极小，较早的无抵押利率保持平稳。
SOFR_ANCHOR：3.00bp（2026-11-16，+3.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3170.00bn（2026-11-16，+78.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：2.64mn/day（2026-11-16，+2.64mn/day）；日频，纽约联储SOFR记录随利率一同发布。
SRP_ACCEPTED：0.00bn（2026-11-16，+0.00bn）；daily T+1。
EFFR：3.88%（2026-11-13，+0.00%）；daily T+1。
OBFR：3.88%（2026-11-13，+0.00%）；daily T+1。

## 边际现金流量改善，准备金单周回升
最新TGA下降、RRP小幅流出，方向上减轻短期现金压力；准备金最新周度上升，但仍低于较近多周窗口起点，SOMA最新周度持仓增加。这些观测日期不同。
TGA_FLOW：-8.51bn（2026-11-13，-29.50bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
RRP_FLOW：-0.14bn（2026-11-16，环比未知）；日频，纽约联储每日操作结果。
WRESBAL：2960.60bn（2026-11-11，+30.51bn）；weekly。
WRESBAL：2960.60bn（2026-11-11，-69.06bn）；weekly。
SOMA：6364.92bn（2026-11-10，+7.30bn）；weekly。

## 名义腹部回落，实际贴现率未降
近端和腹部名义收益率全线回落；腹部较短端的实际收益率持平，较长端小升，两个期限的通胀补偿均下降。名义回落未伴随真实贴现率改善。
DGS1：4.62%（2026-11-16，-0.03%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.87%（2026-11-16，-0.05%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.93%（2026-11-16，-0.05%）；daily / same-day (Treasury 4pm ET)。
DGS7：5.01%（2026-11-16，-0.04%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.68%（2026-11-16，+0.00%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.79%（2026-11-16，+0.01%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.25%（2026-11-16，-0.05%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.22%（2026-11-16，-0.05%）；日频，FRED/H.15国债恒定期限收益率。

## 已完成短债组合有规模和投标覆盖记录
2026-11-16 的短债拍卖组合有公告规模、按规模加权的投标覆盖和预计算吸收压力读数。与上一事件的组合可比性未建立，不能据此认定同期限需求改善。
TBILL_AUCTION_SIZE：177.00bn（2026-11-16，-123.00bn）；event-based。
TBILL_AUCTION_BTC：2.79ratio（2026-11-16，+0.05ratio）；event-based。
TBILL_AUCTION_STRESS：40.00index（2026-11-16，-10.00index）；事件驱动，财政部T-bill拍卖后公布。

## 风险资产走弱，信用与波动确认不齐
美股与BTC在各自多期窗口均走弱。高收益利差和VIX最新一期上行，但近月窗口均回落，投资级利差最新持平。BTC价格窗口含周末，不能与股票窗口直接作等期比较。
SP500：-3.56%（2026-11-16，-3.56%）；daily close / US trading observations。
NASDAQCOM：-7.27%（2026-11-16，-7.27%）；daily close / US trading observations。
CBBTCUSD：-20.06%（2026-11-16，-20.06%）；daily / 7-day observations。
BAMLC0A0CM：0.89%（2026-11-13，+0.00%）；daily T+1。
BAMLH0A0HYM2：3.23%（2026-11-13，+0.03%）；daily T+1。
VIXCLS：19.30index（2026-11-13，+0.60index）；daily T+1。
BAMLH0A0HYM2：3.23%（2026-11-13，-0.08%）；daily T+1。
VIXCLS：19.30index（2026-11-13，-0.69index）；daily T+1。

## 逆回购存量缓冲很薄
后续财政补库或其他负债扰动更可能由准备金吸收。准备金最新一周反弹，低RRP本身不足以确认准备金短缺。
RRP_BUFFER：0.18bn（2026-11-16，-0.14bn）；日频，纽约联储每日操作结果。
WRESBAL：2960.60bn（2026-11-11，+30.51bn）；weekly。
WRESBAL：2960.60bn（2026-11-11，-69.06bn）；weekly。

## 公告结算需要净额和传导确认
若净筹资与现金水位或融资价格共同确认，结算才可能增加资金压力。快照仅列公告毛额，到期、净现金筹集与准备金影响均未知。
event:gross_total_by_issue_date:2026-11-19：日期未知；状态 unknown；无可用数值。
event:gross_total_by_issue_date:2026-11-30：日期未知；状态 unknown；无可用数值。
TGA：924.62bn（2026-11-13，-8.51bn）；daily T+1。
WRESBAL：2960.60bn（2026-11-11，+30.51bn）；weekly。
SOFR_ANCHOR：3.00bp（2026-11-16，+3.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3170.00bn（2026-11-16，+78.00bn）；daily T+1。

## 离岸与日元融资覆盖有限
商业票据已陈旧，广义美元不能替代跨币种基差。日债最新报价为混合来源，已配对长端美日利差止于 2026-10-30；实现波动不能替代期权隐含波动。缺少可用的直接融资接口数据使当前压力方向仍待确认。
quality:stale_metric:DCPN3M：2026-11-05；状态 stale；无可用数值。
DTWEXBGS：122.65index（2026-11-13，+0.11index）；daily T+1。
JGB10：2.88原始比例/口径（2026-11-17，+0.08原始比例/口径）；按来源频率。
US_JP_10Y：212.30原始比例/口径（2026-10-30，+1.90原始比例/口径）；按来源频率。
USDJPY_VOL20：4.03原始比例/口径（2026-11-13，-0.20原始比例/口径）；按来源频率。

## 中期研究缺直接预期和资产专属数据
未配置直接政策预期、增长盈利修正、BTC现货资金流和合约杠杆；回抓历史未核验为当时可见版本。缺口限制估值归因、资金流判断以及预测能力验证。
coverage:direct_expectations：2026-11-17；状态 missing；无可用数值。
coverage:growth_earnings：2026-11-17；状态 missing；无可用数值。
coverage:btc_flows_leverage：2026-11-17；状态 missing；无可用数值。
coverage:historical_vintages：2026-11-17；状态 prospective_capture_only；无可用数值。