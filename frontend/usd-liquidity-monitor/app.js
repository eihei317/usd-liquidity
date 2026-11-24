const DATA_URLS = {
  dashboard: "/output/latest/dashboard_data.json",
  analysis: "/output/latest/analysis.json"
};

const chartColors = ["#4d6b8a", "#b85c45", "#7b8f5a", "#7d5f93", "#c38336", "#2f7d55"];
let chartInstances = [];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

async function loadJson(url) {
  if (location.protocol === "file:" || window.STANDALONE_REPORT) {
    const snapshot = url === DATA_URLS.dashboard ? window.DASHBOARD_DATA : window.ANALYSIS_DATA;
    if (!snapshot) throw new Error("离线文件缺少发布数据");
    return snapshot;
  }
  if (!window.__publishedBundle) {
    window.__publishedBundle = fetch("/output/current_bundle.json", {cache: "no-store"}).then(response => {
      if (!response.ok) throw new Error("无法读取本地已发布的报告（HTTP " + response.status + "）");
      return response.json();
    });
  }
  const bundle = await window.__publishedBundle;
  window.__attemptStatus = bundle.latest_attempt;
  window.INVESTMENT_FACTS = bundle.investment_facts || {};
  window.RESEARCH_REVIEW = bundle.research_review || {};
  window.DAILY_BRIEF = bundle.daily_brief;
  return url === DATA_URLS.dashboard ? bundle.dashboard : bundle.analysis;
}

function renderMeta(dashboard) {
  document.getElementById("generated-at").textContent = `更新时间：${dashboard.meta?.generated_at_bjt || "--"}`;
  if(window.__attemptStatus?.status==="failed") document.getElementById("generated-at").textContent += "；最近更新失败，当前展示上次成功结果";
  document.getElementById("data-as-of").textContent = `数据日期：${dashboard.meta?.data_as_of || "--"}`;
  document.getElementById("page-subtitle").textContent = "观察未来几周到几个月，美股与 BTC 面临的流动性环境。";
}

function renderDailyBrief(analysis) {
  const root = document.getElementById("daily-brief");
  const research = analysis.investment_assessment || {};
  const brief = window.DAILY_BRIEF || {
    stance: analysis.stance?.label, confidence: analysis.stance?.confidence,
    headline: analysis.stance?.one_liner || analysis.stance?.summary,
    comparison: research.change_summary, watch: research.next_checks?.[0],
    assets: [["equities", "美股"], ["bitcoin", "BTC"]].filter(([key]) => research[key]).map(([key, name]) => ({
      name, bias: research[key].liquidity_bias, horizon: research[key].horizon,
      confidence: research[key].confidence, summary: research[key].summary
    })),
    alerts: (analysis.risk_flags || []).filter(risk => risk.priority === "P0")
      .map(risk => risk.text + (risk.condition ? " 触发条件：" + risk.condition : ""))
  };
  root.replaceChildren();
  const heading = el("div", "brief-heading");
  if (brief.stance) heading.appendChild(el("strong", "", brief.stance));
  if (brief.confidence) heading.appendChild(el("span", "confidence", "置信度" + brief.confidence));
  root.appendChild(heading);
  root.appendChild(el("p", "brief-headline", brief.headline || "本期缺少总判断。"));
  for (const alert of brief.alerts || []) root.appendChild(el("p", "brief-alert", "优先关注 · " + alert));
  if (brief.comparison) {
    root.append(el("h3", "", "比上次有什么变化"), el("p", "", brief.comparison));
  }
  if (brief.evidence?.length) {
    const list = el("ul", "brief-evidence");
    brief.evidence.forEach(item => list.appendChild(el("li", "", item.text)));
    root.appendChild(list);
  }
  if (brief.assets?.length) {
    const grid = el("div", "brief-assets");
    brief.assets.forEach(asset => {
      const block = el("section", "");
      const context = [asset.bias, asset.horizon, asset.confidence && "置信度" + asset.confidence].filter(Boolean);
      block.append(el("h3", "", asset.name), el("p", "brief-asset-meta", context.join(" · ")), el("p", "", asset.summary));
      grid.appendChild(block);
    });
    root.appendChild(grid);
  }
  if (brief.watch) root.append(el("h3", "", "接下来观察"), el("p", "", brief.watch));
}

function investmentFactMap(facts = window.INVESTMENT_FACTS || {}) {
  const map = new Map();
  ["trend_facts", "calendar_facts", "market_facts", "comparison_facts", "coverage_facts"].forEach(group => {
    (Array.isArray(facts[group]) ? facts[group] : []).forEach(fact => {
      if (fact && typeof fact.fact_id === "string") map.set(fact.fact_id, fact);
    });
  });
  // The catalog also contains canonical and derived facts referenced by an asset.
  // Prefer its complete facts to any compact table copies.
  if (facts.catalog && typeof facts.catalog === "object" && !Array.isArray(facts.catalog)) {
    Object.entries(facts.catalog).forEach(([id, fact]) => {
      if (fact && typeof fact === "object" && !Array.isArray(fact)) map.set(id, {...fact, fact_id: id});
    });
  }
  return map;
}

function researchUnit(unit) {
  const labels = {"percentage points": "个百分点", "percentage point": "个百分点", "USD bn": "十亿美元", "USD mn": "百万美元",
    "USD per 1% SPX move": "美元（指数变动1%）", "Delta百分点/标的变动1%": "个百分点（指数变动1%）", "等值期货手": "手期货等值",
    index: "指数点", ratio: "倍", bps: "bp"};
  return labels[unit] || unit || "";
}

function investmentChangeUnit(fact) {
  // Rate levels use %, but their arithmetic differences are percentage points.
  return researchUnit(fact.change_unit || (fact.unit === "%" ? "percentage points" : fact.unit));
}

function researchNumber(value, unit = "", signed = false) {
  if (typeof value !== "number" || !Number.isFinite(value)) return "未知";
  const label = researchUnit(unit);
  return `${signed && value > 0 ? "+" : ""}${value.toLocaleString("zh-CN", {maximumFractionDigits: 2, minimumFractionDigits: 2})}${label ? ` ${label}` : ""}`;
}

function investmentWindow(fact) {
  if (fact.window_label) return fact.window_label;
  if (Number.isFinite(fact.window_observations)) {
    const frequency = String(fact.frequency || "").toLowerCase();
    const cadence = /week|周/.test(frequency) ? "周频" : /month|月/.test(frequency) ? "月频" : /daily|日/.test(frequency) ? "日频" : "";
    return `${fact.window_observations}个有效${cadence}观测间隔`;
  }
  return fact.window_days ? `未来${fact.window_days}个日历日` : "--";
}

function investmentStatus(status) {
  const labels = {
    ok: "有效", available: "有效", missing: "数据不足", insufficient_history: "历史不足",
    partial_announced: "仅已公告部分", stale: "观测滞后", partial: "部分覆盖",
    anchor_mismatch: "历史锚点不匹配", missing_history: "缺少历史", history_missing: "缺少历史",
    cached: "缓存数据", cached_offline: "离线缓存", cached_after_fetch_failure: "本次抓取失败，使用缓存",
    error: "抓取失败", failed: "抓取失败", invalid: "观测无效", unknown_source_status: "来源状态未知",
    canonical_unusable: "选定观测不可用", canonical_source_history_missing: "缺少选定来源历史",
    history_endpoint_mismatch: "历史终点不匹配", incomplete_date_matched_history: "同日匹配历史不足",
    prospective_capture_only: "仅保存本次可见版本", captured_history_not_verified_point_in_time: "回抓历史未验证当时可见版本",
    missing_price: "缺少价格", pending: "等待观察", collecting: "积累中"
  };
  return labels[status] || status || "未知";
}

