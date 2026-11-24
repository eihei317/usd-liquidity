import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.option_positioning import DATASETS, MARKET_CODE, build_positioning_history, capture_positioning


def leg(kind, day, long, short, multiplier=50):
    return {"id": day + kind, "report_date_as_yyyy_mm_dd": day + "T00:00:00.000",
            "cftc_contract_market_code": MARKET_CODE, "futonly_or_combined": DATASETS[kind][1],
            "contract_units": f"(S&P 500 INDEX X ${multiplier:.2f})",
            "dealer_positions_long_all": str(long), "dealer_positions_short_all": str(short)}


def snapshot(combined, futures):
    return {"sources": {k: {"dataset_id": DATASETS[k][0], "market_code": MARKET_CODE,
                            "rows": v, "captured_at_bjt": "2026-11-24T15:00:00+08:00", "status": "ok"}
                        for k, v in (("combined", combined), ("futures_only", futures))}}


class DealerPositioning(unittest.TestCase):
    def setUp(self):
        self.d1, self.d2 = "2026-11-10", "2026-11-17"
        self.c = [leg("combined", self.d1, 167562, 916219), leg("combined", self.d2, 179269, 984875)]
        self.f = [leg("futures_only", self.d1, 175745, 915197), leg("futures_only", self.d2, 190498, 981913)]

    def test_actual_fields_and_sign_offline(self):
        with patch("scripts.option_positioning.http_get_json", side_effect=AssertionError("offline only")):
            h = build_positioning_history(snapshot(self.c, self.f), "2026-11-24")
        self.assertEqual(h["status"], "ok")
        p = h["points"][-1]
        self.assertEqual((p["combined_net"], p["futures_only_net"], p["value"], p["change"]),
                         (-805606, -791415, -14191, -4986))
        self.assertEqual(p["contract_multiplier"], 50)

    def test_missing_weeks_incompatible_units_and_revisions(self):
        c, f = copy.deepcopy(self.c), copy.deepcopy(self.f)
        for rows in (c, f):
            rows[0]["contract_units"] = "'(S&P 500 INDEX X $250.00)'"
        c.append(leg("combined", "2026-12-01", 300, 0))
        f.append(leg("futures_only", "2026-12-01", 1, 0))
        h = build_positioning_history(snapshot(c, f), "2026-12-02")
        self.assertEqual(h["coverage"]["unit_change_dates"], [self.d2])
        self.assertEqual(h["coverage"]["missing_both_week_starts"], ["2026-11-23"])
        self.assertIsNone(h["points"][-1]["change"])
        self.assertIsNone(h["points"][1]["change"])
        f[1]["contract_units"] = "(S&P 500 INDEX X $250.00)"
        changed = build_positioning_history(snapshot(c, f), "2026-11-24")
        self.assertEqual(changed["coverage"]["incompatible_unit_dates"], [self.d2])
        self.assertEqual(len(changed["points"]), 1)
        self.assertEqual(changed["coverage"]["source_gaps"]["combined"]["after_cutoff_dates"], ["2026-12-01"])

    def test_conflicts_different_markets_sources_and_mismatched_dates(self):
        for field, value in (("dealer_positions_short_all", "-1"), ("cftc_contract_market_code", "13874A"),
                             ("futonly_or_combined", "Combined"), ("contract_units", "unknown")):
            with self.subTest(field=field):
                f = copy.deepcopy(self.f)
                f[1][field] = value
                h = build_positioning_history(snapshot(self.c, f), self.d2)
                self.assertEqual(h["as_of"], self.d1)
                self.assertEqual(h["status"], "partial_latest")
                self.assertIn(self.d2, h["coverage"]["source_gaps"]["futures_only"]["invalid_or_conflicting_dates"])
        conflict = build_positioning_history(snapshot(self.c + [leg("combined", self.d2, 1, 1)], self.f), self.d2)
        self.assertEqual(conflict["as_of"], self.d1)
        f = [self.f[0], leg("futures_only", "2026-11-18", 190498, 981913)]
        self.assertEqual(build_positioning_history(snapshot(self.c, f), "2026-11-24")["as_of"], self.d1)
        double_week = snapshot(self.c + [leg("combined", "2026-11-18", 1, 0)], self.f)
        self.assertEqual(build_positioning_history(double_week, "2026-11-24")["as_of"], self.d1)
        spread_conflict = snapshot(self.c + [dict(self.c[1], dealer_positions_spread_all="999")], self.f)
        self.assertEqual(build_positioning_history(spread_conflict, "2026-11-24")["as_of"], self.d1)
        stale = snapshot(self.c, self.f)
        stale["sources"]["combined"].update(status="cached_after_fetch_failure", error="offline")
        h = build_positioning_history(stale, "2026-11-24")
        self.assertEqual(h["source_statuses"], {"combined": "cached_after_fetch_failure", "futures_only": "ok"})
        self.assertIn("offline", h["message"])
        stale["sources"]["combined"]["dataset_id"] = DATASETS["futures_only"][0]
        self.assertFalse(build_positioning_history(stale, "2026-11-24")["points"])

    def test_pagination_raw_fields_and_one_failed_feed(self):
        requests = []

        def fetch(url, **_):
            qs = parse_qs(urlsplit(url).query)
            self.assertIn(MARKET_CODE, qs["$where"][0])
            requests.append(url)
            if DATASETS["futures_only"][0] in url:
                raise RuntimeError("connection unavailable")
            if "count(" in qs["$select"][0]:
                return [{"observations": "2"}]
            return [self.c[int(qs["$offset"][0])]]

        with patch("scripts.option_positioning.http_get_json", side_effect=fetch):
            c = capture_positioning("2026-11-24")
        self.assertEqual(len(requests), 4)
        self.assertEqual(c["sources"]["combined"]["rows"], self.c)
        self.assertIn("captured_at_bjt", c["sources"]["combined"])
        self.assertEqual(c["sources"]["futures_only"]["status"], "error")
        h = build_positioning_history(c, "2026-11-24")
        self.assertFalse(h["points"])
        self.assertIn("connection unavailable", h["message"])

    def test_repeated_page_cannot_loop_or_publish_complete(self):
        def repeat(url, **_):
            if "count(" in parse_qs(urlsplit(url).query)["$select"][0]:
                return [{"observations": "99"}]
            kind = "combined" if DATASETS["combined"][0] in url else "futures_only"
            return [leg(kind, self.d1, 2, 1)]

        with patch("scripts.option_positioning.http_get_json", side_effect=repeat) as fetch:
            c = capture_positioning("2026-11-24")
        self.assertEqual(fetch.call_count, 6)
        for s in c["sources"].values():
            self.assertEqual(s["status"], "error")
            self.assertIn("pagination", s["error"])
