# 美元流动性分析
2026-11-11 19:19:27 UTC+08:00

中性偏紧
2026-11-11 新抓取快照覆盖最新可得但不同步的观测，境内隔夜融资平稳，薄弱的逆回购缓冲与回升的实际贴现率使整体偏紧，离岸融资直接证据有限。

## 美股与BTC中期投资研究
现金供给层的逆回购缓冲薄，准备金五周净降但最新一周回升。融资及折现层的隔夜资金价格平稳，腹部实际收益率短窗反弹、近月净降、较长窗口上升。下游股指与BTC价格在各自多期窗口偏弱，信用和VIX近期回落提供反向证据。中期流动性对风险承担偏压制，BTC专属渠道的确认更弱。

相对上次：相对上次成功抓取，可比较的隔夜融资与成交规模、TGA、逆回购、准备金、SOMA、美债名义与实际收益率、信用和VIX均未出现实质更新。比较事实未覆盖股指及BTC，无法核对其跨包变化。

### 美股：压制（2—12周，中等置信度）
判断：薄现金缓冲及实际收益率短窗反弹压制久期敏感估值。近月实际利率仍净降，近期信用改善，对压力形成缓冲。
传导：实际无风险收益上升会提高估值贴现率，信用利差若重新走阔还会提高企业融资成本。实际利率下降可缓解估值压力，但若伴随增长恶化或盈利下修，现金流预期可能同步走弱。
市场确认：截至 2026-11-10，标普与纳斯达克综合指数在近周、近月及较长交易观测窗口均走弱，纳斯达克综合指数跌幅更深。信用与VIX短线回落尚未确认持续修复，缺增长和盈利修正验证。
失效条件：若腹部实际收益率连续回落、周度准备金趋稳，信用利差持续收窄且股指在后续多个交易观测中企稳，则撤销偏压制判断。
覆盖边界：美股采用交易日价格指数。缺增长与盈利修正，无法形成完整股票回报判断，股价走势只作下游确认。
事实引用：derived:RRP_BUFFER, trend:WRESBAL:5obs, trend:DFII5:5obs, trend:DFII5:20obs, trend:DFII7:60obs, trend:BAMLH0A0HYM2:5obs, metric:VIXCLS, market:SP500:5obs, market:SP500:20obs, market:SP500:60obs, market:NASDAQCOM:5obs, market:NASDAQCOM:20obs, market:NASDAQCOM:60obs, coverage:growth_earnings

### BTC：压制（2—12周，低置信度）
判断：实际收益率反弹及偏强美元构成流动性逆风，境内隔夜融资平稳限制了对美元资金冲击的判断。
传导：较高实际收益率提高持有非生息资产的机会成本，偏强美元与薄缓冲可能降低风险承接。BTC自身现货资金流及衍生杠杆会改变传导强度。
市场确认：截至 2026-11-10，Coinbase现货在短窗、近月窗口及较长窗口均走弱，仅确认价格表现。ETF净流、稳定币供给及合约仓位和资金费缺失，资金进出与去杠杆进度未知。
失效条件：若实际收益率持续回落、广义美元转弱，BTC在连续现货观测中企稳，且补齐的数据确认现货净流改善及衍生杠杆未同步扩张，则撤销偏压制判断。
覆盖边界：Coinbase日频含周末，近月价格窗口为 2026-10-21 至 2026-11-10，与美股交易日窗口不同。缺ETF、稳定币及衍生品数据，美元指数也缺跨币种基差验证。
事实引用：derived:RRP_BUFFER, trend:EFFR:20obs, trend:DFII5:5obs, trend:DFII7:60obs, trend:DTWEXBGS:20obs, market:CBBTCUSD:5obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：名义曲线反映已观察到的价格重估，FRBSF提供平均预期短率和期限溢价的模型估计。缺SOFR期货、调查共识及事件预期差，实际政策路径定价与已计价程度无法直接核实。

