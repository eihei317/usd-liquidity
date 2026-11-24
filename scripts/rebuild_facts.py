"""Rebuild research facts from an isolated run's own frozen inputs, offline."""
import json
import sqlite3
import sys
from contextlib import closing
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.analysis import build_model_input_package
from scripts.dashboard import build_dashboard_data
from scripts.history_audit import rebuild_and_audit
from scripts.jpy_carry import carry_risk, chart_points_jpy, fmt_bp, outputs_from_jpy_history, pct_change, point_before, rebuild_jpy_spreads
from scripts.signals import derive_signals, stance_from_score
from scripts.utils import Metric


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def replay_jpy(conn, payload, generated):
    """Read only active raw yields. Earlier captures may also have a legacy quarantine."""
    if conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='quarantine_jpy_v1'").fetchone():
        # An exact provenance match identifies an original quarantined copy. A later
        # official refresh can contain the same date and value with a new ingest time.
        conn.execute("""
            DELETE FROM jpy_carry_series_ts WHERE (series_id, as_of, value, snapshot_file, ingested_at) IN
            (SELECT series_id, as_of, value, snapshot_file, ingested_at FROM quarantine_jpy_v1
             WHERE series_id IN ('JGB2','JGB5','JGB10','JGB30'))
        """)
    series = rebuild_jpy_spreads(conn, "frozen_history_rebuild", generated)
    for sid in ("JGB2", "JGB5", "JGB10", "JGB30"):
        series[sid] = conn.execute("""
            SELECT as_of, value FROM jpy_carry_series_ts
            WHERE series_id=? AND unit='%' AND value IS NOT NULL AND as_of<=? ORDER BY as_of
        """, (sid, generated[:10])).fetchall()
    overlay = payload["jpy_carry"]
    history = overlay["history"]
    for sid in history.keys() & series.keys():
        history[sid] = chart_points_jpy(series[sid] if sid.startswith("US_JP") else series[sid][-260:])
    for chart in payload.get("charts", []):
        for line in chart.get("series", []):
            if line.get("id") in series:
                line["points"] = chart_points_jpy(series[line["id"]][-260:])
    for card in overlay.get("cards", []):
        sid = card.get("id")
        if sid not in ("US_JP_10Y", "JGB10"):
            continue
        rows = series[sid]
        day, value = rows[-1] if rows else ("NA", None)
        card["as_of"] = day
        if sid == "US_JP_10Y":
            card.update(value_text=fmt_bp(value, 1), change_text="同日收益率之差")
        else:
            card.update(value_text=f"{value:.3f}%" if value is not None else "NA",
                        change_text="逐日 " + fmt_bp((value - rows[-2][1]) * 100) if len(rows) > 1 else "NA")


def replay_chart_signals(conn, charts, jpy_payload, signal_ids, cutoff):
    jpy_charts = {c["id"]: c for c in jpy_payload.get("charts", [])}
    for i, chart in enumerate(charts.get("charts", [])):
        if chart["id"] in jpy_charts:
            charts["charts"][i] = jpy_charts[chart["id"]]
            continue
        dates = [p["date"] for line in chart.get("series", []) for p in line.get("points", []) if p.get("date")]
        for line in chart.get("series", []):
            if line.get("id") not in signal_ids or not dates:
                continue
            rows = conn.execute("""
                SELECT as_of, value FROM derived_signals_ts
                WHERE signal_id=? AND as_of BETWEEN ? AND ? AND value IS NOT NULL ORDER BY as_of
            """, (line["id"], min(dates), cutoff)).fetchall()
            line["points"] = chart_points_jpy(rows)


