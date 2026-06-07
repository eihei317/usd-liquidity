# Frontend & Output Structure Analysis
## USD Liquidity Monitor Dashboard

Generated: 2026-05-27

---

## 1. FRONTEND ARCHITECTURE

### Location
- **Frontend root**: `/Users/eiheisun/WorkBuddy/2026-05-04-task-1/frontend/usd-liquidity-monitor/`

### Key Files
```
frontend/usd-liquidity-monitor/
├── index.html           # Main HTML template (114 lines)
├── app.js              # Main React-like app logic (438 lines)
├── data.js             # Fallback data preload (216KB)
├── styles.css          # Styling (12.4KB)
└── chart.min.js        # Chart.js library (205KB)
```

### Data Loading Strategy (app.js, lines 1-4)

The frontend uses **relative paths** with a fallback mechanism:

```javascript
const DATA_URLS = {
  dashboard: "../../output/latest/dashboard_data.json",
  analysis: "../../output/latest/analysis.json"
};
```

**Path Assumption**: The app is served from project root and reads `output/latest/` as the single source of truth.

### Current Path Strategy
- `app.js` loads: `../../output/latest/dashboard_data.json` and `../../output/latest/analysis.json`
- These files are produced by `scripts/run.py` on every pipeline run.
- If fetch fails, the browser falls back to `window.DASHBOARD_DATA` and `window.ANALYSIS_DATA` from `data.js`.

### data.js Role

`data.js` (216KB) serves as **fallback embedded data**:

```javascript
window.DASHBOARD_DATA = { ... };  // Preloaded dashboard data
window.ANALYSIS_DATA = { ... };    // Preloaded analysis data (inferred)
```

**When it's used** (app.js, lines 410-423):
```javascript
let dashboard;
try {
  dashboard = await loadJson(DATA_URLS.dashboard);  // Try fetch first
} catch (e) {
  dashboard = window.DASHBOARD_DATA || {};  // Fall back to preload
}

let analysis;
try {
  analysis = await loadJson(DATA_URLS.analysis);
} catch (e) {
  analysis = window.ANALYSIS_DATA || {};
}
```

**Frequency**: `data.js` is regenerated with each pipeline run and should be treated as fallback, not the primary data source.

---

## 2. DATA FLOW: JSON STRUCTURE

### 2a. dashboard_data.json (211KB)
**Purpose**: Provides all visual/UI data for the dashboard

