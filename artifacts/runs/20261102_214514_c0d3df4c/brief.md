# 美元流动性分析
2026-11-02 21:46:48 UTC+08:00

中性偏紧
2026-11-02最新可得快照显示数量缓冲与回购融资偏紧，腹部贴现率回落提供抵消；观测日期不齐、离岸覆盖不足，尚无全面融资紧张的交叉确认。

## 美股与BTC中期投资研究
流动性对中期风险承担的贡献分化：上游现金与缓冲偏紧，融资相对价格承压，而月度实际贴现率下降形成支持；下游尚未一致确认。美股与BTC都不能据此推导确定回报，判断以条件路径为主。

相对上次：相对上次成功事实包，可比较的核心资金价格、数量缓冲、曲线、信用及金融条件均未实质变化；常备回购新增观测日期，使用量仍未变化。比较事实未覆盖本次股票与BTC价格，不能推断其相对上次包的变化，更不能臆测上次模型观点。

### 美股：分化（2—12周，中等置信度）
判断：真实贴现率月度下降有利于估值，但上游现金约束与较长窗口信用收紧抵消支持，美股流动性贡献分化。
传导：实际利率下降降低长久期现金流折现压力；TGA累计增加、准备金跨周下降与回购溢价扩大则约束融资风险承担。若利率下降源于增长恶化，估值支持可能被盈利压力抵消。
市场确认：标普月度上涨与纳斯达克综合月度下跌呈分化，近期信用及VIX修复没有延伸为一致的中期确认。股价只作下游证据，不能反推现金供给增加。
失效条件：若回购溢价持续回落、准备金连续跨周企稳且信用同步收窄，判断应转向支持；若实际收益率重新持续上行，同时信用走阔与主要股指共同走弱，则转向压制。
覆盖边界：缺增长和盈利修正，无法区分贴现率利好与增长冲击的全部贡献。股票、信用与上游观测日期不同，缺直接政策预期，不能给出完整股票回报结论。
事实引用：trend:TGA:20obs, trend:WRESBAL:5obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:DFII7:20obs, trend:DFII5:60obs, trend:BAMLH0A0HYM2:60obs, trend:BAMLH0A0HYM2:5obs, trend:VIXCLS:5obs, market:SP500:20obs, market:NASDAQCOM:20obs, coverage:growth_earnings, coverage:direct_expectations

### BTC：分化（2—12周，低置信度）
判断：美元实际贴现率下降提供潜在支持，但融资与现金缓冲偏紧；BTC近期与中段价格窗口偏弱，尚未确认流动性支持有效传导。
传导：真实无风险收益下降可能降低持有BTC的机会成本；美元融资溢价和缓冲消耗则可能限制风险承担。该宏观机制不能替代BTC自身资金流和合约杠杆分析。
市场确认：BTC最新价格回升，但近期及中段窗口仍下跌，较长窗口上涨，确认混合。没有ETF流、稳定币供给、合约仓位和资金费资料，不能声称新增资金入场或去杠杆完成；股票表现不作为BTC资金流证据。
失效条件：若美元融资溢价持续回落、准备金企稳且BTC近期和中段价格窗口同步转强，判断可转向支持；若融资溢价继续扩大并伴实际收益率持续反弹、BTC跨窗口走弱，则转向压制。
覆盖边界：BTC是含周末的日频口径，与美股交易观测窗口不可机械等同。缺现货资金流、稳定币及衍生杠杆，无法判断宏观支持是否抵消资产特定抛压。
事实引用：trend:DFII5:20obs, trend:DFII7:20obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:TGA:20obs, trend:WRESBAL:5obs, derived:RRP_BUFFER, market:CBBTCUSD:level, market:CBBTCUSD:5obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：近端名义收益率与FRBSF模型提供政策路径和期限风险补偿的间接观察；模型分解不是期货直接定价或调查共识。近期与月度模型变化不完全同向，且缺直接预期资料，无法判断充分定价或存在预期差。

