# 美元流动性分析
2026-10-30 14:13:31 UTC+08:00

中性偏紧
2026-10-30最新可得快照显示美元流动性中性偏紧：主要市场观测截至2026-10-28至2026-10-29，缓冲偏薄但即时压力缓和，尚无新鲜独立证据确认严重融资紧张，离岸与杠杆覆盖仍不完整。

## 美股与BTC中期投资研究
中期流动性贡献呈分化：上游现金缓冲偏薄、财政现金在近期窗口积累，融资端尚无全面失灵；折现率较月度起点下降提供支持，但下游价格与信用确认不一致。美股和BTC均不宜据此形成单向收益判断，较长期窗口的融资及真实贴现率约束仍在。当前研究未建立稳定样本外预测优势，捕获历史亦不等于当时可见版本。

相对上次：相对上次成功事实包，可比的资金利率、现金余额、准备金、SOMA、国债曲线、实际收益率、信用、VIX及模型分解均未改变观测值或日期，未见已覆盖核心事实的实质更新；不能由此臆测上次模型观点。资产价格和日历未提供对应比较事实，不判断其相对上次变化。

### 美股：分化（2—12周，中等置信度）
判断：较月度起点下降的真实贴现率有利于估值，但上游现金缓冲与担保融资约束抵消部分支持；标普与纳斯达克综合的价格确认分化，未形成普遍流动性利好。
传导：真实无风险收益率回落可降低长久期现金流折现压力，而现金缓冲薄及回购相对政策锚偏贵会限制风险中介扩张。若利率下降来自增长恶化，盈利压力可能抵消估值支持；现有数据无法区分这一驱动。
市场确认：信用利差最新收窄、NFCI水平偏松，与市场仍具承接能力一致；标普月度窗口上涨，但纳斯达克综合对应窗口下降，且信用月度窗口未净改善，尚缺广度及增长盈利确认。股价不是新增美元供给证据。
失效条件：若准备金连续回升、TGA持续回落且回购溢价回归政策锚附近，同时真实收益率下降和信用收窄延续、股指改善趋于一致，分化判断将转向支持；若准备金继续减少、回购溢价持续扩大并伴信用扩张，则转向压制。
覆盖边界：缺增长与盈利修正、估值和行业资金流，不能得出完整股票回报结论。价格指数不含股息，股指窗口日期不完全一致。近期改善与较长窗口约束并存，置信度不能提高至高。
事实引用：trend:DFII5:20obs, trend:DFII7:20obs, trend:DFII5:60obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:TGA:20obs, trend:WRESBAL:5obs, derived:RRP_BUFFER, metric:NFCI, trend:BAMLC0A0CM:20obs, metric:BAMLH0A0HYM2, market:SP500:20obs, market:NASDAQCOM:20obs, coverage:growth_earnings

### BTC：分化（2—12周，低置信度）
判断：真实贴现率回落改善美元背景，但现金缓冲薄与担保融资约束仍在，BTC近期价格尚未确认改善；无法把宏观支持解读为新增现货资金或明确持有机会。
传导：美元实际融资与现金替代收益下降可改善风险承担环境，然而准备金缓冲偏弱和回购溢价会约束杠杆中介。BTC自身现货流量及衍生杠杆可使价格偏离宏观方向，当前缺少这些渠道的数据。
市场确认：BTC最新及近期较短价格窗口下降，未确认折现率缓和已传导为价格支持；较长价格窗口接近平稳也不足以证明流入。美股或信用改善不属于BTC资金流事实。
失效条件：若现金供给持续改善、回购溢价收敛且BTC价格在后续连续观测中恢复升势，并补充到同向现货流量确认，可转向支持；若回购溢价持续扩大、准备金继续减少且BTC弱势延续，则转向压制。
覆盖边界：缺ETF流、稳定币供给、合约未平仓量、资金费率及清算信息，不能判断新增资金入场、去杠杆完成或BTC买入机会。BTC观测含周末，其窗口不能与美股交易日窗口等同。
事实引用：trend:DFII5:20obs, trend:DFII7:20obs, derived:RRP_BUFFER, trend:WRESBAL:5obs, trend:TGA:20obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, market:CBBTCUSD:level, market:CBBTCUSD:5obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：已覆盖名义曲线反应与FRBSF模型的预期短率、期限溢价分解，但未配置直接SOFR期货、调查共识或事件预期差。模型分解与资产价格均不能代表直接共识，无法判断充分计价或存在预期差。

