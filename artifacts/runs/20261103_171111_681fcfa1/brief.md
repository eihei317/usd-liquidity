# 美元流动性分析
2026-11-03 17:00:59 UTC+08:00

中性偏紧
2026-11-03最新可得快照显示回购融资偏紧、数量缓冲偏薄及信用边际恶化；财政现金释放与近期折现率下降构成抵消，但融资、周频和缓存市场数据日期不齐，尚不足确认全面紧张。

## 美股与BTC中期投资研究
美元流动性对中期风险承担的贡献偏受限：上游缓冲偏薄、担保融资相对政策锚变贵，下游信用风险补偿走阔；近期腹部实际收益率下降提供估值支持，财政现金释放也构成抵消。因此美股呈机制分化，BTC美元背景偏压制但资产确认不足。流动性贡献不等于预期收益或综合评级。

相对上次：comparison_facts列示的融资、数量、折现率和信用事实均未较比较包变化，不能报告新增转向。比较包生成时间与本包相同，只能理解为本次比较基准未显示实质更新，不能据此声称跨日趋势稳定或沿用上次模型观点。依据包括comparison:SOFR、comparison:SOFR_VOLUME、comparison:TGA、comparison:WRESBAL、comparison:DFII5及comparison:BAMLH0A0HYM2。

### 美股：分化（2—12周，中等置信度）
判断：近期实际贴现率下降有利于估值，但融资约束、数量缓冲与信用走弱抵消支持；较长窗口实际收益率仍高于起点，尚不支持全面流动性利好判断。
传导：上游现金与缓冲影响风险承载能力，担保融资影响持仓成本，实际收益率通过折现率影响估值。利率下降若伴随增长恶化，估值支持可能被盈利压力抵消；增长与盈利缺失，不能形成完整股票回报结论。
市场确认：信用利差及较长窗口隐含波动确认边际风险偏好转弱。股票缓存窗口也偏弱，但不能作为当前价格确认；尚缺新鲜股票行情、盈利修正和增长数据。
失效条件：若准备金转为持续恢复、担保融资相对政策锚溢价收敛、信用利差持续回落且实际收益率继续下降，分化判断应向支持调整；若实际收益率持续回升并伴随信用扩大和准备金下降，应向压制调整。
覆盖边界：价格数据为离线缓存；缺增长、盈利和直接预期。窗口起止日及频率不完全一致，近期与较长窗口提供期限对照，不是额外独立投票。
事实引用：trend:DFII5:20obs, trend:DFII7:20obs, trend:DFII5:60obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:WRESBAL:5obs, derived:RRP_BUFFER, trend:BAMLH0A0HYM2:20obs, trend:VIXCLS:20obs, market:SP500:20obs, market:NASDAQCOM:20obs, coverage:market:SP500, coverage:market:NASDAQCOM, coverage:growth_earnings

### BTC：压制（2—12周，低置信度）
判断：美元融资与缓冲环境对BTC风险承担偏压制，近期实际收益率下降构成反向支持；缺乏资产资金流和杠杆确认，不能将此判断转换成价格预测。
传导：美元担保融资变贵和现金缓冲偏薄可能限制跨资产风险承载；实际贴现率下降可能降低持有非生息风险资产的机会成本。该机制不能证明BTC现货资金流入或特定杠杆仓位变化。
市场确认：BTC缓存中的近期及较长价格窗口偏弱，仅为截至各自观测日期的背景，不能代表当前价格确认。未覆盖ETF资金流、稳定币供给、合约仓位及资金费率，无法确认新增资金入场或杠杆去化完成。
失效条件：若美元融资溢价持续收敛、准备金恢复，并由新鲜BTC现货价格和实际现货资金流共同确认改善，压制判断应撤销；若仅价格反弹而融资继续收紧，尚不足推翻。若实际收益率持续回升且BTC资金流转弱，将强化压制判断。
覆盖边界：BTC每日观测包含周末，与美股交易日窗口不同；资产价格为离线缓存，资金流及衍生杠杆缺失，美股表现不能替代BTC确认。
事实引用：trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:WRESBAL:5obs, derived:RRP_BUFFER, trend:DFII5:20obs, trend:DFII7:20obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:market:CBBTCUSD, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：名义收益率及FRBSF模型分解覆盖部分政策路径和期限风险补偿代理。模型估计不等于期货直接定价或调查共识；缺乏直接预期和事件预期差，已计价程度及是否存在预期差保持未知。