### 基准情景
若融资压力仍集中于担保链条、实际贴现率改善延续而数量缓冲未修复，风险承担维持分化，美股与BTC需要各自价格及资金证据确认。
触发：无抵押融资继续稳定，回购溢价没有持续加速上行，实际收益率保持近期回落方向，同时准备金和TGA尚未形成明确反转。
失效：现金缓冲与融资价格同时持续改善，或融资压力扩散到无抵押及信用市场，均使分化基准失效。
事实引用：metric:EFFR, metric:OBFR, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:TGA:20obs, trend:WRESBAL:5obs, market:NASDAQCOM:20obs, market:CBBTCUSD:20obs

### 改善情景
若财政现金释放与准备金企稳共同降低融资约束，且贴现率下降没有伴随增长盈利恶化，流动性贡献可转为支持；BTC仍需独立资金流验证。
触发：TGA在后续连续观测中回落、准备金连续跨周企稳，回购相对政策锚溢价持续收窄；信用收窄与股指及BTC各自中段价格改善形成下游确认。
失效：TGA重新持续增加、准备金再度跨周下降或融资溢价重新扩大；即使利率下降，若盈利修正恶化也削弱股票改善路径。
事实引用：metric:TGA, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:DFII5, metric:BAMLH0A0HYM2, market:SP500:20obs, market:CBBTCUSD:20obs, coverage:growth_earnings, coverage:btc_flows_leverage

### 恶化情景
若净结算与财政现金增加进一步压缩缓冲，且融资溢价、真实贴现率及信用同时恶化，美元流动性对美股与BTC的贡献可能转为压制。
触发：公告结算获得净筹资增加的资料确认，TGA继续上升、准备金继续跨周下降，回购溢价持续扩大并扩散至无抵押融资或信用；同时实际收益率反弹及风险资产跨窗口转弱。
失效：结算后财政现金未持续增加、准备金企稳，融资溢价回落且信用稳定，便不足以维持收紧传导路径。
事实引用：calendar:7d, calendar:28d, metric:TGA, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:EFFR, metric:BAMLH0A0HYM2, metric:DFII5, market:NASDAQCOM:20obs, market:CBBTCUSD:20obs

### 下一轮核查
- 核查同日回购溢价、交易量及尾部分布的连续性，并观察无抵押融资和常备回购是否出现扩散确认。
- 补齐2026-11-05结算对应到期与净现金筹资，联查TGA及下一次准备金观测。
- 跟踪腹部实际收益率与信用是否同向改善，补充增长盈利资料以区分估值支持与增长冲击。
- 补齐BTC现货ETF流、稳定币供给、合约仓位和资金费，验证价格改善是否有资产自身证据。
- 更新离岸美元基差与同日美日利差，核验日债混合来源、直接预期及事实包捕获时间的一致性。