def update_jpy_summary(jpy, facts):
    overlay = jpy["jpy_carry"]
    compact = facts["jpy_carry"]
    decomposition = {k: v for k, v in compact["cftc_decomposition"].items() if k != "fact_id"}
    overlay["cftc_decomposition"] = decomposition
    indicators = {r["id"]: r for r in compact["indicators"]}
    for card in overlay.get("cards", []):
        sid = card.get("id")
        if sid == "CFTC_JPY":
            row = indicators.get("CFTC_JPY_NET_OI", {})
            net_change = decomposition["net_change"]
            card.update(why=decomposition["text"], as_of=row.get("as_of") or "NA",
                        value_text=f"{row['value']:.1%}" if row.get("value") is not None else "NA",
                        change_text=f"净周变化 {net_change:+,.0f} 手" if net_change is not None else "NA")
        elif sid in ("CFTC_JPY_SHORT_SHARE", "CFTC_JPY_GROSS_SHORT"):
            card["why"] = "空头合约占非商业多空合约合计的比例。" if sid.endswith("SHARE") else "本周非商业交易者持有的日元期货空头合约数。"
    values = {key: row.get("value") for key, row in indicators.items()}
    def prior(sid, days):
        rows = [(r["date"], r["value"]) for r in overlay["history"].get(sid, [])]
        return point_before(rows, rows[-1][0], days) if rows else None
    jgb_prior, fx_prior = prior("JGB10", 60), prior("USDJPY", 20)
    vix = next((r["value"] for r in facts["canonical_metrics"] if r["id"] == "VIXCLS" and r["status"] == "ok"), None)
    overlay["risk"] = carry_risk(values.get("CFTC_JPY_NET_OI"),
                                 (values["JGB10"] - jgb_prior[1]) * 100 if jgb_prior else None,
                                 pct_change(values["USDJPY"], fx_prior[1]) if fx_prior else None,
                                 values.get("USDJPY_VOL20"), vix, values.get("US_JP_10Y"))


def main():
    if ROOT.name != "work" or ROOT.parent.parent.name != "runs":
        raise RuntimeError("离线重建仅可通过 pipeline reanalyze 在新建的隔离运行目录执行。")
    output = ROOT / "output"
    latest = output / "latest"
    db = output / "usd_liquidity.db"
    if not db.is_file():
        raise FileNotFoundError("缺少本次快照的冻结数据库，无法重建历史。")
    snapshot = read(latest / "snapshot.json")
    generated = snapshot["generated_at_bjt"]
    trigger = snapshot.get("trigger", "离线重分析")
    auctions = snapshot.get("upcoming_auctions")
    jpy_path = latest / "jpy_carry_history.json"
    jpy = read(jpy_path) if jpy_path.exists() else {}
    if jpy.get("jpy_carry"):
        with closing(sqlite3.connect(db)) as conn, conn:
            replay_jpy(conn, jpy, generated)
        write(jpy_path, jpy)
    metrics = [Metric(**row) for row in snapshot["metrics"]]
    signals, score, _ = derive_signals(metrics)
    snapshot.update(derived_signals=[asdict(s) for s in signals], score=score, stance=stance_from_score(score))
    write(latest / "snapshot.json", snapshot)
    previous_coverage = read(output / "history_coverage.json") if (output / "history_coverage.json").is_file() else {}
    coverage = rebuild_and_audit(metrics, signals, db)
    audited = {(r["kind"], r["id"]) for r in coverage["series"]}
    for row in previous_coverage.get("series", []):
        if row["kind"] != "market" and (row["kind"], row["id"]) not in audited:
            coverage["series"].append({**row, "observations": 0, "first": None, "last": None, "status": "missing_history"})
    coverage["missing"] = [r["id"] for r in coverage["series"] if r["status"] == "missing_history"]
    write(output / "history_coverage.json", coverage)
    package = build_model_input_package(trigger, generated, metrics, signals, auctions)
    write(latest / "model_input.json", package)
    if jpy.get("jpy_carry"):
        update_jpy_summary(jpy, package["data"]["facts"])
        history, analysis, jpy_input = outputs_from_jpy_history(jpy, trigger)
        write(jpy_path, history)
        write(latest / "jpy_carry_analysis.json", analysis)
        write(latest / "jpy_carry_model_input.json", jpy_input)
    charts = read(latest / "charts.json")
    with closing(sqlite3.connect(db)) as conn:
        replay_chart_signals(conn, charts, jpy, {s.id for s in signals}, generated[:10])
    write(latest / "charts.json", charts)
    dashboard = build_dashboard_data(trigger, generated, snapshot, metrics, signals, charts, [], auctions, allow_jpy_fetch=False)
    dashboard["history_coverage"] = coverage
    write(latest / "dashboard_data.json", dashboard)
    print("已按本次冻结数据重建事实、历史覆盖与图表。", flush=True)


if __name__ == "__main__":
    main()
