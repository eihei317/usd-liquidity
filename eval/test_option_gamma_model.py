import math
import sys
import unittest
from pathlib import Path
from statistics import NormalDist

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.option_gamma_model import build_standard_gamma_history, standard_gamma


class StandardGamma(unittest.TestCase):
    def test_against_finite_difference_with_strike_held_fixed(self):
        normal = NormalDist()
        spot, strike, vol_time = 5500.0, 5500.0, 0.20 * math.sqrt(30 / 365)

        def delta(spot_bump, put):
            d1 = (math.log((spot + spot_bump) / strike) + 0.5 * vol_time**2) / vol_time
            return normal.cdf(d1) - int(put)

        result = standard_gamma(spot, 20)
        for put in (True, False):
            step = spot / 100_000
            numerical_gamma = (delta(step, put) - delta(-step, put)) / (2 * step)
            self.assertAlmostEqual(result["gamma_per_point"], numerical_gamma, places=9)
            self.assertAlmostEqual(result["value"], numerical_gamma * 0.01 * spot * 100, places=6)
        self.assertGreater(result["value"], 6)
        self.assertLess(result["value"], 7)
        self.assertNotAlmostEqual(result["value"], 100 * (delta(.01 * spot, False) - delta(0, False)), places=2)

    def test_units_and_invalid_inputs(self):
        base = standard_gamma(5000, 20)
        higher_spot = standard_gamma(10000, 20)
        self.assertEqual(base["value"], higher_spot["value"])
        self.assertEqual(base["gamma_per_point"] / 2, higher_spot["gamma_per_point"])
        self.assertLess(standard_gamma(5000, 40)["value"], base["value"])
        for bad in (None, False, -1, 0, math.inf, math.nan, "20"):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                standard_gamma(bad, 20)
            with self.subTest(value=bad), self.assertRaises(ValueError):
                standard_gamma(5000, bad)

    def test_all_common_dates_revision_deletion_and_gaps(self):
        d1, d2, d3, d4, future = ("2026-11-16", "2026-11-17", "2026-11-18", "2026-11-19", "2026-11-24")
        spot = [(d1, 5000), (d2, 5100), (d3, 5200), (d4, 5300), (future, 9999)]
        vix = [{"as_of": d1, "value": 20, "captured_at_bjt": "2026-11-19T20:00:00+08:00"},
               (d3, 22), (d4, 23), (future, 79)]
        first = build_standard_gamma_history(spot, vix, d4)
        self.assertEqual([p["date"] for p in first["points"]], [d1, d3, d4])
        self.assertIn("vix_captured_at_bjt", first["points"][0])
        self.assertEqual(first["coverage"]["missing_vix_dates"], [d2])
        self.assertEqual(first["coverage"]["sp500_gaps"]["after_cutoff_dates"], [future])
        new_vix = [(d1, 30), (d1, 30), (d4, 23)]
        revised = build_standard_gamma_history(spot, new_vix, d4)
        self.assertLess(revised["points"][0]["value"], first["points"][0]["value"])
        self.assertEqual(revised["coverage"]["missing_vix_dates"], [d2, d3])
        self.assertEqual(revised["points"][-1], first["points"][-1])

    def test_conflicts_stale_and_failures_remain_visible(self):
        d1, d2 = "2026-11-16", "2026-11-17"
        spot = [(d1, 5000), (d2, 5100), (d2, 5300), ("invalid", 22)]
        vix = [(d1, 20), (d2, 21)]
        partial = build_standard_gamma_history(spot, vix, d2)
        self.assertEqual(partial["as_of"], d1)
        self.assertEqual(partial["status"], "partial_latest")
        self.assertEqual(partial["coverage"]["sp500_gaps"]["conflicting_dates"], [d2])
        self.assertEqual(partial["coverage"]["sp500_gaps"]["undated_rows"], 1)
        self.assertEqual(build_standard_gamma_history(spot, vix, "2026-11-24")["status"], "stale")
        cached = build_standard_gamma_history(spot, vix, d2, sp500_status="cached_after_fetch_failure")
        self.assertEqual(cached["source_statuses"]["SP500"], "cached_after_fetch_failure")
        self.assertEqual(cached["status"], "cached_after_fetch_failure")
        missing = build_standard_gamma_history([(d1, False)], vix, d2)
        self.assertEqual(missing["status"], "missing")
        self.assertEqual(missing["points"], [])
        self.assertEqual(missing["coverage"]["sp500_gaps"]["invalid_dates"], [d1])
