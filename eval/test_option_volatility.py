import math
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.option_volatility import build_volatility_spread_history


class VolatilitySpread(unittest.TestCase):
    def setUp(self):
        start = date(2026, 3, 2)
        self.days = [(start + timedelta(days=i)).isoformat() for i in range(100)
                     if (start + timedelta(days=i)).weekday() < 5][:62]
        prices = [100.0]
        # 21 returns [0.01, 0.02, ..., 0.21] have a known sample variance.
        for i in range(1, len(self.days)):
            prices.append(prices[-1] * math.exp(i / 100))
        self.spot = list(zip(self.days, prices))
        self.vix = [(d, 22.5) for d in self.days]

    def test_sample_stdev_and_endpoint_alignment(self):
        end = self.days[21]
        only_vix = [(self.days[2], 81.0), (end, 22.5)]
        result = build_volatility_spread_history(self.spot, only_vix, end)
        self.assertEqual(len(result["points"]), 1)
        p = result["points"][0]
        expected_rv = math.sqrt(sum((i - 11)**2 for i in range(1, 22)) / 20 * 252)
        self.assertAlmostEqual(p["realized_vol_pct"], expected_rv, places=10)
        self.assertAlmostEqual(p["value"], 22.5 - expected_rv, places=10)
        self.assertEqual((p["date"], p["window_start"], p["window_end"], p["return_count"]),
                         (end, self.days[0], end, 21))
        self.assertEqual(result["coverage"]["insufficient_window_dates"], self.days[:21])
        self.assertEqual(result["coverage"]["sp500_gaps"]["after_cutoff_dates"], self.days[22:])
        missing = build_volatility_spread_history(self.spot, only_vix[:-1], end)
        self.assertFalse(missing["points"])
        self.assertEqual(result["realized_points"], missing["realized_points"])
        self.assertEqual(missing["status"], "missing")
        flat = build_volatility_spread_history([(d, 100) for d in self.days], only_vix, end)
        self.assertEqual(flat["points"][0]["realized_vol_pct"], 0)
        self.assertEqual(flat["points"][0]["value"], 22.5)

    def test_cash_error_removes_affected_rolling_windows_and_recovers(self):
        broken = self.days[25]
        for modification, reason in (([(broken, 0)], "invalid_dates"), ([(broken, 500)], "conflicting_dates")):
            with self.subTest(reason=reason):
                result = build_volatility_spread_history(self.spot + modification, self.vix, self.days[-1])
                self.assertIn(broken, result["coverage"]["sp500_gaps"][reason])
                self.assertEqual(result["coverage"]["interrupted_window_dates"], [broken])
                self.assertEqual([p["date"] for p in result["points"]], self.days[21:25] + self.days[47:])
        # VIX is used only for its own date. A rejected VIX cannot invalidate later realized windows.
        result = build_volatility_spread_history(self.spot, self.vix + [(broken, 23.0)], self.days[-1])
        self.assertEqual([p["date"] for p in result["points"]], self.days[21:25] + self.days[26:])
        self.assertEqual([p["date"] for p in result["realized_points"]], self.days[21:])

    def test_open_cash_session_and_vix_trading_on_cash_holiday(self):
        spot = self.spot[:25] + self.spot[26:]
        holiday = self.days[25]
        # A valid Nasdaq reference spans this date, but neither cash series quotes on it.
        allowed = build_volatility_spread_history(spot, self.vix, self.days[-1], equity_session_rows=spot)
        self.assertEqual(allowed["coverage"]["vix_only_dates_within_reference"], [holiday])
        self.assertEqual([p["date"] for p in allowed["points"]], self.days[21:25] + self.days[26:])
        # Nasdaq printed a close: SPX is missing irrespective of whether VIX was also missing.
        for vix in (self.vix, self.vix[:25] + self.vix[26:]):
            missing = build_volatility_spread_history(spot, vix, self.days[-1], equity_session_rows=self.spot)
            self.assertEqual(missing["coverage"]["missing_sp500_session_dates"], [holiday])
            self.assertEqual([p["date"] for p in missing["points"]], self.days[21:25] + self.days[47:])
        for witness in (None, self.spot[:20], spot + [(holiday, -1)]):
            unresolved = build_volatility_spread_history(spot, self.vix, self.days[-1], equity_session_rows=witness)
            self.assertEqual(unresolved["coverage"]["unconfirmed_session_dates"], [holiday])
            self.assertEqual([p["date"] for p in unresolved["points"]], self.days[21:25] + self.days[47:])

    def test_vintage_revisions_freshness_and_failures(self):
        cutoff = self.days[42]
        before = build_volatility_spread_history(self.spot, self.vix, cutoff)
        modified = self.spot.copy()
        modified[30] = self.days[30], self.spot[30][1] * 1.1
        after = build_volatility_spread_history(modified, self.vix, cutoff)
        def value_at(result, d):
            return next(p["value"] for p in result["points"] if p["date"] == d)
        self.assertEqual(value_at(before, self.days[29]), value_at(after, self.days[29]))
        self.assertNotEqual(value_at(before, self.days[30]), value_at(after, self.days[30]))
        partial = build_volatility_spread_history(self.spot, self.vix[:42], cutoff)
        self.assertEqual((partial["as_of"], partial["status"]), (self.days[41], "partial_latest"))
        stale = build_volatility_spread_history(self.spot[:30], self.vix[:30], cutoff)
        self.assertEqual(stale["status"], "stale")
        error = build_volatility_spread_history(self.spot, self.vix, cutoff, vix_status="cached_after_fetch_failure")
        self.assertEqual(error["points"], before["points"])
        self.assertEqual(error["status"], "cached_after_fetch_failure")
        self.assertEqual(error["source_statuses"]["VIXCLS"], "cached_after_fetch_failure")
        with self.assertRaises(ValueError):
            build_volatility_spread_history([], [], "invalid")

    def test_recorded_equity_market_closure_has_provenance(self):
        start = date(2019, 3, 4)
        holiday = "2019-04-19"
        days = [(start + timedelta(days=i)).isoformat() for i in range(60)
                if (start + timedelta(days=i)).weekday() < 5]
        spot = [(d, 100) for d in days if d != holiday]
        witness = spot + [(holiday, 99.99)]
        result = build_volatility_spread_history(spot, spot, days[-1], equity_session_rows=witness)
        closure = result["coverage"]["confirmed_reference_closures"][holiday]
        self.assertIn("Good Friday", closure["reason"])
        self.assertIn("theice.com", closure["source_url"])
        self.assertFalse(result["coverage"]["interrupted_window_dates"])
        self.assertNotIn(holiday, [p["date"] for p in result["points"]])
        self.assertEqual(result["points"][-1]["date"], days[-1])


if __name__ == "__main__":
    unittest.main()