function investmentFactStatus(fact) {
  const parts = [investmentStatus(fact.status)];
  if (fact.source_status && fact.source_status !== "ok" && fact.source_status !== fact.status) {
    parts.push(`来源：${investmentStatus(fact.source_status)}`);
  }
  return parts.join("；");
}

function investmentFactText(fact) {
  const range = [fact.previous_as_of, fact.as_of].filter(Boolean).join(" 至 ");
  const values = [];
  if (fact.value !== undefined) values.push(`观测值 ${researchNumber(fact.value, fact.unit)}`);
  if (fact.change !== undefined) values.push(`变化 ${researchNumber(fact.change, investmentChangeUnit(fact), true)}`);
  if (!values.length) values.push(fact.summary || fact.message || fact.coverage_note || fact.note || fact.reason || "");
  return [fact.name || fact.id || fact.fact_id, range, ...values, investmentFactStatus(fact)].filter(Boolean).join(" · ");
}

function appendInvestmentRefs(root, ids, facts) {
  if (!Array.isArray(ids) || !ids.length) return;
  const details = el("details", "investment-refs");
  details.appendChild(el("summary", "", `查看依据（${ids.length}项）`));
  const list = el("ul", "analysis-evidence");
  ids.forEach(id => {
    const item = el("li");
    const fact = facts.get(id);
    if (fact) item.appendChild(el("span", "fact-description", investmentFactText(fact)));
    else item.appendChild(el("span", "fact-description", "本页未提供该依据的完整数值。"));
    item.appendChild(el("code", "fact-reference", id));
    list.appendChild(item);
  });
  details.appendChild(list);
  root.appendChild(details);
}

function appendInvestmentField(root, label, text, className = "") {
  if (!text) return;
  const field = el("div", `investment-field ${className}`.trim());
  field.append(el("dt", "", label), el("dd", "", text));
  root.appendChild(field);
}

function renderInvestmentAssessment(analysis) {
  const root = document.getElementById("investment-assessment");
  if (!root) return;
  root.replaceChildren();
  const research = analysis?.investment_assessment;
  if (!research || typeof research !== "object") {
    root.appendChild(el("p", "card investment-empty", "本版尚无投资研究结论。"));
    return;
  }
  const facts = investmentFactMap();
  const overview = el("article", "card investment-overview");
  overview.appendChild(el("p", "investment-summary", research.summary || "本版尚无投资研究结论。"));
  if (research.change_summary) {
    const change = el("div", "investment-change");
    change.append(el("strong", "", "相比上次"), el("p", "", research.change_summary));
    overview.appendChild(change);
  }
  root.appendChild(overview);
  const assets = el("div", "investment-assets");
  [["equities", "美股"], ["bitcoin", "BTC"]].forEach(([key, label]) => {
    const asset = research[key] || {};
    const bias = ["支持", "中性", "压制", "分化", "数据不足"].includes(asset.liquidity_bias) ? asset.liquidity_bias : "数据不足";
    const tone = {支持: "supportive", 压制: "restrictive", 分化: "mixed", 数据不足: "uncovered", 中性: "neutral"}[bias];
    const card = el("article", `card investment-asset ${tone}`);
    const head = el("div", "investment-card-head");
    head.append(el("h3", "", label), el("span", `investment-bias ${tone}`, bias));
    card.appendChild(head);
    card.appendChild(el("p", "investment-asset-meta", `${asset.horizon || "期限待确认"} · 置信度：${asset.confidence || "未知"}`));
    card.appendChild(el("p", "investment-asset-summary", asset.summary || "本版尚无该资产的投资研究结论。"));
    const fields = el("dl", "investment-fields");
    appendInvestmentField(fields, "传导路径", asset.transmission);
    appendInvestmentField(fields, "继续确认", asset.confirmation);
    appendInvestmentField(fields, "改判条件", asset.invalidation, "invalidation");
    appendInvestmentField(fields, "覆盖边界", asset.coverage_limits, "coverage");
    card.appendChild(fields);
    appendInvestmentRefs(card, asset.fact_ids, facts);
    assets.appendChild(card);
  });
  root.appendChild(assets);
  const expectations = research.expectations || {};
  if (expectations.summary || expectations.status) {
    const card = el("article", "card investment-expectations");
    const head = el("div", "investment-card-head");
    head.append(el("h3", "", "市场预期与价格反应"), el("span", "investment-coverage-label", expectations.status || "数据不足"));
    card.append(head, el("p", "", expectations.summary || "缺少直接预期数据，当前无法判断价格已反映多少。"));
    appendInvestmentRefs(card, expectations.fact_ids, facts);
    root.appendChild(card);
  }
  const scenarios = el("div", "investment-scenarios");
  [["base", "基准路径"], ["upside", "改善路径"], ["downside", "恶化路径"]].forEach(([key, label]) => {
    const scenario = research.scenarios?.[key] || {};
    const card = el("article", `card investment-scenario ${key}`);
    card.append(el("h3", "", label), el("p", "investment-path", scenario.path || "本版尚无该情景判断。"));
    const fields = el("dl", "investment-fields");
    appendInvestmentField(fields, "观察条件", scenario.trigger);
    appendInvestmentField(fields, "失效条件", scenario.invalidation);
    card.appendChild(fields);
    appendInvestmentRefs(card, scenario.fact_ids, facts);
    scenarios.appendChild(card);
  });
  root.appendChild(scenarios);
  if (Array.isArray(research.next_checks) && research.next_checks.length) {
    const card = el("article", "card investment-next");
    const list = el("ol");
    card.appendChild(el("h3", "", "下一步观察"));
    research.next_checks.forEach(item => list.appendChild(el("li", "", item)));
    card.appendChild(list);
    root.appendChild(card);
  }
}

function investmentTable(headers, rows, caption) {
  const wrapper = el("div", "investment-table-wrap");
  const table = el("table", "investment-table");
  if (caption) table.appendChild(el("caption", "", caption));
  const head = el("thead");
  const header = el("tr");
  headers.forEach(text => {
    const cell = el("th", "", text);
    cell.scope = "col";
    header.appendChild(cell);
  });
  head.appendChild(header);
  table.appendChild(head);
  const body = el("tbody");
  rows.forEach(values => {
    const row = el("tr");
    values.forEach(text => row.appendChild(el("td", "", text)));
    body.appendChild(row);
  });
  table.appendChild(body);
  wrapper.appendChild(table);
  return wrapper;
}

