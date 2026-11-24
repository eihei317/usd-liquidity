"""Frozen inputs for policy effective dates, Treasury settlements and cross-run prices."""
import copy
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.db import TABLE_DEFS
from scripts.investment_facts import enrich_package


def metric(mid, points):
    return {"id": mid, "fact_id": f"metric:{mid}", "name": mid, "frequency": "daily", "unit": "%",
            "source": "official", "status": "ok", "as_of": points[-1][0], "value": points[-1][1],
            "extra": {"history": [{"date": d, "value": v} for d, v in points]}}


def frozen(day, metrics=(), prices=None, events=(), status="ok"):
    generated = day + " 12:00:00 UTC+08:00"
    canonical = [{k: copy.deepcopy(v) for k, v in r.items() if k != "extra"} for r in metrics]
    package = {"generated_at_bjt": generated, "data": {"facts": {"canonical_metrics": canonical,
               "event_facts": {"as_of": day, "status": status, "upcoming_auctions": list(events)}}}}
    context = {"series": {}, "price_history": {}}
    for sid, (d, v, source_status) in (prices or {}).items():
        context["price_history"][sid] = [{"date": d, "value": v}]
        context["series"][sid] = {"status": source_status}
    return package, {"generated_at_bjt": generated, "metrics": list(metrics), "investment_market_context": context}


def event(cusip, auction="2026-11-23", issue="2026-11-27", amount=95):
    return {"fact_id": f"event:auction:{auction}:Bill:13-Week:{cusip}", "cusip": cusip, "auction_date": auction,
            "issue_date": issue, "security_type": "Bill", "security_term": "13-Week", "gross_announced_offering_usd_bn": amount}


def add_capture(db, stamp, calendar, rows):
    with closing(sqlite3.connect(db)) as conn:
        conn.execute(next(t["create"] for t in TABLE_DEFS if t["name"] == "treasury_auctions_ts"))
        for row in rows:
            conn.execute("""INSERT INTO treasury_auctions_ts
                (snapshot_file, ingested_at, calendar_as_of, auction_date, issue_date, announcement_date,
                 security_type, security_term, cusip, offering_amount_bn, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ok')""",
                (f"usd_liquidity_snapshot_{stamp}.json", calendar, calendar, row["auction_date"], row["issue_date"],
                 row.get("announcement_date", calendar), row["security_type"], row["security_term"],
                 row["cusip"], row["gross_announced_offering_usd_bn"]))
        conn.commit()


