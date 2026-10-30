"use strict";

// Offline rendering regression checks. No browser, network, or production writes.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

class TestNode {
  constructor(tag = "div") {
    this.tagName = tag;
    this.children = [];
    this._text = "";
    this.className = "";
  }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(node => node.textContent).join(" "); }
  appendChild(node) { this.children.push(node); return node; }
  append(...nodes) { nodes.forEach(node => this.appendChild(node)); }
  replaceChildren(...nodes) { this.children = []; this._text = ""; this.append(...nodes); }
  addEventListener() {}
}

function allNodes(node) { return [node, ...node.children.flatMap(allNodes)]; }

function makeContext() {
  const roots = Object.fromEntries(["investment-assessment", "investment-facts", "research-review"].map(id => [id, new TestNode()]));
  const document = {
    body: new TestNode("body"),
    createElement: tag => new TestNode(tag),
    getElementById: id => roots[id] || null
  };
  const context = {
    document, window: {}, location: {protocol: "file:"}, Map, Set, console,
    fetch: () => { throw new Error("Test must not make network requests"); }
  };
  vm.createContext(context);
  const file = path.join(__dirname, "../frontend/usd-liquidity-monitor/app.js");
  const source = fs.readFileSync(file, "utf8");
  assert.match(source, /init\(\);\s*$/);
  vm.runInContext(source.replace(/init\(\);\s*$/, ""), context, {filename: file});
  return {context, roots};
}