### 中期趋势（有效观测数，日频与周频分开）
- ICE BofA US Corporate OAS：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.0 %；状态 ok；trend:BAMLC0A0CM:5obs
- ICE BofA US Corporate OAS：20个有效日频观测间隔变化：2026-10-01 至 2026-10-29；20期；变化 0.030000000000000027 %；状态 ok；trend:BAMLC0A0CM:20obs
- ICE BofA US Corporate OAS：60个有效日频观测间隔变化：2026-08-06 至 2026-10-29；60期；变化 0.10999999999999999 %；状态 ok；trend:BAMLC0A0CM:60obs
- ICE BofA US High Yield OAS：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.14000000000000012 %；状态 ok；trend:BAMLH0A0HYM2:5obs
- ICE BofA US High Yield OAS：20个有效日频观测间隔变化：2026-10-01 至 2026-10-29；20期；变化 0.019999999999999574 %；状态 ok；trend:BAMLH0A0HYM2:20obs
- ICE BofA US High Yield OAS：60个有效日频观测间隔变化：2026-08-06 至 2026-10-29；60期；变化 0.5499999999999998 %；状态 ok；trend:BAMLH0A0HYM2:60obs
- Broad General Collateral Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:BGCR:5obs
- Broad General Collateral Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0900000000000003 %；状态 ok；trend:BGCR:20obs
- Broad General Collateral Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.30000000000000027 %；状态 ok；trend:BGCR:60obs
- 10-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.06000000000000005 %；状态 ok；trend:DFII10:5obs
- 10-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.2799999999999998 %；状态 ok；trend:DFII10:20obs
- 10-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.18999999999999995 %；状态 ok；trend:DFII10:60obs
- 5-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.08999999999999986 %；状态 ok；trend:DFII5:5obs
- 5-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.3999999999999999 %；状态 ok；trend:DFII5:20obs
- 5-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.10000000000000009 %；状态 ok；trend:DFII5:60obs
- 7-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.07000000000000028 %；状态 ok；trend:DFII7:5obs
- 7-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.33999999999999986 %；状态 ok；trend:DFII7:20obs
- 7-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.1499999999999999 %；状态 ok；trend:DFII7:60obs
- 1年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.08000000000000007 %；状态 ok；trend:DGS1:5obs
- 1年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.08000000000000007 %；状态 ok；trend:DGS1:20obs
- 1年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.33000000000000007 %；状态 ok；trend:DGS1:60obs
- 10年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.05999999999999961 %；状态 ok；trend:DGS10:5obs
- 10年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.2999999999999998 %；状态 ok；trend:DGS10:20obs
- 10年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.3100000000000005 %；状态 ok；trend:DGS10:60obs
- 2年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.13000000000000078 %；状态 ok；trend:DGS2:5obs
- 2年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.22000000000000064 %；状态 ok；trend:DGS2:20obs
- 2年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.3799999999999999 %；状态 ok；trend:DGS2:60obs
- 3年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.09999999999999964 %；状态 ok；trend:DGS3:5obs
- 3年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.2599999999999998 %；状态 ok；trend:DGS3:20obs
- 3年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.41000000000000014 %；状态 ok；trend:DGS3:60obs
- 5年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.11000000000000032 %；状态 ok；trend:DGS5:5obs
- 5年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.2999999999999998 %；状态 ok；trend:DGS5:20obs
- 5年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.3799999999999999 %；状态 ok；trend:DGS5:60obs
- 7年期国债收益率：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.08999999999999986 %；状态 ok；trend:DGS7:5obs
- 7年期国债收益率：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.3200000000000003 %；状态 ok；trend:DGS7:20obs
- 7年期国债收益率：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.33000000000000007 %；状态 ok；trend:DGS7:60obs
- Trade-weighted broad dollar index：5个有效日频观测间隔变化：2026-10-16 至 2026-10-23；5期；变化 -0.08459999999999468 index；状态 stale；trend:DTWEXBGS:5obs
- Trade-weighted broad dollar index：20个有效日频观测间隔变化：2026-09-24 至 2026-10-23；20期；变化 0.768100000000004 index；状态 stale；trend:DTWEXBGS:20obs
- Trade-weighted broad dollar index：60个有效日频观测间隔变化：2026-07-29 至 2026-10-23；60期；变化 0.5310000000000059 index；状态 stale；trend:DTWEXBGS:60obs
- Effective Federal Funds Rate：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.0 %；状态 ok；trend:EFFR:5obs
- Effective Federal Funds Rate：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 0.0 %；状态 ok；trend:EFFR:20obs
- Effective Federal Funds Rate：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.25 %；状态 ok；trend:EFFR:60obs
- FRBSF average expected overnight rate over next 10 years：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -0.01563099999999995 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:5obs
- FRBSF average expected overnight rate over next 10 years：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.1540569999999999 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:20obs
- FRBSF average expected overnight rate over next 10 years：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.26250600000000013 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:60obs
- FRBSF average expected overnight rate over next 2 years：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.01269000000000009 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:5obs
- FRBSF average expected overnight rate over next 2 years：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.17328600000000005 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:20obs
- FRBSF average expected overnight rate over next 2 years：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.4771860000000001 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:60obs
- FRBSF 10-year Treasury term premium：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.03983099999999995 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:5obs
- FRBSF 10-year Treasury term premium：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -0.15684300000000007 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:20obs
- FRBSF 10-year Treasury term premium：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 -0.00020599999999992846 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:60obs
- Interest on Reserve Balances：5个有效日频观测间隔变化：2026-10-28 至 2026-11-02；5期；变化 0.0 %；状态 ok；trend:IORB:5obs
- Interest on Reserve Balances：20个有效日频观测间隔变化：2026-10-13 至 2026-11-02；20期；变化 0.0 %；状态 ok；trend:IORB:20obs
- Interest on Reserve Balances：60个有效日频观测间隔变化：2026-09-03 至 2026-11-02；60期；变化 0.25 %；状态 ok；trend:IORB:60obs
- Chicago Fed National Financial Conditions Index：5个有效周频观测间隔变化：2026-09-18 至 2026-10-23；5期；变化 0.041000000000000036 index；状态 ok；trend:NFCI:5obs
- Chicago Fed National Financial Conditions Index：20个有效周频观测间隔变化：2026-06-05 至 2026-10-23；20期；变化 0.02200000000000002 index；状态 ok；trend:NFCI:20obs
- Chicago Fed National Financial Conditions Index：60个有效周频观测间隔变化：2025-08-29 至 2026-10-23；60期；变化 0.040000000000000036 index；状态 ok；trend:NFCI:60obs
- Overnight Bank Funding Rate：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.0 %；状态 ok；trend:OBFR:5obs
- Overnight Bank Funding Rate：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 0.0 %；状态 ok；trend:OBFR:20obs
- Overnight Bank Funding Rate：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.25 %；状态 ok；trend:OBFR:60obs
- Overnight Reverse Repo accepted amount：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 4.175 USD bn；状态 ok；trend:RRPONTSYD:5obs
- Overnight Reverse Repo accepted amount：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 4.025 USD bn；状态 ok；trend:RRPONTSYD:20obs
- Overnight Reverse Repo accepted amount：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 2.725 USD bn；状态 ok；trend:RRPONTSYD:60obs
- Secured Overnight Financing Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:SOFR:5obs
- Secured Overnight Financing Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.08000000000000007 %；状态 ok；trend:SOFR:20obs
- Secured Overnight Financing Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.31000000000000005 %；状态 ok；trend:SOFR:60obs
- SOFR transaction volume：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 110.0 USD bn；状态 ok；trend:SOFR_VOLUME:5obs
- SOFR transaction volume：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 108.0 USD bn；状态 ok；trend:SOFR_VOLUME:20obs
- SOFR transaction volume：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 186.0 USD bn；状态 ok；trend:SOFR_VOLUME:60obs
- SOMA holdings / QT background：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -9.215094331399087 USD bn；状态 ok；trend:SOMA:5obs
- SOMA holdings / QT background：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 14.961344576400734 USD bn；状态 ok；trend:SOMA:20obs
- SOMA holdings / QT background：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 160.9273346189011 USD bn；状态 ok；trend:SOMA:60obs
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.005 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 0.0 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.0 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
- Treasury General Account closing balance：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 78.47700000000009 USD bn；状态 ok；trend:TGA:5obs
- Treasury General Account closing balance：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 56.190000000000055 USD bn；状态 ok；trend:TGA:20obs
- Treasury General Account closing balance：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 116.01700000000005 USD bn；状态 ok；trend:TGA:60obs
- Tri-party General Collateral Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:TGCR:5obs
- Tri-party General Collateral Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0900000000000003 %；状态 ok；trend:TGCR:20obs
- Tri-party General Collateral Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.30000000000000027 %；状态 ok；trend:TGCR:60obs
- CBOE Volatility Index: VIX：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 -1.8300000000000018 index；状态 ok；trend:VIXCLS:5obs
- CBOE Volatility Index: VIX：20个有效日频观测间隔变化：2026-10-01 至 2026-10-29；20期；变化 0.8099999999999987 index；状态 ok；trend:VIXCLS:20obs
- CBOE Volatility Index: VIX：60个有效日频观测间隔变化：2026-08-06 至 2026-10-29；60期；变化 2.049999999999999 index；状态 ok；trend:VIXCLS:60obs
- Reserve balances with Federal Reserve Banks：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -36.42300000000023 USD bn；状态 ok；trend:WRESBAL:5obs
- Reserve balances with Federal Reserve Banks：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 -186.95299999999997 USD bn；状态 ok；trend:WRESBAL:20obs
- Reserve balances with Federal Reserve Banks：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 -287.93100000000004 USD bn；状态 ok；trend:WRESBAL:60obs
- 同日SOFR减IORB：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 3.000000000000025 bp；状态 ok；trend:SOFR_IORB:5obs
- 同日SOFR减IORB：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 8.000000000000007 bp；状态 ok；trend:SOFR_IORB:20obs
- 同日SOFR减IORB：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 6.000000000000005 bp；状态 ok；trend:SOFR_IORB:60obs

