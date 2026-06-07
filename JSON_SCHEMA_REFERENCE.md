# JSON Schema Reference for Frontend

## dashboard_data.json Structure

### Top-Level Keys (Required)
```
{
  "meta": {...},                          // Metadata
  "status_scale": {...},                  // Status scale definition
  "trading_dashboard": {...},             // Core/confirm/background metrics
  "jpy_carry": {...},                     // JPY carry risk data
  "indicator_groups": [...],              // Indicator tables
  "derived_signals": [...],               // Pre-calculated spreads and scale signals
  "charts": [...],                        // Chart data for rendering
  "data_quality": {...}                   // Data quality tracking
}
```

### meta (Required)
```json
{
  "title": "美元流动性监测",
  "trigger": "更新数据并分析",
  "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
  "data_as_of": "2026-05-26",
  "timezone": "BJT",
  "theme": "warm_claude",
  "version": "1.0"
}
```

### status_scale (Required)
```json
{
  "values": [
    "宽松",
    "中性偏松", 
    "中性",
    "中性偏紧",
    "紧张"
  ],
  "current_from_rule": "中性",
  "score_from_rule": 1.0
}
```

### trading_dashboard.core (Required - Array of Metrics)
```json
[
  {
    "type": "signal|metric",
    "id": "SOFR_ANCHOR",
    "label": "SOFR-IORB（担保隔夜融资利率-准备金余额利率）",
    "priority": "P0|P1",
    "value_text": "-10.0bp",
    "previous_text": "-14.0bp",
    "change_text": "+4.0bp",
    "severity": "宽松|偏松|中性|偏紧|紧张",
    "why": "回购融资是否高于政策锚",
    "interpretation": "SOFR相对IORB（准备金余额利率）的位置。回购融资低于政策锚，说明资金面不紧",
    "as_of": "2026-05-26",           // Optional for signals
    "frequency": "daily|weekly"      // Optional
  }
]
```

Quantity-aware core signals now include:

- `SOFR_VOLUME_IMPACT`: signal item, `unit = "USD mn/day"`, rough daily funding-cost magnitude from SOFR-policy spread × SOFR transaction volume.
- `SOFR_VOLUME`: metric item, `unit = "USD bn"`, SOFR transaction volume from NY Fed.
- `TBILL_AUCTION_ABSORPTION`: signal item, `unit = "USD bn"`, T-bill supply absorption diagnosis combining issue size and bid-to-cover.
- `TBILL_AUCTION_SIZE`: metric item, `unit = "USD bn"`, latest T-bill auction-day offering amount aggregate.
- `TBILL_AUCTION_BTC`: metric item, `unit = "ratio"`, offering-amount-weighted bid-to-cover.

### jpy_carry (Required Structure)
```json
{
  "meta": {
    "lookback": "180 days|1Y"
  },
  "risk": {
    "label": "中性|偏高|中性偏高",
    "score": 2.5,
    "reasons": [
      "理由1",
      "理由2"
    ]
  },
  "cards": [
    {
      "label": "JPY LIBOR",
      "id": "jpy_libor",
      "as_of": "2026-05-26",
      "value_text": "0.15%",
      "change_text": "+0.05%",
      "why": "解释文本"
    }
  ],
  "sources": [
    {
      "name": "BOJ",
      "items": ["item1", "item2"]
    }
  ]
}
```

### indicator_groups (Required - Array)
```json
[
  {
    "title": "Fed 负债端",
    "indicators": [
      {
        "id": "TGA",
        "label": "TGA (财政部一般账户)",
        "value_text": "785.9bn",
        "previous": 782.0,
        "unit": "USD bn",
        "change_text": "+3.9bn",
        "change_direction": "up|down|unknown",
        "as_of": "2026-05-21",
        "frequency": "daily|weekly|monthly",
        "comparison_basis": "前日|周环比|月环比",
        "freshness": "ok|stale|missing",
        "meaning": "Optional description",
        "status": "ok|warning|error"
      }
    ]
  }
]
```