### 基准情景
若资金价格保持有序、现金缓冲未明显修复，而真实贴现率不再上冲，则中期风险承担继续分化，美元因素对两类资产缺少一致推动。
触发：银行间利率继续稳定，回购溢价未持续扩大，准备金在后续周报中未加速减少，同时腹部实际收益率维持近期回落状态、信用未出现持续扩张。
失效：数量缓冲与融资价格同步持续改善，或资金价格与信用同步持续恶化，使当前相互抵消的机制失衡。
事实引用：metric:EFFR, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, trend:WRESBAL:5obs, trend:DFII5:20obs, trend:DFII7:20obs, trend:BAMLH0A0HYM2:20obs

### 改善情景
若上游现金修复与折现率缓和同时延续，流动性可对美股和BTC形成更广泛支持；BTC仍需自身价格与现货资金渠道确认。
触发：TGA连续回落、后续准备金周报转向回升，回购相对政策锚溢价持续收敛；腹部实际收益率下降且信用持续收窄，股指改善趋于一致，BTC价格转强并获得新增流量数据支持。
失效：TGA重新持续积累、准备金修复中断或回购溢价反复扩大；若实际利率回落同时信用扩张，则不能认定为良性宽松。
事实引用：derived:TGA_FLOW, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:DFII5, metric:DFII7, metric:BAMLH0A0HYM2, market:SP500:20obs, market:NASDAQCOM:20obs, market:CBBTCUSD:20obs, coverage:btc_flows_leverage, coverage:growth_earnings

### 恶化情景
若现金需求进一步触及准备金并进入融资与信用价格，流动性对美股和BTC的贡献将转向压制；若再伴日元升值和波动放大，杠杆调整可能放大传导。
触发：后续净结算信息与TGA持续上升、准备金继续下降相互确认，同时回购溢价及尾部持续抬升、信用利差扩大；日元快速升值与实现波动上升若同步出现，将构成额外确认。公告毛发行本身不满足触发条件。
失效：结算期间TGA未持续上升、准备金企稳回升且回购溢价收敛，信用保持稳定，表明现金需求被有序吸收。
事实引用：calendar:7d, event:gross_total_by_issue_date:2026-11-05, metric:TGA, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR, metric:SOFR_VOLUME, metric:BAMLH0A0HYM2, jpy:USDJPY, jpy:USDJPY_VOL20

### 下一轮核查
- 核查更新后的核心资金利率、SOFR成交规模与尾部，重点区分最新缓解延续还是溢价重新扩大，并补齐常备回购结果。
- 追踪TGA连续方向与后续准备金周报，结合2026-11-05结算到期净额，验证公告供给是否实际形成现金压力。
- 观察名义腹部与实际收益率回落能否同信用收窄延续，并补充增长和盈利修正以辨别利率下降的经济含义。
- 补齐BTC现货ETF流、稳定币及合约杠杆数据，验证价格弱势与宏观折现率缓和之间的背离。
- 更新离岸融资基差、同日期美日利差和CFTC仓位，修复日本国债来源及派生元数据问题。

