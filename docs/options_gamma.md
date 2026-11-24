# 怎样读美股期权与 Gamma

如果做市商整体持有负 Gamma，指数上涨时，他们为了维持对冲可能需要买入更多标的，这种买入又可能放大涨势。判断这种反馈是否真的发生，需要知道做市商在各合约上的持仓方向，并核对实际的对冲交易。一笔期权成交同时有买卖双方，成交量很大也可能伴随很小的净敞口。[Cboe 对 SPX 当日到期期权的研究](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/)

| 看板读数 | 它回答的问题 | 观测口径 |
| --- | --- | --- |
| 标普500平值期权的30天模型 | 假设指数上涨1%，这份标准期权的 Delta 大约增加几个百分点？ | 只配对同日的标普500收盘值和 VIX，设行权价等于指数点位、剩余30个自然日、利率与股息率均为零。使用局部 Gamma 做一阶近似。VIX 是模型输入，两者合计只提供一份波动率证据。 |
| 标普500股指期货期权的交易商方向敞口 | 把交易商的期权风险换算成标普期货，方向相当于净多还是净空多少手？ | 对齐 CFTC 两份报表的交易日期、合约市场编号 `13874+` 和交易商类别，用合并表的净多手数减去仅期货表的净多手数。两次净额都等于多头减空头。正数表示净多头，负数表示净空头。范围为该股指期货市场的期权，SPX 现金指数期权和 SPY ETF 期权在其范围之外。 |
| SPX 与 SPXW 真实期权链 | 全部存续合约按未平仓量计算，对指数变动有多少敏感度？主要集中在哪些到期日和行权价？ | 基于获准使用的合约 Gamma 和未平仓量，将各合约敏感度按绝对值汇总。做市商的持仓方向、净 Gamma 和实际对冲交易仍然未知。 |

CFTC 的合并报表将期权按交易所提供的 Delta 转换为期货等值。看板使用持仓观测日标记数据，当期是否可用还取决于真实发布时间，节假日可能延后。CFTC 自身发布的政府信息可附来源再分发。标普500和 VIX 来自项目既有的 FRED 序列，其页面另列有原数据提供方版权条款。[CFTC 合并报表](https://publicreporting.cftc.gov/Commitments-of-Traders/TFF-Combined/yw9f-hn96) · [仅期货报表](https://publicreporting.cftc.gov/Commitments-of-Traders/TFF-Futures-Only/gpe5-46if) · [CFTC 口径](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes/index.htm) · [发布日历](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm) · [CFTC 使用条款](https://www.cftc.gov/WebPolicy/index.htm) · [标普500来源](https://fred.stlouisfed.org/series/SP500) · [VIX 来源](https://fred.stlouisfed.org/series/VIXCLS)

## 启用真实期权链

1. 自动更新使用已有公开数据计算模型和 CFTC 仓位。若另有 SPX 与 SPXW 标准期权的完整快照，先核对供应商协议是否明确允许本项目加工数据，并向指定仓库 `github.com/eihei317/usd-liquidity` 导出总敞口、到期占比及按行权价汇总的数据。应按仓库的实际访问范围核对许可。可访问网页、持有账户或购买个人行情订阅本身不能确认这项权限。[OCC 网站条款](https://www.theocc.com/specialpages/legal/terms-and-conditions) · [Cboe API 外部分发条款](https://datashop.cboe.com/cboe-all-access-api) · [OPRA 数据分发说明](https://www.opraplan.com/faqs)
2. 将每份快照保存为一个 UTF-8 JSON 文件，放在项目本机的 `.workbuddy/option_chains/`。供应商原始逐合约数据仅存本机，密钥和授权合同单独保存。对同日不同时刻的快照使用不同文件名。下次正常更新时，管线按采集截止时刻选用当时已可取得的快照。
3. 打开本地看板的“美股期权与 Gamma”，核对行情时刻和未平仓量日期，再展开“查看数据范围与逐日缺口”。如果数据部分缺失、快照尚未发布或向指定仓库导出的权限未确认，面板会保留缺口。滞后的完整观测会注明时点。

### 快照字段

| 字段 | 值或含义 |
| --- | --- |
| `schema_version`、`underlying` | 数字 `1`、字符串 `"SPX"`。 |
| `source`、`source_url` | 可对外显示的供应商名称、无查询参数的 HTTPS 产品说明地址。 |
| `allowed_aggregate_destination` | 确认有向指定仓库导出的权限后填写 `"github.com/eihei317/usd-liquidity"`。这个字段记录已经获得的权限。 |
| `observed_at`、`available_at` | 含时区的 ISO 8601 时间。前者是指数点位与合约 Gamma 的共同报价时点，后者是包含未平仓量在内的完整快照实际可取得的时刻。 |
| `open_interest_as_of` | 本次未平仓量的观测日期，格式为 `YYYY-MM-DD`。即使当天有新报价，未平仓量也可能来自前一个交易日。 |
| `scope`、`complete_chain` | `"all_unexpired_standard_SPX_SPXW"` 与布尔值 `true`。提供者确认已包含观测时刻仍然存续的全部标准 SPX 与 SPXW 合约。 |
| `spot`、`contract_multiplier`、`gamma_unit` | 指数点位、数字 `100` 美元／指数点、字符串 `"delta_per_index_point"`。 |
| `contracts` | 每一行包括 `root`（`"SPX"` 或 `"SPXW"`）、`right`（`"C"` 或 `"P"`）、`expiration`（纽约到期日期）、`strike`（行权价）、`gamma`（每一指数点对应的 Delta 变化）和 `open_interest`（未平仓合约数，非负整数）。若供应商提供 `expires_at`、`last_trade_at`，保留带时区的原始时间。 |
| `session_open_at_observation` | 可选布尔值。在供应商或市场日历确认报价时确实开市时填 `true`。计算当日到期占比还需要每个有关合约的到期及最后交易时刻。 |

### 数字如何汇总

对每份合约，用 `Gamma × 未平仓量 × 100 × 指数点位² × 0.01` 估计指数变动 1% 对应的美元敏感度，将看涨与看跌合约的正向绝对量累加。看板列出纽约到期日距观测日 0–7 日的合约占总量的比例，也可列出同一行权价合并后的前五档。计算当日仍可交易的到期合约占比需要可靠的最后交易与到期时刻。条件欠缺时该占比显示为未知。总量和少数行权价集中不能单独证明即将发生强制对冲、价格被固定在某个点位或出现 Gamma 挤压。[Gamma 定义](https://www.optionseducation.org/advancedconcepts/gamma) · [Cboe 对持仓方向的说明](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/)