### charts (Required - Array)
```json
[
  {
    "id": "sofr_iorb_1w",
    "title": "SOFR vs IORB (1周)",
    "unit": "bp|%|USD bn",
    "dual_axis": false,
    "y_axes": {
      "y": "bp",
      "y1": "Optional second axis label"
    },
    "series": [
      {
        "label": "SOFR",
        "y_axis": "y|y1",  // Default: "y"
        "points": [
          { "date": "2026-05-20", "value": -12.0 },
          { "date": "2026-05-21", "value": -10.5 }
        ]
      }
    ]
  }
]
```

### data_quality (Required - Can be empty)
```json
{
  "missing": [
    {
      "id": "some_indicator",
      "label": "Missing Indicator",
      "reason": "API timeout"
    }
  ],
  "stale": [
    {
      "id": "WRESBAL",
      "label": "Bank Reserves",
      "reason": "Weekly data"
    }
  ],
  "degraded_sources": [
    {
      "id": "alt_data",
      "label": "Alternative Source",
      "reason": "Primary failed"
    }
  ]
}
```

---

## analysis.json Structure

### Top-Level Keys (Required)
```json
{
  "meta": {...},
  "stance": {...},
  "key_takeaways": [...],
  "risk_flags": [...],
  "narrative_blocks": {...}
}
```

### meta (Required)
```json
{
  "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
  "data_as_of": "2026-05-26",
  "model": "Claude 3.5 Sonnet or similar",
  "input_freshness_note": "All daily metrics as of 2026-05-22, weekly metrics as of 2026-05-20"
}
```

### stance (Required)
```json
{
  "label": "宽松|中性偏松|中性|中性偏紧|紧张",
  "confidence": "高|中等|低",
  "score_text": "Rule score: 1.0; inferred from Fed liability dynamics",
  "one_liner": "SOFR相对IORB低4bp，回购融资不紧；但RRP接近低位，后续缓冲能力有限。"
}
```

### key_takeaways (Required - Array, 0-5 items)
```json
[
  {
    "title": "SOFR-IORB 回购融资不紧",
    "text": "SOFR-IORB从-14bp升至-10bp（+4bp），仍显示回购融资低于政策锚，资金面边际偏松。",
    "related_indicators": ["SOFR_ANCHOR", "SOFR", "IORB"]
  }
]
```

### risk_flags (Required - Array, 0-5 items, sorted by priority)
```json
[
  {
    "priority": "P0|P1|P2",
    "severity": "high|medium|low|info",
    "type": "market|data",
    "title": "RRP 缓冲垫耗尽风险",
    "text": "RRP余额已跌至0.96bn低位，若TGA继续补库或美联储继续QT，后续冲击更容易直接打到准备金，风险集中在准备金边际稀缺。",
    "evidence": [
      "RRP从3.28bn跌至0.96bn (5/21-5/22)",
      "RRP 3个月均值：约50bn，当前仅占2%",
      "TGA上升3.9bn可能持续补库"
    ],
    "related_indicators": ["RRPONTSYD", "TGA"]
  }
]
```

### narrative_blocks (Optional - Can be omitted)
```json
{
  "summary": "Today's liquidity backdrop: SOFR financing costs remain below IORB...",
  "rates": "1Y UST yield rose 4bp to 3.83%...",
  "balance_sheet": "TGA rose 3.9bn to 785.9bn...",
  "market_transmission": "SOFR-IORB still negative (policy accommodative)..."
}
```

---

## model_input.json Structure (NOT USED BY FRONTEND)

This file is for backend LLM analysis only. Frontend doesn't read it.