### 中期趋势（有效观测数，日频与周频分开）
- ICE BofA US Corporate OAS：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 -0.020000000000000018 %；状态 ok；trend:BAMLC0A0CM:5obs
- ICE BofA US Corporate OAS：20个有效日频观测间隔变化：2026-09-30 至 2026-10-28；20期；变化 0.020000000000000018 %；状态 ok；trend:BAMLC0A0CM:20obs
- ICE BofA US Corporate OAS：60个有效日频观测间隔变化：2026-08-05 至 2026-10-28；60期；变化 0.07999999999999996 %；状态 ok；trend:BAMLC0A0CM:60obs
- ICE BofA US High Yield OAS：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 -0.1299999999999999 %；状态 ok；trend:BAMLH0A0HYM2:5obs
- ICE BofA US High Yield OAS：20个有效日频观测间隔变化：2026-09-30 至 2026-10-28；20期；变化 0.020000000000000018 %；状态 ok；trend:BAMLH0A0HYM2:20obs
- ICE BofA US High Yield OAS：60个有效日频观测间隔变化：2026-08-05 至 2026-10-28；60期；变化 0.3900000000000001 %；状态 ok；trend:BAMLH0A0HYM2:60obs
- Broad General Collateral Rate：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.06000000000000005 %；状态 ok；trend:BGCR:5obs
- Broad General Collateral Rate：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 0.04999999999999982 %；状态 ok；trend:BGCR:20obs
- Broad General Collateral Rate：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.29000000000000004 %；状态 ok；trend:BGCR:60obs
- 10-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.010000000000000231 %；状态 ok；trend:DFII10:5obs
- 10-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.30000000000000027 %；状态 ok；trend:DFII10:20obs
- 10-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.22999999999999998 %；状态 ok；trend:DFII10:60obs
- 5-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.020000000000000018 %；状态 ok；trend:DFII5:5obs
- 5-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.41999999999999993 %；状态 ok；trend:DFII5:20obs
- 5-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.16999999999999993 %；状态 ok；trend:DFII5:60obs
- 7-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.020000000000000018 %；状态 ok；trend:DFII7:5obs
- 7-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.3599999999999999 %；状态 ok；trend:DFII7:20obs
- 7-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.20000000000000018 %；状态 ok；trend:DFII7:60obs
- 1年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.009999999999999787 %；状态 ok；trend:DGS1:5obs
- 1年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.1200000000000001 %；状态 ok；trend:DGS1:20obs
- 1年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.3799999999999999 %；状态 ok；trend:DGS1:60obs
- 10年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.020000000000000462 %；状态 ok；trend:DGS10:5obs
- 10年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.3099999999999996 %；状态 ok；trend:DGS10:20obs
- 10年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.35000000000000053 %；状态 ok；trend:DGS10:60obs
- 2年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.040000000000000036 %；状态 ok；trend:DGS2:5obs
- 2年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.2699999999999996 %；状态 ok；trend:DGS2:20obs
- 2年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.41000000000000014 %；状态 ok；trend:DGS2:60obs
- 3年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.010000000000000675 %；状态 ok；trend:DGS3:5obs
- 3年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.2699999999999996 %；状态 ok；trend:DGS3:20obs
- 3年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.4800000000000004 %；状态 ok；trend:DGS3:60obs
- 5年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.0 %；状态 ok；trend:DGS5:5obs
- 5年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.3099999999999996 %；状态 ok；trend:DGS5:20obs
- 5年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.4500000000000002 %；状态 ok；trend:DGS5:60obs
- 7年期国债收益率：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.009999999999999787 %；状态 ok；trend:DGS7:5obs
- 7年期国债收益率：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.3200000000000003 %；状态 ok；trend:DGS7:20obs
- 7年期国债收益率：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.40000000000000036 %；状态 ok；trend:DGS7:60obs
- Trade-weighted broad dollar index：5个有效日频观测间隔变化：2026-10-16 至 2026-10-23；5期；变化 -0.08459999999999468 index；状态 stale；trend:DTWEXBGS:5obs
- Trade-weighted broad dollar index：20个有效日频观测间隔变化：2026-09-24 至 2026-10-23；20期；变化 0.768100000000004 index；状态 stale；trend:DTWEXBGS:20obs
- Trade-weighted broad dollar index：60个有效日频观测间隔变化：2026-07-29 至 2026-10-23；60期；变化 0.5310000000000059 index；状态 stale；trend:DTWEXBGS:60obs
- Effective Federal Funds Rate：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.0 %；状态 ok；trend:EFFR:5obs
- Effective Federal Funds Rate：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 0.0 %；状态 ok；trend:EFFR:20obs
- Effective Federal Funds Rate：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.25 %；状态 ok；trend:EFFR:60obs
- FRBSF average expected overnight rate over next 10 years：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 -0.02268800000000004 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:5obs
- FRBSF average expected overnight rate over next 10 years：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 -0.11309600000000009 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:20obs
- FRBSF average expected overnight rate over next 10 years：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.28290499999999996 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:60obs
- FRBSF average expected overnight rate over next 2 years：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 -0.028519000000000183 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:5obs
- FRBSF average expected overnight rate over next 2 years：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 -0.12869300000000017 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:20obs
- FRBSF average expected overnight rate over next 2 years：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.5010679999999996 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:60obs
- FRBSF 10-year Treasury term premium：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 -0.0486120000000001 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:5obs
- FRBSF 10-year Treasury term premium：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 -0.09870400000000012 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:20obs
- FRBSF 10-year Treasury term premium：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 -0.023005000000000164 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:60obs
- Interest on Reserve Balances：5个有效日频观测间隔变化：2026-10-25 至 2026-10-30；5期；变化 0.0 %；状态 ok；trend:IORB:5obs
- Interest on Reserve Balances：20个有效日频观测间隔变化：2026-10-10 至 2026-10-30；20期；变化 0.0 %；状态 ok；trend:IORB:20obs
- Interest on Reserve Balances：60个有效日频观测间隔变化：2026-08-31 至 2026-10-30；60期；变化 0.25 %；状态 ok；trend:IORB:60obs
- Chicago Fed National Financial Conditions Index：5个有效周频观测间隔变化：2026-09-18 至 2026-10-23；5期；变化 0.041000000000000036 index；状态 ok；trend:NFCI:5obs
- Chicago Fed National Financial Conditions Index：20个有效周频观测间隔变化：2026-06-05 至 2026-10-23；20期；变化 0.02200000000000002 index；状态 ok；trend:NFCI:20obs
- Chicago Fed National Financial Conditions Index：60个有效周频观测间隔变化：2025-08-29 至 2026-10-23；60期；变化 0.040000000000000036 index；状态 ok；trend:NFCI:60obs
- Overnight Bank Funding Rate：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.0 %；状态 ok；trend:OBFR:5obs
- Overnight Bank Funding Rate：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 0.0 %；状态 ok；trend:OBFR:20obs
- Overnight Bank Funding Rate：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.25 %；状态 ok；trend:OBFR:60obs
- Overnight Reverse Repo accepted amount：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.0020000000000000018 USD bn；状态 ok；trend:RRPONTSYD:5obs
- Overnight Reverse Repo accepted amount：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -11.186 USD bn；状态 ok；trend:RRPONTSYD:20obs
- Overnight Reverse Repo accepted amount：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 -1.898 USD bn；状态 ok；trend:RRPONTSYD:60obs
- Secured Overnight Financing Rate：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.06000000000000005 %；状态 ok；trend:SOFR:5obs
- Secured Overnight Financing Rate：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 0.06000000000000005 %；状态 ok；trend:SOFR:20obs
- Secured Overnight Financing Rate：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.29000000000000004 %；状态 ok；trend:SOFR:60obs
- SOFR transaction volume：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 132.0 USD bn；状态 ok；trend:SOFR_VOLUME:5obs
- SOFR transaction volume：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 107.0 USD bn；状态 ok；trend:SOFR_VOLUME:20obs
- SOFR transaction volume：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 19.0 USD bn；状态 ok；trend:SOFR_VOLUME:60obs
- SOMA holdings / QT background：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -9.215094331399087 USD bn；状态 ok；trend:SOMA:5obs
- SOMA holdings / QT background：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 14.961344576400734 USD bn；状态 ok；trend:SOMA:20obs
- SOMA holdings / QT background：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 160.9273346189011 USD bn；状态 ok；trend:SOMA:60obs
- Treasury General Account closing balance：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 70.47899999999993 USD bn；状态 ok；trend:TGA:5obs
- Treasury General Account closing balance：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 79.03199999999993 USD bn；状态 ok；trend:TGA:20obs
- Treasury General Account closing balance：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 145.54899999999998 USD bn；状态 ok；trend:TGA:60obs
- Tri-party General Collateral Rate：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.06000000000000005 %；状态 ok；trend:TGCR:5obs
- Tri-party General Collateral Rate：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 0.04999999999999982 %；状态 ok；trend:TGCR:20obs
- Tri-party General Collateral Rate：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 0.29000000000000004 %；状态 ok；trend:TGCR:60obs
- CBOE Volatility Index: VIX：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 0.23000000000000043 index；状态 ok；trend:VIXCLS:5obs
- CBOE Volatility Index: VIX：20个有效日频观测间隔变化：2026-09-30 至 2026-10-28；20期；变化 0.5700000000000003 index；状态 ok；trend:VIXCLS:20obs
- CBOE Volatility Index: VIX：60个有效日频观测间隔变化：2026-08-05 至 2026-10-28；60期；变化 1.0999999999999996 index；状态 ok；trend:VIXCLS:60obs
- Reserve balances with Federal Reserve Banks：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -36.42300000000023 USD bn；状态 ok；trend:WRESBAL:5obs
- Reserve balances with Federal Reserve Banks：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 -186.95299999999997 USD bn；状态 ok；trend:WRESBAL:20obs
- Reserve balances with Federal Reserve Banks：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 -287.93100000000004 USD bn；状态 ok；trend:WRESBAL:60obs
- 同日SOFR减IORB：5个有效日频观测间隔变化：2026-10-21 至 2026-10-28；5期；变化 6.000000000000005 bp；状态 ok；trend:SOFR_IORB:5obs
- 同日SOFR减IORB：20个有效日频观测间隔变化：2026-09-29 至 2026-10-28；20期；变化 6.000000000000005 bp；状态 ok；trend:SOFR_IORB:20obs
- 同日SOFR减IORB：60个有效日频观测间隔变化：2026-08-03 至 2026-10-28；60期；变化 4.0000000000000036 bp；状态 ok；trend:SOFR_IORB:60obs