function renderInvestmentFacts(facts = window.INVESTMENT_FACTS || {}) {
  const root = document.getElementById("investment-facts");
  if (!root) return;
  root.replaceChildren();
  const trends = Array.isArray(facts.trend_facts) ? facts.trend_facts : [];
  if (trends.length) {
    root.appendChild(investmentTable(["指标", "窗口", "观测区间", "变化", "状态"], trends.map(fact => [
      fact.name || fact.id || fact.fact_id,
      investmentWindow(fact),
      [fact.previous_as_of || "未知", fact.as_of || "未知"].join(" 至 "),
      researchNumber(fact.change, investmentChangeUnit(fact), true),
      investmentFactStatus(fact)
    ]), "中期趋势 · 按有效观测计算，周频窗口与日频窗口分别标注"));
  } else root.appendChild(el("p", "empty", "本版尚无中期趋势证据。"));
  const calendar = Array.isArray(facts.calendar_facts) ? facts.calendar_facts : [];
  if (calendar.length) {
    root.appendChild(investmentTable(["窗口", "日期区间", "已公告毛发行", "到期额", "净现金影响", "状态"], calendar.map(fact => [
      investmentWindow(fact),
      [fact.window_start || fact.as_of || "未知", fact.window_end || "未知"].join(" 至 "),
      researchNumber(fact.gross_announced_offering_usd_bn, "十亿美元"),
      researchNumber(fact.maturities_usd_bn, "十亿美元"),
      researchNumber(fact.net_cash_impact_usd_bn, "十亿美元", true),
      `${investmentStatus(fact.status)}${Number.isFinite(fact.unknown_amount_count) && fact.unknown_amount_count > 0 ? `；${fact.unknown_amount_count}项金额未知` : ""}`
    ]), "未来资金日历 · 已公告毛发行不等于净融资或准备金消耗"));
    const notes = [...new Set(calendar.map(fact => fact.coverage_note).filter(note => typeof note === "string" && note.trim()))];
    if (!notes.length) notes.push("仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。到期、净筹资及准备金影响缺失时保持未知。");
    notes.forEach(note => root.appendChild(el("p", "investment-review-note", note)));
  } else root.appendChild(el("p", "empty", "未来资金日历尚无可用事实，净现金影响未知。"));
  const market = Array.isArray(facts.market_facts) ? facts.market_facts : [];
  if (market.length) {
    root.appendChild(investmentTable(["市场确认", "窗口", "日期", "观测值", "状态"], market.map(fact => [
      fact.name || fact.id || fact.fact_id,
      investmentWindow(fact),
      fact.as_of || "未知",
      researchNumber(fact.value, fact.unit),
      investmentFactStatus(fact)
    ]), "价格反应 · 用作市场确认，不能单独证明流动性预测能力"));
  }
  const coverage = Array.isArray(facts.coverage_facts) ? facts.coverage_facts : [];
  if (coverage.length) {
    const details = el("details", "investment-refs");
    details.appendChild(el("summary", "", "来源与覆盖边界"));
    const list = el("ul", "analysis-evidence");
    coverage.forEach(fact => list.appendChild(el("li", "", [fact.name || fact.id || fact.fact_id, fact.summary || fact.note || fact.notes || fact.reason, investmentStatus(fact.status)].filter(Boolean).join(" · "))));
    details.appendChild(list);
    root.appendChild(details);
  }
}

function optionNumber(value) {
  if (!Number.isFinite(value)) return "";
  return value.toLocaleString("zh-CN", {maximumFractionDigits: 2});
}

function appendOptionSource(root, record, dates) {
  const meta = el("p", "options-meta", dates.filter(Boolean).join(" · "));
  if (record.source) {
    if (meta.textContent) meta.appendChild(el("span", "", " · "));
    const link = /^https?:\/\//i.test(record.source_url || "") ? el("a", "", record.source) : el("span", "", record.source);
    if (link.tagName.toLowerCase() === "a") link.href = record.source_url;
    meta.appendChild(link);
  }
  if (meta.textContent) root.appendChild(meta);
}

function appendOptionsCoverage(root, audit) {
  if (!audit || !Object.keys(audit).length) return;
  const details = el("details", "investment-refs");
  details.appendChild(el("summary", "", "查看数据范围与逐日缺口"));
  const seriesLabels = {model: "30天平值模型", positioning: "交易商方向敞口", chain: "真实期权链"};
  const fieldLabels = {first: "最早观测", last: "最近观测", observations: "观测数", scope: "覆盖范围",
    status: "状态", missing_sp500_dates: "缺少标普收盘值的日期", missing_vix_dates: "缺少 VIX 的日期",
    missing_futures_only_dates: "缺少仅期货报表的日期", missing_combined_dates: "缺少合并报表的日期",
    missing_dates: "缺失日期", message: "说明", note: "口径", cutoff: "统计截止日期",
    first_common_as_of: "最早匹配日期", latest_common_as_of: "最近匹配日期", latest_sp500_as_of: "最近标普收盘日期",
    latest_vix_as_of: "最近 VIX 日期", sp500_gaps: "标普数据质量", vix_gaps: "VIX 数据质量",
    invalid_dates: "无效值日期", invalid_or_conflicting_dates: "无效或同日冲突的日期",
    conflicting_dates: "同日数值冲突", model_error_dates: "模型不可计算日期",
    after_cutoff_dates: "晚于截止日的记录", undated_rows: "缺少日期的记录数", source_gaps: "分来源核对",
    combined: "合并报表", futures_only: "仅期货报表", excluded_dates: "排除的报告日",
    missing_both_week_starts: "两张报表均缺少的周（周一日期）", incompatible_unit_dates: "合约单位不一致的日期",
    unit_change_dates: "合约单位变更日期", coverage: "合约覆盖", input_status: "输入状态",
    source_histories: "完整源历史", eligible_observations: "有效观测数", eligible_first: "最早有效日期", eligible_last: "最近有效日期",
    missing_snapshot_dates: "缺少期权链快照的交易日", missing_fact_dates: "按读数核对缺失日期",
    "option:SPX:gross_gamma_1pct": "指数变动1%的总 Gamma 敞口", "option:SPX:gamma_share_7d": "7日内到期占比",
    "option:SPX:gamma_share_0dte": "当日到期占比",
    available_snapshots: "可用快照数", listed_rows: "合约记录", eligible_contracts: "有效合约", expired_contracts: "已到期合约",
    duplicate_rows: "重复记录", missing_contracts: "缺少 Gamma 或持仓的合约", same_day_timing_missing: "当日到期合约时刻缺失",
    quote_stale: "报价滞后", oi_stale: "未平仓量滞后", session_open_at_observation: "报价时开市", reason: "核对结果"};
  const valueLabels = {ok: "有效", stale: "观测滞后", missing: "数据缺失", not_configured: "未接入期权链",
    invalid: "数据校验失败", redistribution_unconfirmed: "向指定仓库导出的权限待确认", unavailable_at_cutoff: "采集时尚不可用",
    partial: "部分覆盖", complete: "完整", incomplete_chain: "合约链不完整", true: "是", false: "否"};
  function addFields(parent, fields) {
    Object.entries(fields).forEach(([key, value]) => {
      const label = fieldLabels[key] || key;
      if (Array.isArray(value)) {
        const more = el("details", "options-audit");
        more.appendChild(el("summary", "", label + "（" + value.length + " 项）"));
        more.appendChild(el("p", "", value.map(item => typeof item === "object" ? JSON.stringify(item) : valueLabels[item] ?? item).join("，") || "无"));
        parent.appendChild(more);
      } else if (value && typeof value === "object") {
        const group = el("details", "options-audit");
        group.appendChild(el("summary", "", label));
        addFields(group, value);
        parent.appendChild(group);
      } else if (value != null) {
        parent.appendChild(el("p", "options-meta", label + "：" + (valueLabels[value] ?? String(value))));
      }
    });
  }
  Object.entries(audit).forEach(([series, fields]) => {
    if (!fields || typeof fields !== "object") return;
    details.appendChild(el("h4", "", seriesLabels[series] || series));
    addFields(details, fields);
  });
  root.appendChild(details);
}

