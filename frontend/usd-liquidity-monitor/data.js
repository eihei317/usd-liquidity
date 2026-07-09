window.DASHBOARD_DATA = {
  "meta": {
    "title": "美元流动性监测",
    "trigger": "今天的美元流动性简报",
    "generated_at_bjt": "2026-07-09 11:01:59 UTC+08:00",
    "data_as_of": "2026-07-09",
    "timezone": "BJT",
    "theme": "warm_claude",
    "version": "1.0"
  },
  "status_scale": {
    "values": [
      "宽松",
      "中性偏松",
      "中性",
      "中性偏紧",
      "紧张"
    ],
    "current_from_rule": "中性",
    "score_from_rule": 0.5999999999999999
  },
  "trading_dashboard": {
    "core": [
      {
        "type": "signal",
        "id": "SOFR_ANCHOR",
        "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
        "priority": "P0",
        "value_text": "-3.0bp",
        "previous_text": "-2.0bp",
        "change_text": "-1.0bp",
        "severity": "中性",
        "why": "回购融资是否高于政策锚",
        "interpretation": "SOFR相对IORB（准备金余额利率）的位置。回购融资与政策锚接近",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "signal",
        "id": "SOFR_VOLUME_IMPACT",
        "label": "SOFR Rate-Volume Impact（SOFR价格×交易量影响）",
        "priority": "P0",
        "value_text": "-2.6mn/day",
        "previous_text": "-1.8mn/day",
        "change_text": "-0.8mn/day",
        "severity": "中性",
        "why": "SOFR价格偏离作用在多大交易量上",
        "interpretation": "SOFR交易量约3,154bn，但SOFR相对政策锚偏离有限，价格×规模冲击不大。",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储SOFR记录随利率一同发布"
      },
      {
        "type": "metric",
        "id": "TGA",
        "label": "TGA（财政部一般账户）",
        "priority": "P0",
        "value_text": "NA",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "缺失",
        "why": "财政抽水/放水",
        "interpretation": "财政部现金余额，余额上升通常抽走银行体系准备金，下降通常释放准备金。",
        "as_of": null,
        "frequency": "日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布"
      },
      {
        "type": "signal",
        "id": "RRP_FLOW",
        "label": "RRP Flow（隔夜逆回购边际流量）",
        "priority": "P0",
        "value_text": "-1.14bn",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "中性",
        "why": "RRP边际流量方向",
        "interpretation": "RRP日变化幅度有限，短期边际流量影响不大。",
        "as_of": "2026-07-08",
        "frequency": "日频，纽约联储每日操作结果"
      },
      {
        "type": "signal",
        "id": "RRP_BUFFER",
        "label": "RRP Buffer（隔夜逆回购存量缓冲垫）",
        "priority": "P0",
        "value_text": "3.35bn",
        "previous_text": "4.48bn",
        "change_text": "-1.1bn",
        "severity": "偏紧",
        "why": "非银现金缓冲垫厚度",
        "interpretation": "RRP存量缓冲垫几乎耗尽，后续TGA补库、QT或美债供给冲击更容易直接落到准备金。",
        "as_of": "2026-07-08",
        "frequency": "日频，纽约联储每日操作结果"
      },
      {
        "type": "metric",
        "id": "WRESBAL",
        "label": "WRESBAL（银行准备金余额）",
        "priority": "P1",
        "value_text": "2,966.9bn",
        "previous_text": "2,951.4bn",
        "change_text": "+15.5bn",
        "severity": "中性",
        "why": "银行准备金水位",
        "interpretation": "银行体系准备金余额，是美元流动性水位的核心变量，但发布频率较低。",
        "as_of": "2026-07-01",
        "frequency": "周频，H.4.1 通常周四 16:30 ET 发布"
      },
      {
        "type": "signal",
        "id": "UST_1Y_YIELD",
        "label": "1Y Treasury Yield（1年期美国国债收益率）",
        "priority": "P1",
        "value_text": "4.060%",
        "previous_text": "3.950%",
        "change_text": "+0.11%",
        "severity": "中性",
        "why": "短债近端政策路径",
        "interpretation": "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "UST_3Y_YIELD",
        "label": "3Y Treasury Yield（3年期美国国债收益率）",
        "priority": "P1",
        "value_text": "4.180%",
        "previous_text": "4.140%",
        "change_text": "+0.04%",
        "severity": "中性",
        "why": "中段政策路径再定价",
        "interpretation": "3年期收益率处于中间区间，观察其相对1年和10年的斜率变化。",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "REAL_10Y",
        "label": "10Y Treasury Yield（10年期美国国债收益率）",
        "priority": "P1",
        "value_text": "4.550%",
        "previous_text": "4.480%",
        "change_text": "+0.07%",
        "severity": "偏紧",
        "why": "10年期国债收益率压力",
        "interpretation": "10年期国债收益率处于高位，对长期资产估值有压力；这描述的是level风险，不代表边际继续恶化。",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "HY_CHANGE",
        "label": "HY OAS Change（高收益债期权调整利差变化）",
        "priority": "P1",
        "value_text": "2.670%",
        "previous_text": "2.720%",
        "change_text": "-0.05%",
        "severity": "偏松",
        "why": "信用压力是否扩散",
        "interpretation": "信用风险偏好改善",
        "as_of": "2026-07-07",
        "frequency": "日频，高收益债OAS"
      }
    ],
    "confirm": [
      {
        "type": "metric",
        "id": "OBFR",
        "label": "OBFR（隔夜银行融资利率）",
        "priority": "P2",
        "value_text": "3.620%",
        "previous_text": "3.620%",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "银行融资压力是否扩散",
        "interpretation": "更广义的银行隔夜融资成本，观察压力是否从联邦基金市场扩散。",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储参考利率"
      },
      {
        "type": "metric",
        "id": "TGCR",
        "label": "TGCR（三方一般抵押品利率）",
        "priority": "P2",
        "value_text": "3.600%",
        "previous_text": "3.610%",
        "change_text": "-1.0bp",
        "severity": "中性",
        "why": "三方回购融资确认",
        "interpretation": "三方回购市场的一般抵押品融资成本，反映机构化回购资金价格。",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "metric",
        "id": "BGCR",
        "label": "BGCR（广义一般抵押品利率）",
        "priority": "P2",
        "value_text": "3.600%",
        "previous_text": "3.610%",
        "change_text": "-1.0bp",
        "severity": "中性",
        "why": "广义回购融资确认",
        "interpretation": "覆盖更广的一般抵押品回购利率，观察回购市场结构性扰动。",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "signal",
        "id": "BGCR_TGCR",
        "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
        "priority": "P2",
        "value_text": "0.0bp",
        "previous_text": "0.0bp",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "回购内部结构扰动",
        "interpretation": "比较广义回购与三方回购的结构差异。一般抵押品利率结构稳定",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "signal",
        "id": "REAL_10Y_MOMENTUM",
        "label": "10Y Yield Momentum（10年期国债收益率边际变化）",
        "priority": "P2",
        "value_text": "7.0bp",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "偏紧",
        "why": "10年期国债收益率边际变化",
        "interpretation": "10年期国债收益率边际上行，长期资产估值压力正在增强。",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "IG_CHANGE",
        "label": "IG OAS Change（投资级公司债期权调整利差变化）",
        "priority": "P2",
        "value_text": "0.760%",
        "previous_text": "0.750%",
        "change_text": "+0.01%",
        "severity": "中性",
        "why": "投资级信用融资",
        "interpretation": "投资级信用利差变化有限",
        "as_of": "2026-07-07",
        "frequency": "日频，投资级公司债OAS"
      },
      {
        "type": "signal",
        "id": "VIX_RISK",
        "label": "VIX Level（标普500隐含波动率水平）",
        "priority": "P2",
        "value_text": "16.13",
        "previous_text": "15.57",
        "change_text": "+0.56",
        "severity": "中性",
        "why": "证券市场波动率水平",
        "interpretation": "证券市场波动率处于中性区间。",
        "as_of": "2026-07-07",
        "frequency": "日频，标普500隐含波动率"
      },
      {
        "type": "signal",
        "id": "VIX_MOMENTUM",
        "label": "VIX Momentum（标普500隐含波动率边际变化）",
        "priority": "P2",
        "value_text": "0.56pt",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "中性",
        "why": "证券市场风险偏好边际变化",
        "interpretation": "VIX边际变化有限。",
        "as_of": "2026-07-07",
        "frequency": "日频，标普500隐含波动率"
      },
      {
        "type": "metric",
        "id": "SOFR_VOLUME",
        "label": "SOFR Volume（SOFR交易量）",
        "priority": "P2",
        "value_text": "3,154.0bn",
        "previous_text": "3,212.0bn",
        "change_text": "-58.0bn",
        "severity": "中性",
        "why": "回购融资交易量级",
        "interpretation": "SOFR对应的隔夜回购交易量，用于把利率偏离转化为价格×规模的实际资金成本量级。",
        "as_of": "2026-07-07",
        "frequency": "日频，纽约联储SOFR记录随利率一同发布"
      },
      {
        "type": "signal",
        "id": "TBILL_AUCTION_STRESS",
        "label": "T-bill Auction Stress Score（短债拍卖吸收压力评分）",
        "priority": "P2",
        "value_text": "40.00",
        "previous_text": "40.00",
        "change_text": "0.00index",
        "severity": "中性",
        "why": "T-bill供给×需求吸收压力",
        "interpretation": "最新T-bill拍卖规模约142.0bn，认购倍数2.89x，上一T-bill拍卖日认购倍数 2.80x；该分数综合供给规模与需求覆盖，数值越高表示吸收压力越大。供给吸收处于中性区间。",
        "as_of": "2026-07-07",
        "frequency": "事件驱动，财政部T-bill拍卖后公布"
      },
      {
        "type": "metric",
        "id": "TBILL_AUCTION_BTC",
        "label": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
        "priority": "P2",
        "value_text": "2.89x",
        "previous_text": "2.80x",
        "change_text": "+0.09x",
        "severity": "中性",
        "why": "短债拍卖需求强度",
        "interpretation": "短期国债拍卖投标覆盖倍数，和拍卖规模一起观察T-bill供给吸收压力。",
        "as_of": "2026-07-07",
        "frequency": "事件驱动，财政部T-bill拍卖后公布"
      },
      {
        "type": "metric",
        "id": "UST_AUCTION_BTC",
        "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
        "priority": "P2",
        "value_text": "3.14x",
        "previous_text": "2.74x",
        "change_text": "+0.40x",
        "severity": "中性",
        "why": "国债供给吸收能力",
        "interpretation": "国债拍卖需求强弱代理指标，观察国债供给吸收能力。",
        "as_of": "2026-07-07",
        "frequency": "事件驱动，财政部拍卖后公布"
      },
      {
        "type": "metric",
        "id": "REPO_FAILS_UST",
        "label": "Repo Fails（美国国债回购交割失败）",
        "priority": "P2",
        "value_text": "91.9bn",
        "previous_text": "101.2bn",
        "change_text": "-9.4bn",
        "severity": "中性",
        "why": "抵押品交割链条",
        "interpretation": "回购和证券交割失败规模，观察抵押品链条和交割压力。",
        "as_of": "2026-06-24",
        "frequency": "周频，OFR/STFM 或一级交易商口径"
      },
      {
        "type": "metric",
        "id": "DTWEXBGS",
        "label": "DTWEXBGS（广义美元指数）",
        "priority": "P2",
        "value_text": "120.69",
        "previous_text": "121.15",
        "change_text": "-0.46",
        "severity": "中性",
        "why": "离岸美元压力",
        "interpretation": "广义美元指数，作为离岸美元融资压力的替代观察。",
        "as_of": "2026-07-02",
        "frequency": "日频，FRED/美联储美元指数口径"
      },
      {
        "type": "signal",
        "id": "CP_PROXY",
        "label": "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）",
        "priority": "P2",
        "value_text": "-3.0bp",
        "previous_text": "-8.0bp",
        "change_text": "+5.0bp",
        "severity": "偏松",
        "why": "企业短融压力代理",
        "interpretation": "用90天AA非金融商业票据利率减联邦基金目标上限，粗略观察企业短融相对政策利率是否变贵；这是信用传导代理指标，不是FRA-OIS。企业短融压力不明显",
        "as_of": "2026-06-26",
        "frequency": "日频，商业票据利率"
      }
    ],
    "background": [
      {
        "type": "metric",
        "id": "SOMA",
        "label": "SOMA（系统公开市场账户持仓）",
        "priority": "B",
        "value_text": "6,334.5bn",
        "previous_text": "6,344.3bn",
        "change_text": "-9.9bn",
        "severity": "中性",
        "why": "QT结构背景",
        "interpretation": "美联储公开市场账户持仓，反映QT和资产端收缩的结构背景。",
        "as_of": "2026-07-01",
        "frequency": "周频，纽约联储/Fed资产负债表背景数据"
      },
      {
        "type": "metric",
        "id": "DGS1",
        "label": "1Y Treasury Yield（1年期美国国债收益率）",
        "priority": "B",
        "value_text": "4.060%",
        "previous_text": "3.950%",
        "change_text": "+11.0bp",
        "severity": "中性",
        "why": "近端政策路径",
        "interpretation": "1年期美国国债收益率，主要反映未来一年政策利率路径和短端再定价。",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "metric",
        "id": "DGS30",
        "label": "30Y Treasury Yield（30年期美国国债收益率）",
        "priority": "B",
        "value_text": "5.050%",
        "previous_text": "4.990%",
        "change_text": "+6.0bp",
        "severity": "中性",
        "why": "长期期限溢价",
        "interpretation": "30年期美国国债收益率，反映长期通胀、财政供给和期限溢价。",
        "as_of": "2026-07-07",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "UST_10Y2Y",
        "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
        "priority": "B",
        "value_text": "35.0bp",
        "previous_text": "36.0bp",
        "change_text": "-1.0bp",
        "severity": "中性",
        "why": "收益率曲线斜率",
        "interpretation": "收益率曲线为正，期限结构相对正常",
        "as_of": "2026-07-08",
        "frequency": "日频，FRED曲线利差"
      },
      {
        "type": "signal",
        "id": "UST_10Y3M",
        "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
        "priority": "B",
        "value_text": "69.0bp",
        "previous_text": "69.0bp",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "衰退/降息预期",
        "interpretation": "10年-3个月曲线为正，政策短端对长期利率压制较弱",
        "as_of": "2026-07-08",
        "frequency": "日频，FRED曲线利差"
      },
      {
        "type": "signal",
        "id": "NFCI_LEVEL",
        "label": "NFCI（芝加哥联储全国金融条件指数）",
        "priority": "B",
        "value_text": "-0.52",
        "previous_text": "-0.51",
        "change_text": "-0.01",
        "severity": "偏松",
        "why": "公开金融条件代理",
        "interpretation": "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察",
        "as_of": "2026-07-03",
        "frequency": "周频，芝加哥联储全国金融条件指数"
      }
    ],
    "core_chart_ids": [
      "anchor_spreads_30d",
      "fed_liability_30d",
      "treasury_combined_supply_30d",
      "us_jp_spread",
      "treasury_yields_30d",
      "jpy_usdjpy_funding_1y"
    ],
    "chart_groups": [
      {
        "id": "core_monthly",
        "title": "核心图表",
        "description": "最近一月核心视图：资金利差、Fed负债端、美债发行、利差、收益率与JPY carry。",
        "chart_ids": [
          "anchor_spreads_30d",
          "fed_liability_30d",
          "treasury_combined_supply_30d",
          "us_jp_spread",
          "treasury_yields_30d",
          "jpy_usdjpy_funding_1y"
        ],
        "default_open": true
      },
      {
        "id": "review_background",
        "title": "背景复盘",
        "description": "复盘时再看，不占用日常交易主视图。",
        "chart_ids": [
          "short_rates_30d",
          "sofr_volume_30d",
          "real_yields_30d",
          "treasury_curve_30d",
          "cp_proxy_30d",
          "credit_oas_30d",
          "risk_appetite_30d",
          "financial_conditions_30d",
          "tbill_auction_size_45d",
          "tbill_auction_btc_45d",
          "upcoming_tbill_supply_60d",
          "jpy_jgb_curve_1y",
          "jpy_cftc_position_2y",
          "jpy_effective_fx_3y"
        ],
        "default_open": false
      }
    ]
  },
  "upcoming_auctions": {
    "status": "ok",
    "as_of": "2026-07-09",
    "lookforward_days": 60,
    "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-07-09&endDate=2026-09-07",
    "auctions": [
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 100.0,
        "offeringAmountText": "$100bn",
        "cusip": "912797UT2",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 95.0,
        "offeringAmountText": "$95bn",
        "cusip": "912797VB0",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-15",
        "announcementDate": "2026-07-02",
        "securityType": "Bond",
        "securityTerm": "29-Year 10-Month",
        "offeringAmount": 22.0,
        "offeringAmountText": "$22bn",
        "cusip": "912810UU0",
        "is_bill": false,
        "is_note_or_bond": true
      }
    ],
    "bill_schedule": [
      {
        "auctionDate": "2026-07-09",
        "totalBillOffering": 195.0,
        "items": [
          {
            "auctionDate": "2026-07-09",
            "issueDate": "2026-07-14",
            "announcementDate": "2026-07-07",
            "securityType": "Bill",
            "securityTerm": "4-Week",
            "offeringAmount": 100.0,
            "offeringAmountText": "$100bn",
            "cusip": "912797UT2",
            "is_bill": true,
            "is_note_or_bond": false
          },
          {
            "auctionDate": "2026-07-09",
            "issueDate": "2026-07-14",
            "announcementDate": "2026-07-07",
            "securityType": "Bill",
            "securityTerm": "8-Week",
            "offeringAmount": 95.0,
            "offeringAmountText": "$95bn",
            "cusip": "912797VB0",
            "is_bill": true,
            "is_note_or_bond": false
          }
        ],
        "totalBillOfferingText": "$195bn"
      }
    ],
    "next_auctions": [
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 100.0,
        "offeringAmountText": "$100bn",
        "cusip": "912797UT2",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 95.0,
        "offeringAmountText": "$95bn",
        "cusip": "912797VB0",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-15",
        "announcementDate": "2026-07-02",
        "securityType": "Bond",
        "securityTerm": "29-Year 10-Month",
        "offeringAmount": 22.0,
        "offeringAmountText": "$22bn",
        "cusip": "912810UU0",
        "is_bill": false,
        "is_note_or_bond": true
      }
    ],
    "large_auctions": [
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 100.0,
        "offeringAmountText": "$100bn",
        "cusip": "912797UT2",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-09",
        "issueDate": "2026-07-14",
        "announcementDate": "2026-07-07",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 95.0,
        "offeringAmountText": "$95bn",
        "cusip": "912797VB0",
        "is_bill": true,
        "is_note_or_bond": false
      }
    ],
    "notes": "TreasuryDirect future auction calendar. offeringAmount may be absent before official announcement; treat missing amounts as data risk, not zero issuance."
  },
  "jpy_carry": {
    "meta": {
      "generated_at_bjt": "2026-07-09 11:01:41 UTC+08:00",
      "lookback": "日频约1年，CFTC约2年，REER/NEER约3年"
    },
    "risk": {
      "label": "中性偏高",
      "score": 2.0,
      "reasons": [
        "CFTC日元非商业净空头占未平仓合约比例偏高",
        "美日10Y利差处于相对较窄区域，收益端安全垫下降"
      ]
    },
    "cards": [
      {
        "id": "USDJPY",
        "label": "USD/JPY（美元兑日元）",
        "value_text": "161.97",
        "change_text": "逐日 -0.12%",
        "as_of": "2026-07-07",
        "why": "日元快速升值会触发carry止损/回补"
      },
      {
        "id": "JPY_CALL",
        "label": "JPY隔夜融资成本（日本无担保隔夜拆借利率）",
        "value_text": "0.978%",
        "change_text": "逐日 0.1bp",
        "as_of": "2026-07-07",
        "why": "carry trade 的融资端"
      },
      {
        "id": "JGB10",
        "label": "JGB 10Y（日本10年期国债收益率）",
        "value_text": "2.690%",
        "change_text": "逐日 4.6bp",
        "as_of": "2026-06-30",
        "why": "日本本土资产吸引力和资金回流压力"
      },
      {
        "id": "US_JP_10Y",
        "label": "10Y UST-JGB利差（美日10年期国债利差）",
        "value_text": "186bp",
        "change_text": "收益端核心",
        "as_of": "2026-06-30",
        "why": "美日长端利差越宽，carry收益端越顺风"
      },
      {
        "id": "CFTC_JPY",
        "label": "CFTC JPY净仓位/OI（日元期货非商业净仓位占比）",
        "value_text": "-35.3%",
        "change_text": "净周变化 -8,988 口",
        "as_of": "2026-06-30",
        "why": "净空头边际变化需拆分：净空头变化中空头主动加仓（空头周变化 +7,162.0 口、多头 -1,826.0 口）：投机盘真实卖出日元、买入美元，carry 资金流在增强，对美元短期利好。"
      },
      {
        "id": "CFTC_JPY_GROSS_SHORT",
        "label": "CFTC JPY非商业空头（总口数）",
        "value_text": "266,964",
        "change_text": "周变化 7,162 口",
        "as_of": "2026-06-30",
        "why": "空头合约绝对量；周变化确认 carry 是否真在加仓（比 net/OI 更直接）"
      },
      {
        "id": "CFTC_JPY_SHORT_SHARE",
        "label": "CFTC JPY空头占比（空头/(空头+多头)）",
        "value_text": "70.5%",
        "change_text": "周变化 +0.9%",
        "as_of": "2026-06-30",
        "why": "空头一侧真实强度代理；近1年分位 100%"
      },
      {
        "id": "USDJPY_VOL20",
        "label": "USD/JPY 20日实现波动率（年化）",
        "value_text": "5.22%",
        "change_text": "年化",
        "as_of": "2026-07-07",
        "why": "波动率上升会降低carry策略夏普"
      },
      {
        "id": "JPY_REER",
        "label": "JPY REER（日元实际有效汇率）",
        "value_text": "65.93",
        "change_text": "NA",
        "as_of": "202605",
        "why": "估值和政策敏感度背景"
      }
    ],
    "cftc_decomposition": {
      "driver": "short_building",
      "text": "净空头变化中空头主动加仓（空头周变化 +7,162.0 口、多头 -1,826.0 口）：投机盘真实卖出日元、买入美元，carry 资金流在增强，对美元短期利好。"
    },
    "history": {
      "USDJPY": [
        {
          "date": "2025-06-13",
          "value": 143.8
        },
        {
          "date": "2025-06-16",
          "value": 144.19
        },
        {
          "date": "2025-06-17",
          "value": 144.54
        },
        {
          "date": "2025-06-18",
          "value": 144.95
        },
        {
          "date": "2025-06-19",
          "value": 145.4
        },
        {
          "date": "2025-06-20",
          "value": 145.41
        },
        {
          "date": "2025-06-23",
          "value": 147.33
        },
        {
          "date": "2025-06-24",
          "value": 145.31
        },
        {
          "date": "2025-06-25",
          "value": 145.32
        },
        {
          "date": "2025-06-26",
          "value": 144.06
        },
        {
          "date": "2025-06-27",
          "value": 144.48
        },
        {
          "date": "2025-06-30",
          "value": 144.13
        },
        {
          "date": "2025-07-01",
          "value": 143.08
        },
        {
          "date": "2025-07-02",
          "value": 143.9
        },
        {
          "date": "2025-07-03",
          "value": 143.87
        },
        {
          "date": "2025-07-04",
          "value": 144.41
        },
        {
          "date": "2025-07-07",
          "value": 145.2
        },
        {
          "date": "2025-07-08",
          "value": 146.04
        },
        {
          "date": "2025-07-09",
          "value": 146.85
        },
        {
          "date": "2025-07-10",
          "value": 146.27
        },
        {
          "date": "2025-07-11",
          "value": 146.86
        },
        {
          "date": "2025-07-14",
          "value": 147.38
        },
        {
          "date": "2025-07-15",
          "value": 147.74
        },
        {
          "date": "2025-07-16",
          "value": 148.89
        },
        {
          "date": "2025-07-17",
          "value": 148.73
        },
        {
          "date": "2025-07-18",
          "value": 148.78
        },
        {
          "date": "2025-07-22",
          "value": 147.72
        },
        {
          "date": "2025-07-23",
          "value": 146.74
        },
        {
          "date": "2025-07-24",
          "value": 146.42
        },
        {
          "date": "2025-07-25",
          "value": 147.38
        },
        {
          "date": "2025-07-28",
          "value": 148.29
        },
        {
          "date": "2025-07-29",
          "value": 148.58
        },
        {
          "date": "2025-07-30",
          "value": 148.09
        },
        {
          "date": "2025-07-31",
          "value": 149.39
        },
        {
          "date": "2025-08-01",
          "value": 150.54
        },
        {
          "date": "2025-08-04",
          "value": 147.88
        },
        {
          "date": "2025-08-05",
          "value": 147.37
        },
        {
          "date": "2025-08-06",
          "value": 147.56
        },
        {
          "date": "2025-08-07",
          "value": 146.81
        },
        {
          "date": "2025-08-08",
          "value": 147.32
        },
        {
          "date": "2025-08-12",
          "value": 148.27
        },
        {
          "date": "2025-08-13",
          "value": 147.53
        },
        {
          "date": "2025-08-14",
          "value": 146.56
        },
        {
          "date": "2025-08-15",
          "value": 147.01
        },
        {
          "date": "2025-08-18",
          "value": 147.46
        },
        {
          "date": "2025-08-19",
          "value": 147.71
        },
        {
          "date": "2025-08-20",
          "value": 147.63
        },
        {
          "date": "2025-08-21",
          "value": 147.59
        },
        {
          "date": "2025-08-22",
          "value": 148.61
        },
        {
          "date": "2025-08-25",
          "value": 147.34
        },
        {
          "date": "2025-08-26",
          "value": 147.69
        },
        {
          "date": "2025-08-27",
          "value": 147.76
        },
        {
          "date": "2025-08-28",
          "value": 147.17
        },
        {
          "date": "2025-08-29",
          "value": 147.01
        },
        {
          "date": "2025-09-01",
          "value": 147.07
        },
        {
          "date": "2025-09-02",
          "value": 148.65
        },
        {
          "date": "2025-09-03",
          "value": 148.74
        },
        {
          "date": "2025-09-04",
          "value": 148.38
        },
        {
          "date": "2025-09-05",
          "value": 148.22
        },
        {
          "date": "2025-09-08",
          "value": 147.53
        },
        {
          "date": "2025-09-09",
          "value": 147.23
        },
        {
          "date": "2025-09-10",
          "value": 147.51
        },
        {
          "date": "2025-09-11",
          "value": 147.78
        },
        {
          "date": "2025-09-12",
          "value": 147.46
        },
        {
          "date": "2025-09-16",
          "value": 146.89
        },
        {
          "date": "2025-09-17",
          "value": 146.67
        },
        {
          "date": "2025-09-18",
          "value": 147.12
        },
        {
          "date": "2025-09-19",
          "value": 147.94
        },
        {
          "date": "2025-09-22",
          "value": 148.12
        },
        {
          "date": "2025-09-24",
          "value": 148.05
        },
        {
          "date": "2025-09-25",
          "value": 148.82
        },
        {
          "date": "2025-09-26",
          "value": 149.84
        },
        {
          "date": "2025-09-29",
          "value": 148.57
        },
        {
          "date": "2025-09-30",
          "value": 148.07
        },
        {
          "date": "2025-10-01",
          "value": 147.12
        },
        {
          "date": "2025-10-02",
          "value": 147.08
        },
        {
          "date": "2025-10-03",
          "value": 147.41
        },
        {
          "date": "2025-10-06",
          "value": 150.02
        },
        {
          "date": "2025-10-07",
          "value": 150.63
        },
        {
          "date": "2025-10-08",
          "value": 152.57
        },
        {
          "date": "2025-10-09",
          "value": 153.07
        },
        {
          "date": "2025-10-10",
          "value": 152.85
        },
        {
          "date": "2025-10-14",
          "value": 151.97
        },
        {
          "date": "2025-10-15",
          "value": 151.25
        },
        {
          "date": "2025-10-16",
          "value": 151.24
        },
        {
          "date": "2025-10-17",
          "value": 149.71
        },
        {
          "date": "2025-10-20",
          "value": 150.75
        },
        {
          "date": "2025-10-21",
          "value": 151.16
        },
        {
          "date": "2025-10-22",
          "value": 151.83
        },
        {
          "date": "2025-10-23",
          "value": 152.5
        },
        {
          "date": "2025-10-24",
          "value": 152.83
        },
        {
          "date": "2025-10-27",
          "value": 153.03
        },
        {
          "date": "2025-10-28",
          "value": 152.16
        },
        {
          "date": "2025-10-29",
          "value": 152.06
        },
        {
          "date": "2025-10-30",
          "value": 153.44
        },
        {
          "date": "2025-10-31",
          "value": 154.31
        },
        {
          "date": "2025-11-04",
          "value": 153.59
        },
        {
          "date": "2025-11-05",
          "value": 153.55
        },
        {
          "date": "2025-11-06",
          "value": 153.87
        },
        {
          "date": "2025-11-07",
          "value": 153.39
        },
        {
          "date": "2025-11-10",
          "value": 154.05
        },
        {
          "date": "2025-11-11",
          "value": 154.19
        },
        {
          "date": "2025-11-12",
          "value": 154.62
        },
        {
          "date": "2025-11-13",
          "value": 154.72
        },
        {
          "date": "2025-11-14",
          "value": 154.68
        },
        {
          "date": "2025-11-17",
          "value": 154.68
        },
        {
          "date": "2025-11-18",
          "value": 155.0
        },
        {
          "date": "2025-11-19",
          "value": 155.52
        },
        {
          "date": "2025-11-20",
          "value": 157.46
        },
        {
          "date": "2025-11-21",
          "value": 156.74
        },
        {
          "date": "2025-11-25",
          "value": 156.63
        },
        {
          "date": "2025-11-26",
          "value": 156.38
        },
        {
          "date": "2025-11-27",
          "value": 156.11
        },
        {
          "date": "2025-11-28",
          "value": 156.32
        },
        {
          "date": "2025-12-01",
          "value": 155.38
        },
        {
          "date": "2025-12-02",
          "value": 155.77
        },
        {
          "date": "2025-12-03",
          "value": 155.69
        },
        {
          "date": "2025-12-04",
          "value": 155.25
        },
        {
          "date": "2025-12-05",
          "value": 154.63
        },
        {
          "date": "2025-12-08",
          "value": 155.36
        },
        {
          "date": "2025-12-09",
          "value": 156.2
        },
        {
          "date": "2025-12-10",
          "value": 156.66
        },
        {
          "date": "2025-12-11",
          "value": 156.05
        },
        {
          "date": "2025-12-12",
          "value": 155.65
        },
        {
          "date": "2025-12-15",
          "value": 155.26
        },
        {
          "date": "2025-12-16",
          "value": 154.89
        },
        {
          "date": "2025-12-17",
          "value": 155.5
        },
        {
          "date": "2025-12-18",
          "value": 155.93
        },
        {
          "date": "2025-12-19",
          "value": 156.74
        },
        {
          "date": "2025-12-22",
          "value": 157.49
        },
        {
          "date": "2025-12-23",
          "value": 156.08
        },
        {
          "date": "2025-12-24",
          "value": 155.83
        },
        {
          "date": "2025-12-25",
          "value": 156.0
        },
        {
          "date": "2025-12-26",
          "value": 156.37
        },
        {
          "date": "2025-12-29",
          "value": 156.08
        },
        {
          "date": "2025-12-30",
          "value": 155.98
        },
        {
          "date": "2026-01-05",
          "value": 156.98
        },
        {
          "date": "2026-01-06",
          "value": 156.33
        },
        {
          "date": "2026-01-07",
          "value": 156.49
        },
        {
          "date": "2026-01-08",
          "value": 156.47
        },
        {
          "date": "2026-01-09",
          "value": 157.49
        },
        {
          "date": "2026-01-13",
          "value": 158.95
        },
        {
          "date": "2026-01-14",
          "value": 159.18
        },
        {
          "date": "2026-01-15",
          "value": 158.59
        },
        {
          "date": "2026-01-16",
          "value": 158.17
        },
        {
          "date": "2026-01-19",
          "value": 158.07
        },
        {
          "date": "2026-01-20",
          "value": 158.37
        },
        {
          "date": "2026-01-21",
          "value": 157.92
        },
        {
          "date": "2026-01-22",
          "value": 158.78
        },
        {
          "date": "2026-01-23",
          "value": 158.39
        },
        {
          "date": "2026-01-26",
          "value": 154.26
        },
        {
          "date": "2026-01-27",
          "value": 154.72
        },
        {
          "date": "2026-01-28",
          "value": 152.64
        },
        {
          "date": "2026-01-29",
          "value": 153.33
        },
        {
          "date": "2026-01-30",
          "value": 153.8
        },
        {
          "date": "2026-02-02",
          "value": 154.89
        },
        {
          "date": "2026-02-03",
          "value": 155.41
        },
        {
          "date": "2026-02-04",
          "value": 156.43
        },
        {
          "date": "2026-02-05",
          "value": 157.12
        },
        {
          "date": "2026-02-06",
          "value": 156.89
        },
        {
          "date": "2026-02-09",
          "value": 156.6
        },
        {
          "date": "2026-02-10",
          "value": 155.57
        },
        {
          "date": "2026-02-12",
          "value": 153.01
        },
        {
          "date": "2026-02-13",
          "value": 153.4
        },
        {
          "date": "2026-02-16",
          "value": 153.35
        },
        {
          "date": "2026-02-17",
          "value": 153.09
        },
        {
          "date": "2026-02-18",
          "value": 153.68
        },
        {
          "date": "2026-02-19",
          "value": 154.97
        },
        {
          "date": "2026-02-20",
          "value": 155.5
        },
        {
          "date": "2026-02-24",
          "value": 156.11
        },
        {
          "date": "2026-02-25",
          "value": 155.92
        },
        {
          "date": "2026-02-26",
          "value": 156.04
        },
        {
          "date": "2026-02-27",
          "value": 156.09
        },
        {
          "date": "2026-03-02",
          "value": 156.99
        },
        {
          "date": "2026-03-03",
          "value": 157.42
        },
        {
          "date": "2026-03-04",
          "value": 157.46
        },
        {
          "date": "2026-03-05",
          "value": 157.26
        },
        {
          "date": "2026-03-06",
          "value": 157.54
        },
        {
          "date": "2026-03-09",
          "value": 158.46
        },
        {
          "date": "2026-03-10",
          "value": 157.32
        },
        {
          "date": "2026-03-11",
          "value": 158.23
        },
        {
          "date": "2026-03-12",
          "value": 158.8
        },
        {
          "date": "2026-03-13",
          "value": 159.43
        },
        {
          "date": "2026-03-16",
          "value": 159.29
        },
        {
          "date": "2026-03-17",
          "value": 159.23
        },
        {
          "date": "2026-03-18",
          "value": 158.77
        },
        {
          "date": "2026-03-19",
          "value": 159.22
        },
        {
          "date": "2026-03-23",
          "value": 159.59
        },
        {
          "date": "2026-03-24",
          "value": 158.5
        },
        {
          "date": "2026-03-25",
          "value": 159.14
        },
        {
          "date": "2026-03-26",
          "value": 159.5
        },
        {
          "date": "2026-03-27",
          "value": 159.95
        },
        {
          "date": "2026-03-30",
          "value": 159.78
        },
        {
          "date": "2026-03-31",
          "value": 159.63
        },
        {
          "date": "2026-04-01",
          "value": 158.8
        },
        {
          "date": "2026-04-02",
          "value": 159.57
        },
        {
          "date": "2026-04-03",
          "value": 159.6
        },
        {
          "date": "2026-04-06",
          "value": 159.38
        },
        {
          "date": "2026-04-07",
          "value": 159.87
        },
        {
          "date": "2026-04-08",
          "value": 158.21
        },
        {
          "date": "2026-04-09",
          "value": 158.97
        },
        {
          "date": "2026-04-10",
          "value": 159.35
        },
        {
          "date": "2026-04-13",
          "value": 159.61
        },
        {
          "date": "2026-04-14",
          "value": 159.07
        },
        {
          "date": "2026-04-15",
          "value": 158.94
        },
        {
          "date": "2026-04-16",
          "value": 158.87
        },
        {
          "date": "2026-04-17",
          "value": 159.27
        },
        {
          "date": "2026-04-20",
          "value": 158.97
        },
        {
          "date": "2026-04-21",
          "value": 159.02
        },
        {
          "date": "2026-04-22",
          "value": 159.22
        },
        {
          "date": "2026-04-23",
          "value": 159.6
        },
        {
          "date": "2026-04-24",
          "value": 159.68
        },
        {
          "date": "2026-04-27",
          "value": 159.24
        },
        {
          "date": "2026-04-28",
          "value": 159.53
        },
        {
          "date": "2026-04-30",
          "value": 160.14
        },
        {
          "date": "2026-05-01",
          "value": 156.62
        },
        {
          "date": "2026-05-07",
          "value": 156.27
        },
        {
          "date": "2026-05-08",
          "value": 156.84
        },
        {
          "date": "2026-05-11",
          "value": 157.12
        },
        {
          "date": "2026-05-12",
          "value": 157.51
        },
        {
          "date": "2026-05-13",
          "value": 157.85
        },
        {
          "date": "2026-05-14",
          "value": 157.93
        },
        {
          "date": "2026-05-15",
          "value": 158.45
        },
        {
          "date": "2026-05-18",
          "value": 158.93
        },
        {
          "date": "2026-05-19",
          "value": 159.04
        },
        {
          "date": "2026-05-20",
          "value": 159.07
        },
        {
          "date": "2026-05-21",
          "value": 159.03
        },
        {
          "date": "2026-05-22",
          "value": 159.13
        },
        {
          "date": "2026-05-25",
          "value": 158.97
        },
        {
          "date": "2026-05-26",
          "value": 159.2
        },
        {
          "date": "2026-05-27",
          "value": 159.36
        },
        {
          "date": "2026-05-28",
          "value": 159.47
        },
        {
          "date": "2026-05-29",
          "value": 159.27
        },
        {
          "date": "2026-06-01",
          "value": 159.47
        },
        {
          "date": "2026-06-02",
          "value": 159.69
        },
        {
          "date": "2026-06-03",
          "value": 159.71
        },
        {
          "date": "2026-06-04",
          "value": 159.9
        },
        {
          "date": "2026-06-05",
          "value": 159.95
        },
        {
          "date": "2026-06-08",
          "value": 160.23
        },
        {
          "date": "2026-06-09",
          "value": 160.2
        },
        {
          "date": "2026-06-10",
          "value": 160.39
        },
        {
          "date": "2026-06-11",
          "value": 160.51
        },
        {
          "date": "2026-06-12",
          "value": 160.28
        },
        {
          "date": "2026-06-15",
          "value": 160.13
        },
        {
          "date": "2026-06-16",
          "value": 160.23
        },
        {
          "date": "2026-06-17",
          "value": 160.19
        },
        {
          "date": "2026-06-18",
          "value": 160.6
        },
        {
          "date": "2026-06-19",
          "value": 161.32
        },
        {
          "date": "2026-06-22",
          "value": 161.74
        },
        {
          "date": "2026-06-23",
          "value": 161.48
        },
        {
          "date": "2026-06-24",
          "value": 161.72
        },
        {
          "date": "2026-06-25",
          "value": 161.82
        },
        {
          "date": "2026-06-26",
          "value": 161.63
        },
        {
          "date": "2026-06-29",
          "value": 161.83
        },
        {
          "date": "2026-06-30",
          "value": 162.26
        },
        {
          "date": "2026-07-01",
          "value": 162.68
        },
        {
          "date": "2026-07-02",
          "value": 161.44
        },
        {
          "date": "2026-07-03",
          "value": 160.78
        },
        {
          "date": "2026-07-06",
          "value": 162.17
        },
        {
          "date": "2026-07-07",
          "value": 161.97
        }
      ],
      "JPY_CALL": [
        {
          "date": "2025-06-13",
          "value": 0.477
        },
        {
          "date": "2025-06-16",
          "value": 0.477
        },
        {
          "date": "2025-06-17",
          "value": 0.477
        },
        {
          "date": "2025-06-18",
          "value": 0.478
        },
        {
          "date": "2025-06-19",
          "value": 0.477
        },
        {
          "date": "2025-06-20",
          "value": 0.477
        },
        {
          "date": "2025-06-23",
          "value": 0.476
        },
        {
          "date": "2025-06-24",
          "value": 0.478
        },
        {
          "date": "2025-06-25",
          "value": 0.478
        },
        {
          "date": "2025-06-26",
          "value": 0.478
        },
        {
          "date": "2025-06-27",
          "value": 0.477
        },
        {
          "date": "2025-06-30",
          "value": 0.477
        },
        {
          "date": "2025-07-01",
          "value": 0.477
        },
        {
          "date": "2025-07-02",
          "value": 0.477
        },
        {
          "date": "2025-07-03",
          "value": 0.477
        },
        {
          "date": "2025-07-04",
          "value": 0.477
        },
        {
          "date": "2025-07-07",
          "value": 0.477
        },
        {
          "date": "2025-07-08",
          "value": 0.477
        },
        {
          "date": "2025-07-09",
          "value": 0.477
        },
        {
          "date": "2025-07-10",
          "value": 0.477
        },
        {
          "date": "2025-07-11",
          "value": 0.477
        },
        {
          "date": "2025-07-14",
          "value": 0.479
        },
        {
          "date": "2025-07-15",
          "value": 0.476
        },
        {
          "date": "2025-07-16",
          "value": 0.477
        },
        {
          "date": "2025-07-17",
          "value": 0.477
        },
        {
          "date": "2025-07-18",
          "value": 0.477
        },
        {
          "date": "2025-07-22",
          "value": 0.479
        },
        {
          "date": "2025-07-23",
          "value": 0.478
        },
        {
          "date": "2025-07-24",
          "value": 0.477
        },
        {
          "date": "2025-07-25",
          "value": 0.477
        },
        {
          "date": "2025-07-28",
          "value": 0.479
        },
        {
          "date": "2025-07-29",
          "value": 0.478
        },
        {
          "date": "2025-07-30",
          "value": 0.481
        },
        {
          "date": "2025-07-31",
          "value": 0.478
        },
        {
          "date": "2025-08-01",
          "value": 0.477
        },
        {
          "date": "2025-08-04",
          "value": 0.476
        },
        {
          "date": "2025-08-05",
          "value": 0.477
        },
        {
          "date": "2025-08-06",
          "value": 0.477
        },
        {
          "date": "2025-08-07",
          "value": 0.477
        },
        {
          "date": "2025-08-08",
          "value": 0.477
        },
        {
          "date": "2025-08-12",
          "value": 0.477
        },
        {
          "date": "2025-08-13",
          "value": 0.477
        },
        {
          "date": "2025-08-14",
          "value": 0.477
        },
        {
          "date": "2025-08-15",
          "value": 0.477
        },
        {
          "date": "2025-08-18",
          "value": 0.477
        },
        {
          "date": "2025-08-19",
          "value": 0.477
        },
        {
          "date": "2025-08-20",
          "value": 0.476
        },
        {
          "date": "2025-08-21",
          "value": 0.476
        },
        {
          "date": "2025-08-22",
          "value": 0.476
        },
        {
          "date": "2025-08-25",
          "value": 0.477
        },
        {
          "date": "2025-08-26",
          "value": 0.478
        },
        {
          "date": "2025-08-27",
          "value": 0.478
        },
        {
          "date": "2025-08-28",
          "value": 0.478
        },
        {
          "date": "2025-08-29",
          "value": 0.477
        },
        {
          "date": "2025-09-01",
          "value": 0.477
        },
        {
          "date": "2025-09-02",
          "value": 0.478
        },
        {
          "date": "2025-09-03",
          "value": 0.478
        },
        {
          "date": "2025-09-04",
          "value": 0.479
        },
        {
          "date": "2025-09-05",
          "value": 0.477
        },
        {
          "date": "2025-09-08",
          "value": 0.477
        },
        {
          "date": "2025-09-09",
          "value": 0.477
        },
        {
          "date": "2025-09-10",
          "value": 0.477
        },
        {
          "date": "2025-09-11",
          "value": 0.48
        },
        {
          "date": "2025-09-12",
          "value": 0.477
        },
        {
          "date": "2025-09-16",
          "value": 0.477
        },
        {
          "date": "2025-09-17",
          "value": 0.478
        },
        {
          "date": "2025-09-18",
          "value": 0.477
        },
        {
          "date": "2025-09-19",
          "value": 0.477
        },
        {
          "date": "2025-09-22",
          "value": 0.476
        },
        {
          "date": "2025-09-24",
          "value": 0.478
        },
        {
          "date": "2025-09-25",
          "value": 0.477
        },
        {
          "date": "2025-09-26",
          "value": 0.476
        },
        {
          "date": "2025-09-29",
          "value": 0.477
        },
        {
          "date": "2025-09-30",
          "value": 0.477
        },
        {
          "date": "2025-10-01",
          "value": 0.477
        },
        {
          "date": "2025-10-02",
          "value": 0.477
        },
        {
          "date": "2025-10-03",
          "value": 0.477
        },
        {
          "date": "2025-10-06",
          "value": 0.477
        },
        {
          "date": "2025-10-07",
          "value": 0.477
        },
        {
          "date": "2025-10-08",
          "value": 0.477
        },
        {
          "date": "2025-10-09",
          "value": 0.478
        },
        {
          "date": "2025-10-10",
          "value": 0.477
        },
        {
          "date": "2025-10-14",
          "value": 0.477
        },
        {
          "date": "2025-10-15",
          "value": 0.477
        },
        {
          "date": "2025-10-16",
          "value": 0.477
        },
        {
          "date": "2025-10-17",
          "value": 0.477
        },
        {
          "date": "2025-10-20",
          "value": 0.477
        },
        {
          "date": "2025-10-21",
          "value": 0.477
        },
        {
          "date": "2025-10-22",
          "value": 0.477
        },
        {
          "date": "2025-10-23",
          "value": 0.477
        },
        {
          "date": "2025-10-24",
          "value": 0.477
        },
        {
          "date": "2025-10-27",
          "value": 0.477
        },
        {
          "date": "2025-10-28",
          "value": 0.477
        },
        {
          "date": "2025-10-29",
          "value": 0.477
        },
        {
          "date": "2025-10-30",
          "value": 0.476
        },
        {
          "date": "2025-10-31",
          "value": 0.477
        },
        {
          "date": "2025-11-04",
          "value": 0.476
        },
        {
          "date": "2025-11-05",
          "value": 0.477
        },
        {
          "date": "2025-11-06",
          "value": 0.477
        },
        {
          "date": "2025-11-07",
          "value": 0.478
        },
        {
          "date": "2025-11-10",
          "value": 0.481
        },
        {
          "date": "2025-11-11",
          "value": 0.477
        },
        {
          "date": "2025-11-12",
          "value": 0.479
        },
        {
          "date": "2025-11-13",
          "value": 0.477
        },
        {
          "date": "2025-11-14",
          "value": 0.478
        },
        {
          "date": "2025-11-17",
          "value": 0.477
        },
        {
          "date": "2025-11-18",
          "value": 0.478
        },
        {
          "date": "2025-11-19",
          "value": 0.479
        },
        {
          "date": "2025-11-20",
          "value": 0.477
        },
        {
          "date": "2025-11-21",
          "value": 0.478
        },
        {
          "date": "2025-11-25",
          "value": 0.478
        },
        {
          "date": "2025-11-26",
          "value": 0.478
        },
        {
          "date": "2025-11-27",
          "value": 0.477
        },
        {
          "date": "2025-11-28",
          "value": 0.477
        },
        {
          "date": "2025-12-01",
          "value": 0.477
        },
        {
          "date": "2025-12-02",
          "value": 0.477
        },
        {
          "date": "2025-12-03",
          "value": 0.478
        },
        {
          "date": "2025-12-04",
          "value": 0.477
        },
        {
          "date": "2025-12-05",
          "value": 0.477
        },
        {
          "date": "2025-12-08",
          "value": 0.477
        },
        {
          "date": "2025-12-09",
          "value": 0.482
        },
        {
          "date": "2025-12-10",
          "value": 0.477
        },
        {
          "date": "2025-12-11",
          "value": 0.478
        },
        {
          "date": "2025-12-12",
          "value": 0.477
        },
        {
          "date": "2025-12-15",
          "value": 0.477
        },
        {
          "date": "2025-12-16",
          "value": 0.482
        },
        {
          "date": "2025-12-17",
          "value": 0.478
        },
        {
          "date": "2025-12-18",
          "value": 0.477
        },
        {
          "date": "2025-12-19",
          "value": 0.477
        },
        {
          "date": "2025-12-22",
          "value": 0.727
        },
        {
          "date": "2025-12-23",
          "value": 0.727
        },
        {
          "date": "2025-12-24",
          "value": 0.727
        },
        {
          "date": "2025-12-25",
          "value": 0.728
        },
        {
          "date": "2025-12-26",
          "value": 0.727
        },
        {
          "date": "2025-12-29",
          "value": 0.728
        },
        {
          "date": "2025-12-30",
          "value": 0.727
        },
        {
          "date": "2026-01-05",
          "value": 0.727
        },
        {
          "date": "2026-01-06",
          "value": 0.727
        },
        {
          "date": "2026-01-07",
          "value": 0.727
        },
        {
          "date": "2026-01-08",
          "value": 0.729
        },
        {
          "date": "2026-01-09",
          "value": 0.727
        },
        {
          "date": "2026-01-13",
          "value": 0.727
        },
        {
          "date": "2026-01-14",
          "value": 0.727
        },
        {
          "date": "2026-01-15",
          "value": 0.727
        },
        {
          "date": "2026-01-16",
          "value": 0.727
        },
        {
          "date": "2026-01-19",
          "value": 0.727
        },
        {
          "date": "2026-01-20",
          "value": 0.728
        },
        {
          "date": "2026-01-21",
          "value": 0.727
        },
        {
          "date": "2026-01-22",
          "value": 0.727
        },
        {
          "date": "2026-01-23",
          "value": 0.727
        },
        {
          "date": "2026-01-26",
          "value": 0.728
        },
        {
          "date": "2026-01-27",
          "value": 0.736
        },
        {
          "date": "2026-01-28",
          "value": 0.727
        },
        {
          "date": "2026-01-29",
          "value": 0.727
        },
        {
          "date": "2026-01-30",
          "value": 0.727
        },
        {
          "date": "2026-02-02",
          "value": 0.727
        },
        {
          "date": "2026-02-03",
          "value": 0.73
        },
        {
          "date": "2026-02-04",
          "value": 0.727
        },
        {
          "date": "2026-02-05",
          "value": 0.727
        },
        {
          "date": "2026-02-06",
          "value": 0.728
        },
        {
          "date": "2026-02-09",
          "value": 0.728
        },
        {
          "date": "2026-02-10",
          "value": 0.727
        },
        {
          "date": "2026-02-12",
          "value": 0.728
        },
        {
          "date": "2026-02-13",
          "value": 0.728
        },
        {
          "date": "2026-02-16",
          "value": 0.728
        },
        {
          "date": "2026-02-17",
          "value": 0.73
        },
        {
          "date": "2026-02-18",
          "value": 0.728
        },
        {
          "date": "2026-02-19",
          "value": 0.728
        },
        {
          "date": "2026-02-20",
          "value": 0.729
        },
        {
          "date": "2026-02-24",
          "value": 0.727
        },
        {
          "date": "2026-02-25",
          "value": 0.729
        },
        {
          "date": "2026-02-26",
          "value": 0.728
        },
        {
          "date": "2026-02-27",
          "value": 0.727
        },
        {
          "date": "2026-03-02",
          "value": 0.727
        },
        {
          "date": "2026-03-03",
          "value": 0.727
        },
        {
          "date": "2026-03-04",
          "value": 0.73
        },
        {
          "date": "2026-03-05",
          "value": 0.728
        },
        {
          "date": "2026-03-06",
          "value": 0.728
        },
        {
          "date": "2026-03-09",
          "value": 0.727
        },
        {
          "date": "2026-03-10",
          "value": 0.728
        },
        {
          "date": "2026-03-11",
          "value": 0.727
        },
        {
          "date": "2026-03-12",
          "value": 0.734
        },
        {
          "date": "2026-03-13",
          "value": 0.728
        },
        {
          "date": "2026-03-16",
          "value": 0.727
        },
        {
          "date": "2026-03-17",
          "value": 0.727
        },
        {
          "date": "2026-03-18",
          "value": 0.727
        },
        {
          "date": "2026-03-19",
          "value": 0.728
        },
        {
          "date": "2026-03-23",
          "value": 0.727
        },
        {
          "date": "2026-03-24",
          "value": 0.727
        },
        {
          "date": "2026-03-25",
          "value": 0.727
        },
        {
          "date": "2026-03-26",
          "value": 0.727
        },
        {
          "date": "2026-03-27",
          "value": 0.727
        },
        {
          "date": "2026-03-30",
          "value": 0.726
        },
        {
          "date": "2026-03-31",
          "value": 0.727
        },
        {
          "date": "2026-04-01",
          "value": 0.728
        },
        {
          "date": "2026-04-02",
          "value": 0.727
        },
        {
          "date": "2026-04-03",
          "value": 0.728
        },
        {
          "date": "2026-04-06",
          "value": 0.727
        },
        {
          "date": "2026-04-07",
          "value": 0.727
        },
        {
          "date": "2026-04-08",
          "value": 0.727
        },
        {
          "date": "2026-04-09",
          "value": 0.727
        },
        {
          "date": "2026-04-10",
          "value": 0.728
        },
        {
          "date": "2026-04-13",
          "value": 0.726
        },
        {
          "date": "2026-04-14",
          "value": 0.726
        },
        {
          "date": "2026-04-15",
          "value": 0.727
        },
        {
          "date": "2026-04-16",
          "value": 0.727
        },
        {
          "date": "2026-04-17",
          "value": 0.728
        },
        {
          "date": "2026-04-20",
          "value": 0.727
        },
        {
          "date": "2026-04-21",
          "value": 0.727
        },
        {
          "date": "2026-04-22",
          "value": 0.727
        },
        {
          "date": "2026-04-23",
          "value": 0.727
        },
        {
          "date": "2026-04-24",
          "value": 0.728
        },
        {
          "date": "2026-04-27",
          "value": 0.727
        },
        {
          "date": "2026-04-28",
          "value": 0.727
        },
        {
          "date": "2026-04-30",
          "value": 0.727
        },
        {
          "date": "2026-05-01",
          "value": 0.727
        },
        {
          "date": "2026-05-07",
          "value": 0.727
        },
        {
          "date": "2026-05-08",
          "value": 0.727
        },
        {
          "date": "2026-05-11",
          "value": 0.726
        },
        {
          "date": "2026-05-12",
          "value": 0.727
        },
        {
          "date": "2026-05-13",
          "value": 0.727
        },
        {
          "date": "2026-05-14",
          "value": 0.727
        },
        {
          "date": "2026-05-15",
          "value": 0.727
        },
        {
          "date": "2026-05-18",
          "value": 0.728
        },
        {
          "date": "2026-05-19",
          "value": 0.728
        },
        {
          "date": "2026-05-20",
          "value": 0.728
        },
        {
          "date": "2026-05-21",
          "value": 0.727
        },
        {
          "date": "2026-05-22",
          "value": 0.726
        },
        {
          "date": "2026-05-25",
          "value": 0.727
        },
        {
          "date": "2026-05-26",
          "value": 0.727
        },
        {
          "date": "2026-05-27",
          "value": 0.727
        },
        {
          "date": "2026-05-28",
          "value": 0.727
        },
        {
          "date": "2026-05-29",
          "value": 0.727
        },
        {
          "date": "2026-06-01",
          "value": 0.726
        },
        {
          "date": "2026-06-02",
          "value": 0.727
        },
        {
          "date": "2026-06-03",
          "value": 0.727
        },
        {
          "date": "2026-06-04",
          "value": 0.726
        },
        {
          "date": "2026-06-05",
          "value": 0.727
        },
        {
          "date": "2026-06-08",
          "value": 0.727
        },
        {
          "date": "2026-06-09",
          "value": 0.727
        },
        {
          "date": "2026-06-10",
          "value": 0.727
        },
        {
          "date": "2026-06-11",
          "value": 0.727
        },
        {
          "date": "2026-06-12",
          "value": 0.727
        },
        {
          "date": "2026-06-15",
          "value": 0.727
        },
        {
          "date": "2026-06-16",
          "value": 0.727
        },
        {
          "date": "2026-06-17",
          "value": 0.978
        },
        {
          "date": "2026-06-18",
          "value": 0.977
        },
        {
          "date": "2026-06-19",
          "value": 0.977
        },
        {
          "date": "2026-06-22",
          "value": 0.977
        },
        {
          "date": "2026-06-23",
          "value": 0.976
        },
        {
          "date": "2026-06-24",
          "value": 0.977
        },
        {
          "date": "2026-06-25",
          "value": 0.978
        },
        {
          "date": "2026-06-26",
          "value": 0.977
        },
        {
          "date": "2026-06-29",
          "value": 0.978
        },
        {
          "date": "2026-06-30",
          "value": 0.976
        },
        {
          "date": "2026-07-01",
          "value": 0.977
        },
        {
          "date": "2026-07-02",
          "value": 0.977
        },
        {
          "date": "2026-07-03",
          "value": 0.977
        },
        {
          "date": "2026-07-06",
          "value": 0.977
        },
        {
          "date": "2026-07-07",
          "value": 0.978
        }
      ],
      "JGB10": [
        {
          "date": "2025-06-06",
          "value": 1.477
        },
        {
          "date": "2025-06-09",
          "value": 1.491
        },
        {
          "date": "2025-06-10",
          "value": 1.498
        },
        {
          "date": "2025-06-11",
          "value": 1.48
        },
        {
          "date": "2025-06-12",
          "value": 1.48
        },
        {
          "date": "2025-06-13",
          "value": 1.429
        },
        {
          "date": "2025-06-16",
          "value": 1.477
        },
        {
          "date": "2025-06-17",
          "value": 1.498
        },
        {
          "date": "2025-06-18",
          "value": 1.479
        },
        {
          "date": "2025-06-19",
          "value": 1.439
        },
        {
          "date": "2025-06-20",
          "value": 1.424
        },
        {
          "date": "2025-06-23",
          "value": 1.437
        },
        {
          "date": "2025-06-24",
          "value": 1.445
        },
        {
          "date": "2025-06-25",
          "value": 1.426
        },
        {
          "date": "2025-06-26",
          "value": 1.445
        },
        {
          "date": "2025-06-27",
          "value": 1.459
        },
        {
          "date": "2025-06-30",
          "value": 1.462
        },
        {
          "date": "2025-07-01",
          "value": 1.419
        },
        {
          "date": "2025-07-02",
          "value": 1.434
        },
        {
          "date": "2025-07-03",
          "value": 1.448
        },
        {
          "date": "2025-07-04",
          "value": 1.444
        },
        {
          "date": "2025-07-07",
          "value": 1.463
        },
        {
          "date": "2025-07-08",
          "value": 1.492
        },
        {
          "date": "2025-07-09",
          "value": 1.507
        },
        {
          "date": "2025-07-10",
          "value": 1.498
        },
        {
          "date": "2025-07-11",
          "value": 1.507
        },
        {
          "date": "2025-07-14",
          "value": 1.574
        },
        {
          "date": "2025-07-15",
          "value": 1.588
        },
        {
          "date": "2025-07-16",
          "value": 1.575
        },
        {
          "date": "2025-07-17",
          "value": 1.561
        },
        {
          "date": "2025-07-18",
          "value": 1.528
        },
        {
          "date": "2025-07-22",
          "value": 1.51
        },
        {
          "date": "2025-07-23",
          "value": 1.596
        },
        {
          "date": "2025-07-24",
          "value": 1.605
        },
        {
          "date": "2025-07-25",
          "value": 1.605
        },
        {
          "date": "2025-07-28",
          "value": 1.571
        },
        {
          "date": "2025-07-29",
          "value": 1.564
        },
        {
          "date": "2025-07-30",
          "value": 1.565
        },
        {
          "date": "2025-07-31",
          "value": 1.559
        },
        {
          "date": "2025-08-01",
          "value": 1.56
        },
        {
          "date": "2025-08-04",
          "value": 1.52
        },
        {
          "date": "2025-08-05",
          "value": 1.487
        },
        {
          "date": "2025-08-06",
          "value": 1.509
        },
        {
          "date": "2025-08-07",
          "value": 1.5
        },
        {
          "date": "2025-08-08",
          "value": 1.502
        },
        {
          "date": "2025-08-12",
          "value": 1.516
        },
        {
          "date": "2025-08-13",
          "value": 1.53
        },
        {
          "date": "2025-08-14",
          "value": 1.563
        },
        {
          "date": "2025-08-15",
          "value": 1.574
        },
        {
          "date": "2025-08-18",
          "value": 1.584
        },
        {
          "date": "2025-08-19",
          "value": 1.603
        },
        {
          "date": "2025-08-20",
          "value": 1.617
        },
        {
          "date": "2025-08-21",
          "value": 1.617
        },
        {
          "date": "2025-08-22",
          "value": 1.626
        },
        {
          "date": "2025-08-25",
          "value": 1.628
        },
        {
          "date": "2025-08-26",
          "value": 1.631
        },
        {
          "date": "2025-08-27",
          "value": 1.637
        },
        {
          "date": "2025-08-28",
          "value": 1.628
        },
        {
          "date": "2025-08-29",
          "value": 1.613
        },
        {
          "date": "2025-09-01",
          "value": 1.633
        },
        {
          "date": "2025-09-02",
          "value": 1.615
        },
        {
          "date": "2025-09-03",
          "value": 1.643
        },
        {
          "date": "2025-09-04",
          "value": 1.617
        },
        {
          "date": "2025-09-05",
          "value": 1.59
        },
        {
          "date": "2025-09-08",
          "value": 1.586
        },
        {
          "date": "2025-09-09",
          "value": 1.58
        },
        {
          "date": "2025-09-10",
          "value": 1.585
        },
        {
          "date": "2025-09-11",
          "value": 1.594
        },
        {
          "date": "2025-09-12",
          "value": 1.613
        },
        {
          "date": "2025-09-16",
          "value": 1.623
        },
        {
          "date": "2025-09-17",
          "value": 1.611
        },
        {
          "date": "2025-09-18",
          "value": 1.615
        },
        {
          "date": "2025-09-19",
          "value": 1.655
        },
        {
          "date": "2025-09-22",
          "value": 1.669
        },
        {
          "date": "2025-09-24",
          "value": 1.655
        },
        {
          "date": "2025-09-25",
          "value": 1.659
        },
        {
          "date": "2025-09-26",
          "value": 1.669
        },
        {
          "date": "2025-09-29",
          "value": 1.657
        },
        {
          "date": "2025-09-30",
          "value": 1.662
        },
        {
          "date": "2025-10-01",
          "value": 1.663
        },
        {
          "date": "2025-10-02",
          "value": 1.675
        },
        {
          "date": "2025-10-03",
          "value": 1.667
        },
        {
          "date": "2025-10-06",
          "value": 1.677
        },
        {
          "date": "2025-10-07",
          "value": 1.682
        },
        {
          "date": "2025-10-08",
          "value": 1.701
        },
        {
          "date": "2025-10-09",
          "value": 1.697
        },
        {
          "date": "2025-10-10",
          "value": 1.697
        },
        {
          "date": "2025-10-14",
          "value": 1.67
        },
        {
          "date": "2025-10-15",
          "value": 1.662
        },
        {
          "date": "2025-10-16",
          "value": 1.663
        },
        {
          "date": "2025-10-17",
          "value": 1.638
        },
        {
          "date": "2025-10-20",
          "value": 1.676
        },
        {
          "date": "2025-10-21",
          "value": 1.667
        },
        {
          "date": "2025-10-22",
          "value": 1.663
        },
        {
          "date": "2025-10-23",
          "value": 1.667
        },
        {
          "date": "2025-10-24",
          "value": 1.667
        },
        {
          "date": "2025-10-27",
          "value": 1.683
        },
        {
          "date": "2025-10-28",
          "value": 1.654
        },
        {
          "date": "2025-10-29",
          "value": 1.664
        },
        {
          "date": "2025-10-30",
          "value": 1.66
        },
        {
          "date": "2025-10-31",
          "value": 1.67
        },
        {
          "date": "2025-11-04",
          "value": 1.684
        },
        {
          "date": "2025-11-05",
          "value": 1.676
        },
        {
          "date": "2025-11-06",
          "value": 1.694
        },
        {
          "date": "2025-11-07",
          "value": 1.688
        },
        {
          "date": "2025-11-10",
          "value": 1.712
        },
        {
          "date": "2025-11-11",
          "value": 1.704
        },
        {
          "date": "2025-11-12",
          "value": 1.7
        },
        {
          "date": "2025-11-13",
          "value": 1.705
        },
        {
          "date": "2025-11-14",
          "value": 1.714
        },
        {
          "date": "2025-11-17",
          "value": 1.745
        },
        {
          "date": "2025-11-18",
          "value": 1.759
        },
        {
          "date": "2025-11-19",
          "value": 1.779
        },
        {
          "date": "2025-11-20",
          "value": 1.824
        },
        {
          "date": "2025-11-21",
          "value": 1.792
        },
        {
          "date": "2025-11-25",
          "value": 1.811
        },
        {
          "date": "2025-11-26",
          "value": 1.825
        },
        {
          "date": "2025-11-27",
          "value": 1.807
        },
        {
          "date": "2025-11-28",
          "value": 1.812
        },
        {
          "date": "2025-12-01",
          "value": 1.881
        },
        {
          "date": "2025-12-02",
          "value": 1.864
        },
        {
          "date": "2025-12-03",
          "value": 1.897
        },
        {
          "date": "2025-12-04",
          "value": 1.939
        },
        {
          "date": "2025-12-05",
          "value": 1.951
        },
        {
          "date": "2025-12-08",
          "value": 1.966
        },
        {
          "date": "2025-12-09",
          "value": 1.962
        },
        {
          "date": "2025-12-10",
          "value": 1.958
        },
        {
          "date": "2025-12-11",
          "value": 1.933
        },
        {
          "date": "2025-12-12",
          "value": 1.956
        },
        {
          "date": "2025-12-15",
          "value": 1.961
        },
        {
          "date": "2025-12-16",
          "value": 1.957
        },
        {
          "date": "2025-12-17",
          "value": 1.98
        },
        {
          "date": "2025-12-18",
          "value": 1.972
        },
        {
          "date": "2025-12-19",
          "value": 2.021
        },
        {
          "date": "2025-12-22",
          "value": 2.073
        },
        {
          "date": "2025-12-23",
          "value": 2.039
        },
        {
          "date": "2025-12-24",
          "value": 2.044
        },
        {
          "date": "2025-12-25",
          "value": 2.042
        },
        {
          "date": "2025-12-26",
          "value": 2.039
        },
        {
          "date": "2025-12-29",
          "value": 2.052
        },
        {
          "date": "2025-12-30",
          "value": 2.066
        },
        {
          "date": "2026-01-05",
          "value": 2.111
        },
        {
          "date": "2026-01-06",
          "value": 2.123
        },
        {
          "date": "2026-01-07",
          "value": 2.124
        },
        {
          "date": "2026-01-08",
          "value": 2.083
        },
        {
          "date": "2026-01-09",
          "value": 2.096
        },
        {
          "date": "2026-01-13",
          "value": 2.163
        },
        {
          "date": "2026-01-14",
          "value": 2.182
        },
        {
          "date": "2026-01-15",
          "value": 2.164
        },
        {
          "date": "2026-01-16",
          "value": 2.182
        },
        {
          "date": "2026-01-19",
          "value": 2.266
        },
        {
          "date": "2026-01-20",
          "value": 2.33
        },
        {
          "date": "2026-01-21",
          "value": 2.28
        },
        {
          "date": "2026-01-22",
          "value": 2.239
        },
        {
          "date": "2026-01-23",
          "value": 2.253
        },
        {
          "date": "2026-01-26",
          "value": 2.236
        },
        {
          "date": "2026-01-27",
          "value": 2.281
        },
        {
          "date": "2026-01-28",
          "value": 2.237
        },
        {
          "date": "2026-01-29",
          "value": 2.252
        },
        {
          "date": "2026-01-30",
          "value": 2.247
        },
        {
          "date": "2026-02-02",
          "value": 2.235
        },
        {
          "date": "2026-02-03",
          "value": 2.258
        },
        {
          "date": "2026-02-04",
          "value": 2.249
        },
        {
          "date": "2026-02-05",
          "value": 2.231
        },
        {
          "date": "2026-02-06",
          "value": 2.236
        },
        {
          "date": "2026-02-09",
          "value": 2.289
        },
        {
          "date": "2026-02-10",
          "value": 2.241
        },
        {
          "date": "2026-02-12",
          "value": 2.238
        },
        {
          "date": "2026-02-13",
          "value": 2.218
        },
        {
          "date": "2026-02-16",
          "value": 2.22
        },
        {
          "date": "2026-02-17",
          "value": 2.143
        },
        {
          "date": "2026-02-18",
          "value": 2.152
        },
        {
          "date": "2026-02-19",
          "value": 2.157
        },
        {
          "date": "2026-02-20",
          "value": 2.125
        },
        {
          "date": "2026-02-24",
          "value": 2.119
        },
        {
          "date": "2026-02-25",
          "value": 2.154
        },
        {
          "date": "2026-02-26",
          "value": 2.168
        },
        {
          "date": "2026-02-27",
          "value": 2.132
        },
        {
          "date": "2026-03-02",
          "value": 2.087
        },
        {
          "date": "2026-03-03",
          "value": 2.148
        },
        {
          "date": "2026-03-04",
          "value": 2.134
        },
        {
          "date": "2026-03-05",
          "value": 2.175
        },
        {
          "date": "2026-03-06",
          "value": 2.18
        },
        {
          "date": "2026-03-09",
          "value": 2.205
        },
        {
          "date": "2026-03-10",
          "value": 2.199
        },
        {
          "date": "2026-03-11",
          "value": 2.178
        },
        {
          "date": "2026-03-12",
          "value": 2.201
        },
        {
          "date": "2026-03-13",
          "value": 2.255
        },
        {
          "date": "2026-03-16",
          "value": 2.288
        },
        {
          "date": "2026-03-17",
          "value": 2.279
        },
        {
          "date": "2026-03-18",
          "value": 2.231
        },
        {
          "date": "2026-03-19",
          "value": 2.273
        },
        {
          "date": "2026-03-23",
          "value": 2.322
        },
        {
          "date": "2026-03-24",
          "value": 2.282
        },
        {
          "date": "2026-03-25",
          "value": 2.267
        },
        {
          "date": "2026-03-26",
          "value": 2.286
        },
        {
          "date": "2026-03-27",
          "value": 2.38
        },
        {
          "date": "2026-03-30",
          "value": 2.368
        },
        {
          "date": "2026-03-31",
          "value": 2.366
        },
        {
          "date": "2026-04-01",
          "value": 2.315
        },
        {
          "date": "2026-04-02",
          "value": 2.395
        },
        {
          "date": "2026-04-03",
          "value": 2.386
        },
        {
          "date": "2026-04-06",
          "value": 2.429
        },
        {
          "date": "2026-04-07",
          "value": 2.411
        },
        {
          "date": "2026-04-08",
          "value": 2.374
        },
        {
          "date": "2026-04-09",
          "value": 2.397
        },
        {
          "date": "2026-04-10",
          "value": 2.439
        },
        {
          "date": "2026-04-13",
          "value": 2.467
        },
        {
          "date": "2026-04-14",
          "value": 2.423
        },
        {
          "date": "2026-04-15",
          "value": 2.414
        },
        {
          "date": "2026-04-16",
          "value": 2.409
        },
        {
          "date": "2026-04-17",
          "value": 2.428
        },
        {
          "date": "2026-04-20",
          "value": 2.405
        },
        {
          "date": "2026-04-21",
          "value": 2.392
        },
        {
          "date": "2026-04-22",
          "value": 2.406
        },
        {
          "date": "2026-04-23",
          "value": 2.429
        },
        {
          "date": "2026-04-24",
          "value": 2.443
        },
        {
          "date": "2026-04-27",
          "value": 2.477
        },
        {
          "date": "2026-04-28",
          "value": 2.468
        },
        {
          "date": "2026-04-30",
          "value": 2.52
        },
        {
          "date": "2026-05-01",
          "value": 2.507
        },
        {
          "date": "2026-05-07",
          "value": 2.485
        },
        {
          "date": "2026-05-08",
          "value": 2.485
        },
        {
          "date": "2026-05-11",
          "value": 2.527
        },
        {
          "date": "2026-05-12",
          "value": 2.546
        },
        {
          "date": "2026-05-13",
          "value": 2.587
        },
        {
          "date": "2026-05-14",
          "value": 2.628
        },
        {
          "date": "2026-05-15",
          "value": 2.691
        },
        {
          "date": "2026-05-18",
          "value": 2.729
        },
        {
          "date": "2026-05-19",
          "value": 2.783
        },
        {
          "date": "2026-05-20",
          "value": 2.77
        },
        {
          "date": "2026-05-21",
          "value": 2.748
        },
        {
          "date": "2026-05-22",
          "value": 2.749
        },
        {
          "date": "2026-05-25",
          "value": 2.686
        },
        {
          "date": "2026-05-26",
          "value": 2.713
        },
        {
          "date": "2026-05-27",
          "value": 2.687
        },
        {
          "date": "2026-05-28",
          "value": 2.692
        },
        {
          "date": "2026-05-29",
          "value": 2.657
        },
        {
          "date": "2026-06-01",
          "value": 2.682
        },
        {
          "date": "2026-06-02",
          "value": 2.577
        },
        {
          "date": "2026-06-03",
          "value": 2.645
        },
        {
          "date": "2026-06-04",
          "value": 2.671
        },
        {
          "date": "2026-06-05",
          "value": 2.669
        },
        {
          "date": "2026-06-08",
          "value": 2.715
        },
        {
          "date": "2026-06-09",
          "value": 2.669
        },
        {
          "date": "2026-06-10",
          "value": 2.681
        },
        {
          "date": "2026-06-11",
          "value": 2.682
        },
        {
          "date": "2026-06-12",
          "value": 2.643
        },
        {
          "date": "2026-06-15",
          "value": 2.589
        },
        {
          "date": "2026-06-16",
          "value": 2.655
        },
        {
          "date": "2026-06-17",
          "value": 2.613
        },
        {
          "date": "2026-06-18",
          "value": 2.628
        },
        {
          "date": "2026-06-19",
          "value": 2.656
        },
        {
          "date": "2026-06-22",
          "value": 2.677
        },
        {
          "date": "2026-06-23",
          "value": 2.683
        },
        {
          "date": "2026-06-24",
          "value": 2.674
        },
        {
          "date": "2026-06-25",
          "value": 2.637
        },
        {
          "date": "2026-06-26",
          "value": 2.611
        },
        {
          "date": "2026-06-29",
          "value": 2.644
        },
        {
          "date": "2026-06-30",
          "value": 2.69
        }
      ],
      "US_JP_10Y": [
        {
          "date": "2025-04-14",
          "value": 303.0
        },
        {
          "date": "2025-04-15",
          "value": 297.3
        },
        {
          "date": "2025-04-16",
          "value": 298.50000000000006
        },
        {
          "date": "2025-04-17",
          "value": 301.99999999999994
        },
        {
          "date": "2025-04-21",
          "value": 311.8
        },
        {
          "date": "2025-04-22",
          "value": 308.70000000000005
        },
        {
          "date": "2025-04-23",
          "value": 306.00000000000006
        },
        {
          "date": "2025-04-24",
          "value": 299.2
        },
        {
          "date": "2025-04-25",
          "value": 294.3
        },
        {
          "date": "2025-04-28",
          "value": 290.1000000000001
        },
        {
          "date": "2025-04-29",
          "value": 286.1000000000001
        },
        {
          "date": "2025-04-30",
          "value": 284.0
        },
        {
          "date": "2025-05-01",
          "value": 295.90000000000003
        },
        {
          "date": "2025-05-02",
          "value": 304.7
        },
        {
          "date": "2025-05-05",
          "value": 307.70000000000005
        },
        {
          "date": "2025-05-06",
          "value": 301.7
        },
        {
          "date": "2025-05-07",
          "value": 294.2
        },
        {
          "date": "2025-05-08",
          "value": 302.7
        },
        {
          "date": "2025-05-09",
          "value": 300.0
        },
        {
          "date": "2025-05-12",
          "value": 304.5
        },
        {
          "date": "2025-05-13",
          "value": 303.0
        },
        {
          "date": "2025-05-14",
          "value": 306.4
        },
        {
          "date": "2025-05-15",
          "value": 296.1
        },
        {
          "date": "2025-05-16",
          "value": 296.4
        },
        {
          "date": "2025-05-19",
          "value": 296.6
        },
        {
          "date": "2025-05-20",
          "value": 295.0
        },
        {
          "date": "2025-05-21",
          "value": 305.0
        },
        {
          "date": "2025-05-22",
          "value": 296.7
        },
        {
          "date": "2025-05-23",
          "value": 295.09999999999997
        },
        {
          "date": "2025-05-27",
          "value": 295.09999999999997
        },
        {
          "date": "2025-05-28",
          "value": 293.9
        },
        {
          "date": "2025-05-29",
          "value": 289.79999999999995
        },
        {
          "date": "2025-05-30",
          "value": 289.20000000000005
        },
        {
          "date": "2025-06-02",
          "value": 293.70000000000005
        },
        {
          "date": "2025-06-03",
          "value": 296.09999999999997
        },
        {
          "date": "2025-06-04",
          "value": 285.20000000000005
        },
        {
          "date": "2025-06-05",
          "value": 291.90000000000003
        },
        {
          "date": "2025-06-06",
          "value": 303.29999999999995
        },
        {
          "date": "2025-06-09",
          "value": 299.90000000000003
        },
        {
          "date": "2025-06-10",
          "value": 297.19999999999993
        },
        {
          "date": "2025-06-11",
          "value": 293.0
        },
        {
          "date": "2025-06-12",
          "value": 288.00000000000006
        },
        {
          "date": "2025-06-13",
          "value": 298.09999999999997
        },
        {
          "date": "2025-06-16",
          "value": 298.29999999999995
        },
        {
          "date": "2025-06-17",
          "value": 289.19999999999993
        },
        {
          "date": "2025-06-18",
          "value": 290.09999999999997
        },
        {
          "date": "2025-06-20",
          "value": 295.6
        },
        {
          "date": "2025-06-23",
          "value": 290.29999999999995
        },
        {
          "date": "2025-06-24",
          "value": 285.49999999999994
        },
        {
          "date": "2025-06-25",
          "value": 286.4
        },
        {
          "date": "2025-06-26",
          "value": 281.49999999999994
        },
        {
          "date": "2025-06-27",
          "value": 283.1
        },
        {
          "date": "2025-06-30",
          "value": 277.80000000000007
        },
        {
          "date": "2025-07-01",
          "value": 284.09999999999997
        },
        {
          "date": "2025-07-02",
          "value": 286.59999999999997
        },
        {
          "date": "2025-07-03",
          "value": 290.2
        },
        {
          "date": "2025-07-07",
          "value": 293.70000000000005
        },
        {
          "date": "2025-07-08",
          "value": 292.8
        },
        {
          "date": "2025-07-09",
          "value": 283.3
        },
        {
          "date": "2025-07-10",
          "value": 285.19999999999993
        },
        {
          "date": "2025-07-11",
          "value": 292.3
        },
        {
          "date": "2025-07-14",
          "value": 285.59999999999997
        },
        {
          "date": "2025-07-15",
          "value": 291.2
        },
        {
          "date": "2025-07-16",
          "value": 288.5
        },
        {
          "date": "2025-07-17",
          "value": 290.9
        },
        {
          "date": "2025-07-18",
          "value": 291.20000000000005
        },
        {
          "date": "2025-07-21",
          "value": 285.2
        },
        {
          "date": "2025-07-22",
          "value": 284.0
        },
        {
          "date": "2025-07-23",
          "value": 280.40000000000003
        },
        {
          "date": "2025-07-24",
          "value": 282.5
        },
        {
          "date": "2025-07-25",
          "value": 279.50000000000006
        },
        {
          "date": "2025-07-28",
          "value": 284.90000000000003
        },
        {
          "date": "2025-07-29",
          "value": 277.59999999999997
        },
        {
          "date": "2025-07-30",
          "value": 281.5
        },
        {
          "date": "2025-07-31",
          "value": 281.1
        },
        {
          "date": "2025-08-01",
          "value": 267.00000000000006
        },
        {
          "date": "2025-08-04",
          "value": 270.0
        },
        {
          "date": "2025-08-05",
          "value": 273.29999999999995
        },
        {
          "date": "2025-08-06",
          "value": 271.09999999999997
        },
        {
          "date": "2025-08-07",
          "value": 273.00000000000006
        },
        {
          "date": "2025-08-08",
          "value": 276.79999999999995
        },
        {
          "date": "2025-08-11",
          "value": 276.79999999999995
        },
        {
          "date": "2025-08-12",
          "value": 277.4
        },
        {
          "date": "2025-08-13",
          "value": 271.0
        },
        {
          "date": "2025-08-14",
          "value": 272.70000000000005
        },
        {
          "date": "2025-08-15",
          "value": 275.6
        },
        {
          "date": "2025-08-18",
          "value": 275.59999999999997
        },
        {
          "date": "2025-08-19",
          "value": 269.7
        },
        {
          "date": "2025-08-20",
          "value": 267.3
        },
        {
          "date": "2025-08-21",
          "value": 271.3
        },
        {
          "date": "2025-08-22",
          "value": 263.4
        },
        {
          "date": "2025-08-25",
          "value": 265.2
        },
        {
          "date": "2025-08-26",
          "value": 262.9
        },
        {
          "date": "2025-08-27",
          "value": 260.3
        },
        {
          "date": "2025-08-28",
          "value": 259.2
        },
        {
          "date": "2025-08-29",
          "value": 261.70000000000005
        },
        {
          "date": "2025-09-02",
          "value": 266.5
        },
        {
          "date": "2025-09-03",
          "value": 257.7
        },
        {
          "date": "2025-09-04",
          "value": 255.29999999999998
        },
        {
          "date": "2025-09-05",
          "value": 250.99999999999997
        },
        {
          "date": "2025-09-08",
          "value": 246.39999999999995
        },
        {
          "date": "2025-09-09",
          "value": 250.0
        },
        {
          "date": "2025-09-10",
          "value": 245.5
        },
        {
          "date": "2025-09-11",
          "value": 241.59999999999994
        },
        {
          "date": "2025-09-12",
          "value": 244.69999999999996
        },
        {
          "date": "2025-09-15",
          "value": 243.7
        },
        {
          "date": "2025-09-16",
          "value": 241.7
        },
        {
          "date": "2025-09-17",
          "value": 244.89999999999998
        },
        {
          "date": "2025-09-18",
          "value": 249.5
        },
        {
          "date": "2025-09-19",
          "value": 248.49999999999994
        },
        {
          "date": "2025-09-22",
          "value": 248.10000000000002
        },
        {
          "date": "2025-09-23",
          "value": 245.1
        },
        {
          "date": "2025-09-24",
          "value": 250.5
        },
        {
          "date": "2025-09-25",
          "value": 252.1
        },
        {
          "date": "2025-09-26",
          "value": 253.10000000000002
        },
        {
          "date": "2025-09-29",
          "value": 249.30000000000004
        },
        {
          "date": "2025-09-30",
          "value": 249.8
        },
        {
          "date": "2025-10-01",
          "value": 245.7
        },
        {
          "date": "2025-10-02",
          "value": 242.49999999999997
        },
        {
          "date": "2025-10-03",
          "value": 246.3
        },
        {
          "date": "2025-10-06",
          "value": 250.29999999999995
        },
        {
          "date": "2025-10-07",
          "value": 245.79999999999998
        },
        {
          "date": "2025-10-08",
          "value": 242.89999999999998
        },
        {
          "date": "2025-10-09",
          "value": 244.29999999999995
        },
        {
          "date": "2025-10-10",
          "value": 235.29999999999998
        },
        {
          "date": "2025-10-14",
          "value": 236.00000000000003
        },
        {
          "date": "2025-10-15",
          "value": 238.79999999999998
        },
        {
          "date": "2025-10-16",
          "value": 232.7
        },
        {
          "date": "2025-10-17",
          "value": 238.19999999999996
        },
        {
          "date": "2025-10-20",
          "value": 232.39999999999998
        },
        {
          "date": "2025-10-21",
          "value": 231.29999999999998
        },
        {
          "date": "2025-10-22",
          "value": 230.70000000000005
        },
        {
          "date": "2025-10-23",
          "value": 234.3
        },
        {
          "date": "2025-10-24",
          "value": 235.29999999999998
        },
        {
          "date": "2025-10-27",
          "value": 232.7
        },
        {
          "date": "2025-10-28",
          "value": 233.60000000000002
        },
        {
          "date": "2025-10-29",
          "value": 241.60000000000002
        },
        {
          "date": "2025-10-30",
          "value": 245.00000000000003
        },
        {
          "date": "2025-10-31",
          "value": 244.00000000000003
        },
        {
          "date": "2025-11-03",
          "value": 246.0
        },
        {
          "date": "2025-11-04",
          "value": 241.59999999999994
        },
        {
          "date": "2025-11-05",
          "value": 249.39999999999998
        },
        {
          "date": "2025-11-06",
          "value": 241.60000000000002
        },
        {
          "date": "2025-11-07",
          "value": 242.20000000000005
        },
        {
          "date": "2025-11-10",
          "value": 241.8
        },
        {
          "date": "2025-11-12",
          "value": 238.0
        },
        {
          "date": "2025-11-13",
          "value": 240.50000000000003
        },
        {
          "date": "2025-11-14",
          "value": 242.59999999999997
        },
        {
          "date": "2025-11-17",
          "value": 238.49999999999997
        },
        {
          "date": "2025-11-18",
          "value": 236.10000000000002
        },
        {
          "date": "2025-11-19",
          "value": 235.1
        },
        {
          "date": "2025-11-20",
          "value": 227.59999999999997
        },
        {
          "date": "2025-11-21",
          "value": 226.79999999999998
        },
        {
          "date": "2025-11-24",
          "value": 224.8
        },
        {
          "date": "2025-11-25",
          "value": 219.89999999999998
        },
        {
          "date": "2025-11-26",
          "value": 217.49999999999997
        },
        {
          "date": "2025-11-28",
          "value": 220.79999999999993
        },
        {
          "date": "2025-12-01",
          "value": 220.89999999999998
        },
        {
          "date": "2025-12-02",
          "value": 222.6
        },
        {
          "date": "2025-12-03",
          "value": 216.29999999999993
        },
        {
          "date": "2025-12-04",
          "value": 217.10000000000002
        },
        {
          "date": "2025-12-05",
          "value": 218.89999999999995
        },
        {
          "date": "2025-12-08",
          "value": 220.39999999999998
        },
        {
          "date": "2025-12-09",
          "value": 221.8
        },
        {
          "date": "2025-12-10",
          "value": 217.19999999999996
        },
        {
          "date": "2025-12-11",
          "value": 220.7
        },
        {
          "date": "2025-12-12",
          "value": 223.40000000000003
        },
        {
          "date": "2025-12-15",
          "value": 221.89999999999995
        },
        {
          "date": "2025-12-16",
          "value": 219.30000000000004
        },
        {
          "date": "2025-12-17",
          "value": 218.00000000000003
        },
        {
          "date": "2025-12-18",
          "value": 214.8
        },
        {
          "date": "2025-12-19",
          "value": 213.90000000000003
        },
        {
          "date": "2025-12-22",
          "value": 209.7
        },
        {
          "date": "2025-12-23",
          "value": 214.09999999999997
        },
        {
          "date": "2025-12-24",
          "value": 210.60000000000002
        },
        {
          "date": "2025-12-26",
          "value": 210.09999999999997
        },
        {
          "date": "2025-12-29",
          "value": 206.8
        },
        {
          "date": "2025-12-30",
          "value": 207.39999999999998
        },
        {
          "date": "2025-12-31",
          "value": 211.39999999999998
        },
        {
          "date": "2026-01-02",
          "value": 212.40000000000006
        },
        {
          "date": "2026-01-05",
          "value": 205.89999999999998
        },
        {
          "date": "2026-01-06",
          "value": 205.69999999999996
        },
        {
          "date": "2026-01-07",
          "value": 202.60000000000002
        },
        {
          "date": "2026-01-08",
          "value": 210.70000000000002
        },
        {
          "date": "2026-01-09",
          "value": 208.39999999999998
        },
        {
          "date": "2026-01-12",
          "value": 209.40000000000003
        },
        {
          "date": "2026-01-13",
          "value": 201.7
        },
        {
          "date": "2026-01-14",
          "value": 196.80000000000004
        },
        {
          "date": "2026-01-15",
          "value": 200.59999999999997
        },
        {
          "date": "2026-01-16",
          "value": 205.80000000000004
        },
        {
          "date": "2026-01-20",
          "value": 196.99999999999997
        },
        {
          "date": "2026-01-21",
          "value": 198.0
        },
        {
          "date": "2026-01-22",
          "value": 202.1
        },
        {
          "date": "2026-01-23",
          "value": 198.70000000000002
        },
        {
          "date": "2026-01-26",
          "value": 198.39999999999995
        },
        {
          "date": "2026-01-27",
          "value": 195.9
        },
        {
          "date": "2026-01-28",
          "value": 202.29999999999995
        },
        {
          "date": "2026-01-29",
          "value": 198.80000000000004
        },
        {
          "date": "2026-01-30",
          "value": 201.29999999999998
        },
        {
          "date": "2026-02-02",
          "value": 205.50000000000003
        },
        {
          "date": "2026-02-03",
          "value": 202.20000000000002
        },
        {
          "date": "2026-02-04",
          "value": 204.1
        },
        {
          "date": "2026-02-05",
          "value": 197.9
        },
        {
          "date": "2026-02-06",
          "value": 198.39999999999995
        },
        {
          "date": "2026-02-09",
          "value": 193.09999999999997
        },
        {
          "date": "2026-02-10",
          "value": 191.9
        },
        {
          "date": "2026-02-11",
          "value": 193.89999999999995
        },
        {
          "date": "2026-02-12",
          "value": 185.2
        },
        {
          "date": "2026-02-13",
          "value": 182.20000000000002
        },
        {
          "date": "2026-02-17",
          "value": 190.7
        },
        {
          "date": "2026-02-18",
          "value": 193.79999999999998
        },
        {
          "date": "2026-02-19",
          "value": 192.3
        },
        {
          "date": "2026-02-20",
          "value": 195.5
        },
        {
          "date": "2026-02-23",
          "value": 190.50000000000003
        },
        {
          "date": "2026-02-24",
          "value": 192.1
        },
        {
          "date": "2026-02-25",
          "value": 189.6
        },
        {
          "date": "2026-02-26",
          "value": 185.19999999999993
        },
        {
          "date": "2026-02-27",
          "value": 183.8
        },
        {
          "date": "2026-03-02",
          "value": 196.29999999999995
        },
        {
          "date": "2026-03-03",
          "value": 191.19999999999996
        },
        {
          "date": "2026-03-04",
          "value": 195.6
        },
        {
          "date": "2026-03-05",
          "value": 195.5
        },
        {
          "date": "2026-03-06",
          "value": 197.00000000000003
        },
        {
          "date": "2026-03-09",
          "value": 191.5
        },
        {
          "date": "2026-03-10",
          "value": 195.10000000000005
        },
        {
          "date": "2026-03-11",
          "value": 203.2
        },
        {
          "date": "2026-03-12",
          "value": 206.89999999999995
        },
        {
          "date": "2026-03-13",
          "value": 202.50000000000003
        },
        {
          "date": "2026-03-16",
          "value": 194.20000000000007
        },
        {
          "date": "2026-03-17",
          "value": 192.10000000000002
        },
        {
          "date": "2026-03-18",
          "value": 202.89999999999998
        },
        {
          "date": "2026-03-19",
          "value": 197.7
        },
        {
          "date": "2026-03-20",
          "value": 211.69999999999996
        },
        {
          "date": "2026-03-23",
          "value": 201.79999999999998
        },
        {
          "date": "2026-03-24",
          "value": 210.79999999999995
        },
        {
          "date": "2026-03-25",
          "value": 206.3
        },
        {
          "date": "2026-03-26",
          "value": 213.39999999999998
        },
        {
          "date": "2026-03-27",
          "value": 206.00000000000006
        },
        {
          "date": "2026-03-30",
          "value": 198.2
        },
        {
          "date": "2026-03-31",
          "value": 193.39999999999998
        },
        {
          "date": "2026-04-01",
          "value": 201.5
        },
        {
          "date": "2026-04-02",
          "value": 191.49999999999997
        },
        {
          "date": "2026-04-03",
          "value": 196.39999999999995
        },
        {
          "date": "2026-04-06",
          "value": 191.1
        },
        {
          "date": "2026-04-07",
          "value": 191.9
        },
        {
          "date": "2026-04-08",
          "value": 191.6
        },
        {
          "date": "2026-04-09",
          "value": 189.3
        },
        {
          "date": "2026-04-10",
          "value": 187.09999999999997
        },
        {
          "date": "2026-04-13",
          "value": 183.29999999999998
        },
        {
          "date": "2026-04-14",
          "value": 183.7
        },
        {
          "date": "2026-04-15",
          "value": 187.6
        },
        {
          "date": "2026-04-16",
          "value": 191.10000000000005
        },
        {
          "date": "2026-04-17",
          "value": 183.2
        },
        {
          "date": "2026-04-20",
          "value": 185.5
        },
        {
          "date": "2026-04-21",
          "value": 190.79999999999998
        },
        {
          "date": "2026-04-22",
          "value": 189.39999999999998
        },
        {
          "date": "2026-04-23",
          "value": 191.1
        },
        {
          "date": "2026-04-24",
          "value": 186.69999999999996
        },
        {
          "date": "2026-04-27",
          "value": 187.29999999999998
        },
        {
          "date": "2026-04-28",
          "value": 189.20000000000005
        },
        {
          "date": "2026-04-29",
          "value": 195.2
        },
        {
          "date": "2026-04-30",
          "value": 188.00000000000003
        },
        {
          "date": "2026-05-01",
          "value": 188.29999999999995
        },
        {
          "date": "2026-05-04",
          "value": 194.3
        },
        {
          "date": "2026-05-05",
          "value": 192.29999999999995
        },
        {
          "date": "2026-05-06",
          "value": 185.3
        },
        {
          "date": "2026-05-07",
          "value": 192.50000000000003
        },
        {
          "date": "2026-05-08",
          "value": 189.5
        },
        {
          "date": "2026-05-11",
          "value": 189.29999999999998
        },
        {
          "date": "2026-05-12",
          "value": 191.4
        },
        {
          "date": "2026-05-13",
          "value": 187.29999999999998
        },
        {
          "date": "2026-05-14",
          "value": 184.19999999999996
        },
        {
          "date": "2026-05-15",
          "value": 189.9
        },
        {
          "date": "2026-05-18",
          "value": 188.10000000000002
        },
        {
          "date": "2026-05-19",
          "value": 188.7
        },
        {
          "date": "2026-05-20",
          "value": 180.00000000000003
        },
        {
          "date": "2026-05-21",
          "value": 182.20000000000002
        },
        {
          "date": "2026-05-22",
          "value": 181.09999999999994
        },
        {
          "date": "2026-05-26",
          "value": 178.7
        },
        {
          "date": "2026-05-27",
          "value": 179.30000000000007
        },
        {
          "date": "2026-05-28",
          "value": 175.8
        },
        {
          "date": "2026-05-29",
          "value": 179.3
        },
        {
          "date": "2026-06-01",
          "value": 178.79999999999998
        },
        {
          "date": "2026-06-02",
          "value": 188.3
        },
        {
          "date": "2026-06-03",
          "value": 184.50000000000003
        },
        {
          "date": "2026-06-04",
          "value": 179.9
        },
        {
          "date": "2026-06-05",
          "value": 188.09999999999997
        },
        {
          "date": "2026-06-08",
          "value": 184.49999999999997
        },
        {
          "date": "2026-06-09",
          "value": 186.10000000000002
        },
        {
          "date": "2026-06-10",
          "value": 186.89999999999998
        },
        {
          "date": "2026-06-11",
          "value": 176.8
        },
        {
          "date": "2026-06-12",
          "value": 183.70000000000007
        },
        {
          "date": "2026-06-15",
          "value": 188.09999999999997
        },
        {
          "date": "2026-06-16",
          "value": 177.5
        },
        {
          "date": "2026-06-17",
          "value": 187.70000000000002
        },
        {
          "date": "2026-06-18",
          "value": 183.2
        },
        {
          "date": "2026-06-22",
          "value": 183.29999999999998
        },
        {
          "date": "2026-06-23",
          "value": 181.70000000000002
        },
        {
          "date": "2026-06-24",
          "value": 173.60000000000002
        },
        {
          "date": "2026-06-25",
          "value": 176.30000000000004
        },
        {
          "date": "2026-06-26",
          "value": 176.89999999999998
        },
        {
          "date": "2026-06-29",
          "value": 173.59999999999997
        },
        {
          "date": "2026-06-30",
          "value": 175.00000000000006
        },
        {
          "date": "2026-07-01",
          "value": 179.00000000000006
        },
        {
          "date": "2026-07-02",
          "value": 180.00000000000003
        },
        {
          "date": "2026-07-06",
          "value": 179.00000000000006
        },
        {
          "date": "2026-07-07",
          "value": 186.0
        }
      ],
      "CFTC_JPY_NET_OI": [
        {
          "date": "2023-12-12",
          "value": -0.3149727658484127
        },
        {
          "date": "2023-12-19",
          "value": -0.3490480800258148
        },
        {
          "date": "2023-12-26",
          "value": -0.2947279091969874
        },
        {
          "date": "2024-01-02",
          "value": -0.3107714543419437
        },
        {
          "date": "2024-01-09",
          "value": -0.27932740552873453
        },
        {
          "date": "2024-01-16",
          "value": -0.26515524427004955
        },
        {
          "date": "2024-01-23",
          "value": -0.2906818855130189
        },
        {
          "date": "2024-01-30",
          "value": -0.3324188423701292
        },
        {
          "date": "2024-02-06",
          "value": -0.32453321620392844
        },
        {
          "date": "2024-02-13",
          "value": -0.3661816462677943
        },
        {
          "date": "2024-02-20",
          "value": -0.39542558555255075
        },
        {
          "date": "2024-02-27",
          "value": -0.4285880380967145
        },
        {
          "date": "2024-03-05",
          "value": -0.37777587050917716
        },
        {
          "date": "2024-03-12",
          "value": -0.31418438627466033
        },
        {
          "date": "2024-03-19",
          "value": -0.3835107438016529
        },
        {
          "date": "2024-03-26",
          "value": -0.42232769928786623
        },
        {
          "date": "2024-04-02",
          "value": -0.45210205518151314
        },
        {
          "date": "2024-04-09",
          "value": -0.4997272550765997
        },
        {
          "date": "2024-04-16",
          "value": -0.5001932892392257
        },
        {
          "date": "2024-04-23",
          "value": -0.535207203562515
        },
        {
          "date": "2024-04-30",
          "value": -0.5028789181957186
        },
        {
          "date": "2024-05-07",
          "value": -0.4499514771942813
        },
        {
          "date": "2024-05-14",
          "value": -0.42399010772632273
        },
        {
          "date": "2024-05-21",
          "value": -0.4791231767419478
        },
        {
          "date": "2024-05-28",
          "value": -0.47977898785786105
        },
        {
          "date": "2024-06-04",
          "value": -0.43596394826556306
        },
        {
          "date": "2024-06-11",
          "value": -0.4340441125804168
        },
        {
          "date": "2024-06-18",
          "value": -0.4972889467785418
        },
        {
          "date": "2024-06-25",
          "value": -0.5111143114946346
        },
        {
          "date": "2024-07-02",
          "value": -0.5266267791445242
        },
        {
          "date": "2024-07-09",
          "value": -0.5216532838139124
        },
        {
          "date": "2024-07-16",
          "value": -0.4917628293810322
        },
        {
          "date": "2024-07-23",
          "value": -0.3486781495069714
        },
        {
          "date": "2024-07-30",
          "value": -0.24232148335318043
        },
        {
          "date": "2024-08-06",
          "value": -0.03798124688479512
        },
        {
          "date": "2024-08-13",
          "value": 0.07326741464714052
        },
        {
          "date": "2024-08-20",
          "value": 0.07458957548616843
        },
        {
          "date": "2024-08-27",
          "value": 0.08127971243546922
        },
        {
          "date": "2024-09-03",
          "value": 0.12581587845591272
        },
        {
          "date": "2024-09-10",
          "value": 0.1481219821839294
        },
        {
          "date": "2024-09-17",
          "value": 0.28496513137774926
        },
        {
          "date": "2024-09-24",
          "value": 0.3178159093316386
        },
        {
          "date": "2024-10-01",
          "value": 0.2893577981651376
        },
        {
          "date": "2024-10-08",
          "value": 0.1857182804992755
        },
        {
          "date": "2024-10-15",
          "value": 0.1723850387373592
        },
        {
          "date": "2024-10-22",
          "value": 0.06159507663814641
        },
        {
          "date": "2024-10-29",
          "value": -0.1098612623619928
        },
        {
          "date": "2024-11-05",
          "value": -0.18733722991830745
        },
        {
          "date": "2024-11-12",
          "value": -0.2518627177051318
        },
        {
          "date": "2024-11-19",
          "value": -0.18445650505535505
        },
        {
          "date": "2024-11-26",
          "value": -0.08925881230133377
        },
        {
          "date": "2024-12-03",
          "value": 0.00908705114678274
        },
        {
          "date": "2024-12-10",
          "value": 0.0937001972099522
        },
        {
          "date": "2024-12-17",
          "value": 0.032811700142563835
        },
        {
          "date": "2024-12-24",
          "value": 0.011513551215623755
        },
        {
          "date": "2024-12-31",
          "value": -0.04079315459653768
        },
        {
          "date": "2025-01-07",
          "value": -0.09502673494747148
        },
        {
          "date": "2025-01-14",
          "value": -0.13132724869614917
        },
        {
          "date": "2025-01-21",
          "value": -0.06933654664020414
        },
        {
          "date": "2025-01-28",
          "value": -0.004423676587264978
        },
        {
          "date": "2025-02-04",
          "value": 0.08092759722479745
        },
        {
          "date": "2025-02-11",
          "value": 0.1998251095809216
        },
        {
          "date": "2025-02-18",
          "value": 0.21542308198447163
        },
        {
          "date": "2025-02-25",
          "value": 0.2915676851384931
        },
        {
          "date": "2025-03-04",
          "value": 0.37710311358153575
        },
        {
          "date": "2025-03-11",
          "value": 0.3001089251375012
        },
        {
          "date": "2025-03-18",
          "value": 0.41462468851895184
        },
        {
          "date": "2025-03-25",
          "value": 0.4127224486302497
        },
        {
          "date": "2025-04-01",
          "value": 0.39135241449791425
        },
        {
          "date": "2025-04-08",
          "value": 0.458498307134974
        },
        {
          "date": "2025-04-15",
          "value": 0.5071728114883031
        },
        {
          "date": "2025-04-22",
          "value": 0.5062666203527074
        },
        {
          "date": "2025-04-29",
          "value": 0.4893213850799736
        },
        {
          "date": "2025-05-06",
          "value": 0.4709383138150852
        },
        {
          "date": "2025-05-13",
          "value": 0.47915977091741513
        },
        {
          "date": "2025-05-20",
          "value": 0.4561078325814673
        },
        {
          "date": "2025-05-27",
          "value": 0.435032399585158
        },
        {
          "date": "2025-06-03",
          "value": 0.4129663832484536
        },
        {
          "date": "2025-06-10",
          "value": 0.37241508977162385
        },
        {
          "date": "2025-06-17",
          "value": 0.4121811648290045
        },
        {
          "date": "2025-06-24",
          "value": 0.4202378267099156
        },
        {
          "date": "2025-07-01",
          "value": 0.40521112104655194
        },
        {
          "date": "2025-07-08",
          "value": 0.37636777795418974
        },
        {
          "date": "2025-07-15",
          "value": 0.3223339038431617
        },
        {
          "date": "2025-07-22",
          "value": 0.340675313059034
        },
        {
          "date": "2025-07-29",
          "value": 0.27116053659055345
        },
        {
          "date": "2025-08-05",
          "value": 0.2430686055403731
        },
        {
          "date": "2025-08-12",
          "value": 0.21139470844024
        },
        {
          "date": "2025-08-19",
          "value": 0.2223065946094641
        },
        {
          "date": "2025-08-26",
          "value": 0.23640749259862437
        },
        {
          "date": "2025-09-02",
          "value": 0.17684532732728384
        },
        {
          "date": "2025-09-09",
          "value": 0.22308476895026522
        },
        {
          "date": "2025-09-16",
          "value": 0.2049629530738936
        },
        {
          "date": "2025-09-23",
          "value": 0.25654016063609053
        },
        {
          "date": "2025-09-30",
          "value": 0.20105589919891662
        },
        {
          "date": "2025-10-07",
          "value": 0.15175955481853873
        },
        {
          "date": "2025-10-14",
          "value": 0.12185453913568063
        },
        {
          "date": "2025-10-21",
          "value": 0.22893724660157558
        },
        {
          "date": "2025-10-28",
          "value": 0.21161021345867675
        },
        {
          "date": "2025-11-04",
          "value": 0.1631656004328591
        },
        {
          "date": "2025-11-10",
          "value": 0.15495213284533874
        },
        {
          "date": "2025-11-18",
          "value": 0.09457105045893838
        },
        {
          "date": "2025-11-25",
          "value": 0.07699030253759945
        },
        {
          "date": "2025-12-02",
          "value": 0.09223039110163375
        },
        {
          "date": "2025-12-09",
          "value": 0.0374890420612957
        },
        {
          "date": "2025-12-16",
          "value": -0.007748650833993979
        },
        {
          "date": "2025-12-23",
          "value": 0.004289963659833593
        },
        {
          "date": "2025-12-30",
          "value": 0.04916611913382635
        },
        {
          "date": "2026-01-06",
          "value": 0.030637957701197364
        },
        {
          "date": "2026-01-13",
          "value": -0.15349270328505107
        },
        {
          "date": "2026-01-20",
          "value": -0.1532054940585837
        },
        {
          "date": "2026-01-27",
          "value": -0.1128369346182239
        },
        {
          "date": "2026-02-03",
          "value": -0.0632983505283644
        },
        {
          "date": "2026-02-10",
          "value": -0.05704169005338142
        },
        {
          "date": "2026-02-17",
          "value": 0.036562168386353885
        },
        {
          "date": "2026-02-24",
          "value": 0.031210020528993486
        },
        {
          "date": "2026-03-03",
          "value": -0.03975039390661835
        },
        {
          "date": "2026-03-10",
          "value": -0.09676235276513964
        },
        {
          "date": "2026-03-17",
          "value": -0.20747624644921148
        },
        {
          "date": "2026-03-24",
          "value": -0.19135919076201213
        },
        {
          "date": "2026-03-31",
          "value": -0.21105434492985323
        },
        {
          "date": "2026-04-07",
          "value": -0.2683149527868496
        },
        {
          "date": "2026-04-14",
          "value": -0.23482265820784323
        },
        {
          "date": "2026-04-21",
          "value": -0.2685185711605483
        },
        {
          "date": "2026-04-28",
          "value": -0.2737780996834594
        },
        {
          "date": "2026-05-05",
          "value": -0.1743986666854988
        },
        {
          "date": "2026-05-12",
          "value": -0.20744002077107077
        },
        {
          "date": "2026-05-19",
          "value": -0.23679120868036907
        },
        {
          "date": "2026-05-26",
          "value": -0.2683562137544641
        },
        {
          "date": "2026-06-02",
          "value": -0.2562866552600607
        },
        {
          "date": "2026-06-09",
          "value": -0.2887056377765678
        },
        {
          "date": "2026-06-16",
          "value": -0.28825805212883404
        },
        {
          "date": "2026-06-23",
          "value": -0.33896480523397443
        },
        {
          "date": "2026-06-30",
          "value": -0.35342562524924515
        }
      ],
      "CFTC_JPY_GROSS_SHORT": [
        {
          "date": "2024-01-02",
          "value": 90780.0
        },
        {
          "date": "2024-01-09",
          "value": 97313.0
        },
        {
          "date": "2024-01-16",
          "value": 100740.0
        },
        {
          "date": "2024-01-23",
          "value": 123230.0
        },
        {
          "date": "2024-01-30",
          "value": 125373.0
        },
        {
          "date": "2024-02-06",
          "value": 139876.0
        },
        {
          "date": "2024-02-13",
          "value": 170090.0
        },
        {
          "date": "2024-02-20",
          "value": 174640.0
        },
        {
          "date": "2024-02-27",
          "value": 183966.0
        },
        {
          "date": "2024-03-05",
          "value": 173514.0
        },
        {
          "date": "2024-03-12",
          "value": 157245.0
        },
        {
          "date": "2024-03-19",
          "value": 182286.0
        },
        {
          "date": "2024-03-26",
          "value": 189075.0
        },
        {
          "date": "2024-04-02",
          "value": 198420.0
        },
        {
          "date": "2024-04-09",
          "value": 209426.0
        },
        {
          "date": "2024-04-16",
          "value": 215082.0
        },
        {
          "date": "2024-04-23",
          "value": 222345.0
        },
        {
          "date": "2024-04-30",
          "value": 208823.0
        },
        {
          "date": "2024-05-07",
          "value": 169912.0
        },
        {
          "date": "2024-05-14",
          "value": 161485.0
        },
        {
          "date": "2024-05-21",
          "value": 173981.0
        },
        {
          "date": "2024-05-28",
          "value": 184604.0
        },
        {
          "date": "2024-06-04",
          "value": 172528.0
        },
        {
          "date": "2024-06-11",
          "value": 169342.0
        },
        {
          "date": "2024-06-18",
          "value": 177182.0
        },
        {
          "date": "2024-06-25",
          "value": 208476.0
        },
        {
          "date": "2024-07-02",
          "value": 220937.0
        },
        {
          "date": "2024-07-09",
          "value": 223554.0
        },
        {
          "date": "2024-07-16",
          "value": 198428.0
        },
        {
          "date": "2024-07-23",
          "value": 171498.0
        },
        {
          "date": "2024-07-30",
          "value": 138476.0
        },
        {
          "date": "2024-08-06",
          "value": 77523.0
        },
        {
          "date": "2024-08-13",
          "value": 63997.0
        },
        {
          "date": "2024-08-20",
          "value": 65176.0
        },
        {
          "date": "2024-08-27",
          "value": 58437.0
        },
        {
          "date": "2024-09-03",
          "value": 50675.0
        },
        {
          "date": "2024-09-10",
          "value": 43124.0
        },
        {
          "date": "2024-09-17",
          "value": 40492.0
        },
        {
          "date": "2024-09-24",
          "value": 38679.0
        },
        {
          "date": "2024-10-01",
          "value": 38741.0
        },
        {
          "date": "2024-10-08",
          "value": 47151.0
        },
        {
          "date": "2024-10-15",
          "value": 52575.0
        },
        {
          "date": "2024-10-22",
          "value": 66593.0
        },
        {
          "date": "2024-10-29",
          "value": 89742.0
        },
        {
          "date": "2024-11-05",
          "value": 104501.0
        },
        {
          "date": "2024-11-12",
          "value": 128940.0
        },
        {
          "date": "2024-11-19",
          "value": 125841.0
        },
        {
          "date": "2024-11-26",
          "value": 110230.0
        },
        {
          "date": "2024-12-03",
          "value": 91288.0
        },
        {
          "date": "2024-12-10",
          "value": 72186.0
        },
        {
          "date": "2024-12-17",
          "value": 81247.0
        },
        {
          "date": "2024-12-24",
          "value": 93647.0
        },
        {
          "date": "2024-12-31",
          "value": 104562.0
        },
        {
          "date": "2025-01-07",
          "value": 111395.0
        },
        {
          "date": "2025-01-14",
          "value": 120845.0
        },
        {
          "date": "2025-01-21",
          "value": 108830.0
        },
        {
          "date": "2025-01-28",
          "value": 97768.0
        },
        {
          "date": "2025-02-04",
          "value": 85916.0
        },
        {
          "date": "2025-02-11",
          "value": 89543.0
        },
        {
          "date": "2025-02-18",
          "value": 86997.0
        },
        {
          "date": "2025-02-25",
          "value": 75771.0
        },
        {
          "date": "2025-03-04",
          "value": 50304.0
        },
        {
          "date": "2025-03-11",
          "value": 42888.0
        },
        {
          "date": "2025-03-18",
          "value": 41788.0
        },
        {
          "date": "2025-03-25",
          "value": 35098.0
        },
        {
          "date": "2025-04-01",
          "value": 39792.0
        },
        {
          "date": "2025-04-08",
          "value": 29488.0
        },
        {
          "date": "2025-04-15",
          "value": 26705.0
        },
        {
          "date": "2025-04-22",
          "value": 24559.0
        },
        {
          "date": "2025-04-29",
          "value": 23585.0
        },
        {
          "date": "2025-05-06",
          "value": 27149.0
        },
        {
          "date": "2025-05-13",
          "value": 21958.0
        },
        {
          "date": "2025-05-20",
          "value": 27180.0
        },
        {
          "date": "2025-05-27",
          "value": 27790.0
        },
        {
          "date": "2025-06-03",
          "value": 38365.0
        },
        {
          "date": "2025-06-10",
          "value": 39600.0
        },
        {
          "date": "2025-06-17",
          "value": 44724.0
        },
        {
          "date": "2025-06-24",
          "value": 46126.0
        },
        {
          "date": "2025-07-01",
          "value": 43286.0
        },
        {
          "date": "2025-07-08",
          "value": 50037.0
        },
        {
          "date": "2025-07-15",
          "value": 61862.0
        },
        {
          "date": "2025-07-22",
          "value": 57766.0
        },
        {
          "date": "2025-07-29",
          "value": 72879.0
        },
        {
          "date": "2025-08-05",
          "value": 78252.0
        },
        {
          "date": "2025-08-12",
          "value": 90459.0
        },
        {
          "date": "2025-08-19",
          "value": 90782.0
        },
        {
          "date": "2025-08-26",
          "value": 86281.0
        },
        {
          "date": "2025-09-02",
          "value": 101516.0
        },
        {
          "date": "2025-09-09",
          "value": 89081.0
        },
        {
          "date": "2025-09-16",
          "value": 100262.0
        },
        {
          "date": "2025-09-23",
          "value": 96900.0
        },
        {
          "date": "2025-09-30",
          "value": 106346.0
        },
        {
          "date": "2025-10-07",
          "value": 112890.0
        },
        {
          "date": "2025-10-14",
          "value": 123473.0
        },
        {
          "date": "2025-10-21",
          "value": 105310.0
        },
        {
          "date": "2025-10-28",
          "value": 110630.0
        },
        {
          "date": "2025-11-04",
          "value": 118915.0
        },
        {
          "date": "2025-11-10",
          "value": 123873.0
        },
        {
          "date": "2025-11-18",
          "value": 138733.0
        },
        {
          "date": "2025-11-25",
          "value": 142701.0
        },
        {
          "date": "2025-12-02",
          "value": 148540.0
        },
        {
          "date": "2025-12-09",
          "value": 167040.0
        },
        {
          "date": "2025-12-16",
          "value": 149217.0
        },
        {
          "date": "2025-12-23",
          "value": 139910.0
        },
        {
          "date": "2025-12-30",
          "value": 130528.0
        },
        {
          "date": "2026-01-06",
          "value": 131626.0
        },
        {
          "date": "2026-01-13",
          "value": 156907.0
        },
        {
          "date": "2026-01-20",
          "value": 151968.0
        },
        {
          "date": "2026-01-27",
          "value": 138393.0
        },
        {
          "date": "2026-02-03",
          "value": 133650.0
        },
        {
          "date": "2026-02-10",
          "value": 147196.0
        },
        {
          "date": "2026-02-17",
          "value": 130217.0
        },
        {
          "date": "2026-02-24",
          "value": 137825.0
        },
        {
          "date": "2026-03-03",
          "value": 151520.0
        },
        {
          "date": "2026-03-10",
          "value": 160798.0
        },
        {
          "date": "2026-03-17",
          "value": 174599.0
        },
        {
          "date": "2026-03-24",
          "value": 161077.0
        },
        {
          "date": "2026-03-31",
          "value": 168228.0
        },
        {
          "date": "2026-04-07",
          "value": 185302.0
        },
        {
          "date": "2026-04-14",
          "value": 185322.0
        },
        {
          "date": "2026-04-21",
          "value": 195846.0
        },
        {
          "date": "2026-04-28",
          "value": 208589.0
        },
        {
          "date": "2026-05-05",
          "value": 170773.0
        },
        {
          "date": "2026-05-12",
          "value": 175257.0
        },
        {
          "date": "2026-05-19",
          "value": 200508.0
        },
        {
          "date": "2026-05-26",
          "value": 227660.0
        },
        {
          "date": "2026-06-02",
          "value": 244416.0
        },
        {
          "date": "2026-06-09",
          "value": 267338.0
        },
        {
          "date": "2026-06-16",
          "value": 267507.0
        },
        {
          "date": "2026-06-23",
          "value": 259802.0
        },
        {
          "date": "2026-06-30",
          "value": 266964.0
        }
      ],
      "CFTC_JPY_GROSS_LONG": [
        {
          "date": "2024-01-02",
          "value": 33585.0
        },
        {
          "date": "2024-01-09",
          "value": 41364.0
        },
        {
          "date": "2024-01-16",
          "value": 44180.0
        },
        {
          "date": "2024-01-23",
          "value": 52585.0
        },
        {
          "date": "2024-01-30",
          "value": 44918.0
        },
        {
          "date": "2024-02-06",
          "value": 55646.0
        },
        {
          "date": "2024-02-13",
          "value": 58554.0
        },
        {
          "date": "2024-02-20",
          "value": 53862.0
        },
        {
          "date": "2024-02-27",
          "value": 51261.0
        },
        {
          "date": "2024-03-05",
          "value": 54671.0
        },
        {
          "date": "2024-03-12",
          "value": 54923.0
        },
        {
          "date": "2024-03-19",
          "value": 66274.0
        },
        {
          "date": "2024-03-26",
          "value": 59969.0
        },
        {
          "date": "2024-04-02",
          "value": 55190.0
        },
        {
          "date": "2024-04-09",
          "value": 47275.0
        },
        {
          "date": "2024-04-16",
          "value": 49463.0
        },
        {
          "date": "2024-04-23",
          "value": 42426.0
        },
        {
          "date": "2024-04-30",
          "value": 40435.0
        },
        {
          "date": "2024-05-07",
          "value": 34990.0
        },
        {
          "date": "2024-05-14",
          "value": 35303.0
        },
        {
          "date": "2024-05-21",
          "value": 29614.0
        },
        {
          "date": "2024-05-28",
          "value": 28565.0
        },
        {
          "date": "2024-06-04",
          "value": 40427.0
        },
        {
          "date": "2024-06-11",
          "value": 30763.0
        },
        {
          "date": "2024-06-18",
          "value": 29429.0
        },
        {
          "date": "2024-06-25",
          "value": 34576.0
        },
        {
          "date": "2024-07-02",
          "value": 36714.0
        },
        {
          "date": "2024-07-09",
          "value": 41521.0
        },
        {
          "date": "2024-07-16",
          "value": 47356.0
        },
        {
          "date": "2024-07-23",
          "value": 64390.0
        },
        {
          "date": "2024-07-30",
          "value": 65016.0
        },
        {
          "date": "2024-08-06",
          "value": 66169.0
        },
        {
          "date": "2024-08-13",
          "value": 87101.0
        },
        {
          "date": "2024-08-20",
          "value": 88761.0
        },
        {
          "date": "2024-08-27",
          "value": 84305.0
        },
        {
          "date": "2024-09-03",
          "value": 91791.0
        },
        {
          "date": "2024-09-10",
          "value": 98894.0
        },
        {
          "date": "2024-09-17",
          "value": 97332.0
        },
        {
          "date": "2024-09-24",
          "value": 104690.0
        },
        {
          "date": "2024-10-01",
          "value": 95513.0
        },
        {
          "date": "2024-10-08",
          "value": 83679.0
        },
        {
          "date": "2024-10-15",
          "value": 86685.0
        },
        {
          "date": "2024-10-22",
          "value": 79364.0
        },
        {
          "date": "2024-10-29",
          "value": 64925.0
        },
        {
          "date": "2024-11-05",
          "value": 60334.0
        },
        {
          "date": "2024-11-12",
          "value": 64038.0
        },
        {
          "date": "2024-11-19",
          "value": 78973.0
        },
        {
          "date": "2024-11-26",
          "value": 87597.0
        },
        {
          "date": "2024-12-03",
          "value": 93622.0
        },
        {
          "date": "2024-12-10",
          "value": 97938.0
        },
        {
          "date": "2024-12-17",
          "value": 87208.0
        },
        {
          "date": "2024-12-24",
          "value": 95958.0
        },
        {
          "date": "2024-12-31",
          "value": 96119.0
        },
        {
          "date": "2025-01-07",
          "value": 91206.0
        },
        {
          "date": "2025-01-14",
          "value": 91434.0
        },
        {
          "date": "2025-01-21",
          "value": 94157.0
        },
        {
          "date": "2025-01-28",
          "value": 96809.0
        },
        {
          "date": "2025-02-04",
          "value": 104684.0
        },
        {
          "date": "2025-02-11",
          "value": 144158.0
        },
        {
          "date": "2025-02-18",
          "value": 147566.0
        },
        {
          "date": "2025-02-25",
          "value": 171751.0
        },
        {
          "date": "2025-03-04",
          "value": 183955.0
        },
        {
          "date": "2025-03-11",
          "value": 176790.0
        },
        {
          "date": "2025-03-18",
          "value": 164752.0
        },
        {
          "date": "2025-03-25",
          "value": 160474.0
        },
        {
          "date": "2025-04-01",
          "value": 161566.0
        },
        {
          "date": "2025-04-08",
          "value": 176555.0
        },
        {
          "date": "2025-04-15",
          "value": 198560.0
        },
        {
          "date": "2025-04-22",
          "value": 202373.0
        },
        {
          "date": "2025-04-29",
          "value": 202797.0
        },
        {
          "date": "2025-05-06",
          "value": 204008.0
        },
        {
          "date": "2025-05-13",
          "value": 194226.0
        },
        {
          "date": "2025-05-20",
          "value": 194510.0
        },
        {
          "date": "2025-05-27",
          "value": 191802.0
        },
        {
          "date": "2025-06-03",
          "value": 189514.0
        },
        {
          "date": "2025-06-10",
          "value": 184195.0
        },
        {
          "date": "2025-06-17",
          "value": 175601.0
        },
        {
          "date": "2025-06-24",
          "value": 178403.0
        },
        {
          "date": "2025-07-01",
          "value": 170624.0
        },
        {
          "date": "2025-07-08",
          "value": 166192.0
        },
        {
          "date": "2025-07-15",
          "value": 165444.0
        },
        {
          "date": "2025-07-22",
          "value": 164411.0
        },
        {
          "date": "2025-07-29",
          "value": 162122.0
        },
        {
          "date": "2025-08-05",
          "value": 160258.0
        },
        {
          "date": "2025-08-12",
          "value": 164693.0
        },
        {
          "date": "2025-08-19",
          "value": 168363.0
        },
        {
          "date": "2025-08-26",
          "value": 170765.0
        },
        {
          "date": "2025-09-02",
          "value": 174774.0
        },
        {
          "date": "2025-09-09",
          "value": 180724.0
        },
        {
          "date": "2025-09-16",
          "value": 161673.0
        },
        {
          "date": "2025-09-23",
          "value": 176400.0
        },
        {
          "date": "2025-09-30",
          "value": 167811.0
        },
        {
          "date": "2025-10-07",
          "value": 159197.0
        },
        {
          "date": "2025-10-14",
          "value": 160639.0
        },
        {
          "date": "2025-10-21",
          "value": 175724.0
        },
        {
          "date": "2025-10-28",
          "value": 178745.0
        },
        {
          "date": "2025-11-04",
          "value": 170180.0
        },
        {
          "date": "2025-11-10",
          "value": 172349.0
        },
        {
          "date": "2025-11-18",
          "value": 169890.0
        },
        {
          "date": "2025-11-25",
          "value": 169218.0
        },
        {
          "date": "2025-12-02",
          "value": 184958.0
        },
        {
          "date": "2025-12-09",
          "value": 184488.0
        },
        {
          "date": "2025-12-16",
          "value": 146275.0
        },
        {
          "date": "2025-12-23",
          "value": 141133.0
        },
        {
          "date": "2025-12-30",
          "value": 144596.0
        },
        {
          "date": "2026-01-06",
          "value": 140441.0
        },
        {
          "date": "2026-01-13",
          "value": 111743.0
        },
        {
          "date": "2026-01-20",
          "value": 107139.0
        },
        {
          "date": "2026-01-27",
          "value": 104460.0
        },
        {
          "date": "2026-02-03",
          "value": 114428.0
        },
        {
          "date": "2026-02-10",
          "value": 128090.0
        },
        {
          "date": "2026-02-17",
          "value": 143172.0
        },
        {
          "date": "2026-02-24",
          "value": 149364.0
        },
        {
          "date": "2026-03-03",
          "value": 134945.0
        },
        {
          "date": "2026-03-10",
          "value": 119411.0
        },
        {
          "date": "2026-03-17",
          "value": 106819.0
        },
        {
          "date": "2026-03-24",
          "value": 98271.0
        },
        {
          "date": "2026-03-31",
          "value": 95356.0
        },
        {
          "date": "2026-04-07",
          "value": 91560.0
        },
        {
          "date": "2026-04-14",
          "value": 102114.0
        },
        {
          "date": "2026-04-21",
          "value": 101386.0
        },
        {
          "date": "2026-04-28",
          "value": 106530.0
        },
        {
          "date": "2026-05-05",
          "value": 109035.0
        },
        {
          "date": "2026-05-12",
          "value": 100155.0
        },
        {
          "date": "2026-05-19",
          "value": 106603.0
        },
        {
          "date": "2026-05-26",
          "value": 112993.0
        },
        {
          "date": "2026-06-02",
          "value": 114849.0
        },
        {
          "date": "2026-06-09",
          "value": 121520.0
        },
        {
          "date": "2026-06-16",
          "value": 117375.0
        },
        {
          "date": "2026-06-23",
          "value": 113698.0
        },
        {
          "date": "2026-06-30",
          "value": 111872.0
        }
      ],
      "CFTC_JPY_SHORT_SHARE": [
        {
          "date": "2024-01-02",
          "value": 0.7299481365335906
        },
        {
          "date": "2024-01-09",
          "value": 0.701724150363795
        },
        {
          "date": "2024-01-16",
          "value": 0.6951421473916644
        },
        {
          "date": "2024-01-23",
          "value": 0.7009072035946876
        },
        {
          "date": "2024-01-30",
          "value": 0.7362279862118374
        },
        {
          "date": "2024-02-06",
          "value": 0.715397755751271
        },
        {
          "date": "2024-02-13",
          "value": 0.7439075593499064
        },
        {
          "date": "2024-02-20",
          "value": 0.7642821507032761
        },
        {
          "date": "2024-02-27",
          "value": 0.7820785879172034
        },
        {
          "date": "2024-03-05",
          "value": 0.7604093170015558
        },
        {
          "date": "2024-03-12",
          "value": 0.7411343840729988
        },
        {
          "date": "2024-03-19",
          "value": 0.7333682008368201
        },
        {
          "date": "2024-03-26",
          "value": 0.7592031930100706
        },
        {
          "date": "2024-04-02",
          "value": 0.7823823981704191
        },
        {
          "date": "2024-04-09",
          "value": 0.8158363231931313
        },
        {
          "date": "2024-04-16",
          "value": 0.8130261392201705
        },
        {
          "date": "2024-04-23",
          "value": 0.839763418199123
        },
        {
          "date": "2024-04-30",
          "value": 0.8377785266671481
        },
        {
          "date": "2024-05-07",
          "value": 0.8292354393807772
        },
        {
          "date": "2024-05-14",
          "value": 0.820603898611704
        },
        {
          "date": "2024-05-21",
          "value": 0.8545445615069133
        },
        {
          "date": "2024-05-28",
          "value": 0.8659983393457773
        },
        {
          "date": "2024-06-04",
          "value": 0.8101617712662299
        },
        {
          "date": "2024-06-11",
          "value": 0.8462657105019865
        },
        {
          "date": "2024-06-18",
          "value": 0.8575632468745614
        },
        {
          "date": "2024-06-25",
          "value": 0.857742376117045
        },
        {
          "date": "2024-07-02",
          "value": 0.8575049194452962
        },
        {
          "date": "2024-07-09",
          "value": 0.8433613128359898
        },
        {
          "date": "2024-07-16",
          "value": 0.807326758454578
        },
        {
          "date": "2024-07-23",
          "value": 0.7270314725632504
        },
        {
          "date": "2024-07-30",
          "value": 0.6804984962553811
        },
        {
          "date": "2024-08-06",
          "value": 0.5395081145784039
        },
        {
          "date": "2024-08-13",
          "value": 0.4235463076943441
        },
        {
          "date": "2024-08-20",
          "value": 0.4233939858513548
        },
        {
          "date": "2024-08-27",
          "value": 0.4093889675078113
        },
        {
          "date": "2024-09-03",
          "value": 0.35569890359805145
        },
        {
          "date": "2024-09-10",
          "value": 0.30365164979087156
        },
        {
          "date": "2024-09-17",
          "value": 0.2937949849082888
        },
        {
          "date": "2024-09-24",
          "value": 0.2697863554882855
        },
        {
          "date": "2024-10-01",
          "value": 0.2885649589583923
        },
        {
          "date": "2024-10-08",
          "value": 0.360398991057097
        },
        {
          "date": "2024-10-15",
          "value": 0.37753123653597587
        },
        {
          "date": "2024-10-22",
          "value": 0.45625081359578507
        },
        {
          "date": "2024-10-29",
          "value": 0.5802271977862117
        },
        {
          "date": "2024-11-05",
          "value": 0.6339733673067006
        },
        {
          "date": "2024-11-12",
          "value": 0.6681590647638591
        },
        {
          "date": "2024-11-19",
          "value": 0.6144160067182908
        },
        {
          "date": "2024-11-26",
          "value": 0.557204021695724
        },
        {
          "date": "2024-12-03",
          "value": 0.49368882158888105
        },
        {
          "date": "2024-12-10",
          "value": 0.4243140297665232
        },
        {
          "date": "2024-12-17",
          "value": 0.4823068475260455
        },
        {
          "date": "2024-12-24",
          "value": 0.4939057514306057
        },
        {
          "date": "2024-12-31",
          "value": 0.5210358728529357
        },
        {
          "date": "2025-01-07",
          "value": 0.5498245319618363
        },
        {
          "date": "2025-01-14",
          "value": 0.5692743983154245
        },
        {
          "date": "2025-01-21",
          "value": 0.5361427086463665
        },
        {
          "date": "2025-01-28",
          "value": 0.5024643200378256
        },
        {
          "date": "2025-02-04",
          "value": 0.4507660020986359
        },
        {
          "date": "2025-02-11",
          "value": 0.3831519762431483
        },
        {
          "date": "2025-02-18",
          "value": 0.3708896970110375
        },
        {
          "date": "2025-02-25",
          "value": 0.30611824403487364
        },
        {
          "date": "2025-03-04",
          "value": 0.2147366803409901
        },
        {
          "date": "2025-03-11",
          "value": 0.19523120203206512
        },
        {
          "date": "2025-03-18",
          "value": 0.20232400503534426
        },
        {
          "date": "2025-03-25",
          "value": 0.179463317857362
        },
        {
          "date": "2025-04-01",
          "value": 0.19761817260799175
        },
        {
          "date": "2025-04-08",
          "value": 0.14311575739044763
        },
        {
          "date": "2025-04-15",
          "value": 0.11854926419994229
        },
        {
          "date": "2025-04-22",
          "value": 0.10822184619181076
        },
        {
          "date": "2025-04-29",
          "value": 0.1041823113145038
        },
        {
          "date": "2025-05-06",
          "value": 0.11744831434912202
        },
        {
          "date": "2025-05-13",
          "value": 0.1015708840617252
        },
        {
          "date": "2025-05-20",
          "value": 0.1226036357075195
        },
        {
          "date": "2025-05-27",
          "value": 0.12655287988633465
        },
        {
          "date": "2025-06-03",
          "value": 0.1683568911571492
        },
        {
          "date": "2025-06-10",
          "value": 0.17694765298599163
        },
        {
          "date": "2025-06-17",
          "value": 0.20299103596959037
        },
        {
          "date": "2025-06-24",
          "value": 0.20543448730453528
        },
        {
          "date": "2025-07-01",
          "value": 0.20235613108316583
        },
        {
          "date": "2025-07-08",
          "value": 0.23140744303493055
        },
        {
          "date": "2025-07-15",
          "value": 0.2721529568071234
        },
        {
          "date": "2025-07-22",
          "value": 0.25999990998168127
        },
        {
          "date": "2025-07-29",
          "value": 0.3101220845868741
        },
        {
          "date": "2025-08-05",
          "value": 0.32808687266781267
        },
        {
          "date": "2025-08-12",
          "value": 0.3545298488743964
        },
        {
          "date": "2025-08-19",
          "value": 0.3503135310347489
        },
        {
          "date": "2025-08-26",
          "value": 0.3356636555324728
        },
        {
          "date": "2025-09-02",
          "value": 0.36742553114481163
        },
        {
          "date": "2025-09-09",
          "value": 0.33016808435722095
        },
        {
          "date": "2025-09-16",
          "value": 0.38277435241567564
        },
        {
          "date": "2025-09-23",
          "value": 0.3545554335894621
        },
        {
          "date": "2025-09-30",
          "value": 0.3879018226782464
        },
        {
          "date": "2025-10-07",
          "value": 0.4149040564231294
        },
        {
          "date": "2025-10-14",
          "value": 0.434592695838261
        },
        {
          "date": "2025-10-21",
          "value": 0.37472334308304334
        },
        {
          "date": "2025-10-28",
          "value": 0.38230669546436286
        },
        {
          "date": "2025-11-04",
          "value": 0.4113353741849565
        },
        {
          "date": "2025-11-10",
          "value": 0.4181762326903471
        },
        {
          "date": "2025-11-18",
          "value": 0.44952255664678265
        },
        {
          "date": "2025-11-25",
          "value": 0.4574937724216864
        },
        {
          "date": "2025-12-02",
          "value": 0.44539997241362767
        },
        {
          "date": "2025-12-09",
          "value": 0.4751826312555472
        },
        {
          "date": "2025-12-16",
          "value": 0.5049781381560245
        },
        {
          "date": "2025-12-23",
          "value": 0.49782417637158727
        },
        {
          "date": "2025-12-30",
          "value": 0.4744333464183423
        },
        {
          "date": "2026-01-06",
          "value": 0.48379994633674794
        },
        {
          "date": "2026-01-13",
          "value": 0.5840573236553136
        },
        {
          "date": "2026-01-20",
          "value": 0.5865067327397562
        },
        {
          "date": "2026-01-27",
          "value": 0.5698632506083927
        },
        {
          "date": "2026-02-03",
          "value": 0.5387418473222132
        },
        {
          "date": "2026-02-10",
          "value": 0.5347020916428732
        },
        {
          "date": "2026-02-17",
          "value": 0.4763066546203395
        },
        {
          "date": "2026-02-24",
          "value": 0.47991044225231466
        },
        {
          "date": "2026-03-03",
          "value": 0.5289302358054212
        },
        {
          "date": "2026-03-10",
          "value": 0.573850233218776
        },
        {
          "date": "2026-03-17",
          "value": 0.6204258434073158
        },
        {
          "date": "2026-03-24",
          "value": 0.6210844116785169
        },
        {
          "date": "2026-03-31",
          "value": 0.6382329731698434
        },
        {
          "date": "2026-04-07",
          "value": 0.6692937275610232
        },
        {
          "date": "2026-04-14",
          "value": 0.6447417859975786
        },
        {
          "date": "2026-04-21",
          "value": 0.6588994455509501
        },
        {
          "date": "2026-04-28",
          "value": 0.6619372364091026
        },
        {
          "date": "2026-05-05",
          "value": 0.6103220779963403
        },
        {
          "date": "2026-05-12",
          "value": 0.6363448215764019
        },
        {
          "date": "2026-05-19",
          "value": 0.6528844619697765
        },
        {
          "date": "2026-05-26",
          "value": 0.6683046971551696
        },
        {
          "date": "2026-06-02",
          "value": 0.6803223247463571
        },
        {
          "date": "2026-06-09",
          "value": 0.687495178188439
        },
        {
          "date": "2026-06-16",
          "value": 0.6950364007669884
        },
        {
          "date": "2026-06-23",
          "value": 0.6955876840696118
        },
        {
          "date": "2026-06-30",
          "value": 0.7046954354918751
        }
      ],
      "CFTC_JPY_OPEN_INTEREST": [
        {
          "date": "2024-01-02",
          "value": 184042.0
        },
        {
          "date": "2024-01-09",
          "value": 200299.0
        },
        {
          "date": "2024-01-16",
          "value": 213309.0
        },
        {
          "date": "2024-01-23",
          "value": 243032.0
        },
        {
          "date": "2024-01-30",
          "value": 242029.0
        },
        {
          "date": "2024-02-06",
          "value": 259542.0
        },
        {
          "date": "2024-02-13",
          "value": 304592.0
        },
        {
          "date": "2024-02-20",
          "value": 305438.0
        },
        {
          "date": "2024-02-27",
          "value": 309633.0
        },
        {
          "date": "2024-03-05",
          "value": 314586.0
        },
        {
          "date": "2024-03-12",
          "value": 325675.0
        },
        {
          "date": "2024-03-19",
          "value": 302500.0
        },
        {
          "date": "2024-03-26",
          "value": 305701.0
        },
        {
          "date": "2024-04-02",
          "value": 316809.0
        },
        {
          "date": "2024-04-09",
          "value": 324479.0
        },
        {
          "date": "2024-04-16",
          "value": 331110.0
        },
        {
          "date": "2024-04-23",
          "value": 336167.0
        },
        {
          "date": "2024-04-30",
          "value": 334848.0
        },
        {
          "date": "2024-05-07",
          "value": 299859.0
        },
        {
          "date": "2024-05-14",
          "value": 297606.0
        },
        {
          "date": "2024-05-21",
          "value": 301315.0
        },
        {
          "date": "2024-05-28",
          "value": 325231.0
        },
        {
          "date": "2024-06-04",
          "value": 303009.0
        },
        {
          "date": "2024-06-11",
          "value": 319274.0
        },
        {
          "date": "2024-06-18",
          "value": 297117.0
        },
        {
          "date": "2024-06-25",
          "value": 340237.0
        },
        {
          "date": "2024-07-02",
          "value": 349817.0
        },
        {
          "date": "2024-07-09",
          "value": 348954.0
        },
        {
          "date": "2024-07-16",
          "value": 307205.0
        },
        {
          "date": "2024-07-23",
          "value": 307183.0
        },
        {
          "date": "2024-07-30",
          "value": 303151.0
        },
        {
          "date": "2024-08-06",
          "value": 298937.0
        },
        {
          "date": "2024-08-13",
          "value": 315338.0
        },
        {
          "date": "2024-08-20",
          "value": 316197.0
        },
        {
          "date": "2024-08-27",
          "value": 318259.0
        },
        {
          "date": "2024-09-03",
          "value": 326795.0
        },
        {
          "date": "2024-09-10",
          "value": 376514.0
        },
        {
          "date": "2024-09-17",
          "value": 199463.0
        },
        {
          "date": "2024-09-24",
          "value": 207702.0
        },
        {
          "date": "2024-10-01",
          "value": 196200.0
        },
        {
          "date": "2024-10-08",
          "value": 196685.0
        },
        {
          "date": "2024-10-15",
          "value": 197871.0
        },
        {
          "date": "2024-10-22",
          "value": 207338.0
        },
        {
          "date": "2024-10-29",
          "value": 225894.0
        },
        {
          "date": "2024-11-05",
          "value": 235762.0
        },
        {
          "date": "2024-11-12",
          "value": 257688.0
        },
        {
          "date": "2024-11-19",
          "value": 254087.0
        },
        {
          "date": "2024-11-26",
          "value": 253566.0
        },
        {
          "date": "2024-12-03",
          "value": 256849.0
        },
        {
          "date": "2024-12-10",
          "value": 274834.0
        },
        {
          "date": "2024-12-17",
          "value": 181673.0
        },
        {
          "date": "2024-12-24",
          "value": 200720.0
        },
        {
          "date": "2024-12-31",
          "value": 206971.0
        },
        {
          "date": "2025-01-07",
          "value": 212456.0
        },
        {
          "date": "2025-01-14",
          "value": 223952.0
        },
        {
          "date": "2025-01-21",
          "value": 211620.0
        },
        {
          "date": "2025-01-28",
          "value": 216788.0
        },
        {
          "date": "2025-02-04",
          "value": 231911.0
        },
        {
          "date": "2025-02-11",
          "value": 273314.0
        },
        {
          "date": "2025-02-18",
          "value": 281163.0
        },
        {
          "date": "2025-02-25",
          "value": 329186.0
        },
        {
          "date": "2025-03-04",
          "value": 354415.0
        },
        {
          "date": "2025-03-11",
          "value": 446178.0
        },
        {
          "date": "2025-03-18",
          "value": 296567.0
        },
        {
          "date": "2025-03-25",
          "value": 303778.0
        },
        {
          "date": "2025-04-01",
          "value": 311162.0
        },
        {
          "date": "2025-04-08",
          "value": 320758.0
        },
        {
          "date": "2025-04-15",
          "value": 338849.0
        },
        {
          "date": "2025-04-22",
          "value": 351226.0
        },
        {
          "date": "2025-04-29",
          "value": 366246.0
        },
        {
          "date": "2025-05-06",
          "value": 375546.0
        },
        {
          "date": "2025-05-13",
          "value": 359521.0
        },
        {
          "date": "2025-05-20",
          "value": 366865.0
        },
        {
          "date": "2025-05-27",
          "value": 377011.0
        },
        {
          "date": "2025-06-03",
          "value": 366008.0
        },
        {
          "date": "2025-06-10",
          "value": 388263.0
        },
        {
          "date": "2025-06-17",
          "value": 317523.0
        },
        {
          "date": "2025-06-24",
          "value": 314767.0
        },
        {
          "date": "2025-07-01",
          "value": 314251.0
        },
        {
          "date": "2025-07-08",
          "value": 308621.0
        },
        {
          "date": "2025-07-15",
          "value": 321350.0
        },
        {
          "date": "2025-07-22",
          "value": 313040.0
        },
        {
          "date": "2025-07-29",
          "value": 329115.0
        },
        {
          "date": "2025-08-05",
          "value": 337378.0
        },
        {
          "date": "2025-08-12",
          "value": 351163.0
        },
        {
          "date": "2025-08-19",
          "value": 348982.0
        },
        {
          "date": "2025-08-26",
          "value": 357366.0
        },
        {
          "date": "2025-09-02",
          "value": 414249.0
        },
        {
          "date": "2025-09-09",
          "value": 410799.0
        },
        {
          "date": "2025-09-16",
          "value": 299620.0
        },
        {
          "date": "2025-09-23",
          "value": 309893.0
        },
        {
          "date": "2025-09-30",
          "value": 305711.0
        },
        {
          "date": "2025-10-07",
          "value": 305134.0
        },
        {
          "date": "2025-10-14",
          "value": 305003.0
        },
        {
          "date": "2025-10-21",
          "value": 307569.0
        },
        {
          "date": "2025-10-28",
          "value": 321889.0
        },
        {
          "date": "2025-11-04",
          "value": 314190.0
        },
        {
          "date": "2025-11-10",
          "value": 312845.0
        },
        {
          "date": "2025-11-18",
          "value": 329456.0
        },
        {
          "date": "2025-11-25",
          "value": 344420.0
        },
        {
          "date": "2025-12-02",
          "value": 394859.0
        },
        {
          "date": "2025-12-09",
          "value": 465416.0
        },
        {
          "date": "2025-12-16",
          "value": 379679.0
        },
        {
          "date": "2025-12-23",
          "value": 285084.0
        },
        {
          "date": "2025-12-30",
          "value": 286132.0
        },
        {
          "date": "2026-01-06",
          "value": 287715.0
        },
        {
          "date": "2026-01-13",
          "value": 294242.0
        },
        {
          "date": "2026-01-20",
          "value": 292607.0
        },
        {
          "date": "2026-01-27",
          "value": 300726.0
        },
        {
          "date": "2026-02-03",
          "value": 303673.0
        },
        {
          "date": "2026-02-10",
          "value": 334948.0
        },
        {
          "date": "2026-02-17",
          "value": 354328.0
        },
        {
          "date": "2026-02-24",
          "value": 369721.0
        },
        {
          "date": "2026-03-03",
          "value": 416977.0
        },
        {
          "date": "2026-03-10",
          "value": 427718.0
        },
        {
          "date": "2026-03-17",
          "value": 326688.0
        },
        {
          "date": "2026-03-24",
          "value": 328210.0
        },
        {
          "date": "2026-03-31",
          "value": 345276.0
        },
        {
          "date": "2026-04-07",
          "value": 349373.0
        },
        {
          "date": "2026-04-14",
          "value": 354344.0
        },
        {
          "date": "2026-04-21",
          "value": 351782.0
        },
        {
          "date": "2026-04-28",
          "value": 372780.0
        },
        {
          "date": "2026-05-05",
          "value": 354005.0
        },
        {
          "date": "2026-05-12",
          "value": 362042.0
        },
        {
          "date": "2026-05-19",
          "value": 396573.0
        },
        {
          "date": "2026-05-26",
          "value": 427294.0
        },
        {
          "date": "2026-06-02",
          "value": 505555.0
        },
        {
          "date": "2026-06-09",
          "value": 505075.0
        },
        {
          "date": "2026-06-16",
          "value": 520825.0
        },
        {
          "date": "2026-06-23",
          "value": 431030.0
        },
        {
          "date": "2026-06-30",
          "value": 438825.0
        }
      ],
      "USDJPY_VOL20": [
        {
          "date": "2025-06-02",
          "value": 11.998406665389783
        },
        {
          "date": "2025-06-03",
          "value": 11.799519213141467
        },
        {
          "date": "2025-06-04",
          "value": 11.253441897618716
        },
        {
          "date": "2025-06-05",
          "value": 11.041724583677576
        },
        {
          "date": "2025-06-06",
          "value": 10.921278092618298
        },
        {
          "date": "2025-06-09",
          "value": 8.280098366477704
        },
        {
          "date": "2025-06-10",
          "value": 8.511929585312664
        },
        {
          "date": "2025-06-11",
          "value": 8.40636347691232
        },
        {
          "date": "2025-06-12",
          "value": 8.538546523388623
        },
        {
          "date": "2025-06-13",
          "value": 8.425731580636423
        },
        {
          "date": "2025-06-16",
          "value": 8.454967731720384
        },
        {
          "date": "2025-06-17",
          "value": 8.310084451597183
        },
        {
          "date": "2025-06-18",
          "value": 8.333639816403334
        },
        {
          "date": "2025-06-19",
          "value": 8.04822005096808
        },
        {
          "date": "2025-06-20",
          "value": 8.041991889366415
        },
        {
          "date": "2025-06-23",
          "value": 9.031185414610848
        },
        {
          "date": "2025-06-24",
          "value": 10.377066036281485
        },
        {
          "date": "2025-06-25",
          "value": 10.342018374890031
        },
        {
          "date": "2025-06-26",
          "value": 10.442218958657232
        },
        {
          "date": "2025-06-27",
          "value": 10.048719862246337
        },
        {
          "date": "2025-06-30",
          "value": 9.649467218770997
        },
        {
          "date": "2025-07-01",
          "value": 10.030965544671805
        },
        {
          "date": "2025-07-02",
          "value": 9.73288922434201
        },
        {
          "date": "2025-07-03",
          "value": 9.546898048617102
        },
        {
          "date": "2025-07-04",
          "value": 9.539169147242395
        },
        {
          "date": "2025-07-07",
          "value": 9.71343736220667
        },
        {
          "date": "2025-07-08",
          "value": 9.806181539828714
        },
        {
          "date": "2025-07-09",
          "value": 9.945282464713998
        },
        {
          "date": "2025-07-10",
          "value": 9.496420299880311
        },
        {
          "date": "2025-07-11",
          "value": 9.547246187691327
        },
        {
          "date": "2025-07-14",
          "value": 9.57072103924638
        },
        {
          "date": "2025-07-15",
          "value": 9.57100417352176
        },
        {
          "date": "2025-07-16",
          "value": 9.845002517674239
        },
        {
          "date": "2025-07-17",
          "value": 9.857610974422766
        },
        {
          "date": "2025-07-18",
          "value": 9.854241924320915
        },
        {
          "date": "2025-07-22",
          "value": 9.19235128079438
        },
        {
          "date": "2025-07-23",
          "value": 8.031643030705368
        },
        {
          "date": "2025-07-24",
          "value": 8.086880781400096
        },
        {
          "date": "2025-07-25",
          "value": 7.6117233685117025
        },
        {
          "date": "2025-07-28",
          "value": 7.796764222040897
        },
        {
          "date": "2025-07-29",
          "value": 7.673109549302945
        },
        {
          "date": "2025-07-30",
          "value": 7.17704717692314
        },
        {
          "date": "2025-07-31",
          "value": 7.474527631314764
        },
        {
          "date": "2025-08-01",
          "value": 7.703191140441359
        },
        {
          "date": "2025-08-04",
          "value": 10.464817313085153
        },
        {
          "date": "2025-08-05",
          "value": 10.460752510503129
        },
        {
          "date": "2025-08-06",
          "value": 10.294782236176562
        },
        {
          "date": "2025-08-07",
          "value": 10.299479359777997
        },
        {
          "date": "2025-08-08",
          "value": 10.259548232048767
        },
        {
          "date": "2025-08-12",
          "value": 10.407825965044088
        },
        {
          "date": "2025-08-13",
          "value": 10.515930031499032
        },
        {
          "date": "2025-08-14",
          "value": 10.730672152654027
        },
        {
          "date": "2025-08-15",
          "value": 10.38149772498261
        },
        {
          "date": "2025-08-18",
          "value": 10.461559465094671
        },
        {
          "date": "2025-08-19",
          "value": 10.48580137922888
        },
        {
          "date": "2025-08-20",
          "value": 10.176114300243004
        },
        {
          "date": "2025-08-21",
          "value": 9.872583017407754
        },
        {
          "date": "2025-08-22",
          "value": 10.093891466647658
        },
        {
          "date": "2025-08-25",
          "value": 10.36596497851871
        },
        {
          "date": "2025-08-26",
          "value": 10.152136050711668
        },
        {
          "date": "2025-08-27",
          "value": 10.123995770386454
        },
        {
          "date": "2025-08-28",
          "value": 10.154639104301506
        },
        {
          "date": "2025-08-29",
          "value": 9.575440421010585
        },
        {
          "date": "2025-09-01",
          "value": 9.056244676909413
        },
        {
          "date": "2025-09-02",
          "value": 7.644229837680817
        },
        {
          "date": "2025-09-03",
          "value": 7.517374484624943
        },
        {
          "date": "2025-09-04",
          "value": 7.578505997118345
        },
        {
          "date": "2025-09-05",
          "value": 7.330897698546207
        },
        {
          "date": "2025-09-08",
          "value": 7.458363803627546
        },
        {
          "date": "2025-09-09",
          "value": 7.098004420884707
        },
        {
          "date": "2025-09-10",
          "value": 6.918715162239134
        },
        {
          "date": "2025-09-11",
          "value": 6.487295519124077
        },
        {
          "date": "2025-09-12",
          "value": 6.4695807145304585
        },
        {
          "date": "2025-09-16",
          "value": 6.5244496885646
        },
        {
          "date": "2025-09-17",
          "value": 6.500324651229214
        },
        {
          "date": "2025-09-18",
          "value": 6.611477800866805
        },
        {
          "date": "2025-09-19",
          "value": 6.916761079606706
        },
        {
          "date": "2025-09-22",
          "value": 6.458425400486233
        },
        {
          "date": "2025-09-24",
          "value": 5.647144244575187
        },
        {
          "date": "2025-09-25",
          "value": 5.872024902713536
        },
        {
          "date": "2025-09-26",
          "value": 6.303047494794789
        },
        {
          "date": "2025-09-29",
          "value": 6.922138407461423
        },
        {
          "date": "2025-09-30",
          "value": 7.036936563582813
        },
        {
          "date": "2025-10-01",
          "value": 7.438599030207538
        },
        {
          "date": "2025-10-02",
          "value": 6.280981802753427
        },
        {
          "date": "2025-10-03",
          "value": 6.346728143469314
        },
        {
          "date": "2025-10-06",
          "value": 8.949326196577287
        },
        {
          "date": "2025-10-07",
          "value": 9.010890425431905
        },
        {
          "date": "2025-10-08",
          "value": 9.709301930293531
        },
        {
          "date": "2025-10-09",
          "value": 9.622336551466272
        },
        {
          "date": "2025-10-10",
          "value": 9.697079103604365
        },
        {
          "date": "2025-10-14",
          "value": 10.060515596317412
        },
        {
          "date": "2025-10-15",
          "value": 10.222280751312427
        },
        {
          "date": "2025-10-16",
          "value": 10.056279561675245
        },
        {
          "date": "2025-10-17",
          "value": 10.835137606884402
        },
        {
          "date": "2025-10-20",
          "value": 11.016485179473099
        },
        {
          "date": "2025-10-21",
          "value": 10.913712675704057
        },
        {
          "date": "2025-10-22",
          "value": 10.978308465718142
        },
        {
          "date": "2025-10-23",
          "value": 11.01396989473499
        },
        {
          "date": "2025-10-24",
          "value": 10.930963029626135
        },
        {
          "date": "2025-10-27",
          "value": 10.736388250794354
        },
        {
          "date": "2025-10-28",
          "value": 10.44673996521385
        },
        {
          "date": "2025-10-29",
          "value": 10.333259311155674
        },
        {
          "date": "2025-10-30",
          "value": 10.250050713605772
        },
        {
          "date": "2025-10-31",
          "value": 10.283719932103699
        },
        {
          "date": "2025-11-04",
          "value": 10.586566968305032
        },
        {
          "date": "2025-11-05",
          "value": 8.878505912191336
        },
        {
          "date": "2025-11-06",
          "value": 8.820566380574684
        },
        {
          "date": "2025-11-07",
          "value": 7.758212610350109
        },
        {
          "date": "2025-11-10",
          "value": 7.818918368337184
        },
        {
          "date": "2025-11-11",
          "value": 7.793292378720398
        },
        {
          "date": "2025-11-12",
          "value": 7.474338512638577
        },
        {
          "date": "2025-11-13",
          "value": 7.176329705953662
        },
        {
          "date": "2025-11-14",
          "value": 7.180922435288249
        },
        {
          "date": "2025-11-17",
          "value": 5.842496018893482
        },
        {
          "date": "2025-11-18",
          "value": 5.5038163179800526
        },
        {
          "date": "2025-11-19",
          "value": 5.52858138876853
        },
        {
          "date": "2025-11-20",
          "value": 6.702664350684014
        },
        {
          "date": "2025-11-21",
          "value": 6.996014137845371
        },
        {
          "date": "2025-11-25",
          "value": 7.026881374283528
        },
        {
          "date": "2025-11-26",
          "value": 7.097818657112037
        },
        {
          "date": "2025-11-27",
          "value": 6.724426739820285
        },
        {
          "date": "2025-11-28",
          "value": 6.685304442391793
        },
        {
          "date": "2025-12-01",
          "value": 6.535176984788809
        },
        {
          "date": "2025-12-02",
          "value": 6.30562568423936
        },
        {
          "date": "2025-12-03",
          "value": 6.0216247122716755
        },
        {
          "date": "2025-12-04",
          "value": 6.142665802164351
        },
        {
          "date": "2025-12-05",
          "value": 6.318561892884937
        },
        {
          "date": "2025-12-08",
          "value": 6.3759420892715575
        },
        {
          "date": "2025-12-09",
          "value": 6.470711637339585
        },
        {
          "date": "2025-12-10",
          "value": 6.519707983197534
        },
        {
          "date": "2025-12-11",
          "value": 6.679040490127866
        },
        {
          "date": "2025-12-12",
          "value": 6.76399881178735
        },
        {
          "date": "2025-12-15",
          "value": 6.835412262089763
        },
        {
          "date": "2025-12-16",
          "value": 6.896273009219665
        },
        {
          "date": "2025-12-17",
          "value": 6.998898235013263
        },
        {
          "date": "2025-12-18",
          "value": 6.966421271783528
        },
        {
          "date": "2025-12-19",
          "value": 5.622651892570745
        },
        {
          "date": "2025-12-22",
          "value": 5.642588923926893
        },
        {
          "date": "2025-12-23",
          "value": 6.524537406929914
        },
        {
          "date": "2025-12-24",
          "value": 6.524700499565708
        },
        {
          "date": "2025-12-25",
          "value": 6.512477133959529
        },
        {
          "date": "2025-12-26",
          "value": 6.551307642809126
        },
        {
          "date": "2025-12-29",
          "value": 6.198258698525095
        },
        {
          "date": "2025-12-30",
          "value": 6.145027200920616
        },
        {
          "date": "2026-01-05",
          "value": 6.534793831762434
        },
        {
          "date": "2026-01-06",
          "value": 6.637578647576644
        },
        {
          "date": "2026-01-07",
          "value": 6.4376302660654
        },
        {
          "date": "2026-01-08",
          "value": 6.2542089744118305
        },
        {
          "date": "2026-01-09",
          "value": 6.383250570107456
        },
        {
          "date": "2026-01-13",
          "value": 7.067158079424517
        },
        {
          "date": "2026-01-14",
          "value": 6.8545188664416
        },
        {
          "date": "2026-01-15",
          "value": 6.944996241476102
        },
        {
          "date": "2026-01-16",
          "value": 6.9545873515796055
        },
        {
          "date": "2026-01-19",
          "value": 6.871101808795845
        },
        {
          "date": "2026-01-20",
          "value": 6.794170395231393
        },
        {
          "date": "2026-01-21",
          "value": 6.882934652013092
        },
        {
          "date": "2026-01-22",
          "value": 6.905359635530453
        },
        {
          "date": "2026-01-23",
          "value": 6.808628237133958
        },
        {
          "date": "2026-01-26",
          "value": 11.29240200751406
        },
        {
          "date": "2026-01-27",
          "value": 11.354595541664319
        },
        {
          "date": "2026-01-28",
          "value": 12.258099708418094
        },
        {
          "date": "2026-01-29",
          "value": 12.361338092310376
        },
        {
          "date": "2026-01-30",
          "value": 12.438168172854997
        },
        {
          "date": "2026-02-02",
          "value": 12.742775365077097
        },
        {
          "date": "2026-02-03",
          "value": 12.574085692378024
        },
        {
          "date": "2026-02-04",
          "value": 12.734503339780778
        },
        {
          "date": "2026-02-05",
          "value": 12.825506591392532
        },
        {
          "date": "2026-02-06",
          "value": 12.838826848006441
        },
        {
          "date": "2026-02-09",
          "value": 12.630300123839493
        },
        {
          "date": "2026-02-10",
          "value": 12.294540776943164
        },
        {
          "date": "2026-02-12",
          "value": 13.419882699844997
        },
        {
          "date": "2026-02-13",
          "value": 13.49613963113582
        },
        {
          "date": "2026-02-16",
          "value": 13.49880442944171
        },
        {
          "date": "2026-02-17",
          "value": 13.494522714257231
        },
        {
          "date": "2026-02-18",
          "value": 13.579049812405477
        },
        {
          "date": "2026-02-19",
          "value": 14.007817440671289
        },
        {
          "date": "2026-02-20",
          "value": 13.904010029663707
        },
        {
          "date": "2026-02-24",
          "value": 14.001703488671094
        },
        {
          "date": "2026-02-25",
          "value": 10.212434821030996
        },
        {
          "date": "2026-02-26",
          "value": 10.172393735900991
        },
        {
          "date": "2026-02-27",
          "value": 8.73842407658084
        },
        {
          "date": "2026-03-02",
          "value": 8.812981798471483
        },
        {
          "date": "2026-03-03",
          "value": 8.804524692668725
        },
        {
          "date": "2026-03-04",
          "value": 8.52682269289957
        },
        {
          "date": "2026-03-05",
          "value": 8.50284085687188
        },
        {
          "date": "2026-03-06",
          "value": 8.224297672971812
        },
        {
          "date": "2026-03-09",
          "value": 8.331870061264699
        },
        {
          "date": "2026-03-10",
          "value": 8.745191209855049
        },
        {
          "date": "2026-03-11",
          "value": 8.931695914941388
        },
        {
          "date": "2026-03-12",
          "value": 8.580506480947966
        },
        {
          "date": "2026-03-13",
          "value": 5.548582827082594
        },
        {
          "date": "2026-03-16",
          "value": 5.640791807534337
        },
        {
          "date": "2026-03-17",
          "value": 5.64345663264703
        },
        {
          "date": "2026-03-18",
          "value": 5.758842970294824
        },
        {
          "date": "2026-03-19",
          "value": 5.72263152835582
        },
        {
          "date": "2026-03-23",
          "value": 5.175900181582896
        },
        {
          "date": "2026-03-24",
          "value": 5.897028087622037
        },
        {
          "date": "2026-03-25",
          "value": 5.904789818584628
        },
        {
          "date": "2026-03-26",
          "value": 5.863464433704303
        },
        {
          "date": "2026-03-27",
          "value": 5.891521559678016
        },
        {
          "date": "2026-03-30",
          "value": 5.940363474456391
        },
        {
          "date": "2026-03-31",
          "value": 5.726854894418104
        },
        {
          "date": "2026-04-01",
          "value": 6.062018558018296
        },
        {
          "date": "2026-04-02",
          "value": 6.258831935350175
        },
        {
          "date": "2026-04-03",
          "value": 6.220267035095591
        },
        {
          "date": "2026-04-06",
          "value": 6.2511544185707395
        },
        {
          "date": "2026-04-07",
          "value": 6.016941965530517
        },
        {
          "date": "2026-04-08",
          "value": 6.636890281853396
        },
        {
          "date": "2026-04-09",
          "value": 6.538252341072069
        },
        {
          "date": "2026-04-10",
          "value": 6.469537053498047
        },
        {
          "date": "2026-04-13",
          "value": 6.340268810618875
        },
        {
          "date": "2026-04-14",
          "value": 6.4510249091318235
        },
        {
          "date": "2026-04-15",
          "value": 6.455709440153481
        },
        {
          "date": "2026-04-16",
          "value": 6.372692716214677
        },
        {
          "date": "2026-04-17",
          "value": 6.355266657335283
        },
        {
          "date": "2026-04-20",
          "value": 6.328228001944258
        },
        {
          "date": "2026-04-21",
          "value": 5.818872438837822
        },
        {
          "date": "2026-04-22",
          "value": 5.65548580453372
        },
        {
          "date": "2026-04-23",
          "value": 5.66216138742934
        },
        {
          "date": "2026-04-24",
          "value": 5.569946358687419
        },
        {
          "date": "2026-04-27",
          "value": 5.641549316882149
        },
        {
          "date": "2026-04-28",
          "value": 5.676491896222666
        },
        {
          "date": "2026-04-30",
          "value": 5.484914956612559
        },
        {
          "date": "2026-05-01",
          "value": 9.521507113689466
        },
        {
          "date": "2026-05-07",
          "value": 9.522553302852547
        },
        {
          "date": "2026-05-08",
          "value": 9.665488747180891
        },
        {
          "date": "2026-05-11",
          "value": 9.60774978127863
        },
        {
          "date": "2026-05-12",
          "value": 8.974432652590588
        },
        {
          "date": "2026-05-13",
          "value": 8.826666524668823
        },
        {
          "date": "2026-05-14",
          "value": 8.774292724620556
        },
        {
          "date": "2026-05-15",
          "value": 8.84575386660027
        },
        {
          "date": "2026-05-18",
          "value": 8.847894401776763
        },
        {
          "date": "2026-05-19",
          "value": 8.846614526032198
        },
        {
          "date": "2026-05-20",
          "value": 8.844981419171399
        },
        {
          "date": "2026-05-21",
          "value": 8.797660561016134
        },
        {
          "date": "2026-05-22",
          "value": 8.774289513207547
        },
        {
          "date": "2026-05-25",
          "value": 8.781532659460469
        },
        {
          "date": "2026-05-26",
          "value": 8.785417700953662
        },
        {
          "date": "2026-05-27",
          "value": 8.749217673398519
        },
        {
          "date": "2026-05-28",
          "value": 8.751124843628446
        },
        {
          "date": "2026-05-29",
          "value": 8.705887759975077
        },
        {
          "date": "2026-06-01",
          "value": 8.692615975356542
        },
        {
          "date": "2026-06-02",
          "value": 8.592454182139992
        },
        {
          "date": "2026-06-03",
          "value": 2.415484550556715
        },
        {
          "date": "2026-06-04",
          "value": 2.0958462243692515
        },
        {
          "date": "2026-06-05",
          "value": 1.894087603629379
        },
        {
          "date": "2026-06-08",
          "value": 1.892180842178366
        },
        {
          "date": "2026-06-09",
          "value": 1.8482042453420418
        },
        {
          "date": "2026-06-10",
          "value": 1.7881155332598375
        },
        {
          "date": "2026-06-11",
          "value": 1.7849476981022583
        },
        {
          "date": "2026-06-12",
          "value": 1.7007221398648593
        },
        {
          "date": "2026-06-15",
          "value": 1.5147566356304047
        },
        {
          "date": "2026-06-16",
          "value": 1.513076823492419
        },
        {
          "date": "2026-06-17",
          "value": 1.5280741573328824
        },
        {
          "date": "2026-06-18",
          "value": 1.6969671320678097
        },
        {
          "date": "2026-06-19",
          "value": 2.2095686211992636
        },
        {
          "date": "2026-06-22",
          "value": 2.2146506681351728
        },
        {
          "date": "2026-06-23",
          "value": 2.3682712631720784
        },
        {
          "date": "2026-06-24",
          "value": 2.3822755691270787
        },
        {
          "date": "2026-06-25",
          "value": 2.382592188780257
        },
        {
          "date": "2026-06-26",
          "value": 2.373888023653078
        },
        {
          "date": "2026-06-29",
          "value": 2.3733653520142317
        },
        {
          "date": "2026-06-30",
          "value": 2.460795247403947
        },
        {
          "date": "2026-07-01",
          "value": 2.52562080703534
        },
        {
          "date": "2026-07-02",
          "value": 3.949486141774603
        },
        {
          "date": "2026-07-03",
          "value": 4.2711713955841635
        },
        {
          "date": "2026-07-06",
          "value": 5.184829354584157
        },
        {
          "date": "2026-07-07",
          "value": 5.219157410224872
        }
      ]
    },
    "sources": [
      {
        "name": "BOJ Time-Series Data Search API",
        "url": "https://www.stat-search.boj.or.jp/api/v1/getDataCode",
        "items": [
          "FM08/FXERD04 USDJPY",
          "FM01/STRDCLUCON call rate",
          "FM09 NEER/REER"
        ]
      },
      {
        "name": "MOF JGB constant-maturity CSV",
        "url": "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/historical/jgbcme_all.csv",
        "items": [
          "2Y/10Y/30Y JGB yields"
        ]
      },
      {
        "name": "CFTC Public Reporting API",
        "url": "https://publicreporting.cftc.gov/resource/6dca-aqww.json?cftc_contract_market_code=097741&%24limit=130&%24order=report_date_as_yyyy_mm_dd+DESC",
        "items": [
          "JPY futures non-commercial positioning"
        ]
      },
      {
        "name": "FRED",
        "url": "https://fred.stlouisfed.org/",
        "items": [
          "DGS2/DGS10",
          "VIXCLS",
          "BAMLH0A0HYM2"
        ]
      }
    ],
    "notes": [],
    "chart_ids": [
      "jpy_usdjpy_funding_1y",
      "jpy_jgb_curve_1y",
      "jpy_cftc_position_2y",
      "jpy_effective_fx_3y",
      "us_jp_spread",
      "jpy_cftc_gross_2y",
      "jpy_cftc_short_share_2y"
    ]
  },
  "indicator_groups": [
    {
      "id": "front_end_rates",
      "title": "短端资金利率",
      "description": "观察银行间与回购市场资金价格是否偏离政策锚。",
      "indicators": [
        {
          "id": "EFFR",
          "label": "EFFR（有效联邦基金利率）",
          "category": "银行间/回购融资",
          "value": 3.63,
          "value_text": "3.630%",
          "unit": "%",
          "previous": 3.63,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "银行间无抵押隔夜资金价格，最能观察准备金边际是否稀缺。",
          "frequency": "日频，纽约联储约 9:00 ET 发布",
          "data_lag": "反映上一工作日交易",
          "comparison_basis": "与上一条有效工作日观测比较，不按自然日补零。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/unsecured/effr/last/2.json",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "SOFR",
          "label": "SOFR（担保隔夜融资利率）",
          "category": "银行间/回购融资",
          "value": 3.62,
          "value_text": "3.620%",
          "unit": "%",
          "previous": 3.63,
          "change": -0.009999999999999787,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "以美国国债为抵押的隔夜融资价格，反映回购市场和抵押品融资压力。",
          "frequency": "日频，纽约联储约 8:00 ET 发布",
          "data_lag": "反映上一工作日回购交易，约 14:30 ET 可能同日修订",
          "comparison_basis": "与上一条有效工作日观测比较。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/secured/sofr/last/2.json",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "OBFR",
          "label": "OBFR（隔夜银行融资利率）",
          "category": "银行间/回购融资",
          "value": 3.62,
          "value_text": "3.620%",
          "unit": "%",
          "previous": 3.62,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "更广义的银行隔夜融资成本，观察压力是否从联邦基金市场扩散。",
          "frequency": "日频，纽约联储参考利率",
          "data_lag": "通常反映上一工作日交易",
          "comparison_basis": "与上一条有效工作日观测比较。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/unsecured/obfr/last/2.json",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "TGCR",
          "label": "TGCR（三方一般抵押品利率）",
          "category": "银行间/回购融资",
          "value": 3.6,
          "value_text": "3.600%",
          "unit": "%",
          "previous": 3.61,
          "change": -0.009999999999999787,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "三方回购市场的一般抵押品融资成本，反映机构化回购资金价格。",
          "frequency": "日频，纽约联储约 8:00 ET 发布",
          "data_lag": "反映上一工作日三方回购交易，可能同日修订",
          "comparison_basis": "与上一条有效工作日观测比较。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/secured/tgcr/last/2.json",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "BGCR",
          "label": "BGCR（广义一般抵押品利率）",
          "category": "银行间/回购融资",
          "value": 3.6,
          "value_text": "3.600%",
          "unit": "%",
          "previous": 3.61,
          "change": -0.009999999999999787,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "覆盖更广的一般抵押品回购利率，观察回购市场结构性扰动。",
          "frequency": "日频，纽约联储约 8:00 ET 发布",
          "data_lag": "反映上一工作日广义一般抵押品回购交易，可能同日修订",
          "comparison_basis": "与上一条有效工作日观测比较。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/secured/bgcr/last/2.json",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "IORB",
          "label": "IORB（准备金余额利率）",
          "category": "政策锚",
          "value": 3.65,
          "value_text": "3.650%",
          "unit": "%",
          "previous": 3.65,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-07-09",
          "previous_as_of": "2026-07-08",
          "meaning": "美联储支付给银行准备金的利率，是银行持有准备金的政策锚。",
          "frequency": "政策阶梯型，美联储政策利率",
          "data_lag": "只有政策调整时变化",
          "comparison_basis": "不做普通日度环比；用于锚定EFFR和SOFR。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/IORB",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "POLICY_UPPER_NYFED",
          "label": "POLICY_UPPER_NYFED（纽约联储政策上限）",
          "category": "政策锚",
          "value": 3.75,
          "value_text": "3.750%",
          "unit": "%",
          "previous": 3.75,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "纽约联储记录中的政策利率上限；当 IORB/FRED 不可用时，用作临时政策锚。",
          "frequency": "政策阶梯型，纽约联储记录中的目标上限",
          "data_lag": "来自EFFR记录，作为IORB缺失时的临时锚",
          "comparison_basis": "只用于锚定，不代表市场日度变化。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/unsecured/effr/last/2.json",
          "status": "ok",
          "notes": "Fallback policy anchor when IORB/FRED is unavailable; not identical to IORB"
        }
      ]
    },
    {
      "id": "fed_liability",
      "title": "Fed负债端水位",
      "description": "观察TGA、RRP、SOMA与准备金水位对银行体系流动性的影响。",
      "indicators": [
        {
          "id": "TGA",
          "label": "TGA（财政部一般账户）",
          "category": "Fed负债端",
          "value": null,
          "value_text": "NA",
          "unit": "USD bn",
          "previous": null,
          "change": null,
          "change_text": "NA",
          "change_direction": "unknown",
          "as_of": null,
          "previous_as_of": null,
          "meaning": "财政部现金余额，余额上升通常抽走银行体系准备金，下降通常释放准备金。",
          "frequency": "日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布",
          "data_lag": "覆盖上一工作日财政现金和债务操作",
          "comparison_basis": "与上一条有效工作日观测比较，不能与当天市场利率强行同日对齐。",
          "freshness": "error",
          "importance": "high",
          "interpretation_hint": "",
          "source": "Treasury FiscalData",
          "source_url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90",
          "status": "error",
          "notes": "GET failed: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90 | HTTPSConnectionPool(host='api.fiscaldata.treasury.gov', port=443): Read timed out. (read timeout=10)"
        },
        {
          "id": "RRPONTSYD",
          "label": "RRP（隔夜逆回购）",
          "category": "Fed负债端",
          "value": 3.347,
          "value_text": "3.3bn",
          "unit": "USD bn",
          "previous": 4.484,
          "change": -1.137,
          "change_text": "-1.1bn",
          "change_direction": "down",
          "as_of": "2026-07-08",
          "previous_as_of": "2026-07-07",
          "meaning": "货币基金等机构停放在美联储的隔夜逆回购余额，是准备金压力前的缓冲垫。",
          "frequency": "日频，纽约联储每日操作结果",
          "data_lag": "同日操作结果，工作日/操作日口径",
          "comparison_basis": "与上一条操作日观测比较。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?startDate=2026-06-25&endDate=2026-07-09",
          "status": "ok",
          "notes": "NY Fed reverse repo accepted amount; replaces FRED RRPONTSYD when FRED is slow or unavailable"
        },
        {
          "id": "SOMA",
          "label": "SOMA（系统公开市场账户持仓）",
          "category": "Fed负债端",
          "value": 6334.4721750830995,
          "value_text": "6,334.5bn",
          "unit": "USD bn",
          "previous": 6344.3455674457,
          "change": -9.873392362600498,
          "change_text": "-9.9bn",
          "change_direction": "down",
          "as_of": "2026-07-01",
          "previous_as_of": "2026-06-24",
          "meaning": "美联储公开市场账户持仓，反映QT和资产端收缩的结构背景。",
          "frequency": "周频，纽约联储/Fed资产负债表背景数据",
          "data_lag": "周度持仓或H.4.1口径",
          "comparison_basis": "只与上一周比较，不能当作昨日边际变化。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/soma/summary.json",
          "status": "ok",
          "notes": "SOMA endpoint schema may change; use as weekly QT background"
        },
        {
          "id": "WRESBAL",
          "label": "WRESBAL（银行准备金余额）",
          "category": "Fed负债端",
          "value": 2966.897,
          "value_text": "2,966.9bn",
          "unit": "USD bn",
          "previous": 2951.416,
          "change": 15.480999999999767,
          "change_text": "+15.5bn",
          "change_direction": "up",
          "as_of": "2026-07-01",
          "previous_as_of": "2026-06-24",
          "meaning": "银行体系准备金余额，是美元流动性水位的核心变量，但发布频率较低。",
          "frequency": "周频，H.4.1 通常周四 16:30 ET 发布",
          "data_lag": "反映周度准备金余额",
          "comparison_basis": "只与上一周比较，作为结构背景。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/WRESBAL",
          "status": "ok",
          "notes": ""
        }
      ]
    },
    {
      "id": "treasury_curve",
      "title": "国债收益率与曲线",
      "description": "观察1Y、3Y、10Y收益率组合、真实折现率和曲线利差的变化。",
      "indicators": [
        {
          "id": "DGS1",
          "label": "1Y Treasury Yield（1年期美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 4.06,
          "value_text": "4.060%",
          "unit": "%",
          "previous": 3.95,
          "change": 0.10999999999999943,
          "change_text": "+11.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "1年期美国国债收益率，主要反映未来一年政策利率路径和短端再定价。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看未来一年政策路径。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS1",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DGS3",
          "label": "3Y Treasury Yield（3年期美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 4.18,
          "value_text": "4.180%",
          "unit": "%",
          "previous": 4.14,
          "change": 0.040000000000000036,
          "change_text": "+4.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "3年期美国国债收益率，观察政策路径从短端向中段扩散的再定价。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看中段政策路径再定价。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS3",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DGS10",
          "label": "10Y Treasury Yield（10年期美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 4.55,
          "value_text": "4.550%",
          "unit": "%",
          "previous": 4.48,
          "change": 0.0699999999999994,
          "change_text": "+7.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "10年期美国国债收益率，是全球资产折现率和长期美元资金价格的重要锚。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看长期折现率。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS10",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DFII10",
          "label": "10Y Real Yield（10年期TIPS实际收益率）",
          "category": "国债收益率/曲线",
          "value": 2.3,
          "value_text": "2.300%",
          "unit": "%",
          "previous": 2.24,
          "change": 0.05999999999999961,
          "change_text": "+6.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "10年期TIPS实际收益率，剔除通胀补偿后观察真实无风险回报，对成长股、黄金和长期资产估值更敏感。",
          "frequency": "日频，FRED/H.15 10年期TIPS实际收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看真实贴现率。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DFII10",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DGS30",
          "label": "30Y Treasury Yield（30年期美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 5.05,
          "value_text": "5.050%",
          "unit": "%",
          "previous": 4.99,
          "change": 0.05999999999999961,
          "change_text": "+6.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "30年期美国国债收益率，反映长期通胀、财政供给和期限溢价。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看长期期限溢价。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS30",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "T10Y2Y",
          "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
          "category": "国债收益率/曲线",
          "value": 0.35,
          "value_text": "0.350%",
          "unit": "%",
          "previous": 0.36,
          "change": -0.010000000000000009,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-08",
          "previous_as_of": "2026-07-07",
          "meaning": "10年减2年美债利差，观察收益率曲线是否倒挂以及增长/降息预期。",
          "frequency": "日频，FRED曲线利差",
          "data_lag": "由10年和2年国债收益率差计算",
          "comparison_basis": "与上一条有效观测比较；倒挂或加深倒挂反映增长/降息预期。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/T10Y2Y",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "T10Y3M",
          "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
          "category": "国债收益率/曲线",
          "value": 0.69,
          "value_text": "0.690%",
          "unit": "%",
          "previous": 0.69,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-07-08",
          "previous_as_of": "2026-07-07",
          "meaning": "10年减3个月美债利差，观察政策短端与长期增长预期的差异。",
          "frequency": "日频，FRED曲线利差",
          "data_lag": "由10年和3个月国债收益率差计算",
          "comparison_basis": "与上一条有效观测比较；常用于观察衰退预期。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/T10Y3M",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DTB3",
          "label": "3M T-bill Rate（3个月美国国库券二级市场利率）",
          "category": "国债收益率/曲线",
          "value": 3.73,
          "value_text": "3.730%",
          "unit": "%",
          "previous": 3.74,
          "change": -0.010000000000000231,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "3个月国库券二级市场利率，代表现金/货币基金可获得的短端无风险替代收益。",
          "frequency": "日频，3个月国库券二级市场利率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看现金替代收益。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DTB3",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DGS3MO",
          "label": "3M Treasury Yield（3个月美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 3.86,
          "value_text": "3.860%",
          "unit": "%",
          "previous": 3.87,
          "change": -0.010000000000000231,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "3个月美国国债收益率，主要受当前政策利率和短端美元资金价格影响。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看政策短端。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS3MO",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DGS2",
          "label": "2Y Treasury Yield（2年期美国国债收益率）",
          "category": "国债收益率/曲线",
          "value": 4.19,
          "value_text": "4.190%",
          "unit": "%",
          "previous": 4.13,
          "change": 0.0600000000000005,
          "change_text": "+6.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "2年期美国国债收益率，主要反映未来数年美联储政策路径预期。",
          "frequency": "日频，FRED/H.15国债恒定期限收益率",
          "data_lag": "通常随H.15数据发布滞后更新",
          "comparison_basis": "与上一条有效观测比较，主要看政策路径预期。",
          "freshness": "ok",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DGS2",
          "status": "ok",
          "notes": ""
        }
      ]
    },
    {
      "id": "collateral_treasury",
      "title": "抵押品与国债吸收",
      "description": "观察SOFR交易量、T-bill拍卖量级/认购倍数、回购抵押品链条和交割压力。",
      "indicators": [
        {
          "id": "SOFR_VOLUME",
          "label": "SOFR Volume（SOFR交易量）",
          "category": "回购融资/市场深度",
          "value": 3154.0,
          "value_text": "3,154.0bn",
          "unit": "USD bn",
          "previous": 3212.0,
          "change": -58.0,
          "change_text": "-58.0bn",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "SOFR对应的隔夜回购交易量，用于把利率偏离转化为价格×规模的实际资金成本量级。",
          "frequency": "日频，纽约联储SOFR记录随利率一同发布",
          "data_lag": "反映上一工作日SOFR合格交易量",
          "comparison_basis": "与上一条有效工作日观测比较，并与SOFR相对政策锚利差相乘理解量级。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rates/secured/sofr/last/2.json",
          "status": "ok",
          "notes": "SOFR transaction volume reported by NY Fed in billions of dollars; use with SOFR-Policy spread to estimate price × size impact."
        },
        {
          "id": "TBILL_AUCTION_SIZE",
          "label": "T-bill Auction Size（短期国债拍卖规模）",
          "category": "国债/抵押品",
          "value": 142.0,
          "value_text": "142.0bn",
          "unit": "USD bn",
          "previous": 171.0,
          "change": -29.0,
          "change_text": "-29.0bn",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "短期国债拍卖发行规模，观察货币基金、银行和交易商需要吸收的新增/滚续短债供给量级。",
          "frequency": "事件驱动，财政部T-bill拍卖后公布",
          "data_lag": "同一拍卖日多只Bill按发行额加总",
          "comparison_basis": "与上一T-bill拍卖日比较，并与认购倍数一起判断供给吸收压力。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-18&endDate=2026-07-09",
          "status": "ok",
          "notes": "Aggregates all Treasury Bill auctions on the latest auction date; bid-to-cover is offering-amount weighted. Latest terms: 52-Week, 6-Week."
        },
        {
          "id": "TBILL_AUCTION_BTC",
          "label": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
          "category": "国债/抵押品",
          "value": 2.8864788732394366,
          "value_text": "2.89x",
          "unit": "ratio",
          "previous": 2.7971345029239765,
          "change": 0.08934437031546016,
          "change_text": "+0.09x",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "短期国债拍卖投标覆盖倍数，和拍卖规模一起观察T-bill供给吸收压力。",
          "frequency": "事件驱动，财政部T-bill拍卖后公布",
          "data_lag": "同一拍卖日多只Bill按发行额加权平均",
          "comparison_basis": "与上一T-bill拍卖日比较；必须结合拍卖规模，不能只看倍数。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-18&endDate=2026-07-09",
          "status": "ok",
          "notes": "Aggregates all Treasury Bill auctions on the latest auction date; bid-to-cover is offering-amount weighted. Latest terms: 52-Week, 6-Week."
        },
        {
          "id": "UST_AUCTION_BTC",
          "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
          "category": "国债/抵押品",
          "value": 3.14,
          "value_text": "3.14x",
          "unit": "ratio",
          "previous": 2.74,
          "change": 0.3999999999999999,
          "change_text": "+0.40x",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-07",
          "meaning": "国债拍卖需求强弱代理指标，观察国债供给吸收能力。",
          "frequency": "事件驱动，财政部拍卖后公布",
          "data_lag": "只在拍卖发生时更新",
          "comparison_basis": "与上一场可比拍卖比较，不能日度环比。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-18&endDate=2026-07-09",
          "status": "ok",
          "notes": "Uses bid-to-cover as free auction demand proxy; auction tail requires WI yield not available here"
        },
        {
          "id": "REPO_FAILS_UST",
          "label": "Repo Fails（美国国债回购交割失败）",
          "category": "国债/抵押品",
          "value": 91.889,
          "value_text": "91.9bn",
          "unit": "USD bn",
          "previous": 101.239,
          "change": -9.350000000000009,
          "change_text": "-9.4bn",
          "change_direction": "down",
          "as_of": "2026-06-24",
          "previous_as_of": "2026-06-17",
          "meaning": "回购和证券交割失败规模，观察抵押品链条和交割压力。",
          "frequency": "周频，OFR/STFM 或一级交易商口径",
          "data_lag": "交割失败周度背景",
          "comparison_basis": "只看周度趋势，不参与日度环比。",
          "freshness": "stale",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "OFR STFM",
          "source_url": "https://data.financialresearch.gov/v1/series/timeseries?mnemonic=NYPD-PD_AFtD_T-A",
          "status": "ok",
          "notes": "Optional OFR STFM series; if unavailable, do not block the main briefing"
        }
      ]
    },
    {
      "id": "offshore_credit",
      "title": "离岸美元、信用与金融条件",
      "description": "观察压力是否外溢到离岸美元、信用市场和综合金融条件。",
      "indicators": [
        {
          "id": "DTWEXBGS",
          "label": "DTWEXBGS（广义美元指数）",
          "category": "离岸美元",
          "value": 120.6902,
          "value_text": "120.69",
          "unit": "index",
          "previous": 121.1455,
          "change": -0.45529999999999404,
          "change_text": "-0.46",
          "change_direction": "down",
          "as_of": "2026-07-02",
          "previous_as_of": "2026-07-01",
          "meaning": "广义美元指数，作为离岸美元融资压力的替代观察。",
          "frequency": "日频，FRED/美联储美元指数口径",
          "data_lag": "通常随源数据滞后更新",
          "comparison_basis": "与上一条有效观测比较，注意可能比资金利率更滞后。",
          "freshness": "stale",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DTWEXBGS",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "DCPN3M",
          "label": "CP Rate（90天AA非金融商业票据利率）",
          "category": "信用传导",
          "value": 3.72,
          "value_text": "3.720%",
          "unit": "%",
          "previous": 3.67,
          "change": 0.050000000000000266,
          "change_text": "+5.0bp",
          "change_direction": "up",
          "as_of": "2026-06-26",
          "previous_as_of": "2026-06-17",
          "meaning": "企业短期融资价格，观察货币市场压力是否传导到商业票据。",
          "frequency": "日频，商业票据利率",
          "data_lag": "通常T+1或随源数据更新",
          "comparison_basis": "与上一条有效观测比较。",
          "freshness": "stale",
          "importance": "medium",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/DCPN3M",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "BAMLC0A0CM",
          "label": "IG OAS（投资级公司债期权调整利差）",
          "category": "信用传导",
          "value": 0.76,
          "value_text": "0.760%",
          "unit": "%",
          "previous": 0.75,
          "change": 0.010000000000000009,
          "change_text": "+1.0bp",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "投资级公司债信用利差，观察高等级企业融资成本和信用风险溢价。",
          "frequency": "日频，投资级公司债OAS",
          "data_lag": "通常随ICE/BofA数据更新",
          "comparison_basis": "与上一条有效观测比较，作为高等级信用融资条件确认。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/BAMLC0A0CM",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "BAMLH0A0HYM2",
          "label": "HY OAS（高收益债期权调整利差）",
          "category": "信用传导",
          "value": 2.67,
          "value_text": "2.670%",
          "unit": "%",
          "previous": 2.72,
          "change": -0.050000000000000266,
          "change_text": "-5.0bp",
          "change_direction": "down",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "高收益债信用利差，观察压力是否外溢到风险信用资产。",
          "frequency": "日频，高收益债OAS",
          "data_lag": "通常随ICE/BofA数据更新",
          "comparison_basis": "与上一条有效观测比较，作为信用传导而非银行间流动性核心。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "NFCI",
          "label": "NFCI（芝加哥联储全国金融条件指数）",
          "category": "金融条件",
          "value": -0.515,
          "value_text": "-0.52",
          "unit": "index",
          "previous": -0.505,
          "change": -0.010000000000000009,
          "change_text": "-0.01",
          "change_direction": "flat",
          "as_of": "2026-07-03",
          "previous_as_of": "2026-06-26",
          "meaning": "芝加哥联储全国金融条件指数，公开金融条件代理；正值偏紧，负值偏松。",
          "frequency": "周频，芝加哥联储全国金融条件指数",
          "data_lag": "通常每周更新",
          "comparison_basis": "只与上一周比较；正值偏紧，负值偏松。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/NFCI",
          "status": "ok",
          "notes": ""
        }
      ]
    },
    {
      "id": "securities_risk",
      "title": "证券市场风险偏好",
      "description": "观察利率和信用条件是否进一步反映到股票波动率和风险偏好。",
      "indicators": [
        {
          "id": "VIXCLS",
          "label": "VIX（标普500隐含波动率指数）",
          "category": "证券市场风险偏好",
          "value": 16.13,
          "value_text": "16.13",
          "unit": "index",
          "previous": 15.57,
          "change": 0.5599999999999987,
          "change_text": "+0.56",
          "change_direction": "up",
          "as_of": "2026-07-07",
          "previous_as_of": "2026-07-06",
          "meaning": "标普500隐含波动率指数，作为证券市场风险偏好和避险需求的确认指标。",
          "frequency": "日频，标普500隐含波动率",
          "data_lag": "通常随CBOE/FRED数据更新",
          "comparison_basis": "与上一条有效观测比较，作为证券市场风险偏好确认。",
          "freshness": "ok",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "FRED API",
          "source_url": "https://fred.stlouisfed.org/series/VIXCLS",
          "status": "ok",
          "notes": ""
        }
      ]
    }
  ],
  "derived_signals": [
    {
      "id": "SOFR_ANCHOR",
      "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
      "value": -2.9999999999999805,
      "value_text": "-3.0bp",
      "previous": -2.0000000000000018,
      "previous_text": "-2.0bp",
      "change": -0.9999999999999787,
      "change_text": "-1.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "SOFR相对IORB（准备金余额利率）的位置。回购融资与政策锚接近",
      "as_of": "2026-07-07"
    },
    {
      "id": "SOFR_VOLUME_IMPACT",
      "label": "SOFR Rate-Volume Impact（SOFR价格×交易量影响）",
      "value": -2.628333333333316,
      "value_text": "-2.6mn/day",
      "previous": -1.7844444444444458,
      "previous_text": "-1.8mn/day",
      "change": -0.8438888888888703,
      "change_text": "-0.8mn/day",
      "unit": "USD mn/day",
      "severity": "中性",
      "meaning": "SOFR交易量约3,154bn，但SOFR相对政策锚偏离有限，价格×规模冲击不大。",
      "as_of": "2026-07-07"
    },
    {
      "id": "BGCR_TGCR",
      "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
      "value": 0.0,
      "value_text": "0.0bp",
      "previous": 0.0,
      "previous_text": "0.0bp",
      "change": 0.0,
      "change_text": "0.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "比较广义回购与三方回购的结构差异。一般抵押品利率结构稳定",
      "as_of": "2026-07-07"
    },
    {
      "id": "CP_PROXY",
      "label": "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）",
      "value": -2.9999999999999805,
      "value_text": "-3.0bp",
      "previous": -8.000000000000007,
      "previous_text": "-8.0bp",
      "change": 5.000000000000027,
      "change_text": "+5.0bp",
      "unit": "bp",
      "severity": "偏松",
      "meaning": "用90天AA非金融商业票据利率减联邦基金目标上限，粗略观察企业短融相对政策利率是否变贵；这是信用传导代理指标，不是FRA-OIS。企业短融压力不明显",
      "as_of": "2026-06-26"
    },
    {
      "id": "RRP_FLOW",
      "label": "RRP Flow（隔夜逆回购边际流量）",
      "value": -1.137,
      "value_text": "-1.14bn",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "bn",
      "severity": "中性",
      "meaning": "RRP日变化幅度有限，短期边际流量影响不大。",
      "as_of": "2026-07-08"
    },
    {
      "id": "RRP_BUFFER",
      "label": "RRP Buffer（隔夜逆回购存量缓冲垫）",
      "value": 3.347,
      "value_text": "3.35bn",
      "previous": 4.484,
      "previous_text": "4.48bn",
      "change": -1.137,
      "change_text": "-1.1bn",
      "unit": "bn",
      "severity": "偏紧",
      "meaning": "RRP存量缓冲垫几乎耗尽，后续TGA补库、QT或美债供给冲击更容易直接落到准备金。",
      "as_of": "2026-07-08"
    },
    {
      "id": "UST_1Y_YIELD",
      "label": "1Y Treasury Yield（1年期美国国债收益率）",
      "value": 4.06,
      "value_text": "4.060%",
      "previous": 3.95,
      "previous_text": "3.950%",
      "change": 0.10999999999999943,
      "change_text": "+0.11%",
      "unit": "%",
      "severity": "中性",
      "meaning": "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价",
      "as_of": "2026-07-07"
    },
    {
      "id": "UST_3Y_YIELD",
      "label": "3Y Treasury Yield（3年期美国国债收益率）",
      "value": 4.18,
      "value_text": "4.180%",
      "previous": 4.14,
      "previous_text": "4.140%",
      "change": 0.040000000000000036,
      "change_text": "+0.04%",
      "unit": "%",
      "severity": "中性",
      "meaning": "3年期收益率处于中间区间，观察其相对1年和10年的斜率变化。",
      "as_of": "2026-07-07"
    },
    {
      "id": "NOMINAL_10Y",
      "label": "10Y Treasury Yield（10年期美国国债收益率）",
      "value": 4.55,
      "value_text": "4.550%",
      "previous": 4.48,
      "previous_text": "4.480%",
      "change": 0.0699999999999994,
      "change_text": "+0.07%",
      "unit": "%",
      "severity": "偏紧",
      "meaning": "长期名义折现率上行，债券久期和股票估值承压",
      "as_of": "2026-07-07"
    },
    {
      "id": "REAL_10Y",
      "label": "10Y Treasury Yield（10年期美国国债收益率）",
      "value": 4.55,
      "value_text": "4.550%",
      "previous": 4.48,
      "previous_text": "4.480%",
      "change": 0.0699999999999994,
      "change_text": "+0.07%",
      "unit": "%",
      "severity": "偏紧",
      "meaning": "10年期国债收益率处于高位，对长期资产估值有压力；这描述的是level风险，不代表边际继续恶化。",
      "as_of": "2026-07-07"
    },
    {
      "id": "REAL_10Y_MOMENTUM",
      "label": "10Y Yield Momentum（10年期国债收益率边际变化）",
      "value": 6.99999999999994,
      "value_text": "7.0bp",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "bp",
      "severity": "偏紧",
      "meaning": "10年期国债收益率边际上行，长期资产估值压力正在增强。",
      "as_of": "2026-07-07"
    },
    {
      "id": "HY_CHANGE",
      "label": "HY OAS Change（高收益债期权调整利差变化）",
      "value": 2.67,
      "value_text": "2.670%",
      "previous": 2.72,
      "previous_text": "2.720%",
      "change": -0.050000000000000266,
      "change_text": "-0.05%",
      "unit": "%",
      "severity": "偏松",
      "meaning": "信用风险偏好改善",
      "as_of": "2026-07-07"
    },
    {
      "id": "IG_CHANGE",
      "label": "IG OAS Change（投资级公司债期权调整利差变化）",
      "value": 0.76,
      "value_text": "0.760%",
      "previous": 0.75,
      "previous_text": "0.750%",
      "change": 0.010000000000000009,
      "change_text": "+0.01%",
      "unit": "%",
      "severity": "中性",
      "meaning": "投资级信用利差变化有限",
      "as_of": "2026-07-07"
    },
    {
      "id": "VIX_RISK",
      "label": "VIX Level（标普500隐含波动率水平）",
      "value": 16.13,
      "value_text": "16.13",
      "previous": 15.57,
      "previous_text": "15.57",
      "change": 0.5599999999999987,
      "change_text": "+0.56",
      "unit": "",
      "severity": "中性",
      "meaning": "证券市场波动率处于中性区间。",
      "as_of": "2026-07-07"
    },
    {
      "id": "VIX_MOMENTUM",
      "label": "VIX Momentum（标普500隐含波动率边际变化）",
      "value": 0.5599999999999987,
      "value_text": "0.56pt",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "pt",
      "severity": "中性",
      "meaning": "VIX边际变化有限。",
      "as_of": "2026-07-07"
    },
    {
      "id": "USD_CHANGE",
      "label": "Broad Dollar Index Change（广义美元指数变化）",
      "value": -0.45529999999999404,
      "value_text": "-0.46pt",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "pt",
      "severity": "偏松",
      "meaning": "外部美元压力缓和",
      "as_of": "2026-07-02"
    },
    {
      "id": "UST_10Y2Y",
      "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
      "value": 35.0,
      "value_text": "35.0bp",
      "previous": 36.0,
      "previous_text": "36.0bp",
      "change": -1.0,
      "change_text": "-1.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "收益率曲线为正，期限结构相对正常",
      "as_of": "2026-07-08"
    },
    {
      "id": "UST_10Y3M",
      "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
      "value": 69.0,
      "value_text": "69.0bp",
      "previous": 69.0,
      "previous_text": "69.0bp",
      "change": 0.0,
      "change_text": "0.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "10年-3个月曲线为正，政策短端对长期利率压制较弱",
      "as_of": "2026-07-08"
    },
    {
      "id": "NFCI_LEVEL",
      "label": "NFCI（芝加哥联储全国金融条件指数）",
      "value": -0.515,
      "value_text": "-0.52",
      "previous": -0.505,
      "previous_text": "-0.51",
      "change": -0.010000000000000009,
      "change_text": "-0.01",
      "unit": "",
      "severity": "偏松",
      "meaning": "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察",
      "as_of": "2026-07-03"
    },
    {
      "id": "TBILL_AUCTION_STRESS",
      "label": "T-bill Auction Stress Score（短债拍卖吸收压力评分）",
      "value": 40.0,
      "value_text": "40.00",
      "previous": 40.0,
      "previous_text": "40.00",
      "change": 0.0,
      "change_text": "0.00index",
      "unit": "index",
      "severity": "中性",
      "meaning": "最新T-bill拍卖规模约142.0bn，认购倍数2.89x，上一T-bill拍卖日认购倍数 2.80x；该分数综合供给规模与需求覆盖，数值越高表示吸收压力越大。供给吸收处于中性区间。",
      "as_of": "2026-07-07"
    },
    {
      "id": "AUCTION_BTC",
      "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
      "value": 3.14,
      "value_text": "3.14x",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "x",
      "severity": "偏松",
      "meaning": "拍卖需求较强，吸收压力不明显",
      "as_of": "2026-07-07"
    }
  ],
  "core_indicator_impacts": [
    {
      "indicator": "SOFR-IORB / SOFR-政策锚",
      "importance": "高",
      "reason": "观察回购和抵押品融资是否紧张；SOFR高于政策锚通常比单纯上升更重要。"
    },
    {
      "indicator": "SOFR交易量",
      "importance": "高",
      "reason": "把SOFR相对政策锚的价格偏离映射到实际回购融资规模；利率冲击的影响取决于交易量。"
    },
    {
      "indicator": "TGA",
      "importance": "高",
      "reason": "财政部现金余额上升会抽走准备金，下降会释放准备金，是Fed负债端最重要的日频水位之一。"
    },
    {
      "indicator": "RRP",
      "importance": "高",
      "reason": "RRP下降可释放缓冲，但余额过低后，QT和TGA补库更容易直接冲击准备金。"
    },
    {
      "indicator": "WRESBAL",
      "importance": "高但周频",
      "reason": "银行准备金本身是核心水位，但周频发布，适合看趋势而非日内或日度拐点。"
    },
    {
      "indicator": "TGCR/BGCR",
      "importance": "中高",
      "reason": "帮助确认SOFR变化是否是广泛回购市场压力，而非单点噪音。"
    },
    {
      "indicator": "T-bill拍卖规模 / bid-to-cover / repo fails",
      "importance": "中高",
      "reason": "观察短债供给吸收、货币基金现金分流和抵押品链条压力；拍卖倍数必须和发行规模一起看。"
    },
    {
      "indicator": "1Y / 3Y / 10Y国债收益率",
      "importance": "中高",
      "reason": "1年期看近端政策路径，3年期看中段再定价，10年期是全球折现率锚。"
    },
    {
      "indicator": "10Y实际收益率",
      "importance": "高",
      "reason": "真实无风险回报直接影响成长股、黄金和长期资产估值，是证券市场贴现率压力的核心代理。"
    },
    {
      "indicator": "美元指数 / CP利差 / IG OAS / HY OAS",
      "importance": "中高",
      "reason": "观察压力是否向离岸美元和信用市场扩散，属于传导确认指标。"
    },
    {
      "indicator": "10Y-2Y / 10Y-3M曲线利差",
      "importance": "中高",
      "reason": "长短端利差观察当前政策短端与增长、降息和衰退预期的相对关系。"
    },
    {
      "indicator": "VIX / NFCI / FCI代理",
      "importance": "中",
      "reason": "观察利率、信用、杠杆和风险资产综合后的证券市场风险偏好与金融条件。"
    }
  ],
  "charts": [
    {
      "id": "short_rates_7d",
      "title": "短端资金利率：最近一周",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "EFFR",
          "label": "EFFR（有效联邦基金利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": 3.63
            },
            {
              "date": "2026-06-30",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.63
            },
            {
              "date": "2026-07-03",
              "value": 3.63
            },
            {
              "date": "2026-07-06",
              "value": 3.63
            },
            {
              "date": "2026-07-07",
              "value": 3.63
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "SOFR",
          "label": "SOFR（担保隔夜融资利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": 3.62
            },
            {
              "date": "2026-06-30",
              "value": 3.68
            },
            {
              "date": "2026-07-01",
              "value": 3.66
            },
            {
              "date": "2026-07-02",
              "value": 3.64
            },
            {
              "date": "2026-07-06",
              "value": 3.63
            },
            {
              "date": "2026-07-07",
              "value": 3.62
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "TGCR",
          "label": "TGCR（三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": 3.6
            },
            {
              "date": "2026-06-30",
              "value": 3.64
            },
            {
              "date": "2026-07-01",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.62
            },
            {
              "date": "2026-07-06",
              "value": 3.61
            },
            {
              "date": "2026-07-07",
              "value": 3.6
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR",
          "label": "BGCR（广义一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": 3.6
            },
            {
              "date": "2026-06-30",
              "value": 3.64
            },
            {
              "date": "2026-07-01",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.62
            },
            {
              "date": "2026-07-06",
              "value": 3.61
            },
            {
              "date": "2026-07-07",
              "value": 3.6
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "short_rates_30d",
      "title": "短端资金利率：最近一月",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "EFFR",
          "label": "EFFR（有效联邦基金利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3.62
            },
            {
              "date": "2026-06-05",
              "value": 3.62
            },
            {
              "date": "2026-06-08",
              "value": 3.62
            },
            {
              "date": "2026-06-09",
              "value": 3.62
            },
            {
              "date": "2026-06-10",
              "value": 3.62
            },
            {
              "date": "2026-06-11",
              "value": 3.62
            },
            {
              "date": "2026-06-12",
              "value": 3.62
            },
            {
              "date": "2026-06-15",
              "value": 3.63
            },
            {
              "date": "2026-06-16",
              "value": 3.63
            },
            {
              "date": "2026-06-17",
              "value": 3.63
            },
            {
              "date": "2026-06-18",
              "value": 3.63
            },
            {
              "date": "2026-06-22",
              "value": 3.63
            },
            {
              "date": "2026-06-24",
              "value": 3.63
            },
            {
              "date": "2026-06-25",
              "value": 3.63
            },
            {
              "date": "2026-06-29",
              "value": 3.63
            },
            {
              "date": "2026-06-30",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.63
            },
            {
              "date": "2026-07-03",
              "value": 3.63
            },
            {
              "date": "2026-07-06",
              "value": 3.63
            },
            {
              "date": "2026-07-07",
              "value": 3.63
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "SOFR",
          "label": "SOFR（担保隔夜融资利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3.62
            },
            {
              "date": "2026-06-05",
              "value": 3.63
            },
            {
              "date": "2026-06-08",
              "value": 3.63
            },
            {
              "date": "2026-06-09",
              "value": 3.6
            },
            {
              "date": "2026-06-10",
              "value": 3.59
            },
            {
              "date": "2026-06-11",
              "value": 3.6
            },
            {
              "date": "2026-06-12",
              "value": 3.65
            },
            {
              "date": "2026-06-15",
              "value": 3.69
            },
            {
              "date": "2026-06-16",
              "value": 3.63
            },
            {
              "date": "2026-06-17",
              "value": 3.63
            },
            {
              "date": "2026-06-18",
              "value": 3.62
            },
            {
              "date": "2026-06-22",
              "value": 3.61
            },
            {
              "date": "2026-06-24",
              "value": 3.62
            },
            {
              "date": "2026-06-25",
              "value": 3.64
            },
            {
              "date": "2026-06-29",
              "value": 3.62
            },
            {
              "date": "2026-06-30",
              "value": 3.68
            },
            {
              "date": "2026-07-01",
              "value": 3.66
            },
            {
              "date": "2026-07-02",
              "value": 3.64
            },
            {
              "date": "2026-07-06",
              "value": 3.63
            },
            {
              "date": "2026-07-07",
              "value": 3.62
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "TGCR",
          "label": "TGCR（三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3.59
            },
            {
              "date": "2026-06-05",
              "value": 3.61
            },
            {
              "date": "2026-06-08",
              "value": 3.61
            },
            {
              "date": "2026-06-09",
              "value": 3.59
            },
            {
              "date": "2026-06-10",
              "value": 3.57
            },
            {
              "date": "2026-06-11",
              "value": 3.58
            },
            {
              "date": "2026-06-12",
              "value": 3.63
            },
            {
              "date": "2026-06-15",
              "value": 3.67
            },
            {
              "date": "2026-06-16",
              "value": 3.61
            },
            {
              "date": "2026-06-17",
              "value": 3.61
            },
            {
              "date": "2026-06-18",
              "value": 3.6
            },
            {
              "date": "2026-06-22",
              "value": 3.59
            },
            {
              "date": "2026-06-24",
              "value": 3.61
            },
            {
              "date": "2026-06-25",
              "value": 3.62
            },
            {
              "date": "2026-06-29",
              "value": 3.6
            },
            {
              "date": "2026-06-30",
              "value": 3.64
            },
            {
              "date": "2026-07-01",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.62
            },
            {
              "date": "2026-07-06",
              "value": 3.61
            },
            {
              "date": "2026-07-07",
              "value": 3.6
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR",
          "label": "BGCR（广义一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3.59
            },
            {
              "date": "2026-06-05",
              "value": 3.61
            },
            {
              "date": "2026-06-08",
              "value": 3.61
            },
            {
              "date": "2026-06-09",
              "value": 3.59
            },
            {
              "date": "2026-06-10",
              "value": 3.57
            },
            {
              "date": "2026-06-11",
              "value": 3.58
            },
            {
              "date": "2026-06-12",
              "value": 3.63
            },
            {
              "date": "2026-06-15",
              "value": 3.67
            },
            {
              "date": "2026-06-16",
              "value": 3.61
            },
            {
              "date": "2026-06-17",
              "value": 3.61
            },
            {
              "date": "2026-06-18",
              "value": 3.6
            },
            {
              "date": "2026-06-22",
              "value": 3.59
            },
            {
              "date": "2026-06-24",
              "value": 3.61
            },
            {
              "date": "2026-06-25",
              "value": 3.62
            },
            {
              "date": "2026-06-29",
              "value": 3.6
            },
            {
              "date": "2026-06-30",
              "value": 3.64
            },
            {
              "date": "2026-07-01",
              "value": 3.63
            },
            {
              "date": "2026-07-02",
              "value": 3.62
            },
            {
              "date": "2026-07-06",
              "value": 3.61
            },
            {
              "date": "2026-07-07",
              "value": 3.6
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "anchor_spreads_7d",
      "title": "关键利差：最近一周",
      "chart_type": "line",
      "unit": "bp",
      "series": [
        {
          "id": "SOFR_ANCHOR",
          "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-30",
              "value": 3.000000000000025
            },
            {
              "date": "2026-07-01",
              "value": 1.000000000000023
            },
            {
              "date": "2026-07-02",
              "value": -0.9999999999999787
            },
            {
              "date": "2026-07-06",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-07-07",
              "value": -2.9999999999999805
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR_TGCR",
          "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-29",
              "value": 0.0
            },
            {
              "date": "2026-06-30",
              "value": 0.0
            },
            {
              "date": "2026-07-01",
              "value": 0.0
            },
            {
              "date": "2026-07-02",
              "value": 0.0
            },
            {
              "date": "2026-07-06",
              "value": 0.0
            },
            {
              "date": "2026-07-07",
              "value": 0.0
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "anchor_spreads_30d",
      "title": "关键利差：最近一月",
      "chart_type": "line",
      "unit": "bp",
      "series": [
        {
          "id": "SOFR_ANCHOR",
          "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-05",
              "value": -4.0000000000000036
            },
            {
              "date": "2026-06-06",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-07",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-08",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-09",
              "value": -4.999999999999982
            },
            {
              "date": "2026-06-10",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-11",
              "value": -4.999999999999982
            },
            {
              "date": "2026-06-12",
              "value": 0.0
            },
            {
              "date": "2026-06-15",
              "value": 4.0000000000000036
            },
            {
              "date": "2026-06-16",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-17",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-18",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-22",
              "value": -4.0000000000000036
            },
            {
              "date": "2026-06-24",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-25",
              "value": -0.9999999999999787
            },
            {
              "date": "2026-06-29",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-30",
              "value": 3.000000000000025
            },
            {
              "date": "2026-07-01",
              "value": 1.000000000000023
            },
            {
              "date": "2026-07-02",
              "value": -0.9999999999999787
            },
            {
              "date": "2026-07-06",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-07-07",
              "value": -2.9999999999999805
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR_TGCR",
          "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 0.9999999999999787
            },
            {
              "date": "2026-06-05",
              "value": 0.0
            },
            {
              "date": "2026-06-06",
              "value": 0.0
            },
            {
              "date": "2026-06-07",
              "value": 0.0
            },
            {
              "date": "2026-06-08",
              "value": 0.0
            },
            {
              "date": "2026-06-09",
              "value": 0.0
            },
            {
              "date": "2026-06-10",
              "value": 0.0
            },
            {
              "date": "2026-06-11",
              "value": 0.0
            },
            {
              "date": "2026-06-12",
              "value": 0.0
            },
            {
              "date": "2026-06-15",
              "value": 0.0
            },
            {
              "date": "2026-06-16",
              "value": 0.0
            },
            {
              "date": "2026-06-17",
              "value": 0.0
            },
            {
              "date": "2026-06-18",
              "value": 0.0
            },
            {
              "date": "2026-06-22",
              "value": 0.0
            },
            {
              "date": "2026-06-24",
              "value": 0.0
            },
            {
              "date": "2026-06-25",
              "value": 0.0
            },
            {
              "date": "2026-06-29",
              "value": 0.0
            },
            {
              "date": "2026-06-30",
              "value": 0.0
            },
            {
              "date": "2026-07-01",
              "value": 0.0
            },
            {
              "date": "2026-07-02",
              "value": 0.0
            },
            {
              "date": "2026-07-06",
              "value": 0.0
            },
            {
              "date": "2026-07-07",
              "value": 0.0
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "sofr_volume_30d",
      "title": "SOFR交易量：最近一月",
      "chart_type": "line",
      "unit": "USD bn",
      "series": [
        {
          "id": "SOFR_VOLUME",
          "label": "SOFR Volume（SOFR交易量）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3147.0
            },
            {
              "date": "2026-06-05",
              "value": 3131.0
            },
            {
              "date": "2026-06-08",
              "value": 3115.0
            },
            {
              "date": "2026-06-09",
              "value": 3063.0
            },
            {
              "date": "2026-06-10",
              "value": 3023.0
            },
            {
              "date": "2026-06-11",
              "value": 3061.0
            },
            {
              "date": "2026-06-12",
              "value": 3059.0
            },
            {
              "date": "2026-06-15",
              "value": 3147.0
            },
            {
              "date": "2026-06-16",
              "value": 3137.0
            },
            {
              "date": "2026-06-17",
              "value": 3114.0
            },
            {
              "date": "2026-06-18",
              "value": 3148.0
            },
            {
              "date": "2026-06-22",
              "value": 3073.0
            },
            {
              "date": "2026-06-24",
              "value": 3116.0
            },
            {
              "date": "2026-06-25",
              "value": 3145.0
            },
            {
              "date": "2026-06-29",
              "value": 3126.0
            },
            {
              "date": "2026-06-30",
              "value": 3418.0
            },
            {
              "date": "2026-07-01",
              "value": 3321.0
            },
            {
              "date": "2026-07-02",
              "value": 3208.0
            },
            {
              "date": "2026-07-06",
              "value": 3212.0
            },
            {
              "date": "2026-07-07",
              "value": 3154.0
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "tbill_auction_size_45d",
      "title": "T-bill拍卖规模：最近45日",
      "chart_type": "line",
      "unit": "USD bn",
      "series": [
        {
          "id": "TBILL_AUCTION_SIZE",
          "label": "T-bill Auction Size（短期国债拍卖规模）",
          "points": [
            {
              "date": "2026-05-26",
              "value": 251.0
            },
            {
              "date": "2026-05-28",
              "value": 165.0
            },
            {
              "date": "2026-06-02",
              "value": 75.0
            },
            {
              "date": "2026-06-04",
              "value": 150.0
            },
            {
              "date": "2026-06-09",
              "value": 115.0
            },
            {
              "date": "2026-06-11",
              "value": 145.0
            },
            {
              "date": "2026-06-16",
              "value": 65.0
            },
            {
              "date": "2026-06-18",
              "value": 145.0
            },
            {
              "date": "2026-06-23",
              "value": 65.0
            },
            {
              "date": "2026-06-25",
              "value": 145.0
            },
            {
              "date": "2026-06-30",
              "value": 80.0
            },
            {
              "date": "2026-07-02",
              "value": 170.0
            },
            {
              "date": "2026-07-07",
              "value": 142.0
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "tbill_auction_btc_45d",
      "title": "T-bill拍卖认购倍数：最近45日",
      "chart_type": "line",
      "unit": "ratio",
      "series": [
        {
          "id": "TBILL_AUCTION_BTC",
          "label": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
          "points": [
            {
              "date": "2026-05-26",
              "value": 2.859601593625498
            },
            {
              "date": "2026-05-28",
              "value": 2.915151515151515
            },
            {
              "date": "2026-06-02",
              "value": 3.28
            },
            {
              "date": "2026-06-04",
              "value": 3.135
            },
            {
              "date": "2026-06-09",
              "value": 3.2891304347826087
            },
            {
              "date": "2026-06-11",
              "value": 3.0317241379310347
            },
            {
              "date": "2026-06-16",
              "value": 3.12
            },
            {
              "date": "2026-06-18",
              "value": 2.7727586206896553
            },
            {
              "date": "2026-06-23",
              "value": 2.91
            },
            {
              "date": "2026-06-25",
              "value": 2.765862068965517
            },
            {
              "date": "2026-06-30",
              "value": 2.71
            },
            {
              "date": "2026-07-02",
              "value": 2.7100000000000004
            },
            {
              "date": "2026-07-07",
              "value": 2.8864788732394366
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "cp_proxy_30d",
      "title": "企业短融代理利差：最近一月",
      "chart_type": "line",
      "unit": "bp",
      "series": [
        {
          "id": "CP_PROXY",
          "label": "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）",
          "points": [
            {
              "date": "2026-06-04",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-05",
              "value": -6.999999999999984
            },
            {
              "date": "2026-06-06",
              "value": -4.999999999999982
            },
            {
              "date": "2026-06-07",
              "value": -4.999999999999982
            },
            {
              "date": "2026-06-09",
              "value": -8.999999999999986
            },
            {
              "date": "2026-06-10",
              "value": -8.000000000000007
            },
            {
              "date": "2026-06-15",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-16",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-17",
              "value": -8.000000000000007
            },
            {
              "date": "2026-06-26",
              "value": -2.9999999999999805
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "credit_oas_30d",
      "title": "信用利差：最近一月",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "BAMLH0A0HYM2",
          "label": "HY OAS（高收益债期权调整利差）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 2.74
            },
            {
              "date": "2026-06-05",
              "value": 2.76
            },
            {
              "date": "2026-06-08",
              "value": 2.75
            },
            {
              "date": "2026-06-09",
              "value": 2.78
            },
            {
              "date": "2026-06-10",
              "value": 2.8
            },
            {
              "date": "2026-06-11",
              "value": 2.78
            },
            {
              "date": "2026-06-12",
              "value": 2.71
            },
            {
              "date": "2026-06-15",
              "value": 2.66
            },
            {
              "date": "2026-06-16",
              "value": 2.71
            },
            {
              "date": "2026-06-17",
              "value": 2.63
            },
            {
              "date": "2026-06-19",
              "value": 2.66
            },
            {
              "date": "2026-06-22",
              "value": 2.65
            },
            {
              "date": "2026-06-24",
              "value": 2.76
            },
            {
              "date": "2026-06-25",
              "value": 2.78
            },
            {
              "date": "2026-06-29",
              "value": 2.8
            },
            {
              "date": "2026-06-30",
              "value": 2.75
            },
            {
              "date": "2026-07-02",
              "value": 2.75
            },
            {
              "date": "2026-07-03",
              "value": 2.74
            },
            {
              "date": "2026-07-06",
              "value": 2.72
            },
            {
              "date": "2026-07-07",
              "value": 2.67
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BAMLC0A0CM",
          "label": "IG OAS（投资级公司债期权调整利差）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 0.74
            },
            {
              "date": "2026-06-05",
              "value": 0.74
            },
            {
              "date": "2026-06-08",
              "value": 0.75
            },
            {
              "date": "2026-06-09",
              "value": 0.75
            },
            {
              "date": "2026-06-10",
              "value": 0.75
            },
            {
              "date": "2026-06-11",
              "value": 0.75
            },
            {
              "date": "2026-06-12",
              "value": 0.74
            },
            {
              "date": "2026-06-15",
              "value": 0.73
            },
            {
              "date": "2026-06-16",
              "value": 0.75
            },
            {
              "date": "2026-06-17",
              "value": 0.74
            },
            {
              "date": "2026-06-19",
              "value": 0.74
            },
            {
              "date": "2026-06-22",
              "value": 0.74
            },
            {
              "date": "2026-06-24",
              "value": 0.75
            },
            {
              "date": "2026-06-25",
              "value": 0.76
            },
            {
              "date": "2026-06-29",
              "value": 0.76
            },
            {
              "date": "2026-06-30",
              "value": 0.76
            },
            {
              "date": "2026-07-02",
              "value": 0.75
            },
            {
              "date": "2026-07-03",
              "value": 0.75
            },
            {
              "date": "2026-07-06",
              "value": 0.75
            },
            {
              "date": "2026-07-07",
              "value": 0.76
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "treasury_yields_30d",
      "title": "美国国债收益率：1Y / 3Y / 10Y 最近一月",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "DGS1",
          "label": "1Y Treasury Yield（1年期美国国债收益率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 3.82
            },
            {
              "date": "2026-06-05",
              "value": 3.88
            },
            {
              "date": "2026-06-08",
              "value": 3.85
            },
            {
              "date": "2026-06-09",
              "value": 3.9
            },
            {
              "date": "2026-06-10",
              "value": 3.9
            },
            {
              "date": "2026-06-11",
              "value": 3.85
            },
            {
              "date": "2026-06-12",
              "value": 3.86
            },
            {
              "date": "2026-06-15",
              "value": 3.84
            },
            {
              "date": "2026-06-16",
              "value": 3.84
            },
            {
              "date": "2026-06-17",
              "value": 3.98
            },
            {
              "date": "2026-06-18",
              "value": 4.0
            },
            {
              "date": "2026-06-22",
              "value": 4.04
            },
            {
              "date": "2026-06-24",
              "value": 3.99
            },
            {
              "date": "2026-06-25",
              "value": 3.96
            },
            {
              "date": "2026-06-29",
              "value": 3.97
            },
            {
              "date": "2026-06-30",
              "value": 3.98
            },
            {
              "date": "2026-07-01",
              "value": 4.0
            },
            {
              "date": "2026-07-02",
              "value": 3.96
            },
            {
              "date": "2026-07-06",
              "value": 3.95
            },
            {
              "date": "2026-07-07",
              "value": 4.06
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "DGS3",
          "label": "3Y Treasury Yield（3年期美国国债收益率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 4.1
            },
            {
              "date": "2026-06-05",
              "value": 4.22
            },
            {
              "date": "2026-06-08",
              "value": 4.21
            },
            {
              "date": "2026-06-09",
              "value": 4.16
            },
            {
              "date": "2026-06-10",
              "value": 4.17
            },
            {
              "date": "2026-06-11",
              "value": 4.09
            },
            {
              "date": "2026-06-12",
              "value": 4.12
            },
            {
              "date": "2026-06-15",
              "value": 4.1
            },
            {
              "date": "2026-06-16",
              "value": 4.08
            },
            {
              "date": "2026-06-17",
              "value": 4.23
            },
            {
              "date": "2026-06-18",
              "value": 4.19
            },
            {
              "date": "2026-06-22",
              "value": 4.25
            },
            {
              "date": "2026-06-24",
              "value": 4.15
            },
            {
              "date": "2026-06-25",
              "value": 4.13
            },
            {
              "date": "2026-06-29",
              "value": 4.1
            },
            {
              "date": "2026-06-30",
              "value": 4.15
            },
            {
              "date": "2026-07-01",
              "value": 4.19
            },
            {
              "date": "2026-07-02",
              "value": 4.16
            },
            {
              "date": "2026-07-06",
              "value": 4.14
            },
            {
              "date": "2026-07-07",
              "value": 4.18
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "DGS10",
          "label": "10Y Treasury Yield（10年期美国国债收益率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 4.47
            },
            {
              "date": "2026-06-05",
              "value": 4.55
            },
            {
              "date": "2026-06-08",
              "value": 4.56
            },
            {
              "date": "2026-06-09",
              "value": 4.53
            },
            {
              "date": "2026-06-10",
              "value": 4.55
            },
            {
              "date": "2026-06-11",
              "value": 4.45
            },
            {
              "date": "2026-06-12",
              "value": 4.48
            },
            {
              "date": "2026-06-15",
              "value": 4.47
            },
            {
              "date": "2026-06-16",
              "value": 4.43
            },
            {
              "date": "2026-06-17",
              "value": 4.49
            },
            {
              "date": "2026-06-18",
              "value": 4.46
            },
            {
              "date": "2026-06-22",
              "value": 4.51
            },
            {
              "date": "2026-06-24",
              "value": 4.41
            },
            {
              "date": "2026-06-25",
              "value": 4.4
            },
            {
              "date": "2026-06-29",
              "value": 4.38
            },
            {
              "date": "2026-06-30",
              "value": 4.44
            },
            {
              "date": "2026-07-01",
              "value": 4.48
            },
            {
              "date": "2026-07-02",
              "value": 4.49
            },
            {
              "date": "2026-07-06",
              "value": 4.48
            },
            {
              "date": "2026-07-07",
              "value": 4.55
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "real_yields_30d",
      "title": "真实贴现率：最近一月",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "DFII10",
          "label": "10Y Real Yield（10年期TIPS实际收益率）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 2.11
            },
            {
              "date": "2026-06-05",
              "value": 2.19
            },
            {
              "date": "2026-06-08",
              "value": 2.21
            },
            {
              "date": "2026-06-09",
              "value": 2.2
            },
            {
              "date": "2026-06-10",
              "value": 2.21
            },
            {
              "date": "2026-06-11",
              "value": 2.16
            },
            {
              "date": "2026-06-12",
              "value": 2.17
            },
            {
              "date": "2026-06-15",
              "value": 2.15
            },
            {
              "date": "2026-06-16",
              "value": 2.14
            },
            {
              "date": "2026-06-17",
              "value": 2.23
            },
            {
              "date": "2026-06-18",
              "value": 2.21
            },
            {
              "date": "2026-06-22",
              "value": 2.28
            },
            {
              "date": "2026-06-24",
              "value": 2.23
            },
            {
              "date": "2026-06-25",
              "value": 2.19
            },
            {
              "date": "2026-06-29",
              "value": 2.16
            },
            {
              "date": "2026-06-30",
              "value": 2.2
            },
            {
              "date": "2026-07-01",
              "value": 2.25
            },
            {
              "date": "2026-07-02",
              "value": 2.26
            },
            {
              "date": "2026-07-06",
              "value": 2.24
            },
            {
              "date": "2026-07-07",
              "value": 2.3
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "treasury_curve_30d",
      "title": "美债长短端利差：最近一月",
      "chart_type": "line",
      "unit": "%",
      "series": [
        {
          "id": "T10Y2Y",
          "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 0.42
            },
            {
              "date": "2026-06-05",
              "value": 0.38
            },
            {
              "date": "2026-06-08",
              "value": 0.41
            },
            {
              "date": "2026-06-09",
              "value": 0.4
            },
            {
              "date": "2026-06-10",
              "value": 0.42
            },
            {
              "date": "2026-06-11",
              "value": 0.4
            },
            {
              "date": "2026-06-12",
              "value": 0.39
            },
            {
              "date": "2026-06-15",
              "value": 0.4
            },
            {
              "date": "2026-06-16",
              "value": 0.38
            },
            {
              "date": "2026-06-17",
              "value": 0.29
            },
            {
              "date": "2026-06-18",
              "value": 0.27
            },
            {
              "date": "2026-06-22",
              "value": 0.27
            },
            {
              "date": "2026-06-23",
              "value": 0.34
            },
            {
              "date": "2026-06-25",
              "value": 0.31
            },
            {
              "date": "2026-06-26",
              "value": 0.31
            },
            {
              "date": "2026-06-30",
              "value": 0.3
            },
            {
              "date": "2026-07-01",
              "value": 0.31
            },
            {
              "date": "2026-07-02",
              "value": 0.35
            },
            {
              "date": "2026-07-06",
              "value": 0.35
            },
            {
              "date": "2026-07-07",
              "value": 0.36
            },
            {
              "date": "2026-07-08",
              "value": 0.35
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "T10Y3M",
          "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 0.69
            },
            {
              "date": "2026-06-05",
              "value": 0.77
            },
            {
              "date": "2026-06-08",
              "value": 0.76
            },
            {
              "date": "2026-06-09",
              "value": 0.74
            },
            {
              "date": "2026-06-10",
              "value": 0.76
            },
            {
              "date": "2026-06-11",
              "value": 0.67
            },
            {
              "date": "2026-06-12",
              "value": 0.7
            },
            {
              "date": "2026-06-15",
              "value": 0.68
            },
            {
              "date": "2026-06-16",
              "value": 0.64
            },
            {
              "date": "2026-06-17",
              "value": 0.66
            },
            {
              "date": "2026-06-18",
              "value": 0.63
            },
            {
              "date": "2026-06-22",
              "value": 0.66
            },
            {
              "date": "2026-06-23",
              "value": 0.65
            },
            {
              "date": "2026-06-25",
              "value": 0.56
            },
            {
              "date": "2026-06-26",
              "value": 0.55
            },
            {
              "date": "2026-06-30",
              "value": 0.57
            },
            {
              "date": "2026-07-01",
              "value": 0.63
            },
            {
              "date": "2026-07-02",
              "value": 0.67
            },
            {
              "date": "2026-07-06",
              "value": 0.61
            },
            {
              "date": "2026-07-07",
              "value": 0.69
            },
            {
              "date": "2026-07-08",
              "value": 0.69
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "risk_appetite_30d",
      "title": "证券市场风险偏好：最近一月",
      "chart_type": "line",
      "unit": "index",
      "series": [
        {
          "id": "VIXCLS",
          "label": "VIX（标普500隐含波动率指数）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 15.4
            },
            {
              "date": "2026-06-05",
              "value": 21.51
            },
            {
              "date": "2026-06-08",
              "value": 18.92
            },
            {
              "date": "2026-06-09",
              "value": 19.87
            },
            {
              "date": "2026-06-10",
              "value": 22.22
            },
            {
              "date": "2026-06-11",
              "value": 19.44
            },
            {
              "date": "2026-06-12",
              "value": 17.68
            },
            {
              "date": "2026-06-15",
              "value": 16.2
            },
            {
              "date": "2026-06-16",
              "value": 16.41
            },
            {
              "date": "2026-06-17",
              "value": 18.44
            },
            {
              "date": "2026-06-19",
              "value": 16.78
            },
            {
              "date": "2026-06-22",
              "value": 17.28
            },
            {
              "date": "2026-06-24",
              "value": 18.63
            },
            {
              "date": "2026-06-25",
              "value": 18.89
            },
            {
              "date": "2026-06-29",
              "value": 17.65
            },
            {
              "date": "2026-06-30",
              "value": 16.45
            },
            {
              "date": "2026-07-01",
              "value": 16.59
            },
            {
              "date": "2026-07-03",
              "value": 15.81
            },
            {
              "date": "2026-07-06",
              "value": 15.57
            },
            {
              "date": "2026-07-07",
              "value": 16.13
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "financial_conditions_30d",
      "title": "公开金融条件代理：最近一月",
      "chart_type": "line",
      "unit": "index",
      "series": [
        {
          "id": "NFCI",
          "label": "NFCI（芝加哥联储全国金融条件指数）",
          "points": [
            {
              "date": "2026-06-05",
              "value": -0.506
            },
            {
              "date": "2026-06-12",
              "value": -0.505
            },
            {
              "date": "2026-06-19",
              "value": -0.516
            },
            {
              "date": "2026-06-26",
              "value": -0.504
            },
            {
              "date": "2026-07-03",
              "value": -0.515
            }
          ],
          "y_axis": "y"
        }
      ]
    },
    {
      "id": "fed_liability_30d",
      "title": "Fed负债端水位：最近一月",
      "chart_type": "line",
      "unit": "USD bn",
      "series": [
        {
          "id": "TGA",
          "label": "TGA（财政部一般账户）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 844.521
            },
            {
              "date": "2026-06-05",
              "value": 825.54
            },
            {
              "date": "2026-06-08",
              "value": 844.229
            },
            {
              "date": "2026-06-09",
              "value": 830.399
            },
            {
              "date": "2026-06-10",
              "value": 801.084
            },
            {
              "date": "2026-06-11",
              "value": 799.517
            },
            {
              "date": "2026-06-12",
              "value": 816.023
            },
            {
              "date": "2026-06-15",
              "value": 979.791
            },
            {
              "date": "2026-06-16",
              "value": 981.113
            },
            {
              "date": "2026-06-17",
              "value": 956.502
            },
            {
              "date": "2026-06-18",
              "value": 915.085
            },
            {
              "date": "2026-06-22",
              "value": 942.815
            },
            {
              "date": "2026-06-24",
              "value": 901.845
            },
            {
              "date": "2026-06-25",
              "value": 871.469
            },
            {
              "date": "2026-06-29",
              "value": 876.961
            },
            {
              "date": "2026-06-30",
              "value": 919.145
            },
            {
              "date": "2026-07-02",
              "value": 770.587
            },
            {
              "date": "2026-07-03",
              "value": 776.843
            },
            {
              "date": "2026-07-06",
              "value": 783.107
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "RRP",
          "label": "RRP（隔夜逆回购）",
          "points": [
            {
              "date": "2026-06-04",
              "value": 1.122
            },
            {
              "date": "2026-06-05",
              "value": 0.761
            },
            {
              "date": "2026-06-08",
              "value": 1.832
            },
            {
              "date": "2026-06-09",
              "value": 0.577
            },
            {
              "date": "2026-06-10",
              "value": 0.387
            },
            {
              "date": "2026-06-11",
              "value": 0.46
            },
            {
              "date": "2026-06-12",
              "value": 0.454
            },
            {
              "date": "2026-06-15",
              "value": 0.581
            },
            {
              "date": "2026-06-16",
              "value": 10.721
            },
            {
              "date": "2026-06-17",
              "value": 6.828
            },
            {
              "date": "2026-06-18",
              "value": 0.251
            },
            {
              "date": "2026-06-22",
              "value": 3.925
            },
            {
              "date": "2026-06-23",
              "value": 6.484
            },
            {
              "date": "2026-06-25",
              "value": 5.718
            },
            {
              "date": "2026-06-26",
              "value": 6.426
            },
            {
              "date": "2026-06-30",
              "value": 26.9
            },
            {
              "date": "2026-07-01",
              "value": 1.001
            },
            {
              "date": "2026-07-02",
              "value": 2.175
            },
            {
              "date": "2026-07-06",
              "value": 2.719
            },
            {
              "date": "2026-07-07",
              "value": 4.484
            },
            {
              "date": "2026-07-08",
              "value": 3.347
            }
          ],
          "y_axis": "y1"
        }
      ],
      "dual_axis": true,
      "y_axes": {
        "y": "TGA（十亿美元）",
        "y1": "RRP（十亿美元）"
      }
    },
    {
      "id": "jpy_usdjpy_funding_1y",
      "title": "JPY Carry：USD/JPY 与日元隔夜融资成本",
      "chart_type": "line",
      "unit": "",
      "dual_axis": true,
      "y_axes": {
        "y": "USD/JPY",
        "y1": "%"
      },
      "data_source": "SQLite jpy_carry_series_ts",
      "series": [
        {
          "id": "USDJPY",
          "label": "USD/JPY（东京17:00）",
          "points": [
            {
              "date": "2025-06-13",
              "value": 143.8
            },
            {
              "date": "2025-06-16",
              "value": 144.19
            },
            {
              "date": "2025-06-17",
              "value": 144.54
            },
            {
              "date": "2025-06-18",
              "value": 144.95
            },
            {
              "date": "2025-06-19",
              "value": 145.4
            },
            {
              "date": "2025-06-20",
              "value": 145.41
            },
            {
              "date": "2025-06-23",
              "value": 147.33
            },
            {
              "date": "2025-06-24",
              "value": 145.31
            },
            {
              "date": "2025-06-25",
              "value": 145.32
            },
            {
              "date": "2025-06-26",
              "value": 144.06
            },
            {
              "date": "2025-06-27",
              "value": 144.48
            },
            {
              "date": "2025-06-30",
              "value": 144.13
            },
            {
              "date": "2025-07-01",
              "value": 143.08
            },
            {
              "date": "2025-07-02",
              "value": 143.9
            },
            {
              "date": "2025-07-03",
              "value": 143.87
            },
            {
              "date": "2025-07-04",
              "value": 144.41
            },
            {
              "date": "2025-07-07",
              "value": 145.2
            },
            {
              "date": "2025-07-08",
              "value": 146.04
            },
            {
              "date": "2025-07-09",
              "value": 146.85
            },
            {
              "date": "2025-07-10",
              "value": 146.27
            },
            {
              "date": "2025-07-11",
              "value": 146.86
            },
            {
              "date": "2025-07-14",
              "value": 147.38
            },
            {
              "date": "2025-07-15",
              "value": 147.74
            },
            {
              "date": "2025-07-16",
              "value": 148.89
            },
            {
              "date": "2025-07-17",
              "value": 148.73
            },
            {
              "date": "2025-07-18",
              "value": 148.78
            },
            {
              "date": "2025-07-22",
              "value": 147.72
            },
            {
              "date": "2025-07-23",
              "value": 146.74
            },
            {
              "date": "2025-07-24",
              "value": 146.42
            },
            {
              "date": "2025-07-25",
              "value": 147.38
            },
            {
              "date": "2025-07-28",
              "value": 148.29
            },
            {
              "date": "2025-07-29",
              "value": 148.58
            },
            {
              "date": "2025-07-30",
              "value": 148.09
            },
            {
              "date": "2025-07-31",
              "value": 149.39
            },
            {
              "date": "2025-08-01",
              "value": 150.54
            },
            {
              "date": "2025-08-04",
              "value": 147.88
            },
            {
              "date": "2025-08-05",
              "value": 147.37
            },
            {
              "date": "2025-08-06",
              "value": 147.56
            },
            {
              "date": "2025-08-07",
              "value": 146.81
            },
            {
              "date": "2025-08-08",
              "value": 147.32
            },
            {
              "date": "2025-08-12",
              "value": 148.27
            },
            {
              "date": "2025-08-13",
              "value": 147.53
            },
            {
              "date": "2025-08-14",
              "value": 146.56
            },
            {
              "date": "2025-08-15",
              "value": 147.01
            },
            {
              "date": "2025-08-18",
              "value": 147.46
            },
            {
              "date": "2025-08-19",
              "value": 147.71
            },
            {
              "date": "2025-08-20",
              "value": 147.63
            },
            {
              "date": "2025-08-21",
              "value": 147.59
            },
            {
              "date": "2025-08-22",
              "value": 148.61
            },
            {
              "date": "2025-08-25",
              "value": 147.34
            },
            {
              "date": "2025-08-26",
              "value": 147.69
            },
            {
              "date": "2025-08-27",
              "value": 147.76
            },
            {
              "date": "2025-08-28",
              "value": 147.17
            },
            {
              "date": "2025-08-29",
              "value": 147.01
            },
            {
              "date": "2025-09-01",
              "value": 147.07
            },
            {
              "date": "2025-09-02",
              "value": 148.65
            },
            {
              "date": "2025-09-03",
              "value": 148.74
            },
            {
              "date": "2025-09-04",
              "value": 148.38
            },
            {
              "date": "2025-09-05",
              "value": 148.22
            },
            {
              "date": "2025-09-08",
              "value": 147.53
            },
            {
              "date": "2025-09-09",
              "value": 147.23
            },
            {
              "date": "2025-09-10",
              "value": 147.51
            },
            {
              "date": "2025-09-11",
              "value": 147.78
            },
            {
              "date": "2025-09-12",
              "value": 147.46
            },
            {
              "date": "2025-09-16",
              "value": 146.89
            },
            {
              "date": "2025-09-17",
              "value": 146.67
            },
            {
              "date": "2025-09-18",
              "value": 147.12
            },
            {
              "date": "2025-09-19",
              "value": 147.94
            },
            {
              "date": "2025-09-22",
              "value": 148.12
            },
            {
              "date": "2025-09-24",
              "value": 148.05
            },
            {
              "date": "2025-09-25",
              "value": 148.82
            },
            {
              "date": "2025-09-26",
              "value": 149.84
            },
            {
              "date": "2025-09-29",
              "value": 148.57
            },
            {
              "date": "2025-09-30",
              "value": 148.07
            },
            {
              "date": "2025-10-01",
              "value": 147.12
            },
            {
              "date": "2025-10-02",
              "value": 147.08
            },
            {
              "date": "2025-10-03",
              "value": 147.41
            },
            {
              "date": "2025-10-06",
              "value": 150.02
            },
            {
              "date": "2025-10-07",
              "value": 150.63
            },
            {
              "date": "2025-10-08",
              "value": 152.57
            },
            {
              "date": "2025-10-09",
              "value": 153.07
            },
            {
              "date": "2025-10-10",
              "value": 152.85
            },
            {
              "date": "2025-10-14",
              "value": 151.97
            },
            {
              "date": "2025-10-15",
              "value": 151.25
            },
            {
              "date": "2025-10-16",
              "value": 151.24
            },
            {
              "date": "2025-10-17",
              "value": 149.71
            },
            {
              "date": "2025-10-20",
              "value": 150.75
            },
            {
              "date": "2025-10-21",
              "value": 151.16
            },
            {
              "date": "2025-10-22",
              "value": 151.83
            },
            {
              "date": "2025-10-23",
              "value": 152.5
            },
            {
              "date": "2025-10-24",
              "value": 152.83
            },
            {
              "date": "2025-10-27",
              "value": 153.03
            },
            {
              "date": "2025-10-28",
              "value": 152.16
            },
            {
              "date": "2025-10-29",
              "value": 152.06
            },
            {
              "date": "2025-10-30",
              "value": 153.44
            },
            {
              "date": "2025-10-31",
              "value": 154.31
            },
            {
              "date": "2025-11-04",
              "value": 153.59
            },
            {
              "date": "2025-11-05",
              "value": 153.55
            },
            {
              "date": "2025-11-06",
              "value": 153.87
            },
            {
              "date": "2025-11-07",
              "value": 153.39
            },
            {
              "date": "2025-11-10",
              "value": 154.05
            },
            {
              "date": "2025-11-11",
              "value": 154.19
            },
            {
              "date": "2025-11-12",
              "value": 154.62
            },
            {
              "date": "2025-11-13",
              "value": 154.72
            },
            {
              "date": "2025-11-14",
              "value": 154.68
            },
            {
              "date": "2025-11-17",
              "value": 154.68
            },
            {
              "date": "2025-11-18",
              "value": 155.0
            },
            {
              "date": "2025-11-19",
              "value": 155.52
            },
            {
              "date": "2025-11-20",
              "value": 157.46
            },
            {
              "date": "2025-11-21",
              "value": 156.74
            },
            {
              "date": "2025-11-25",
              "value": 156.63
            },
            {
              "date": "2025-11-26",
              "value": 156.38
            },
            {
              "date": "2025-11-27",
              "value": 156.11
            },
            {
              "date": "2025-11-28",
              "value": 156.32
            },
            {
              "date": "2025-12-01",
              "value": 155.38
            },
            {
              "date": "2025-12-02",
              "value": 155.77
            },
            {
              "date": "2025-12-03",
              "value": 155.69
            },
            {
              "date": "2025-12-04",
              "value": 155.25
            },
            {
              "date": "2025-12-05",
              "value": 154.63
            },
            {
              "date": "2025-12-08",
              "value": 155.36
            },
            {
              "date": "2025-12-09",
              "value": 156.2
            },
            {
              "date": "2025-12-10",
              "value": 156.66
            },
            {
              "date": "2025-12-11",
              "value": 156.05
            },
            {
              "date": "2025-12-12",
              "value": 155.65
            },
            {
              "date": "2025-12-15",
              "value": 155.26
            },
            {
              "date": "2025-12-16",
              "value": 154.89
            },
            {
              "date": "2025-12-17",
              "value": 155.5
            },
            {
              "date": "2025-12-18",
              "value": 155.93
            },
            {
              "date": "2025-12-19",
              "value": 156.74
            },
            {
              "date": "2025-12-22",
              "value": 157.49
            },
            {
              "date": "2025-12-23",
              "value": 156.08
            },
            {
              "date": "2025-12-24",
              "value": 155.83
            },
            {
              "date": "2025-12-25",
              "value": 156.0
            },
            {
              "date": "2025-12-26",
              "value": 156.37
            },
            {
              "date": "2025-12-29",
              "value": 156.08
            },
            {
              "date": "2025-12-30",
              "value": 155.98
            },
            {
              "date": "2026-01-05",
              "value": 156.98
            },
            {
              "date": "2026-01-06",
              "value": 156.33
            },
            {
              "date": "2026-01-07",
              "value": 156.49
            },
            {
              "date": "2026-01-08",
              "value": 156.47
            },
            {
              "date": "2026-01-09",
              "value": 157.49
            },
            {
              "date": "2026-01-13",
              "value": 158.95
            },
            {
              "date": "2026-01-14",
              "value": 159.18
            },
            {
              "date": "2026-01-15",
              "value": 158.59
            },
            {
              "date": "2026-01-16",
              "value": 158.17
            },
            {
              "date": "2026-01-19",
              "value": 158.07
            },
            {
              "date": "2026-01-20",
              "value": 158.37
            },
            {
              "date": "2026-01-21",
              "value": 157.92
            },
            {
              "date": "2026-01-22",
              "value": 158.78
            },
            {
              "date": "2026-01-23",
              "value": 158.39
            },
            {
              "date": "2026-01-26",
              "value": 154.26
            },
            {
              "date": "2026-01-27",
              "value": 154.72
            },
            {
              "date": "2026-01-28",
              "value": 152.64
            },
            {
              "date": "2026-01-29",
              "value": 153.33
            },
            {
              "date": "2026-01-30",
              "value": 153.8
            },
            {
              "date": "2026-02-02",
              "value": 154.89
            },
            {
              "date": "2026-02-03",
              "value": 155.41
            },
            {
              "date": "2026-02-04",
              "value": 156.43
            },
            {
              "date": "2026-02-05",
              "value": 157.12
            },
            {
              "date": "2026-02-06",
              "value": 156.89
            },
            {
              "date": "2026-02-09",
              "value": 156.6
            },
            {
              "date": "2026-02-10",
              "value": 155.57
            },
            {
              "date": "2026-02-12",
              "value": 153.01
            },
            {
              "date": "2026-02-13",
              "value": 153.4
            },
            {
              "date": "2026-02-16",
              "value": 153.35
            },
            {
              "date": "2026-02-17",
              "value": 153.09
            },
            {
              "date": "2026-02-18",
              "value": 153.68
            },
            {
              "date": "2026-02-19",
              "value": 154.97
            },
            {
              "date": "2026-02-20",
              "value": 155.5
            },
            {
              "date": "2026-02-24",
              "value": 156.11
            },
            {
              "date": "2026-02-25",
              "value": 155.92
            },
            {
              "date": "2026-02-26",
              "value": 156.04
            },
            {
              "date": "2026-02-27",
              "value": 156.09
            },
            {
              "date": "2026-03-02",
              "value": 156.99
            },
            {
              "date": "2026-03-03",
              "value": 157.42
            },
            {
              "date": "2026-03-04",
              "value": 157.46
            },
            {
              "date": "2026-03-05",
              "value": 157.26
            },
            {
              "date": "2026-03-06",
              "value": 157.54
            },
            {
              "date": "2026-03-09",
              "value": 158.46
            },
            {
              "date": "2026-03-10",
              "value": 157.32
            },
            {
              "date": "2026-03-11",
              "value": 158.23
            },
            {
              "date": "2026-03-12",
              "value": 158.8
            },
            {
              "date": "2026-03-13",
              "value": 159.43
            },
            {
              "date": "2026-03-16",
              "value": 159.29
            },
            {
              "date": "2026-03-17",
              "value": 159.23
            },
            {
              "date": "2026-03-18",
              "value": 158.77
            },
            {
              "date": "2026-03-19",
              "value": 159.22
            },
            {
              "date": "2026-03-23",
              "value": 159.59
            },
            {
              "date": "2026-03-24",
              "value": 158.5
            },
            {
              "date": "2026-03-25",
              "value": 159.14
            },
            {
              "date": "2026-03-26",
              "value": 159.5
            },
            {
              "date": "2026-03-27",
              "value": 159.95
            },
            {
              "date": "2026-03-30",
              "value": 159.78
            },
            {
              "date": "2026-03-31",
              "value": 159.63
            },
            {
              "date": "2026-04-01",
              "value": 158.8
            },
            {
              "date": "2026-04-02",
              "value": 159.57
            },
            {
              "date": "2026-04-03",
              "value": 159.6
            },
            {
              "date": "2026-04-06",
              "value": 159.38
            },
            {
              "date": "2026-04-07",
              "value": 159.87
            },
            {
              "date": "2026-04-08",
              "value": 158.21
            },
            {
              "date": "2026-04-09",
              "value": 158.97
            },
            {
              "date": "2026-04-10",
              "value": 159.35
            },
            {
              "date": "2026-04-13",
              "value": 159.61
            },
            {
              "date": "2026-04-14",
              "value": 159.07
            },
            {
              "date": "2026-04-15",
              "value": 158.94
            },
            {
              "date": "2026-04-16",
              "value": 158.87
            },
            {
              "date": "2026-04-17",
              "value": 159.27
            },
            {
              "date": "2026-04-20",
              "value": 158.97
            },
            {
              "date": "2026-04-21",
              "value": 159.02
            },
            {
              "date": "2026-04-22",
              "value": 159.22
            },
            {
              "date": "2026-04-23",
              "value": 159.6
            },
            {
              "date": "2026-04-24",
              "value": 159.68
            },
            {
              "date": "2026-04-27",
              "value": 159.24
            },
            {
              "date": "2026-04-28",
              "value": 159.53
            },
            {
              "date": "2026-04-30",
              "value": 160.14
            },
            {
              "date": "2026-05-01",
              "value": 156.62
            },
            {
              "date": "2026-05-07",
              "value": 156.27
            },
            {
              "date": "2026-05-08",
              "value": 156.84
            },
            {
              "date": "2026-05-11",
              "value": 157.12
            },
            {
              "date": "2026-05-12",
              "value": 157.51
            },
            {
              "date": "2026-05-13",
              "value": 157.85
            },
            {
              "date": "2026-05-14",
              "value": 157.93
            },
            {
              "date": "2026-05-15",
              "value": 158.45
            },
            {
              "date": "2026-05-18",
              "value": 158.93
            },
            {
              "date": "2026-05-19",
              "value": 159.04
            },
            {
              "date": "2026-05-20",
              "value": 159.07
            },
            {
              "date": "2026-05-21",
              "value": 159.03
            },
            {
              "date": "2026-05-22",
              "value": 159.13
            },
            {
              "date": "2026-05-25",
              "value": 158.97
            },
            {
              "date": "2026-05-26",
              "value": 159.2
            },
            {
              "date": "2026-05-27",
              "value": 159.36
            },
            {
              "date": "2026-05-28",
              "value": 159.47
            },
            {
              "date": "2026-05-29",
              "value": 159.27
            },
            {
              "date": "2026-06-01",
              "value": 159.47
            },
            {
              "date": "2026-06-02",
              "value": 159.69
            },
            {
              "date": "2026-06-03",
              "value": 159.71
            },
            {
              "date": "2026-06-04",
              "value": 159.9
            },
            {
              "date": "2026-06-05",
              "value": 159.95
            },
            {
              "date": "2026-06-08",
              "value": 160.23
            },
            {
              "date": "2026-06-09",
              "value": 160.2
            },
            {
              "date": "2026-06-10",
              "value": 160.39
            },
            {
              "date": "2026-06-11",
              "value": 160.51
            },
            {
              "date": "2026-06-12",
              "value": 160.28
            },
            {
              "date": "2026-06-15",
              "value": 160.13
            },
            {
              "date": "2026-06-16",
              "value": 160.23
            },
            {
              "date": "2026-06-17",
              "value": 160.19
            },
            {
              "date": "2026-06-18",
              "value": 160.6
            },
            {
              "date": "2026-06-19",
              "value": 161.32
            },
            {
              "date": "2026-06-22",
              "value": 161.74
            },
            {
              "date": "2026-06-23",
              "value": 161.48
            },
            {
              "date": "2026-06-24",
              "value": 161.72
            },
            {
              "date": "2026-06-25",
              "value": 161.82
            },
            {
              "date": "2026-06-26",
              "value": 161.63
            },
            {
              "date": "2026-06-29",
              "value": 161.83
            },
            {
              "date": "2026-06-30",
              "value": 162.26
            },
            {
              "date": "2026-07-01",
              "value": 162.68
            },
            {
              "date": "2026-07-02",
              "value": 161.44
            },
            {
              "date": "2026-07-03",
              "value": 160.78
            },
            {
              "date": "2026-07-06",
              "value": 162.17
            },
            {
              "date": "2026-07-07",
              "value": 161.97
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "JPY_CALL",
          "label": "JPY隔夜融资成本",
          "points": [
            {
              "date": "2025-06-13",
              "value": 0.477
            },
            {
              "date": "2025-06-16",
              "value": 0.477
            },
            {
              "date": "2025-06-17",
              "value": 0.477
            },
            {
              "date": "2025-06-18",
              "value": 0.478
            },
            {
              "date": "2025-06-19",
              "value": 0.477
            },
            {
              "date": "2025-06-20",
              "value": 0.477
            },
            {
              "date": "2025-06-23",
              "value": 0.476
            },
            {
              "date": "2025-06-24",
              "value": 0.478
            },
            {
              "date": "2025-06-25",
              "value": 0.478
            },
            {
              "date": "2025-06-26",
              "value": 0.478
            },
            {
              "date": "2025-06-27",
              "value": 0.477
            },
            {
              "date": "2025-06-30",
              "value": 0.477
            },
            {
              "date": "2025-07-01",
              "value": 0.477
            },
            {
              "date": "2025-07-02",
              "value": 0.477
            },
            {
              "date": "2025-07-03",
              "value": 0.477
            },
            {
              "date": "2025-07-04",
              "value": 0.477
            },
            {
              "date": "2025-07-07",
              "value": 0.477
            },
            {
              "date": "2025-07-08",
              "value": 0.477
            },
            {
              "date": "2025-07-09",
              "value": 0.477
            },
            {
              "date": "2025-07-10",
              "value": 0.477
            },
            {
              "date": "2025-07-11",
              "value": 0.477
            },
            {
              "date": "2025-07-14",
              "value": 0.479
            },
            {
              "date": "2025-07-15",
              "value": 0.476
            },
            {
              "date": "2025-07-16",
              "value": 0.477
            },
            {
              "date": "2025-07-17",
              "value": 0.477
            },
            {
              "date": "2025-07-18",
              "value": 0.477
            },
            {
              "date": "2025-07-22",
              "value": 0.479
            },
            {
              "date": "2025-07-23",
              "value": 0.478
            },
            {
              "date": "2025-07-24",
              "value": 0.477
            },
            {
              "date": "2025-07-25",
              "value": 0.477
            },
            {
              "date": "2025-07-28",
              "value": 0.479
            },
            {
              "date": "2025-07-29",
              "value": 0.478
            },
            {
              "date": "2025-07-30",
              "value": 0.481
            },
            {
              "date": "2025-07-31",
              "value": 0.478
            },
            {
              "date": "2025-08-01",
              "value": 0.477
            },
            {
              "date": "2025-08-04",
              "value": 0.476
            },
            {
              "date": "2025-08-05",
              "value": 0.477
            },
            {
              "date": "2025-08-06",
              "value": 0.477
            },
            {
              "date": "2025-08-07",
              "value": 0.477
            },
            {
              "date": "2025-08-08",
              "value": 0.477
            },
            {
              "date": "2025-08-12",
              "value": 0.477
            },
            {
              "date": "2025-08-13",
              "value": 0.477
            },
            {
              "date": "2025-08-14",
              "value": 0.477
            },
            {
              "date": "2025-08-15",
              "value": 0.477
            },
            {
              "date": "2025-08-18",
              "value": 0.477
            },
            {
              "date": "2025-08-19",
              "value": 0.477
            },
            {
              "date": "2025-08-20",
              "value": 0.476
            },
            {
              "date": "2025-08-21",
              "value": 0.476
            },
            {
              "date": "2025-08-22",
              "value": 0.476
            },
            {
              "date": "2025-08-25",
              "value": 0.477
            },
            {
              "date": "2025-08-26",
              "value": 0.478
            },
            {
              "date": "2025-08-27",
              "value": 0.478
            },
            {
              "date": "2025-08-28",
              "value": 0.478
            },
            {
              "date": "2025-08-29",
              "value": 0.477
            },
            {
              "date": "2025-09-01",
              "value": 0.477
            },
            {
              "date": "2025-09-02",
              "value": 0.478
            },
            {
              "date": "2025-09-03",
              "value": 0.478
            },
            {
              "date": "2025-09-04",
              "value": 0.479
            },
            {
              "date": "2025-09-05",
              "value": 0.477
            },
            {
              "date": "2025-09-08",
              "value": 0.477
            },
            {
              "date": "2025-09-09",
              "value": 0.477
            },
            {
              "date": "2025-09-10",
              "value": 0.477
            },
            {
              "date": "2025-09-11",
              "value": 0.48
            },
            {
              "date": "2025-09-12",
              "value": 0.477
            },
            {
              "date": "2025-09-16",
              "value": 0.477
            },
            {
              "date": "2025-09-17",
              "value": 0.478
            },
            {
              "date": "2025-09-18",
              "value": 0.477
            },
            {
              "date": "2025-09-19",
              "value": 0.477
            },
            {
              "date": "2025-09-22",
              "value": 0.476
            },
            {
              "date": "2025-09-24",
              "value": 0.478
            },
            {
              "date": "2025-09-25",
              "value": 0.477
            },
            {
              "date": "2025-09-26",
              "value": 0.476
            },
            {
              "date": "2025-09-29",
              "value": 0.477
            },
            {
              "date": "2025-09-30",
              "value": 0.477
            },
            {
              "date": "2025-10-01",
              "value": 0.477
            },
            {
              "date": "2025-10-02",
              "value": 0.477
            },
            {
              "date": "2025-10-03",
              "value": 0.477
            },
            {
              "date": "2025-10-06",
              "value": 0.477
            },
            {
              "date": "2025-10-07",
              "value": 0.477
            },
            {
              "date": "2025-10-08",
              "value": 0.477
            },
            {
              "date": "2025-10-09",
              "value": 0.478
            },
            {
              "date": "2025-10-10",
              "value": 0.477
            },
            {
              "date": "2025-10-14",
              "value": 0.477
            },
            {
              "date": "2025-10-15",
              "value": 0.477
            },
            {
              "date": "2025-10-16",
              "value": 0.477
            },
            {
              "date": "2025-10-17",
              "value": 0.477
            },
            {
              "date": "2025-10-20",
              "value": 0.477
            },
            {
              "date": "2025-10-21",
              "value": 0.477
            },
            {
              "date": "2025-10-22",
              "value": 0.477
            },
            {
              "date": "2025-10-23",
              "value": 0.477
            },
            {
              "date": "2025-10-24",
              "value": 0.477
            },
            {
              "date": "2025-10-27",
              "value": 0.477
            },
            {
              "date": "2025-10-28",
              "value": 0.477
            },
            {
              "date": "2025-10-29",
              "value": 0.477
            },
            {
              "date": "2025-10-30",
              "value": 0.476
            },
            {
              "date": "2025-10-31",
              "value": 0.477
            },
            {
              "date": "2025-11-04",
              "value": 0.476
            },
            {
              "date": "2025-11-05",
              "value": 0.477
            },
            {
              "date": "2025-11-06",
              "value": 0.477
            },
            {
              "date": "2025-11-07",
              "value": 0.478
            },
            {
              "date": "2025-11-10",
              "value": 0.481
            },
            {
              "date": "2025-11-11",
              "value": 0.477
            },
            {
              "date": "2025-11-12",
              "value": 0.479
            },
            {
              "date": "2025-11-13",
              "value": 0.477
            },
            {
              "date": "2025-11-14",
              "value": 0.478
            },
            {
              "date": "2025-11-17",
              "value": 0.477
            },
            {
              "date": "2025-11-18",
              "value": 0.478
            },
            {
              "date": "2025-11-19",
              "value": 0.479
            },
            {
              "date": "2025-11-20",
              "value": 0.477
            },
            {
              "date": "2025-11-21",
              "value": 0.478
            },
            {
              "date": "2025-11-25",
              "value": 0.478
            },
            {
              "date": "2025-11-26",
              "value": 0.478
            },
            {
              "date": "2025-11-27",
              "value": 0.477
            },
            {
              "date": "2025-11-28",
              "value": 0.477
            },
            {
              "date": "2025-12-01",
              "value": 0.477
            },
            {
              "date": "2025-12-02",
              "value": 0.477
            },
            {
              "date": "2025-12-03",
              "value": 0.478
            },
            {
              "date": "2025-12-04",
              "value": 0.477
            },
            {
              "date": "2025-12-05",
              "value": 0.477
            },
            {
              "date": "2025-12-08",
              "value": 0.477
            },
            {
              "date": "2025-12-09",
              "value": 0.482
            },
            {
              "date": "2025-12-10",
              "value": 0.477
            },
            {
              "date": "2025-12-11",
              "value": 0.478
            },
            {
              "date": "2025-12-12",
              "value": 0.477
            },
            {
              "date": "2025-12-15",
              "value": 0.477
            },
            {
              "date": "2025-12-16",
              "value": 0.482
            },
            {
              "date": "2025-12-17",
              "value": 0.478
            },
            {
              "date": "2025-12-18",
              "value": 0.477
            },
            {
              "date": "2025-12-19",
              "value": 0.477
            },
            {
              "date": "2025-12-22",
              "value": 0.727
            },
            {
              "date": "2025-12-23",
              "value": 0.727
            },
            {
              "date": "2025-12-24",
              "value": 0.727
            },
            {
              "date": "2025-12-25",
              "value": 0.728
            },
            {
              "date": "2025-12-26",
              "value": 0.727
            },
            {
              "date": "2025-12-29",
              "value": 0.728
            },
            {
              "date": "2025-12-30",
              "value": 0.727
            },
            {
              "date": "2026-01-05",
              "value": 0.727
            },
            {
              "date": "2026-01-06",
              "value": 0.727
            },
            {
              "date": "2026-01-07",
              "value": 0.727
            },
            {
              "date": "2026-01-08",
              "value": 0.729
            },
            {
              "date": "2026-01-09",
              "value": 0.727
            },
            {
              "date": "2026-01-13",
              "value": 0.727
            },
            {
              "date": "2026-01-14",
              "value": 0.727
            },
            {
              "date": "2026-01-15",
              "value": 0.727
            },
            {
              "date": "2026-01-16",
              "value": 0.727
            },
            {
              "date": "2026-01-19",
              "value": 0.727
            },
            {
              "date": "2026-01-20",
              "value": 0.728
            },
            {
              "date": "2026-01-21",
              "value": 0.727
            },
            {
              "date": "2026-01-22",
              "value": 0.727
            },
            {
              "date": "2026-01-23",
              "value": 0.727
            },
            {
              "date": "2026-01-26",
              "value": 0.728
            },
            {
              "date": "2026-01-27",
              "value": 0.736
            },
            {
              "date": "2026-01-28",
              "value": 0.727
            },
            {
              "date": "2026-01-29",
              "value": 0.727
            },
            {
              "date": "2026-01-30",
              "value": 0.727
            },
            {
              "date": "2026-02-02",
              "value": 0.727
            },
            {
              "date": "2026-02-03",
              "value": 0.73
            },
            {
              "date": "2026-02-04",
              "value": 0.727
            },
            {
              "date": "2026-02-05",
              "value": 0.727
            },
            {
              "date": "2026-02-06",
              "value": 0.728
            },
            {
              "date": "2026-02-09",
              "value": 0.728
            },
            {
              "date": "2026-02-10",
              "value": 0.727
            },
            {
              "date": "2026-02-12",
              "value": 0.728
            },
            {
              "date": "2026-02-13",
              "value": 0.728
            },
            {
              "date": "2026-02-16",
              "value": 0.728
            },
            {
              "date": "2026-02-17",
              "value": 0.73
            },
            {
              "date": "2026-02-18",
              "value": 0.728
            },
            {
              "date": "2026-02-19",
              "value": 0.728
            },
            {
              "date": "2026-02-20",
              "value": 0.729
            },
            {
              "date": "2026-02-24",
              "value": 0.727
            },
            {
              "date": "2026-02-25",
              "value": 0.729
            },
            {
              "date": "2026-02-26",
              "value": 0.728
            },
            {
              "date": "2026-02-27",
              "value": 0.727
            },
            {
              "date": "2026-03-02",
              "value": 0.727
            },
            {
              "date": "2026-03-03",
              "value": 0.727
            },
            {
              "date": "2026-03-04",
              "value": 0.73
            },
            {
              "date": "2026-03-05",
              "value": 0.728
            },
            {
              "date": "2026-03-06",
              "value": 0.728
            },
            {
              "date": "2026-03-09",
              "value": 0.727
            },
            {
              "date": "2026-03-10",
              "value": 0.728
            },
            {
              "date": "2026-03-11",
              "value": 0.727
            },
            {
              "date": "2026-03-12",
              "value": 0.734
            },
            {
              "date": "2026-03-13",
              "value": 0.728
            },
            {
              "date": "2026-03-16",
              "value": 0.727
            },
            {
              "date": "2026-03-17",
              "value": 0.727
            },
            {
              "date": "2026-03-18",
              "value": 0.727
            },
            {
              "date": "2026-03-19",
              "value": 0.728
            },
            {
              "date": "2026-03-23",
              "value": 0.727
            },
            {
              "date": "2026-03-24",
              "value": 0.727
            },
            {
              "date": "2026-03-25",
              "value": 0.727
            },
            {
              "date": "2026-03-26",
              "value": 0.727
            },
            {
              "date": "2026-03-27",
              "value": 0.727
            },
            {
              "date": "2026-03-30",
              "value": 0.726
            },
            {
              "date": "2026-03-31",
              "value": 0.727
            },
            {
              "date": "2026-04-01",
              "value": 0.728
            },
            {
              "date": "2026-04-02",
              "value": 0.727
            },
            {
              "date": "2026-04-03",
              "value": 0.728
            },
            {
              "date": "2026-04-06",
              "value": 0.727
            },
            {
              "date": "2026-04-07",
              "value": 0.727
            },
            {
              "date": "2026-04-08",
              "value": 0.727
            },
            {
              "date": "2026-04-09",
              "value": 0.727
            },
            {
              "date": "2026-04-10",
              "value": 0.728
            },
            {
              "date": "2026-04-13",
              "value": 0.726
            },
            {
              "date": "2026-04-14",
              "value": 0.726
            },
            {
              "date": "2026-04-15",
              "value": 0.727
            },
            {
              "date": "2026-04-16",
              "value": 0.727
            },
            {
              "date": "2026-04-17",
              "value": 0.728
            },
            {
              "date": "2026-04-20",
              "value": 0.727
            },
            {
              "date": "2026-04-21",
              "value": 0.727
            },
            {
              "date": "2026-04-22",
              "value": 0.727
            },
            {
              "date": "2026-04-23",
              "value": 0.727
            },
            {
              "date": "2026-04-24",
              "value": 0.728
            },
            {
              "date": "2026-04-27",
              "value": 0.727
            },
            {
              "date": "2026-04-28",
              "value": 0.727
            },
            {
              "date": "2026-04-30",
              "value": 0.727
            },
            {
              "date": "2026-05-01",
              "value": 0.727
            },
            {
              "date": "2026-05-07",
              "value": 0.727
            },
            {
              "date": "2026-05-08",
              "value": 0.727
            },
            {
              "date": "2026-05-11",
              "value": 0.726
            },
            {
              "date": "2026-05-12",
              "value": 0.727
            },
            {
              "date": "2026-05-13",
              "value": 0.727
            },
            {
              "date": "2026-05-14",
              "value": 0.727
            },
            {
              "date": "2026-05-15",
              "value": 0.727
            },
            {
              "date": "2026-05-18",
              "value": 0.728
            },
            {
              "date": "2026-05-19",
              "value": 0.728
            },
            {
              "date": "2026-05-20",
              "value": 0.728
            },
            {
              "date": "2026-05-21",
              "value": 0.727
            },
            {
              "date": "2026-05-22",
              "value": 0.726
            },
            {
              "date": "2026-05-25",
              "value": 0.727
            },
            {
              "date": "2026-05-26",
              "value": 0.727
            },
            {
              "date": "2026-05-27",
              "value": 0.727
            },
            {
              "date": "2026-05-28",
              "value": 0.727
            },
            {
              "date": "2026-05-29",
              "value": 0.727
            },
            {
              "date": "2026-06-01",
              "value": 0.726
            },
            {
              "date": "2026-06-02",
              "value": 0.727
            },
            {
              "date": "2026-06-03",
              "value": 0.727
            },
            {
              "date": "2026-06-04",
              "value": 0.726
            },
            {
              "date": "2026-06-05",
              "value": 0.727
            },
            {
              "date": "2026-06-08",
              "value": 0.727
            },
            {
              "date": "2026-06-09",
              "value": 0.727
            },
            {
              "date": "2026-06-10",
              "value": 0.727
            },
            {
              "date": "2026-06-11",
              "value": 0.727
            },
            {
              "date": "2026-06-12",
              "value": 0.727
            },
            {
              "date": "2026-06-15",
              "value": 0.727
            },
            {
              "date": "2026-06-16",
              "value": 0.727
            },
            {
              "date": "2026-06-17",
              "value": 0.978
            },
            {
              "date": "2026-06-18",
              "value": 0.977
            },
            {
              "date": "2026-06-19",
              "value": 0.977
            },
            {
              "date": "2026-06-22",
              "value": 0.977
            },
            {
              "date": "2026-06-23",
              "value": 0.976
            },
            {
              "date": "2026-06-24",
              "value": 0.977
            },
            {
              "date": "2026-06-25",
              "value": 0.978
            },
            {
              "date": "2026-06-26",
              "value": 0.977
            },
            {
              "date": "2026-06-29",
              "value": 0.978
            },
            {
              "date": "2026-06-30",
              "value": 0.976
            },
            {
              "date": "2026-07-01",
              "value": 0.977
            },
            {
              "date": "2026-07-02",
              "value": 0.977
            },
            {
              "date": "2026-07-03",
              "value": 0.977
            },
            {
              "date": "2026-07-06",
              "value": 0.977
            },
            {
              "date": "2026-07-07",
              "value": 0.978
            }
          ],
          "y_axis": "y1"
        }
      ]
    },
    {
      "id": "jpy_jgb_curve_1y",
      "title": "JGB收益率：2Y / 10Y / 30Y",
      "chart_type": "line",
      "unit": "%",
      "data_source": "SQLite jpy_carry_series_ts",
      "series": [
        {
          "id": "JGB2",
          "label": "JGB 2Y",
          "points": [
            {
              "date": "2025-06-06",
              "value": 0.76
            },
            {
              "date": "2025-06-09",
              "value": 0.775
            },
            {
              "date": "2025-06-10",
              "value": 0.771
            },
            {
              "date": "2025-06-11",
              "value": 0.756
            },
            {
              "date": "2025-06-12",
              "value": 0.756
            },
            {
              "date": "2025-06-13",
              "value": 0.736
            },
            {
              "date": "2025-06-16",
              "value": 0.758
            },
            {
              "date": "2025-06-17",
              "value": 0.769
            },
            {
              "date": "2025-06-18",
              "value": 0.755
            },
            {
              "date": "2025-06-19",
              "value": 0.728
            },
            {
              "date": "2025-06-20",
              "value": 0.728
            },
            {
              "date": "2025-06-23",
              "value": 0.738
            },
            {
              "date": "2025-06-24",
              "value": 0.738
            },
            {
              "date": "2025-06-25",
              "value": 0.724
            },
            {
              "date": "2025-06-26",
              "value": 0.735
            },
            {
              "date": "2025-06-27",
              "value": 0.74
            },
            {
              "date": "2025-06-30",
              "value": 0.746
            },
            {
              "date": "2025-07-01",
              "value": 0.735
            },
            {
              "date": "2025-07-02",
              "value": 0.741
            },
            {
              "date": "2025-07-03",
              "value": 0.746
            },
            {
              "date": "2025-07-04",
              "value": 0.736
            },
            {
              "date": "2025-07-07",
              "value": 0.732
            },
            {
              "date": "2025-07-08",
              "value": 0.733
            },
            {
              "date": "2025-07-09",
              "value": 0.754
            },
            {
              "date": "2025-07-10",
              "value": 0.76
            },
            {
              "date": "2025-07-11",
              "value": 0.764
            },
            {
              "date": "2025-07-14",
              "value": 0.781
            },
            {
              "date": "2025-07-15",
              "value": 0.792
            },
            {
              "date": "2025-07-16",
              "value": 0.793
            },
            {
              "date": "2025-07-17",
              "value": 0.788
            },
            {
              "date": "2025-07-18",
              "value": 0.772
            },
            {
              "date": "2025-07-22",
              "value": 0.76
            },
            {
              "date": "2025-07-23",
              "value": 0.838
            },
            {
              "date": "2025-07-24",
              "value": 0.854
            },
            {
              "date": "2025-07-25",
              "value": 0.863
            },
            {
              "date": "2025-07-28",
              "value": 0.849
            },
            {
              "date": "2025-07-29",
              "value": 0.835
            },
            {
              "date": "2025-07-30",
              "value": 0.826
            },
            {
              "date": "2025-07-31",
              "value": 0.826
            },
            {
              "date": "2025-08-01",
              "value": 0.814
            },
            {
              "date": "2025-08-04",
              "value": 0.764
            },
            {
              "date": "2025-08-05",
              "value": 0.754
            },
            {
              "date": "2025-08-06",
              "value": 0.774
            },
            {
              "date": "2025-08-07",
              "value": 0.77
            },
            {
              "date": "2025-08-08",
              "value": 0.77
            },
            {
              "date": "2025-08-12",
              "value": 0.775
            },
            {
              "date": "2025-08-13",
              "value": 0.785
            },
            {
              "date": "2025-08-14",
              "value": 0.822
            },
            {
              "date": "2025-08-15",
              "value": 0.826
            },
            {
              "date": "2025-08-18",
              "value": 0.833
            },
            {
              "date": "2025-08-19",
              "value": 0.849
            },
            {
              "date": "2025-08-20",
              "value": 0.858
            },
            {
              "date": "2025-08-21",
              "value": 0.862
            },
            {
              "date": "2025-08-22",
              "value": 0.873
            },
            {
              "date": "2025-08-25",
              "value": 0.869
            },
            {
              "date": "2025-08-26",
              "value": 0.874
            },
            {
              "date": "2025-08-27",
              "value": 0.869
            },
            {
              "date": "2025-08-28",
              "value": 0.871
            },
            {
              "date": "2025-08-29",
              "value": 0.871
            },
            {
              "date": "2025-09-01",
              "value": 0.88
            },
            {
              "date": "2025-09-02",
              "value": 0.87
            },
            {
              "date": "2025-09-03",
              "value": 0.87
            },
            {
              "date": "2025-09-04",
              "value": 0.855
            },
            {
              "date": "2025-09-05",
              "value": 0.841
            },
            {
              "date": "2025-09-08",
              "value": 0.831
            },
            {
              "date": "2025-09-09",
              "value": 0.842
            },
            {
              "date": "2025-09-10",
              "value": 0.857
            },
            {
              "date": "2025-09-11",
              "value": 0.862
            },
            {
              "date": "2025-09-12",
              "value": 0.873
            },
            {
              "date": "2025-09-16",
              "value": 0.884
            },
            {
              "date": "2025-09-17",
              "value": 0.883
            },
            {
              "date": "2025-09-18",
              "value": 0.888
            },
            {
              "date": "2025-09-19",
              "value": 0.918
            },
            {
              "date": "2025-09-22",
              "value": 0.935
            },
            {
              "date": "2025-09-24",
              "value": 0.932
            },
            {
              "date": "2025-09-25",
              "value": 0.936
            },
            {
              "date": "2025-09-26",
              "value": 0.931
            },
            {
              "date": "2025-09-29",
              "value": 0.931
            },
            {
              "date": "2025-09-30",
              "value": 0.958
            },
            {
              "date": "2025-10-01",
              "value": 0.954
            },
            {
              "date": "2025-10-02",
              "value": 0.955
            },
            {
              "date": "2025-10-03",
              "value": 0.945
            },
            {
              "date": "2025-10-06",
              "value": 0.899
            },
            {
              "date": "2025-10-07",
              "value": 0.909
            },
            {
              "date": "2025-10-08",
              "value": 0.93
            },
            {
              "date": "2025-10-09",
              "value": 0.93
            },
            {
              "date": "2025-10-10",
              "value": 0.925
            },
            {
              "date": "2025-10-14",
              "value": 0.895
            },
            {
              "date": "2025-10-15",
              "value": 0.9
            },
            {
              "date": "2025-10-16",
              "value": 0.92
            },
            {
              "date": "2025-10-17",
              "value": 0.909
            },
            {
              "date": "2025-10-20",
              "value": 0.95
            },
            {
              "date": "2025-10-21",
              "value": 0.94
            },
            {
              "date": "2025-10-22",
              "value": 0.929
            },
            {
              "date": "2025-10-23",
              "value": 0.933
            },
            {
              "date": "2025-10-24",
              "value": 0.932
            },
            {
              "date": "2025-10-27",
              "value": 0.943
            },
            {
              "date": "2025-10-28",
              "value": 0.94
            },
            {
              "date": "2025-10-29",
              "value": 0.943
            },
            {
              "date": "2025-10-30",
              "value": 0.929
            },
            {
              "date": "2025-10-31",
              "value": 0.928
            },
            {
              "date": "2025-11-04",
              "value": 0.945
            },
            {
              "date": "2025-11-05",
              "value": 0.93
            },
            {
              "date": "2025-11-06",
              "value": 0.941
            },
            {
              "date": "2025-11-07",
              "value": 0.941
            },
            {
              "date": "2025-11-10",
              "value": 0.948
            },
            {
              "date": "2025-11-11",
              "value": 0.937
            },
            {
              "date": "2025-11-12",
              "value": 0.942
            },
            {
              "date": "2025-11-13",
              "value": 0.932
            },
            {
              "date": "2025-11-14",
              "value": 0.932
            },
            {
              "date": "2025-11-17",
              "value": 0.938
            },
            {
              "date": "2025-11-18",
              "value": 0.928
            },
            {
              "date": "2025-11-19",
              "value": 0.934
            },
            {
              "date": "2025-11-20",
              "value": 0.965
            },
            {
              "date": "2025-11-21",
              "value": 0.959
            },
            {
              "date": "2025-11-25",
              "value": 0.975
            },
            {
              "date": "2025-11-26",
              "value": 0.985
            },
            {
              "date": "2025-11-27",
              "value": 0.977
            },
            {
              "date": "2025-11-28",
              "value": 0.992
            },
            {
              "date": "2025-12-01",
              "value": 1.02
            },
            {
              "date": "2025-12-02",
              "value": 1.005
            },
            {
              "date": "2025-12-03",
              "value": 1.016
            },
            {
              "date": "2025-12-04",
              "value": 1.021
            },
            {
              "date": "2025-12-05",
              "value": 1.052
            },
            {
              "date": "2025-12-08",
              "value": 1.063
            },
            {
              "date": "2025-12-09",
              "value": 1.069
            },
            {
              "date": "2025-12-10",
              "value": 1.074
            },
            {
              "date": "2025-12-11",
              "value": 1.054
            },
            {
              "date": "2025-12-12",
              "value": 1.07
            },
            {
              "date": "2025-12-15",
              "value": 1.071
            },
            {
              "date": "2025-12-16",
              "value": 1.067
            },
            {
              "date": "2025-12-17",
              "value": 1.077
            },
            {
              "date": "2025-12-18",
              "value": 1.073
            },
            {
              "date": "2025-12-19",
              "value": 1.101
            },
            {
              "date": "2025-12-22",
              "value": 1.129
            },
            {
              "date": "2025-12-23",
              "value": 1.111
            },
            {
              "date": "2025-12-24",
              "value": 1.111
            },
            {
              "date": "2025-12-25",
              "value": 1.147
            },
            {
              "date": "2025-12-26",
              "value": 1.141
            },
            {
              "date": "2025-12-29",
              "value": 1.15
            },
            {
              "date": "2025-12-30",
              "value": 1.167
            },
            {
              "date": "2026-01-05",
              "value": 1.194
            },
            {
              "date": "2026-01-06",
              "value": 1.185
            },
            {
              "date": "2026-01-07",
              "value": 1.17
            },
            {
              "date": "2026-01-08",
              "value": 1.129
            },
            {
              "date": "2026-01-09",
              "value": 1.151
            },
            {
              "date": "2026-01-13",
              "value": 1.164
            },
            {
              "date": "2026-01-14",
              "value": 1.186
            },
            {
              "date": "2026-01-15",
              "value": 1.19
            },
            {
              "date": "2026-01-16",
              "value": 1.205
            },
            {
              "date": "2026-01-19",
              "value": 1.23
            },
            {
              "date": "2026-01-20",
              "value": 1.22
            },
            {
              "date": "2026-01-21",
              "value": 1.235
            },
            {
              "date": "2026-01-22",
              "value": 1.224
            },
            {
              "date": "2026-01-23",
              "value": 1.262
            },
            {
              "date": "2026-01-26",
              "value": 1.277
            },
            {
              "date": "2026-01-27",
              "value": 1.284
            },
            {
              "date": "2026-01-28",
              "value": 1.257
            },
            {
              "date": "2026-01-29",
              "value": 1.264
            },
            {
              "date": "2026-01-30",
              "value": 1.251
            },
            {
              "date": "2026-02-02",
              "value": 1.265
            },
            {
              "date": "2026-02-03",
              "value": 1.286
            },
            {
              "date": "2026-02-04",
              "value": 1.276
            },
            {
              "date": "2026-02-05",
              "value": 1.276
            },
            {
              "date": "2026-02-06",
              "value": 1.281
            },
            {
              "date": "2026-02-09",
              "value": 1.313
            },
            {
              "date": "2026-02-10",
              "value": 1.303
            },
            {
              "date": "2026-02-12",
              "value": 1.305
            },
            {
              "date": "2026-02-13",
              "value": 1.289
            },
            {
              "date": "2026-02-16",
              "value": 1.275
            },
            {
              "date": "2026-02-17",
              "value": 1.233
            },
            {
              "date": "2026-02-18",
              "value": 1.242
            },
            {
              "date": "2026-02-19",
              "value": 1.265
            },
            {
              "date": "2026-02-20",
              "value": 1.26
            },
            {
              "date": "2026-02-24",
              "value": 1.251
            },
            {
              "date": "2026-02-25",
              "value": 1.224
            },
            {
              "date": "2026-02-26",
              "value": 1.246
            },
            {
              "date": "2026-02-27",
              "value": 1.25
            },
            {
              "date": "2026-03-02",
              "value": 1.219
            },
            {
              "date": "2026-03-03",
              "value": 1.25
            },
            {
              "date": "2026-03-04",
              "value": 1.235
            },
            {
              "date": "2026-03-05",
              "value": 1.256
            },
            {
              "date": "2026-03-06",
              "value": 1.246
            },
            {
              "date": "2026-03-09",
              "value": 1.242
            },
            {
              "date": "2026-03-10",
              "value": 1.258
            },
            {
              "date": "2026-03-11",
              "value": 1.253
            },
            {
              "date": "2026-03-12",
              "value": 1.263
            },
            {
              "date": "2026-03-13",
              "value": 1.289
            },
            {
              "date": "2026-03-16",
              "value": 1.287
            },
            {
              "date": "2026-03-17",
              "value": 1.28
            },
            {
              "date": "2026-03-18",
              "value": 1.261
            },
            {
              "date": "2026-03-19",
              "value": 1.277
            },
            {
              "date": "2026-03-23",
              "value": 1.311
            },
            {
              "date": "2026-03-24",
              "value": 1.311
            },
            {
              "date": "2026-03-25",
              "value": 1.317
            },
            {
              "date": "2026-03-26",
              "value": 1.348
            },
            {
              "date": "2026-03-27",
              "value": 1.393
            },
            {
              "date": "2026-03-30",
              "value": 1.369
            },
            {
              "date": "2026-03-31",
              "value": 1.375
            },
            {
              "date": "2026-04-01",
              "value": 1.349
            },
            {
              "date": "2026-04-02",
              "value": 1.39
            },
            {
              "date": "2026-04-03",
              "value": 1.391
            },
            {
              "date": "2026-04-06",
              "value": 1.402
            },
            {
              "date": "2026-04-07",
              "value": 1.387
            },
            {
              "date": "2026-04-08",
              "value": 1.382
            },
            {
              "date": "2026-04-09",
              "value": 1.394
            },
            {
              "date": "2026-04-10",
              "value": 1.405
            },
            {
              "date": "2026-04-13",
              "value": 1.401
            },
            {
              "date": "2026-04-14",
              "value": 1.382
            },
            {
              "date": "2026-04-15",
              "value": 1.382
            },
            {
              "date": "2026-04-16",
              "value": 1.366
            },
            {
              "date": "2026-04-17",
              "value": 1.372
            },
            {
              "date": "2026-04-20",
              "value": 1.369
            },
            {
              "date": "2026-04-21",
              "value": 1.359
            },
            {
              "date": "2026-04-22",
              "value": 1.362
            },
            {
              "date": "2026-04-23",
              "value": 1.365
            },
            {
              "date": "2026-04-24",
              "value": 1.363
            },
            {
              "date": "2026-04-27",
              "value": 1.375
            },
            {
              "date": "2026-04-28",
              "value": 1.389
            },
            {
              "date": "2026-04-30",
              "value": 1.402
            },
            {
              "date": "2026-05-01",
              "value": 1.385
            },
            {
              "date": "2026-05-07",
              "value": 1.372
            },
            {
              "date": "2026-05-08",
              "value": 1.378
            },
            {
              "date": "2026-05-11",
              "value": 1.395
            },
            {
              "date": "2026-05-12",
              "value": 1.401
            },
            {
              "date": "2026-05-13",
              "value": 1.401
            },
            {
              "date": "2026-05-14",
              "value": 1.407
            },
            {
              "date": "2026-05-15",
              "value": 1.413
            },
            {
              "date": "2026-05-18",
              "value": 1.431
            },
            {
              "date": "2026-05-19",
              "value": 1.452
            },
            {
              "date": "2026-05-20",
              "value": 1.464
            },
            {
              "date": "2026-05-21",
              "value": 1.453
            },
            {
              "date": "2026-05-22",
              "value": 1.443
            },
            {
              "date": "2026-05-25",
              "value": 1.42
            },
            {
              "date": "2026-05-26",
              "value": 1.421
            },
            {
              "date": "2026-05-27",
              "value": 1.399
            },
            {
              "date": "2026-05-28",
              "value": 1.366
            },
            {
              "date": "2026-05-29",
              "value": 1.393
            },
            {
              "date": "2026-06-01",
              "value": 1.4
            },
            {
              "date": "2026-06-02",
              "value": 1.38
            },
            {
              "date": "2026-06-03",
              "value": 1.401
            },
            {
              "date": "2026-06-04",
              "value": 1.417
            },
            {
              "date": "2026-06-05",
              "value": 1.412
            },
            {
              "date": "2026-06-08",
              "value": 1.42
            },
            {
              "date": "2026-06-09",
              "value": 1.42
            },
            {
              "date": "2026-06-10",
              "value": 1.426
            },
            {
              "date": "2026-06-11",
              "value": 1.427
            },
            {
              "date": "2026-06-12",
              "value": 1.417
            },
            {
              "date": "2026-06-15",
              "value": 1.409
            },
            {
              "date": "2026-06-16",
              "value": 1.414
            },
            {
              "date": "2026-06-17",
              "value": 1.398
            },
            {
              "date": "2026-06-18",
              "value": 1.4
            },
            {
              "date": "2026-06-19",
              "value": 1.409
            },
            {
              "date": "2026-06-22",
              "value": 1.415
            },
            {
              "date": "2026-06-23",
              "value": 1.426
            },
            {
              "date": "2026-06-24",
              "value": 1.432
            },
            {
              "date": "2026-06-25",
              "value": 1.421
            },
            {
              "date": "2026-06-26",
              "value": 1.409
            },
            {
              "date": "2026-06-29",
              "value": 1.411
            },
            {
              "date": "2026-06-30",
              "value": 1.382
            }
          ]
        },
        {
          "id": "JGB10",
          "label": "JGB 10Y",
          "points": [
            {
              "date": "2025-06-06",
              "value": 1.477
            },
            {
              "date": "2025-06-09",
              "value": 1.491
            },
            {
              "date": "2025-06-10",
              "value": 1.498
            },
            {
              "date": "2025-06-11",
              "value": 1.48
            },
            {
              "date": "2025-06-12",
              "value": 1.48
            },
            {
              "date": "2025-06-13",
              "value": 1.429
            },
            {
              "date": "2025-06-16",
              "value": 1.477
            },
            {
              "date": "2025-06-17",
              "value": 1.498
            },
            {
              "date": "2025-06-18",
              "value": 1.479
            },
            {
              "date": "2025-06-19",
              "value": 1.439
            },
            {
              "date": "2025-06-20",
              "value": 1.424
            },
            {
              "date": "2025-06-23",
              "value": 1.437
            },
            {
              "date": "2025-06-24",
              "value": 1.445
            },
            {
              "date": "2025-06-25",
              "value": 1.426
            },
            {
              "date": "2025-06-26",
              "value": 1.445
            },
            {
              "date": "2025-06-27",
              "value": 1.459
            },
            {
              "date": "2025-06-30",
              "value": 1.462
            },
            {
              "date": "2025-07-01",
              "value": 1.419
            },
            {
              "date": "2025-07-02",
              "value": 1.434
            },
            {
              "date": "2025-07-03",
              "value": 1.448
            },
            {
              "date": "2025-07-04",
              "value": 1.444
            },
            {
              "date": "2025-07-07",
              "value": 1.463
            },
            {
              "date": "2025-07-08",
              "value": 1.492
            },
            {
              "date": "2025-07-09",
              "value": 1.507
            },
            {
              "date": "2025-07-10",
              "value": 1.498
            },
            {
              "date": "2025-07-11",
              "value": 1.507
            },
            {
              "date": "2025-07-14",
              "value": 1.574
            },
            {
              "date": "2025-07-15",
              "value": 1.588
            },
            {
              "date": "2025-07-16",
              "value": 1.575
            },
            {
              "date": "2025-07-17",
              "value": 1.561
            },
            {
              "date": "2025-07-18",
              "value": 1.528
            },
            {
              "date": "2025-07-22",
              "value": 1.51
            },
            {
              "date": "2025-07-23",
              "value": 1.596
            },
            {
              "date": "2025-07-24",
              "value": 1.605
            },
            {
              "date": "2025-07-25",
              "value": 1.605
            },
            {
              "date": "2025-07-28",
              "value": 1.571
            },
            {
              "date": "2025-07-29",
              "value": 1.564
            },
            {
              "date": "2025-07-30",
              "value": 1.565
            },
            {
              "date": "2025-07-31",
              "value": 1.559
            },
            {
              "date": "2025-08-01",
              "value": 1.56
            },
            {
              "date": "2025-08-04",
              "value": 1.52
            },
            {
              "date": "2025-08-05",
              "value": 1.487
            },
            {
              "date": "2025-08-06",
              "value": 1.509
            },
            {
              "date": "2025-08-07",
              "value": 1.5
            },
            {
              "date": "2025-08-08",
              "value": 1.502
            },
            {
              "date": "2025-08-12",
              "value": 1.516
            },
            {
              "date": "2025-08-13",
              "value": 1.53
            },
            {
              "date": "2025-08-14",
              "value": 1.563
            },
            {
              "date": "2025-08-15",
              "value": 1.574
            },
            {
              "date": "2025-08-18",
              "value": 1.584
            },
            {
              "date": "2025-08-19",
              "value": 1.603
            },
            {
              "date": "2025-08-20",
              "value": 1.617
            },
            {
              "date": "2025-08-21",
              "value": 1.617
            },
            {
              "date": "2025-08-22",
              "value": 1.626
            },
            {
              "date": "2025-08-25",
              "value": 1.628
            },
            {
              "date": "2025-08-26",
              "value": 1.631
            },
            {
              "date": "2025-08-27",
              "value": 1.637
            },
            {
              "date": "2025-08-28",
              "value": 1.628
            },
            {
              "date": "2025-08-29",
              "value": 1.613
            },
            {
              "date": "2025-09-01",
              "value": 1.633
            },
            {
              "date": "2025-09-02",
              "value": 1.615
            },
            {
              "date": "2025-09-03",
              "value": 1.643
            },
            {
              "date": "2025-09-04",
              "value": 1.617
            },
            {
              "date": "2025-09-05",
              "value": 1.59
            },
            {
              "date": "2025-09-08",
              "value": 1.586
            },
            {
              "date": "2025-09-09",
              "value": 1.58
            },
            {
              "date": "2025-09-10",
              "value": 1.585
            },
            {
              "date": "2025-09-11",
              "value": 1.594
            },
            {
              "date": "2025-09-12",
              "value": 1.613
            },
            {
              "date": "2025-09-16",
              "value": 1.623
            },
            {
              "date": "2025-09-17",
              "value": 1.611
            },
            {
              "date": "2025-09-18",
              "value": 1.615
            },
            {
              "date": "2025-09-19",
              "value": 1.655
            },
            {
              "date": "2025-09-22",
              "value": 1.669
            },
            {
              "date": "2025-09-24",
              "value": 1.655
            },
            {
              "date": "2025-09-25",
              "value": 1.659
            },
            {
              "date": "2025-09-26",
              "value": 1.669
            },
            {
              "date": "2025-09-29",
              "value": 1.657
            },
            {
              "date": "2025-09-30",
              "value": 1.662
            },
            {
              "date": "2025-10-01",
              "value": 1.663
            },
            {
              "date": "2025-10-02",
              "value": 1.675
            },
            {
              "date": "2025-10-03",
              "value": 1.667
            },
            {
              "date": "2025-10-06",
              "value": 1.677
            },
            {
              "date": "2025-10-07",
              "value": 1.682
            },
            {
              "date": "2025-10-08",
              "value": 1.701
            },
            {
              "date": "2025-10-09",
              "value": 1.697
            },
            {
              "date": "2025-10-10",
              "value": 1.697
            },
            {
              "date": "2025-10-14",
              "value": 1.67
            },
            {
              "date": "2025-10-15",
              "value": 1.662
            },
            {
              "date": "2025-10-16",
              "value": 1.663
            },
            {
              "date": "2025-10-17",
              "value": 1.638
            },
            {
              "date": "2025-10-20",
              "value": 1.676
            },
            {
              "date": "2025-10-21",
              "value": 1.667
            },
            {
              "date": "2025-10-22",
              "value": 1.663
            },
            {
              "date": "2025-10-23",
              "value": 1.667
            },
            {
              "date": "2025-10-24",
              "value": 1.667
            },
            {
              "date": "2025-10-27",
              "value": 1.683
            },
            {
              "date": "2025-10-28",
              "value": 1.654
            },
            {
              "date": "2025-10-29",
              "value": 1.664
            },
            {
              "date": "2025-10-30",
              "value": 1.66
            },
            {
              "date": "2025-10-31",
              "value": 1.67
            },
            {
              "date": "2025-11-04",
              "value": 1.684
            },
            {
              "date": "2025-11-05",
              "value": 1.676
            },
            {
              "date": "2025-11-06",
              "value": 1.694
            },
            {
              "date": "2025-11-07",
              "value": 1.688
            },
            {
              "date": "2025-11-10",
              "value": 1.712
            },
            {
              "date": "2025-11-11",
              "value": 1.704
            },
            {
              "date": "2025-11-12",
              "value": 1.7
            },
            {
              "date": "2025-11-13",
              "value": 1.705
            },
            {
              "date": "2025-11-14",
              "value": 1.714
            },
            {
              "date": "2025-11-17",
              "value": 1.745
            },
            {
              "date": "2025-11-18",
              "value": 1.759
            },
            {
              "date": "2025-11-19",
              "value": 1.779
            },
            {
              "date": "2025-11-20",
              "value": 1.824
            },
            {
              "date": "2025-11-21",
              "value": 1.792
            },
            {
              "date": "2025-11-25",
              "value": 1.811
            },
            {
              "date": "2025-11-26",
              "value": 1.825
            },
            {
              "date": "2025-11-27",
              "value": 1.807
            },
            {
              "date": "2025-11-28",
              "value": 1.812
            },
            {
              "date": "2025-12-01",
              "value": 1.881
            },
            {
              "date": "2025-12-02",
              "value": 1.864
            },
            {
              "date": "2025-12-03",
              "value": 1.897
            },
            {
              "date": "2025-12-04",
              "value": 1.939
            },
            {
              "date": "2025-12-05",
              "value": 1.951
            },
            {
              "date": "2025-12-08",
              "value": 1.966
            },
            {
              "date": "2025-12-09",
              "value": 1.962
            },
            {
              "date": "2025-12-10",
              "value": 1.958
            },
            {
              "date": "2025-12-11",
              "value": 1.933
            },
            {
              "date": "2025-12-12",
              "value": 1.956
            },
            {
              "date": "2025-12-15",
              "value": 1.961
            },
            {
              "date": "2025-12-16",
              "value": 1.957
            },
            {
              "date": "2025-12-17",
              "value": 1.98
            },
            {
              "date": "2025-12-18",
              "value": 1.972
            },
            {
              "date": "2025-12-19",
              "value": 2.021
            },
            {
              "date": "2025-12-22",
              "value": 2.073
            },
            {
              "date": "2025-12-23",
              "value": 2.039
            },
            {
              "date": "2025-12-24",
              "value": 2.044
            },
            {
              "date": "2025-12-25",
              "value": 2.042
            },
            {
              "date": "2025-12-26",
              "value": 2.039
            },
            {
              "date": "2025-12-29",
              "value": 2.052
            },
            {
              "date": "2025-12-30",
              "value": 2.066
            },
            {
              "date": "2026-01-05",
              "value": 2.111
            },
            {
              "date": "2026-01-06",
              "value": 2.123
            },
            {
              "date": "2026-01-07",
              "value": 2.124
            },
            {
              "date": "2026-01-08",
              "value": 2.083
            },
            {
              "date": "2026-01-09",
              "value": 2.096
            },
            {
              "date": "2026-01-13",
              "value": 2.163
            },
            {
              "date": "2026-01-14",
              "value": 2.182
            },
            {
              "date": "2026-01-15",
              "value": 2.164
            },
            {
              "date": "2026-01-16",
              "value": 2.182
            },
            {
              "date": "2026-01-19",
              "value": 2.266
            },
            {
              "date": "2026-01-20",
              "value": 2.33
            },
            {
              "date": "2026-01-21",
              "value": 2.28
            },
            {
              "date": "2026-01-22",
              "value": 2.239
            },
            {
              "date": "2026-01-23",
              "value": 2.253
            },
            {
              "date": "2026-01-26",
              "value": 2.236
            },
            {
              "date": "2026-01-27",
              "value": 2.281
            },
            {
              "date": "2026-01-28",
              "value": 2.237
            },
            {
              "date": "2026-01-29",
              "value": 2.252
            },
            {
              "date": "2026-01-30",
              "value": 2.247
            },
            {
              "date": "2026-02-02",
              "value": 2.235
            },
            {
              "date": "2026-02-03",
              "value": 2.258
            },
            {
              "date": "2026-02-04",
              "value": 2.249
            },
            {
              "date": "2026-02-05",
              "value": 2.231
            },
            {
              "date": "2026-02-06",
              "value": 2.236
            },
            {
              "date": "2026-02-09",
              "value": 2.289
            },
            {
              "date": "2026-02-10",
              "value": 2.241
            },
            {
              "date": "2026-02-12",
              "value": 2.238
            },
            {
              "date": "2026-02-13",
              "value": 2.218
            },
            {
              "date": "2026-02-16",
              "value": 2.22
            },
            {
              "date": "2026-02-17",
              "value": 2.143
            },
            {
              "date": "2026-02-18",
              "value": 2.152
            },
            {
              "date": "2026-02-19",
              "value": 2.157
            },
            {
              "date": "2026-02-20",
              "value": 2.125
            },
            {
              "date": "2026-02-24",
              "value": 2.119
            },
            {
              "date": "2026-02-25",
              "value": 2.154
            },
            {
              "date": "2026-02-26",
              "value": 2.168
            },
            {
              "date": "2026-02-27",
              "value": 2.132
            },
            {
              "date": "2026-03-02",
              "value": 2.087
            },
            {
              "date": "2026-03-03",
              "value": 2.148
            },
            {
              "date": "2026-03-04",
              "value": 2.134
            },
            {
              "date": "2026-03-05",
              "value": 2.175
            },
            {
              "date": "2026-03-06",
              "value": 2.18
            },
            {
              "date": "2026-03-09",
              "value": 2.205
            },
            {
              "date": "2026-03-10",
              "value": 2.199
            },
            {
              "date": "2026-03-11",
              "value": 2.178
            },
            {
              "date": "2026-03-12",
              "value": 2.201
            },
            {
              "date": "2026-03-13",
              "value": 2.255
            },
            {
              "date": "2026-03-16",
              "value": 2.288
            },
            {
              "date": "2026-03-17",
              "value": 2.279
            },
            {
              "date": "2026-03-18",
              "value": 2.231
            },
            {
              "date": "2026-03-19",
              "value": 2.273
            },
            {
              "date": "2026-03-23",
              "value": 2.322
            },
            {
              "date": "2026-03-24",
              "value": 2.282
            },
            {
              "date": "2026-03-25",
              "value": 2.267
            },
            {
              "date": "2026-03-26",
              "value": 2.286
            },
            {
              "date": "2026-03-27",
              "value": 2.38
            },
            {
              "date": "2026-03-30",
              "value": 2.368
            },
            {
              "date": "2026-03-31",
              "value": 2.366
            },
            {
              "date": "2026-04-01",
              "value": 2.315
            },
            {
              "date": "2026-04-02",
              "value": 2.395
            },
            {
              "date": "2026-04-03",
              "value": 2.386
            },
            {
              "date": "2026-04-06",
              "value": 2.429
            },
            {
              "date": "2026-04-07",
              "value": 2.411
            },
            {
              "date": "2026-04-08",
              "value": 2.374
            },
            {
              "date": "2026-04-09",
              "value": 2.397
            },
            {
              "date": "2026-04-10",
              "value": 2.439
            },
            {
              "date": "2026-04-13",
              "value": 2.467
            },
            {
              "date": "2026-04-14",
              "value": 2.423
            },
            {
              "date": "2026-04-15",
              "value": 2.414
            },
            {
              "date": "2026-04-16",
              "value": 2.409
            },
            {
              "date": "2026-04-17",
              "value": 2.428
            },
            {
              "date": "2026-04-20",
              "value": 2.405
            },
            {
              "date": "2026-04-21",
              "value": 2.392
            },
            {
              "date": "2026-04-22",
              "value": 2.406
            },
            {
              "date": "2026-04-23",
              "value": 2.429
            },
            {
              "date": "2026-04-24",
              "value": 2.443
            },
            {
              "date": "2026-04-27",
              "value": 2.477
            },
            {
              "date": "2026-04-28",
              "value": 2.468
            },
            {
              "date": "2026-04-30",
              "value": 2.52
            },
            {
              "date": "2026-05-01",
              "value": 2.507
            },
            {
              "date": "2026-05-07",
              "value": 2.485
            },
            {
              "date": "2026-05-08",
              "value": 2.485
            },
            {
              "date": "2026-05-11",
              "value": 2.527
            },
            {
              "date": "2026-05-12",
              "value": 2.546
            },
            {
              "date": "2026-05-13",
              "value": 2.587
            },
            {
              "date": "2026-05-14",
              "value": 2.628
            },
            {
              "date": "2026-05-15",
              "value": 2.691
            },
            {
              "date": "2026-05-18",
              "value": 2.729
            },
            {
              "date": "2026-05-19",
              "value": 2.783
            },
            {
              "date": "2026-05-20",
              "value": 2.77
            },
            {
              "date": "2026-05-21",
              "value": 2.748
            },
            {
              "date": "2026-05-22",
              "value": 2.749
            },
            {
              "date": "2026-05-25",
              "value": 2.686
            },
            {
              "date": "2026-05-26",
              "value": 2.713
            },
            {
              "date": "2026-05-27",
              "value": 2.687
            },
            {
              "date": "2026-05-28",
              "value": 2.692
            },
            {
              "date": "2026-05-29",
              "value": 2.657
            },
            {
              "date": "2026-06-01",
              "value": 2.682
            },
            {
              "date": "2026-06-02",
              "value": 2.577
            },
            {
              "date": "2026-06-03",
              "value": 2.645
            },
            {
              "date": "2026-06-04",
              "value": 2.671
            },
            {
              "date": "2026-06-05",
              "value": 2.669
            },
            {
              "date": "2026-06-08",
              "value": 2.715
            },
            {
              "date": "2026-06-09",
              "value": 2.669
            },
            {
              "date": "2026-06-10",
              "value": 2.681
            },
            {
              "date": "2026-06-11",
              "value": 2.682
            },
            {
              "date": "2026-06-12",
              "value": 2.643
            },
            {
              "date": "2026-06-15",
              "value": 2.589
            },
            {
              "date": "2026-06-16",
              "value": 2.655
            },
            {
              "date": "2026-06-17",
              "value": 2.613
            },
            {
              "date": "2026-06-18",
              "value": 2.628
            },
            {
              "date": "2026-06-19",
              "value": 2.656
            },
            {
              "date": "2026-06-22",
              "value": 2.677
            },
            {
              "date": "2026-06-23",
              "value": 2.683
            },
            {
              "date": "2026-06-24",
              "value": 2.674
            },
            {
              "date": "2026-06-25",
              "value": 2.637
            },
            {
              "date": "2026-06-26",
              "value": 2.611
            },
            {
              "date": "2026-06-29",
              "value": 2.644
            },
            {
              "date": "2026-06-30",
              "value": 2.69
            }
          ]
        },
        {
          "id": "JGB30",
          "label": "JGB 30Y",
          "points": [
            {
              "date": "2025-06-06",
              "value": 2.78
            },
            {
              "date": "2025-06-09",
              "value": 2.805
            },
            {
              "date": "2025-06-10",
              "value": 2.809
            },
            {
              "date": "2025-06-11",
              "value": 2.808
            },
            {
              "date": "2025-06-12",
              "value": 2.804
            },
            {
              "date": "2025-06-13",
              "value": 2.781
            },
            {
              "date": "2025-06-16",
              "value": 2.799
            },
            {
              "date": "2025-06-17",
              "value": 2.823
            },
            {
              "date": "2025-06-18",
              "value": 2.819
            },
            {
              "date": "2025-06-19",
              "value": 2.808
            },
            {
              "date": "2025-06-20",
              "value": 2.798
            },
            {
              "date": "2025-06-23",
              "value": 2.808
            },
            {
              "date": "2025-06-24",
              "value": 2.811
            },
            {
              "date": "2025-06-25",
              "value": 2.796
            },
            {
              "date": "2025-06-26",
              "value": 2.792
            },
            {
              "date": "2025-06-27",
              "value": 2.8
            },
            {
              "date": "2025-06-30",
              "value": 2.803
            },
            {
              "date": "2025-07-01",
              "value": 2.789
            },
            {
              "date": "2025-07-02",
              "value": 2.785
            },
            {
              "date": "2025-07-03",
              "value": 2.844
            },
            {
              "date": "2025-07-04",
              "value": 2.852
            },
            {
              "date": "2025-07-07",
              "value": 2.932
            },
            {
              "date": "2025-07-08",
              "value": 3.007
            },
            {
              "date": "2025-07-09",
              "value": 3.003
            },
            {
              "date": "2025-07-10",
              "value": 3.008
            },
            {
              "date": "2025-07-11",
              "value": 2.992
            },
            {
              "date": "2025-07-14",
              "value": 3.083
            },
            {
              "date": "2025-07-15",
              "value": 3.087
            },
            {
              "date": "2025-07-16",
              "value": 3.011
            },
            {
              "date": "2025-07-17",
              "value": 3.029
            },
            {
              "date": "2025-07-18",
              "value": 3.014
            },
            {
              "date": "2025-07-22",
              "value": 3.022
            },
            {
              "date": "2025-07-23",
              "value": 3.062
            },
            {
              "date": "2025-07-24",
              "value": 3.034
            },
            {
              "date": "2025-07-25",
              "value": 3.006
            },
            {
              "date": "2025-07-28",
              "value": 2.975
            },
            {
              "date": "2025-07-29",
              "value": 2.999
            },
            {
              "date": "2025-07-30",
              "value": 3.019
            },
            {
              "date": "2025-07-31",
              "value": 3.026
            },
            {
              "date": "2025-08-01",
              "value": 3.037
            },
            {
              "date": "2025-08-04",
              "value": 3.046
            },
            {
              "date": "2025-08-05",
              "value": 3.019
            },
            {
              "date": "2025-08-06",
              "value": 3.015
            },
            {
              "date": "2025-08-07",
              "value": 3.006
            },
            {
              "date": "2025-08-08",
              "value": 3.014
            },
            {
              "date": "2025-08-12",
              "value": 3.029
            },
            {
              "date": "2025-08-13",
              "value": 3.025
            },
            {
              "date": "2025-08-14",
              "value": 3.024
            },
            {
              "date": "2025-08-15",
              "value": 3.032
            },
            {
              "date": "2025-08-18",
              "value": 3.049
            },
            {
              "date": "2025-08-19",
              "value": 3.068
            },
            {
              "date": "2025-08-20",
              "value": 3.095
            },
            {
              "date": "2025-08-21",
              "value": 3.098
            },
            {
              "date": "2025-08-22",
              "value": 3.12
            },
            {
              "date": "2025-08-25",
              "value": 3.119
            },
            {
              "date": "2025-08-26",
              "value": 3.11
            },
            {
              "date": "2025-08-27",
              "value": 3.134
            },
            {
              "date": "2025-08-28",
              "value": 3.122
            },
            {
              "date": "2025-08-29",
              "value": 3.096
            },
            {
              "date": "2025-09-01",
              "value": 3.102
            },
            {
              "date": "2025-09-02",
              "value": 3.111
            },
            {
              "date": "2025-09-03",
              "value": 3.17
            },
            {
              "date": "2025-09-04",
              "value": 3.158
            },
            {
              "date": "2025-09-05",
              "value": 3.128
            },
            {
              "date": "2025-09-08",
              "value": 3.167
            },
            {
              "date": "2025-09-09",
              "value": 3.147
            },
            {
              "date": "2025-09-10",
              "value": 3.123
            },
            {
              "date": "2025-09-11",
              "value": 3.115
            },
            {
              "date": "2025-09-12",
              "value": 3.103
            },
            {
              "date": "2025-09-16",
              "value": 3.132
            },
            {
              "date": "2025-09-17",
              "value": 3.108
            },
            {
              "date": "2025-09-18",
              "value": 3.093
            },
            {
              "date": "2025-09-19",
              "value": 3.072
            },
            {
              "date": "2025-09-22",
              "value": 3.094
            },
            {
              "date": "2025-09-24",
              "value": 3.074
            },
            {
              "date": "2025-09-25",
              "value": 3.054
            },
            {
              "date": "2025-09-26",
              "value": 3.084
            },
            {
              "date": "2025-09-29",
              "value": 3.05
            },
            {
              "date": "2025-09-30",
              "value": 3.067
            },
            {
              "date": "2025-10-01",
              "value": 3.074
            },
            {
              "date": "2025-10-02",
              "value": 3.087
            },
            {
              "date": "2025-10-03",
              "value": 3.072
            },
            {
              "date": "2025-10-06",
              "value": 3.175
            },
            {
              "date": "2025-10-07",
              "value": 3.177
            },
            {
              "date": "2025-10-08",
              "value": 3.164
            },
            {
              "date": "2025-10-09",
              "value": 3.18
            },
            {
              "date": "2025-10-10",
              "value": 3.187
            },
            {
              "date": "2025-10-14",
              "value": 3.218
            },
            {
              "date": "2025-10-15",
              "value": 3.175
            },
            {
              "date": "2025-10-16",
              "value": 3.134
            },
            {
              "date": "2025-10-17",
              "value": 3.134
            },
            {
              "date": "2025-10-20",
              "value": 3.129
            },
            {
              "date": "2025-10-21",
              "value": 3.138
            },
            {
              "date": "2025-10-22",
              "value": 3.13
            },
            {
              "date": "2025-10-23",
              "value": 3.101
            },
            {
              "date": "2025-10-24",
              "value": 3.081
            },
            {
              "date": "2025-10-27",
              "value": 3.097
            },
            {
              "date": "2025-10-28",
              "value": 3.083
            },
            {
              "date": "2025-10-29",
              "value": 3.072
            },
            {
              "date": "2025-10-30",
              "value": 3.063
            },
            {
              "date": "2025-10-31",
              "value": 3.068
            },
            {
              "date": "2025-11-04",
              "value": 3.105
            },
            {
              "date": "2025-11-05",
              "value": 3.101
            },
            {
              "date": "2025-11-06",
              "value": 3.105
            },
            {
              "date": "2025-11-07",
              "value": 3.117
            },
            {
              "date": "2025-11-10",
              "value": 3.141
            },
            {
              "date": "2025-11-11",
              "value": 3.177
            },
            {
              "date": "2025-11-12",
              "value": 3.189
            },
            {
              "date": "2025-11-13",
              "value": 3.188
            },
            {
              "date": "2025-11-14",
              "value": 3.205
            },
            {
              "date": "2025-11-17",
              "value": 3.241
            },
            {
              "date": "2025-11-18",
              "value": 3.285
            },
            {
              "date": "2025-11-19",
              "value": 3.308
            },
            {
              "date": "2025-11-20",
              "value": 3.334
            },
            {
              "date": "2025-11-21",
              "value": 3.291
            },
            {
              "date": "2025-11-25",
              "value": 3.302
            },
            {
              "date": "2025-11-26",
              "value": 3.294
            },
            {
              "date": "2025-11-27",
              "value": 3.297
            },
            {
              "date": "2025-11-28",
              "value": 3.3
            },
            {
              "date": "2025-12-01",
              "value": 3.343
            },
            {
              "date": "2025-12-02",
              "value": 3.331
            },
            {
              "date": "2025-12-03",
              "value": 3.367
            },
            {
              "date": "2025-12-04",
              "value": 3.343
            },
            {
              "date": "2025-12-05",
              "value": 3.315
            },
            {
              "date": "2025-12-08",
              "value": 3.338
            },
            {
              "date": "2025-12-09",
              "value": 3.334
            },
            {
              "date": "2025-12-10",
              "value": 3.346
            },
            {
              "date": "2025-12-11",
              "value": 3.334
            },
            {
              "date": "2025-12-12",
              "value": 3.309
            },
            {
              "date": "2025-12-15",
              "value": 3.32
            },
            {
              "date": "2025-12-16",
              "value": 3.307
            },
            {
              "date": "2025-12-17",
              "value": 3.311
            },
            {
              "date": "2025-12-18",
              "value": 3.33
            },
            {
              "date": "2025-12-19",
              "value": 3.362
            },
            {
              "date": "2025-12-22",
              "value": 3.374
            },
            {
              "date": "2025-12-23",
              "value": 3.371
            },
            {
              "date": "2025-12-24",
              "value": 3.371
            },
            {
              "date": "2025-12-25",
              "value": 3.349
            },
            {
              "date": "2025-12-26",
              "value": 3.335
            },
            {
              "date": "2025-12-29",
              "value": 3.371
            },
            {
              "date": "2025-12-30",
              "value": 3.354
            },
            {
              "date": "2026-01-05",
              "value": 3.393
            },
            {
              "date": "2026-01-06",
              "value": 3.42
            },
            {
              "date": "2026-01-07",
              "value": 3.428
            },
            {
              "date": "2026-01-08",
              "value": 3.435
            },
            {
              "date": "2026-01-09",
              "value": 3.399
            },
            {
              "date": "2026-01-13",
              "value": 3.462
            },
            {
              "date": "2026-01-14",
              "value": 3.486
            },
            {
              "date": "2026-01-15",
              "value": 3.454
            },
            {
              "date": "2026-01-16",
              "value": 3.462
            },
            {
              "date": "2026-01-19",
              "value": 3.562
            },
            {
              "date": "2026-01-20",
              "value": 3.765
            },
            {
              "date": "2026-01-21",
              "value": 3.647
            },
            {
              "date": "2026-01-22",
              "value": 3.604
            },
            {
              "date": "2026-01-23",
              "value": 3.585
            },
            {
              "date": "2026-01-26",
              "value": 3.568
            },
            {
              "date": "2026-01-27",
              "value": 3.599
            },
            {
              "date": "2026-01-28",
              "value": 3.579
            },
            {
              "date": "2026-01-29",
              "value": 3.566
            },
            {
              "date": "2026-01-30",
              "value": 3.577
            },
            {
              "date": "2026-02-02",
              "value": 3.583
            },
            {
              "date": "2026-02-03",
              "value": 3.58
            },
            {
              "date": "2026-02-04",
              "value": 3.579
            },
            {
              "date": "2026-02-05",
              "value": 3.525
            },
            {
              "date": "2026-02-06",
              "value": 3.513
            },
            {
              "date": "2026-02-09",
              "value": 3.52
            },
            {
              "date": "2026-02-10",
              "value": 3.468
            },
            {
              "date": "2026-02-12",
              "value": 3.413
            },
            {
              "date": "2026-02-13",
              "value": 3.422
            },
            {
              "date": "2026-02-16",
              "value": 3.461
            },
            {
              "date": "2026-02-17",
              "value": 3.382
            },
            {
              "date": "2026-02-18",
              "value": 3.371
            },
            {
              "date": "2026-02-19",
              "value": 3.34
            },
            {
              "date": "2026-02-20",
              "value": 3.323
            },
            {
              "date": "2026-02-24",
              "value": 3.295
            },
            {
              "date": "2026-02-25",
              "value": 3.38
            },
            {
              "date": "2026-02-26",
              "value": 3.366
            },
            {
              "date": "2026-02-27",
              "value": 3.342
            },
            {
              "date": "2026-03-02",
              "value": 3.293
            },
            {
              "date": "2026-03-03",
              "value": 3.337
            },
            {
              "date": "2026-03-04",
              "value": 3.353
            },
            {
              "date": "2026-03-05",
              "value": 3.374
            },
            {
              "date": "2026-03-06",
              "value": 3.384
            },
            {
              "date": "2026-03-09",
              "value": 3.44
            },
            {
              "date": "2026-03-10",
              "value": 3.412
            },
            {
              "date": "2026-03-11",
              "value": 3.421
            },
            {
              "date": "2026-03-12",
              "value": 3.451
            },
            {
              "date": "2026-03-13",
              "value": 3.479
            },
            {
              "date": "2026-03-16",
              "value": 3.515
            },
            {
              "date": "2026-03-17",
              "value": 3.514
            },
            {
              "date": "2026-03-18",
              "value": 3.462
            },
            {
              "date": "2026-03-19",
              "value": 3.491
            },
            {
              "date": "2026-03-23",
              "value": 3.522
            },
            {
              "date": "2026-03-24",
              "value": 3.509
            },
            {
              "date": "2026-03-25",
              "value": 3.479
            },
            {
              "date": "2026-03-26",
              "value": 3.489
            },
            {
              "date": "2026-03-27",
              "value": 3.629
            },
            {
              "date": "2026-03-30",
              "value": 3.698
            },
            {
              "date": "2026-03-31",
              "value": 3.64
            },
            {
              "date": "2026-04-01",
              "value": 3.564
            },
            {
              "date": "2026-04-02",
              "value": 3.614
            },
            {
              "date": "2026-04-03",
              "value": 3.611
            },
            {
              "date": "2026-04-06",
              "value": 3.672
            },
            {
              "date": "2026-04-07",
              "value": 3.667
            },
            {
              "date": "2026-04-08",
              "value": 3.615
            },
            {
              "date": "2026-04-09",
              "value": 3.619
            },
            {
              "date": "2026-04-10",
              "value": 3.638
            },
            {
              "date": "2026-04-13",
              "value": 3.698
            },
            {
              "date": "2026-04-14",
              "value": 3.633
            },
            {
              "date": "2026-04-15",
              "value": 3.606
            },
            {
              "date": "2026-04-16",
              "value": 3.623
            },
            {
              "date": "2026-04-17",
              "value": 3.622
            },
            {
              "date": "2026-04-20",
              "value": 3.586
            },
            {
              "date": "2026-04-21",
              "value": 3.581
            },
            {
              "date": "2026-04-22",
              "value": 3.597
            },
            {
              "date": "2026-04-23",
              "value": 3.63
            },
            {
              "date": "2026-04-24",
              "value": 3.66
            },
            {
              "date": "2026-04-27",
              "value": 3.675
            },
            {
              "date": "2026-04-28",
              "value": 3.647
            },
            {
              "date": "2026-04-30",
              "value": 3.721
            },
            {
              "date": "2026-05-01",
              "value": 3.706
            },
            {
              "date": "2026-05-07",
              "value": 3.714
            },
            {
              "date": "2026-05-08",
              "value": 3.706
            },
            {
              "date": "2026-05-11",
              "value": 3.741
            },
            {
              "date": "2026-05-12",
              "value": 3.78
            },
            {
              "date": "2026-05-13",
              "value": 3.783
            },
            {
              "date": "2026-05-14",
              "value": 3.852
            },
            {
              "date": "2026-05-15",
              "value": 3.922
            },
            {
              "date": "2026-05-18",
              "value": 4.0
            },
            {
              "date": "2026-05-19",
              "value": 4.043
            },
            {
              "date": "2026-05-20",
              "value": 4.0
            },
            {
              "date": "2026-05-21",
              "value": 3.939
            },
            {
              "date": "2026-05-22",
              "value": 3.931
            },
            {
              "date": "2026-05-25",
              "value": 3.876
            },
            {
              "date": "2026-05-26",
              "value": 3.866
            },
            {
              "date": "2026-05-27",
              "value": 3.856
            },
            {
              "date": "2026-05-28",
              "value": 3.896
            },
            {
              "date": "2026-05-29",
              "value": 3.859
            },
            {
              "date": "2026-06-01",
              "value": 3.863
            },
            {
              "date": "2026-06-02",
              "value": 3.81
            },
            {
              "date": "2026-06-03",
              "value": 3.817
            },
            {
              "date": "2026-06-04",
              "value": 3.833
            },
            {
              "date": "2026-06-05",
              "value": 3.841
            },
            {
              "date": "2026-06-08",
              "value": 3.876
            },
            {
              "date": "2026-06-09",
              "value": 3.823
            },
            {
              "date": "2026-06-10",
              "value": 3.811
            },
            {
              "date": "2026-06-11",
              "value": 3.823
            },
            {
              "date": "2026-06-12",
              "value": 3.767
            },
            {
              "date": "2026-06-15",
              "value": 3.725
            },
            {
              "date": "2026-06-16",
              "value": 3.747
            },
            {
              "date": "2026-06-17",
              "value": 3.709
            },
            {
              "date": "2026-06-18",
              "value": 3.737
            },
            {
              "date": "2026-06-19",
              "value": 3.786
            },
            {
              "date": "2026-06-22",
              "value": 3.797
            },
            {
              "date": "2026-06-23",
              "value": 3.79
            },
            {
              "date": "2026-06-24",
              "value": 3.808
            },
            {
              "date": "2026-06-25",
              "value": 3.781
            },
            {
              "date": "2026-06-26",
              "value": 3.759
            },
            {
              "date": "2026-06-29",
              "value": 3.785
            },
            {
              "date": "2026-06-30",
              "value": 3.873
            }
          ]
        }
      ]
    },
    {
      "id": "jpy_cftc_position_2y",
      "title": "CFTC JPY仓位拥挤度",
      "chart_type": "line",
      "unit": "net/OI",
      "data_source": "SQLite jpy_carry_series_ts.CFTC_JPY_NET_OI",
      "series": [
        {
          "id": "CFTC_JPY_NET_OI",
          "label": "JPY非商业净仓位/OI",
          "points": [
            {
              "date": "2023-12-12",
              "value": -0.3149727658484127
            },
            {
              "date": "2023-12-19",
              "value": -0.3490480800258148
            },
            {
              "date": "2023-12-26",
              "value": -0.2947279091969874
            },
            {
              "date": "2024-01-02",
              "value": -0.3107714543419437
            },
            {
              "date": "2024-01-09",
              "value": -0.27932740552873453
            },
            {
              "date": "2024-01-16",
              "value": -0.26515524427004955
            },
            {
              "date": "2024-01-23",
              "value": -0.2906818855130189
            },
            {
              "date": "2024-01-30",
              "value": -0.3324188423701292
            },
            {
              "date": "2024-02-06",
              "value": -0.32453321620392844
            },
            {
              "date": "2024-02-13",
              "value": -0.3661816462677943
            },
            {
              "date": "2024-02-20",
              "value": -0.39542558555255075
            },
            {
              "date": "2024-02-27",
              "value": -0.4285880380967145
            },
            {
              "date": "2024-03-05",
              "value": -0.37777587050917716
            },
            {
              "date": "2024-03-12",
              "value": -0.31418438627466033
            },
            {
              "date": "2024-03-19",
              "value": -0.3835107438016529
            },
            {
              "date": "2024-03-26",
              "value": -0.42232769928786623
            },
            {
              "date": "2024-04-02",
              "value": -0.45210205518151314
            },
            {
              "date": "2024-04-09",
              "value": -0.4997272550765997
            },
            {
              "date": "2024-04-16",
              "value": -0.5001932892392257
            },
            {
              "date": "2024-04-23",
              "value": -0.535207203562515
            },
            {
              "date": "2024-04-30",
              "value": -0.5028789181957186
            },
            {
              "date": "2024-05-07",
              "value": -0.4499514771942813
            },
            {
              "date": "2024-05-14",
              "value": -0.42399010772632273
            },
            {
              "date": "2024-05-21",
              "value": -0.4791231767419478
            },
            {
              "date": "2024-05-28",
              "value": -0.47977898785786105
            },
            {
              "date": "2024-06-04",
              "value": -0.43596394826556306
            },
            {
              "date": "2024-06-11",
              "value": -0.4340441125804168
            },
            {
              "date": "2024-06-18",
              "value": -0.4972889467785418
            },
            {
              "date": "2024-06-25",
              "value": -0.5111143114946346
            },
            {
              "date": "2024-07-02",
              "value": -0.5266267791445242
            },
            {
              "date": "2024-07-09",
              "value": -0.5216532838139124
            },
            {
              "date": "2024-07-16",
              "value": -0.4917628293810322
            },
            {
              "date": "2024-07-23",
              "value": -0.3486781495069714
            },
            {
              "date": "2024-07-30",
              "value": -0.24232148335318043
            },
            {
              "date": "2024-08-06",
              "value": -0.03798124688479512
            },
            {
              "date": "2024-08-13",
              "value": 0.07326741464714052
            },
            {
              "date": "2024-08-20",
              "value": 0.07458957548616843
            },
            {
              "date": "2024-08-27",
              "value": 0.08127971243546922
            },
            {
              "date": "2024-09-03",
              "value": 0.12581587845591272
            },
            {
              "date": "2024-09-10",
              "value": 0.1481219821839294
            },
            {
              "date": "2024-09-17",
              "value": 0.28496513137774926
            },
            {
              "date": "2024-09-24",
              "value": 0.3178159093316386
            },
            {
              "date": "2024-10-01",
              "value": 0.2893577981651376
            },
            {
              "date": "2024-10-08",
              "value": 0.1857182804992755
            },
            {
              "date": "2024-10-15",
              "value": 0.1723850387373592
            },
            {
              "date": "2024-10-22",
              "value": 0.06159507663814641
            },
            {
              "date": "2024-10-29",
              "value": -0.1098612623619928
            },
            {
              "date": "2024-11-05",
              "value": -0.18733722991830745
            },
            {
              "date": "2024-11-12",
              "value": -0.2518627177051318
            },
            {
              "date": "2024-11-19",
              "value": -0.18445650505535505
            },
            {
              "date": "2024-11-26",
              "value": -0.08925881230133377
            },
            {
              "date": "2024-12-03",
              "value": 0.00908705114678274
            },
            {
              "date": "2024-12-10",
              "value": 0.0937001972099522
            },
            {
              "date": "2024-12-17",
              "value": 0.032811700142563835
            },
            {
              "date": "2024-12-24",
              "value": 0.011513551215623755
            },
            {
              "date": "2024-12-31",
              "value": -0.04079315459653768
            },
            {
              "date": "2025-01-07",
              "value": -0.09502673494747148
            },
            {
              "date": "2025-01-14",
              "value": -0.13132724869614917
            },
            {
              "date": "2025-01-21",
              "value": -0.06933654664020414
            },
            {
              "date": "2025-01-28",
              "value": -0.004423676587264978
            },
            {
              "date": "2025-02-04",
              "value": 0.08092759722479745
            },
            {
              "date": "2025-02-11",
              "value": 0.1998251095809216
            },
            {
              "date": "2025-02-18",
              "value": 0.21542308198447163
            },
            {
              "date": "2025-02-25",
              "value": 0.2915676851384931
            },
            {
              "date": "2025-03-04",
              "value": 0.37710311358153575
            },
            {
              "date": "2025-03-11",
              "value": 0.3001089251375012
            },
            {
              "date": "2025-03-18",
              "value": 0.41462468851895184
            },
            {
              "date": "2025-03-25",
              "value": 0.4127224486302497
            },
            {
              "date": "2025-04-01",
              "value": 0.39135241449791425
            },
            {
              "date": "2025-04-08",
              "value": 0.458498307134974
            },
            {
              "date": "2025-04-15",
              "value": 0.5071728114883031
            },
            {
              "date": "2025-04-22",
              "value": 0.5062666203527074
            },
            {
              "date": "2025-04-29",
              "value": 0.4893213850799736
            },
            {
              "date": "2025-05-06",
              "value": 0.4709383138150852
            },
            {
              "date": "2025-05-13",
              "value": 0.47915977091741513
            },
            {
              "date": "2025-05-20",
              "value": 0.4561078325814673
            },
            {
              "date": "2025-05-27",
              "value": 0.435032399585158
            },
            {
              "date": "2025-06-03",
              "value": 0.4129663832484536
            },
            {
              "date": "2025-06-10",
              "value": 0.37241508977162385
            },
            {
              "date": "2025-06-17",
              "value": 0.4121811648290045
            },
            {
              "date": "2025-06-24",
              "value": 0.4202378267099156
            },
            {
              "date": "2025-07-01",
              "value": 0.40521112104655194
            },
            {
              "date": "2025-07-08",
              "value": 0.37636777795418974
            },
            {
              "date": "2025-07-15",
              "value": 0.3223339038431617
            },
            {
              "date": "2025-07-22",
              "value": 0.340675313059034
            },
            {
              "date": "2025-07-29",
              "value": 0.27116053659055345
            },
            {
              "date": "2025-08-05",
              "value": 0.2430686055403731
            },
            {
              "date": "2025-08-12",
              "value": 0.21139470844024
            },
            {
              "date": "2025-08-19",
              "value": 0.2223065946094641
            },
            {
              "date": "2025-08-26",
              "value": 0.23640749259862437
            },
            {
              "date": "2025-09-02",
              "value": 0.17684532732728384
            },
            {
              "date": "2025-09-09",
              "value": 0.22308476895026522
            },
            {
              "date": "2025-09-16",
              "value": 0.2049629530738936
            },
            {
              "date": "2025-09-23",
              "value": 0.25654016063609053
            },
            {
              "date": "2025-09-30",
              "value": 0.20105589919891662
            },
            {
              "date": "2025-10-07",
              "value": 0.15175955481853873
            },
            {
              "date": "2025-10-14",
              "value": 0.12185453913568063
            },
            {
              "date": "2025-10-21",
              "value": 0.22893724660157558
            },
            {
              "date": "2025-10-28",
              "value": 0.21161021345867675
            },
            {
              "date": "2025-11-04",
              "value": 0.1631656004328591
            },
            {
              "date": "2025-11-10",
              "value": 0.15495213284533874
            },
            {
              "date": "2025-11-18",
              "value": 0.09457105045893838
            },
            {
              "date": "2025-11-25",
              "value": 0.07699030253759945
            },
            {
              "date": "2025-12-02",
              "value": 0.09223039110163375
            },
            {
              "date": "2025-12-09",
              "value": 0.0374890420612957
            },
            {
              "date": "2025-12-16",
              "value": -0.007748650833993979
            },
            {
              "date": "2025-12-23",
              "value": 0.004289963659833593
            },
            {
              "date": "2025-12-30",
              "value": 0.04916611913382635
            },
            {
              "date": "2026-01-06",
              "value": 0.030637957701197364
            },
            {
              "date": "2026-01-13",
              "value": -0.15349270328505107
            },
            {
              "date": "2026-01-20",
              "value": -0.1532054940585837
            },
            {
              "date": "2026-01-27",
              "value": -0.1128369346182239
            },
            {
              "date": "2026-02-03",
              "value": -0.0632983505283644
            },
            {
              "date": "2026-02-10",
              "value": -0.05704169005338142
            },
            {
              "date": "2026-02-17",
              "value": 0.036562168386353885
            },
            {
              "date": "2026-02-24",
              "value": 0.031210020528993486
            },
            {
              "date": "2026-03-03",
              "value": -0.03975039390661835
            },
            {
              "date": "2026-03-10",
              "value": -0.09676235276513964
            },
            {
              "date": "2026-03-17",
              "value": -0.20747624644921148
            },
            {
              "date": "2026-03-24",
              "value": -0.19135919076201213
            },
            {
              "date": "2026-03-31",
              "value": -0.21105434492985323
            },
            {
              "date": "2026-04-07",
              "value": -0.2683149527868496
            },
            {
              "date": "2026-04-14",
              "value": -0.23482265820784323
            },
            {
              "date": "2026-04-21",
              "value": -0.2685185711605483
            },
            {
              "date": "2026-04-28",
              "value": -0.2737780996834594
            },
            {
              "date": "2026-05-05",
              "value": -0.1743986666854988
            },
            {
              "date": "2026-05-12",
              "value": -0.20744002077107077
            },
            {
              "date": "2026-05-19",
              "value": -0.23679120868036907
            },
            {
              "date": "2026-05-26",
              "value": -0.2683562137544641
            },
            {
              "date": "2026-06-02",
              "value": -0.2562866552600607
            },
            {
              "date": "2026-06-09",
              "value": -0.2887056377765678
            },
            {
              "date": "2026-06-16",
              "value": -0.28825805212883404
            },
            {
              "date": "2026-06-23",
              "value": -0.33896480523397443
            },
            {
              "date": "2026-06-30",
              "value": -0.35342562524924515
            }
          ]
        }
      ]
    },
    {
      "id": "jpy_effective_fx_3y",
      "title": "JPY NEER / REER",
      "chart_type": "line",
      "unit": "index",
      "data_source": "SQLite jpy_carry_series_ts",
      "series": [
        {
          "id": "JPY_NEER",
          "label": "JPY NEER",
          "points": [
            {
              "date": "2023-01-01",
              "value": 75.67
            },
            {
              "date": "2023-01-02",
              "value": 77.87
            },
            {
              "date": "2024-01-01",
              "value": 74.37
            },
            {
              "date": "2024-01-02",
              "value": 74.84
            },
            {
              "date": "2025-01-01",
              "value": 71.46
            },
            {
              "date": "2025-01-02",
              "value": 70.53
            }
          ]
        },
        {
          "id": "JPY_REER",
          "label": "JPY REER",
          "points": [
            {
              "date": "2023-01-01",
              "value": 72.15
            },
            {
              "date": "2023-01-02",
              "value": 74.03
            },
            {
              "date": "2024-01-01",
              "value": 71.66
            },
            {
              "date": "2024-01-02",
              "value": 72.4
            },
            {
              "date": "2025-01-01",
              "value": 69.66
            },
            {
              "date": "2025-01-02",
              "value": 68.46
            }
          ]
        }
      ]
    },
    {
      "id": "us_jp_spread",
      "title": "美日利差代理",
      "chart_type": "line",
      "unit": "bp",
      "data_source": "SQLite jpy_carry_series_ts.US_JP_2Y/US_JP_10Y",
      "series": [
        {
          "id": "US_JP_2Y",
          "label": "2Y UST-JGB",
          "points": [
            {
              "date": "2025-06-23",
              "value": 310.2
            },
            {
              "date": "2025-06-24",
              "value": 301.2
            },
            {
              "date": "2025-06-25",
              "value": 301.6
            },
            {
              "date": "2025-06-26",
              "value": 296.50000000000006
            },
            {
              "date": "2025-06-27",
              "value": 299.0
            },
            {
              "date": "2025-06-30",
              "value": 297.40000000000003
            },
            {
              "date": "2025-07-01",
              "value": 304.5
            },
            {
              "date": "2025-07-02",
              "value": 303.9
            },
            {
              "date": "2025-07-03",
              "value": 313.4
            },
            {
              "date": "2025-07-07",
              "value": 316.8
            },
            {
              "date": "2025-07-08",
              "value": 316.7
            },
            {
              "date": "2025-07-09",
              "value": 310.59999999999997
            },
            {
              "date": "2025-07-10",
              "value": 309.99999999999994
            },
            {
              "date": "2025-07-11",
              "value": 313.6
            },
            {
              "date": "2025-07-14",
              "value": 311.9
            },
            {
              "date": "2025-07-15",
              "value": 315.8
            },
            {
              "date": "2025-07-16",
              "value": 308.7
            },
            {
              "date": "2025-07-17",
              "value": 312.2
            },
            {
              "date": "2025-07-18",
              "value": 310.79999999999995
            },
            {
              "date": "2025-07-21",
              "value": 307.8
            },
            {
              "date": "2025-07-22",
              "value": 307.0
            },
            {
              "date": "2025-07-23",
              "value": 304.2
            },
            {
              "date": "2025-07-24",
              "value": 305.6
            },
            {
              "date": "2025-07-25",
              "value": 304.7
            },
            {
              "date": "2025-07-28",
              "value": 306.1
            },
            {
              "date": "2025-07-29",
              "value": 302.5
            },
            {
              "date": "2025-07-30",
              "value": 311.4
            },
            {
              "date": "2025-07-31",
              "value": 311.4
            },
            {
              "date": "2025-08-01",
              "value": 287.59999999999997
            },
            {
              "date": "2025-08-04",
              "value": 292.6
            },
            {
              "date": "2025-08-05",
              "value": 296.6
            },
            {
              "date": "2025-08-06",
              "value": 291.59999999999997
            },
            {
              "date": "2025-08-07",
              "value": 295.0
            },
            {
              "date": "2025-08-08",
              "value": 299.0
            },
            {
              "date": "2025-08-11",
              "value": 299.0
            },
            {
              "date": "2025-08-12",
              "value": 294.5
            },
            {
              "date": "2025-08-13",
              "value": 288.5
            },
            {
              "date": "2025-08-14",
              "value": 291.8
            },
            {
              "date": "2025-08-15",
              "value": 292.4
            },
            {
              "date": "2025-08-18",
              "value": 293.70000000000005
            },
            {
              "date": "2025-08-19",
              "value": 290.09999999999997
            },
            {
              "date": "2025-08-20",
              "value": 288.2
            },
            {
              "date": "2025-08-21",
              "value": 292.8
            },
            {
              "date": "2025-08-22",
              "value": 280.70000000000005
            },
            {
              "date": "2025-08-25",
              "value": 286.09999999999997
            },
            {
              "date": "2025-08-26",
              "value": 273.59999999999997
            },
            {
              "date": "2025-08-27",
              "value": 272.1
            },
            {
              "date": "2025-08-28",
              "value": 274.90000000000003
            },
            {
              "date": "2025-08-29",
              "value": 271.9
            },
            {
              "date": "2025-09-02",
              "value": 279.0
            },
            {
              "date": "2025-09-03",
              "value": 274.0
            },
            {
              "date": "2025-09-04",
              "value": 273.5
            },
            {
              "date": "2025-09-05",
              "value": 266.9
            },
            {
              "date": "2025-09-08",
              "value": 265.90000000000003
            },
            {
              "date": "2025-09-09",
              "value": 269.8
            },
            {
              "date": "2025-09-10",
              "value": 268.29999999999995
            },
            {
              "date": "2025-09-11",
              "value": 265.8
            },
            {
              "date": "2025-09-12",
              "value": 268.70000000000005
            },
            {
              "date": "2025-09-15",
              "value": 266.7
            },
            {
              "date": "2025-09-16",
              "value": 262.59999999999997
            },
            {
              "date": "2025-09-17",
              "value": 263.7
            },
            {
              "date": "2025-09-18",
              "value": 268.2
            },
            {
              "date": "2025-09-19",
              "value": 265.2
            },
            {
              "date": "2025-09-22",
              "value": 267.5
            },
            {
              "date": "2025-09-23",
              "value": 259.5
            },
            {
              "date": "2025-09-24",
              "value": 263.8
            },
            {
              "date": "2025-09-25",
              "value": 270.40000000000003
            },
            {
              "date": "2025-09-26",
              "value": 269.9
            },
            {
              "date": "2025-09-29",
              "value": 269.9
            },
            {
              "date": "2025-09-30",
              "value": 264.20000000000005
            },
            {
              "date": "2025-10-01",
              "value": 259.6
            },
            {
              "date": "2025-10-02",
              "value": 259.5
            },
            {
              "date": "2025-10-03",
              "value": 263.5
            },
            {
              "date": "2025-10-06",
              "value": 270.1
            },
            {
              "date": "2025-10-07",
              "value": 266.09999999999997
            },
            {
              "date": "2025-10-08",
              "value": 265.0
            },
            {
              "date": "2025-10-09",
              "value": 267.0
            },
            {
              "date": "2025-10-10",
              "value": 259.5
            },
            {
              "date": "2025-10-14",
              "value": 258.5
            },
            {
              "date": "2025-10-15",
              "value": 260.0
            },
            {
              "date": "2025-10-16",
              "value": 249.00000000000003
            },
            {
              "date": "2025-10-17",
              "value": 255.10000000000002
            },
            {
              "date": "2025-10-20",
              "value": 250.99999999999997
            },
            {
              "date": "2025-10-21",
              "value": 251.00000000000003
            },
            {
              "date": "2025-10-22",
              "value": 252.1
            },
            {
              "date": "2025-10-23",
              "value": 254.69999999999996
            },
            {
              "date": "2025-10-24",
              "value": 254.8
            },
            {
              "date": "2025-10-27",
              "value": 253.7
            },
            {
              "date": "2025-10-28",
              "value": 253.00000000000003
            },
            {
              "date": "2025-10-29",
              "value": 264.7
            },
            {
              "date": "2025-10-30",
              "value": 268.1
            },
            {
              "date": "2025-10-31",
              "value": 267.2
            },
            {
              "date": "2025-11-03",
              "value": 267.2
            },
            {
              "date": "2025-11-04",
              "value": 263.5
            },
            {
              "date": "2025-11-05",
              "value": 270.0
            },
            {
              "date": "2025-11-06",
              "value": 262.9
            },
            {
              "date": "2025-11-07",
              "value": 260.9
            },
            {
              "date": "2025-11-10",
              "value": 263.2
            },
            {
              "date": "2025-11-12",
              "value": 261.8
            },
            {
              "date": "2025-11-13",
              "value": 264.8
            },
            {
              "date": "2025-11-14",
              "value": 268.8
            },
            {
              "date": "2025-11-17",
              "value": 266.2
            },
            {
              "date": "2025-11-18",
              "value": 265.2
            },
            {
              "date": "2025-11-19",
              "value": 264.59999999999997
            },
            {
              "date": "2025-11-20",
              "value": 258.5
            },
            {
              "date": "2025-11-21",
              "value": 255.09999999999997
            },
            {
              "date": "2025-11-24",
              "value": 250.1
            },
            {
              "date": "2025-11-25",
              "value": 245.5
            },
            {
              "date": "2025-11-26",
              "value": 246.50000000000003
            },
            {
              "date": "2025-11-28",
              "value": 247.8
            },
            {
              "date": "2025-12-01",
              "value": 252.0
            },
            {
              "date": "2025-12-02",
              "value": 250.5
            },
            {
              "date": "2025-12-03",
              "value": 247.40000000000003
            },
            {
              "date": "2025-12-04",
              "value": 249.9
            },
            {
              "date": "2025-12-05",
              "value": 250.8
            },
            {
              "date": "2025-12-08",
              "value": 250.69999999999996
            },
            {
              "date": "2025-12-09",
              "value": 254.1
            },
            {
              "date": "2025-12-10",
              "value": 246.60000000000002
            },
            {
              "date": "2025-12-11",
              "value": 246.60000000000002
            },
            {
              "date": "2025-12-12",
              "value": 245.00000000000003
            },
            {
              "date": "2025-12-15",
              "value": 243.9
            },
            {
              "date": "2025-12-16",
              "value": 241.3
            },
            {
              "date": "2025-12-17",
              "value": 241.3
            },
            {
              "date": "2025-12-18",
              "value": 238.7
            },
            {
              "date": "2025-12-19",
              "value": 237.9
            },
            {
              "date": "2025-12-22",
              "value": 231.1
            },
            {
              "date": "2025-12-23",
              "value": 236.89999999999998
            },
            {
              "date": "2025-12-24",
              "value": 235.9
            },
            {
              "date": "2025-12-26",
              "value": 231.9
            },
            {
              "date": "2025-12-29",
              "value": 230.00000000000003
            },
            {
              "date": "2025-12-30",
              "value": 228.30000000000004
            },
            {
              "date": "2025-12-31",
              "value": 230.29999999999998
            },
            {
              "date": "2026-01-02",
              "value": 230.29999999999998
            },
            {
              "date": "2026-01-05",
              "value": 226.6
            },
            {
              "date": "2026-01-06",
              "value": 228.5
            },
            {
              "date": "2026-01-07",
              "value": 230.00000000000003
            },
            {
              "date": "2026-01-08",
              "value": 236.10000000000002
            },
            {
              "date": "2026-01-09",
              "value": 238.90000000000003
            },
            {
              "date": "2026-01-12",
              "value": 238.90000000000003
            },
            {
              "date": "2026-01-13",
              "value": 236.59999999999997
            },
            {
              "date": "2026-01-14",
              "value": 232.39999999999998
            },
            {
              "date": "2026-01-15",
              "value": 237.0
            },
            {
              "date": "2026-01-16",
              "value": 238.49999999999997
            },
            {
              "date": "2026-01-20",
              "value": 238.0
            },
            {
              "date": "2026-01-21",
              "value": 236.50000000000003
            },
            {
              "date": "2026-01-22",
              "value": 238.60000000000002
            },
            {
              "date": "2026-01-23",
              "value": 233.8
            },
            {
              "date": "2026-01-26",
              "value": 228.30000000000004
            },
            {
              "date": "2026-01-27",
              "value": 224.59999999999997
            },
            {
              "date": "2026-01-28",
              "value": 230.29999999999998
            },
            {
              "date": "2026-01-29",
              "value": 226.6
            },
            {
              "date": "2026-01-30",
              "value": 226.9
            },
            {
              "date": "2026-02-02",
              "value": 230.49999999999997
            },
            {
              "date": "2026-02-03",
              "value": 228.39999999999998
            },
            {
              "date": "2026-02-04",
              "value": 229.39999999999995
            },
            {
              "date": "2026-02-05",
              "value": 219.4
            },
            {
              "date": "2026-02-06",
              "value": 221.90000000000003
            },
            {
              "date": "2026-02-09",
              "value": 216.7
            },
            {
              "date": "2026-02-10",
              "value": 214.70000000000002
            },
            {
              "date": "2026-02-11",
              "value": 221.70000000000002
            },
            {
              "date": "2026-02-12",
              "value": 216.5
            },
            {
              "date": "2026-02-13",
              "value": 211.09999999999997
            },
            {
              "date": "2026-02-17",
              "value": 219.70000000000002
            },
            {
              "date": "2026-02-18",
              "value": 222.8
            },
            {
              "date": "2026-02-19",
              "value": 220.5
            },
            {
              "date": "2026-02-20",
              "value": 221.99999999999997
            },
            {
              "date": "2026-02-23",
              "value": 217.0
            },
            {
              "date": "2026-02-24",
              "value": 217.90000000000003
            },
            {
              "date": "2026-02-25",
              "value": 222.6
            },
            {
              "date": "2026-02-26",
              "value": 217.4
            },
            {
              "date": "2026-02-27",
              "value": 213.0
            },
            {
              "date": "2026-03-02",
              "value": 225.10000000000002
            },
            {
              "date": "2026-03-03",
              "value": 225.99999999999997
            },
            {
              "date": "2026-03-04",
              "value": 230.49999999999997
            },
            {
              "date": "2026-03-05",
              "value": 231.4
            },
            {
              "date": "2026-03-06",
              "value": 231.4
            },
            {
              "date": "2026-03-09",
              "value": 231.8
            },
            {
              "date": "2026-03-10",
              "value": 231.2
            },
            {
              "date": "2026-03-11",
              "value": 238.70000000000005
            },
            {
              "date": "2026-03-12",
              "value": 249.7
            },
            {
              "date": "2026-03-13",
              "value": 244.1
            },
            {
              "date": "2026-03-16",
              "value": 239.3
            },
            {
              "date": "2026-03-17",
              "value": 240.00000000000003
            },
            {
              "date": "2026-03-18",
              "value": 249.89999999999998
            },
            {
              "date": "2026-03-19",
              "value": 251.29999999999998
            },
            {
              "date": "2026-03-20",
              "value": 260.29999999999995
            },
            {
              "date": "2026-03-23",
              "value": 251.9
            },
            {
              "date": "2026-03-24",
              "value": 258.9
            },
            {
              "date": "2026-03-25",
              "value": 252.29999999999995
            },
            {
              "date": "2026-03-26",
              "value": 261.2
            },
            {
              "date": "2026-03-27",
              "value": 248.70000000000002
            },
            {
              "date": "2026-03-30",
              "value": 245.09999999999997
            },
            {
              "date": "2026-03-31",
              "value": 241.5
            },
            {
              "date": "2026-04-01",
              "value": 246.10000000000002
            },
            {
              "date": "2026-04-02",
              "value": 240.00000000000003
            },
            {
              "date": "2026-04-03",
              "value": 244.89999999999998
            },
            {
              "date": "2026-04-06",
              "value": 243.79999999999998
            },
            {
              "date": "2026-04-07",
              "value": 242.3
            },
            {
              "date": "2026-04-08",
              "value": 240.80000000000004
            },
            {
              "date": "2026-04-09",
              "value": 238.60000000000002
            },
            {
              "date": "2026-04-10",
              "value": 240.50000000000003
            },
            {
              "date": "2026-04-13",
              "value": 237.89999999999995
            },
            {
              "date": "2026-04-14",
              "value": 237.8
            },
            {
              "date": "2026-04-15",
              "value": 237.8
            },
            {
              "date": "2026-04-16",
              "value": 241.39999999999998
            },
            {
              "date": "2026-04-17",
              "value": 233.8
            },
            {
              "date": "2026-04-20",
              "value": 235.1
            },
            {
              "date": "2026-04-21",
              "value": 242.1
            },
            {
              "date": "2026-04-22",
              "value": 242.79999999999998
            },
            {
              "date": "2026-04-23",
              "value": 246.5
            },
            {
              "date": "2026-04-24",
              "value": 241.7
            },
            {
              "date": "2026-04-27",
              "value": 240.49999999999997
            },
            {
              "date": "2026-04-28",
              "value": 245.09999999999997
            },
            {
              "date": "2026-04-29",
              "value": 253.09999999999997
            },
            {
              "date": "2026-04-30",
              "value": 247.79999999999998
            },
            {
              "date": "2026-05-01",
              "value": 249.5
            },
            {
              "date": "2026-05-04",
              "value": 256.50000000000006
            },
            {
              "date": "2026-05-05",
              "value": 254.5
            },
            {
              "date": "2026-05-06",
              "value": 248.50000000000003
            },
            {
              "date": "2026-05-07",
              "value": 254.8
            },
            {
              "date": "2026-05-08",
              "value": 252.20000000000002
            },
            {
              "date": "2026-05-11",
              "value": 255.50000000000003
            },
            {
              "date": "2026-05-12",
              "value": 259.90000000000003
            },
            {
              "date": "2026-05-13",
              "value": 257.9
            },
            {
              "date": "2026-05-14",
              "value": 259.3
            },
            {
              "date": "2026-05-15",
              "value": 267.69999999999993
            },
            {
              "date": "2026-05-18",
              "value": 263.90000000000003
            },
            {
              "date": "2026-05-19",
              "value": 267.8
            },
            {
              "date": "2026-05-20",
              "value": 257.6
            },
            {
              "date": "2026-05-21",
              "value": 262.7
            },
            {
              "date": "2026-05-22",
              "value": 268.7
            },
            {
              "date": "2026-05-26",
              "value": 258.9
            },
            {
              "date": "2026-05-27",
              "value": 260.1
            },
            {
              "date": "2026-05-28",
              "value": 262.40000000000003
            },
            {
              "date": "2026-05-29",
              "value": 258.7
            },
            {
              "date": "2026-06-01",
              "value": 265.0
            },
            {
              "date": "2026-06-02",
              "value": 267.0
            },
            {
              "date": "2026-06-03",
              "value": 267.90000000000003
            },
            {
              "date": "2026-06-04",
              "value": 263.3
            },
            {
              "date": "2026-06-05",
              "value": 275.8
            },
            {
              "date": "2026-06-08",
              "value": 273.00000000000006
            },
            {
              "date": "2026-06-09",
              "value": 271.0
            },
            {
              "date": "2026-06-10",
              "value": 270.4
            },
            {
              "date": "2026-06-11",
              "value": 262.29999999999995
            },
            {
              "date": "2026-06-12",
              "value": 267.3
            },
            {
              "date": "2026-06-15",
              "value": 266.1
            },
            {
              "date": "2026-06-16",
              "value": 263.6
            },
            {
              "date": "2026-06-17",
              "value": 280.20000000000005
            },
            {
              "date": "2026-06-18",
              "value": 279.00000000000006
            },
            {
              "date": "2026-06-22",
              "value": 282.5
            },
            {
              "date": "2026-06-23",
              "value": 273.4
            },
            {
              "date": "2026-06-24",
              "value": 267.8
            },
            {
              "date": "2026-06-25",
              "value": 266.9
            },
            {
              "date": "2026-06-26",
              "value": 266.1
            },
            {
              "date": "2026-06-29",
              "value": 268.9
            },
            {
              "date": "2026-06-30",
              "value": 275.8
            },
            {
              "date": "2026-07-01",
              "value": 278.8
            },
            {
              "date": "2026-07-02",
              "value": 275.8
            },
            {
              "date": "2026-07-06",
              "value": 274.8
            },
            {
              "date": "2026-07-07",
              "value": 280.80000000000007
            }
          ]
        },
        {
          "id": "US_JP_10Y",
          "label": "10Y UST-JGB",
          "points": [
            {
              "date": "2025-06-23",
              "value": 290.29999999999995
            },
            {
              "date": "2025-06-24",
              "value": 285.49999999999994
            },
            {
              "date": "2025-06-25",
              "value": 286.4
            },
            {
              "date": "2025-06-26",
              "value": 281.49999999999994
            },
            {
              "date": "2025-06-27",
              "value": 283.1
            },
            {
              "date": "2025-06-30",
              "value": 277.80000000000007
            },
            {
              "date": "2025-07-01",
              "value": 284.09999999999997
            },
            {
              "date": "2025-07-02",
              "value": 286.59999999999997
            },
            {
              "date": "2025-07-03",
              "value": 290.2
            },
            {
              "date": "2025-07-07",
              "value": 293.70000000000005
            },
            {
              "date": "2025-07-08",
              "value": 292.8
            },
            {
              "date": "2025-07-09",
              "value": 283.3
            },
            {
              "date": "2025-07-10",
              "value": 285.19999999999993
            },
            {
              "date": "2025-07-11",
              "value": 292.3
            },
            {
              "date": "2025-07-14",
              "value": 285.59999999999997
            },
            {
              "date": "2025-07-15",
              "value": 291.2
            },
            {
              "date": "2025-07-16",
              "value": 288.5
            },
            {
              "date": "2025-07-17",
              "value": 290.9
            },
            {
              "date": "2025-07-18",
              "value": 291.20000000000005
            },
            {
              "date": "2025-07-21",
              "value": 285.2
            },
            {
              "date": "2025-07-22",
              "value": 284.0
            },
            {
              "date": "2025-07-23",
              "value": 280.40000000000003
            },
            {
              "date": "2025-07-24",
              "value": 282.5
            },
            {
              "date": "2025-07-25",
              "value": 279.50000000000006
            },
            {
              "date": "2025-07-28",
              "value": 284.90000000000003
            },
            {
              "date": "2025-07-29",
              "value": 277.59999999999997
            },
            {
              "date": "2025-07-30",
              "value": 281.5
            },
            {
              "date": "2025-07-31",
              "value": 281.1
            },
            {
              "date": "2025-08-01",
              "value": 267.00000000000006
            },
            {
              "date": "2025-08-04",
              "value": 270.0
            },
            {
              "date": "2025-08-05",
              "value": 273.29999999999995
            },
            {
              "date": "2025-08-06",
              "value": 271.09999999999997
            },
            {
              "date": "2025-08-07",
              "value": 273.00000000000006
            },
            {
              "date": "2025-08-08",
              "value": 276.79999999999995
            },
            {
              "date": "2025-08-11",
              "value": 276.79999999999995
            },
            {
              "date": "2025-08-12",
              "value": 277.4
            },
            {
              "date": "2025-08-13",
              "value": 271.0
            },
            {
              "date": "2025-08-14",
              "value": 272.70000000000005
            },
            {
              "date": "2025-08-15",
              "value": 275.6
            },
            {
              "date": "2025-08-18",
              "value": 275.59999999999997
            },
            {
              "date": "2025-08-19",
              "value": 269.7
            },
            {
              "date": "2025-08-20",
              "value": 267.3
            },
            {
              "date": "2025-08-21",
              "value": 271.3
            },
            {
              "date": "2025-08-22",
              "value": 263.4
            },
            {
              "date": "2025-08-25",
              "value": 265.2
            },
            {
              "date": "2025-08-26",
              "value": 262.9
            },
            {
              "date": "2025-08-27",
              "value": 260.3
            },
            {
              "date": "2025-08-28",
              "value": 259.2
            },
            {
              "date": "2025-08-29",
              "value": 261.70000000000005
            },
            {
              "date": "2025-09-02",
              "value": 266.5
            },
            {
              "date": "2025-09-03",
              "value": 257.7
            },
            {
              "date": "2025-09-04",
              "value": 255.29999999999998
            },
            {
              "date": "2025-09-05",
              "value": 250.99999999999997
            },
            {
              "date": "2025-09-08",
              "value": 246.39999999999995
            },
            {
              "date": "2025-09-09",
              "value": 250.0
            },
            {
              "date": "2025-09-10",
              "value": 245.5
            },
            {
              "date": "2025-09-11",
              "value": 241.59999999999994
            },
            {
              "date": "2025-09-12",
              "value": 244.69999999999996
            },
            {
              "date": "2025-09-15",
              "value": 243.7
            },
            {
              "date": "2025-09-16",
              "value": 241.7
            },
            {
              "date": "2025-09-17",
              "value": 244.89999999999998
            },
            {
              "date": "2025-09-18",
              "value": 249.5
            },
            {
              "date": "2025-09-19",
              "value": 248.49999999999994
            },
            {
              "date": "2025-09-22",
              "value": 248.10000000000002
            },
            {
              "date": "2025-09-23",
              "value": 245.1
            },
            {
              "date": "2025-09-24",
              "value": 250.5
            },
            {
              "date": "2025-09-25",
              "value": 252.1
            },
            {
              "date": "2025-09-26",
              "value": 253.10000000000002
            },
            {
              "date": "2025-09-29",
              "value": 249.30000000000004
            },
            {
              "date": "2025-09-30",
              "value": 249.8
            },
            {
              "date": "2025-10-01",
              "value": 245.7
            },
            {
              "date": "2025-10-02",
              "value": 242.49999999999997
            },
            {
              "date": "2025-10-03",
              "value": 246.3
            },
            {
              "date": "2025-10-06",
              "value": 250.29999999999995
            },
            {
              "date": "2025-10-07",
              "value": 245.79999999999998
            },
            {
              "date": "2025-10-08",
              "value": 242.89999999999998
            },
            {
              "date": "2025-10-09",
              "value": 244.29999999999995
            },
            {
              "date": "2025-10-10",
              "value": 235.29999999999998
            },
            {
              "date": "2025-10-14",
              "value": 236.00000000000003
            },
            {
              "date": "2025-10-15",
              "value": 238.79999999999998
            },
            {
              "date": "2025-10-16",
              "value": 232.7
            },
            {
              "date": "2025-10-17",
              "value": 238.19999999999996
            },
            {
              "date": "2025-10-20",
              "value": 232.39999999999998
            },
            {
              "date": "2025-10-21",
              "value": 231.29999999999998
            },
            {
              "date": "2025-10-22",
              "value": 230.70000000000005
            },
            {
              "date": "2025-10-23",
              "value": 234.3
            },
            {
              "date": "2025-10-24",
              "value": 235.29999999999998
            },
            {
              "date": "2025-10-27",
              "value": 232.7
            },
            {
              "date": "2025-10-28",
              "value": 233.60000000000002
            },
            {
              "date": "2025-10-29",
              "value": 241.60000000000002
            },
            {
              "date": "2025-10-30",
              "value": 245.00000000000003
            },
            {
              "date": "2025-10-31",
              "value": 244.00000000000003
            },
            {
              "date": "2025-11-03",
              "value": 246.0
            },
            {
              "date": "2025-11-04",
              "value": 241.59999999999994
            },
            {
              "date": "2025-11-05",
              "value": 249.39999999999998
            },
            {
              "date": "2025-11-06",
              "value": 241.60000000000002
            },
            {
              "date": "2025-11-07",
              "value": 242.20000000000005
            },
            {
              "date": "2025-11-10",
              "value": 241.8
            },
            {
              "date": "2025-11-12",
              "value": 238.0
            },
            {
              "date": "2025-11-13",
              "value": 240.50000000000003
            },
            {
              "date": "2025-11-14",
              "value": 242.59999999999997
            },
            {
              "date": "2025-11-17",
              "value": 238.49999999999997
            },
            {
              "date": "2025-11-18",
              "value": 236.10000000000002
            },
            {
              "date": "2025-11-19",
              "value": 235.1
            },
            {
              "date": "2025-11-20",
              "value": 227.59999999999997
            },
            {
              "date": "2025-11-21",
              "value": 226.79999999999998
            },
            {
              "date": "2025-11-24",
              "value": 224.8
            },
            {
              "date": "2025-11-25",
              "value": 219.89999999999998
            },
            {
              "date": "2025-11-26",
              "value": 217.49999999999997
            },
            {
              "date": "2025-11-28",
              "value": 220.79999999999993
            },
            {
              "date": "2025-12-01",
              "value": 220.89999999999998
            },
            {
              "date": "2025-12-02",
              "value": 222.6
            },
            {
              "date": "2025-12-03",
              "value": 216.29999999999993
            },
            {
              "date": "2025-12-04",
              "value": 217.10000000000002
            },
            {
              "date": "2025-12-05",
              "value": 218.89999999999995
            },
            {
              "date": "2025-12-08",
              "value": 220.39999999999998
            },
            {
              "date": "2025-12-09",
              "value": 221.8
            },
            {
              "date": "2025-12-10",
              "value": 217.19999999999996
            },
            {
              "date": "2025-12-11",
              "value": 220.7
            },
            {
              "date": "2025-12-12",
              "value": 223.40000000000003
            },
            {
              "date": "2025-12-15",
              "value": 221.89999999999995
            },
            {
              "date": "2025-12-16",
              "value": 219.30000000000004
            },
            {
              "date": "2025-12-17",
              "value": 218.00000000000003
            },
            {
              "date": "2025-12-18",
              "value": 214.8
            },
            {
              "date": "2025-12-19",
              "value": 213.90000000000003
            },
            {
              "date": "2025-12-22",
              "value": 209.7
            },
            {
              "date": "2025-12-23",
              "value": 214.09999999999997
            },
            {
              "date": "2025-12-24",
              "value": 210.60000000000002
            },
            {
              "date": "2025-12-26",
              "value": 210.09999999999997
            },
            {
              "date": "2025-12-29",
              "value": 206.8
            },
            {
              "date": "2025-12-30",
              "value": 207.39999999999998
            },
            {
              "date": "2025-12-31",
              "value": 211.39999999999998
            },
            {
              "date": "2026-01-02",
              "value": 212.40000000000006
            },
            {
              "date": "2026-01-05",
              "value": 205.89999999999998
            },
            {
              "date": "2026-01-06",
              "value": 205.69999999999996
            },
            {
              "date": "2026-01-07",
              "value": 202.60000000000002
            },
            {
              "date": "2026-01-08",
              "value": 210.70000000000002
            },
            {
              "date": "2026-01-09",
              "value": 208.39999999999998
            },
            {
              "date": "2026-01-12",
              "value": 209.40000000000003
            },
            {
              "date": "2026-01-13",
              "value": 201.7
            },
            {
              "date": "2026-01-14",
              "value": 196.80000000000004
            },
            {
              "date": "2026-01-15",
              "value": 200.59999999999997
            },
            {
              "date": "2026-01-16",
              "value": 205.80000000000004
            },
            {
              "date": "2026-01-20",
              "value": 196.99999999999997
            },
            {
              "date": "2026-01-21",
              "value": 198.0
            },
            {
              "date": "2026-01-22",
              "value": 202.1
            },
            {
              "date": "2026-01-23",
              "value": 198.70000000000002
            },
            {
              "date": "2026-01-26",
              "value": 198.39999999999995
            },
            {
              "date": "2026-01-27",
              "value": 195.9
            },
            {
              "date": "2026-01-28",
              "value": 202.29999999999995
            },
            {
              "date": "2026-01-29",
              "value": 198.80000000000004
            },
            {
              "date": "2026-01-30",
              "value": 201.29999999999998
            },
            {
              "date": "2026-02-02",
              "value": 205.50000000000003
            },
            {
              "date": "2026-02-03",
              "value": 202.20000000000002
            },
            {
              "date": "2026-02-04",
              "value": 204.1
            },
            {
              "date": "2026-02-05",
              "value": 197.9
            },
            {
              "date": "2026-02-06",
              "value": 198.39999999999995
            },
            {
              "date": "2026-02-09",
              "value": 193.09999999999997
            },
            {
              "date": "2026-02-10",
              "value": 191.9
            },
            {
              "date": "2026-02-11",
              "value": 193.89999999999995
            },
            {
              "date": "2026-02-12",
              "value": 185.2
            },
            {
              "date": "2026-02-13",
              "value": 182.20000000000002
            },
            {
              "date": "2026-02-17",
              "value": 190.7
            },
            {
              "date": "2026-02-18",
              "value": 193.79999999999998
            },
            {
              "date": "2026-02-19",
              "value": 192.3
            },
            {
              "date": "2026-02-20",
              "value": 195.5
            },
            {
              "date": "2026-02-23",
              "value": 190.50000000000003
            },
            {
              "date": "2026-02-24",
              "value": 192.1
            },
            {
              "date": "2026-02-25",
              "value": 189.6
            },
            {
              "date": "2026-02-26",
              "value": 185.19999999999993
            },
            {
              "date": "2026-02-27",
              "value": 183.8
            },
            {
              "date": "2026-03-02",
              "value": 196.29999999999995
            },
            {
              "date": "2026-03-03",
              "value": 191.19999999999996
            },
            {
              "date": "2026-03-04",
              "value": 195.6
            },
            {
              "date": "2026-03-05",
              "value": 195.5
            },
            {
              "date": "2026-03-06",
              "value": 197.00000000000003
            },
            {
              "date": "2026-03-09",
              "value": 191.5
            },
            {
              "date": "2026-03-10",
              "value": 195.10000000000005
            },
            {
              "date": "2026-03-11",
              "value": 203.2
            },
            {
              "date": "2026-03-12",
              "value": 206.89999999999995
            },
            {
              "date": "2026-03-13",
              "value": 202.50000000000003
            },
            {
              "date": "2026-03-16",
              "value": 194.20000000000007
            },
            {
              "date": "2026-03-17",
              "value": 192.10000000000002
            },
            {
              "date": "2026-03-18",
              "value": 202.89999999999998
            },
            {
              "date": "2026-03-19",
              "value": 197.7
            },
            {
              "date": "2026-03-20",
              "value": 211.69999999999996
            },
            {
              "date": "2026-03-23",
              "value": 201.79999999999998
            },
            {
              "date": "2026-03-24",
              "value": 210.79999999999995
            },
            {
              "date": "2026-03-25",
              "value": 206.3
            },
            {
              "date": "2026-03-26",
              "value": 213.39999999999998
            },
            {
              "date": "2026-03-27",
              "value": 206.00000000000006
            },
            {
              "date": "2026-03-30",
              "value": 198.2
            },
            {
              "date": "2026-03-31",
              "value": 193.39999999999998
            },
            {
              "date": "2026-04-01",
              "value": 201.5
            },
            {
              "date": "2026-04-02",
              "value": 191.49999999999997
            },
            {
              "date": "2026-04-03",
              "value": 196.39999999999995
            },
            {
              "date": "2026-04-06",
              "value": 191.1
            },
            {
              "date": "2026-04-07",
              "value": 191.9
            },
            {
              "date": "2026-04-08",
              "value": 191.6
            },
            {
              "date": "2026-04-09",
              "value": 189.3
            },
            {
              "date": "2026-04-10",
              "value": 187.09999999999997
            },
            {
              "date": "2026-04-13",
              "value": 183.29999999999998
            },
            {
              "date": "2026-04-14",
              "value": 183.7
            },
            {
              "date": "2026-04-15",
              "value": 187.6
            },
            {
              "date": "2026-04-16",
              "value": 191.10000000000005
            },
            {
              "date": "2026-04-17",
              "value": 183.2
            },
            {
              "date": "2026-04-20",
              "value": 185.5
            },
            {
              "date": "2026-04-21",
              "value": 190.79999999999998
            },
            {
              "date": "2026-04-22",
              "value": 189.39999999999998
            },
            {
              "date": "2026-04-23",
              "value": 191.1
            },
            {
              "date": "2026-04-24",
              "value": 186.69999999999996
            },
            {
              "date": "2026-04-27",
              "value": 187.29999999999998
            },
            {
              "date": "2026-04-28",
              "value": 189.20000000000005
            },
            {
              "date": "2026-04-29",
              "value": 195.2
            },
            {
              "date": "2026-04-30",
              "value": 188.00000000000003
            },
            {
              "date": "2026-05-01",
              "value": 188.29999999999995
            },
            {
              "date": "2026-05-04",
              "value": 194.3
            },
            {
              "date": "2026-05-05",
              "value": 192.29999999999995
            },
            {
              "date": "2026-05-06",
              "value": 185.3
            },
            {
              "date": "2026-05-07",
              "value": 192.50000000000003
            },
            {
              "date": "2026-05-08",
              "value": 189.5
            },
            {
              "date": "2026-05-11",
              "value": 189.29999999999998
            },
            {
              "date": "2026-05-12",
              "value": 191.4
            },
            {
              "date": "2026-05-13",
              "value": 187.29999999999998
            },
            {
              "date": "2026-05-14",
              "value": 184.19999999999996
            },
            {
              "date": "2026-05-15",
              "value": 189.9
            },
            {
              "date": "2026-05-18",
              "value": 188.10000000000002
            },
            {
              "date": "2026-05-19",
              "value": 188.7
            },
            {
              "date": "2026-05-20",
              "value": 180.00000000000003
            },
            {
              "date": "2026-05-21",
              "value": 182.20000000000002
            },
            {
              "date": "2026-05-22",
              "value": 181.09999999999994
            },
            {
              "date": "2026-05-26",
              "value": 178.7
            },
            {
              "date": "2026-05-27",
              "value": 179.30000000000007
            },
            {
              "date": "2026-05-28",
              "value": 175.8
            },
            {
              "date": "2026-05-29",
              "value": 179.3
            },
            {
              "date": "2026-06-01",
              "value": 178.79999999999998
            },
            {
              "date": "2026-06-02",
              "value": 188.3
            },
            {
              "date": "2026-06-03",
              "value": 184.50000000000003
            },
            {
              "date": "2026-06-04",
              "value": 179.9
            },
            {
              "date": "2026-06-05",
              "value": 188.09999999999997
            },
            {
              "date": "2026-06-08",
              "value": 184.49999999999997
            },
            {
              "date": "2026-06-09",
              "value": 186.10000000000002
            },
            {
              "date": "2026-06-10",
              "value": 186.89999999999998
            },
            {
              "date": "2026-06-11",
              "value": 176.8
            },
            {
              "date": "2026-06-12",
              "value": 183.70000000000007
            },
            {
              "date": "2026-06-15",
              "value": 188.09999999999997
            },
            {
              "date": "2026-06-16",
              "value": 177.5
            },
            {
              "date": "2026-06-17",
              "value": 187.70000000000002
            },
            {
              "date": "2026-06-18",
              "value": 183.2
            },
            {
              "date": "2026-06-22",
              "value": 183.29999999999998
            },
            {
              "date": "2026-06-23",
              "value": 181.70000000000002
            },
            {
              "date": "2026-06-24",
              "value": 173.60000000000002
            },
            {
              "date": "2026-06-25",
              "value": 176.30000000000004
            },
            {
              "date": "2026-06-26",
              "value": 176.89999999999998
            },
            {
              "date": "2026-06-29",
              "value": 173.59999999999997
            },
            {
              "date": "2026-06-30",
              "value": 175.00000000000006
            },
            {
              "date": "2026-07-01",
              "value": 179.00000000000006
            },
            {
              "date": "2026-07-02",
              "value": 180.00000000000003
            },
            {
              "date": "2026-07-06",
              "value": 179.00000000000006
            },
            {
              "date": "2026-07-07",
              "value": 186.0
            }
          ]
        }
      ]
    },
    {
      "id": "jpy_cftc_gross_2y",
      "title": "CFTC JPY：空头 vs 多头（非商业，验证空头是否真加仓）",
      "chart_type": "line",
      "unit": "contracts",
      "data_source": "SQLite jpy_carry_series_ts",
      "series": [
        {
          "id": "CFTC_JPY_GROSS_SHORT",
          "label": "非商业空头",
          "points": [
            {
              "date": "2024-07-09",
              "value": 223554.0
            },
            {
              "date": "2024-07-16",
              "value": 198428.0
            },
            {
              "date": "2024-07-23",
              "value": 171498.0
            },
            {
              "date": "2024-07-30",
              "value": 138476.0
            },
            {
              "date": "2024-08-06",
              "value": 77523.0
            },
            {
              "date": "2024-08-13",
              "value": 63997.0
            },
            {
              "date": "2024-08-20",
              "value": 65176.0
            },
            {
              "date": "2024-08-27",
              "value": 58437.0
            },
            {
              "date": "2024-09-03",
              "value": 50675.0
            },
            {
              "date": "2024-09-10",
              "value": 43124.0
            },
            {
              "date": "2024-09-17",
              "value": 40492.0
            },
            {
              "date": "2024-09-24",
              "value": 38679.0
            },
            {
              "date": "2024-10-01",
              "value": 38741.0
            },
            {
              "date": "2024-10-08",
              "value": 47151.0
            },
            {
              "date": "2024-10-15",
              "value": 52575.0
            },
            {
              "date": "2024-10-22",
              "value": 66593.0
            },
            {
              "date": "2024-10-29",
              "value": 89742.0
            },
            {
              "date": "2024-11-05",
              "value": 104501.0
            },
            {
              "date": "2024-11-12",
              "value": 128940.0
            },
            {
              "date": "2024-11-19",
              "value": 125841.0
            },
            {
              "date": "2024-11-26",
              "value": 110230.0
            },
            {
              "date": "2024-12-03",
              "value": 91288.0
            },
            {
              "date": "2024-12-10",
              "value": 72186.0
            },
            {
              "date": "2024-12-17",
              "value": 81247.0
            },
            {
              "date": "2024-12-24",
              "value": 93647.0
            },
            {
              "date": "2024-12-31",
              "value": 104562.0
            },
            {
              "date": "2025-01-07",
              "value": 111395.0
            },
            {
              "date": "2025-01-14",
              "value": 120845.0
            },
            {
              "date": "2025-01-21",
              "value": 108830.0
            },
            {
              "date": "2025-01-28",
              "value": 97768.0
            },
            {
              "date": "2025-02-04",
              "value": 85916.0
            },
            {
              "date": "2025-02-11",
              "value": 89543.0
            },
            {
              "date": "2025-02-18",
              "value": 86997.0
            },
            {
              "date": "2025-02-25",
              "value": 75771.0
            },
            {
              "date": "2025-03-04",
              "value": 50304.0
            },
            {
              "date": "2025-03-11",
              "value": 42888.0
            },
            {
              "date": "2025-03-18",
              "value": 41788.0
            },
            {
              "date": "2025-03-25",
              "value": 35098.0
            },
            {
              "date": "2025-04-01",
              "value": 39792.0
            },
            {
              "date": "2025-04-08",
              "value": 29488.0
            },
            {
              "date": "2025-04-15",
              "value": 26705.0
            },
            {
              "date": "2025-04-22",
              "value": 24559.0
            },
            {
              "date": "2025-04-29",
              "value": 23585.0
            },
            {
              "date": "2025-05-06",
              "value": 27149.0
            },
            {
              "date": "2025-05-13",
              "value": 21958.0
            },
            {
              "date": "2025-05-20",
              "value": 27180.0
            },
            {
              "date": "2025-05-27",
              "value": 27790.0
            },
            {
              "date": "2025-06-03",
              "value": 38365.0
            },
            {
              "date": "2025-06-10",
              "value": 39600.0
            },
            {
              "date": "2025-06-17",
              "value": 44724.0
            },
            {
              "date": "2025-06-24",
              "value": 46126.0
            },
            {
              "date": "2025-07-01",
              "value": 43286.0
            },
            {
              "date": "2025-07-08",
              "value": 50037.0
            },
            {
              "date": "2025-07-15",
              "value": 61862.0
            },
            {
              "date": "2025-07-22",
              "value": 57766.0
            },
            {
              "date": "2025-07-29",
              "value": 72879.0
            },
            {
              "date": "2025-08-05",
              "value": 78252.0
            },
            {
              "date": "2025-08-12",
              "value": 90459.0
            },
            {
              "date": "2025-08-19",
              "value": 90782.0
            },
            {
              "date": "2025-08-26",
              "value": 86281.0
            },
            {
              "date": "2025-09-02",
              "value": 101516.0
            },
            {
              "date": "2025-09-09",
              "value": 89081.0
            },
            {
              "date": "2025-09-16",
              "value": 100262.0
            },
            {
              "date": "2025-09-23",
              "value": 96900.0
            },
            {
              "date": "2025-09-30",
              "value": 106346.0
            },
            {
              "date": "2025-10-07",
              "value": 112890.0
            },
            {
              "date": "2025-10-14",
              "value": 123473.0
            },
            {
              "date": "2025-10-21",
              "value": 105310.0
            },
            {
              "date": "2025-10-28",
              "value": 110630.0
            },
            {
              "date": "2025-11-04",
              "value": 118915.0
            },
            {
              "date": "2025-11-10",
              "value": 123873.0
            },
            {
              "date": "2025-11-18",
              "value": 138733.0
            },
            {
              "date": "2025-11-25",
              "value": 142701.0
            },
            {
              "date": "2025-12-02",
              "value": 148540.0
            },
            {
              "date": "2025-12-09",
              "value": 167040.0
            },
            {
              "date": "2025-12-16",
              "value": 149217.0
            },
            {
              "date": "2025-12-23",
              "value": 139910.0
            },
            {
              "date": "2025-12-30",
              "value": 130528.0
            },
            {
              "date": "2026-01-06",
              "value": 131626.0
            },
            {
              "date": "2026-01-13",
              "value": 156907.0
            },
            {
              "date": "2026-01-20",
              "value": 151968.0
            },
            {
              "date": "2026-01-27",
              "value": 138393.0
            },
            {
              "date": "2026-02-03",
              "value": 133650.0
            },
            {
              "date": "2026-02-10",
              "value": 147196.0
            },
            {
              "date": "2026-02-17",
              "value": 130217.0
            },
            {
              "date": "2026-02-24",
              "value": 137825.0
            },
            {
              "date": "2026-03-03",
              "value": 151520.0
            },
            {
              "date": "2026-03-10",
              "value": 160798.0
            },
            {
              "date": "2026-03-17",
              "value": 174599.0
            },
            {
              "date": "2026-03-24",
              "value": 161077.0
            },
            {
              "date": "2026-03-31",
              "value": 168228.0
            },
            {
              "date": "2026-04-07",
              "value": 185302.0
            },
            {
              "date": "2026-04-14",
              "value": 185322.0
            },
            {
              "date": "2026-04-21",
              "value": 195846.0
            },
            {
              "date": "2026-04-28",
              "value": 208589.0
            },
            {
              "date": "2026-05-05",
              "value": 170773.0
            },
            {
              "date": "2026-05-12",
              "value": 175257.0
            },
            {
              "date": "2026-05-19",
              "value": 200508.0
            },
            {
              "date": "2026-05-26",
              "value": 227660.0
            },
            {
              "date": "2026-06-02",
              "value": 244416.0
            },
            {
              "date": "2026-06-09",
              "value": 267338.0
            },
            {
              "date": "2026-06-16",
              "value": 267507.0
            },
            {
              "date": "2026-06-23",
              "value": 259802.0
            },
            {
              "date": "2026-06-30",
              "value": 266964.0
            }
          ]
        },
        {
          "id": "CFTC_JPY_GROSS_LONG",
          "label": "非商业多头",
          "points": [
            {
              "date": "2024-07-09",
              "value": 41521.0
            },
            {
              "date": "2024-07-16",
              "value": 47356.0
            },
            {
              "date": "2024-07-23",
              "value": 64390.0
            },
            {
              "date": "2024-07-30",
              "value": 65016.0
            },
            {
              "date": "2024-08-06",
              "value": 66169.0
            },
            {
              "date": "2024-08-13",
              "value": 87101.0
            },
            {
              "date": "2024-08-20",
              "value": 88761.0
            },
            {
              "date": "2024-08-27",
              "value": 84305.0
            },
            {
              "date": "2024-09-03",
              "value": 91791.0
            },
            {
              "date": "2024-09-10",
              "value": 98894.0
            },
            {
              "date": "2024-09-17",
              "value": 97332.0
            },
            {
              "date": "2024-09-24",
              "value": 104690.0
            },
            {
              "date": "2024-10-01",
              "value": 95513.0
            },
            {
              "date": "2024-10-08",
              "value": 83679.0
            },
            {
              "date": "2024-10-15",
              "value": 86685.0
            },
            {
              "date": "2024-10-22",
              "value": 79364.0
            },
            {
              "date": "2024-10-29",
              "value": 64925.0
            },
            {
              "date": "2024-11-05",
              "value": 60334.0
            },
            {
              "date": "2024-11-12",
              "value": 64038.0
            },
            {
              "date": "2024-11-19",
              "value": 78973.0
            },
            {
              "date": "2024-11-26",
              "value": 87597.0
            },
            {
              "date": "2024-12-03",
              "value": 93622.0
            },
            {
              "date": "2024-12-10",
              "value": 97938.0
            },
            {
              "date": "2024-12-17",
              "value": 87208.0
            },
            {
              "date": "2024-12-24",
              "value": 95958.0
            },
            {
              "date": "2024-12-31",
              "value": 96119.0
            },
            {
              "date": "2025-01-07",
              "value": 91206.0
            },
            {
              "date": "2025-01-14",
              "value": 91434.0
            },
            {
              "date": "2025-01-21",
              "value": 94157.0
            },
            {
              "date": "2025-01-28",
              "value": 96809.0
            },
            {
              "date": "2025-02-04",
              "value": 104684.0
            },
            {
              "date": "2025-02-11",
              "value": 144158.0
            },
            {
              "date": "2025-02-18",
              "value": 147566.0
            },
            {
              "date": "2025-02-25",
              "value": 171751.0
            },
            {
              "date": "2025-03-04",
              "value": 183955.0
            },
            {
              "date": "2025-03-11",
              "value": 176790.0
            },
            {
              "date": "2025-03-18",
              "value": 164752.0
            },
            {
              "date": "2025-03-25",
              "value": 160474.0
            },
            {
              "date": "2025-04-01",
              "value": 161566.0
            },
            {
              "date": "2025-04-08",
              "value": 176555.0
            },
            {
              "date": "2025-04-15",
              "value": 198560.0
            },
            {
              "date": "2025-04-22",
              "value": 202373.0
            },
            {
              "date": "2025-04-29",
              "value": 202797.0
            },
            {
              "date": "2025-05-06",
              "value": 204008.0
            },
            {
              "date": "2025-05-13",
              "value": 194226.0
            },
            {
              "date": "2025-05-20",
              "value": 194510.0
            },
            {
              "date": "2025-05-27",
              "value": 191802.0
            },
            {
              "date": "2025-06-03",
              "value": 189514.0
            },
            {
              "date": "2025-06-10",
              "value": 184195.0
            },
            {
              "date": "2025-06-17",
              "value": 175601.0
            },
            {
              "date": "2025-06-24",
              "value": 178403.0
            },
            {
              "date": "2025-07-01",
              "value": 170624.0
            },
            {
              "date": "2025-07-08",
              "value": 166192.0
            },
            {
              "date": "2025-07-15",
              "value": 165444.0
            },
            {
              "date": "2025-07-22",
              "value": 164411.0
            },
            {
              "date": "2025-07-29",
              "value": 162122.0
            },
            {
              "date": "2025-08-05",
              "value": 160258.0
            },
            {
              "date": "2025-08-12",
              "value": 164693.0
            },
            {
              "date": "2025-08-19",
              "value": 168363.0
            },
            {
              "date": "2025-08-26",
              "value": 170765.0
            },
            {
              "date": "2025-09-02",
              "value": 174774.0
            },
            {
              "date": "2025-09-09",
              "value": 180724.0
            },
            {
              "date": "2025-09-16",
              "value": 161673.0
            },
            {
              "date": "2025-09-23",
              "value": 176400.0
            },
            {
              "date": "2025-09-30",
              "value": 167811.0
            },
            {
              "date": "2025-10-07",
              "value": 159197.0
            },
            {
              "date": "2025-10-14",
              "value": 160639.0
            },
            {
              "date": "2025-10-21",
              "value": 175724.0
            },
            {
              "date": "2025-10-28",
              "value": 178745.0
            },
            {
              "date": "2025-11-04",
              "value": 170180.0
            },
            {
              "date": "2025-11-10",
              "value": 172349.0
            },
            {
              "date": "2025-11-18",
              "value": 169890.0
            },
            {
              "date": "2025-11-25",
              "value": 169218.0
            },
            {
              "date": "2025-12-02",
              "value": 184958.0
            },
            {
              "date": "2025-12-09",
              "value": 184488.0
            },
            {
              "date": "2025-12-16",
              "value": 146275.0
            },
            {
              "date": "2025-12-23",
              "value": 141133.0
            },
            {
              "date": "2025-12-30",
              "value": 144596.0
            },
            {
              "date": "2026-01-06",
              "value": 140441.0
            },
            {
              "date": "2026-01-13",
              "value": 111743.0
            },
            {
              "date": "2026-01-20",
              "value": 107139.0
            },
            {
              "date": "2026-01-27",
              "value": 104460.0
            },
            {
              "date": "2026-02-03",
              "value": 114428.0
            },
            {
              "date": "2026-02-10",
              "value": 128090.0
            },
            {
              "date": "2026-02-17",
              "value": 143172.0
            },
            {
              "date": "2026-02-24",
              "value": 149364.0
            },
            {
              "date": "2026-03-03",
              "value": 134945.0
            },
            {
              "date": "2026-03-10",
              "value": 119411.0
            },
            {
              "date": "2026-03-17",
              "value": 106819.0
            },
            {
              "date": "2026-03-24",
              "value": 98271.0
            },
            {
              "date": "2026-03-31",
              "value": 95356.0
            },
            {
              "date": "2026-04-07",
              "value": 91560.0
            },
            {
              "date": "2026-04-14",
              "value": 102114.0
            },
            {
              "date": "2026-04-21",
              "value": 101386.0
            },
            {
              "date": "2026-04-28",
              "value": 106530.0
            },
            {
              "date": "2026-05-05",
              "value": 109035.0
            },
            {
              "date": "2026-05-12",
              "value": 100155.0
            },
            {
              "date": "2026-05-19",
              "value": 106603.0
            },
            {
              "date": "2026-05-26",
              "value": 112993.0
            },
            {
              "date": "2026-06-02",
              "value": 114849.0
            },
            {
              "date": "2026-06-09",
              "value": 121520.0
            },
            {
              "date": "2026-06-16",
              "value": 117375.0
            },
            {
              "date": "2026-06-23",
              "value": 113698.0
            },
            {
              "date": "2026-06-30",
              "value": 111872.0
            }
          ]
        }
      ]
    },
    {
      "id": "jpy_cftc_short_share_2y",
      "title": "CFTC JPY空头占比（空头/(空头+多头)，空头一侧真实强度）",
      "chart_type": "line",
      "unit": "short/(short+long)",
      "data_source": "SQLite jpy_carry_series_ts",
      "series": [
        {
          "id": "CFTC_JPY_SHORT_SHARE",
          "label": "空头占比",
          "points": [
            {
              "date": "2024-07-09",
              "value": 0.8433613128359898
            },
            {
              "date": "2024-07-16",
              "value": 0.807326758454578
            },
            {
              "date": "2024-07-23",
              "value": 0.7270314725632504
            },
            {
              "date": "2024-07-30",
              "value": 0.6804984962553811
            },
            {
              "date": "2024-08-06",
              "value": 0.5395081145784039
            },
            {
              "date": "2024-08-13",
              "value": 0.4235463076943441
            },
            {
              "date": "2024-08-20",
              "value": 0.4233939858513548
            },
            {
              "date": "2024-08-27",
              "value": 0.4093889675078113
            },
            {
              "date": "2024-09-03",
              "value": 0.35569890359805145
            },
            {
              "date": "2024-09-10",
              "value": 0.30365164979087156
            },
            {
              "date": "2024-09-17",
              "value": 0.2937949849082888
            },
            {
              "date": "2024-09-24",
              "value": 0.2697863554882855
            },
            {
              "date": "2024-10-01",
              "value": 0.2885649589583923
            },
            {
              "date": "2024-10-08",
              "value": 0.360398991057097
            },
            {
              "date": "2024-10-15",
              "value": 0.37753123653597587
            },
            {
              "date": "2024-10-22",
              "value": 0.45625081359578507
            },
            {
              "date": "2024-10-29",
              "value": 0.5802271977862117
            },
            {
              "date": "2024-11-05",
              "value": 0.6339733673067006
            },
            {
              "date": "2024-11-12",
              "value": 0.6681590647638591
            },
            {
              "date": "2024-11-19",
              "value": 0.6144160067182908
            },
            {
              "date": "2024-11-26",
              "value": 0.557204021695724
            },
            {
              "date": "2024-12-03",
              "value": 0.49368882158888105
            },
            {
              "date": "2024-12-10",
              "value": 0.4243140297665232
            },
            {
              "date": "2024-12-17",
              "value": 0.4823068475260455
            },
            {
              "date": "2024-12-24",
              "value": 0.4939057514306057
            },
            {
              "date": "2024-12-31",
              "value": 0.5210358728529357
            },
            {
              "date": "2025-01-07",
              "value": 0.5498245319618363
            },
            {
              "date": "2025-01-14",
              "value": 0.5692743983154245
            },
            {
              "date": "2025-01-21",
              "value": 0.5361427086463665
            },
            {
              "date": "2025-01-28",
              "value": 0.5024643200378256
            },
            {
              "date": "2025-02-04",
              "value": 0.4507660020986359
            },
            {
              "date": "2025-02-11",
              "value": 0.3831519762431483
            },
            {
              "date": "2025-02-18",
              "value": 0.3708896970110375
            },
            {
              "date": "2025-02-25",
              "value": 0.30611824403487364
            },
            {
              "date": "2025-03-04",
              "value": 0.2147366803409901
            },
            {
              "date": "2025-03-11",
              "value": 0.19523120203206512
            },
            {
              "date": "2025-03-18",
              "value": 0.20232400503534426
            },
            {
              "date": "2025-03-25",
              "value": 0.179463317857362
            },
            {
              "date": "2025-04-01",
              "value": 0.19761817260799175
            },
            {
              "date": "2025-04-08",
              "value": 0.14311575739044763
            },
            {
              "date": "2025-04-15",
              "value": 0.11854926419994229
            },
            {
              "date": "2025-04-22",
              "value": 0.10822184619181076
            },
            {
              "date": "2025-04-29",
              "value": 0.1041823113145038
            },
            {
              "date": "2025-05-06",
              "value": 0.11744831434912202
            },
            {
              "date": "2025-05-13",
              "value": 0.1015708840617252
            },
            {
              "date": "2025-05-20",
              "value": 0.1226036357075195
            },
            {
              "date": "2025-05-27",
              "value": 0.12655287988633465
            },
            {
              "date": "2025-06-03",
              "value": 0.1683568911571492
            },
            {
              "date": "2025-06-10",
              "value": 0.17694765298599163
            },
            {
              "date": "2025-06-17",
              "value": 0.20299103596959037
            },
            {
              "date": "2025-06-24",
              "value": 0.20543448730453528
            },
            {
              "date": "2025-07-01",
              "value": 0.20235613108316583
            },
            {
              "date": "2025-07-08",
              "value": 0.23140744303493055
            },
            {
              "date": "2025-07-15",
              "value": 0.2721529568071234
            },
            {
              "date": "2025-07-22",
              "value": 0.25999990998168127
            },
            {
              "date": "2025-07-29",
              "value": 0.3101220845868741
            },
            {
              "date": "2025-08-05",
              "value": 0.32808687266781267
            },
            {
              "date": "2025-08-12",
              "value": 0.3545298488743964
            },
            {
              "date": "2025-08-19",
              "value": 0.3503135310347489
            },
            {
              "date": "2025-08-26",
              "value": 0.3356636555324728
            },
            {
              "date": "2025-09-02",
              "value": 0.36742553114481163
            },
            {
              "date": "2025-09-09",
              "value": 0.33016808435722095
            },
            {
              "date": "2025-09-16",
              "value": 0.38277435241567564
            },
            {
              "date": "2025-09-23",
              "value": 0.3545554335894621
            },
            {
              "date": "2025-09-30",
              "value": 0.3879018226782464
            },
            {
              "date": "2025-10-07",
              "value": 0.4149040564231294
            },
            {
              "date": "2025-10-14",
              "value": 0.434592695838261
            },
            {
              "date": "2025-10-21",
              "value": 0.37472334308304334
            },
            {
              "date": "2025-10-28",
              "value": 0.38230669546436286
            },
            {
              "date": "2025-11-04",
              "value": 0.4113353741849565
            },
            {
              "date": "2025-11-10",
              "value": 0.4181762326903471
            },
            {
              "date": "2025-11-18",
              "value": 0.44952255664678265
            },
            {
              "date": "2025-11-25",
              "value": 0.4574937724216864
            },
            {
              "date": "2025-12-02",
              "value": 0.44539997241362767
            },
            {
              "date": "2025-12-09",
              "value": 0.4751826312555472
            },
            {
              "date": "2025-12-16",
              "value": 0.5049781381560245
            },
            {
              "date": "2025-12-23",
              "value": 0.49782417637158727
            },
            {
              "date": "2025-12-30",
              "value": 0.4744333464183423
            },
            {
              "date": "2026-01-06",
              "value": 0.48379994633674794
            },
            {
              "date": "2026-01-13",
              "value": 0.5840573236553136
            },
            {
              "date": "2026-01-20",
              "value": 0.5865067327397562
            },
            {
              "date": "2026-01-27",
              "value": 0.5698632506083927
            },
            {
              "date": "2026-02-03",
              "value": 0.5387418473222132
            },
            {
              "date": "2026-02-10",
              "value": 0.5347020916428732
            },
            {
              "date": "2026-02-17",
              "value": 0.4763066546203395
            },
            {
              "date": "2026-02-24",
              "value": 0.47991044225231466
            },
            {
              "date": "2026-03-03",
              "value": 0.5289302358054212
            },
            {
              "date": "2026-03-10",
              "value": 0.573850233218776
            },
            {
              "date": "2026-03-17",
              "value": 0.6204258434073158
            },
            {
              "date": "2026-03-24",
              "value": 0.6210844116785169
            },
            {
              "date": "2026-03-31",
              "value": 0.6382329731698434
            },
            {
              "date": "2026-04-07",
              "value": 0.6692937275610232
            },
            {
              "date": "2026-04-14",
              "value": 0.6447417859975786
            },
            {
              "date": "2026-04-21",
              "value": 0.6588994455509501
            },
            {
              "date": "2026-04-28",
              "value": 0.6619372364091026
            },
            {
              "date": "2026-05-05",
              "value": 0.6103220779963403
            },
            {
              "date": "2026-05-12",
              "value": 0.6363448215764019
            },
            {
              "date": "2026-05-19",
              "value": 0.6528844619697765
            },
            {
              "date": "2026-05-26",
              "value": 0.6683046971551696
            },
            {
              "date": "2026-06-02",
              "value": 0.6803223247463571
            },
            {
              "date": "2026-06-09",
              "value": 0.687495178188439
            },
            {
              "date": "2026-06-16",
              "value": 0.6950364007669884
            },
            {
              "date": "2026-06-23",
              "value": 0.6955876840696118
            },
            {
              "date": "2026-06-30",
              "value": 0.7046954354918751
            }
          ]
        }
      ]
    },
    {
      "id": "upcoming_tbill_supply_60d",
      "title": "未来已公告拍卖规模：T-bill / Total",
      "chart_type": "line",
      "unit": "USD bn",
      "series": [
        {
          "id": "UPCOMING_TBILL_SUPPLY",
          "label": "Upcoming T-bill Supply（未来短债发行规模）",
          "points": [
            {
              "date": "2026-07-09",
              "value": 195.0
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "UPCOMING_TOTAL_TREASURY_SUPPLY",
          "label": "Upcoming Total Treasury Supply（未来已公告美债发行总额）",
          "points": [
            {
              "date": "2026-07-09",
              "value": 217.0
            }
          ],
          "y_axis": "y"
        }
      ],
      "data_source": "dashboard_data.upcoming_auctions.bill_schedule / auctions",
      "note": "只包含TreasuryDirect已公告发行规模；未公告规模不当作零供给。"
    }
  ],
  "chart_paths": [
    "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/output/usd_liquidity_chart_7d_20260709_110141.svg",
    "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/output/usd_liquidity_chart_30d_20260709_110141.svg"
  ],
  "data_quality": {
    "missing": [
      {
        "id": "TGA",
        "label": "TGA（财政部一般账户）",
        "reason": "GET failed: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90 | HTTPSConnectionPool(host='api.fiscaldata.treasury.gov', port=443): Read timed out. (read timeout=10)",
        "fallback": "详见缺失数据与替代指标"
      }
    ],
    "stale": [
      {
        "id": "DCPN3M",
        "label": "CP Rate（90天AA非金融商业票据利率）",
        "stale_days": 13
      },
      {
        "id": "REPO_FAILS_UST",
        "label": "Repo Fails（美国国债回购交割失败）",
        "stale_days": 15
      },
      {
        "id": "DTWEXBGS",
        "label": "DTWEXBGS（广义美元指数）",
        "stale_days": 7
      }
    ],
    "degraded_sources": [
      {
        "name": "MOVE Index",
        "reason": "ICE/BofA proprietary index; no free official real-time API found",
        "proxy": "Use Treasury/repo rates, HY spread and auction signals as substitutes"
      },
      {
        "name": "FRA-OIS",
        "reason": "No free official daily API found; usually Bloomberg/Refinitiv",
        "proxy": "Use CP-Fed target proxy and SOFR/EFFR/IORB spreads"
      },
      {
        "name": "True cross-currency basis",
        "reason": "CME/market vendor access generally requires onboarding or paid data",
        "proxy": "Use Fed broad dollar index DTWEXBGS as an offshore USD stress proxy"
      },
      {
        "name": "Real-time Treasury order book depth",
        "reason": "BrokerTec/ICAP depth is proprietary; no free official API",
        "proxy": "Use auction bid-to-cover, repo fails and volatility/funding proxies"
      },
      {
        "name": "Goldman Sachs Financial Conditions Index",
        "reason": "Goldman Sachs FCI is proprietary; no free official public API found",
        "proxy": "Use Chicago Fed NFCI plus rates, credit spreads, dollar index and equity/credit proxies"
      }
    ]
  }
};
window.ANALYSIS_DATA = {
  "meta": {
    "status": "pending_model_analysis",
    "generated_at_bjt": "2026-07-09 11:01:59 UTC+08:00"
  },
  "stance": {
    "label": "待模型分析",
    "score_text": "",
    "one_liner": ""
  },
  "key_takeaways": [],
  "risk_flags": [],
  "narrative_blocks": {}
};