### 基准情景
若融资约束局限于担保链条、财政现金释放与折现率支持延续，风险资产流动性环境维持受限且分化，美股估值支持难完全抵消信用约束，BTC资产确认继续不足。
触发：无抵押银行融资继续稳定，担保融资溢价未持续恶化，实际收益率维持近期改善方向，同时准备金与信用未出现进一步持续恶化。
失效：融资溢价、准备金和信用共同持续改善，或同步持续恶化，将分别使基准路径转向改善或收紧情景。
事实引用：metric:EFFR, metric:OBFR, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, derived:TGA_FLOW, trend:DFII5:20obs, trend:WRESBAL:5obs, trend:BAMLH0A0HYM2:20obs, coverage:btc_flows_leverage

### 改善情景
若上游现金承载能力与融资价格同步改善，且实际贴现率继续下降、信用风险补偿收敛，流动性对美股和BTC的贡献转向支持；BTC仍需独立资金流确认。
触发：准备金连续恢复，担保融资相对政策锚溢价持续收敛，腹部实际收益率下降，同时信用利差回落；新鲜资产价格与BTC现货资金流进一步确认。
失效：准备金再度持续下降或融资溢价重新走阔，且信用未改善；仅缓存价格反弹不满足触发条件。
事实引用：trend:WRESBAL:5obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:DFII7:20obs, trend:BAMLH0A0HYM2:20obs, coverage:market:SP500, coverage:market:CBBTCUSD, coverage:btc_flows_leverage

### 恶化情景
若实际净现金吸收与融资溢价扩大共同出现，低缓冲可能放大准备金下降及信用收紧；若再叠加实际收益率上升或日元快速升值，风险资产承载能力可能进一步下降。
触发：结算到期净额确认财政现金吸收，TGA持续回升、准备金继续下降，担保融资溢价与信用利差同步走阔；实际收益率持续上行或日元升值且波动放大构成进一步确认。
失效：净现金吸收未获确认，或财政释放、准备金恢复和融资溢价收敛抵消供给影响；信用与实际收益率改善也会削弱该路径。
事实引用：calendar:7d, event:gross_total_by_issue_date:2026-11-05, metric:TGA, metric:WRESBAL, derived:RRP_BUFFER, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, metric:BAMLH0A0HYM2, metric:DFII5, metric:DFII7, jpy:USDJPY, jpy:USDJPY_VOL20

### 下一轮核查
- 更新核心担保和无抵押融资价格、交易量及尾部，核查相对政策锚溢价是否持续扩大或收敛。
- 补齐财政结算与到期净额，并结合后续TGA、准备金及逆回购流量确认现金吸收方向。
- 核查腹部实际收益率回升是否延续，以及信用利差是否停止走阔；同时补充增长盈利和直接市场预期。
- 恢复新鲜美股及BTC行情，并补充BTC现货资金流、稳定币、合约仓位和资金费率。
- 补齐同日期美日利差、可靠日债历史与离岸融资基差，核查日元汇率波动是否与仓位变化共同确认套利反转。