function renderOptions(options = window.INVESTMENT_FACTS?.options, coverage) {
  const root = document.getElementById("options-panel");
  if (!root) return;
  root.replaceChildren();
  if (!options) {
    root.appendChild(el("p", "empty", "本期归档未收录期权数据。"));
    appendOptionsCoverage(root, coverage);
    return;
  }
  root.appendChild(el("p", "", "Delta 表示期权价格对指数涨跌有多敏感，Gamma 表示这种敏感度变得有多快。若做市商整体持有负 Gamma，指数越涨，他们为对冲而追买的需求可能越大。"));
  const readings = [
    [options.model, "标普500平值期权 · 30天模型", "指数上涨1%时，模型估算期权 Delta 增加", "个百分点",
      "取同日 VIX 作为波动率假设，行权价等于指数点位。这项读数会随 VIX 变化。"],
    [options.positioning, "标普500股指期货期权 · 交易商方向敞口", "交易商期权净敞口折算为", "手股指期货",
      "取 CFTC 两张持仓报表中交易商净持仓之差。正数代表净多，负数代表净空。"]
  ];
  readings.forEach(([fact, title, prefix, unit, note]) => {
    const section = el("div", "options-row");
    section.appendChild(el("h3", "", title));
    if (["ok", "stale", "partial_latest"].includes(fact?.status) && Number.isFinite(fact.value)) {
      const freshness = {stale: "上次读数（已滞后）· ", partial_latest: "最新一期未配对，最近可比读数 · "};
      const weekly = fact === options.positioning;
      const direction = weekly && fact.value !== 0 ? (fact.value < 0 ? "净空 " : "净多 ") : "";
      const level = weekly ? Math.abs(fact.value) : fact.value;
      let reading = (freshness[fact.status] || "") + prefix + " " + direction + optionNumber(level) + " " + unit + "。";
      if (weekly && Number.isFinite(fact.change) && fact.previous_as_of) {
        reading += fact.change === 0 ? "与上周持平。" : "较上周向" + (fact.change < 0 ? "净空" : "净多") + "方向变动 " + optionNumber(Math.abs(fact.change)) + " 手。";
      }
      section.appendChild(el("p", "", reading));
      section.appendChild(el("p", "options-meta", note));
    } else {
      section.appendChild(el("p", "", fact?.message || "本期缺少有效读数。"));
    }
    if (fact) appendOptionSource(section, fact, [fact.as_of && "观测日 " + fact.as_of]);
    root.appendChild(section);
  });
  const chain = options.chain || {};
  const section = el("div", "options-row");
  section.appendChild(el("h3", "", "SPX 与 SPXW · 真实期权链"));
  const facts = Array.isArray(chain.facts) ? chain.facts : [];
  const byId = new Map(facts.filter(fact => ["ok", "stale"].includes(fact.status) && Number.isFinite(fact.value)).map(fact => [fact.fact_id, fact.value]));
  const gross = byId.get("option:SPX:gross_gamma_1pct");
  if (["ok", "stale"].includes(chain.status) && Number.isFinite(gross)) {
    if (chain.status === "stale") section.appendChild(el("p", "", "以下为上次完整观测，行情已滞后。"));
    if (chain.input_status?.length) section.appendChild(el("p", "", "本次另有输入未通过校验，以下读数取标注日期的最近合格快照。"));
    section.appendChild(el("p", "", "按各合约未平仓量和 Gamma 计算。缺少做市商持仓方向，以下按绝对值汇总。"));
    const measures = el("dl", "options-measures");
    for (const [label, value, unit] of [
      ["指数变动1%的总 Gamma 敞口", gross >= 1e8 ? gross / 1e8 : gross, gross >= 1e8 ? " 亿美元" : " 美元"],
      ["7日内到期占比", byId.get("option:SPX:gamma_share_7d"), "%"],
      ["当日到期占比", byId.get("option:SPX:gamma_share_0dte"), "%"]
    ]) {
      const entry = el("div", "");
      entry.append(el("dt", "", label), el("dd", "", Number.isFinite(value) ? optionNumber(value) + unit : "未知"));
      measures.appendChild(entry);
    }
    section.appendChild(measures);
    const strikes = (chain.strike_distribution || []).filter(row => Number.isFinite(row.strike) && Number.isFinite(row.share_pct));
    if (strikes.length) {
      section.appendChild(el("p", "options-meta", "敞口集中的行权价（指数点／占总量）：" +
        strikes.slice(0, 5).map(row => optionNumber(row.strike) + " 点／" + optionNumber(row.share_pct) + "%").join("，")));
    }
  } else {
    const limits = {partial: "本期取得的合约不全。", invalid: "本期合约快照未通过校验。",
      unavailable_at_cutoff: "本期采集时还没有已发布的合约快照。", redistribution_unconfirmed: "本期未确认向指定仓库导出汇总的权限。"};
    section.appendChild(el("p", "", (limits[chain.status] || "本期没有可展示的完整期权链汇总。") + "做市商净 Gamma 未知。"));
  }
  appendOptionSource(section, chain, [chain.observed_at ? "行情时刻 " + chain.observed_at : chain.as_of && "行情日期 " + chain.as_of,
    chain.open_interest_as_of && "未平仓量日期 " + chain.open_interest_as_of,
    chain.available_at && "可用时刻 " + chain.available_at]);
  root.appendChild(section);
  appendOptionsCoverage(root, coverage);
}

function renderResearchReview(review = window.RESEARCH_REVIEW || {}) {
  const root = document.getElementById("research-review");
  if (!root) return;
  root.replaceChildren();
  root.appendChild(el("p", "investment-review-note", review.methodology_note || "按判断发布后可观察到的价格持续记录；新判断需要等待观察窗口结束。"));
  const rows = Array.isArray(review.records) ? review.records : [];
  const mature = rows.filter(row => /^(complete|completed|matured|available|已完成)$/.test(row.status) && Number.isFinite(row.return_pct));
  root.appendChild(el("p", "investment-review-status", mature.length ? `已有${mature.length}项完成观察，结果按原始判断逐条展示。` : "观察样本积累中，当前尚无完成观察的验证结果。"));
  if (!rows.length) return;
  const statusLabels = {pending: "等待观察", collecting: "积累中", complete: "已完成", completed: "已完成", matured: "已完成", available: "已完成", missing: "缺少价格", missing_price: "缺少价格", insufficient_data: "价格不足"};
  const assetLabels = {equities: "美股", bitcoin: "BTC", SP500: "标普500", NASDAQCOM: "纳斯达克综合", CBBTCUSD: "BTC"};
  root.appendChild(el("p", "investment-review-note", "基准为同一资产、同一观察窗口的持有价格变化，不是策略超额收益。最大回撤从窗口内高点计算，最大不利变动相对观察起点计算。"));
  root.appendChild(investmentTable(["判断发布时间", "资产", "原始流动性判断", "观察窗口", "状态", "区间收益", "最大回撤", "最大不利变动", "同资产持有基准"], rows.map(row => [
    row.published_at_bjt || row.run_id || "未知",
    assetLabels[row.asset] || row.asset || "未知",
    row.liquidity_bias || "未知",
    row.horizon || "未知",
    statusLabels[row.status] || row.status || "未知",
    researchNumber(row.return_pct, "%", true),
    researchNumber(row.max_drawdown_pct, "%", true),
    researchNumber(row.max_adverse_excursion_pct, "%", true),
    researchNumber(row.benchmark_return_pct, "%", true)
  ]), "后续表现记录 · 收益与回撤是市场表现，不等于执行策略的收益"));
}