**Top-level schema**:
```json
{
  "meta": {
    "title": "美元流动性监测",
    "trigger": "更新数据并分析",
    "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
    "data_as_of": "2026-05-26",
    "timezone": "BJT",
    "theme": "warm_claude",
    "version": "1.0"
  },
  "status_scale": {
    "values": ["宽松", "中性偏松", "中性", "中性偏紧", "紧张"],
    "current_from_rule": "中性",
    "score_from_rule": 1.0
  },
  "trading_dashboard": {
    "core": [
      { "type": "signal|metric", "id": "SOFR_ANCHOR", "label": "...", "priority": "P0|P1", 
        "value_text": "-10.0bp", "previous_text": "-14.0bp", "change_text": "+4.0bp",
        "severity": "宽松|偏松|中性|偏紧|紧张", "why": "...", "interpretation": "..." }
      // ... more core items
    ],
    "confirm": [ /* secondary indicators */ ],
    "background": [ /* background data */ ],
    "core_chart_ids": ["chart_id_1", "chart_id_2"],
    "chart_groups": [ 
      { "id": "core", "title": "核心图表", "chart_ids": [...], "default_open": true }
    ]
  },
  "jpy_carry": {
    "meta": { "lookback": "..." },
    "risk": { "label": "...", "score": 2.5, "reasons": [...] },
    "cards": [
      { "label": "JPY LIBOR", "id": "jpy_libor", "as_of": "2026-05-26",
        "value_text": "0.15%", "change_text": "+0.05%", "why": "..." }
    ],
    "sources": [ { "name": "BOJ", "items": [...] } ]
  },
  "indicator_groups": [
    {
      "title": "Fed 负债端",
      "indicators": [
        { "id": "TGA", "label": "TGA (财政部一般账户)", "value_text": "785.9bn",
          "previous": 782.0, "unit": "USD bn", "change_text": "+3.9bn",
          "change_direction": "up", "as_of": "2026-05-21", "frequency": "daily",
          "comparison_basis": "前日", "freshness": "ok" }
      ]
    }
  ],
  "derived_signals": [
    { "id": "SOFR_ANCHOR", "label": "SOFR-IORB", "value": -10.0, "previous": -14.0,
      "change": 4.0, "unit": "bp" },
    { "id": "SOFR_VOLUME_IMPACT", "label": "SOFR价格×交易量影响", "value": -8.6,
      "previous": -12.0, "change": 3.4, "unit": "USD mn/day" },
    { "id": "TBILL_AUCTION_ABSORPTION", "label": "T-bill拍卖吸收压力", "value": 220.0,
      "previous": 69.0, "change": 151.0, "unit": "USD bn" }
  ],
  "core_indicator_impacts": [
    { "indicator_id": "TGA", "impact": "SOFR_ANCHOR", "relationship": "positive" }
  ],
  "charts": [
    { "id": "sofr_iorb_1w", "title": "SOFR vs IORB (1周)", "unit": "bp",
      "series": [
        { "label": "SOFR", "points": [
          { "date": "2026-05-20", "value": -12.0 },
          { "date": "2026-05-21", "value": -10.5 }
        ]},
        { "label": "IORB", "points": [...] }
      ],
      "dual_axis": false, "y_axes": { "y": "bp" }
    }
  ],
  "chart_paths": {
    "core": ["sofr_iorb_1w", "tga_1m"]
  },
  "data_quality": {
    "missing": [
      { "id": "some_indicator", "label": "Missing Indicator", "reason": "API timeout" }
    ],
    "stale": [
      { "id": "WRESBAL", "label": "Bank Reserves", "reason": "Weekly data" }
    ],
    "degraded_sources": [
      { "id": "alt_data", "label": "Alternative Source", "reason": "Primary failed" }
    ]
  }
}
```

**Expected fields for app.js rendering**:
- `meta.generated_at_bjt`, `meta.data_as_of` → Header timestamp display
- `meta.trigger` → Optional trigger note
- `status_scale.values`, `status_scale.current_from_rule` → Status scale chips
- `trading_dashboard.core` → P0/P1 radar items, including quantity-aware SOFR impact when available
- `trading_dashboard.core_chart_ids` → Chart ordering
- `jpy_carry` → JPY Carry card rendering
- `indicator_groups[]` → Indicator table rendering
- `charts[]` → Chart canvas rendering (with Chart.js)
- `data_quality` → Missing/stale/degraded data display

---

### 2b. analysis.json (5KB)
**Purpose**: Provides LLM-generated insight and trend analysis

