# 美元流动性分析
2026-10-30 14:20:01 UTC+08:00

中性偏紧
2026-10-30最新可得快照显示：核心融资与信用观测主要截至2026-10-28，国债曲线截至2026-10-29；缓冲偏薄与回购溢价构成约束，财政现金单日释放和折现率回落提供抵消，尚无严重融资压力的交叉确认。

## 美股与BTC中期投资研究
中期风险承担面对上游现金与缓冲约束、融资相对成本偏紧和折现率改善的拉扯。实际利率回落提供估值支持，但未伴随一致的风险资产价格确认；美股偏分化，BTC缺少资金流与杠杆验证。判断仅描述美元流动性贡献，不代表综合回报评级。

相对上次：已提供的比较事实显示，相对上次成功事实包，资金价格、数量缓冲、名义与实际收益率、模型分解及信用金融条件均未实质更新；因此没有新增上游变化可据以调整研究倾向。资产价格与日元模块未提供对应比较事实，不推断其包间变化，也不臆测上次模型观点。

### 美股：分化（2—12周，中等置信度）
判断：腹部实际收益率月度回落有利估值，但现金供给与融资背景限制风险承担，权益确认分化。缺少增长及盈利数据，不能认定利率下降必然改善完整股票回报。
传导：上游财政现金积累与准备金偏弱可能约束中介风险承载；回购相对成本走高提高融资摩擦。真实贴现率回落则减轻久期估值压力，两条机制方向相反，信用和股价仅作下游确认。
市场确认：标普在其月度窗口上涨，近期信用修复支持风险承受尚有韧性；纳斯达克综合指数在对应窗口下跌，最新实际利率下降时其价格仍走弱，尚缺一致的久期资产确认。两指数日期与窗口不完全相同。
失效条件：若财政现金持续下降、准备金连续周度回升且回购溢价收窄，并伴随主要股指共同走强和信用不再走阔，可推翻当前分化判断；若实际收益率重新持续上行并伴随信用走阔，则转向更明确压制。
覆盖边界：缺增长、盈利修正、权益资金流及市场广度，无法区分增长恶化与折现率下降的完整影响。窗口端点变化不代表连续路径，不能将价格上涨当作新增美元供给。
事实引用：trend:TGA:20obs, trend:WRESBAL:5obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:DFII7:20obs, market:SP500:20obs, market:NASDAQCOM:20obs, market:NASDAQCOM:level, trend:BAMLH0A0HYM2:5obs, coverage:growth_earnings

### BTC：分化（2—12周，低置信度）
判断：实际贴现率下降改善美元背景，但缓冲薄和融资摩擦仍构成约束，BTC近期价格未确认改善向自身传导；资产特定资金机制未知。
传导：真实无风险收益下降可能降低非生息资产的机会成本，数量缓冲偏弱与美元融资摩擦则可能限制风险预算。两者不能直接映射成BTC现货净流入或杠杆变化。
市场确认：BTC最新价格及近期多个窗口走弱，尚未确认折现率改善带来价格支持；较长窗口大体持平。窗口含周末，不能与美股交易观测窗口直接等同。缺现货资金流与衍生仓位，不能认定杠杆去化完成。
失效条件：若准备金连续回升、回购溢价持续收窄且BTC价格趋势转强，并有补充现货净流入确认，可推翻当前分化判断并提高支持置信度；若实际利率回升、融资溢价扩大且BTC持续走弱，则转向压制。
覆盖边界：未配置ETF流、稳定币供给、合约持仓、资金费率及清算数据；无法区分现货卖压、衍生去杠杆或其他驱动，不形成买入机会结论。
事实引用：derived:RRP_BUFFER, trend:WRESBAL:5obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:DFII7:20obs, market:CBBTCUSD:level, market:CBBTCUSD:5obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：名义曲线与FRBSF提供政策路径及期限补偿的代理信息，后者属于模型估计；没有直接期货、调查共识或事件预期差数据，无法判断充分定价或存在可交易预期差。

### 基准情景
若银行间价格继续稳定、回购溢价未持续扩大且实际收益率保留近期回落，薄缓冲背景下风险资产维持分化，估值改善难以独自转化为全面风险扩张。
触发：后续融资观测仍围绕政策锚运行，准备金未出现连续加速下降，信用利差没有持续走阔。
失效：数量与融资同时持续改善并获得广泛价格确认，或数量收缩与融资及信用恶化形成同步链条。
事实引用：metric:EFFR, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, derived:RRP_BUFFER, trend:DFII5:20obs, metric:BAMLH0A0HYM2, market:NASDAQCOM:20obs, market:CBBTCUSD:20obs