const AXIS_META = {
  funding_price: { label: "资金价格", horizon: "即时" },
  liquidity_buffer: { label: "数量与缓冲", horizon: "结构" },
  treasury_pricing: { label: "美债供给与定价", horizon: "战术" },
  cross_market_transmission: { label: "跨市场传导", horizon: "即时 / 战术" }
};

const HORIZON_META = {
  immediate: { label: "即时状态", fallbackWindow: "1—3个交易日" },
  tactical: { label: "战术趋势", fallbackWindow: "1—4周" },
  structural: { label: "结构环境", fallbackWindow: "1—3个月" }
};

function renderStance(dashboard, analysis) {
  const stance = analysis.stance || {};
  const label = stance.label || dashboard.status_scale?.current_from_rule || "--";
  document.getElementById("stance-label").textContent = label;
  document.getElementById("stance-confidence").textContent = `置信度：${stance.confidence || "--"}`;
  
  // 日元Carry状态：优先用模型分析，fallback 到 dashboard 中的确定性历史数据。
  const jpy = analysis.narrative_blocks?.jpy_carry || {};
  const jpyFallback = dashboard.jpy_carry?.risk || {};
  document.getElementById("stance-jpy-label").textContent = jpy.label || jpyFallback.label || "--";
  
  document.getElementById("stance-one-liner").textContent = stance.one_liner || stance.summary || "暂无模型分析。";

  // 渲染状态刻度尺
  const scale = document.getElementById("status-scale");
  scale.innerHTML = "";
  (dashboard.status_scale?.values || []).forEach(item => {
    const chip = el("span", item === label ? "active" : "", item);
    scale.appendChild(chip);
  });

  renderAxisAssessment(analysis.axis_assessment || {});
}

function renderAxisAssessment(axes) {
  const root = document.getElementById("axis-assessment");
  if (!root) return;
  root.innerHTML = "";
  Object.entries(AXIS_META).forEach(([key, meta]) => {
    const item = axes[key] || {};
    const card = el("article", `axis-item ${severityClass(item.label)}`);
    const top = el("div", "axis-top");
    top.appendChild(el("span", "axis-name", meta.label));
    top.appendChild(el("span", "axis-horizon", meta.horizon));
    card.appendChild(top);
    card.appendChild(el("strong", "axis-label", item.label || "待分析"));
    appendExpandableText(card, "axis-summary", item.summary || "暂无轴判断。");
    root.appendChild(card);
  });
}

function renderHorizonAssessment(horizons) {
  const root = document.getElementById("horizon-assessment");
  if (!root) return;
  root.innerHTML = "";
  Object.entries(HORIZON_META).forEach(([key, meta]) => {
    const item = horizons?.[key] || {};
    const card = el("article", `horizon-card card ${severityClass(item.label)}`);
    const top = el("div", "horizon-top");
    top.appendChild(el("span", "horizon-name", meta.label));
    top.appendChild(el("span", "horizon-window", item.window || meta.fallbackWindow));
    card.appendChild(top);
    card.appendChild(el("strong", "horizon-label", item.label || "待分析"));
    appendExpandableText(card, "horizon-summary", item.summary || "当前 analysis.json 尚未提供该期限判断。");
    root.appendChild(card);
  });
}

/**
 * 渲染关键变化与风险信号（合并）
 * 格式：每个信号卡片包含 title, text, evidence, priority, type
 */
function renderKeySignals(analysis) {
  const container = document.getElementById("key-signals");
  container.innerHTML = "";
  
  const signals = [];
  
  // 1. 风险信号优先，按 P0/P1/P2 排序。
  if (analysis.risk_flags) {
    const sorted = [...analysis.risk_flags].sort((a, b) => {
      const order = { "P0": 0, "P1": 1, "P2": 2, "P3": 3 };
      return (order[a.priority] ?? 9) - (order[b.priority] ?? 9);
    });
    sorted.forEach(item => {
      signals.push({
        priority: item.priority || "P2",
        title: item.title,
        text: item.text,
        condition: item.condition,
        evidence: item.evidence || [],
        type: "risk"
      });
    });
  }
  
  // 同一利率可以同时支持一条已发生的观察和一条未来风险。
  for (const item of analysis.key_takeaways || []) {
    signals.push({
      priority: "INFO", title: item.title, text: item.text,
      evidence: item.evidence || [], type: "takeaway"
    });
  }
  
  // 3. 日元 Carry 只作为一条补充状态，不再重复渲染整段 narrative。
  const jpy = analysis.narrative_blocks?.jpy_carry;
  if (jpy?.one_liner || jpy?.analysis) {
    signals.push({
      priority: "INFO",
      title: `日元 Carry：${jpy.label || "--"}`,
      text: jpy.one_liner || jpy.analysis,
      evidence: [],
      type: "jpy"
    });
  }
  
  if (!signals.length) {
    container.appendChild(el("p", "empty", "暂无关键变化与风险信号"));
    return;
  }
  
  signals.forEach(sig => {
    const card = el("article", `signal-card ${getPriorityClass(sig.priority)}`);
    const head = el("div", "signal-head");
    head.appendChild(el("span", `signal-priority ${getPriorityClass(sig.priority)}`, sig.priority));
    head.appendChild(el("h4", "signal-title", sig.title));
    card.appendChild(head);

    if (sig.text) {
      appendExpandableText(card, "signal-text", sig.text);
    }
    if (sig.condition) card.appendChild(el("p", "signal-text", "触发条件：" + sig.condition));

    if (sig.evidence && sig.evidence.length) {
      const details = el("details", "signal-details");
      details.appendChild(el("summary", "", `查看证据（${sig.evidence.length}项）`));
      const evidenceList = el("ul", "signal-evidence");
      sig.evidence.forEach(e => evidenceList.appendChild(el("li", "", e)));
      details.appendChild(evidenceList);
      card.appendChild(details);
    }

    container.appendChild(card);
  });
}

function getPriorityClass(priority) {
  if (priority === "P0") return "p0";
  if (priority === "P1") return "p1";
  if (priority === "P2") return "p2";
  if (priority === "INFO") return "info";
  if (priority === "NARR") return "narr";
  return "p2";
}