### 基准情景
从快照出发，隔夜资金市场保持平稳，薄缓冲与偏高的实际贴现率继续限制美股和BTC的风险承接。
触发：后续可比观测中隔夜利率相对有效同日参照及常备回购用量保持平稳，腹部实际利率和信用未形成同向持续变化。
失效：连续出现准备金趋稳且实际收益率与信用利差共降，或结算后准备金转弱且隔夜融资价格同步上行。
事实引用：metric:EFFR, metric:SOFR, metric:SOFR_VOLUME, metric:SRP_ACCEPTED, derived:RRP_BUFFER, metric:DFII5, metric:BAMLH0A0HYM2, calendar:7d

### 改善情景
现金缓冲趋稳与真实贴现率下降可缓解股市估值和BTC的美元流动性逆风，BTC传导仍取决于现货承接。
触发：连续周度准备金企稳、TGA停止持续补库，且多个交易日腹部实际收益率回落与信用利差收窄并存。
失效：实际收益率重新持续上行，或其下行伴随信用利差持续走阔。
事实引用：metric:WRESBAL, trend:WRESBAL:5obs, trend:TGA:20obs, metric:DFII5, metric:DFII7, metric:BAMLH0A0HYM2, coverage:btc_flows_leverage

### 恶化情景
若财政净现金吸收挤压准备金并传至核心融资价格，信用压力可进一步压低美股与BTC的风险承接。
触发：若确认快照公告所涉结算净现金吸收，随后TGA持续回补、准备金走低，且连续可比观测中SOFR相对同日参照抬升并伴随成交量或常备回购用量走高。
失效：结算后TGA回落且准备金企稳，同时隔夜资金价格和常备回购用量未持续上升。
事实引用：calendar:7d, derived:RRP_BUFFER, derived:TGA_FLOW, metric:WRESBAL, metric:SOFR, metric:SOFR_VOLUME, metric:SRP_ACCEPTED, metric:POLICY_UPPER_NYFED, metric:BAMLH0A0HYM2

### 下一轮核查
- 补齐同日IORB，核对SOFR、EFFR、回购成交量、利率上尾及常备回购用量是否同步转紧。
- 核对快照公告所列结算日的到期抵扣、净现金流、TGA路径与随后周度准备金。
- 核对5Y与7Y实际收益率反弹能否延续，并用信用利差、VIX、增长与盈利修正检验美股传导。
- 核对BTC现货企稳的连续性，补充ETF净流、稳定币供给、合约持仓及资金费。
- 补充直接政策预期、跨币种基差和同日美日利差，核对政策重估及离岸传导。

