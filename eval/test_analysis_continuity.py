"""Regression cases for daily evidence using different capture and observation dates."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import pipeline
from scripts.analysis import _build_derived_facts, analysis_output_contract
from scripts.signals import derive_signals
from scripts.utils import Metric


def metric(mid, day, value, previous_day=None, previous=None, history=()):
    return Metric(mid, mid, "test", value, previous, None if previous is None else value - previous,
                  "USD bn" if mid == "SOFR_VOLUME" else "%", day, previous_day, "daily", "test", "",
                  extra={"history": [{"date": d, "value": v} for d, v in history]})


def signals(metrics):
    result, _, _ = derive_signals(metrics)
    return {s.id: s for s in result}


class FundingObservations(unittest.TestCase):
    def test_financing_cost_uses_size_on_both_rate_fixing_dates(self):
        rows = [metric("SOFR", "2026-07-24", 4.2, "2026-07-23", 4.1),
                metric("IORB", "2026-07-25", 5, "2026-07-24", 4, [("2026-07-23", 4)]),
                metric("SOFR_VOLUME", "2026-07-25", 800, "2026-07-24", 720, [("2026-07-23", 360)])]
        value = signals(rows)["SOFR_VOLUME_IMPACT"]
        self.assertEqual("2026-07-24", value.as_of)
        self.assertAlmostEqual(4, value.value)
        self.assertAlmostEqual(1, value.previous)
        facts, _ = _build_derived_facts([value], rows)
        self.assertEqual("2026-07-23", facts[0]["previous_as_of"])
        self.assertIsNone(signals(rows[:2])["SOFR_VOLUME_IMPACT"].value)

    def test_missing_dates_and_mixed_windows_do_not_form_spreads(self):
        self.assertIsNone(signals([metric("SOFR", None, 5), metric("IORB", None, 4)])["SOFR_ANCHOR"].value)
        rows = [metric(mid, "2026-07-24", 4, "2026-07-23", 3.95) for mid in ("DGS1","DGS3","DGS5","DGS7")]
        self.assertAlmostEqual(5, signals(rows)["UST_BELLY_MOMENTUM"].value)
        rows[0].previous_as_of = "2026-07-22"
        self.assertIsNone(signals(rows)["UST_BELLY_MOMENTUM"].value)
        self.assertIsNotNone(signals(rows)["UST_1Y_CHANGE_BP"].value)
        self.assertIsNone(signals([metric("TBILL_AUCTION_SIZE", "2026-07-24", 120),
                                   metric("TBILL_AUCTION_BTC", "2026-07-23", 2.5)])["TBILL_AUCTION_STRESS"].value)

    def test_equal_policy_rate_and_tga_from_own_capture(self):
        rows = [metric("SOFR", "2026-07-24", 4), metric("IORB", "2026-07-24", 4),
                metric("TGA", "2026-07-24", 300, "2026-07-23", 280, [("2026-07-22", 250)])]
        self.assertEqual("中性", signals(rows)["SOFR_ANCHOR"].severity)
        self.assertEqual(30, signals(rows)["TGA_FLOW"].previous)


class ComparisonBaseline(unittest.TestCase):
    def test_frozen_market_context_excludes_later_retrieval(self):
        stamp = "2026-07-24 20:00:00 UTC+08:00"
        saved = {"generated_at_bjt": stamp, "series": {"SP500": {"status": "cached_after_fetch_failure"}}}
        self.assertIs(saved, pipeline.market_context_for_capture(stamp, saved, False))
        future = {"generated_at_bjt": "2026-07-23", "retrieved_at_bjt": "2026-07-26",
                  "price_history": {"SP500": [{"date": "2026-07-22", "value": 100}]},
                  "series": {"SP500": {"source": "FRED public CSV"}}}
        self.assertEqual([], pipeline.market_context_for_capture(stamp, future, False)["price_history"]["SP500"])

    def test_export_line_endings_recover_only_exact_original_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "model_input.json"
            path.write_bytes(b'{\n}\n')
            original = b'{\r\n}\r\n'
            digest = hashlib.sha256(original).hexdigest()
            self.assertEqual(original, pipeline.verified_json_bytes(path, digest, exported=True))
            with self.assertRaises(ValueError):
                pipeline.verified_json_bytes(path, digest)
            path.write_bytes(b'{"updated":1}\n')
            with self.assertRaises(ValueError):
                pipeline.verified_json_bytes(path, digest, exported=True)

    def test_skip_same_capture_and_future_on_manifest_chain(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(pipeline, "OUT", Path(folder)):
            for rid, stamp, predecessor in (("first","2026-07-22",None), ("capture","2026-07-23","first"),
                                              ("repeat","2026-07-23","capture"), ("future","2026-07-26","repeat")):
                run = Path(folder) / "runs" / rid
                latest = run / "work/output/latest"
                latest.mkdir(parents=True)
                raw = json.dumps({"generated_at_bjt": stamp}).encode()
                (latest / "model_input.json").write_bytes(raw)
                (run / "manifest.json").write_text(json.dumps({"run_id":rid, "input_sha256":hashlib.sha256(raw).hexdigest(),
                                                               "previous_run_id":predecessor}))
            package, snapshot = pipeline.comparison_baseline("future", "2026-07-23")
            self.assertEqual("2026-07-22", package["generated_at_bjt"])
            self.assertIn("first", snapshot.parts)
            self.assertEqual((None, None), pipeline.comparison_baseline("first", "2026-07-22"))
            (snapshot.parent / "model_input.json").write_bytes(b"{}")
            with self.assertRaisesRegex(ValueError, "哈希"):
                pipeline.comparison_baseline("capture", "2026-07-23")

    def test_prompt_and_evidence_contract_use_one_number_policy(self):
        c = analysis_output_contract()
        self.assertIn("结构化事实", c["number_format_rule"])
        for key in ("indicator_mention_rule", "number_format_rule", "freshness_evidence_rule"):
            self.assertNotIn("必须写成 数量", c[key])


if __name__ == "__main__":
    unittest.main()