### 已公告结算日历（毛额，不等于净融资）
- {"fact_id": "calendar:7d", "id": "ANNOUNCED_SETTLEMENTS_7D", "name": "未来7日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-10-30", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 7, "window_start": "2026-10-30", "window_end": "2026-11-05", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:28d", "id": "ANNOUNCED_SETTLEMENTS_28D", "name": "未来28日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-10-30", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 28, "window_start": "2026-10-30", "window_end": "2026-11-26", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:84d", "id": "ANNOUNCED_SETTLEMENTS_84D", "name": "未来84日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-10-30", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 84, "window_start": "2026-10-30", "window_end": "2027-01-21", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}

### 判断验证记录
这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，从其日期往后两日开始寻找首个有效收盘作为观察起点；评估只使用截至评估时刻UTC日期往前两日的价格。美股按10／20／60个后续有效收盘观察（约2／4／12周），BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。同一快照与方法版本仅首次发布算一个样本。去重后的持有窗口仍可能重叠，不能当作统计独立样本；历史价格截断或起点缺价时不把观察起点向后漂移。收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。所有已成熟样本均保留；分组不足十个样本时明确标为积累中，样本充足时仍只提供描述统计，预测能力需要另行样本外检验。
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}

## 银行间稳定，回购边际缓和
银行间无抵押利率持平；SOFR相对政策锚仍为正溢价，但最新收窄，交易量与价格乘规模代理同步下降。该代理不是实际总成本。
EFFR：3.88%（2026-10-28，+0.00%）；daily T+1。
OBFR：3.88%（2026-10-28，+0.00%）；daily T+1。
SOFR_ANCHOR：4.00bp（2026-10-28，-1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3074.00bn（2026-10-28，-73.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：3.42mn/day（2026-10-28，-0.96mn/day）；日频，纽约联储SOFR记录随利率一同发布。

