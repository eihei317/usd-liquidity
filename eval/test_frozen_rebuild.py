import sqlite3
import sys
import tempfile
import unittest
from contextlib import ExitStack, closing
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import dashboard, jpy_carry
from scripts.rebuild_facts import replay_jpy


def add(conn, sid, day, value, captured="2026-11-20"):
    conn.execute("""
        INSERT INTO jpy_carry_series_ts (series_id, as_of, value, unit, snapshot_file, ingested_at)
        VALUES (?, ?, ?, '%', 'original_snapshot', ?)
    """, (sid, day, value, captured))


class FrozenRebuild(unittest.TestCase):
    def test_quarantined_copy_stays_out_and_official_recapture_survives(self):
        with closing(sqlite3.connect(":memory:")) as conn:
            jpy_carry.ensure_jpy_carry_table(conn)
            for sid in ("DGS10", "JGB10"):
                for day, rate in [("2026-11-17", 2), ("2026-11-18", 2.1)]:
                    add(conn, sid, day, rate + (2 if sid == "DGS10" else 0))
            conn.execute("CREATE TABLE quarantine_jpy_v1 AS SELECT * FROM jpy_carry_series_ts WHERE series_id='JGB10'")
            conn.execute("UPDATE jpy_carry_series_ts SET ingested_at='2026-11-23' WHERE series_id='JGB10' AND as_of='2026-11-18'")
            add(conn, "DGS10", "2026-11-20", 4.6)
            add(conn, "JGB10", "2026-11-24", 2.8)
            add(conn, "JGB10", "2026-11-25", 2.9)
            add(conn, "DGS10", "2026-11-25", 4.9)
            j = {"jpy_carry": {"history": {"JGB10": [], "US_JP_10Y": []},
                 "cards": [{"id": "JGB10"}, {"id": "US_JP_10Y"}]}, "charts": [{"series": [{"id": "US_JP_10Y"}]}]}
            for _ in range(2):
                replay_jpy(conn, j, "2026-11-24 16:00:00")
                self.assertEqual([r["date"] for r in j["jpy_carry"]["history"]["JGB10"]], ["2026-11-18", "2026-11-24"])
                spread = j["jpy_carry"]["history"]["US_JP_10Y"]
                self.assertEqual(j["charts"][0]["series"][0]["points"], spread)
                self.assertEqual([r["date"] for r in spread], ["2026-11-18"])
                self.assertAlmostEqual(spread[0]["value"], 200)
                self.assertEqual(j["jpy_carry"]["cards"][1]["as_of"], "2026-11-18")
                self.assertEqual(conn.execute("SELECT count(*) FROM quarantine_jpy_v1").fetchone()[0], 2)

    def test_live_builder_joins_fresh_us_yield_to_previously_captured_jgb(self):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as mocks:
            root = Path(tmp)
            (root / "output").mkdir()
            mocks.enter_context(patch.object(jpy_carry, "ROOT", root))
            for name in ("fetch_boj_series", "fetch_bis_neer", "fetch_cnbc_jgb", "fetch_cftc_jpy"):
                mocks.enter_context(patch.object(jpy_carry, name, side_effect=ValueError("fixture: unavailable")))
            mocks.enter_context(patch.object(jpy_carry, "fetch_mof_jgb", return_value=({"JGB10": [("2026-11-24", 2.717)]}, {})))
            mocks.enter_context(patch.object(jpy_carry, "fetch_fred_series_jpy",
                                side_effect=lambda sid, _: [("2026-11-18", 5.07), ("2026-11-20", 5.1)] if sid == "DGS10" else []))
            with closing(sqlite3.connect(root / "output/usd_liquidity.db")) as conn, conn:
                jpy_carry.ensure_jpy_carry_table(conn)
                add(conn, "JGB10", "2026-11-18", 2.884)
            # Capture clock is independent of the machine running this regression.
            from datetime import datetime
            mocks.enter_context(patch.object(jpy_carry, "now_bjt", return_value=datetime.fromisoformat("2026-11-24T16:00:00+08:00")))
            history, analysis, model_input = jpy_carry.build_payload("frozen upstream responses")
            card = next(c for c in history["jpy_carry"]["cards"] if c["id"] == "US_JP_10Y")
            self.assertEqual((card["value_text"], card["as_of"]), ("218.6bp", "2026-11-18"))
            spread = next(m for m in analysis["dashboard_modules"] if m["module"] == "美日利差")
            self.assertEqual(spread["as_of"], card["as_of"])
            self.assertEqual(model_input["data"], history)

    def test_missing_frozen_jpy_never_falls_back_to_network(self):
        with patch.object(dashboard, "load_jpy_carry_history_payload", return_value=None), \
             patch.object(dashboard, "fetch_fred_series_points", side_effect=AssertionError("network")), \
             patch.object(dashboard, "fetch_cftc_jpy_position", side_effect=AssertionError("network")):
            self.assertEqual(dashboard.build_jpy_carry_overlay([], [], allow_fetch=False)["status"], "missing")


if __name__ == "__main__":
    unittest.main()
