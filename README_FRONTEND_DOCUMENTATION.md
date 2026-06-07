# Frontend & Output Structure Documentation

**Analysis Date**: 2026-05-26  
**Project**: USD Liquidity Monitor Dashboard  
**Status**: ✅ Complete

---

## Overview

This documentation package provides a complete analysis of the USD Liquidity Monitor frontend, including:
- Architecture and data flow
- JSON structure specifications
- Path dependency issues and solutions
- Validation checklists
- Troubleshooting guides

## 📁 Documentation Files

### 1. **FRONTEND_QUICK_REFERENCE.txt** ⭐ START HERE
**Purpose**: One-page quick lookup card  
**Best for**: Finding answers fast, testing checklist, common issues

**Contains**:
- Problem statement and directory structure
- Path dependency explanation
- Required JSON fields checklist
- Data loading flow
- 4 solution options (with tradeoffs)
- Common issues and fixes
- Testing procedures

**When to use**: Need a quick answer or testing checklist

---

### 2. **FRONTEND_ANALYSIS.md** 📚 DEEP DIVE
**Purpose**: Comprehensive technical reference  
**Best for**: Understanding architecture, data flow, implementation details

**Contains**:
- Section 1: Frontend Architecture (files, loading strategy, problem analysis)
- Section 2: JSON Data Flow (complete schemas with examples)
- Section 3: Relative Path Dependency (problem & 4 solutions)
- Section 4: App.js Rendering Flow (all functions documented)
- Section 5: Index.html Layout (7 sections explained)
- Section 6: data.js Role (fallback mechanism)
- Section 7: Pipeline Output Requirements (what backend must produce)
- Section 8: Summary & Recommendations

**When to use**: Need complete understanding or planning changes

---

### 3. **JSON_SCHEMA_REFERENCE.md** 🔧 VALIDATION
**Purpose**: Exact JSON structures and validation rules  
**Best for**: Validating pipeline output, debugging rendering issues

**Contains**:
- Dashboard_data.json complete schema with field descriptions
- Analysis.json complete schema with field descriptions
- Model_input.json (for reference, NOT used by frontend)
- Validation checklist for both files
- Common rendering issues and fixes
- File size reference table

**When to use**: Validating JSON output, fixing rendering bugs

---

## 🎯 Quick Navigation

### I want to...

**Check the current data path** → FRONTEND_QUICK_REFERENCE.txt
- Look at "CURRENT PATH STRATEGY" section
- Use project-root HTTP preview so `../../output/latest/` resolves correctly

**Understand the architecture** → FRONTEND_ANALYSIS.md
- Read "Section 1: Frontend Architecture"
- Then "Section 4: App.js Rendering Flow"

**Validate my JSON output** → JSON_SCHEMA_REFERENCE.md
- Use the "Validation Checklist" section
- Check "Common Rendering Issues"

**Test the frontend** → FRONTEND_QUICK_REFERENCE.txt
- Use the "TESTING CHECKLIST" section

**Debug a rendering issue** → JSON_SCHEMA_REFERENCE.md
- Look in "Common Rendering Issues and Fixes"

**Understand data flow** → FRONTEND_ANALYSIS.md
- Read "Section 2: Data Flow"
- See "Section 4: App.js Rendering Flow"

**See exact JSON structure** → JSON_SCHEMA_REFERENCE.md
- Full schemas with field-by-field descriptions

---

## 🔍 Key Findings

### Current Data Path
```text
Frontend fetches:     ../../output/latest/dashboard_data.json
Analysis fetches:     ../../output/latest/analysis.json
Fallback:             data.js still embeds latest data for offline/file preview
```

### Current app.js Setting
```javascript
const DATA_URLS = {
  dashboard: "../../output/latest/dashboard_data.json",
  analysis: "../../output/latest/analysis.json"
};
```

### Critical JSON Requirements

**dashboard_data.json (280 KB±, varies with charts/history)**
- Must have exactly 5 values in `status_scale.values`
- Must have `trading_dashboard.core` array with items
- Must have `charts` with `series[].points[{date, value}]`
- Quantity-aware fields should exist when sources are available: `SOFR_VOLUME`, `TBILL_AUCTION_SIZE`, `TBILL_AUCTION_BTC`, `SOFR_VOLUME_IMPACT`, `TBILL_AUCTION_ABSORPTION`
- All required fields documented in JSON_SCHEMA_REFERENCE.md