## 最新现金流与较长窗口方向分化
TGA最新下降，但近期日频窗口净上升；RRP最新回升，周度准备金下降。不同频率与区间的变化可以并存，不能直接拼接为会计归因。
TGA_FLOW：-36.90bn（2026-10-28，-68.73bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
RRP_FLOW：0.18bn（2026-10-29，环比未知）；日频，纽约联储每日操作结果。
TGA：1015.63bn（2026-10-28，+79.03bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。

## 名义腹部与真实贴现率最新回落
近端、中段与腹部名义收益率最新均下降，腹部实际收益率和通胀补偿也回落。通胀补偿包含风险溢价及TIPS流动性影响，不能直接等同纯通胀预期。
DGS1：4.42%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.73%（2026-10-29，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.78%（2026-10-29，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.87%（2026-10-29，-0.08%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.31%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.46%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.47%（2026-10-29，-0.02%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.41%（2026-10-29，-0.03%）；日频，FRED/H.15国债恒定期限收益率。

## 短债拍卖须结合规模与可比性
最新短债拍卖已提供发行规模、加权认购倍数及预计算压力代理。由于跨场期限组合的可比性未获确认，不能把表面变化直接解读为同类需求恶化，压力代理亦不能证明拍卖吸收失败。
TBILL_AUCTION_SIZE：225.00bn（2026-10-29，+150.00bn）；event-based。
TBILL_AUCTION_BTC：2.87ratio（2026-10-29，-0.21ratio）；event-based。
TBILL_AUCTION_STRESS：50.00index（2026-10-29，+50.00index）；事件驱动，财政部T-bill拍卖后公布。

