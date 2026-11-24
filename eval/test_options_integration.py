"""Exercise actual prepare_research persistence and replay with wholly synthetic captures."""
import copy
import json
import shutil
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import option_chain, options_research, pipeline
from scripts.analysis_validator import _collect_facts
from scripts.option_positioning import DATASETS, MARKET_CODE

STAMP = "2026-11-24 20:00:00 UTC+08:00"
MODEL = options_research.MODEL_ID
POSITION = options_research.POSITION_ID
GROSS = "option:SPX:gross_gamma_1pct"
SHORT = "option:SPX:gamma_share_7d"


def prices():
    days = [date(2026, 10, 1) + timedelta(days=i) for i in range(50)]
    closes = [{"date": d.isoformat(), "value": 5000} for d in days if d.weekday() < 5]
    closes.extend([{"date": "2026-11-20", "value": 5000}, {"date": "2026-11-23", "value": 5030}])
    return {"generated_at_bjt": STAMP, "series": {sid: {"status": "ok"} for sid in ("SP500", "NASDAQCOM", "CBBTCUSD")},
            "price_history": {sid: copy.deepcopy(closes) for sid in ("SP500", "NASDAQCOM", "CBBTCUSD")}}


def positioning():
    source = {}
    for kind, (dataset, marker) in DATASETS.items():
        rows = []
        for i, (day, multiplier) in enumerate([("2026-11-03", 250), ("2026-11-10", 50), ("2026-11-17", 50)]):
            rows.append({"id": marker + day, "report_date_as_yyyy_mm_dd": day,
                         "cftc_contract_market_code": MARKET_CODE, "futonly_or_combined": marker,
                         "contract_market_name": "S&P 500 Consolidated", "contract_units": f"(S&P 500 INDEX X ${multiplier})",
                         "open_interest_all": 200 if kind == "combined" else 140 - i,
                         "dealer_positions_long_all": 100 + 3 * i if kind == "combined" else 90 + i,
                         "dealer_positions_short_all": 80 if kind == "combined" else 75})
        source[kind] = {"status": "ok", "dataset_id": dataset, "market_code": MARKET_CODE, "rows": rows,
                        "captured_at_bjt": STAMP}
    return {"status": "ok", "generated_at_bjt": STAMP, "market_code": MARKET_CODE, "sources": source}


def local_file(day, oi=10, released=None, source="Example Exchange"):
    observed = f"2026-11-{day}T15:45:00-05:00"
    return {"schema_version": 1, "source": source, "source_url": "https://example.com/vendor",
            "allowed_aggregate_destination": option_chain.DESTINATION, "underlying": "SPX", "scope": option_chain.SCOPE,
            "observed_at": observed, "available_at": released or observed, "open_interest_as_of": "2026-11-19",
            "gamma_unit": "delta_per_index_point", "complete_chain": True, "spot": 5000, "contract_multiplier": 100,
            "contracts": [{"root": "SPXW", "right": "C", "expiration": "2026-11-27", "strike": 5000,
                           "gamma": .001, "open_interest": oi, "client_reference": "PRIVATE_LINE_ITEM"}]}


class OptionIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.latest = self.root / "runs" / "new" / "work" / "output" / "latest"
        self.latest.mkdir(parents=True)
        self.local = self.root / ".workbuddy/option_chains"
        self.local.mkdir(parents=True)
        shutil.copytree(ROOT / "prompts", self.root / "prompts")
        self.db = self.latest.parent / "usd_liquidity.db"
        self.context = prices()
        self.pos = positioning()
        vix = {"id": "VIXCLS", "fact_id": "metric:VIXCLS", "unit": "index", "source": "FRED",
               "status": "ok", "value": 24, "as_of": "2026-11-23", "frequency": "daily"}
        pipeline.atomic(self.latest / "model_input.json", {"generated_at_bjt": STAMP,
                        "data": {"facts": {"canonical_metrics": [vix], "event_facts": {"status": "missing"}}}})
        history = [{"date": "2026-11-20", "value": 20}, {"date": "2026-11-23", "value": 24}]
        pipeline.atomic(self.latest / "snapshot.json", {"generated_at_bjt": STAMP, "metrics": [{**vix, "extra": {"history": history}}]})
        for name in ("dashboard_data.json", "charts.json"):
            pipeline.atomic(self.latest / name, {"charts": [{"id": "other_chart"}, {"id": "options_obsolete"}]})
        pipeline.atomic(self.latest.parent / "history_coverage.json", {"series": [], "missing": []})

    def prepare(self, fetch):
        with patch.object(pipeline, "ROOT", self.root):
            if fetch:
                with patch("scripts.investment_facts.build_market_context", return_value=copy.deepcopy(self.context)), \
                     patch("scripts.option_positioning.capture_positioning", return_value=copy.deepcopy(self.pos)):
                    return pipeline.prepare_research(self.latest, fetch=True)[0]
            with patch("scripts.option_chain.load_chain_history", side_effect=AssertionError("read mutable chain on replay")), \
                 patch("scripts.option_positioning.capture_positioning", side_effect=AssertionError("network on replay")), \
                 patch("scripts.investment_facts.http_get_text", side_effect=AssertionError("market fetch on replay")):
                return pipeline.prepare_research(self.latest, fetch=False)[0]

    def history(self, fid):
        with closing(sqlite3.connect(self.db)) as conn:
            return conn.execute("SELECT as_of,value,contract_multiplier FROM option_indicator_history WHERE series_id=? ORDER BY as_of", (fid,)).fetchall()

    def audit(self):
        return pipeline.read(self.latest.parent / "history_coverage.json")

    def charts(self):
        charts = pipeline.read(self.latest / "charts.json")["charts"]
        self.assertEqual(charts, pipeline.read(self.latest / "dashboard_data.json")["charts"])
        self.assertEqual(len(charts), len({r["id"] for r in charts}))
        return {r["id"]: r for r in charts}

    def test_capture_artifacts_match_and_replay_ignores_changed_private_file(self):
        pipeline.atomic(self.local / "first.json", local_file("20"))
        pipeline.atomic(self.local / "latest.json", local_file("23", 12))
        pipeline.atomic(self.local / "future.json", local_file("23", 999, "2026-11-25T05:00:00-05:00"))
        package = self.prepare(True)
        facts, duplicates = _collect_facts(package)
        self.assertFalse(duplicates)
        self.assertEqual(facts[GROSS]["value"], 300000)
        self.assertTrue(all(fid in facts for fid in facts[MODEL]["base_fact_ids"]))
        self.assertEqual(facts[POSITION]["value"], 9)
        self.assertEqual(facts[POSITION]["change"], 2)
        spread, share = facts[options_research.SPREAD_ID], facts[options_research.OI_SHARE_ID]
        self.assertEqual(spread["vix_pct"], 24)
        self.assertAlmostEqual(spread["value"], spread["vix_pct"] - spread["realized_vol_pct"])
        self.assertEqual(share["value"], 31)
        self.assertAlmostEqual(share["change"], .5)
        self.assertEqual(share["reference"]["count"], 1)
        self.assertIsNone(share["reference"]["percentile"])
        self.assertGreater(len(self.history(options_research.REALIZED_ID)), len(self.history(options_research.SPREAD_ID)))
        self.assertEqual(self.history(GROSS), [("2026-11-20", 250000, None), ("2026-11-23", 300000, None)])
        self.assertEqual(len(self.history(MODEL)), 2)
        self.assertEqual([r[2] for r in self.history(POSITION)], [250, 50, 50])
        charts = self.charts()
        self.assertIn("other_chart", charts)
        self.assertNotIn("options_obsolete", charts)
        shown = charts["options_dealer_option_delta"]["series"][0]["points"]
        self.assertEqual([r["date"] for r in shown], ["2026-11-10", "2026-11-17"])
        self.assertEqual(charts["options_iv_minus_rv21"]["series"][0]["points"][-1]["value"], spread["value"])
        self.assertEqual(charts["options_option_oi_share"]["series"][0]["points"][-1]["value"], share["value"])
        self.assertEqual(charts["options_gross_gamma_1pct"]["series"][0]["points"][-1]["value"], facts[GROSS]["value"])
        pipeline.require_history_complete(self.audit())
        captured = (self.latest / "options_capture.json").read_bytes()
        self.assertNotIn(b"PRIVATE_LINE_ITEM", captured)
        self.assertNotIn(b"allowed_aggregate_destination", captured)
        self.assertNotIn(b"PRIVATE_LINE_ITEM", (self.latest / "model_input.json").read_bytes())
        pipeline.atomic(self.local / "latest.json", local_file("23", 888))
        replay = self.prepare(False)
        self.assertEqual(captured, (self.latest / "options_capture.json").read_bytes())
        self.assertEqual(_collect_facts(replay)[0][GROSS], facts[GROSS])

    def test_revisions_missing_legs_and_later_incomplete_chain_remove_obsolete_values(self):
        pipeline.atomic(self.local / "first.json", local_file("20"))
        pipeline.atomic(self.local / "latest.json", local_file("23", 12))
        self.prepare(True)
        pipeline.atomic(self.local / "amended.json", local_file("20", 14, "2026-11-23T16:00:00-05:00"))
        pipeline.atomic(self.local / "withdrawn.json", local_file("23", None, "2026-11-23T18:00:00-05:00"))
        self.context["price_history"]["SP500"].pop(-2)
        self.pos["sources"]["futures_only"]["rows"].pop(1)
        package = self.prepare(True)
        self.assertEqual(self.history(GROSS), [("2026-11-20", 350000, None)])
        self.assertEqual(len(self.history(SHORT)), 1)
        self.assertEqual([r[0] for r in self.history(MODEL)], ["2026-11-23"])
        self.assertEqual([r[0] for r in self.history(POSITION)], ["2026-11-03", "2026-11-17"])
        with closing(sqlite3.connect(self.db)) as conn:
            raw_legs = conn.execute("""SELECT report, dealer_long, dealer_short FROM option_cftc_source_history
                                       WHERE as_of='2026-11-10'""").fetchall()
        self.assertEqual(raw_legs, [("combined", 103, 80)])
        with closing(sqlite3.connect(self.db)) as conn:
            oi_legs = conn.execute("SELECT report,open_interest FROM option_cftc_open_interest_history WHERE as_of='2026-11-10'").fetchall()
        self.assertEqual(oi_legs, [("combined", 200)])
        self.assertFalse(self.history(options_research.SPREAD_ID))
        self.assertEqual([row[0] for row in self.history(options_research.OI_SHARE_ID)], ["2026-11-03", "2026-11-17"])
        options = package["data"]["facts"]["investment"]["options"]
        self.assertEqual((options["chain"]["status"], options["chain"]["facts"]), ("partial", []))
        self.assertIsNone(options["positioning"]["change"])
        self.assertIsNone(options["positioning"]["previous_as_of"])
        self.assertIsNone(options["open_interest_share"]["change"])
        self.assertEqual(options["open_interest_share"]["reference"]["count"], 0)
        self.assertEqual(self.audit()["option_details"]["positioning"]["missing_futures_only_dates"], ["2026-11-10"])
        self.assertEqual(self.charts()["options_gross_gamma_1pct"]["series"][0]["points"], [{"date": "2026-11-20", "value": 350000}])
        self.context["price_history"]["SP500"].clear()
        self.prepare(True)
        self.assertFalse(self.history(MODEL))
        self.assertNotIn("options_model_delta_change_1pct", self.charts())

    def test_required_sources_block_publish_but_optional_chain_gaps_are_preserved(self):
        self.prepare(True)
        audit = self.audit()
        self.assertTrue(set(options_research.CHAIN_SERIES).issubset(audit["missing"]))
        pipeline.require_history_complete(audit)
        self.pos["sources"]["combined"]["status"] = "error"
        self.prepare(True)
        audited = self.audit()
        self.assertGreater(len(self.history(POSITION)), 1)
        with self.assertRaises(RuntimeError):
            pipeline.require_history_complete(audited)
        self.pos = positioning()
        self.context["series"]["SP500"]["status"] = "cached_after_fetch_failure"
        self.prepare(True)
        self.assertGreater(len(self.history(MODEL)), 1)
        with self.assertRaises(RuntimeError):
            pipeline.require_history_complete(self.audit())

    def test_replay_of_older_capture_does_not_import_present_day_chain_or_cftc(self):
        pipeline.atomic(self.local / "first.json", local_file("20"))
        self.prepare(True)
        current = pipeline.read(self.latest / "model_input.json")
        current["generated_at_bjt"] = "2026-11-23 19:00:00 UTC+08:00"
        pipeline.atomic(self.latest / "model_input.json", current)
        p = self.prepare(False)
        option = p["data"]["facts"]["investment"]["options"]
        self.assertIsNone(option["positioning"]["value"])
        self.assertFalse(option["chain"]["facts"])
        self.assertFalse(self.history(GROSS))
        self.assertFalse(self.history(POSITION))

    def test_two_sources_for_the_same_capture_cannot_be_resolved_by_filename(self):
        pipeline.atomic(self.local / "a.json", local_file("23", 10, source="Provider A"))
        pipeline.atomic(self.local / "b.json", local_file("23", 24, source="Provider B"))
        p = self.prepare(True)
        option = p["data"]["facts"]["investment"]["options"]
        self.assertFalse(option["chain"]["facts"])
        self.assertFalse(self.history(GROSS))

    def test_reference_compares_only_earlier_observations_including_ties(self):
        points = [{"date": str(i), "value": value, "change": 1} for i, value in enumerate((10, 1, 2, 4, 2))]
        ref = options_research._prior_reference(points, 3)
        self.assertEqual((ref["start"], ref["end"], ref["high"], ref["at_or_below"]), ("1", "3", 4, 2))
        self.assertAlmostEqual(ref["percentile"], 200 / 3)
        points[-2]["change"] = None
        ref = options_research._prior_reference(points, 3, weekly=True)
        self.assertEqual(ref["count"], 1)
        self.assertIsNone(ref["percentile"])


if __name__ == "__main__":
    unittest.main()