**analysis.json (5 KB)**
- `stance.label` must match one of 5 status_scale values
- `risk_flags` must be sorted by priority (P0, P1, P2)
- `key_takeaways` must have title, text, related_indicators

---

## 📊 Data Flow

```
Pipeline generates output/latest/
├── dashboard_data.json (211 KB)
│   ├── Used by: renderMeta, renderStance, renderJpyCarry, 
│   │             renderTradingRadar, renderCharts, renderIndicators,
│   │             renderDataQuality
│   └── Contains: meta, status_scale, trading_dashboard, jpy_carry,
│                 indicator_groups, charts, data_quality
│
├── analysis.json (5 KB)
│   ├── Used by: renderStance, renderStack
│   └── Contains: meta, stance, key_takeaways, risk_flags
│
└── data.js (216 KB, generated)
    ├── Used by: app.js if fetch() fails
    └── Contains: window.DASHBOARD_DATA, window.ANALYSIS_DATA
```

---

## 📋 Documentation by User Role

### For Frontend Developers
1. Start: FRONTEND_QUICK_REFERENCE.txt (overview)
2. Deep dive: FRONTEND_ANALYSIS.md (architecture)
3. Reference: JSON_SCHEMA_REFERENCE.md (validation)

### For Backend/Pipeline Developers
1. Start: FRONTEND_QUICK_REFERENCE.txt (required files)
2. Reference: JSON_SCHEMA_REFERENCE.md (output schemas)
3. Validation: Use checklist to verify output

### For DevOps/Deployment
1. FRONTEND_QUICK_REFERENCE.txt (solution options)
2. Choose Option A, B, or C based on infrastructure
3. Implement path fix or file copying

### For QA/Testing
1. FRONTEND_QUICK_REFERENCE.txt (testing checklist)
2. JSON_SCHEMA_REFERENCE.md (validation)
3. Test all 7 dashboard sections

---

## 🚀 Implementation Checklist

- [ ] Read FRONTEND_QUICK_REFERENCE.txt (5 min)
- [ ] Understand current data path (Section "CURRENT PATH STRATEGY")
- [ ] Serve from project root so `../../output/latest/` resolves
- [ ] Validate pipeline output (JSON_SCHEMA_REFERENCE.md)
- [ ] Implement path fix or file copying
- [ ] Test frontend rendering (TESTING CHECKLIST in Quick Reference)
- [ ] Verify all sections render correctly
- [ ] Check timestamp consistency

---

## 🔗 File References

| File | Size | Purpose | Best For |
|------|------|---------|----------|
| FRONTEND_QUICK_REFERENCE.txt | 11 KB | Quick lookup | Finding answers fast |
| FRONTEND_ANALYSIS.md | 18 KB | Deep dive | Understanding architecture |
| JSON_SCHEMA_REFERENCE.md | 8.9 KB | Validation | Validating output |

---

## 📝 Key Takeaways

1. **Path Strategy**: app.js reads `../../output/latest/` when served from project root.
2. **Fallback**: data.js is still generated and used only when fetch fails.
3. **Critical Fields**: status_scale has 5 values, stance.label must match one.
4. **Quantity Framework**: SOFR/T-bill analysis must include price × scale fields, not just rates/BTC.
5. **Validation**: Use JSON_SCHEMA_REFERENCE.md checklist before testing.

---

## ❓ FAQ

**Q: Why is there a data.js file?**
A: Fallback for offline viewing or when fetch() fails. Embedded 216 KB of pre-rendered data.

**Q: What's model_input.json for?**
A: LLM analysis input—NOT used by frontend. Contains framework docs and prompts.

**Q: Why does status_scale have exactly 5 values?**
A: Frontend renders 5 status pills. Must be: 宽松, 中性偏松, 中性, 中性偏紧, 紧张

**Q: Can I change the dashboard layout?**
A: Only by modifying index.html and app.js. Data structure is predefined.

**Q: How often should data.js be regenerated?**
A: Every pipeline run. It's a snapshot of current output.

---

## 📞 Questions?

Refer to the appropriate documentation file:
- **"How do I..."** → FRONTEND_QUICK_REFERENCE.txt
- **"What is..."** → FRONTEND_ANALYSIS.md
- **"Is this valid JSON?"** → JSON_SCHEMA_REFERENCE.md

---

**Version**: 1.0  
**Last Updated**: 2026-05-26 21:22:51 UTC+08:00  
**Status**: ✅ Analysis Complete