### 改善情景
若财政现金持续释放并带动准备金恢复，融资摩擦缓和且实际收益率保持回落，美元流动性对风险承担的贡献可转为支持；BTC仍须独立资金确认。
触发：财政现金在后续窗口下降、准备金连续周度上升、回购溢价持续收窄，同时信用稳定、主要股指与BTC各自趋势改善。
失效：财政现金重新累计增加、准备金恢复中断，或实际利率回升并伴随信用走阔；仅价格反弹而上游未改善不足以成立。
事实引用：derived:TGA_FLOW, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, trend:DFII5:20obs, market:SP500:20obs, market:CBBTCUSD:20obs, coverage:btc_flows_leverage, coverage:growth_earnings

### 恶化情景
若财政现金继续积累、准备金下降并伴随回购溢价持续扩大，薄缓冲可能使现金约束向信用与风险资产扩散；实际利率重新上行会进一步强化压制。
触发：结算后的净现金吸收获得确认，财政现金增加与准备金下降延续，融资相对价格和信用利差同步恶化，风险资产价格持续走弱。
失效：净结算压力未获确认，财政现金转向释放、准备金恢复且融资溢价收窄，信用保持稳定。
事实引用：calendar:7d, event:gross_total_by_issue_date:2026-11-05, derived:RRP_BUFFER, trend:TGA:20obs, metric:WRESBAL, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, metric:BAMLH0A0HYM2, market:CBBTCUSD:20obs

### 下一轮核查
- 优先核查后续匹配日期的回购溢价、成交规模、尾部和无抵押融资，确认最新缓和是否持续。
- 核查财政现金与准备金后续路径，并补齐2026-11-05公告结算的到期额及净筹资；毛发行保持情景输入。
- 跟踪近端至腹部名义、实际收益率和通胀补偿的多期方向，补直接政策预期与增长盈利数据。
- 补BTC现货ETF流、稳定币供给、合约持仓和资金费率，检验价格偏弱的具体机制。
- 修复日债混合来源与非连续比较，更新同日美日利差、CFTC仓位和离岸融资基差覆盖。

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
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-10-22 至 2026-10-29；5期；变化 0.03 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-09-30 至 2026-10-29；20期；变化 -1.169 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-04 至 2026-10-29；60期；变化 0.03 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
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
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "10个有效交易观测", "window": 10, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "20个有效交易观测", "window": 20, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "equities", "asset_name": "美股", "price_series": "SP500", "horizon": "60个有效交易观测", "window": 60, "window_basis": "valid_trading_observations", "liquidity_bias": "分化", "confidence": "中等", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "14个自然日", "window": 14, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "28个自然日", "window": 28, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}
- {"run_id": "20261030_141915_5b11f5f4", "published_at_bjt": "2026-10-30T14:24:02.117660+08:00", "source_generated_at_bjt": "2026-10-30T14:20:01+08:00", "method_version": "3.0", "asset": "bitcoin", "asset_name": "BTC", "price_series": "CBBTCUSD", "horizon": "84个自然日", "window": 84, "window_basis": "calendar_days", "liquidity_bias": "分化", "confidence": "低", "status": "pending", "status_note": "等待发布后的观察价格和完整持有窗口。", "evaluation_price_cutoff": "2026-10-28", "entry_date": null, "entry_price": null, "exit_date": null, "exit_price": null, "elapsed_calendar_days": null, "return_pct": null, "max_drawdown_pct": null, "max_adverse_excursion_pct": null, "benchmark_return_pct": null, "minimum_entry_date": "2026-11-01"}

## 最新融资边际缓和，银行间价格稳定
回购相对准备金利率仍有正溢价，但最新一期收窄，成交规模及假设性价格乘规模代理同时下降；无抵押隔夜利率持平。
EFFR：3.88%（2026-10-28，+0.00%）；daily T+1。
OBFR：3.88%（2026-10-28，+0.00%）；daily T+1。
SOFR_ANCHOR：4.00bp（2026-10-28，-1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3074.00bn（2026-10-28，-73.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：3.42mn/day（2026-10-28，-0.96mn/day）；日频，纽约联储SOFR记录随利率一同发布。

## 财政现金单日下降，多期数量背景仍弱
财政现金最新单日下降，但多期窗口累计增加；准备金最新周度下降，逆回购最新操作余额增加。这些不同频率的变化并存，不能直接作会计归因。
TGA_FLOW：-36.90bn（2026-10-28，-68.73bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
TGA：1015.63bn（2026-10-28，+79.03bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
RRP_FLOW：0.18bn（2026-10-29，环比未知）；日频，纽约联储每日操作结果。