### 中期趋势（有效观测数，日频与周频分开）
- ICE BofA US Corporate OAS：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.029999999999999916 %；状态 ok；trend:BAMLC0A0CM:5obs
- ICE BofA US Corporate OAS：20个有效日频观测间隔变化：2026-10-12 至 2026-11-09；20期；变化 0.08000000000000007 %；状态 ok；trend:BAMLC0A0CM:20obs
- ICE BofA US Corporate OAS：60个有效日频观测间隔变化：2026-08-17 至 2026-11-09；60期；变化 0.09999999999999998 %；状态 ok；trend:BAMLC0A0CM:60obs
- ICE BofA US High Yield OAS：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.0900000000000003 %；状态 ok；trend:BAMLH0A0HYM2:5obs
- ICE BofA US High Yield OAS：20个有效日频观测间隔变化：2026-10-12 至 2026-11-09；20期；变化 0.22999999999999998 %；状态 ok；trend:BAMLH0A0HYM2:20obs
- ICE BofA US High Yield OAS：60个有效日频观测间隔变化：2026-08-17 至 2026-11-09；60期；变化 0.6399999999999997 %；状态 ok；trend:BAMLH0A0HYM2:60obs
- Broad General Collateral Rate：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.06000000000000005 %；状态 ok；trend:BGCR:5obs
- Broad General Collateral Rate：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 0.009999999999999787 %；状态 ok；trend:BGCR:20obs
- Broad General Collateral Rate：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.2599999999999998 %；状态 ok；trend:BGCR:60obs
- 10-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.1299999999999999 %；状态 ok；trend:DFII10:5obs
- 10-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.10000000000000009 %；状态 ok；trend:DFII10:20obs
- 10-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.36999999999999966 %；状态 ok；trend:DFII10:60obs
- 5-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.20999999999999996 %；状态 ok；trend:DFII5:5obs
- 5-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.10999999999999988 %；状态 ok；trend:DFII5:20obs
- 5-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.43999999999999995 %；状态 ok；trend:DFII5:60obs
- 7-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.16999999999999993 %；状态 ok；trend:DFII7:5obs
- 7-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.10999999999999988 %；状态 ok；trend:DFII7:20obs
- 7-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.41000000000000014 %；状态 ok；trend:DFII7:60obs
- 1年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.15999999999999925 %；状态 ok；trend:DGS1:5obs
- 1年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 0.07999999999999918 %；状态 ok；trend:DGS1:20obs
- 1年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.5799999999999996 %；状态 ok；trend:DGS1:60obs
- 10年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.03000000000000025 %；状态 ok；trend:DGS10:5obs
- 10年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.22999999999999954 %；状态 ok；trend:DGS10:20obs
- 10年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.3000000000000007 %；状态 ok；trend:DGS10:60obs
- 2年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.1200000000000001 %；状态 ok；trend:DGS2:5obs
- 2年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.05999999999999961 %；状态 ok；trend:DGS2:20obs
- 2年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.5600000000000005 %；状态 ok；trend:DGS2:60obs
- 3年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.0600000000000005 %；状态 ok；trend:DGS3:5obs
- 3年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.16000000000000014 %；状态 ok；trend:DGS3:20obs
- 3年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.5 %；状态 ok；trend:DGS3:60obs
- 5年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.0699999999999994 %；状态 ok；trend:DGS5:5obs
- 5年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.1900000000000004 %；状态 ok；trend:DGS5:20obs
- 5年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.4499999999999993 %；状态 ok；trend:DGS5:60obs
- 7年期国债收益率：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.05999999999999961 %；状态 ok；trend:DGS7:5obs
- 7年期国债收益率：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.22000000000000064 %；状态 ok；trend:DGS7:20obs
- 7年期国债收益率：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.3799999999999999 %；状态 ok；trend:DGS7:60obs
- Trade-weighted broad dollar index：5个有效日频观测间隔变化：2026-10-30 至 2026-11-06；5期；变化 0.21470000000000766 index；状态 ok；trend:DTWEXBGS:5obs
- Trade-weighted broad dollar index：20个有效日频观测间隔变化：2026-10-08 至 2026-11-06；20期；变化 0.433400000000006 index；状态 ok；trend:DTWEXBGS:20obs
- Trade-weighted broad dollar index：60个有效日频观测间隔变化：2026-08-12 至 2026-11-06；60期；变化 2.7623999999999995 index；状态 ok；trend:DTWEXBGS:60obs
- Effective Federal Funds Rate：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 0.0 %；状态 ok；trend:EFFR:5obs
- Effective Federal Funds Rate：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 0.0 %；状态 ok；trend:EFFR:20obs
- Effective Federal Funds Rate：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.25 %；状态 ok；trend:EFFR:60obs
- FRBSF average expected overnight rate over next 10 years：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.0345920000000004 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:5obs
- FRBSF average expected overnight rate over next 10 years：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 -0.19513000000000025 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:20obs
- FRBSF average expected overnight rate over next 10 years：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.18948799999999988 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:60obs
- FRBSF average expected overnight rate over next 2 years：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.05631599999999981 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:5obs
- FRBSF average expected overnight rate over next 2 years：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 -0.19094100000000047 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:20obs
- FRBSF average expected overnight rate over next 2 years：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.3868549999999997 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:60obs
- FRBSF 10-year Treasury term premium：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 0.000992000000000104 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:5obs
- FRBSF 10-year Treasury term premium：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 -0.1260699999999999 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:20obs
- FRBSF 10-year Treasury term premium：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.020712000000000064 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:60obs
- Chicago Fed National Financial Conditions Index：5个有效周频观测间隔变化：2026-09-25 至 2026-10-30；5期；变化 0.05099999999999999 index；状态 ok；trend:NFCI:5obs
- Chicago Fed National Financial Conditions Index：20个有效周频观测间隔变化：2026-06-12 至 2026-10-30；20期；变化 0.044999999999999984 index；状态 ok；trend:NFCI:20obs
- Chicago Fed National Financial Conditions Index：60个有效周频观测间隔变化：2025-09-05 至 2026-10-30；60期；变化 0.068 index；状态 ok；trend:NFCI:60obs
- Overnight Bank Funding Rate：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 0.0 %；状态 ok；trend:OBFR:5obs
- Overnight Bank Funding Rate：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 0.0 %；状态 ok；trend:OBFR:20obs
- Overnight Bank Funding Rate：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.25 %；状态 ok；trend:OBFR:60obs
- Overnight Reverse Repo accepted amount：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 -0.275 USD bn；状态 ok；trend:RRPONTSYD:5obs
- Overnight Reverse Repo accepted amount：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 -0.12300000000000003 USD bn；状态 ok；trend:RRPONTSYD:20obs
- Overnight Reverse Repo accepted amount：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 -0.098 USD bn；状态 ok；trend:RRPONTSYD:60obs
- Secured Overnight Financing Rate：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.07000000000000028 %；状态 ok；trend:SOFR:5obs
- Secured Overnight Financing Rate：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 0.009999999999999787 %；状态 ok；trend:SOFR:20obs
- Secured Overnight Financing Rate：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.2599999999999998 %；状态 ok；trend:SOFR:60obs
- SOFR transaction volume：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -168.0 USD bn；状态 ok；trend:SOFR_VOLUME:5obs
- SOFR transaction volume：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 139.0 USD bn；状态 ok；trend:SOFR_VOLUME:20obs
- SOFR transaction volume：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 168.0 USD bn；状态 ok；trend:SOFR_VOLUME:60obs
- SOMA holdings / QT background：5个有效周频观测间隔变化：2026-09-30 至 2026-11-04；5期；变化 -0.9568710189996636 USD bn；状态 ok；trend:SOMA:5obs
- SOMA holdings / QT background：20个有效周频观测间隔变化：2026-06-17 至 2026-11-04；20期；变化 10.08881227710117 USD bn；状态 ok；trend:SOMA:20obs
- SOMA holdings / QT background：60个有效周频观测间隔变化：2025-09-10 至 2026-11-04；60期；变化 162.75433461890043 USD bn；状态 ok；trend:SOMA:60obs
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-11-03 至 2026-11-10；5期；变化 0.0 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-10-13 至 2026-11-10；20期；变化 0.005 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-14 至 2026-11-10；60期；变化 0.005 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
- Treasury General Account closing balance：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -8.12399999999991 USD bn；状态 ok；trend:TGA:5obs
- Treasury General Account closing balance：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 50.107000000000085 USD bn；状态 ok；trend:TGA:20obs
- Treasury General Account closing balance：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 -43.95399999999995 USD bn；状态 ok；trend:TGA:60obs
- Tri-party General Collateral Rate：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -0.06000000000000005 %；状态 ok；trend:TGCR:5obs
- Tri-party General Collateral Rate：20个有效日频观测间隔变化：2026-10-09 至 2026-11-09；20期；变化 0.009999999999999787 %；状态 ok；trend:TGCR:20obs
- Tri-party General Collateral Rate：60个有效日频观测间隔变化：2026-08-13 至 2026-11-09；60期；变化 0.2599999999999998 %；状态 ok；trend:TGCR:60obs
- CBOE Volatility Index: VIX：5个有效日频观测间隔变化：2026-11-02 至 2026-11-09；5期；变化 -1.2299999999999969 index；状态 ok；trend:VIXCLS:5obs
- CBOE Volatility Index: VIX：20个有效日频观测间隔变化：2026-10-12 至 2026-11-09；20期；变化 4.710000000000001 index；状态 ok；trend:VIXCLS:20obs
- CBOE Volatility Index: VIX：60个有效日频观测间隔变化：2026-08-17 至 2026-11-09；60期；变化 4.730000000000002 index；状态 ok；trend:VIXCLS:60obs
- Reserve balances with Federal Reserve Banks：5个有效周频观测间隔变化：2026-09-30 至 2026-11-04；5期；变化 -18.001999999999953 USD bn；状态 ok；trend:WRESBAL:5obs
- Reserve balances with Federal Reserve Banks：20个有效周频观测间隔变化：2026-06-17 至 2026-11-04；20期；变化 -103.35599999999977 USD bn；状态 ok；trend:WRESBAL:20obs
- Reserve balances with Federal Reserve Banks：60个有效周频观测间隔变化：2025-09-10 至 2026-11-04；60期；变化 -230.6859999999997 USD bn；状态 ok；trend:WRESBAL:60obs