**Top-level schema**:
```json
{
  "meta": {
    "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
    "data_as_of": "2026-05-26",
    "model": "Claude 3.5 Sonnet or similar",
    "input_freshness_note": "All daily metrics as of 2026-05-22, weekly metrics as of 2026-05-20"
  },
  "stance": {
    "label": "中性",  // Must be one of: 宽松, 中性偏松, 中性, 中性偏紧, 紧张
    "confidence": "中等",
    "score_text": "Rule score: 1.0; inferred from Fed liability dynamics",
    "one_liner": "SOFR相对IORB低4bp，回购融资不紧；但RRP接近低位，后续缓冲能力有限。"
  },
  "key_takeaways": [
    {
      "title": "SOFR-IORB 回购融资不紧",
      "text": "SOFR-IORB从-14bp升至-10bp（+4bp），仍显示回购融资低于政策锚，资金面边际偏松。",
      "related_indicators": ["SOFR_ANCHOR", "SOFR", "IORB"]
    },
    {
      "title": "RRP缓冲垫接近高风险低位",
      "text": "RRP余额从3.28bn跌至0.96bn（-2.32bn），绝对水平仅1bn，未来冲击直接打到准备金的空间有限。",
      "related_indicators": ["RRPONTSYD"]
    }
  ],
  "risk_flags": [
    {
      "priority": "P0",
      "severity": "high",
      "type": "market",  // or "data"
      "title": "RRP 缓冲垫耗尽风险",
      "text": "RRP余额已跌至0.96bn低位，若TGA继续补库或美联储继续QT，后续冲击更容易直接打到准备金，风险集中在准备金边际稀缺。",
      "evidence": [
        "RRP从3.28bn跌至0.96bn (5/21-5/22)",
        "RRP 3个月均值：约50bn，当前仅占2%",
        "TGA上升3.9bn可能持续补库"
      ],
      "related_indicators": ["RRPONTSYD", "TGA"]
    },
    {
      "priority": "P1",
      "severity": "medium",
      "type": "data",
      "title": "WRESBAL 滞后更新",
      "text": "银行准备金（WRESBAL）仍为2026-05-20数据，周频延迟3个工作日；无法实时观察准备金被TGA/RRP流失影响。",
      "evidence": [
        "WRESBAL 最新: 2026-05-20（距今6日）",
        "需要H.4.1报告，周四16:30 ET发布，通常下一周才可获得"
      ],
      "related_indicators": ["WRESBAL"]
    }
  ],
  "narrative_blocks": {
    "summary": "Today's liquidity backdrop: SOFR financing costs remain below IORB (policy anchor), indicating moderate slack in overnight funding. However, RRP buffer deterioration and modest TGA elevation pose forward risks to reserve adequacy. JPY carry positioning remains stable; watch for policy signals and cross-asset deleveraging.",
    "rates": "1Y UST yield rose 4bp to 3.83%, suggesting near-term policy path repricing slightly higher. 10Y real yield (+5bp to 2.18%) indicates upward pressure on true discount rates, weighing on growth asset valuations.",
    "balance_sheet": "TGA rose 3.9bn to 785.9bn, partially absorbing Fed QT flows; RRP fell 2.3bn to near-critical lows, suggesting monetary fund redemptions and shrinking buffer cushion.",
    "market_transmission": "SOFR-IORB still negative (policy accommodative) but narrowing. Transmission to credit spreads and FX markets remains muted (VIX: 16.76, IG OAS: 75bp). USD index flat (+0.61pt). Overall: no acute transmission to credit or equity risky assets as of latest update."
  }
}
```

**Expected fields for app.js rendering**:
- `stance.label` → Large pill display, must match one of 5 status_scale values
- `stance.confidence` → "置信度: XX"
- `stance.one_liner` → Main narrative summary
- `key_takeaways[]` → Stack of key insight cards
- `risk_flags[]` → Risk priority/severity cards with evidence bullets
- `narrative_blocks.*` → Optional deep-dive text sections

---

### 2c. model_input.json (245KB)
**Purpose**: NOT directly rendered by frontend; used as prompt/context for LLM to generate analysis.json

**Used by**: Backend pipeline (LLM analysis script)
**NOT used by**: Frontend HTML/JS

**Top-level structure**:
```json
{
  "task": "基于美元流动性介绍文档、结构化市场数据和分析prompt，输出一份可由固定前端模板渲染的结构化 analysis.json。",
  "trigger": "更新数据并分析",
  "generated_at_bjt": "2026-05-26 21:22:51 UTC+08:00",
  "intro_document": "# 美元流动性框架介绍\n\n这份文档供模型在分析每日数据前阅读...",
  "analysis_prompt": "【衍生信号强制取值表...】\n以下衍生信号已由脚本精确计算完成...",
  "data": {
    "stance_by_rule_fallback": "中性",
    "score_by_rule_fallback": 1.0,
    "highlights_by_rule_fallback": [...],
    "metrics": [ { "id": "RRPONTSYD", "name": "...", "value": 0.965, "previous": 3.281, ... } ],
    "derived_signals": [ { "id": "SOFR_ANCHOR", "value": -10.0, "previous": -14.0, "change": 4.0, ... } ],
    "quantity_metrics_required": ["SOFR_VOLUME", "TBILL_AUCTION_SIZE", "TBILL_AUCTION_BTC"],
    "quantity_signals_required": ["SOFR_VOLUME_IMPACT", "TBILL_AUCTION_ABSORPTION"],
    "indicator_groups": [...],
    "charts": [...]
  },
  "output_contract": {
    "required_fields": ["meta", "stance", "key_takeaways", "risk_flags"],
    "schema": {...}
  }
}
```