function severityClass(severity) {
  if (["偏紧", "紧张", "中性偏高"].includes(severity)) return "tight";
  if (severity === "偏松") return "loose";
  if (severity === "缺失" || severity === "数据缺口") return "data-gap";
  return "neutral";
}

function renderTradingRadar(radar) {
  const root = document.getElementById("trading-radar");
  if (!root) return;
  root.innerHTML = "";
  const core = radar?.core || [];
  const confirm = radar?.confirm || [];
  const background = radar?.background || [];

  // CORE/CONFIRM/BACKGROUND 是监控层级，不是风险优先级；P0/P1/P2 只属于模型 risk_flags。
  const grid = el("div", "radar-grid");
  core.forEach(item => grid.appendChild(renderRadarItem(item)));
  root.appendChild(grid);

  // 其他指标折叠
  if (confirm.length || background.length) {
    const details = el("details", "radar-details");
    const summary = el("summary", "", `二级确认与背景指标（${confirm.length + background.length}项）`);
    details.appendChild(summary);
    const rows = el("div", "radar-mini-list");
    [...confirm, ...background].forEach(item => rows.appendChild(renderRadarMiniItem(item)));
    details.appendChild(rows);
    root.appendChild(details);
  }
}

function renderRadarItem(item) {
  const card = el("div", `radar-item ${severityClass(item.severity)}`);
  const top = el("div", "radar-top");
  top.appendChild(el("span", "priority", item.priority || ""));
  top.appendChild(el("span", "radar-status", item.severity || "中性"));
  card.appendChild(top);
  card.appendChild(el("strong", "", item.label || item.id));
  const value = el("div", "radar-value", item.value_text || "NA");
  card.appendChild(value);
  // 时间信息行：日期 + 频率 + 上一期 + 变化
  const metaLine = el("p", "radar-meta");
  if (item.as_of) {
    metaLine.appendChild(el("span", "meta-as-of", `${item.as_of} ${item.frequency || ""}`));
  }
  metaLine.appendChild(el("span", "meta-prev", `上期 ${item.previous_text || "NA"}`));
  metaLine.appendChild(el("span", "meta-change", `变化 ${item.change_text || "NA"}`));
  card.appendChild(metaLine);
  card.appendChild(el("p", "radar-why", item.why || item.interpretation || ""));
  return card;
}

function renderRadarMiniItem(item) {
  const row = el("div", `radar-mini ${severityClass(item.severity)}`);
  row.appendChild(el("span", "priority", item.priority || ""));
  row.appendChild(el("strong", "", item.label || item.id));
  row.appendChild(el("span", "mono", item.value_text || "NA"));
  // 时间信息
  if (item.as_of) {
    row.appendChild(el("span", "meta", `${item.as_of} ${item.frequency || ""}`));
  }
  row.appendChild(el("span", "mono", `上期 ${item.previous_text || "NA"}`));
  row.appendChild(el("span", "mono", `变化 ${item.change_text || "NA"}`));
  row.appendChild(el("span", "", item.why || ""));
  return row;
}

