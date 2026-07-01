window.DASHBOARD_DATA = {
  "meta": {
    "title": "美元流动性监测",
    "trigger": "更新数据并分析",
    "generated_at_bjt": "2026-07-01 08:16:07 UTC+08:00",
    "data_as_of": "2026-07-01",
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
    "score_from_rule": 0.3999999999999999
  },
  "trading_dashboard": {
    "core": [
      {
        "type": "signal",
        "id": "SOFR_ANCHOR",
        "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
        "priority": "P0",
        "value_text": "-3.0bp",
        "previous_text": "-3.0bp",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "回购融资是否高于政策锚",
        "interpretation": "SOFR相对IORB（准备金余额利率）的位置。回购融资与政策锚接近",
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "signal",
        "id": "SOFR_VOLUME_IMPACT",
        "label": "SOFR Rate-Volume Impact（SOFR价格×交易量影响）",
        "priority": "P0",
        "value_text": "-2.6mn/day",
        "previous_text": "-2.6mn/day",
        "change_text": "+0.0mn/day",
        "severity": "中性",
        "why": "SOFR价格偏离作用在多大交易量上",
        "interpretation": "SOFR交易量约3,126bn，但SOFR相对政策锚偏离有限，价格×规模冲击不大。",
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储SOFR记录随利率一同发布"
      },
      {
        "type": "metric",
        "id": "TGA",
        "label": "TGA（财政部一般账户）",
        "priority": "P0",
        "value_text": "877.0bn",
        "previous_text": "895.6bn",
        "change_text": "-18.6bn",
        "severity": "中性",
        "why": "财政抽水/放水",
        "interpretation": "财政部现金余额，余额上升通常抽走银行体系准备金，下降通常释放准备金。",
        "as_of": "2026-06-29",
        "frequency": "日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布"
      },
      {
        "type": "signal",
        "id": "RRP_FLOW",
        "label": "RRP Flow（隔夜逆回购边际流量）",
        "priority": "P0",
        "value_text": "23.35bn",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "中性",
        "why": "RRP边际流量方向",
        "interpretation": "RRP日变化幅度有限，短期边际流量影响不大。",
        "as_of": "2026-06-30",
        "frequency": "日频，纽约联储每日操作结果"
      },
      {
        "type": "signal",
        "id": "RRP_BUFFER",
        "label": "RRP Buffer（隔夜逆回购存量缓冲垫）",
        "priority": "P0",
        "value_text": "26.90bn",
        "previous_text": "3.55bn",
        "change_text": "+23.4bn",
        "severity": "偏紧",
        "why": "非银现金缓冲垫厚度",
        "interpretation": "RRP存量缓冲垫几乎耗尽，后续TGA补库、QT或美债供给冲击更容易直接落到准备金。",
        "as_of": "2026-06-30",
        "frequency": "日频，纽约联储每日操作结果"
      },
      {
        "type": "metric",
        "id": "WRESBAL",
        "label": "WRESBAL（银行准备金余额）",
        "priority": "P1",
        "value_text": "2,951.4bn",
        "previous_text": "3,033.4bn",
        "change_text": "-82.0bn",
        "severity": "中性",
        "why": "银行准备金水位",
        "interpretation": "银行体系准备金余额，是美元流动性水位的核心变量，但发布频率较低。",
        "as_of": "2026-06-24",
        "frequency": "周频，H.4.1 通常周四 16:30 ET 发布"
      },
      {
        "type": "signal",
        "id": "UST_1Y_YIELD",
        "label": "1Y Treasury Yield（1年期美国国债收益率）",
        "priority": "P1",
        "value_text": "3.970%",
        "previous_text": "3.940%",
        "change_text": "+0.03%",
        "severity": "中性",
        "why": "短债近端政策路径",
        "interpretation": "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "UST_3Y_YIELD",
        "label": "3Y Treasury Yield（3年期美国国债收益率）",
        "priority": "P1",
        "value_text": "4.100%",
        "previous_text": "4.090%",
        "change_text": "+0.01%",
        "severity": "中性",
        "why": "中段政策路径再定价",
        "interpretation": "3年期收益率处于中间区间，观察其相对1年和10年的斜率变化。",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "REAL_10Y",
        "label": "10Y Treasury Yield（10年期美国国债收益率）",
        "priority": "P1",
        "value_text": "4.380%",
        "previous_text": "4.380%",
        "change_text": "0.00%",
        "severity": "中性",
        "why": "10年期国债收益率压力",
        "interpretation": "10年期国债收益率处于中间区间。",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "HY_CHANGE",
        "label": "HY OAS Change（高收益债期权调整利差变化）",
        "priority": "P1",
        "value_text": "2.800%",
        "previous_text": "2.830%",
        "change_text": "-0.03%",
        "severity": "中性",
        "why": "信用压力是否扩散",
        "interpretation": "信用利差变化有限",
        "as_of": "2026-06-29",
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
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储参考利率"
      },
      {
        "type": "metric",
        "id": "TGCR",
        "label": "TGCR（三方一般抵押品利率）",
        "priority": "P2",
        "value_text": "3.600%",
        "previous_text": "3.600%",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "三方回购融资确认",
        "interpretation": "三方回购市场的一般抵押品融资成本，反映机构化回购资金价格。",
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "metric",
        "id": "BGCR",
        "label": "BGCR（广义一般抵押品利率）",
        "priority": "P2",
        "value_text": "3.600%",
        "previous_text": "3.600%",
        "change_text": "0.0bp",
        "severity": "中性",
        "why": "广义回购融资确认",
        "interpretation": "覆盖更广的一般抵押品回购利率，观察回购市场结构性扰动。",
        "as_of": "2026-06-29",
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
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储约 8:00 ET 发布"
      },
      {
        "type": "signal",
        "id": "REAL_10Y_MOMENTUM",
        "label": "10Y Yield Momentum（10年期国债收益率边际变化）",
        "priority": "P2",
        "value_text": "0.0bp",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "中性",
        "why": "10年期国债收益率边际变化",
        "interpretation": "10年期国债收益率边际变化有限。",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "IG_CHANGE",
        "label": "IG OAS Change（投资级公司债期权调整利差变化）",
        "priority": "P2",
        "value_text": "0.760%",
        "previous_text": "0.770%",
        "change_text": "-0.01%",
        "severity": "中性",
        "why": "投资级信用融资",
        "interpretation": "投资级信用利差变化有限",
        "as_of": "2026-06-29",
        "frequency": "日频，投资级公司债OAS"
      },
      {
        "type": "signal",
        "id": "VIX_RISK",
        "label": "VIX Level（标普500隐含波动率水平）",
        "priority": "P2",
        "value_text": "17.65",
        "previous_text": "18.41",
        "change_text": "-0.76",
        "severity": "中性",
        "why": "证券市场波动率水平",
        "interpretation": "证券市场波动率处于中性区间。",
        "as_of": "2026-06-29",
        "frequency": "日频，标普500隐含波动率"
      },
      {
        "type": "signal",
        "id": "VIX_MOMENTUM",
        "label": "VIX Momentum（标普500隐含波动率边际变化）",
        "priority": "P2",
        "value_text": "-0.76pt",
        "previous_text": "NA",
        "change_text": "NA",
        "severity": "中性",
        "why": "证券市场风险偏好边际变化",
        "interpretation": "VIX边际变化有限。",
        "as_of": "2026-06-29",
        "frequency": "日频，标普500隐含波动率"
      },
      {
        "type": "metric",
        "id": "SOFR_VOLUME",
        "label": "SOFR Volume（SOFR交易量）",
        "priority": "P2",
        "value_text": "3,126.0bn",
        "previous_text": "3,171.0bn",
        "change_text": "-45.0bn",
        "severity": "中性",
        "why": "回购融资交易量级",
        "interpretation": "SOFR对应的隔夜回购交易量，用于把利率偏离转化为价格×规模的实际资金成本量级。",
        "as_of": "2026-06-29",
        "frequency": "日频，纽约联储SOFR记录随利率一同发布"
      },
      {
        "type": "signal",
        "id": "TBILL_AUCTION_STRESS",
        "label": "T-bill Auction Stress Score（短债拍卖吸收压力评分）",
        "priority": "P2",
        "value_text": "40.00",
        "previous_text": "35.00",
        "change_text": "+5.00index",
        "severity": "中性",
        "why": "T-bill供给×需求吸收压力",
        "interpretation": "最新T-bill拍卖规模约145.0bn，认购倍数2.77x，上一T-bill拍卖日认购倍数 2.55x；该分数综合供给规模与需求覆盖，数值越高表示吸收压力越大。供给吸收处于中性区间。",
        "as_of": "2026-06-25",
        "frequency": "事件驱动，财政部T-bill拍卖后公布"
      },
      {
        "type": "metric",
        "id": "TBILL_AUCTION_BTC",
        "label": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
        "priority": "P2",
        "value_text": "2.77x",
        "previous_text": "2.55x",
        "change_text": "+0.22x",
        "severity": "中性",
        "why": "短债拍卖需求强度",
        "interpretation": "短期国债拍卖投标覆盖倍数，和拍卖规模一起观察T-bill供给吸收压力。",
        "as_of": "2026-06-25",
        "frequency": "事件驱动，财政部T-bill拍卖后公布"
      },
      {
        "type": "metric",
        "id": "UST_AUCTION_BTC",
        "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
        "priority": "P2",
        "value_text": "2.50x",
        "previous_text": "2.79x",
        "change_text": "-0.29x",
        "severity": "中性",
        "why": "国债供给吸收能力",
        "interpretation": "国债拍卖需求强弱代理指标，观察国债供给吸收能力。",
        "as_of": "2026-06-25",
        "frequency": "事件驱动，财政部拍卖后公布"
      },
      {
        "type": "metric",
        "id": "REPO_FAILS_UST",
        "label": "Repo Fails（美国国债回购交割失败）",
        "priority": "P2",
        "value_text": "101.2bn",
        "previous_text": "118.7bn",
        "change_text": "-17.5bn",
        "severity": "中性",
        "why": "抵押品交割链条",
        "interpretation": "回购和证券交割失败规模，观察抵押品链条和交割压力。",
        "as_of": "2026-06-17",
        "frequency": "周频，OFR/STFM 或一级交易商口径"
      },
      {
        "type": "metric",
        "id": "DTWEXBGS",
        "label": "DTWEXBGS（广义美元指数）",
        "priority": "P2",
        "value_text": "120.89",
        "previous_text": "121.06",
        "change_text": "-0.17",
        "severity": "中性",
        "why": "离岸美元压力",
        "interpretation": "广义美元指数，作为离岸美元融资压力的替代观察。",
        "as_of": "2026-06-26",
        "frequency": "日频，FRED/美联储美元指数口径"
      },
      {
        "type": "signal",
        "id": "CP_PROXY",
        "label": "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）",
        "priority": "P2",
        "value_text": "-3.0bp",
        "previous_text": "NA",
        "change_text": "NA",
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
        "value_text": "6,344.3bn",
        "previous_text": "6,347.5bn",
        "change_text": "-3.2bn",
        "severity": "中性",
        "why": "QT结构背景",
        "interpretation": "美联储公开市场账户持仓，反映QT和资产端收缩的结构背景。",
        "as_of": "2026-06-24",
        "frequency": "周频，纽约联储/Fed资产负债表背景数据"
      },
      {
        "type": "metric",
        "id": "DGS1",
        "label": "1Y Treasury Yield（1年期美国国债收益率）",
        "priority": "B",
        "value_text": "3.970%",
        "previous_text": "3.940%",
        "change_text": "+3.0bp",
        "severity": "中性",
        "why": "近端政策路径",
        "interpretation": "1年期美国国债收益率，主要反映未来一年政策利率路径和短端再定价。",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "metric",
        "id": "DGS30",
        "label": "30Y Treasury Yield（30年期美国国债收益率）",
        "priority": "B",
        "value_text": "4.860%",
        "previous_text": "4.870%",
        "change_text": "-1.0bp",
        "severity": "中性",
        "why": "长期期限溢价",
        "interpretation": "30年期美国国债收益率，反映长期通胀、财政供给和期限溢价。",
        "as_of": "2026-06-29",
        "frequency": "日频，FRED/H.15国债恒定期限收益率"
      },
      {
        "type": "signal",
        "id": "UST_10Y2Y",
        "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
        "priority": "B",
        "value_text": "30.0bp",
        "previous_text": "28.0bp",
        "change_text": "+2.0bp",
        "severity": "中性",
        "why": "收益率曲线斜率",
        "interpretation": "收益率曲线为正，期限结构相对正常",
        "as_of": "2026-06-30",
        "frequency": "日频，FRED曲线利差"
      },
      {
        "type": "signal",
        "id": "UST_10Y3M",
        "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
        "priority": "B",
        "value_text": "57.0bp",
        "previous_text": "51.0bp",
        "change_text": "+6.0bp",
        "severity": "中性",
        "why": "衰退/降息预期",
        "interpretation": "10年-3个月曲线为正，政策短端对长期利率压制较弱",
        "as_of": "2026-06-30",
        "frequency": "日频，FRED曲线利差"
      },
      {
        "type": "signal",
        "id": "NFCI_LEVEL",
        "label": "NFCI（芝加哥联储全国金融条件指数）",
        "priority": "B",
        "value_text": "-0.52",
        "previous_text": "-0.51",
        "change_text": "-0.00",
        "severity": "偏松",
        "why": "公开金融条件代理",
        "interpretation": "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察",
        "as_of": "2026-06-19",
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
    "as_of": "2026-07-01",
    "lookforward_days": 60,
    "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-07-01&endDate=2026-08-30",
    "auctions": [
      {
        "auctionDate": "2026-07-01",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "17-Week",
        "offeringAmount": 72.0,
        "offeringAmountText": "$72bn",
        "cusip": "912797VP9",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797US4",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797UW5",
        "is_bill": true,
        "is_note_or_bond": false
      }
    ],
    "bill_schedule": [
      {
        "auctionDate": "2026-07-01",
        "totalBillOffering": 72.0,
        "items": [
          {
            "auctionDate": "2026-07-01",
            "issueDate": "2026-07-07",
            "announcementDate": "2026-06-30",
            "securityType": "Bill",
            "securityTerm": "17-Week",
            "offeringAmount": 72.0,
            "offeringAmountText": "$72bn",
            "cusip": "912797VP9",
            "is_bill": true,
            "is_note_or_bond": false
          }
        ],
        "totalBillOfferingText": "$72bn"
      },
      {
        "auctionDate": "2026-07-02",
        "totalBillOffering": 170.0,
        "items": [
          {
            "auctionDate": "2026-07-02",
            "issueDate": "2026-07-07",
            "announcementDate": "2026-06-30",
            "securityType": "Bill",
            "securityTerm": "4-Week",
            "offeringAmount": 85.0,
            "offeringAmountText": "$85bn",
            "cusip": "912797US4",
            "is_bill": true,
            "is_note_or_bond": false
          },
          {
            "auctionDate": "2026-07-02",
            "issueDate": "2026-07-07",
            "announcementDate": "2026-06-30",
            "securityType": "Bill",
            "securityTerm": "8-Week",
            "offeringAmount": 85.0,
            "offeringAmountText": "$85bn",
            "cusip": "912797UW5",
            "is_bill": true,
            "is_note_or_bond": false
          }
        ],
        "totalBillOfferingText": "$170bn"
      }
    ],
    "next_auctions": [
      {
        "auctionDate": "2026-07-01",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "17-Week",
        "offeringAmount": 72.0,
        "offeringAmountText": "$72bn",
        "cusip": "912797VP9",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797US4",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797UW5",
        "is_bill": true,
        "is_note_or_bond": false
      }
    ],
    "large_auctions": [
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "4-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797US4",
        "is_bill": true,
        "is_note_or_bond": false
      },
      {
        "auctionDate": "2026-07-02",
        "issueDate": "2026-07-07",
        "announcementDate": "2026-06-30",
        "securityType": "Bill",
        "securityTerm": "8-Week",
        "offeringAmount": 85.0,
        "offeringAmountText": "$85bn",
        "cusip": "912797UW5",
        "is_bill": true,
        "is_note_or_bond": false
      }
    ],
    "notes": "TreasuryDirect future auction calendar. offeringAmount may be absent before official announcement; treat missing amounts as data risk, not zero issuance."
  },
  "jpy_carry": {
    "meta": {
      "generated_at_bjt": "2026-07-01 08:15:45 UTC+08:00",
      "lookback": "日频约1年，CFTC约2年，REER/NEER约3年"
    },
    "risk": {
      "label": "中性偏高",
      "score": 3.0,
      "reasons": [
        "CFTC日元非商业净空头占未平仓合约比例偏高",
        "JGB 10Y阶段性上行，日本本土收益率吸引力增强",
        "美日10Y利差处于相对较窄区域，收益端安全垫下降"
      ]
    },
    "cards": [
      {
        "id": "USDJPY",
        "label": "USD/JPY（美元兑日元）",
        "value_text": "161.83",
        "change_text": "逐日 +0.12%",
        "as_of": "2026-06-29",
        "why": "日元快速升值会触发carry止损/回补"
      },
      {
        "id": "JPY_CALL",
        "label": "JPY隔夜融资成本（日本无担保隔夜拆借利率）",
        "value_text": "0.978%",
        "change_text": "逐日 0.1bp",
        "as_of": "2026-06-29",
        "why": "carry trade 的融资端"
      },
      {
        "id": "JGB10",
        "label": "JGB 10Y（日本10年期国债收益率）",
        "value_text": "2.657%",
        "change_text": "逐日 -3.5bp",
        "as_of": "2026-05-29",
        "why": "日本本土资产吸引力和资金回流压力"
      },
      {
        "id": "US_JP_10Y",
        "label": "10Y UST-JGB利差（美日10年期国债利差）",
        "value_text": "172bp",
        "change_text": "收益端核心",
        "as_of": "2026-05-29",
        "why": "美日长端利差越宽，carry收益端越顺风"
      },
      {
        "id": "CFTC_JPY",
        "label": "CFTC JPY净仓位/OI（日元期货非商业净仓位占比）",
        "value_text": "-33.9%",
        "change_text": "周变化 4,028 contracts",
        "as_of": "2026-06-23",
        "why": "日元空头拥挤度，周频背景信号"
      },
      {
        "id": "USDJPY_VOL20",
        "label": "USD/JPY 20日实现波动率（年化）",
        "value_text": "2.37%",
        "change_text": "年化",
        "as_of": "2026-06-29",
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
      "us_jp_spread"
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
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "previous": 3.62,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "previous": 3.6,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "previous": 3.6,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "as_of": "2026-07-01",
          "previous_as_of": "2026-06-30",
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
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 876.961,
          "value_text": "877.0bn",
          "unit": "USD bn",
          "previous": 895.576,
          "change": -18.61500000000001,
          "change_text": "-18.6bn",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
          "meaning": "财政部现金余额，余额上升通常抽走银行体系准备金，下降通常释放准备金。",
          "frequency": "日频，Daily Treasury Statement 通常次一工作日 16:00 ET 前发布",
          "data_lag": "覆盖上一工作日财政现金和债务操作",
          "comparison_basis": "与上一条有效工作日观测比较，不能与当天市场利率强行同日对齐。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "Treasury FiscalData",
          "source_url": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=90",
          "status": "ok",
          "notes": ""
        },
        {
          "id": "RRPONTSYD",
          "label": "RRP（隔夜逆回购）",
          "category": "Fed负债端",
          "value": 26.9,
          "value_text": "26.9bn",
          "unit": "USD bn",
          "previous": 3.546,
          "change": 23.354,
          "change_text": "+23.4bn",
          "change_direction": "up",
          "as_of": "2026-06-30",
          "previous_as_of": "2026-06-29",
          "meaning": "货币基金等机构停放在美联储的隔夜逆回购余额，是准备金压力前的缓冲垫。",
          "frequency": "日频，纽约联储每日操作结果",
          "data_lag": "同日操作结果，工作日/操作日口径",
          "comparison_basis": "与上一条操作日观测比较。",
          "freshness": "ok",
          "importance": "high",
          "interpretation_hint": "",
          "source": "NY Fed Markets API",
          "source_url": "https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?startDate=2026-06-17&endDate=2026-07-01",
          "status": "ok",
          "notes": "NY Fed reverse repo accepted amount; replaces FRED RRPONTSYD when FRED is slow or unavailable"
        },
        {
          "id": "SOMA",
          "label": "SOMA（系统公开市场账户持仓）",
          "category": "Fed负债端",
          "value": 6344.3455674457,
          "value_text": "6,344.3bn",
          "unit": "USD bn",
          "previous": 6347.5283145840995,
          "change": -3.1827471383994634,
          "change_text": "-3.2bn",
          "change_direction": "down",
          "as_of": "2026-06-24",
          "previous_as_of": "2026-06-17",
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
          "value": 2951.416,
          "value_text": "2,951.4bn",
          "unit": "USD bn",
          "previous": 3033.444,
          "change": -82.02799999999979,
          "change_text": "-82.0bn",
          "change_direction": "down",
          "as_of": "2026-06-24",
          "previous_as_of": "2026-06-17",
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
          "value": 3.97,
          "value_text": "3.970%",
          "unit": "%",
          "previous": 3.94,
          "change": 0.03000000000000025,
          "change_text": "+3.0bp",
          "change_direction": "up",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 4.1,
          "value_text": "4.100%",
          "unit": "%",
          "previous": 4.09,
          "change": 0.009999999999999787,
          "change_text": "+1.0bp",
          "change_direction": "up",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 4.38,
          "value_text": "4.380%",
          "unit": "%",
          "previous": 4.38,
          "change": 0.0,
          "change_text": "0.0bp",
          "change_direction": "flat",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 2.16,
          "value_text": "2.160%",
          "unit": "%",
          "previous": 2.18,
          "change": -0.020000000000000018,
          "change_text": "-2.0bp",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 4.86,
          "value_text": "4.860%",
          "unit": "%",
          "previous": 4.87,
          "change": -0.009999999999999787,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 0.3,
          "value_text": "0.300%",
          "unit": "%",
          "previous": 0.28,
          "change": 0.019999999999999962,
          "change_text": "+2.0bp",
          "change_direction": "up",
          "as_of": "2026-06-30",
          "previous_as_of": "2026-06-29",
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
          "value": 0.57,
          "value_text": "0.570%",
          "unit": "%",
          "previous": 0.51,
          "change": 0.05999999999999994,
          "change_text": "+6.0bp",
          "change_direction": "up",
          "as_of": "2026-06-30",
          "previous_as_of": "2026-06-29",
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
          "value": 3.74,
          "value_text": "3.740%",
          "unit": "%",
          "previous": 3.67,
          "change": 0.07000000000000028,
          "change_text": "+7.0bp",
          "change_direction": "up",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 3.87,
          "value_text": "3.870%",
          "unit": "%",
          "previous": 3.83,
          "change": 0.040000000000000036,
          "change_text": "+4.0bp",
          "change_direction": "up",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 4.1,
          "value_text": "4.100%",
          "unit": "%",
          "previous": 4.07,
          "change": 0.02999999999999936,
          "change_text": "+3.0bp",
          "change_direction": "up",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 3126.0,
          "value_text": "3,126.0bn",
          "unit": "USD bn",
          "previous": 3171.0,
          "change": -45.0,
          "change_text": "-45.0bn",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 145.0,
          "value_text": "145.0bn",
          "unit": "USD bn",
          "previous": 69.0,
          "change": 76.0,
          "change_text": "+76.0bn",
          "change_direction": "up",
          "as_of": "2026-06-25",
          "previous_as_of": "2026-06-24",
          "meaning": "短期国债拍卖发行规模，观察货币基金、银行和交易商需要吸收的新增/滚续短债供给量级。",
          "frequency": "事件驱动，财政部T-bill拍卖后公布",
          "data_lag": "同一拍卖日多只Bill按发行额加总",
          "comparison_basis": "与上一T-bill拍卖日比较，并与认购倍数一起判断供给吸收压力。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-10&endDate=2026-07-01",
          "status": "ok",
          "notes": "Aggregates all Treasury Bill auctions on the latest auction date; bid-to-cover is offering-amount weighted. Latest terms: 4-Week, 8-Week."
        },
        {
          "id": "TBILL_AUCTION_BTC",
          "label": "T-bill Auction BTC（短期国债拍卖投标覆盖倍数）",
          "category": "国债/抵押品",
          "value": 2.765862068965517,
          "value_text": "2.77x",
          "unit": "ratio",
          "previous": 2.55,
          "change": 0.2158620689655173,
          "change_text": "+0.22x",
          "change_direction": "up",
          "as_of": "2026-06-25",
          "previous_as_of": "2026-06-24",
          "meaning": "短期国债拍卖投标覆盖倍数，和拍卖规模一起观察T-bill供给吸收压力。",
          "frequency": "事件驱动，财政部T-bill拍卖后公布",
          "data_lag": "同一拍卖日多只Bill按发行额加权平均",
          "comparison_basis": "与上一T-bill拍卖日比较；必须结合拍卖规模，不能只看倍数。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-10&endDate=2026-07-01",
          "status": "ok",
          "notes": "Aggregates all Treasury Bill auctions on the latest auction date; bid-to-cover is offering-amount weighted. Latest terms: 4-Week, 8-Week."
        },
        {
          "id": "UST_AUCTION_BTC",
          "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
          "category": "国债/抵押品",
          "value": 2.5,
          "value_text": "2.50x",
          "unit": "ratio",
          "previous": 2.79,
          "change": -0.29000000000000004,
          "change_text": "-0.29x",
          "change_direction": "down",
          "as_of": "2026-06-25",
          "previous_as_of": "2026-06-25",
          "meaning": "国债拍卖需求强弱代理指标，观察国债供给吸收能力。",
          "frequency": "事件驱动，财政部拍卖后公布",
          "data_lag": "只在拍卖发生时更新",
          "comparison_basis": "与上一场可比拍卖比较，不能日度环比。",
          "freshness": "recent",
          "importance": "medium_high",
          "interpretation_hint": "",
          "source": "TreasuryDirect",
          "source_url": "https://www.treasurydirect.gov/TA_WS/securities/search?format=json&startDate=2026-06-10&endDate=2026-07-01",
          "status": "ok",
          "notes": "Uses bid-to-cover as free auction demand proxy; auction tail requires WI yield not available here"
        },
        {
          "id": "REPO_FAILS_UST",
          "label": "Repo Fails（美国国债回购交割失败）",
          "category": "国债/抵押品",
          "value": 101.239,
          "value_text": "101.2bn",
          "unit": "USD bn",
          "previous": 118.735,
          "change": -17.495999999999995,
          "change_text": "-17.5bn",
          "change_direction": "down",
          "as_of": "2026-06-17",
          "previous_as_of": "2026-06-10",
          "meaning": "回购和证券交割失败规模，观察抵押品链条和交割压力。",
          "frequency": "周频，OFR/STFM 或一级交易商口径",
          "data_lag": "交割失败周度背景",
          "comparison_basis": "只看周度趋势，不参与日度环比。",
          "freshness": "ok",
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
          "value": 120.8866,
          "value_text": "120.89",
          "unit": "index",
          "previous": 121.0559,
          "change": -0.16929999999999268,
          "change_text": "-0.17",
          "change_direction": "down",
          "as_of": "2026-06-26",
          "previous_as_of": "2026-06-25",
          "meaning": "广义美元指数，作为离岸美元融资压力的替代观察。",
          "frequency": "日频，FRED/美联储美元指数口径",
          "data_lag": "通常随源数据滞后更新",
          "comparison_basis": "与上一条有效观测比较，注意可能比资金利率更滞后。",
          "freshness": "ok",
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
          "previous": null,
          "change": null,
          "change_text": "NA",
          "change_direction": "unknown",
          "as_of": "2026-06-26",
          "previous_as_of": null,
          "meaning": "企业短期融资价格，观察货币市场压力是否传导到商业票据。",
          "frequency": "日频，商业票据利率",
          "data_lag": "通常T+1或随源数据更新",
          "comparison_basis": "与上一条有效观测比较。",
          "freshness": "ok",
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
          "previous": 0.77,
          "change": -0.010000000000000009,
          "change_text": "-1.0bp",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": 2.8,
          "value_text": "2.800%",
          "unit": "%",
          "previous": 2.83,
          "change": -0.03000000000000025,
          "change_text": "-3.0bp",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
          "value": -0.516,
          "value_text": "-0.52",
          "unit": "index",
          "previous": -0.513,
          "change": -0.0030000000000000027,
          "change_text": "-0.00",
          "change_direction": "flat",
          "as_of": "2026-06-19",
          "previous_as_of": "2026-06-12",
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
          "value": 17.65,
          "value_text": "17.65",
          "unit": "index",
          "previous": 18.41,
          "change": -0.7600000000000016,
          "change_text": "-0.76",
          "change_direction": "down",
          "as_of": "2026-06-29",
          "previous_as_of": "2026-06-26",
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
      "previous": -2.9999999999999805,
      "previous_text": "-3.0bp",
      "change": 0.0,
      "change_text": "0.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "SOFR相对IORB（准备金余额利率）的位置。回购融资与政策锚接近",
      "as_of": "2026-06-29"
    },
    {
      "id": "SOFR_VOLUME_IMPACT",
      "label": "SOFR Rate-Volume Impact（SOFR价格×交易量影响）",
      "value": -2.6049999999999827,
      "value_text": "-2.6mn/day",
      "previous": -2.6424999999999828,
      "previous_text": "-2.6mn/day",
      "change": 0.03750000000000009,
      "change_text": "+0.0mn/day",
      "unit": "USD mn/day",
      "severity": "中性",
      "meaning": "SOFR交易量约3,126bn，但SOFR相对政策锚偏离有限，价格×规模冲击不大。",
      "as_of": "2026-06-29"
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
      "as_of": "2026-06-29"
    },
    {
      "id": "CP_PROXY",
      "label": "CP Rate-Policy Upper Proxy（商业票据利率-政策上限代理利差）",
      "value": -2.9999999999999805,
      "value_text": "-3.0bp",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "bp",
      "severity": "偏松",
      "meaning": "用90天AA非金融商业票据利率减联邦基金目标上限，粗略观察企业短融相对政策利率是否变贵；这是信用传导代理指标，不是FRA-OIS。企业短融压力不明显",
      "as_of": "2026-06-26"
    },
    {
      "id": "TGA_FLOW",
      "label": "TGA Daily Change（财政部一般账户日变化）",
      "value": -18.61500000000001,
      "value_text": "-18.62bn",
      "previous": 24.10699999999997,
      "previous_text": "24.11bn",
      "change": -42.72199999999998,
      "change_text": "-42.7bn",
      "unit": "bn",
      "severity": "中性",
      "meaning": "财政资金流变化不大",
      "as_of": "2026-06-29"
    },
    {
      "id": "RRP_FLOW",
      "label": "RRP Flow（隔夜逆回购边际流量）",
      "value": 23.354,
      "value_text": "23.35bn",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "bn",
      "severity": "中性",
      "meaning": "RRP日变化幅度有限，短期边际流量影响不大。",
      "as_of": "2026-06-30"
    },
    {
      "id": "RRP_BUFFER",
      "label": "RRP Buffer（隔夜逆回购存量缓冲垫）",
      "value": 26.9,
      "value_text": "26.90bn",
      "previous": 3.546,
      "previous_text": "3.55bn",
      "change": 23.354,
      "change_text": "+23.4bn",
      "unit": "bn",
      "severity": "偏紧",
      "meaning": "RRP存量缓冲垫几乎耗尽，后续TGA补库、QT或美债供给冲击更容易直接落到准备金。",
      "as_of": "2026-06-30"
    },
    {
      "id": "UST_1Y_YIELD",
      "label": "1Y Treasury Yield（1年期美国国债收益率）",
      "value": 3.97,
      "value_text": "3.970%",
      "previous": 3.94,
      "previous_text": "3.940%",
      "change": 0.03000000000000025,
      "change_text": "+0.03%",
      "unit": "%",
      "severity": "中性",
      "meaning": "1年期收益率处于中间区间，需结合3年期和10年期确认曲线重定价",
      "as_of": "2026-06-29"
    },
    {
      "id": "UST_3Y_YIELD",
      "label": "3Y Treasury Yield（3年期美国国债收益率）",
      "value": 4.1,
      "value_text": "4.100%",
      "previous": 4.09,
      "previous_text": "4.090%",
      "change": 0.009999999999999787,
      "change_text": "+0.01%",
      "unit": "%",
      "severity": "中性",
      "meaning": "3年期收益率处于中间区间，观察其相对1年和10年的斜率变化。",
      "as_of": "2026-06-29"
    },
    {
      "id": "NOMINAL_10Y",
      "label": "10Y Treasury Yield（10年期美国国债收益率）",
      "value": 4.38,
      "value_text": "4.380%",
      "previous": 4.38,
      "previous_text": "4.380%",
      "change": 0.0,
      "change_text": "0.00%",
      "unit": "%",
      "severity": "中性",
      "meaning": "长期名义折现率边际变化有限",
      "as_of": "2026-06-29"
    },
    {
      "id": "REAL_10Y",
      "label": "10Y Treasury Yield（10年期美国国债收益率）",
      "value": 4.38,
      "value_text": "4.380%",
      "previous": 4.38,
      "previous_text": "4.380%",
      "change": 0.0,
      "change_text": "0.00%",
      "unit": "%",
      "severity": "中性",
      "meaning": "10年期国债收益率处于中间区间。",
      "as_of": "2026-06-29"
    },
    {
      "id": "REAL_10Y_MOMENTUM",
      "label": "10Y Yield Momentum（10年期国债收益率边际变化）",
      "value": 0.0,
      "value_text": "0.0bp",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "bp",
      "severity": "中性",
      "meaning": "10年期国债收益率边际变化有限。",
      "as_of": "2026-06-29"
    },
    {
      "id": "HY_CHANGE",
      "label": "HY OAS Change（高收益债期权调整利差变化）",
      "value": 2.8,
      "value_text": "2.800%",
      "previous": 2.83,
      "previous_text": "2.830%",
      "change": -0.03000000000000025,
      "change_text": "-0.03%",
      "unit": "%",
      "severity": "中性",
      "meaning": "信用利差变化有限",
      "as_of": "2026-06-29"
    },
    {
      "id": "IG_CHANGE",
      "label": "IG OAS Change（投资级公司债期权调整利差变化）",
      "value": 0.76,
      "value_text": "0.760%",
      "previous": 0.77,
      "previous_text": "0.770%",
      "change": -0.010000000000000009,
      "change_text": "-0.01%",
      "unit": "%",
      "severity": "中性",
      "meaning": "投资级信用利差变化有限",
      "as_of": "2026-06-29"
    },
    {
      "id": "VIX_RISK",
      "label": "VIX Level（标普500隐含波动率水平）",
      "value": 17.65,
      "value_text": "17.65",
      "previous": 18.41,
      "previous_text": "18.41",
      "change": -0.7600000000000016,
      "change_text": "-0.76",
      "unit": "",
      "severity": "中性",
      "meaning": "证券市场波动率处于中性区间。",
      "as_of": "2026-06-29"
    },
    {
      "id": "VIX_MOMENTUM",
      "label": "VIX Momentum（标普500隐含波动率边际变化）",
      "value": -0.7600000000000016,
      "value_text": "-0.76pt",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "pt",
      "severity": "中性",
      "meaning": "VIX边际变化有限。",
      "as_of": "2026-06-29"
    },
    {
      "id": "USD_CHANGE",
      "label": "Broad Dollar Index Change（广义美元指数变化）",
      "value": -0.16929999999999268,
      "value_text": "-0.17pt",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "pt",
      "severity": "中性",
      "meaning": "离岸美元代理指标变化有限",
      "as_of": "2026-06-26"
    },
    {
      "id": "UST_10Y2Y",
      "label": "10Y-2Y Treasury Spread（10年-2年美债利差）",
      "value": 30.0,
      "value_text": "30.0bp",
      "previous": 28.000000000000004,
      "previous_text": "28.0bp",
      "change": 1.9999999999999964,
      "change_text": "+2.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "收益率曲线为正，期限结构相对正常",
      "as_of": "2026-06-30"
    },
    {
      "id": "UST_10Y3M",
      "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
      "value": 56.99999999999999,
      "value_text": "57.0bp",
      "previous": 51.0,
      "previous_text": "51.0bp",
      "change": 5.999999999999993,
      "change_text": "+6.0bp",
      "unit": "bp",
      "severity": "中性",
      "meaning": "10年-3个月曲线为正，政策短端对长期利率压制较弱",
      "as_of": "2026-06-30"
    },
    {
      "id": "NFCI_LEVEL",
      "label": "NFCI（芝加哥联储全国金融条件指数）",
      "value": -0.516,
      "value_text": "-0.52",
      "previous": -0.513,
      "previous_text": "-0.51",
      "change": -0.0030000000000000027,
      "change_text": "-0.00",
      "unit": "",
      "severity": "偏松",
      "meaning": "公开金融条件代理显示金融条件偏松；它不是高盛FCI，但可作为免费公开替代观察",
      "as_of": "2026-06-19"
    },
    {
      "id": "TBILL_AUCTION_STRESS",
      "label": "T-bill Auction Stress Score（短债拍卖吸收压力评分）",
      "value": 40.0,
      "value_text": "40.00",
      "previous": 35.0,
      "previous_text": "35.00",
      "change": 5.0,
      "change_text": "+5.00index",
      "unit": "index",
      "severity": "中性",
      "meaning": "最新T-bill拍卖规模约145.0bn，认购倍数2.77x，上一T-bill拍卖日认购倍数 2.55x；该分数综合供给规模与需求覆盖，数值越高表示吸收压力越大。供给吸收处于中性区间。",
      "as_of": "2026-06-25"
    },
    {
      "id": "AUCTION_BTC",
      "label": "UST Auction BTC（国债拍卖投标覆盖倍数）",
      "value": 2.5,
      "value_text": "2.50x",
      "previous": null,
      "previous_text": "NA",
      "change": null,
      "change_text": "NA",
      "unit": "x",
      "severity": "中性",
      "meaning": "拍卖需求中性",
      "as_of": "2026-06-25"
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "SOFR",
          "label": "SOFR（担保隔夜融资利率）",
          "points": [
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "TGCR",
          "label": "TGCR（三方一般抵押品利率）",
          "points": [
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR",
          "label": "BGCR（广义一般抵押品利率）",
          "points": [
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
              "date": "2026-05-27",
              "value": 3.62
            },
            {
              "date": "2026-05-28",
              "value": 3.62
            },
            {
              "date": "2026-05-29",
              "value": 3.62
            },
            {
              "date": "2026-06-01",
              "value": 3.62
            },
            {
              "date": "2026-06-02",
              "value": 3.62
            },
            {
              "date": "2026-06-03",
              "value": 3.62
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "SOFR",
          "label": "SOFR（担保隔夜融资利率）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 3.63
            },
            {
              "date": "2026-05-28",
              "value": 3.62
            },
            {
              "date": "2026-05-29",
              "value": 3.63
            },
            {
              "date": "2026-06-01",
              "value": 3.65
            },
            {
              "date": "2026-06-02",
              "value": 3.63
            },
            {
              "date": "2026-06-03",
              "value": 3.61
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "TGCR",
          "label": "TGCR（三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 3.62
            },
            {
              "date": "2026-05-28",
              "value": 3.6
            },
            {
              "date": "2026-05-29",
              "value": 3.61
            },
            {
              "date": "2026-06-01",
              "value": 3.63
            },
            {
              "date": "2026-06-02",
              "value": 3.6
            },
            {
              "date": "2026-06-03",
              "value": 3.59
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR",
          "label": "BGCR（广义一般抵押品利率）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 3.62
            },
            {
              "date": "2026-05-28",
              "value": 3.6
            },
            {
              "date": "2026-05-29",
              "value": 3.61
            },
            {
              "date": "2026-06-01",
              "value": 3.63
            },
            {
              "date": "2026-06-02",
              "value": 3.61
            },
            {
              "date": "2026-06-03",
              "value": 3.59
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR_TGCR",
          "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
          "points": [
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
              "date": "2026-05-27",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-05-28",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-01",
              "value": -2.9999999999999805
            },
            {
              "date": "2026-06-02",
              "value": -2.0000000000000018
            },
            {
              "date": "2026-06-03",
              "value": 0.0
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BGCR_TGCR",
          "label": "BGCR-TGCR（广义一般抵押品利率-三方一般抵押品利率）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 0.0
            },
            {
              "date": "2026-05-28",
              "value": 0.0
            },
            {
              "date": "2026-06-01",
              "value": 0.0
            },
            {
              "date": "2026-06-02",
              "value": 0.0
            },
            {
              "date": "2026-06-03",
              "value": 0.0
            },
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
              "date": "2026-05-27",
              "value": 3176.0
            },
            {
              "date": "2026-05-28",
              "value": 3139.0
            },
            {
              "date": "2026-05-29",
              "value": 3201.0
            },
            {
              "date": "2026-06-01",
              "value": 3224.0
            },
            {
              "date": "2026-06-02",
              "value": 3148.0
            },
            {
              "date": "2026-06-03",
              "value": 3098.0
            },
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
              "date": "2026-05-21",
              "value": 220.0
            },
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
              "date": "2026-05-21",
              "value": 2.900681818181818
            },
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
              "date": "2026-05-27",
              "value": -6.000000000000005
            },
            {
              "date": "2026-05-28",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-01",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-02",
              "value": -6.000000000000005
            },
            {
              "date": "2026-06-03",
              "value": -6.000000000000005
            },
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
              "date": "2026-05-27",
              "value": 2.71
            },
            {
              "date": "2026-05-28",
              "value": 2.72
            },
            {
              "date": "2026-05-31",
              "value": 2.74
            },
            {
              "date": "2026-06-01",
              "value": 2.72
            },
            {
              "date": "2026-06-02",
              "value": 2.71
            },
            {
              "date": "2026-06-03",
              "value": 2.75
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "BAMLC0A0CM",
          "label": "IG OAS（投资级公司债期权调整利差）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 0.74
            },
            {
              "date": "2026-05-28",
              "value": 0.73
            },
            {
              "date": "2026-05-31",
              "value": 0.74
            },
            {
              "date": "2026-06-01",
              "value": 0.73
            },
            {
              "date": "2026-06-02",
              "value": 0.74
            },
            {
              "date": "2026-06-03",
              "value": 0.74
            },
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
              "date": "2026-05-28",
              "value": 3.8
            },
            {
              "date": "2026-05-29",
              "value": 3.79
            },
            {
              "date": "2026-06-01",
              "value": 3.83
            },
            {
              "date": "2026-06-02",
              "value": 3.82
            },
            {
              "date": "2026-06-03",
              "value": 3.84
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "DGS3",
          "label": "3Y Treasury Yield（3年期美国国债收益率）",
          "points": [
            {
              "date": "2026-05-28",
              "value": 4.07
            },
            {
              "date": "2026-05-29",
              "value": 4.06
            },
            {
              "date": "2026-06-01",
              "value": 4.09
            },
            {
              "date": "2026-06-02",
              "value": 4.09
            },
            {
              "date": "2026-06-03",
              "value": 4.14
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "DGS10",
          "label": "10Y Treasury Yield（10年期美国国债收益率）",
          "points": [
            {
              "date": "2026-05-28",
              "value": 4.45
            },
            {
              "date": "2026-05-29",
              "value": 4.45
            },
            {
              "date": "2026-06-01",
              "value": 4.47
            },
            {
              "date": "2026-06-02",
              "value": 4.46
            },
            {
              "date": "2026-06-03",
              "value": 4.49
            },
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
              "date": "2026-05-28",
              "value": 2.06
            },
            {
              "date": "2026-05-29",
              "value": 2.07
            },
            {
              "date": "2026-06-01",
              "value": 2.07
            },
            {
              "date": "2026-06-02",
              "value": 2.07
            },
            {
              "date": "2026-06-03",
              "value": 2.11
            },
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
              "date": "2026-05-27",
              "value": 0.48
            },
            {
              "date": "2026-05-29",
              "value": 0.47
            },
            {
              "date": "2026-06-01",
              "value": 0.42
            },
            {
              "date": "2026-06-02",
              "value": 0.41
            },
            {
              "date": "2026-06-03",
              "value": 0.41
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "T10Y3M",
          "label": "10Y-3M Treasury Spread（10年-3个月美债利差）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 0.8
            },
            {
              "date": "2026-05-29",
              "value": 0.76
            },
            {
              "date": "2026-06-01",
              "value": 0.69
            },
            {
              "date": "2026-06-02",
              "value": 0.69
            },
            {
              "date": "2026-06-03",
              "value": 0.71
            },
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
              "date": "2026-05-27",
              "value": 16.29
            },
            {
              "date": "2026-05-28",
              "value": 15.74
            },
            {
              "date": "2026-05-29",
              "value": 15.32
            },
            {
              "date": "2026-06-01",
              "value": 16.05
            },
            {
              "date": "2026-06-02",
              "value": 15.77
            },
            {
              "date": "2026-06-03",
              "value": 16.06
            },
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
              "date": "2026-05-29",
              "value": -0.494
            },
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
              "date": "2026-05-28",
              "value": 849.71
            },
            {
              "date": "2026-05-29",
              "value": 903.881
            },
            {
              "date": "2026-06-02",
              "value": 866.075
            },
            {
              "date": "2026-06-03",
              "value": 845.722
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "RRP",
          "label": "RRP（隔夜逆回购）",
          "points": [
            {
              "date": "2026-05-27",
              "value": 1.853
            },
            {
              "date": "2026-05-29",
              "value": 11.677
            },
            {
              "date": "2026-06-01",
              "value": 1.302
            },
            {
              "date": "2026-06-02",
              "value": 2.502
            },
            {
              "date": "2026-06-03",
              "value": 2.062
            },
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
      "id": "treasury_combined_supply_30d",
      "title": "合并美债发行量：前20日 + 后10日",
      "chart_type": "line",
      "unit": "USD bn",
      "series": [
        {
          "id": "TREASURY_COMBINED_SUPPLY",
          "label": "Total Treasury Supply（全部美债发行量）",
          "points": [
            {
              "date": "2026-06-11",
              "value": 167.0
            },
            {
              "date": "2026-06-15",
              "value": 166.0
            },
            {
              "date": "2026-06-16",
              "value": 78.0
            },
            {
              "date": "2026-06-17",
              "value": 69.0
            },
            {
              "date": "2026-06-18",
              "value": 169.0
            },
            {
              "date": "2026-06-22",
              "value": 166.0
            },
            {
              "date": "2026-06-23",
              "value": 134.0
            },
            {
              "date": "2026-06-24",
              "value": 167.0
            },
            {
              "date": "2026-06-25",
              "value": 189.0
            },
            {
              "date": "2026-06-29",
              "value": 171.0
            },
            {
              "date": "2026-06-30",
              "value": 80.0
            },
            {
              "date": "2026-07-01",
              "value": 72.0
            },
            {
              "date": "2026-07-02",
              "value": 170.0
            }
          ],
          "y_axis": "y"
        }
      ],
      "data_source": "SQLite engineered_series_ts.TREASURY_COMBINED_SUPPLY（由 treasury_auctions_ts 工程聚合后落表）",
      "note": "统计所有类型美债的当日发行规模；未公告规模不当作零。该图专用窗口：前20日 + 后10日。"
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
              "date": "2025-06-05",
              "value": 143.35
            },
            {
              "date": "2025-06-06",
              "value": 143.91
            },
            {
              "date": "2025-06-09",
              "value": 144.13
            },
            {
              "date": "2025-06-10",
              "value": 144.75
            },
            {
              "date": "2025-06-11",
              "value": 145.13
            },
            {
              "date": "2025-06-12",
              "value": 143.88
            },
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
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "JPY_CALL",
          "label": "JPY隔夜融资成本",
          "points": [
            {
              "date": "2025-06-05",
              "value": 0.477
            },
            {
              "date": "2025-06-06",
              "value": 0.477
            },
            {
              "date": "2025-06-09",
              "value": 0.477
            },
            {
              "date": "2025-06-10",
              "value": 0.477
            },
            {
              "date": "2025-06-11",
              "value": 0.477
            },
            {
              "date": "2025-06-12",
              "value": 0.481
            },
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
              "date": "2025-05-07",
              "value": 0.609
            },
            {
              "date": "2025-05-08",
              "value": 0.619
            },
            {
              "date": "2025-05-09",
              "value": 0.634
            },
            {
              "date": "2025-05-12",
              "value": 0.66
            },
            {
              "date": "2025-05-13",
              "value": 0.718
            },
            {
              "date": "2025-05-14",
              "value": 0.706
            },
            {
              "date": "2025-05-15",
              "value": 0.717
            },
            {
              "date": "2025-05-16",
              "value": 0.707
            },
            {
              "date": "2025-05-19",
              "value": 0.718
            },
            {
              "date": "2025-05-20",
              "value": 0.728
            },
            {
              "date": "2025-05-21",
              "value": 0.72
            },
            {
              "date": "2025-05-22",
              "value": 0.737
            },
            {
              "date": "2025-05-23",
              "value": 0.731
            },
            {
              "date": "2025-05-26",
              "value": 0.728
            },
            {
              "date": "2025-05-27",
              "value": 0.739
            },
            {
              "date": "2025-05-28",
              "value": 0.753
            },
            {
              "date": "2025-05-29",
              "value": 0.758
            },
            {
              "date": "2025-05-30",
              "value": 0.75
            },
            {
              "date": "2025-06-02",
              "value": 0.755
            },
            {
              "date": "2025-06-03",
              "value": 0.755
            },
            {
              "date": "2025-06-04",
              "value": 0.765
            },
            {
              "date": "2025-06-05",
              "value": 0.755
            },
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
            }
          ]
        },
        {
          "id": "JGB10",
          "label": "JGB 10Y",
          "points": [
            {
              "date": "2025-05-07",
              "value": 1.318
            },
            {
              "date": "2025-05-08",
              "value": 1.343
            },
            {
              "date": "2025-05-09",
              "value": 1.37
            },
            {
              "date": "2025-05-12",
              "value": 1.405
            },
            {
              "date": "2025-05-13",
              "value": 1.46
            },
            {
              "date": "2025-05-14",
              "value": 1.466
            },
            {
              "date": "2025-05-15",
              "value": 1.489
            },
            {
              "date": "2025-05-16",
              "value": 1.466
            },
            {
              "date": "2025-05-19",
              "value": 1.494
            },
            {
              "date": "2025-05-20",
              "value": 1.53
            },
            {
              "date": "2025-05-21",
              "value": 1.53
            },
            {
              "date": "2025-05-22",
              "value": 1.573
            },
            {
              "date": "2025-05-23",
              "value": 1.559
            },
            {
              "date": "2025-05-26",
              "value": 1.522
            },
            {
              "date": "2025-05-27",
              "value": 1.479
            },
            {
              "date": "2025-05-28",
              "value": 1.531
            },
            {
              "date": "2025-05-29",
              "value": 1.532
            },
            {
              "date": "2025-05-30",
              "value": 1.518
            },
            {
              "date": "2025-06-02",
              "value": 1.523
            },
            {
              "date": "2025-06-03",
              "value": 1.499
            },
            {
              "date": "2025-06-04",
              "value": 1.518
            },
            {
              "date": "2025-06-05",
              "value": 1.481
            },
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
            }
          ]
        },
        {
          "id": "JGB30",
          "label": "JGB 30Y",
          "points": [
            {
              "date": "2025-05-07",
              "value": 2.791
            },
            {
              "date": "2025-05-08",
              "value": 2.779
            },
            {
              "date": "2025-05-09",
              "value": 2.802
            },
            {
              "date": "2025-05-12",
              "value": 2.836
            },
            {
              "date": "2025-05-13",
              "value": 2.779
            },
            {
              "date": "2025-05-14",
              "value": 2.811
            },
            {
              "date": "2025-05-15",
              "value": 2.839
            },
            {
              "date": "2025-05-16",
              "value": 2.84
            },
            {
              "date": "2025-05-19",
              "value": 2.851
            },
            {
              "date": "2025-05-20",
              "value": 2.969
            },
            {
              "date": "2025-05-21",
              "value": 2.976
            },
            {
              "date": "2025-05-22",
              "value": 2.999
            },
            {
              "date": "2025-05-23",
              "value": 2.925
            },
            {
              "date": "2025-05-26",
              "value": 2.9
            },
            {
              "date": "2025-05-27",
              "value": 2.743
            },
            {
              "date": "2025-05-28",
              "value": 2.796
            },
            {
              "date": "2025-05-29",
              "value": 2.853
            },
            {
              "date": "2025-05-30",
              "value": 2.846
            },
            {
              "date": "2025-06-02",
              "value": 2.821
            },
            {
              "date": "2025-06-03",
              "value": 2.825
            },
            {
              "date": "2025-06-04",
              "value": 2.833
            },
            {
              "date": "2025-06-05",
              "value": 2.787
            },
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
              "date": "2025-06-13",
              "value": 322.40000000000003
            },
            {
              "date": "2025-06-16",
              "value": 321.20000000000005
            },
            {
              "date": "2025-06-17",
              "value": 317.09999999999997
            },
            {
              "date": "2025-06-18",
              "value": 318.5
            },
            {
              "date": "2025-06-20",
              "value": 317.2
            },
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
              "value": 265.7
            },
            {
              "date": "2026-06-02",
              "value": 265.7
            },
            {
              "date": "2026-06-03",
              "value": 268.70000000000005
            },
            {
              "date": "2026-06-04",
              "value": 265.7
            },
            {
              "date": "2026-06-05",
              "value": 277.7
            },
            {
              "date": "2026-06-08",
              "value": 275.70000000000005
            },
            {
              "date": "2026-06-09",
              "value": 273.7
            },
            {
              "date": "2026-06-10",
              "value": 273.7
            },
            {
              "date": "2026-06-11",
              "value": 265.7
            },
            {
              "date": "2026-06-12",
              "value": 269.7
            },
            {
              "date": "2026-06-15",
              "value": 267.70000000000005
            },
            {
              "date": "2026-06-16",
              "value": 265.7
            },
            {
              "date": "2026-06-17",
              "value": 280.70000000000005
            },
            {
              "date": "2026-06-18",
              "value": 279.70000000000005
            },
            {
              "date": "2026-06-22",
              "value": 284.70000000000005
            },
            {
              "date": "2026-06-23",
              "value": 276.70000000000005
            },
            {
              "date": "2026-06-24",
              "value": 271.70000000000005
            },
            {
              "date": "2026-06-25",
              "value": 269.7
            },
            {
              "date": "2026-06-26",
              "value": 267.70000000000005
            },
            {
              "date": "2026-06-29",
              "value": 270.7
            }
          ]
        },
        {
          "id": "US_JP_10Y",
          "label": "10Y UST-JGB",
          "points": [
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
              "value": 181.29999999999998
            },
            {
              "date": "2026-06-02",
              "value": 180.29999999999998
            },
            {
              "date": "2026-06-03",
              "value": 183.3
            },
            {
              "date": "2026-06-04",
              "value": 181.29999999999998
            },
            {
              "date": "2026-06-05",
              "value": 189.29999999999998
            },
            {
              "date": "2026-06-08",
              "value": 190.29999999999995
            },
            {
              "date": "2026-06-09",
              "value": 187.3
            },
            {
              "date": "2026-06-10",
              "value": 189.29999999999998
            },
            {
              "date": "2026-06-11",
              "value": 179.3
            },
            {
              "date": "2026-06-12",
              "value": 182.30000000000004
            },
            {
              "date": "2026-06-15",
              "value": 181.29999999999998
            },
            {
              "date": "2026-06-16",
              "value": 177.29999999999995
            },
            {
              "date": "2026-06-17",
              "value": 183.3
            },
            {
              "date": "2026-06-18",
              "value": 180.29999999999998
            },
            {
              "date": "2026-06-22",
              "value": 185.29999999999998
            },
            {
              "date": "2026-06-23",
              "value": 184.3
            },
            {
              "date": "2026-06-24",
              "value": 175.3
            },
            {
              "date": "2026-06-25",
              "value": 174.30000000000004
            },
            {
              "date": "2026-06-26",
              "value": 172.29999999999998
            },
            {
              "date": "2026-06-29",
              "value": 172.29999999999998
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
              "date": "2026-07-01",
              "value": 72.0
            },
            {
              "date": "2026-07-02",
              "value": 170.0
            }
          ],
          "y_axis": "y"
        },
        {
          "id": "UPCOMING_TOTAL_TREASURY_SUPPLY",
          "label": "Upcoming Total Treasury Supply（未来已公告美债发行总额）",
          "points": [
            {
              "date": "2026-07-01",
              "value": 72.0
            },
            {
              "date": "2026-07-02",
              "value": 170.0
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
    "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/output/usd_liquidity_chart_7d_20260701_081545.svg",
    "/Users/eiheisun/WorkBuddy/2026-05-04-task-1/output/usd_liquidity_chart_30d_20260701_081545.svg"
  ],
  "data_quality": {
    "missing": [],
    "stale": [],
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
    "generated_at_bjt": "2026-07-01 08:16:07 UTC+08:00",
    "data_as_of": "2026-06-30",
    "model": "AI Agent",
    "input_freshness_note": "核心日频指标截至2026-06-30（RRP）和2026-06-29（SOFR/收益率/VIX等）；周频指标WRESBAL和SOMA截至2026-06-24；NFCI截至2026-06-19；T-bill拍卖数据截至2026-06-25；未来拍卖日程已更新至2026-08-30。"
  },
  "stance": {
    "label": "中性偏松",
    "confidence": "中等",
    "score_text": "TGA下降释放流动性，金融条件偏松（NFCI -0.516），SOFR融资压力不大（SOFR-ANCHOR -3bp）；但RRP缓冲垫极低（26.9bn）和准备金周频下降（-82bn）构成中期风险，整体偏松但需警惕流动性边际收紧。",
    "one_liner": "美元流动性总体偏松，TGA释放和稳定融资条件支撑风险资产，但RRP缓冲垫几乎耗尽是中期隐患。"
  },
  "key_takeaways": [
    {
      "title": "TGA下降释放财政资金，短期流动性偏松",
      "text": "TGA余额876.96bn，日变化-18.62bn（2026-06-29），财政资金释放为银行体系注入流动性，短期偏松。未来拍卖日程显示7月1-2日将有242bn T-bill发行，需关注后续TGA回补压力。",
      "evidence": [
        "TGA日变化-18.62bn（2026-06-29，日频T+1），上一期+24.11bn（2026-06-26），边际变化-42.72bn，财政资金释放",
        "未来7月1日17-Week Bill 72bn、7月2日4-Week+8-Week Bill共170bn，合计242bn短期供给",
        "TGA余额876.96bn仍高于历史低位，短期释放不代表趋势反转"
      ],
      "related_indicators": [
        "TGA",
        "TGA_FLOW",
        "TBILL_AUCTION_SIZE"
      ]
    },
    {
      "title": "回购融资条件稳定，SOFR相对政策锚偏离有限",
      "text": "SOFR 3.62%，与IORB（3.65%）利差仅-3bp，回购融资价格贴近政策锚，抵押融资压力不大。SOFR交易量3126bn，价格×交易量影响约-2.6mn/day，冲击有限。",
      "evidence": [
        "SOFR-IORB = -3.0bp（2026-06-29，日频），上一期-3.0bp（2026-06-26），边际变化0.0bp，回购融资稳定",
        "SOFR_VOLUME_IMPACT = -2.6mn/day（2026-06-29），SOFR交易量3126bn，价格偏离有限且交易量正常",
        "BGCR-TGCR = 0.0bp，三方回购与一般抵押品利率结构稳定，无抵押品稀缺迹象"
      ],
      "related_indicators": [
        "SOFR",
        "IORB",
        "SOFR_ANCHOR",
        "SOFR_VOLUME_IMPACT",
        "BGCR_TGCR"
      ]
    },
    {
      "title": "美债收益率曲线正常，长端稳定，金融条件偏松",
      "text": "1Y/3Y/10Y收益率分别为3.97%/4.10%/4.38%，曲线斜率为正（10Y-2Y=30bp，10Y-3M=57bp），长端收益率边际变化为0，利率环境稳定。NFCI -0.516显示金融条件偏松，VIX 17.65较前期18.41回落，风险偏好稳定。",
      "evidence": [
        "10Y Treasury Yield 4.38%（2026-06-29），上一期4.38%，边际变化0.0bp，长端锚稳定",
        "10Y-2Y = 30bp，10Y-3M = 57bp，曲线为正且边际走陡（+2bp/+6bp），无衰退定价",
        "NFCI = -0.516（2026-06-19，周频），金融条件偏松；VIX 17.65（2026-06-29），较上一期18.41回落0.76pt"
      ],
      "related_indicators": [
        "DGS10",
        "DGS1",
        "DGS3",
        "T10Y2Y",
        "T10Y3M",
        "NFCI",
        "VIXCLS"
      ]
    }
  ],
  "risk_flags": [
    {
      "priority": "P1",
      "severity": "medium",
      "type": "market",
      "title": "RRP缓冲垫几乎耗尽，未来冲击吸收能力受限",
      "text": "RRP余额仅26.9bn（2026-06-30），较上一期3.55bn上升23.35bn，缓冲垫存量极低。RRP边际流量为正（+23.35bn）代表资金回到联储停车场，短期偏不利风险资产；更关键的是存量缓冲垫接近耗尽，未来TGA补库、QT或美债供给冲击将更容易直接打到准备金，加剧银行间融资压力。",
      "evidence": [
        "RRP_BUFFER = 26.9bn（2026-06-30，日频），上一期3.55bn，边际变化+23.35bn，缓冲垫极低",
        "RRP_FLOW = +23.35bn（2026-06-30），资金回流联储停车场，短期偏紧",
        "准备金WRESBAL 2951.4bn（2026-06-24，周频），较上一期3033.4bn下降82bn，周频降幅较大"
      ],
      "related_indicators": [
        "RRPONTSYD",
        "RRP_FLOW",
        "RRP_BUFFER",
        "WRESBAL"
      ]
    },
    {
      "priority": "P2",
      "severity": "low",
      "type": "market",
      "title": "准备金周频下降82bn，需关注持续性",
      "text": "银行准备金余额2951.4bn（2026-06-24），周度下降82bn，绝对水平仍高，暂不构成即时压力。但结合RRP缓冲垫耗尽背景，若准备金持续下降，银行间融资价格可能面临上行压力。",
      "evidence": [
        "WRESBAL = 2951.4bn（2026-06-24，周频），上一期3033.4bn（2026-06-17），周度变化-82bn",
        "准备金/GDP比率仍高于2019年9月Repo Crisis前低位，但边际方向需持续监控",
        "SOMA 6344bn（2026-06-24），QT持续缩表背景下准备金长期趋降"
      ],
      "related_indicators": [
        "WRESBAL",
        "SOMA"
      ]
    },
    {
      "priority": "P2",
      "severity": "info",
      "type": "data",
      "title": "JPY Carry数据缺失，无法评估日元carry对风险资产资金供给的影响",
      "text": "jpy_carry_history为空，无法获取美日利差、USD/JPY、CFTC日元仓位等叠加判断数据。若日元快速升值或BOJ意外加息，可能导致carry trade平仓并冲击美股流动性，当前无法评估该风险。",
      "evidence": [
        "jpy_carry_history.history.length = 0，数据缺失",
        "需BOJ政策利率、10Y JGB、USD/JPY历史、CFTC JPY仓位等数据才能评估",
        "建议检查jpy_carry.py脚本状态和API可用性"
      ],
      "related_indicators": [
        "JPY_CARRY"
      ]
    }
  ],
  "narrative_blocks": {
    "summary": "美元流动性总体偏松。TGA下降释放财政资金，SOFR融资价格稳定（SOFR-IORB仅-3bp），美债收益率曲线正常且长端锚定，NFCI显示金融条件偏松，VIX回落至17.65。主要风险来自RRP缓冲垫几乎耗尽（26.9bn）和准备金周频下降82bn，未来TGA补库或美债供给冲击可能更直接地影响准备金水位。短期风险资产流动性支撑仍在，但中期需警惕流动性边际收紧。",
    "rates": "政策锚IORB 3.65%维持不变，SOFR 3.62%贴近政策锚，EFFR 3.63%和OBFR 3.62%均低于IORB，银行间无抵押融资无压力。回购市场BGCR/TGCR均与政策锚一致，抵押融资结构稳定。CP Rate-Policy Upper Proxy -3.0bp，企业短融压力不明显。",
    "balance_sheet": "Fed负债端TGA 877.0bn（日变化-18.6bn）释放流动性；RRP 26.9bn边际上升23.4bn但存量缓冲垫极低；SOMA 6344.3bn反映QT持续背景。银行准备金2951.4bn，周度下降82bn，绝对水平尚高但边际方向偏紧。负债端总体释放流动性，但缓冲垫不足是中期风险。",
    "market_transmission": "信用市场HY OAS 2.80%（边际-3bp）、IG OAS 0.76%（边际-1bp），信用利差稳定略收窄，融资风险溢价未扩大。VIX 17.65较前期回落，风险偏好稳定。NFCI -0.516显示金融条件偏松。离岸美元DTWEXBGS 120.89，美元指数小幅回落，离岸美元融资条件无异常。",
    "treasury_yields": {
      "label": "中性",
      "one_liner": "1Y/3Y/10Y收益率3.97%/4.10%/4.38%，曲线斜率为正，长端锚定，收益率环境对风险资产友好。",
      "analysis": "1Y Treasury Yield 3.97%，较上一期3.94%小幅上行3bp，反映短端政策路径稳定，现金收益率对风险资产的分流效应有限。3Y Treasury Yield 4.10%，与1Y利差仅13bp，中段再定价压力不大。10Y Treasury Yield 4.38%，边际变化0bp，长期名义折现率锚定，对久期资产、成长股和黄金的估值压力未增强。10Y-2Y利差30bp、10Y-3M利差57bp，曲线为正且边际走陡，无衰退定价。整体收益率环境稳定，对风险资产偏友好。"
    },
    "jpy_carry": {
      "label": "数据缺失",
      "one_liner": "JPY Carry数据缺失，无法评估借日元买美元资产资金的边际供给情况。",
      "analysis": "jpy_carry_history数据为空，无法获取美日短端利差、USD/JPY汇率、JGB收益率、CFTC日元仓位等关键变量，本次分析无法覆盖日元carry trade对美股/美元风险资产流动性供给的叠加影响。若后续BOJ加息预期上升或USD/JPY快速下跌，可能触发carry平仓并冲击美元风险资产流动性，建议补充JPY carry数据后再做综合判断。"
    }
  }
};