This is **metadata for the pipeline**, not frontend data.

---

## 3. RELATIVE PATH DEPENDENCY

### Current Setup

```
frontend/
  usd-liquidity-monitor/
    index.html
      <script src="./data.js"></script>
      <script src="./app.js"></script>
    
    app.js (lines 1-4)
      const DATA_URLS = {
        dashboard: "../../output/latest/dashboard_data.json",
        analysis: "../../output/latest/analysis.json"
      };
```

**Requirement**: Serve the project root via HTTP, then open `/frontend/usd-liquidity-monitor/`. This keeps `output/latest/` as the single source of truth.

### Alternatives

**Option A: Copy/Symlink JSON to Frontend**
- Requires pipeline to copy `output/latest/*.json` → `frontend/usd-liquidity-monitor/`
- Pro: No app.js changes needed
- Con: Data duplication; frontend goes stale if pipeline runs but copy fails

**Option B: Relative Path to output/latest** (Implemented)
- app.js line 1-4 currently points to:
  ```javascript
  const DATA_URLS = {
    dashboard: "../../output/latest/dashboard_data.json",
    analysis: "../../output/latest/analysis.json"
  };
  ```
- Pro: Single source of truth; avoids duplication
- Con: Frontend and output directory structure coupling

**Option C: Dynamic Path Resolution** (Most Flexible)
- Detect if local JSON exists; fallback to alternative path
- Frontend served via HTTP server that proxies `/api/data/dashboard` → backend

**Option D: Embedded Data Always** (Simplest for Offline)
- Keep `data.js` fallback as primary
- Pipeline always updates `data.js` with latest data
- Pros: Works offline; no path issues
- Cons: Large JS file (~216KB); slower initial load

---

## 4. APP.JS RENDERING FLOW

**Key Functions** (app.js):

| Function | Purpose | Expected Data |
|----------|---------|----------------|
| `renderMeta()` | Header timestamp + trigger note | `dashboard.meta.generated_at_bjt`, `data_as_of`, `trigger` |
| `renderStance()` | Status pill + confidence + one-liner + scale | `analysis.stance.*` + `dashboard.status_scale.*` |
| `renderStack()` | Key takeaways / risk flags cards | `analysis.key_takeaways[]`, `analysis.risk_flags[]` |
| `renderJpyCarry()` | JPY Carry trade card + metrics grid | `dashboard.jpy_carry.risk`, `.cards`, `.sources` |
| `renderTradingRadar()` | P0/P1/P2 indicator radar grid | `dashboard.trading_dashboard.core/confirm/background` |
| `renderCharts()` | Chart.js canvas rendering | `dashboard.charts[]`, `.chart_groups`, `.core_chart_ids` |
| `renderIndicators()` | Indicator table (expand/collapse) | `dashboard.indicator_groups[]` |
| `renderDataQuality()` | Missing/stale/degraded data notes | `dashboard.data_quality.*` |

**Critical JSON fields app.js depends on**:

```
dashboard_data.json must provide:
  ✓ meta.generated_at_bjt
  ✓ meta.data_as_of
  ✓ meta.trigger (optional)
  ✓ status_scale.values (array of 5 statuses)
  ✓ status_scale.current_from_rule
  ✓ trading_dashboard.core (array of P0 items, including SOFR_VOLUME_IMPACT when available)
  ✓ trading_dashboard.confirm (array of P1/P2 items, including T-bill absorption when available)
  ✓ trading_dashboard.background (array of P2 items)
  ✓ trading_dashboard.core_chart_ids (array of chart IDs to show)
  ✓ trading_dashboard.chart_groups (array of chart group metadata)
  ✓ jpy_carry.risk (object with label, score, reasons)
  ✓ jpy_carry.cards (array of metric cards)
  ✓ jpy_carry.sources (array of data sources)
  ✓ indicator_groups[] (array of tables)
  ✓ charts[] (array of chart data with series/points)
  ✓ data_quality.missing/stale/degraded_sources (arrays)

analysis.json must provide:
  ✓ stance.label (one of 5 values)
  ✓ stance.confidence
  ✓ stance.one_liner
  ✓ key_takeaways[] (array of {title, text, related_indicators})
  ✓ risk_flags[] (array of {priority, severity, title, text, evidence})
  (narrative_blocks optional for deep-dive)
```