function renderUpcomingAuctions(payload) {
  const root = document.getElementById("upcoming-auctions");
  if (!root) return;
  root.innerHTML = "";
  if (!payload || payload.status !== "ok") {
    root.appendChild(el("p", "empty", payload?.notes || "暂无未来拍卖日程"));
    return;
  }

  const billSchedule = payload.bill_schedule || [];
  const nextAuctions = payload.next_auctions || [];
  const largeAuctions = payload.large_auctions || [];

  // 下一场拍卖
  const hero = el("div", "auction-hero");
  const next = nextAuctions[0] || {};
  const nextBox = el("div", "auction-focus");
  nextBox.appendChild(el("span", "card-label", "下一场拍卖"));
  nextBox.appendChild(el("strong", "", next.auctionDate || "--"));
  nextBox.appendChild(el("p", "", `${next.securityTerm || "--"} / ${next.offeringAmountText || "待公布"}`));
  hero.appendChild(nextBox);

  // 未来大额发行
  const largeBox = el("div", "auction-summary");
  largeBox.appendChild(el("h3", "", "未来大额发行"));
  if (largeAuctions.length) {
    largeAuctions.slice(0, 4).forEach(item => {
      largeBox.appendChild(el("p", "", `${item.auctionDate}：${item.securityTerm} ${item.securityType} ${item.offeringAmountText}`));
    });
  } else {
    largeBox.appendChild(el("p", "", "未来窗口暂无已公布的大额发行，或发行规模待公布。"));
  }
  hero.appendChild(largeBox);
  root.appendChild(hero);

  // 未来拍卖日程（精简显示）
  const grid = el("div", "auction-grid");
  billSchedule.slice(0, 8).forEach(day => {
    const card = el("div", "auction-day");
    card.appendChild(el("div", "auction-date", day.auctionDate || "--"));
    card.appendChild(el("div", "auction-size", day.totalBillOfferingText || "待公布"));
    const terms = (day.items || []).map(item => `${item.securityTerm} ${item.offeringAmountText || "待公布"}`).join(" / ");
    card.appendChild(el("p", "", terms || "发行规模待公布"));
    grid.appendChild(card);
  });
  if (!billSchedule.length) grid.appendChild(el("p", "empty", "未来窗口暂无 T-bill 拍卖日程"));
  root.appendChild(grid);

  // 展开全部
  const details = el("details", "auction-details");
  details.appendChild(el("summary", "", "展开全部未来拍卖"));
  const tableWrap = el("div", "table-wrap");
  const table = el("table", "indicator-table");
  const thead = el("thead");
  const headRow = el("tr");
  ["拍卖日", "结算日", "期限/类型", "发行规模"].forEach(label => headRow.appendChild(el("th", "", label)));
  thead.appendChild(headRow);
  table.appendChild(thead);
  const tbody = el("tbody");
  nextAuctions.forEach(item => {
    const row = el("tr");
    row.appendChild(el("td", "mono", item.auctionDate || "--"));
    row.appendChild(el("td", "mono", item.issueDate || "--"));
    const typeTerm = [item.securityTerm || "", item.securityType || ""].filter(Boolean).join(" ") || "--";
    row.appendChild(el("td", "", typeTerm));
    row.appendChild(el("td", "mono", item.offeringAmountText || "待公布"));
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
  tableWrap.appendChild(table);
  details.appendChild(tableWrap);
  root.appendChild(details);
}

function renderIndicators(groups) {
  const root = document.getElementById("indicator-groups");
  root.innerHTML = "";
  const article = el("article", "card indicator-table-card");
  const tableWrap = el("div", "table-wrap");
  const table = el("table", "indicator-table");
  const thead = el("thead");
  const headRow = el("tr");
  ["模块", "指标", "最新值", "上一期", "边际变化", "日期", "频率 / 口径", "状态"].forEach(label => headRow.appendChild(el("th", "", label)));
  thead.appendChild(headRow);
  table.appendChild(thead);

  const tbody = el("tbody");
  (groups || []).forEach(group => {
    (group.indicators || []).forEach(item => {
      const row = el("tr");
      row.appendChild(el("td", "group-name", group.title || "--"));
      const nameCell = el("td", "indicator-name");
      nameCell.appendChild(el("strong", "", item.label || item.id || "--"));
      nameCell.appendChild(el("span", "indicator-meaning", item.meaning || ""));
      row.appendChild(nameCell);
      row.appendChild(el("td", "mono", item.value_text || "NA"));
      row.appendChild(el("td", "mono", item.previous !== null && item.previous !== undefined ? formatTableValue(item.previous, item.unit) : "NA"));
      row.appendChild(el("td", `mono change ${item.change_direction || "unknown"}`, item.change_text || "NA"));
      row.appendChild(el("td", "mono", item.as_of || "NA"));
      const freqCell = el("td", "frequency-cell");
      freqCell.appendChild(el("span", "", item.frequency || "频率未知"));
      freqCell.appendChild(el("small", "", item.comparison_basis || "口径未知"));
      row.appendChild(freqCell);
      row.appendChild(el("td", "", item.freshness || item.status || "unknown"));
      tbody.appendChild(row);
    });
  });
  table.appendChild(tbody);
  tableWrap.appendChild(table);
  article.appendChild(tableWrap);
  root.appendChild(article);
}

function formatTableValue(value, unit) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "NA";
  if (unit === "%") return `${Number(value).toFixed(3)}%`;
  if (unit === "USD bn") return `${Number(value).toLocaleString(undefined, { maximumFractionDigits: 1, minimumFractionDigits: 1 })}bn`;
  if (unit === "ratio") return `${Number(value).toFixed(2)}x`;
  if (unit === "index") return Number(value).toFixed(2);
  return `${Number(value).toFixed(2)}${unit || ""}`;
}

/**
 * 渲染图表
 * 核心图表：展开显示
 * 背景图表：折叠显示
 */
function renderCharts(charts, chartGroups, dashboard) {
  const coreContainer = document.getElementById("charts-core");
  const bgContainer = document.getElementById("charts-background");
  
  coreContainer.innerHTML = "";
  bgContainer.innerHTML = "";
  
  chartInstances.forEach(c => c.destroy());
  chartInstances = [];
  
  const optionsContainer = document.getElementById("options-charts");
  const allCharts = charts || [];
  if (optionsContainer) {
    optionsContainer.replaceChildren(...allCharts.filter(chart => chart.id.startsWith("options_")).map(renderChartCard));
  }
  const otherCharts = optionsContainer ? allCharts.filter(chart => !chart.id.startsWith("options_")) : allCharts;
  const byId = new Map(otherCharts.map(chart => [chart.id, chart]));
  
  const defaultCoreChartIds = [
    "anchor_spreads_30d",
    "fed_liability_30d",
    "treasury_combined_supply_30d",
    "us_jp_spread",
    "treasury_yields_30d",
    "jpy_usdjpy_funding_1y"
  ];
  const groups = Array.isArray(chartGroups) ? chartGroups : [];
  const coreGroup = groups.find(group => group.default_open !== false);
  const backgroundGroups = groups.filter(group => group.default_open === false);
  const coreChartIds = coreGroup?.chart_ids?.length ? coreGroup.chart_ids : defaultCoreChartIds;
  const backgroundChartIds = backgroundGroups.flatMap(group => group.chart_ids || []);
  
  coreChartIds.forEach(chartId => {
    const chart = byId.get(chartId);
    if (chart) coreContainer.appendChild(renderChartCard(chart));
  });
  
  const backgroundCharts = backgroundChartIds.length
    ? backgroundChartIds.map(id => byId.get(id)).filter(Boolean)
    : otherCharts.filter(c => !coreChartIds.includes(c.id));
  backgroundCharts.forEach(chart => bgContainer.appendChild(renderChartCard(chart)));
}

function parseChartDate(value) {
  if (!value) return null;
  const raw = String(value);
  const normalized = /^\d{8}$/.test(raw)
    ? `${raw.slice(0, 4)}-${raw.slice(4, 6)}-${raw.slice(6, 8)}`
    : raw;
  const parsed = new Date(normalized);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function limitChartToRecentMonth(chart) {
  const cloned = { ...chart, series: (chart.series || []).map(s => ({ ...s, points: [...(s.points || [])] })) };
  const parsedDates = cloned.series
    .flatMap(s => s.points || [])
    .map(p => parseChartDate(p.date))
    .filter(Boolean)
    .sort((a, b) => a - b);
  if (!parsedDates.length) return cloned;
  const latest = parsedDates[parsedDates.length - 1];
  const cutoff = new Date(latest);
  cutoff.setDate(cutoff.getDate() - 35);
  cloned.series = cloned.series.map(s => ({
    ...s,
    points: (s.points || []).filter(p => {
      const d = parseChartDate(p.date);
      return d && d >= cutoff;
    })
  }));
  return cloned;
}

function formatChartNumber(value, unit) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "NA";
  const number = Number(value);
  if (unit === "%") return `${number.toFixed(2)}%`;
  if (unit === "bp") return `${number.toFixed(1)}bp`;
  if (unit === "USD bn") return `${number.toFixed(1)}bn`;
  if (unit === "ratio") return `${number.toFixed(2)}x`;
  return `${number.toFixed(2)}${researchUnit(unit)}`;
}

function renderChartStats(chart) {
  const root = el("div", "chart-stats");
  (chart.series || []).slice(0, 4).forEach(series => {
    const points = (series.points || []).filter(point => point.value !== null && point.value !== undefined);
    if (!points.length) return;
    const latest = points[points.length - 1];
    const previous = points.length > 1 ? points[points.length - 2] : null;
    const delta = previous ? Number(latest.value) - Number(previous.value) : null;
    const stat = el("div", "chart-stat");
    stat.appendChild(el("span", "chart-stat-label", series.label));
    const valueRow = el("div", "chart-stat-value");
    valueRow.appendChild(document.createTextNode(formatChartNumber(latest.value, chart.unit)));
    if (delta !== null && !Number.isNaN(delta)) {
      const changeUnit = chart.id.startsWith("options_") && chart.unit === "%" ? "个百分点" : chart.unit;
      valueRow.appendChild(el("small", delta > 0 ? "up" : delta < 0 ? "down" : "flat", `${delta > 0 ? "+" : ""}${formatChartNumber(delta, changeUnit)}`));
    }
    stat.appendChild(valueRow);
    stat.appendChild(el("span", "chart-stat-date", latest.date || "--"));
    root.appendChild(stat);
  });
  return root;
}

function renderChartCard(rawChart) {
  const chart = rawChart.id.startsWith("options_") ? rawChart : limitChartToRecentMonth(rawChart);
  const card = el("article", "card chart-card");
  card.appendChild(el("h3", "", chart.title));
  card.appendChild(renderChartStats(chart));
  if (!chart.series || !chart.series.length) {
    card.appendChild(el("p", "empty", "暂无可绘制数据"));
  } else {
    const chartBox = el("div", "chart-canvas-wrap");
    const canvas = document.createElement("canvas");
    chartBox.appendChild(canvas);
    card.appendChild(chartBox);
    const chartInstance = drawChartJS(chart, canvas);
    if (chartInstance) {
      chartInstances.push(chartInstance);
    }
    card.appendChild(renderLegend(chart.series));
  }
  return card;
}

function renderLegend(series) {
  const legend = el("div", "legend");
  series.forEach((s, index) => {
    const item = el("span");
    const dot = el("i");
    dot.style.background = chartColors[index % chartColors.length];
    item.appendChild(dot);
    item.appendChild(document.createTextNode(s.label));
    legend.appendChild(item);
  });
  return legend;
}

function buildScales(chart, unit) {
  const base = {
    x: {
      ticks: { maxRotation: 45, minRotation: 0, font: { size: 9 }, color: "#8a7d70" },
      grid: { color: "#eadfce" }
    },
    y: {
      type: "linear",
      position: "left",
      title: { display: true, text: chart.y_axes?.y || unit, color: "#6b5e50", font: { size: 11 } },
      ticks: { font: { size: 10 }, color: "#8a7d70" },
      grid: { color: "#eadfce" }
    }
  };
  if (chart.dual_axis) {
    base.y1 = {
      type: "linear",
      position: "right",
      title: { display: true, text: chart.y_axes?.y1 || unit, color: "#6b5e50", font: { size: 11 } },
      ticks: { font: { size: 10 }, color: "#8a7d70" },
      grid: { drawOnChartArea: false }
    };
  }
  return base;
}

function drawChartJS(chart, canvas) {
  const allDates = chart.series.flatMap(s => s.points || []);
  const labels = Array.from(new Set(allDates.map(p => p.date))).sort();
  const unit = chart.id.startsWith("options_") ? researchUnit(chart.unit) : chart.unit || "";

  const datasets = chart.series.map((s, index) => {
    const pointMap = {};
    (s.points || []).forEach(p => { pointMap[p.date] = p.value; });
    return {
      label: s.label,
      data: labels.map(date => pointMap[date] !== undefined ? pointMap[date] : null),
      borderColor: chartColors[index % chartColors.length],
      backgroundColor: chartColors[index % chartColors.length] + "20",
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 5,
      tension: 0.1,
      fill: false,
      yAxisID: s.y_axis || "y"
    };
  });
  const scales = buildScales(chart, unit);

  const ctx = canvas.getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        tooltip: {
          backgroundColor: "#3a3428",
          titleColor: "#f0ebe1",
          bodyColor: "#f0ebe1",
          borderColor: "#5c5447",
          borderWidth: 1,
          callbacks: {
            title: (items) => items[0].label,
            label: (item) => `${item.dataset.label}: ${item.raw !== null ? item.raw : "N/A"}${unit}`
          }
        },
        legend: { display: false }
      },
      scales
    }
  });
}