async function main() {
  const {context, roots} = makeContext();
  context.renderInvestmentAssessment({});
  assert.match(roots["investment-assessment"].textContent, /本版尚无投资研究结论/);
  assert.doesNotMatch(roots["investment-assessment"].textContent, /中性/);

  const malicious = "<img src=x onerror=alert(1)>";
  const facts = {
    trend_facts: [
      {fact_id: "trend:SOFR:20obs", name: "SOFR", value: 3.94, change: -0.4, unit: "%", change_unit: "percentage points", as_of: "2026-10-30", previous_as_of: "2026-09-30", window_observations: 20, frequency: "daily", status: "ok"},
      {fact_id: "trend:WRESBAL:5obs", name: "准备金", change: 0, unit: "USD bn", as_of: "2026-10-28", previous_as_of: "2026-09-23", window_observations: 5, frequency: "weekly", status: "stale"}
    ],
    comparison_facts: [{fact_id: "comparison:IORB", name: "准备金利率", value: 3.9, change: -0.25, unit: "%", as_of: "2026-10-30", previous_as_of: "2026-10-23", status: "ok"}],
    calendar_facts: [{fact_id: "calendar:7d", window_days: 7, window_start: "2026-10-30", window_end: "2026-11-06", gross_announced_offering_usd_bn: 0, maturities_usd_bn: null, net_cash_impact_usd_bn: null, status: "partial_announced", coverage_note: "仅覆盖已捕获公告；已知金额小计不是完整未来发行预测。"}],
    market_facts: [{fact_id: "market:SP500:20obs", name: "标普500窗口收益", value: 2.5, unit: "%", as_of: "2026-10-29", status: "stale", source_status: "cached_after_fetch_failure"}],
    coverage_facts: [],
    catalog: {
      "trend:SOFR:20obs": {name: "选定来源SOFR", value: 3.94, change: -0.4, unit: "%", change_unit: "percentage points", as_of: "2026-10-30", previous_as_of: "2026-09-30", status: "ok"},
      "metric:IORB": {name: "准备金余额利率", value: 3.9, change: -0.25, unit: "%", as_of: "2026-10-30", previous_as_of: "2026-10-23", status: "ok"}
    }
  };
  context.window.INVESTMENT_FACTS = facts;
  const map = context.investmentFactMap();
  assert.equal(map.get("trend:SOFR:20obs").name, "选定来源SOFR", "Catalog must take precedence over compact facts");
  assert(map.has("comparison:IORB"), "Comparison references must be resolvable");
  const reference = context.investmentFactText(map.get("metric:IORB"));
  assert.match(reference, /准备金余额利率.*2026-10-23 至 2026-10-30.*观测值 3.90 %.*变化 -0.25 个百分点/);
  assert.match(context.investmentFactText(map.get("comparison:IORB")), /-0.25 个百分点/);

  const asset = {liquidity_bias: "支持", confidence: "低", horizon: "2—4周", summary: malicious, transmission: "融资压力缓和", confirmation: "信用未扩大", invalidation: "实际利率转升", coverage_limits: "盈利与杠杆未覆盖", fact_ids: ["trend:SOFR:20obs", "metric:IORB"]};
  context.renderInvestmentAssessment({investment_assessment: {summary: "边际改善", change_summary: "可比观察有限", equities: asset, bitcoin: {}, expectations: {status: "数据不足", summary: "暂无可靠预期基准", fact_ids: []}, scenarios: {base: {path: "维持", trigger: "利差稳定", invalidation: "融资压力放大", fact_ids: ["metric:IORB"]}}, next_checks: ["信用利差"]}});
  const researchText = roots["investment-assessment"].textContent;
  assert(researchText.includes(malicious), "Untrusted source text must remain literal");
  assert(!allNodes(roots["investment-assessment"]).some(node => node.tagName === "img"));
  assert.match(researchText, /BTC/);
  assert.match(researchText, /选定来源SOFR.*准备金余额利率/);
  assert.match(researchText, /变化 -0.25 个百分点/);

  context.renderInvestmentFacts();
  const factText = roots["investment-facts"].textContent;
  assert.match(factText, /20个有效日频观测间隔/);
  assert.match(factText, /5个有效周频观测间隔/);
  assert.match(factText, /-0.40 个百分点/);
  assert.doesNotMatch(factText, /-0.40 %/);
  assert.match(factText, /0.00 十亿美元/);
  assert.match(factText, /未知/);
  assert.match(factText, /已知金额小计不是完整未来发行预测/);
  assert.match(factText, /2.50 %/);
  assert.match(factText, /观测滞后；来源：本次抓取失败，使用缓存/);
  assert.equal(context.investmentStatus("cached_offline"), "离线缓存");

  context.renderResearchReview({records: [{asset: "equities", liquidity_bias: "分化", horizon: "20日", status: "pending", return_pct: null}, {asset: "bitcoin", liquidity_bias: "压制", horizon: "28日", status: "missing_price", return_pct: null}]});
  const pendingText = roots["research-review"].textContent;
  assert.match(pendingText, /样本积累中/);
  assert.match(pendingText, /原始流动性判断/);
  assert.match(pendingText, /缺少价格/);
  assert.match(pendingText, /同一资产、同一观察窗口的持有价格变化，不是策略超额收益/);
  assert.doesNotMatch(pendingText, /胜率/);
  context.renderResearchReview({records: [{asset: "equities", liquidity_bias: "压制", horizon: "20日", status: "available", return_pct: -5, max_drawdown_pct: -10, max_adverse_excursion_pct: -7, benchmark_return_pct: -5}]});
  const matureText = roots["research-review"].textContent;
  assert.match(matureText, /已有1项完成观察/);
  assert.match(matureText, /最大不利变动/);
  assert.match(matureText, /-7.00 %/);
  assert.match(matureText, /压制/);

  // Calendar limitations remain visible even when an older bundle omitted the note.
  context.renderInvestmentFacts({calendar_facts: [{window_days: 84, gross_announced_offering_usd_bn: 277, status: "partial_announced"}]});
  assert.match(roots["investment-facts"].textContent, /不是完整未来发行预测/);

  context.location.protocol = "http:";
  const bundle = {dashboard: {meta: {}}, analysis: {}, investment_facts: facts, research_review: {status: "collecting", records: []}};
  context.fetch = async () => ({ok: true, json: async () => bundle});
  const loaded = await context.loadJson("/output/latest/dashboard_data.json");
  assert.equal(loaded, bundle.dashboard);
  assert.equal(context.window.INVESTMENT_FACTS, facts);
  assert.equal(context.window.RESEARCH_REVIEW, bundle.research_review);
  console.log("PASS: research UI legacy compatibility, source-text safety, catalog/comparison references, rate units, calendar coverage, cached/stale status, review context and bundle loading");
}

main().catch(error => { console.error(error); process.exitCode = 1; });