---

## 5. INDEX.HTML LAYOUT

**Sections** (index.html):

1. **Header** (lines 14-25)
   - Title, subtitle, update time, data date

2. **Hero Grid** (lines 28-48)
   - Today's stance (large pill)
   - Key takeaways (cards)
   - Risk flags (cards)

3. **JPY Carry Section** (lines 50-59)
   - Render into `#jpy-carry-card`

4. **Trading Radar Section** (lines 61-70)
   - Render into `#trading-radar`

5. **Charts Section** (lines 72-80)
   - Render into `#charts` (grid of Canvas elements)

6. **Indicators Section** (lines 82-94)
   - `<details>` expandable table
   - Render into `#indicator-groups`

7. **Data Quality Section** (lines 96-107)
   - `<details>` expandable
   - Render into `#data-quality`

---

## 6. DATA.JS ROLE & FALLBACK

**Purpose**: Pre-embedded dashboard + analysis data for offline viewing

**Generated by**: Backend pipeline (exports dashboard_data.json + analysis.json as JS)

**Size**: 216KB (current as of 5/26 21:22)

**When used**:
- If `fetch(../../output/latest/dashboard_data.json)` fails → Falls back to `window.DASHBOARD_DATA`
- If `fetch(../../output/latest/analysis.json)` fails → Falls back to `window.ANALYSIS_DATA`
- Allows browser to display data without network access

**Current limitation**: 
- Takes up large JS file size
- Must be regenerated with every pipeline run
- Stale if pipeline output not synced to data.js

---

## 7. PIPELINE OUTPUT REQUIREMENTS

For frontend to work, backend must produce **in `output/latest/`**:

### Files Required
1. **dashboard_data.json** (210KB+)
   - Full dashboard layout + metrics + charts + indicators
   - Must validate against schema in section 2a

2. **analysis.json** (5KB+)
   - LLM-generated stance, takeaways, risk flags
   - Must match schema in section 2b

3. **data.js** (optional, for offline fallback)
   - Pre-embedded copies of dashboard_data.json + analysis.json
   - Generated from above two files

4. **model_input.json** (backend/LLM only)
   - Includes `analysis_prompt`, `quantity_metrics_required`, and `quantity_signals_required`
   - Not read by frontend

### JSON Schema Validation
Frontend expects:
- `dashboard_data.trading_dashboard.core[]` has items with `id, label, value_text, change_text, severity, why`
- `dashboard_data.charts[]` has `series: [{label, points: [{date, value}]}]`
- `analysis.stance.label` is one of exactly: `["宽松", "中性偏松", "中性", "中性偏紧", "紧张"]`
- `analysis.risk_flags[].priority` is one of: `["P0", "P1", "P2"]`
- `analysis.key_takeaways[]` is array of objects with `title, text, related_indicators`

---

## 8. SUMMARY & RECOMMENDATIONS

| Aspect | Current State | Recommendation |
|--------|---------------|-----------------|
| **Data files** | In `output/latest/` | Keep here; copy or update frontend path |
| **Frontend path** | Relative `../../output/latest/` | Keep serving from project root; use data.js only as fallback |
| **data.js fallback** | 216KB embedded | Keep as backup; regenerate with pipeline |
| **JSON schema** | Defined in app.js | Validate output against section 2a/2b schemas |
| **Caching** | `cache: no-store"` | Good for dev; consider ETags for production |
| **Error handling** | Falls back to data.js | Appropriate; shows error message if both fail |

### Current Preview Recommendation:

- Use HTTP server from project root: `/usr/bin/python3 -m http.server <port>`
- Open `/frontend/usd-liquidity-monitor/`
- Keep `app.js` paths at `../../output/latest/dashboard_data.json` and `../../output/latest/analysis.json`
- Keep data.js as fallback only