### Top-Level Keys
```json
{
  "task": "Task description",
  "trigger": "更新数据并分析",
  "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
  "intro_document": "# 美元流动性框架介绍\n\n...",
  "analysis_prompt": "【衍生信号强制取值表...】\n...",
  "data": {
    "stance_by_rule_fallback": "中性",
    "score_by_rule_fallback": 1.0,
    "highlights_by_rule_fallback": [...],
    "metrics": [...],
    "derived_signals": [...],
    "quantity_metrics_required": ["SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"],
    "quantity_signals_required": ["SOFR_VOLUME_IMPACT", "TBILL_AUCTION_ABSORPTION"],
    "indicator_groups": [...],
    "charts": [...]
  },
  "output_contract": {...}
}
```

---

## Validation Checklist

### dashboard_data.json
- [ ] meta.generated_at_bjt is valid datetime string (ISO 8601 or "YYYY-MM-DD HH:MM:SS UTC+08:00")
- [ ] meta.data_as_of is valid date string (YYYY-MM-DD)
- [ ] status_scale.values has exactly 5 items
- [ ] status_scale.current_from_rule is one of the 5 values
- [ ] trading_dashboard.core has at least 1 item
- [ ] Each core item has: id, label, value_text, severity, why
- [ ] Quantity fields are present when sources are available: SOFR_VOLUME, TBILL_AUCTION_SIZE, TBILL_AUCTION_BTC, SOFR_VOLUME_IMPACT, TBILL_AUCTION_ABSORPTION
- [ ] T-bill analysis never uses bid-to-cover without also exposing issuance size
- [ ] jpy_carry.risk exists with label and score
- [ ] jpy_carry.cards is array with at least 1 item
- [ ] indicator_groups is array with at least 1 group
- [ ] Each indicator has: id, label, value_text, as_of, frequency
- [ ] charts is array with at least 1 chart
- [ ] Each chart has: id, title, series with points
- [ ] data_quality has keys: missing, stale, degraded_sources

### analysis.json
- [ ] meta.generated_at_bjt matches dashboard_data
- [ ] stance.label is one of exactly: 宽松, 中性偏松, 中性, 中性偏紧, 紧张
- [ ] stance.confidence is one of: 高, 中等, 低
- [ ] stance.one_liner is 1-2 sentences
- [ ] key_takeaways is array of 0-5 items
- [ ] Each takeaway has: title, text, related_indicators
- [ ] risk_flags is array of 0-5 items
- [ ] risk_flags sorted by priority (P0, then P1, then P2)
- [ ] Each flag has: priority, severity, type, title, text, evidence
- [ ] severity is one of: high, medium, low, info
- [ ] type is one of: market, data
- [ ] evidence is array of at least 1 item
- [ ] If a risk/takeaway discusses SOFR/repo pressure, evidence mentions SOFR_VOLUME or SOFR_VOLUME_IMPACT
- [ ] If a risk/takeaway discusses T-bill/Treasury auction absorption, evidence mentions both TBILL_AUCTION_SIZE and TBILL_AUCTION_BTC or cites TBILL_AUCTION_ABSORPTION

---

## Common Rendering Issues

### 1. Missing status_scale.values
**Error**: Status pills don't render or show "undefined"
**Fix**: Ensure status_scale.values is exactly 5 items: ["宽松", "中性偏松", "中性", "中性偏紧", "紧张"]

### 2. Missing severity field
**Error**: Radar items don't color-code
**Fix**: Ensure every trading_dashboard item has severity field

### 3. Chart points not showing
**Error**: Canvas renders but no data points visible
**Fix**: Ensure series.points has objects with {date, value}; dates must be unique

### 4. Stance label mismatch
**Error**: Status pill doesn't light up or shows "unknown"
**Fix**: Ensure analysis.stance.label exactly matches one value in dashboard_data.status_scale.values

### 5. Risk flags don't sort correctly
**Error**: P2 items appear before P0
**Fix**: Sort risk_flags array by priority before output; order: P0, P1, P2

---

## File Size Reference

| File | Size | Compression |
|------|------|-------------|
| dashboard_data.json | 210-260 KB | ~20% gzip |
| analysis.json | 4-6 KB | ~50% gzip |
| model_input.json | 200-300 KB | ~10% gzip |
| data.js | 200-220 KB | Embedded |