function renderDataQuality(dataQuality) {
  const root = document.getElementById("data-quality");
  root.innerHTML = "";
  const blocks = [
    ["缺失数据", dataQuality?.missing || []],
    ["滞后数据", dataQuality?.stale || []],
    ["替代观察", dataQuality?.degraded_sources || []]
  ];
  blocks.forEach(([title, items]) => {
    const block = el("div", "quality-block");
    block.appendChild(el("h3", "", title));
    if (!items.length) {
      block.appendChild(el("p", "empty", "暂无"));
    } else {
      const ul = el("ul");
      items.slice(0, 8).forEach(item => {
        const li = el("li", "", item.label || item.name || item.id || "未知项");
        if (item.reason) li.title = item.reason;
        ul.appendChild(li);
      });
      block.appendChild(ul);
    }
    root.appendChild(block);
  });
}


function appendExpandableText(root, className, text) {
  const preview = el("p", className, text);
  const details = el("details", "analysis-expand");
  const summary = el("summary", "", "展开全文");
  details.append(summary, el("p", "analysis-prose", text));
  details.addEventListener("toggle", () => {
    preview.hidden = details.open;
    summary.textContent = details.open ? "收起全文" : "展开全文";
  });
  root.append(preview, details);
}

function renderFullAnalysis(analysis) {
  const root = document.getElementById("full-analysis-content");
  root.replaceChildren();
  const add = (title, text) => {
    if (!text) return;
    const block = el("article", "analysis-block");
    block.append(el("h3", "", title), el("p", "analysis-prose", text));
    root.appendChild(block);
  };
  add("数据日期与可用性", analysis.meta?.input_freshness_note);
  add("综合判断", analysis.stance?.score_text);
  const titles = {summary:"分析总述", rates:"资金价格", balance_sheet:"资产负债表与现金流", market_transmission:"跨市场传导", treasury_yields:"美债收益率", jpy_carry:"日元套利"};
  Object.entries(analysis.narrative_blocks || {}).forEach(([key, value]) => {
    if (typeof value === "string") add(titles[key] || key, value);
    else if (value) add(titles[key] || key, [value.label, value.one_liner, value.analysis].filter(Boolean).join("\n\n"));
  });
  [["全部关键观察", analysis.key_takeaways], ["全部风险与触发条件", analysis.risk_flags]].forEach(([title, items]) => {
    if (!items?.length) return;
    root.appendChild(el("h3", "", title));
    items.forEach(item => {
      const block = el("article", "analysis-block");
      block.append(el("h4", "", item.title), el("p", "analysis-prose", item.text));
      if (item.condition) block.appendChild(el("p", "analysis-prose", "触发条件：" + item.condition));
      const list = el("ul", "analysis-evidence");
      (item.evidence || []).forEach(text => list.appendChild(el("li", "", text)));
      block.appendChild(list);
      root.appendChild(block);
    });
  });
}

async function init() {
  try {
    const dashboard = await loadJson(DATA_URLS.dashboard);
    const analysis = await loadJson(DATA_URLS.analysis);
    
    renderMeta(dashboard);
    renderDailyBrief(analysis);
    renderOptions(window.INVESTMENT_FACTS?.options, dashboard.history_coverage?.option_details);
    renderInvestmentAssessment(analysis);
    renderInvestmentFacts();
    renderResearchReview();
    renderStance(dashboard, analysis);
    renderHorizonAssessment(analysis.horizon_assessment);
    renderKeySignals(analysis);
    renderFullAnalysis(analysis);
    renderTradingRadar(dashboard.trading_dashboard);
    renderUpcomingAuctions(dashboard.upcoming_auctions);
    renderCharts(dashboard.charts, dashboard.trading_dashboard?.chart_groups, dashboard);
    renderIndicators(dashboard.indicator_groups);
    renderDataQuality(dashboard.data_quality);
    if(dashboard.history_coverage){
      const host=document.getElementById('data-quality');
      const detail=el('details','history-coverage');
      detail.appendChild(el('summary','',`全部历史覆盖核对（${dashboard.history_coverage.series.length}项；${dashboard.history_coverage.missing.length}项缺口）`));
      detail.appendChild(el('p','',dashboard.history_coverage.scope));
      detail.appendChild(investmentTable(['类型','指标','来源','起始日期','结束日期','观测数','状态'],dashboard.history_coverage.series.map(r=>[r.kind,r.id,r.source||'依赖原始指标',r.first||'未知',r.last||'未知',String(r.observations),r.status==='history_available'?'有历史':'历史缺失'])));
      host.appendChild(detail);
    }
  } catch (error) {
    const main = el("main", "page-shell");
    const card = el("article", "card");
    card.append(el("h1", "", "美元流动性与风险资产"), el("p", "meaning", `数据加载失败：${error.message}`), el("p", "meaning", "请确认本地服务可用，并在数据更新完成后刷新页面。"));
    main.appendChild(card);
    document.body.replaceChildren(main);
  }
}

init();