### 中期趋势（有效观测数，日频与周频分开）
- ICE BofA US Corporate OAS：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.029999999999999916 %；状态 ok；trend:BAMLC0A0CM:5obs
- ICE BofA US Corporate OAS：20个有效日频观测间隔变化：2026-10-02 至 2026-10-30；20期；变化 0.08999999999999997 %；状态 ok；trend:BAMLC0A0CM:20obs
- ICE BofA US Corporate OAS：60个有效日频观测间隔变化：2026-08-07 至 2026-10-30；60期；变化 0.15999999999999992 %；状态 ok；trend:BAMLC0A0CM:60obs
- ICE BofA US High Yield OAS：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.06000000000000005 %；状态 ok；trend:BAMLH0A0HYM2:5obs
- ICE BofA US High Yield OAS：20个有效日频观测间隔变化：2026-10-02 至 2026-10-30；20期；变化 0.33999999999999986 %；状态 ok；trend:BAMLH0A0HYM2:20obs
- ICE BofA US High Yield OAS：60个有效日频观测间隔变化：2026-08-07 至 2026-10-30；60期；变化 0.7399999999999998 %；状态 ok；trend:BAMLH0A0HYM2:60obs
- Broad General Collateral Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:BGCR:5obs
- Broad General Collateral Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0900000000000003 %；状态 ok；trend:BGCR:20obs
- Broad General Collateral Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.30000000000000027 %；状态 ok；trend:BGCR:60obs
- 10-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.040000000000000036 %；状态 ok；trend:DFII10:5obs
- 10-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.2999999999999998 %；状态 ok；trend:DFII10:20obs
- 10-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.18999999999999995 %；状态 ok；trend:DFII10:60obs
- 5-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.06000000000000005 %；状态 ok；trend:DFII5:5obs
- 5-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.3799999999999999 %；状态 ok；trend:DFII5:20obs
- 5-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.14000000000000012 %；状态 ok；trend:DFII5:60obs
- 7-year Treasury inflation-indexed security real yield：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.05999999999999961 %；状态 ok；trend:DFII7:5obs
- 7-year Treasury inflation-indexed security real yield：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.34999999999999964 %；状态 ok；trend:DFII7:20obs
- 7-year Treasury inflation-indexed security real yield：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.16000000000000014 %；状态 ok；trend:DFII7:60obs
- 1年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.08999999999999986 %；状态 ok；trend:DGS1:5obs
- 1年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.08000000000000007 %；状态 ok；trend:DGS1:20obs
- 1年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.3200000000000003 %；状态 ok；trend:DGS1:60obs
- 10年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.08999999999999986 %；状态 ok；trend:DGS10:5obs
- 10年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.3700000000000001 %；状态 ok；trend:DGS10:20obs
- 10年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.21999999999999975 %；状态 ok；trend:DGS10:60obs
- 2年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.08999999999999986 %；状态 ok；trend:DGS2:5obs
- 2年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.2400000000000002 %；状态 ok；trend:DGS2:20obs
- 2年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.33999999999999986 %；状态 ok；trend:DGS2:60obs
- 3年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.13999999999999968 %；状态 ok；trend:DGS3:5obs
- 3年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.3099999999999996 %；状态 ok；trend:DGS3:20obs
- 3年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.34000000000000075 %；状态 ok；trend:DGS3:60obs
- 5年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.13999999999999968 %；状态 ok；trend:DGS5:5obs
- 5年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.35999999999999943 %；状态 ok；trend:DGS5:20obs
- 5年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.2999999999999998 %；状态 ok；trend:DGS5:60obs
- 7年期国债收益率：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.1200000000000001 %；状态 ok；trend:DGS7:5obs
- 7年期国债收益率：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 -0.3799999999999999 %；状态 ok；trend:DGS7:20obs
- 7年期国债收益率：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.2599999999999998 %；状态 ok；trend:DGS7:60obs
- Trade-weighted broad dollar index：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.34539999999999793 index；状态 ok；trend:DTWEXBGS:5obs
- Trade-weighted broad dollar index：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.1226000000000056 index；状态 ok；trend:DTWEXBGS:20obs
- Trade-weighted broad dollar index：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 2.2775000000000034 index；状态 ok；trend:DTWEXBGS:60obs
- Effective Federal Funds Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.0 %；状态 ok；trend:EFFR:5obs
- Effective Federal Funds Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0 %；状态 ok；trend:EFFR:20obs
- Effective Federal Funds Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.25 %；状态 ok；trend:EFFR:60obs
- FRBSF average expected overnight rate over next 10 years：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.060861000000000054 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:5obs
- FRBSF average expected overnight rate over next 10 years：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.1323000000000003 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:20obs
- FRBSF average expected overnight rate over next 10 years：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.23364699999999994 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_10Y:60obs
- FRBSF average expected overnight rate over next 2 years：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.07794699999999999 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:5obs
- FRBSF average expected overnight rate over next 2 years：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.1341619999999999 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:20obs
- FRBSF average expected overnight rate over next 2 years：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.4229510000000003 %；状态 ok；trend:FRBSF_EXPECTED_SHORT_2Y:60obs
- FRBSF 10-year Treasury term premium：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.0017610000000001236 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:5obs
- FRBSF 10-year Treasury term premium：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 -0.1762999999999999 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:20obs
- FRBSF 10-year Treasury term premium：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 -0.010246999999999895 %；状态 ok；trend:FRBSF_TERM_PREMIUM_10Y:60obs
- Interest on Reserve Balances：5个有效日频观测间隔变化：2026-10-29 至 2026-11-03；5期；变化 0.0 %；状态 ok；trend:IORB:5obs
- Interest on Reserve Balances：20个有效日频观测间隔变化：2026-10-14 至 2026-11-03；20期；变化 0.0 %；状态 ok；trend:IORB:20obs
- Interest on Reserve Balances：60个有效日频观测间隔变化：2026-09-04 至 2026-11-03；60期；变化 0.25 %；状态 ok；trend:IORB:60obs
- Chicago Fed National Financial Conditions Index：5个有效周频观测间隔变化：2026-09-18 至 2026-10-23；5期；变化 0.041000000000000036 index；状态 ok；trend:NFCI:5obs
- Chicago Fed National Financial Conditions Index：20个有效周频观测间隔变化：2026-06-05 至 2026-10-23；20期；变化 0.02200000000000002 index；状态 ok；trend:NFCI:20obs
- Chicago Fed National Financial Conditions Index：60个有效周频观测间隔变化：2025-08-29 至 2026-10-23；60期；变化 0.040000000000000036 index；状态 ok；trend:NFCI:60obs
- Overnight Bank Funding Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.0 %；状态 ok；trend:OBFR:5obs
- Overnight Bank Funding Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0 %；状态 ok；trend:OBFR:20obs
- Overnight Bank Funding Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.25 %；状态 ok；trend:OBFR:60obs
- Overnight Reverse Repo accepted amount：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 4.887 USD bn；状态 ok；trend:RRPONTSYD:5obs
- Overnight Reverse Repo accepted amount：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 3.586 USD bn；状态 ok；trend:RRPONTSYD:20obs
- Overnight Reverse Repo accepted amount：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 3.6579999999999995 USD bn；状态 ok；trend:RRPONTSYD:60obs
- Secured Overnight Financing Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:SOFR:5obs
- Secured Overnight Financing Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.08000000000000007 %；状态 ok；trend:SOFR:20obs
- Secured Overnight Financing Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.31000000000000005 %；状态 ok；trend:SOFR:60obs
- SOFR transaction volume：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 110.0 USD bn；状态 ok；trend:SOFR_VOLUME:5obs
- SOFR transaction volume：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 108.0 USD bn；状态 ok；trend:SOFR_VOLUME:20obs
- SOFR transaction volume：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 186.0 USD bn；状态 ok；trend:SOFR_VOLUME:60obs
- SOMA holdings / QT background：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -9.215094331399087 USD bn；状态 ok；trend:SOMA:5obs
- SOMA holdings / QT background：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 14.961344576400734 USD bn；状态 ok；trend:SOMA:20obs
- SOMA holdings / QT background：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 160.9273346189011 USD bn；状态 ok；trend:SOMA:60obs
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-10-26 至 2026-11-02；5期；变化 -0.003 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-10-02 至 2026-11-02；20期；变化 0.002 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-06 至 2026-11-02；60期；变化 0.002 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
- Treasury General Account closing balance：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -30.896000000000072 USD bn；状态 ok；trend:TGA:5obs
- Treasury General Account closing balance：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 57.894000000000005 USD bn；状态 ok；trend:TGA:20obs
- Treasury General Account closing balance：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 22.267999999999915 USD bn；状态 ok；trend:TGA:60obs
- Tri-party General Collateral Rate：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.03000000000000025 %；状态 ok；trend:TGCR:5obs
- Tri-party General Collateral Rate：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0900000000000003 %；状态 ok；trend:TGCR:20obs
- Tri-party General Collateral Rate：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 0.30000000000000027 %；状态 ok；trend:TGCR:60obs
- CBOE Volatility Index: VIX：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 -0.029999999999997584 index；状态 ok；trend:VIXCLS:5obs
- CBOE Volatility Index: VIX：20个有效日频观测间隔变化：2026-10-02 至 2026-10-30；20期；变化 4.110000000000001 index；状态 ok；trend:VIXCLS:20obs
- CBOE Volatility Index: VIX：60个有效日频观测间隔变化：2026-08-07 至 2026-10-30；60期；变化 4.520000000000001 index；状态 ok；trend:VIXCLS:60obs
- Reserve balances with Federal Reserve Banks：5个有效周频观测间隔变化：2026-09-23 至 2026-10-28；5期；变化 -36.42300000000023 USD bn；状态 ok；trend:WRESBAL:5obs
- Reserve balances with Federal Reserve Banks：20个有效周频观测间隔变化：2026-06-10 至 2026-10-28；20期；变化 -186.95299999999997 USD bn；状态 ok；trend:WRESBAL:20obs
- Reserve balances with Federal Reserve Banks：60个有效周频观测间隔变化：2025-09-03 至 2026-10-28；60期；变化 -287.93100000000004 USD bn；状态 ok；trend:WRESBAL:60obs
- 同日SOFR减IORB：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 3.000000000000025 bp；状态 ok；trend:SOFR_IORB:5obs
- 同日SOFR减IORB：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 8.000000000000007 bp；状态 ok；trend:SOFR_IORB:20obs
- 同日SOFR减IORB：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 6.000000000000005 bp；状态 ok；trend:SOFR_IORB:60obs