## 近端至腹部收益率共同回落
名义主框架各期限最新一期均下降；腹部官方实际收益率与预计算通胀补偿也下降。通胀补偿包含风险溢价和TIPS流动性影响。
DGS1：4.42%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.73%（2026-10-29，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.78%（2026-10-29，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.87%（2026-10-29，-0.08%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.31%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.46%（2026-10-29，-0.05%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.47%（2026-10-29，-0.02%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.41%（2026-10-29，-0.03%）；日频，FRED/H.15国债恒定期限收益率。

## 短债拍卖需联合看规模与覆盖
最新已完成短债拍卖同时提供发行规模、加权投标覆盖倍数与预计算压力指标。期限组合变化限制跨事件比较，压力指标主要依赖规模，不能据此认定需求失灵。
TBILL_AUCTION_SIZE：225.00bn（2026-10-29，+150.00bn）；event-based。
TBILL_AUCTION_BTC：2.87ratio（2026-10-29，-0.21ratio）；event-based。
TBILL_AUCTION_STRESS：50.00index（2026-10-29，+50.00index）；事件驱动，财政部T-bill拍卖后公布。

## 信用修复与风险资产价格分化
信用利差与波动率最新一期下降，但各自窗口内标普价格走高、纳斯达克综合指数与BTC走低；下游表现没有形成一致改善。
BAMLC0A0CM：0.86%（2026-10-28，-0.02%）；daily T+1。
BAMLH0A0HYM2：3.14%（2026-10-28，-0.04%）；daily T+1。
VIXCLS：16.91index（2026-10-28，-0.61index）；daily T+1。
SP500：1.21%（2026-10-28，+1.21%）；daily close / US trading observations。
NASDAQCOM：-2.56%（2026-10-29，-2.56%）；daily close / US trading observations。
CBBTCUSD：-5.58%（2026-10-29，-5.58%）；daily / 7-day observations。

## 可释放缓冲薄，现金冲击敏感度上升
逆回购缓冲很薄，准备金多周下降与财政现金多期积累增加后续现金冲击敏感度；银行间价格仍稳定，尚不能认定准备金稀缺或严重压力。
RRP_BUFFER：0.35bn（2026-10-29，+0.18bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-36.42bn）；weekly。
TGA：1015.63bn（2026-10-28，+79.03bn）；daily T+1。
EFFR：3.88%（2026-10-28，+0.00%）；daily T+1。

## 离岸与日元链条存在陈旧和口径问题
商业票据、广义美元和交割失败只能作背景。日债采用官方历史与商业补丁混合来源，标为单期的比较跨月；美日长端利差停留在较早日期。仓位拆解中的净空头表述与净头寸符号不一致，应以多空原始事实及回补方向为准。
quality:stale_metric:DCPN3M：2026-10-13；状态 stale；无可用数值。
quality:stale_metric:DTWEXBGS：2026-10-23；状态 stale；无可用数值。
quality:stale_metric:REPO_FAILS_UST：2026-10-14；状态 stale；无可用数值。
JGB10：2.77原始比例/口径（2026-10-30，-0.28原始比例/口径）；按来源频率。
US_JP_10Y：223.30原始比例/口径（2026-09-30，+5.50原始比例/口径）；按来源频率。
jpy:CFTC_DECOMPOSITION：日期未知；状态 unknown；无可用数值。
CFTC_JPY_NET_OI：0.18原始比例/口径（2026-10-20，+0.05原始比例/口径）；按来源频率。

## 结算冲击需净额与融资确认
以2026-10-30快照为起点，2026-11-05公告结算是后续核查节点。毛发行不能确定净现金吸收；只有触发条件成立，才将其升级为实际流动性收紧。
event:gross_total_by_issue_date:2026-11-05：日期未知；状态 unknown；无可用数值。
ANNOUNCED_SETTLEMENTS_7D：277.00bn（2026-10-30，环比未知）；announced event schedule。
SOFR_ANCHOR：4.00bp（2026-10-28，-1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3074.00bn（2026-10-28，-73.00bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。

## 中期资产归因仍有关键缺口
缺少直接政策预期、增长盈利及BTC现货资金流和衍生杠杆，不能判断充分定价、完整股票回报或BTC新增资金入场。趋势历史未经逐时点版本验证，不能用于宣称已建立预测优势。
coverage:direct_expectations：2026-10-30；状态 missing；无可用数值。
coverage:btc_flows_leverage：2026-10-30；状态 missing；无可用数值。
coverage:growth_earnings：2026-10-30；状态 missing；无可用数值。
coverage:historical_vintages：2026-10-30；状态 prospective_capture_only；无可用数值。