## 信用缓和与风险资产表现并不一致
信用利差和VIX最新下降，但各自观测窗口内标普与纳斯达克综合表现分化，BTC近期价格窗口下降。下游反应尚未形成共同改善，也不能反推上游现金增加。
BAMLC0A0CM：0.86%（2026-10-28，-0.02%）；daily T+1。
BAMLH0A0HYM2：3.14%（2026-10-28，-0.04%）；daily T+1。
VIXCLS：16.91index（2026-10-28，-0.61index）；daily T+1。
SP500：1.21%（2026-10-28，+1.21%）；daily close / US trading observations。
NASDAQCOM：-2.56%（2026-10-29，-2.56%）；daily close / US trading observations。
CBBTCUSD：-5.58%（2026-10-29，-5.58%）；daily / 7-day observations。

## 现金缓冲薄，后续冲击敏感度上升
可继续释放的RRP缓冲有限，准备金近期多周减少且TGA在月度窗口净积累，使后续现金需求更可能触及银行体系。银行间利率稳定是重要反证，当前不能据此认定准备金已经稀缺。
RRP_BUFFER：0.35bn（2026-10-29，+0.18bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-36.42bn）；weekly。
TGA：1015.63bn（2026-10-28，+79.03bn）；daily T+1。
EFFR：3.88%（2026-10-28，+0.00%）；daily T+1。

## 公告结算仅构成有条件的融资风险
上述条件成立时，发行结算可能强化现金竞争并传导至抵押融资。当前只有已公告毛发行，到期、净融资及净现金影响未知，不能预认确定性抽水。
event:gross_total_by_issue_date:2026-11-05：日期未知；状态 unknown；无可用数值。
ANNOUNCED_SETTLEMENTS_7D：277.00bn（2026-10-30，环比未知）；announced event schedule。
TGA：1015.63bn（2026-10-28，-36.90bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
SOFR_ANCHOR：4.00bp（2026-10-28，-1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3074.00bn（2026-10-28，-73.00bn）；daily T+1。

## 离岸、尾部融资及部分派生元数据覆盖不足
商业票据、美元指数及交割失败陈旧，常备回购结果缺失；日本国债为混合来源且缺少历史窗口，同日期美日长端利差缺失。CFTC解释文字中的净空头表述与净头寸方向不一致，采用结构化多空变化及净持仓方向。腹部组合底层引用不完整，交易量行分布字段亦呈利率口径，不用于量的分位判断。这些缺口不能计作市场中性。
quality:stale_metric:DCPN3M：2026-10-13；状态 stale；无可用数值。
quality:stale_metric:DTWEXBGS：2026-10-23；状态 stale；无可用数值。
quality:stale_metric:REPO_FAILS_UST：2026-10-14；状态 stale；无可用数值。
quality:missing_metric:SRP_ACCEPTED：日期未知；状态 missing；无可用数值。
quality:jpy_missing:US_JP_10Y：日期未知；状态 missing；无可用数值。
JGB10：2.77原始比例/口径（2026-10-30，环比未知）；按来源频率。
jpy:CFTC_DECOMPOSITION：日期未知；状态 unknown；无可用数值。
CFTC_JPY_NET_OI：0.18原始比例/口径（2026-10-20，+0.05原始比例/口径）；按来源频率。
UST_BELLY_MOMENTUM：-6.75bp（2026-10-29，环比未知）；日频，FRED/H.15国债恒定期限收益率。
SOFR_VOLUME：3074.00bn（2026-10-28，-73.00bn）；daily T+1。