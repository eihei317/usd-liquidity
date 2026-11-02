# 美元流动性分析
2026-11-02 21:31:13 UTC+08:00

中性偏紧
2026-11-02最新可得快照显示美元流动性中性偏紧：财政现金积累、准备金回落与回购溢价走高并存，但银行间融资稳定、腹部收益率下降；观测日期不齐，离岸融资与BTC资金流覆盖不足。

## 美股与BTC中期投资研究
上游财政现金积累与薄缓冲限制中期风险承担，融资成本层面回购偏紧而腹部实际贴现率下降，下游股票和BTC确认分化。流动性对美股的贡献呈分化，对BTC的美元融资背景略偏压制但置信度低。实际利率改善未获广泛价格与信用同步确认，不能据此推导完整资产回报、买卖机会或新增资金入场。

相对上次：相对2026-10-30上次成功事实包，新增观测显示财政现金与逆回购增加，回购价格和规模上升；名义腹部及实际收益率下降提供相反方向的估值支持。信用利差与VIX上升，而无抵押融资和政策锚水平未变。准备金、SOMA及NFCI没有新增观测，不能把旧周度变化再写成本轮新冲击。依据comparison:TGA、comparison:RRPONTSYD、comparison:SOFR、comparison:SOFR_VOLUME、comparison:DGS1、comparison:DGS3、comparison:DGS5、comparison:DGS7、comparison:DFII5、comparison:DFII7、comparison:BAMLC0A0CM、comparison:BAMLH0A0HYM2、comparison:VIXCLS、comparison:EFFR、comparison:IORB、comparison:WRESBAL、comparison:SOMA、comparison:NFCI；不推测上次模型观点。

### 美股：分化（2—12周，中等置信度）
判断：腹部真实贴现率下降对估值形成支持，但数量缓冲与抵押融资方向相反，流动性尚未形成一致顺风。标普与纳斯达克综合的中期表现分化，不能用局部上涨反推美元供给增加。
传导：上游现金积累和准备金缓冲下降提高资金敏感度；回购成本上升约束杠杆融资，实际收益率下降缓解久期估值压力。信用利差未同步持续收窄，使估值改善向风险承担的传导仍待确认。
市场确认：标普可用中期窗口上涨，纳斯达克综合同期方向较弱，信用与VIX中期略恶化而较短窗口改善，显示下游确认不一致。缺增长与盈利修正，无法区分利率下降中的估值支持与增长担忧，更不能形成完整股票回报判断。
失效条件：若TGA连续回落、准备金稳定回升、回购相对政策锚溢价持续收敛，同时信用收窄且股票表现趋于同步，将推翻分化判断并转向支持；若实际收益率持续反弹，且信用扩大、股市走弱与融资溢价上升同步，则转向压制。
覆盖边界：股票指数截至不同观测日期，窗口按美国交易观测计；周频准备金不能当作日频资金流。缺盈利、增长、行业资金流和直接政策预期，流动性贡献不等同综合投资评级。
事实引用：trend:TGA:20obs, trend:WRESBAL:5obs, derived:RRP_BUFFER, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, trend:DFII7:20obs, market:SP500:20obs, market:NASDAQCOM:20obs, trend:BAMLH0A0HYM2:20obs, trend:VIXCLS:20obs, coverage:growth_earnings, coverage:direct_expectations

### BTC：压制（2—12周，低置信度）
判断：美元现金缓冲与回购融资背景对BTC风险承担略偏压制，腹部真实贴现率下降提供抵消。现货近期及中期窗口走弱，与尚未形成一致流动性支持相容，但不能确认美元机制是价格变化的唯一原因。
传导：美元融资与现金机会成本通过风险预算及杠杆承受力影响BTC；实际收益率下降可缓解机会成本。BTC现货资金来源及衍生杠杆不在输入中，不能将美元背景直接等同于BTC资金流。
市场确认：BTC最新价格回升，但近期与中期窗口仍下降，较长窗口则上涨，说明反弹尚未形成一致趋势。缺ETF流、稳定币供给、合约仓位和资金费事实，无法确认新增资金进入或杠杆去化完成；股票表现不作为BTC资金流证据。
失效条件：若财政现金持续释放、准备金稳定、回购溢价持续收敛，且BTC现货在后续多个观测窗口止跌转强，则偏压制判断失效；补齐资金流后若进一步显示持续净流入，可增强转向支持的依据。若实际收益率反弹且融资溢价、BTC现货走弱同步持续，则压制判断获得加强。
覆盖边界：BTC含周末观测，其窗口不能等同美股交易日。缺现货资金流和衍生杠杆，只有美元背景与价格确认，因此置信度低，不据此声称出现买入机会。
事实引用：trend:TGA:20obs, trend:WRESBAL:5obs, derived:RRP_BUFFER, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:DFII5:20obs, market:CBBTCUSD:level, market:CBBTCUSD:5obs, market:CBBTCUSD:20obs, market:CBBTCUSD:60obs, coverage:btc_flows_leverage