class DataContinuity(unittest.TestCase):
    def test_future_policy_endpoint_is_separate_and_join_ends_on_last_common_date(self):
        days = [f"2026-11-{i:02d}" for i in range(11, 19)]
        anchor = metric("IORB", [(d, 3.9) for d in days] + [("2026-11-21", 4.2)])
        sofr = metric("SOFR", [(d, 3.91) for d in days] + [("2026-11-20", 4.15)])
        p, s = frozen("2026-11-20", [anchor, sofr])
        raw = copy.deepcopy(s)
        facts = enrich_package(p, s)["data"]["facts"]
        rate = facts["canonical_metrics"][0]
        self.assertEqual((rate["as_of"], rate["value"], rate["stale_days"]), (days[-1], 3.9, 2))
        self.assertEqual((rate["previous_as_of"], rate["change"]), (days[-2], 0))
        self.assertEqual(rate["reported_future_endpoint"]["value"], 4.2)
        self.assertEqual(rate["history_summary"]["5"]["end"], days[-1])
        trend = next(t for t in facts["investment"]["trend_facts"] if t["id"] == "SOFR_IORB")
        self.assertAlmostEqual(trend["value"], 1)
        self.assertEqual((trend["as_of"], trend["stale_days"], trend["status"]), (days[-1], 2, "stale"))
        self.assertFalse(trend["matches_latest_sofr"])
        self.assertEqual(trend["matched_observations"], len(days))
        original = copy.deepcopy(facts)
        self.assertEqual(enrich_package(p, s)["data"]["facts"], original)
        self.assertEqual(s, raw)

    def test_future_only_rate_keeps_effective_value_unknown(self):
        anchor = metric("IORB", [("2026-11-23", 4.2)])
        p, s = frozen("2026-11-22", [anchor])
        facts = enrich_package(p, s)["data"]["facts"]
        self.assertIsNone(facts["canonical_metrics"][0]["value"])
        self.assertEqual(facts["canonical_metrics"][0]["status"], "missing")
        self.assertEqual(facts["investment"]["trend_facts"], [])

    def test_legacy_previous_rate_uses_only_its_own_frozen_input(self):
        previous, previous_raw = frozen("2026-11-21", [metric("IORB", [("2026-11-21", 3.8), ("2026-11-23", 4.2)])])
        untouched = copy.deepcopy(previous)
        p, s = frozen("2026-11-22", [metric("IORB", [("2026-11-21", 3.9), ("2026-11-22", 4.0), ("2026-11-23", 4.2)])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snapshot.json"
            path.write_text(json.dumps(previous_raw), encoding="utf-8")
            row = enrich_package(p, s, previous, previous_snapshot=path)["data"]["facts"]["investment"]["comparison_facts"][0]
        self.assertEqual((row["previous"], row["value"], row["previous_stale_days_at_capture"]), (3.8, 4.0, 0))
        self.assertEqual(previous, untouched)
        for unavailable in (None, s):
            self.assertFalse(enrich_package(p, s, previous, previous_snapshot=unavailable)["data"]["facts"]["investment"]["comparison_facts"])

    def test_archived_auctions_respect_amendments_withdrawals_reopenings_and_capture_time(self):
        a = event("AAA")
        reopened = event("AAA", auction="2026-11-22", amount=10)
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "history.db"
            add_capture(db, "20261120_123000", "2026-11-20", [a, reopened, event("DROP"), event("MOVE"), event("UNKNOWN")])
            add_capture(db, "20261121_133000", "2026-11-21", [dict(a, gross_announced_offering_usd_bn=96), reopened,
                        event("MOVE", issue="2026-12-11", amount=50), event("UNKNOWN", amount=None),
                        event("VANISHED", auction="2026-11-25")])
            add_capture(db, "20261124_160000", "2026-11-24", [event("LATER", auction="2026-11-22", amount=999)])
            p, s = frozen("2026-11-24", events=[event("FRESH", auction="2026-11-25", amount=4)])
            facts = enrich_package(p, s, history_db=db)["data"]["facts"]
        week, month = facts["investment"]["calendar_facts"][:2]
        self.assertEqual((week["event_count"], week["previously_captured_count"], week["value"]), (4, 3, 110))
        self.assertEqual((week["unknown_amount_count"], week["gross_amounts_complete_for_listed_events"]), (1, False))
        self.assertIsNone(week["net_cash_impact_usd_bn"])
        self.assertEqual(month["value"], 160)
        all_sources = facts["event_facts"]["upcoming_auctions"] + facts["event_facts"]["previously_announced_settlements"]
        self.assertEqual(len({r["fact_id"] for r in all_sources}), len(all_sources))
        self.assertEqual(set(month["base_fact_ids"]), {r["fact_id"] for r in all_sources})

    def test_failed_calendar_retains_known_events_and_unknown_amounts(self):
        previous, _ = frozen("2026-11-22", events=[event("KNOWN", amount=None)])
        p, s = frozen("2026-11-23", status="missing")
        s["upcoming_auctions"] = {"as_of": "2026-11-23", "status": "error", "auctions": []}
        week = enrich_package(p, s, previous)["data"]["facts"]["investment"]["calendar_facts"][0]
        self.assertEqual((week["event_count"], week["unknown_amount_count"]), (1, 1))
        self.assertEqual((week["source_status"], week["status"]), ("error", "historical_after_source_failure"))
        self.assertIsNone(week["value"])

    def test_prices_distinguish_revision_unchanged_and_new_observations(self):
        previous, s = frozen("2026-11-19", prices={sid: ("2026-11-17", 100, "ok") for sid in ("SP500", "NASDAQCOM", "CBBTCUSD")})
        enrich_package(previous, s)
        p, s = frozen("2026-11-24", prices={"SP500": ("2026-11-17", 101, "ok"),
                       "NASDAQCOM": ("2026-11-17", 100, "cached_after_fetch_failure"),
                       "CBBTCUSD": ("2026-11-23", 105, "ok")})
        facts = enrich_package(p, s, previous)["data"]["facts"]["investment"]
        r = {v["id"]: v for v in facts["comparison_facts"]}
        self.assertEqual((r["SP500"]["comparison_kind"], r["SP500"]["change"], r["SP500"]["status"]), ("revision_same_observation_date", 1, "stale"))
        self.assertEqual((r["NASDAQCOM"]["comparison_kind"], r["NASDAQCOM"]["source_status"], r["NASDAQCOM"]["stale_days"]), ("unchanged", "cached_after_fetch_failure", 7))
        self.assertEqual((r["CBBTCUSD"]["comparison_kind"], r["CBBTCUSD"]["base_fact_ids"], r["CBBTCUSD"]["unit"]), ("new_observation", ["market:CBBTCUSD:level"], "USD"))
        previous["data"]["facts"]["investment"]["market_facts"][0]["source_url"] = "another-series"
        self.assertNotIn("SP500", {v["id"] for v in enrich_package(p, s, previous)["data"]["facts"]["investment"]["comparison_facts"]})


if __name__ == "__main__":
    unittest.main()
