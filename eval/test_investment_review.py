"""Offline failure-oriented checks for prospective investment observations."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investment_review import create_research_record, build_research_review, load_published_records


class ResearchReview(unittest.TestCase):
    def record(self, run="one", publication="2026-01-01T12:00:00+08:00", generated="2026-01-01T10:00:00+08:00"):
        return create_research_record(run, {
            "meta": {"model": "test-model", "data_as_of": generated[:10]},
            "investment_assessment": {"equities": {"liquidity_bias": "支持"}, "bitcoin": {"liquidity_bias": "压制"}},
        }, {"generated_at_bjt": generated, "research_version": "3.0"}, publication, "a" * 64)

    def prices(self, start="2025-12-01", days=230, weekdays=False):
        begin = date.fromisoformat(start)
        return [{"date": (begin + timedelta(days=i)).isoformat(), "value": 100.0 + i}
                for i in range(days) if not weekdays or (begin + timedelta(days=i)).weekday() < 5]

    def history(self):
        return {"SP500": self.prices(weekdays=True), "CBBTCUSD": self.prices()}

    def test_no_entry_before_actual_publication_and_no_future_prices(self):
        record = self.record(publication="2026-02-01T12:00:00+08:00")
        review = build_research_review([record], self.history(), "2026-02-04T23:00:00+08:00")
        self.assertEqual(review["evaluation_price_cutoff"], "2026-02-02")
        self.assertTrue(all(row["entry_date"] is None for row in review["records"]))
        self.assertTrue(all(row["status"] == "pending" for row in review["records"]))
        self.assertGreater(review["price_quality"]["SP500"]["future_rows_excluded"], 0)

    def test_weekend_and_calendar_horizons_are_different(self):
        review = build_research_review([self.record()], self.history(), "2026-05-01T12:00:00+08:00")
        stock = next(r for r in review["records"] if r["asset"] == "equities" and r["window"] == 10)
        bitcoin = next(r for r in review["records"] if r["asset"] == "bitcoin" and r["window"] == 14)
        self.assertEqual(stock["entry_date"], "2026-01-05")
        self.assertEqual(stock["exit_date"], "2026-01-19")
        self.assertEqual(bitcoin["entry_date"], "2026-01-03")
        self.assertEqual(bitcoin["exit_date"], "2026-01-17")
        self.assertEqual(stock["return_pct"], stock["benchmark_return_pct"])
        self.assertEqual(bitcoin["status"], "available")

    def test_btc_missing_day_is_not_compressed_into_shorter_window(self):
        history = self.history()
        history["CBBTCUSD"] = [r for r in history["CBBTCUSD"] if r["date"] != "2026-01-08"]
        review = build_research_review([self.record()], history, "2026-05-01T12:00:00+08:00")
        row = next(r for r in review["records"] if r["asset"] == "bitcoin" and r["window"] == 14)
        self.assertEqual(row["status"], "missing_price")
        self.assertIsNone(row["return_pct"])
        self.assertIn("2026-01-08", row["missing_dates"])

    def test_btc_missing_exit_is_explicit(self):
        history = self.history()
        history["CBBTCUSD"] = [r for r in history["CBBTCUSD"] if r["date"] != "2026-01-17"]
        review = build_research_review([self.record()], history, "2026-05-01T12:00:00+08:00")
        row = next(r for r in review["records"] if r["asset"] == "bitcoin" and r["window"] == 14)
        self.assertEqual(row["status"], "missing_price")
        self.assertEqual(row["target_exit_date"], "2026-01-17")

    def test_duplicate_snapshot_preserves_first_assessment(self):
        first = self.record()
        later = self.record("two", "2026-01-02T12:00:00+08:00")
        later["assessment"]["equities"]["liquidity_bias"] = "压制"
        review = build_research_review([later, first], self.history(), "2026-05-01T12:00:00+08:00")
        self.assertEqual(review["independent_record_count"], 1)
        self.assertEqual(review["excluded_duplicate_run_ids"], ["two"])
        self.assertEqual({r["run_id"] for r in review["records"]}, {"one"})
        self.assertEqual({r["liquidity_bias"] for r in review["records"] if r["asset"] == "equities"}, {"支持"})
        self.assertTrue(all(g["conclusion_status"] == "样本不足，持续积累" for g in review["groups"]))

    def test_immutable_assessment_copy(self):
        analysis = {"investment_assessment": {"equities": {"liquidity_bias": "支持"}, "bitcoin": {"liquidity_bias": "中性"}}}
        record = create_research_record("one", analysis, {"generated_at_bjt": "2026-01-01T10:00:00+08:00"}, "2026-01-01T12:00:00+08:00", "b" * 64)
        analysis["investment_assessment"]["equities"]["liquidity_bias"] = "压制"
        self.assertEqual(record["assessment"]["equities"]["liquidity_bias"], "支持")

    def test_bad_and_conflicting_prices_are_excluded(self):
        history = self.history()
        history["CBBTCUSD"] += [{"date": "2026-01-04", "value": 999}, {"date": "bad", "value": 3}, {"date": "2026-01-05", "value": float("nan")}, {"date": "2026-01-06", "value": True}]
        review = build_research_review([self.record()], history, "2026-05-01T12:00:00+08:00")
        self.assertEqual(review["price_quality"]["CBBTCUSD"]["invalid_rows"], 3)
        self.assertIn("2026-01-04", review["price_quality"]["CBBTCUSD"]["conflicting_dates"])
        self.assertEqual(next(r for r in review["records"] if r["asset"] == "bitcoin")["status"], "missing_price")
        json.dumps(review, allow_nan=False)

    def test_empty_history_does_not_imply_neutral_or_success(self):
        review = build_research_review([self.record()], {}, "2026-05-01T12:00:00+08:00")
        self.assertEqual(review["status"], "collecting")
        self.assertTrue(all(r["status"] == "missing_price" for r in review["records"]))

    def test_left_truncated_history_cannot_move_old_entry_forward(self):
        history = {"SP500": self.prices(start="2026-02-01", weekdays=True),
                   "CBBTCUSD": self.prices(start="2026-02-01")}
        review = build_research_review([self.record()], history, "2026-05-01T12:00:00+08:00")
        self.assertTrue(all(r["status"] == "missing_price" for r in review["records"]))
        self.assertTrue(all(r["entry_date"] is None for r in review["records"]))

    def test_btc_missing_entry_cannot_select_later_close(self):
        history = self.history()
        history["CBBTCUSD"] = [r for r in history["CBBTCUSD"] if r["date"] != "2026-01-03"]
        review = build_research_review([self.record()], history, "2026-05-01T12:00:00+08:00")
        self.assertTrue(all(r["status"] == "missing_price" for r in review["records"] if r["asset"] == "bitcoin"))

    def test_max_drawdown_differs_from_entry_adverse_move(self):
        prices = [{"date": (date(2026, 1, 3) + timedelta(days=i)).isoformat(), "value": value}
                  for i, value in enumerate([100, 120, 110] + [130] * 12)]
        review = build_research_review([self.record()], {"CBBTCUSD": prices}, "2026-05-01T12:00:00+08:00")
        row = next(r for r in review["records"] if r["asset"] == "bitcoin" and r["window"] == 14)
        self.assertAlmostEqual(row["max_drawdown_pct"], -8.3333, places=4)
        self.assertEqual(row["max_adverse_excursion_pct"], 0)

    def test_source_date_never_backdates_entry(self):
        record = self.record(publication="2026-03-01T12:00:00+08:00", generated="2025-01-01T10:00:00+08:00")
        self.assertTrue(record["historical_snapshot"])
        review = build_research_review([record], self.history(), "2026-05-01T12:00:00+08:00")
        self.assertTrue(all(r["entry_date"] >= "2026-03-03" for r in review["records"]))

    def test_unpublished_future_record_is_explicitly_excluded(self):
        review = build_research_review([self.record(publication="2026-08-01T12:00:00+08:00")], self.history(), "2026-05-01T12:00:00+08:00")
        self.assertEqual(review["independent_record_count"], 0)
        self.assertEqual(len(review["excluded_records"]), 1)

    def _write_run(self, root, record, previous=None):
        folder = root / "runs" / record["run_id"]
        folder.mkdir(parents=True)
        record = copy.deepcopy(record)
        record["previous_run_id"] = previous
        payload = json.dumps(record).encode("utf-8")
        (folder / "research_record.json").write_bytes(payload)
        manifest = {"run_id": record["run_id"], "previous_run_id": previous,
                    "files": {"research_record.json": hashlib.sha256(payload).hexdigest()}}
        manifest_payload = json.dumps(manifest).encode("utf-8")
        (folder / "manifest.json").write_bytes(manifest_payload)
        return hashlib.sha256(manifest_payload).hexdigest()

    def test_only_published_chain_is_loaded(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "output", prefix="review-test-") as temp:
            root = Path(temp)
            self.assertTrue(root.resolve().is_relative_to((ROOT / "output").resolve()))
            self._write_run(root, self.record("one"))
            digest = self._write_run(root, self.record("two", "2026-01-02T12:00:00+08:00"), "one")
            self._write_run(root, self.record("failed", "2026-01-03T12:00:00+08:00"))
            (root / "current.json").write_text(json.dumps({"run_id": "two", "directory": "runs/two", "previous_run_id": "one", "manifest_sha256": digest}))
            self.assertEqual([r["run_id"] for r in load_published_records(root)], ["one", "two"])
            (root / "runs/one/research_record.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "哈希"):
                load_published_records(root)

    def test_missing_current_is_empty_and_bad_pointer_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "output", prefix="review-test-") as temp:
            root = Path(temp)
            self.assertTrue(root.resolve().is_relative_to((ROOT / "output").resolve()))
            self.assertEqual(load_published_records(root), [])
            (root / "current.json").write_text(json.dumps({"run_id": "one", "directory": "../outside"}))
            with self.assertRaises(ValueError):
                load_published_records(root)

    def test_rollback_to_legacy_does_not_follow_navigation_forward(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "output", prefix="review-test-") as temp:
            root = Path(temp)
            self.assertTrue(root.resolve().is_relative_to((ROOT / "output").resolve()))
            legacy = root / "runs" / "oldB"
            legacy.mkdir(parents=True)
            manifest = json.dumps({"run_id": "oldB", "method_version": "2.0", "files": {}}).encode("utf-8")
            (legacy / "manifest.json").write_bytes(manifest)
            self._write_run(root, self.record("newA"), "oldB")
            (root / "current.json").write_text(json.dumps({
                "run_id": "oldB", "directory": "runs/oldB", "previous_run_id": "newA",
                "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
            }))
            self.assertEqual(load_published_records(root), [])
            digest = self._write_run(root, self.record("newC", "2026-01-03T12:00:00+08:00"), "oldB")
            (root / "current.json").write_text(json.dumps({
                "run_id": "newC", "directory": "runs/newC", "previous_run_id": "oldB",
                "manifest_sha256": digest,
            }))
            self.assertEqual([r["run_id"] for r in load_published_records(root)], ["newC"])


if __name__ == "__main__":
    unittest.main()