### 市场预期覆盖
部分覆盖：国债近端与腹部价格及FRBSF模型分解可观察政策路径候选变化，模型中期平均预期短率下降与期限补偿回落提供部分解释。缺SOFR期货、调查共识与事件预期差，无法判断已充分定价或存在可交易预期差；模型与价格反应不是两类直接共识证据。

### 基准情景
若上游现金偏紧与折现率缓解继续并存，流动性对美股维持分化贡献，对BTC风险承担支持有限，市场表现仍需自身价格和资金链条确认。
触发：无抵押融资继续稳定，回购溢价未持续加速扩大，实际收益率维持近期回落方向，而TGA与准备金尚未出现持续改善。
失效：数量缓冲和资金价格同步持续改善，或融资异常向无抵押市场并伴随信用持续恶化扩散，均使此混合路径失效。
事实引用：trend:EFFR:20obs, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, trend:TGA:20obs, trend:WRESBAL:5obs, trend:DFII5:20obs, market:SP500:20obs, market:CBBTCUSD:20obs

### 改善情景
若财政现金释放与融资成本改善共同出现，且真实贴现率保持缓和，流动性对美股和BTC风险承担的贡献可转向支持。
触发：TGA连续下降、准备金稳定回升、回购相对政策锚溢价持续收敛，信用收窄且美股与BTC各自价格趋势改善；BTC资金流支持仍须另行补齐确认。
失效：财政现金重新持续积累，或融资溢价再度扩大且实际收益率反弹，或信用持续走弱而资产价格未能确认改善。
事实引用：derived:TGA_FLOW, metric:WRESBAL, derived:RRP_BUFFER, trend:SOFR_IORB:20obs, metric:SOFR_VOLUME, metric:DFII5, metric:BAMLH0A0HYM2, market:SP500:20obs, market:CBBTCUSD:20obs, coverage:btc_flows_leverage

### 恶化情景
若净现金吸收与薄缓冲相互强化，融资压力持续扩散且真实贴现率反弹，流动性对美股与BTC的压制可能增强。
触发：已公告结算经到期额核实后形成净吸收，随后TGA持续上升、准备金回落，回购溢价扩大并获无抵押融资或信用恶化确认；实际收益率同步持续上行。公告毛发行本身不满足触发条件。
失效：净结算并未吸收现金，或财政支出释放现金、准备金稳定且融资溢价收敛，同时信用未持续恶化。
事实引用：event:gross_total_by_issue_date:2026-11-05, calendar:7d, derived:RRP_BUFFER, metric:TGA, metric:WRESBAL, derived:SOFR_ANCHOR, metric:SOFR_VOLUME, metric:EFFR, metric:BAMLH0A0HYM2, metric:DFII5