### 已公告结算日历（毛额，不等于净融资）
- {"fact_id": "calendar:7d", "id": "ANNOUNCED_SETTLEMENTS_7D", "name": "未来7日已公告结算毛发行（含快照日）", "value": 325.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-11", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 7, "window_start": "2026-11-11", "window_end": "2026-11-17", "event_count": 4, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 325.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-12:Bill:17-Week:912797XH5", "event:auction:2026-11-12:Bill:4-Week:912797WF0", "event:auction:2026-11-12:Bill:8-Week:912797WP8", "event:auction:2026-11-12:Bond:30-Year:912810UY2"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:28d", "id": "ANNOUNCED_SETTLEMENTS_28D", "name": "未来28日已公告结算毛发行（含快照日）", "value": 325.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-11", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 28, "window_start": "2026-11-11", "window_end": "2026-12-08", "event_count": 4, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 325.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-12:Bill:17-Week:912797XH5", "event:auction:2026-11-12:Bill:4-Week:912797WF0", "event:auction:2026-11-12:Bill:8-Week:912797WP8", "event:auction:2026-11-12:Bond:30-Year:912810UY2"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:84d", "id": "ANNOUNCED_SETTLEMENTS_84D", "name": "未来84日已公告结算毛发行（含快照日）", "value": 325.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-11", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 84, "window_start": "2026-11-11", "window_end": "2027-02-02", "event_count": 4, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 325.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-12:Bill:17-Week:912797XH5", "event:auction:2026-11-12:Bill:4-Week:912797WF0", "event:auction:2026-11-12:Bill:8-Week:912797WP8", "event:auction:2026-11-12:Bond:30-Year:912810UY2"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}