### 已公告结算日历（毛额，不等于净融资）
- {"fact_id": "calendar:7d", "id": "ANNOUNCED_SETTLEMENTS_7D", "name": "未来7日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-02", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 7, "window_start": "2026-11-02", "window_end": "2026-11-08", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:28d", "id": "ANNOUNCED_SETTLEMENTS_28D", "name": "未来28日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-02", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 28, "window_start": "2026-11-02", "window_end": "2026-11-29", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:84d", "id": "ANNOUNCED_SETTLEMENTS_84D", "name": "未来84日已公告结算毛发行（含快照日）", "value": 277.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-02", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 84, "window_start": "2026-11-02", "window_end": "2027-01-24", "event_count": 3, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 277.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-02:Bill:13-Week:912797VV6", "event:auction:2026-11-02:Bill:26-Week:912797WX1", "event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}

### 判断验证记录
这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，从其日期往后两日开始寻找首个有效收盘作为观察起点；评估只使用截至评估时刻UTC日期往前两日的价格。美股按10／20／60个后续有效收盘观察（约2／4／12周），BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。同一快照与方法版本仅首次发布算一个样本。去重后的持有窗口仍可能重叠，不能当作统计独立样本；历史价格截断或起点缺价时不把观察起点向后漂移。收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。所有已成熟样本均保留；分组不足十个样本时明确标为积累中，样本充足时仍只提供描述统计，预测能力需要另行样本外检验。
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-31", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}

## 担保融资价格与规模同步上行
回购相对政策锚的溢价扩大，成交规模增加，一般抵押品利率同向上升；无抵押利率保持稳定。价格乘规模代理上行，但不代表实际总融资成本。
SOFR_ANCHOR：5.00bp（2026-10-30，+1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：4.41mn/day（2026-10-30，+0.92mn/day）；日频，纽约联储SOFR记录随利率一同发布。
TGCR：3.93%（2026-10-30，+0.01%）；daily T+1。
BGCR：3.93%（2026-10-30，+0.01%）；daily T+1。
EFFR：3.88%（2026-10-29，+0.00%）；daily T+1。
OBFR：3.88%（2026-10-29，+0.00%）；daily T+1。

## 财政现金与准备金边际方向偏紧
TGA最新增加，RRP最新回升，准备金与SOMA最新周度下降。这些变化分属不同观测日期，不能直接拼接成同日准备金变动的会计解释。
TGA_FLOW：24.60bn（2026-10-29，+61.50bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
RRP_FLOW：4.02bn（2026-10-30，环比未知）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
SOMA：6355.84bn（2026-10-28，-8.00bn）；weekly。

## 名义腹部与实际收益率共同回落
近端与腹部名义收益率最新均下降，腹部实际收益率和通胀补偿同步回落，真实贴现率约束有所缓解；通胀补偿包含风险溢价与TIPS流动性成分。
DGS1：4.36%（2026-10-30，-0.06%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.65%（2026-10-30，-0.08%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.71%（2026-10-30，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.80%（2026-10-30，-0.07%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.25%（2026-10-30，-0.06%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.42%（2026-10-30，-0.04%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.46%（2026-10-30，-0.01%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.38%（2026-10-30，-0.03%）；日频，FRED/H.15国债恒定期限收益率。

## 下游最新转弱与近期修复并存
信用利差和VIX最新回升，但近期窗口高收益利差与VIX仍下降；NFCI边际收紧而水平仍偏松，传导尚不一致。
BAMLC0A0CM：0.89%（2026-10-29，+0.03%）；daily T+1。
BAMLH0A0HYM2：3.26%（2026-10-29，+0.12%）；daily T+1。
VIXCLS：17.20index（2026-10-29，+0.29index）；daily T+1。
BAMLH0A0HYM2：3.26%（2026-10-29，-0.14%）；daily T+1。
VIXCLS：17.20index（2026-10-29，-1.83index）；daily T+1。
NFCI：-0.49index（2026-10-23，+0.01index）；weekly。

## 日元仓位变化由多头增仓主导
CFTC周度多头增加、空头减少，净头寸为净多，不能称为空头主导的carry扩张。另一个观测时点的美元兑日元小幅上行、实现波动回落，尚未显示汇率急变触发的平仓链条。
jpy:CFTC_DECOMPOSITION：日期未知；状态 unknown；无可用数值。
CFTC_JPY_GROSS_LONG：225516.00原始比例/口径（2026-10-27，+25330.00原始比例/口径）；按来源频率。
CFTC_JPY_GROSS_SHORT：123925.00原始比例/口径（2026-10-27，-6383.00原始比例/口径）；按来源频率。
CFTC_JPY_NET_OI：0.27原始比例/口径（2026-10-27，+0.09原始比例/口径）；按来源频率。
USDJPY：157.83原始比例/口径（2026-10-29，+0.04原始比例/口径）；按来源频率。
USDJPY_VOL20：5.08原始比例/口径（2026-10-29，-0.13原始比例/口径）；按来源频率。

## 薄缓冲提高后续冲击敏感度
RRP可继续释放的存量缓冲有限，准备金跨周下降与财政现金累计增加使后续冲击更容易传向银行体系；银行间价格稳定仍是重要反向证据，不能判定准备金已稀缺。
RRP_BUFFER：4.38bn（2026-10-30，+4.02bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-36.42bn）；weekly。
TGA：1040.24bn（2026-10-29，+56.19bn）；daily T+1。
EFFR：3.88%（2026-10-29，+0.00%）；daily T+1。

## 结算压力须等待净额与融资确认
满足条件时，财政结算可能放大薄缓冲下的融资压力。现有公告只覆盖已捕获毛发行，到期、净融资及准备金影响仍未知，不能认定已发生抽水。
ANNOUNCED_SETTLEMENTS_7D：277.00bn（2026-11-02，环比未知）；announced event schedule。
event:gross_total_by_issue_date:2026-11-05：日期未知；状态 unknown；无可用数值。
TGA：1040.24bn（2026-10-29，+24.60bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
SOFR_ANCHOR：5.00bp（2026-10-30，+1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。

## 离岸与日元利差证据不完整
商业票据和广义美元已陈旧，美日长端利差停留在较早日期，日债采用官方历史与商业最新补点混合来源；缺少真实跨币种融资基差。不能将这些缺口视为当前市场平稳。
quality:stale_metric:DCPN3M：2026-10-13；状态 stale；无可用数值。
quality:stale_metric:DTWEXBGS：2026-10-23；状态 stale；无可用数值。
US_JP_10Y：223.30原始比例/口径（2026-09-30，+5.50原始比例/口径）；按来源频率。
JGB10：2.77原始比例/口径（2026-11-02，-0.01原始比例/口径）；按来源频率。

## 投资归因与快照时点存在覆盖限制
直接政策预期、增长盈利、BTC现货资金流和衍生杠杆尚未配置，历史序列未验证当时可见版本。市场事实捕获时间晚于包头生成时间，也限制精确时点审计；不能据此声称预期差、资金入场或预测优势。
coverage:direct_expectations：2026-11-02；状态 missing；无可用数值。
coverage:btc_flows_leverage：2026-11-02；状态 missing；无可用数值。
coverage:growth_earnings：2026-11-02；状态 missing；无可用数值。
coverage:historical_vintages：2026-11-02；状态 prospective_capture_only；无可用数值。
CBBTCUSD：78110.97USD（2026-11-01，+707.05USD）；daily / 7-day observations。