### 下一轮核查
- 优先更新同日政策锚、回购价格与成交规模、无抵押融资及尾部分布，确认溢价扩大是否持续并向银行间扩散。
- 核对2026-11-05结算的到期额与净现金筹集，并结合后续TGA、RRP流量及新一期准备金判断实际现金影响。
- 观察腹部名义与实际收益率回落能否延续，并与信用、VIX和股票各自趋势交叉验证，补齐增长及盈利修正。
- 补齐BTC现货ETF流、稳定币供给、合约仓位与资金费，区分现货反弹、资金流改善和杠杆变化。
- 更新离岸融资基差、直接政策预期及同日美日利差，校核日债混合来源、派生溯源和抓取时间元数据。

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
- Standing overnight repo accepted amount：5个有效日频观测间隔变化：2026-10-23 至 2026-10-30；5期；变化 0.0 USD bn；状态 ok；trend:SRP_ACCEPTED:5obs
- Standing overnight repo accepted amount：20个有效日频观测间隔变化：2026-10-01 至 2026-10-30；20期；变化 0.0 USD bn；状态 ok；trend:SRP_ACCEPTED:20obs
- Standing overnight repo accepted amount：60个有效日频观测间隔变化：2026-08-05 至 2026-10-30；60期；变化 -0.001 USD bn；状态 ok；trend:SRP_ACCEPTED:60obs
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

## 回购价格与规模上升，无抵押融资持平
回购相对政策锚的溢价扩大，成交规模增加，价格乘规模代理同步抬升；无抵押融资与常备工具使用尚未给出全面资金紧张的确认。该代理不等于实际总融资成本。
SOFR_ANCHOR：5.00bp（2026-10-30，+1.00bp）；日频，纽约联储约 8:00 ET 发布。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
SOFR_VOLUME_IMPACT：4.41mn/day（2026-10-30，+0.92mn/day）；日频，纽约联储SOFR记录随利率一同发布。
TGCR：3.93%（2026-10-30，+0.01%）；daily T+1。
BGCR：3.93%（2026-10-30，+0.01%）；daily T+1。
EFFR：3.88%（2026-10-29，+0.00%）；daily T+1。
OBFR：3.88%（2026-10-29，+0.00%）；daily T+1。
SRP_ACCEPTED：0.00bn（2026-10-30，-0.03bn）；daily T+1。

## 财政现金与逆回购增加，准备金周度下降
TGA最新由下降转为增加，RRP也出现资金回流联储工具的方向；准备金和SOMA最新周度下降。各项日期不同，不能拼接为同日准备金变化的会计解释。
TGA_FLOW：24.60bn（2026-10-29，+61.50bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
RRP_FLOW：4.02bn（2026-10-30，环比未知）；日频，纽约联储每日操作结果。
RRP_BUFFER：4.38bn（2026-10-30，+4.02bn）；日频，纽约联储每日操作结果。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。
SOMA：6355.84bn（2026-10-28，-8.00bn）；weekly。

## 腹部名义与实际收益率同步回落
近端至腹部名义收益率最新共同下降，腹部实际收益率与通胀补偿也下降，折现率边际缓解。收益率水平仍保留现金竞争与贴现约束，通胀补偿变化不能直接解释为纯通胀预期变化。
DGS1：4.36%（2026-10-30，-0.06%）；daily / same-day (Treasury 4pm ET)。
DGS3：4.65%（2026-10-30，-0.08%）；daily / same-day (Treasury 4pm ET)。
DGS5：4.71%（2026-10-30，-0.07%）；daily / same-day (Treasury 4pm ET)。
DGS7：4.80%（2026-10-30，-0.07%）；daily / same-day (Treasury 4pm ET)。
DFII5：2.25%（2026-10-30，-0.06%）；daily / same-day (Treasury 4pm ET)。
DFII7：2.42%（2026-10-30，-0.04%）；daily / same-day (Treasury 4pm ET)。
UST_5Y_BREAKEVEN：2.46%（2026-10-30，-0.01%）；日频，FRED/H.15国债恒定期限收益率。
UST_7Y_BREAKEVEN：2.38%（2026-10-30，-0.03%）；日频，FRED/H.15国债恒定期限收益率。

## 短债拍卖组合变化限制直接比较
最新已完成短债拍卖汇总规模较大，覆盖倍数低于前次汇总，预计算压力代理上升；组合和期限不同，不能直接认定需求恶化。另一国债拍卖需求代理较前次改善，构成反向观察，但不能与短债汇总混用。
TBILL_AUCTION_SIZE：225.00bn（2026-10-29，+150.00bn）；event-based。
TBILL_AUCTION_BTC：2.87ratio（2026-10-29，-0.21ratio）；event-based。
TBILL_AUCTION_STRESS：50.00index（2026-10-29，+50.00index）；事件驱动，财政部T-bill拍卖后公布。
UST_AUCTION_BTC：2.46ratio（2026-10-29，+0.04ratio）；event-based。