### 已公告结算日历（毛额，不等于净融资）
- {"fact_id": "calendar:7d", "id": "ANNOUNCED_SETTLEMENTS_7D", "name": "未来7日已公告结算毛发行（含快照日）", "value": 100.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-03", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 7, "window_start": "2026-11-03", "window_end": "2026-11-09", "event_count": 1, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 100.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:28d", "id": "ANNOUNCED_SETTLEMENTS_28D", "name": "未来28日已公告结算毛发行（含快照日）", "value": 100.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-03", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 28, "window_start": "2026-11-03", "window_end": "2026-11-30", "event_count": 1, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 100.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}
- {"fact_id": "calendar:84d", "id": "ANNOUNCED_SETTLEMENTS_84D", "name": "未来84日已公告结算毛发行（含快照日）", "value": 100.0, "previous": null, "change": null, "unit": "USD bn", "as_of": "2026-11-03", "frequency": "announced event schedule", "source": "TreasuryDirect", "source_url": "https://www.treasurydirect.gov/TA_WS/securities/announced?format=json", "status": "partial_announced", "window_days": 84, "window_start": "2026-11-03", "window_end": "2027-01-25", "event_count": 1, "unknown_amount_count": 0, "gross_announced_offering_usd_bn": 100.0, "gross_amounts_complete_for_listed_events": true, "maturities_usd_bn": null, "net_cash_impact_usd_bn": null, "reserve_impact": "unknown_without_funding_and_fed_balance_sheet_confirmation", "base_fact_ids": ["event:auction:2026-11-03:Bill:6-Week:912797VH7"], "role": "announced_future_supply", "coverage_note": "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知，不按毛发行推算。"}

### 判断验证记录
这是判断发布后的价格观察记录，不是交易策略收益或实际成交记录。原始日价缺少精确发布时间，采用保守规则：实际发布时间转为UTC后，从其日期往后两日开始寻找首个有效收盘作为观察起点；评估只使用截至评估时刻UTC日期往前两日的价格。美股按10／20／60个后续有效收盘观察（约2／4／12周），BTC按14／28／84个自然日观察，缺少窗口内日价则保持缺失。同一快照与方法版本仅首次发布算一个样本。去重后的持有窗口仍可能重叠，不能当作统计独立样本；历史价格截断或起点缺价时不把观察起点向后漂移。收益基线是同一资产、同一窗口的持有价格变化，未扣费用且不含股息，不能用它宣称择时超额收益。流动性支持或压制也不等于买卖指令。所有已成熟样本均保留；分组不足十个样本时明确标为积累中，样本充足时仍只提供描述统计，预测能力需要另行样本外检验。
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_134511_54c320d4", "published_at_bjt": "2026-10-30T13:49:14.541966+08:00", "source_generated_at_bjt": "2026-10-30T13:45:58+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141037_52daa842", "published_at_bjt": "2026-10-30T14:17:33.874655+08:00", "source_generated_at_bjt": "2026-10-30T14:13:31+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "missing_price", "status_note": "观察起点已到，价格源没有发布后的有效价格。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-15"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2026-11-29"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": "2026-11-01", "entry_price": 78110.97, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01", "target_exit_date": "2027-01-24"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_212318_976012ed", "published_at_bjt": "2026-11-02T21:36:01.457470+08:00", "source_generated_at_bjt": "2026-11-02T21:31:13+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261102_214514_c0d3df4c", "published_at_bjt": "2026-11-02T21:50:22.686384+08:00", "source_generated_at_bjt": "2026-11-02T21:46:48+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-04"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}
- {"run_id": "20261103_171111_681fcfa1", "published_at_bjt": "2026-11-03T17:14:02.615698+08:00", "source_generated_at_bjt": "2026-11-03T17:00:59+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "压制", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-11-01", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-05"}

## 担保融资走高，无抵押融资稳定
回购相对政策锚溢价与交易规模同时上升，价格乘规模代理随之增加；无抵押融资持平，融资压力尚未全面扩散。
SOFR_ANCHOR：5.00bp（2026-10-30，+1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：4.41mn/day（2026-10-30，+0.92mn/day）；日频，纽约联储SOFR记录随利率一同发布。
EFFR：3.88%（2026-10-30，+0.00%）；daily T+1。
OBFR：3.88%（2026-10-30，+0.00%）；daily T+1。
TGCR：3.93%（2026-10-30，+0.01%）；daily T+1。
BGCR：3.93%（2026-10-30，+0.01%）；daily T+1。

## 财政释放与缓冲偏薄并存
TGA最新下降，逆回购边际增加但存量仍薄；准备金与SOMA最近周度下降。不同日期的现金释放与准备金变化可以并存，不能直接作会计归因。
TGA_FLOW：-88.64bn（2026-10-30，-113.25bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
RRP_FLOW：0.71bn（2026-11-02，环比未知）；日频，纽约联储每日操作结果。
RRP_BUFFER：5.09bn（2026-11-02，+0.71bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
SOMA：6355.84bn（2026-10-28，-8.00bn）；weekly。

## 名义腹部略降，实际贴现率回升
近端名义收益率上行、中段持平、腹部略降；腹部实际收益率上行而通胀补偿下降，名义变化没有同步转化为真实贴现率改善。
DGS1：4.38%（2026-11-02，+0.02%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.65%（2026-11-02，+0.00%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.70%（2026-11-02，-0.01%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.79%（2026-11-02，-0.01%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.31%（2026-11-02，+0.06%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.45%（2026-11-02，+0.03%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.39%（2026-11-02，-0.07%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.34%（2026-11-02，-0.04%）；日频，FRED/H.15国债恒定期限收益率。

## 短债拍卖须按组合评估
最新完成短债拍卖同时提供规模、加权认购覆盖和预计算压力代理。当前与上一场期限组合可比性未获确认，不能将汇总变化直接解释为需求增强或吸收压力下降。
TBILL_AUCTION_SIZE：177.00bn（2026-11-02，-48.00bn）；event-based。
TBILL_AUCTION_BTC：2.88ratio（2026-11-02，+0.01ratio）；event-based。
TBILL_AUCTION_STRESS：40.00index（2026-11-02，-10.00index）；事件驱动，财政部T-bill拍卖后公布。

## 信用边际恶化，日元未现急促反转
信用利差及中期隐含波动走高，但金融条件仍偏松。日元汇率缓慢走弱、实现波动下降，期货多头增仓而空头减少，不能据此认定全球套利空头继续加杠杆。
BAMLC0A0CM：0.94%（2026-10-30，+0.09%）；daily T+1。
BAMLH0A0HYM2：3.44%（2026-10-30，+0.34%）；daily T+1。
VIXCLS：19.42index（2026-10-30，+4.11index）；daily T+1。
NFCI：-0.49index（2026-10-23，+0.01index）；weekly。
USDJPY：157.83原始比例/口径（2026-10-29，+0.04原始比例/口径）；按来源频率。
USDJPY_VOL20：5.08原始比例/口径（2026-10-29，-0.13原始比例/口径）；按来源频率。
jpy:CFTC_DECOMPOSITION：日期未知；状态 unknown；无可用数值。

## 现金缓冲对后续冲击更敏感
低逆回购缓冲叠加准备金近期下降，提高财政补库等冲击传向银行体系的敏感度。银行融资稳定与财政现金释放限制当前严重程度，尚不能认定准备金已稀缺。
RRP_BUFFER：5.09bn（2026-11-02，+0.71bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-36.42bn）；weekly。
EFFR：3.88%（2026-10-30，+0.00%）；daily T+1。
TGA_FLOW：-88.64bn（2026-10-30，-113.25bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。

## 结算与融资压力可能相互放大
仅在净筹资及财政现金吸收获得确认、且资金价格同步恶化时，公告供给才可能放大融资约束。当前只有毛发行安排，到期、净筹资及准备金影响保持未知。
event:gross_total_by_issue_date:2026-11-05：日期未知；状态 unknown；无可用数值。
ANNOUNCED_SETTLEMENTS_7D：100.00bn（2026-11-03，环比未知）；announced event schedule。
SOFR_IORB：5.00bp（2026-10-30，+8.00bp）；daily matched observations。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
TGA：951.59bn（2026-10-30，-88.64bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。

## 当前价格、资金流和直接预期覆盖不足
股票与BTC数据为离线缓存，不能充当当前确认；BTC资金流与衍生杠杆、直接市场预期以及增长盈利均缺失。历史趋势未核验当时可见版本，不能据此宣称预测优势。
coverage:market:SP500：2026-10-30；状态 cached_offline；无可用数值。
coverage:market:NASDAQCOM：2026-11-02；状态 cached_offline；无可用数值。
coverage:market:CBBTCUSD：2026-11-02；状态 cached_offline；无可用数值。
coverage:btc_flows_leverage：2026-11-03；状态 missing；无可用数值。
coverage:direct_expectations：2026-11-03；状态 missing；无可用数值。
coverage:growth_earnings：2026-11-03；状态 missing；无可用数值。
coverage:historical_vintages：2026-11-03；状态 prospective_capture_only；无可用数值。

## 离岸与日元套利链条存在观测盲区
商业票据陈旧，日债来自混合来源且历史样本有限，同期美日利差缺失；广义美元指数无法补足跨币种融资基差。核心融资交易日期也早于快照，限制即时压力与套利反转判断。
quality:stale_metric:DCPN3M：2026-10-13；状态 stale；无可用数值。
quality:jpy_missing:US_JP_10Y：日期未知；状态 missing；无可用数值。
quality:jpy_missing:US_JP_2Y：日期未知；状态 missing；无可用数值。
JGB10：2.77原始比例/口径（2026-11-03，环比未知）；按来源频率。
DTWEXBGS：121.67index（2026-10-30，-0.07index）；daily T+1。
SOFR：3.95%（2026-10-30，+0.01%）；daily T+1。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。