### 判断验证记录
这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，从其日期往后两日开始寻找首个有效收盘作为观察起点；评估只使用截至评估时刻UTC日期往前两日的价格。美股按10／20／60个后续有效收盘观察（约2／4／12周），BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。同一快照与方法版本仅首次发布算一个样本。去重后的持有窗口仍可能重叠，不能当作统计独立样本；历史价格截断或起点缺价时不把观察起点向后漂移。收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。所有已成熟样本均保留；分组不足十个样本时明确标为积累中，样本充足时仍只提供描述统计，预测能力需要另行样本外检验。早期研究归档不完整，缺失运行 20261030_135123_15fc84aa 及其更早链路。当前统计覆盖通过清单校验的记录。
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-02", "entry_price": 7541.4, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "observations_available": 5}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-11-18"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-12-02"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2027-01-27"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 7688.62, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "observations_available": 3}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-11-18"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2026-12-02"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-04", "entry_price": 80420.06, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04", "target_exit_date": "2027-01-27"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 2}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 2}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 7353.73, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "observations_available": 2}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2026-11-19"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2026-12-03"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": "2026-11-05", "entry_price": 76152.52, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05", "target_exit_date": "2027-01-28"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "压制", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}
- {"run_id": "20261111_192802_9400e970", "published_at_bjt": "2026-11-11T19:28:03.328581+08:00", "source_generated_at_bjt": "2026-11-11T19:19:27+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-09", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-13"}

## 隔夜回购价量同降
SOFR随成交规模回落至与持平的EFFR同水平，OBFR也持平，最新融资读数未显示抵押融资相对无抵押融资变贵。
SOFR：3.88%（2026-11-09，-0.01%）；daily T+1。
SOFR_VOLUME：3100.00bn（2026-11-09，-74.00bn）；daily T+1。
EFFR：3.88%（2026-11-09，+0.00%）；daily T+1。
OBFR：3.88%（2026-11-09，+0.00%）；daily T+1。

## 腹部真实贴现率上升
5Y与7Y名义及官方实际收益率同步上升，同期限通胀补偿基本持平，最新名义上行集中在实际利率分量。
DGS5：4.81%（2026-11-10，+0.14%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.89%（2026-11-10，+0.13%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.56%（2026-11-10，+0.14%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.66%（2026-11-10，+0.13%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.25%（2026-11-10，-0.00%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.23%（2026-11-10，-0.00%）；日频，FRED/H.15国债恒定期限收益率。

## 已完成短券拍卖的组合读数
最新拍卖日的组合规模及发行额加权投标覆盖倍数高于上一记录，预计算压力读数较低。组合期限差异限制同口径需求比较。
TBILL_AUCTION_SIZE：277.00bn（2026-11-09，+52.00bn）；event-based。
TBILL_AUCTION_BTC：2.72ratio（2026-11-09，+0.15ratio）；event-based。
TBILL_AUCTION_STRESS：50.00index（2026-11-09，-15.00index）；事件驱动，财政部T-bill拍卖后公布。

## 信用与股市波动短线降温
投资级与高收益利差收窄，VIX回落，显示最近一期下游风险定价缓和。近月窗口三者仍净升。
BAMLC0A0CM：0.91%（2026-11-09，-0.02%）；daily T+1。
BAMLH0A0HYM2：3.34%（2026-11-09，-0.08%）；daily T+1。
VIXCLS：19.92index（2026-11-09，-5.72index）；daily T+1。
BAMLC0A0CM：0.91%（2026-11-09，+0.08%）；daily T+1。
BAMLH0A0HYM2：3.34%（2026-11-09，+0.23%）；daily T+1。
VIXCLS：19.92index（2026-11-09，+4.71index）；daily T+1。

## 逆回购存量缓冲偏薄
可释放的逆回购存量有限，叠加准备金五周净降，后续现金吸收更容易传至准备金。最新周度准备金反弹、EFFR持平，尚无稀缺确认。
RRP_BUFFER：0.15bn（2026-11-10，-0.10bn）；日频，纽约联储每日操作结果。
WRESBAL：2930.09bn（2026-11-04，+36.32bn）；weekly。
WRESBAL：2930.09bn（2026-11-04，-18.00bn）；weekly。
EFFR：3.88%（2026-11-09，+0.00%）；daily T+1。

## 公告结算的净现金影响待确认
满足条件时，结算可能增加融资压力。快照只列毛发行，到期抵扣和净现金影响仍未知。
event:gross_total_by_issue_date:2026-11-16：日期未知；状态 unknown；无可用数值。
event:gross_total_by_issue_date:2026-11-17：日期未知；状态 unknown；无可用数值。
TGA_FLOW：12.32bn（2026-11-09，+24.76bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
WRESBAL：2930.09bn（2026-11-04，+36.32bn）；weekly。
SOFR：3.88%（2026-11-09，-0.01%）；daily T+1。
SOFR_VOLUME：3100.00bn（2026-11-09，-74.00bn）；daily T+1。

## IORB日期越界且缺同日匹配
IORB选中行晚于快照日，相关预计算利差及价格乘规模代理缺可核验的同日锚。对当前回购溢价的判断因此受限。
IORB：3.90%（2026-11-12，+0.00%）；daily / policy step。
coverage:sofr_iorb_freshness：2026-11-09；状态 stale；无可用数值。
coverage:sofr_iorb_matching：2026-11-09；状态 incomplete_date_matched_history；无可用数值。
SOFR_VOLUME_IMPACT：-1.72mn/day（2026-11-09，-0.84mn/day）；日频，纽约联储SOFR记录随利率一同发布。

## 离岸与日元融资覆盖有限
美元指数仅为间接代理，商业票据观测陈旧，跨币种基差缺失。JGB最新值采用混合来源，已给美日长端利差只适用较早日期。
DTWEXBGS：121.88index（2026-11-06，+0.37index）；daily T+1。
quality:stale_metric:DCPN3M：2026-11-05；状态 stale；无可用数值。
JGB10：2.79原始比例/口径（2026-11-11，+0.02原始比例/口径）；按来源频率。
US_JP_10Y：212.30原始比例/口径（2026-10-30，+1.90原始比例/口径）；按来源频率。