## 风险偏好最新转弱，短窗口仍有反向改善
信用利差与VIX最新共同回升，但较短窗口高收益利差和VIX均回落。日元期货多空拆解显示多头主动增仓、空头减少，不能据此声称日元融资carry正在扩张。
BAMLC0A0CM：0.89%（2026-10-29，+0.03%）；daily T+1。
BAMLH0A0HYM2：3.26%（2026-10-29，+0.12%）；daily T+1。
VIXCLS：17.20index（2026-10-29，+0.29index）；daily T+1。
BAMLH0A0HYM2：3.26%（2026-10-29，-0.14%）；daily T+1。
VIXCLS：17.20index（2026-10-29，-1.83index）；daily T+1。
jpy:CFTC_DECOMPOSITION：日期未知；状态 unknown；无可用数值。

## 现金冲击缓冲不足
逆回购存量缓冲薄，叠加财政现金积累与准备金近期回落，使后续现金需求更容易影响银行体系；银行间价格稳定仍是反向证据，尚不能认定准备金已稀缺。
RRP_BUFFER：4.38bn（2026-10-30，+4.02bn）；日频，纽约联储每日操作结果。
TGA：1040.24bn（2026-10-29，+56.19bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-36.42bn）；weekly。
EFFR：3.88%（2026-10-29，+0.00%）；daily T+1。

## 结算后的净现金吸收可能放大融资压力
只有净结算和融资价格共同确认，公告供给才可能转化为实际流动性收缩。当前已公告金额属于毛发行，到期额与净现金影响未知，不能据此认定确定性抽水。
event:gross_total_by_issue_date:2026-11-05：日期未知；状态 unknown；无可用数值。
ANNOUNCED_SETTLEMENTS_7D：277.00bn（2026-11-02，环比未知）；announced event schedule。
TGA_FLOW：24.60bn（2026-10-29，+61.50bn）；日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布。
SOFR_IORB：5.00bp（2026-10-30，+8.00bp）；daily matched observations。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
WRESBAL：2893.77bn（2026-10-28，-68.84bn）；weekly。

## 离岸与资产研究关键链条覆盖不全
美元指数、商业票据及美日长期利差滞后，日债采用官方历史与商业补丁混合来源；最新同日利差不能确认。直接政策预期、BTC资金流与杠杆、增长盈利缺失，限制跨市场和中期资产判断，不能将缺失视为市场中性。
quality:stale_metric:DTWEXBGS：2026-10-23；状态 stale；无可用数值。
quality:stale_metric:DCPN3M：2026-10-13；状态 stale；无可用数值。
US_JP_10Y：223.30原始比例/口径（2026-09-30，+5.50原始比例/口径）；按来源频率。
JGB10：2.77原始比例/口径（2026-11-02，-0.00原始比例/口径）；按来源频率。
coverage:direct_expectations：2026-11-02；状态 missing；无可用数值。
coverage:btc_flows_leverage：2026-11-02；状态 missing；无可用数值。
coverage:growth_earnings：2026-11-02；状态 missing；无可用数值。

## 部分元数据与派生溯源需要校核
成交量记录附带利率分布，腹部组合派生值只列出单一期限基底，短债压力代理仅列规模基底；因此保留原始事实并限制这些派生项的解释权重。日债窗口标签与端点跨度不完全对应，市场记录抓取时间晚于包头时间，历史版本也未经时点验证；这些问题属于数据质量限制。
SOFR_VOLUME：3175.00bn（2026-10-30，+30.00bn）；daily T+1。
UST_BELLY_MOMENTUM：-7.00bp（2026-10-30，环比未知）；日频，FRED/H.15国债恒定期限收益率。
TBILL_AUCTION_STRESS：50.00index（2026-10-29，+50.00index）；事件驱动，财政部T-bill拍卖后公布。
JGB10：2.77原始比例/口径（2026-11-02，-0.00原始比例/口径）；按来源频率。
coverage:historical_vintages：2026-11-02；状态 prospective_capture_only；无可用数值。
SP500：7743.98index（2026-10-28，+21.38index）；daily close / US trading observations。