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
  // 离线 fallback：若 data.js 已注入全局变量，直接返回
  if (url === "/output/latest/dashboard_data.json" && window.DASHBOARD_DATA) {
    return window.DASHBOARD_DATA;
  }
  if (url === "/output/latest/analysis.json" && window.ANALYSIS_DATA) {
    // 占位符时继续 fetch 真正的 analysis.json，避免前端锁死在"待模型分析"
    if (!(window.ANALYSIS_DATA.meta && window.ANALYSIS_DATA.meta.status === "pending_model_analysis")) {
      return window.ANALYSIS_DATA;
    }
  }
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`${url} ${response.status}`);
  return response.json();
}

function renderMeta(dashboard) {
  document.getElementById("generated-at").textContent = `更新时间：${dashboard.meta?.generated_at_bjt || "--"}`;
  document.getElementById("data-as-of").textContent = `数据日期：${dashboard.meta?.data_as_of || "--"}`;
  document.getElementById("page-subtitle").textContent = dashboard.meta?.trigger ? `触发语：${dashboard.meta.trigger}` : "触发脚本 → 模型分析 → 稳定前端渲染";
}

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
}

/**
 * 渲染关键变化与风险信号（合并）
 * 格式：每个信号卡片包含 title, text, evidence, priority, type
 */
function renderKeySignals(analysis) {
  const container = document.getElementById("key-signals");
  container.innerHTML = "";
  
  const signals = [];
  const riskIndicatorSet = new Set();
  const titleSet = new Set();
  const normalizeTitle = value => (value || "").replace(/[\s：:，,。.!！]/g, "").slice(0, 16);
  
  // 1. 风险信号优先，按 P0/P1/P2 排序。
  if (analysis.risk_flags) {
    const sorted = [...analysis.risk_flags].sort((a, b) => {
      const order = { "P0": 0, "P1": 1, "P2": 2, "P3": 3 };
      return (order[a.priority] ?? 9) - (order[b.priority] ?? 9);
    });
    sorted.forEach(item => {
      (item.related_indicators || []).forEach(id => riskIndicatorSet.add(id));
      titleSet.add(normalizeTitle(item.title));
      signals.push({
        priority: item.priority || "P2",
        title: item.title,
        text: item.text,
        evidence: item.evidence || [],
        type: "risk"
      });
    });
  }
  
  // 2. 关键变化只补充未被风险信号覆盖的内容，避免 RRP/SOFR 等重复出现。
  if (analysis.key_takeaways) {
    analysis.key_takeaways.forEach(item => {
      const related = item.related_indicators || [];
      const overlapsRisk = related.some(id => riskIndicatorSet.has(id));
      const titleKey = normalizeTitle(item.title);
      if (!overlapsRisk && !titleSet.has(titleKey)) {
        signals.push({
          priority: "INFO",
          title: item.title,
          text: item.text,
          evidence: item.evidence || [],
          type: "takeaway"
        });
        titleSet.add(titleKey);
      }
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
    const card = el("div", `signal-card ${getPriorityClass(sig.priority)}`);
    
    // 优先级标签
    const priorityTag = el("span", `signal-priority ${getPriorityClass(sig.priority)}`, sig.priority);
    card.appendChild(priorityTag);
    
    // 标题
    const title = el("h4", "signal-title", sig.title);
    card.appendChild(title);
    
    // 正文
    if (sig.text) {
      const text = el("p", "signal-text", sig.text);
      card.appendChild(text);
    }
    
    // 证据列表
    if (sig.evidence && sig.evidence.length) {
      const evidenceList = el("ul", "signal-evidence");
      sig.evidence.forEach(e => {
        evidenceList.appendChild(el("li", "", e));
      });
      card.appendChild(evidenceList);
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

  // 只显示 P0/P1 核心指标
  const grid = el("div", "radar-grid");
  core.forEach(item => {
    if (item.priority === "P0" || item.priority === "P1") {
      grid.appendChild(renderRadarItem(item));
    }
  });
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
  
  const byId = new Map((charts || []).map(chart => [chart.id, chart]));
  
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
    : charts.filter(c => !coreChartIds.includes(c.id));
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

function renderChartCard(rawChart) {
  const chart = limitChartToRecentMonth(rawChart);
  const card = el("article", "card chart-card");
  card.appendChild(el("h3", "", chart.title));
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
  const unit = chart.unit || "";

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

async function init() {
  try {
    // 优先动态加载最新 JSON
    let dashboard;
    try {
      dashboard = await loadJson(DATA_URLS.dashboard);
    } catch (e) {
      dashboard = window.DASHBOARD_DATA || {};
    }

    let analysis;
    try {
      analysis = await loadJson(DATA_URLS.analysis);
    } catch (e) {
      analysis = window.ANALYSIS_DATA || {};
    }
    
    renderMeta(dashboard);
    renderStance(dashboard, analysis);
    renderKeySignals(analysis);
    renderTradingRadar(dashboard.trading_dashboard);
    renderUpcomingAuctions(dashboard.upcoming_auctions);
    renderCharts(dashboard.charts, dashboard.trading_dashboard?.chart_groups, dashboard);
    renderIndicators(dashboard.indicator_groups);
    renderDataQuality(dashboard.data_quality);
  } catch (error) {
    document.body.innerHTML = `<main class="page-shell"><article class="card"><h1>美元流动性监测</h1><p class="meaning">数据加载失败：${error.message}</p><p class="meaning">请先运行脚本生成 output/latest/dashboard_data.json 和 output/latest/analysis.json，并通过本地服务预览页面。</p></article></main>`;
  }
}

init();
