"""Offline tests for source/date fidelity and explicit investment-data gaps."""
import copy
import math
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investment_facts import build_market_context, enrich_package
from scripts import fetchers


def metric(mid="DGS5", count=70, frequency="daily", source="official", start="2026-08-01", step=1):
    first = date.fromisoformat(start)
    points = [{"date": (first + timedelta(days=i * step)).isoformat(), "value": 3.0 + i / 100} for i in range(count)]
    return {"id": mid, "fact_id": f"metric:{mid}", "name": mid, "unit": "%", "frequency": frequency,
            "source": source, "status": "ok", "as_of": points[-1]["date"], "value": points[-1]["value"],
            "extra": {"history": points}}


def package(*metrics, auctions=None):
    return {"generated_at_bjt": "2026-10-30 12:00:00 UTC+08:00", "data": {"facts": {
        "canonical_metrics": [{k: v for k, v in r.items() if k != "extra"} for r in metrics],
        "event_facts": {"status": "ok", "source_url": "https://www.treasurydirect.gov/", "upcoming_auctions": auctions or []},
    }}}


def snapshot(*metrics, context=None):
    return {"metrics": list(metrics), "investment_market_context": context or {"price_history": {}, "series": {}}}


class InvestmentFacts(unittest.TestCase):
    def test_windows_are_calculated_from_canonical_source(self):
        m = metric()
        alt = metric(source="alternative")
        for row in alt["extra"]["history"]:
            row["value"] += 100
        result = enrich_package(package(m), snapshot(alt, m))["data"]["facts"]["investment"]
        facts = {r["fact_id"]: r for r in result["trend_facts"]}
        self.assertAlmostEqual(facts["trend:DGS5:20obs"]["change"], .2)
        self.assertEqual(facts["trend:DGS5:20obs"]["source"], "official")

    def test_future_history_is_excluded(self):
        m = metric()
        m["extra"]["history"].append({"date": "2099-01-01", "value": 999})
        result = enrich_package(package(m), snapshot(m))["data"]["facts"]["investment"]
        self.assertTrue(result["trend_facts"])
        self.assertTrue(all(r["as_of"] == m["as_of"] for r in result["trend_facts"]))
        self.assertTrue(all(r["value"] < 10 for r in result["trend_facts"]))

    def test_nonfinite_and_conflicting_observations_are_excluded(self):
        m = metric(count=7)
        m["extra"]["history"][0]["value"] = math.inf
        m["extra"]["history"].append({"date": m["extra"]["history"][1]["date"], "value": 99})
        result = enrich_package(package(m), snapshot(m))["data"]["facts"]["investment"]
        self.assertFalse(result["trend_facts"])

    def test_history_endpoint_must_match_current_value(self):
        m = metric()
        m["extra"]["history"][-1]["value"] += 1
        result = enrich_package(package(m), snapshot(m))["data"]["facts"]["investment"]
        self.assertFalse(result["trend_facts"])
        self.assertEqual(result["coverage_facts"][0]["status"], "history_endpoint_mismatch")

    def test_missing_selected_source_history_does_not_use_alternative(self):
        m, alt = metric(), metric(source="alternative")
        result = enrich_package(package(m), snapshot(alt))["data"]["facts"]["investment"]
        self.assertFalse(result["trend_facts"])

    def test_weekly_windows_are_not_labelled_days(self):
        m = metric("WRESBAL", count=6, frequency="weekly", start="2026-08-01", step=7)
        result = enrich_package(package(m), snapshot(m))["data"]["facts"]["investment"]
        f = result["trend_facts"][0]
        self.assertIn("周频", f["window_label"])
        self.assertEqual(f["calendar_days"], 35)
        self.assertEqual(f["window_observations"], 5)

    def test_short_sample_never_has_twenty_observation_window(self):
        m = metric(count=8)
        result = enrich_package(package(m), snapshot(m))["data"]["facts"]["investment"]
        self.assertEqual([r["window_observations"] for r in result["trend_facts"]], [5])
        self.assertEqual(result["coverage_facts"][0]["missing_windows"], [20, 60])

    def test_sofr_iorb_requires_same_day_anchor_not_current_anchor(self):
        s, i = metric("SOFR"), metric("IORB")
        for row in i["extra"]["history"]:
            row["value"] = 2.5
        i["value"] = 2.5
        p = package(s, i)
        result = enrich_package(p, snapshot(s, i))["data"]["facts"]["investment"]
        derived = next(r for r in result["trend_facts"] if r["fact_id"] == "trend:SOFR_IORB:20obs")
        self.assertAlmostEqual(derived["value"], (s["value"] - 2.5) * 100)
        self.assertAlmostEqual(derived["change"], 20.0)
        i["extra"]["history"] = [{"date": "2026-10-30", "value": 2.5}]
        i["as_of"] = "2026-10-30"
        result = enrich_package(package(s, i), snapshot(s, i))["data"]["facts"]["investment"]
        self.assertFalse(any(r["id"] == "SOFR_IORB" for r in result["trend_facts"]))

    def test_gross_is_by_settlement_not_auction_date(self):
        rows = [{"fact_id": "event:a", "issue_date": "2026-11-05", "auction_date": "2026-12-01", "gross_announced_offering_usd_bn": 100},
                {"fact_id": "event:b", "issue_date": "2026-11-06", "auction_date": "2026-10-30", "gross_announced_offering_usd_bn": 80}]
        result = enrich_package(package(auctions=rows), snapshot())["data"]["facts"]["investment"]["calendar_facts"]
        self.assertEqual(result[0]["gross_announced_offering_usd_bn"], 100)
        self.assertEqual(result[1]["gross_announced_offering_usd_bn"], 180)
        self.assertIsNone(result[0]["maturities_usd_bn"])
        self.assertIsNone(result[0]["net_cash_impact_usd_bn"])

    def test_same_day_explicit_cash_is_separate_from_gross(self):
        rows = [{"fact_id": "event:a", "issue_date": "2026-10-30", "gross_announced_offering_usd_bn": 100,
                 "maturities_usd_bn": 80, "net_cash_impact_usd_bn": 19.5}]
        f = enrich_package(package(auctions=rows), snapshot())["data"]["facts"]["investment"]["calendar_facts"][0]
        self.assertEqual(f["value"], 100)
        self.assertEqual(f["maturities_usd_bn"], 80)
        self.assertEqual(f["net_cash_impact_usd_bn"], 19.5)
        self.assertIn("unknown", f["reserve_impact"])

    def test_empty_calendar_does_not_mean_zero_issuance(self):
        facts = enrich_package(package(), snapshot())["data"]["facts"]["investment"]["calendar_facts"]
        self.assertTrue(all(r["value"] is None and r["status"] == "missing" for r in facts))

    def test_unknown_announced_amount_is_not_complete_total(self):
        rows = [{"fact_id": "event:a", "issue_date": "2026-10-30", "gross_announced_offering_usd_bn": 100},
                {"fact_id": "event:b", "issue_date": "2026-10-30", "gross_announced_offering_usd_bn": None}]
        f = enrich_package(package(auctions=rows), snapshot())["data"]["facts"]["investment"]["calendar_facts"][0]
        self.assertEqual(f["value"], 100)
        self.assertEqual(f["unknown_amount_count"], 1)
        self.assertFalse(f["gross_amounts_complete_for_listed_events"])
        self.assertIsNone(f["net_cash_impact_usd_bn"])

    def test_future_announcement_is_not_available_in_snapshot(self):
        rows = [{"fact_id": "event:a", "issue_date": "2026-11-01", "announcement_date": "2026-10-31", "gross_announced_offering_usd_bn": 100}]
        f = enrich_package(package(auctions=rows), snapshot())["data"]["facts"]["investment"]["calendar_facts"][0]
        self.assertIsNone(f["value"])

    def test_price_returns_are_confirmation_and_btc_is_seven_day(self):
        points = [{"date": (date(2026, 8, 1) + timedelta(days=i)).isoformat(), "value": 100 + i} for i in range(70)]
        context = {"price_history": {"CBBTCUSD": points}, "series": {"CBBTCUSD": {"status": "ok"}}}
        result = enrich_package(package(), snapshot(context=context))["data"]["facts"]["investment"]
        f = next(r for r in result["market_facts"] if r["fact_id"] == "market:CBBTCUSD:20obs")
        self.assertEqual(f["role"], "market_confirmation")
        self.assertIn("7-day", f["frequency"])
        self.assertAlmostEqual(f["value"], (169 / 149 - 1) * 100)
        self.assertEqual(f["status"], "stale")

    def test_offline_context_is_no_network_and_preserves_age(self):
        old = {"price_history": {"SP500": [{"date": "2026-10-20", "value": 100}]},
               "series": {"SP500": {"status": "ok", "source": "FRED public CSV", "captured_at_bjt": "2026-10-21"}}}
        with patch("scripts.investment_facts.http_get_text", side_effect=AssertionError("offline must not fetch")):
            result = build_market_context("2026-10-30", fetch=False, previous_context=old)
        self.assertEqual(result["series"]["SP500"]["status"], "cached_offline")
        self.assertEqual(result["series"]["SP500"]["as_of"], "2026-10-20")
        self.assertEqual(result["series"]["SP500"]["stale_days"], 10)
        self.assertIsNone(result["retrieved_at_bjt"])

    def test_comparison_uses_facts_and_marks_revision(self):
        m = metric()
        old = package(copy.deepcopy(m))
        old["data"]["facts"]["canonical_metrics"][0]["value"] -= 1
        old["stance"] = {"label": "do not copy this"}
        result = enrich_package(package(m), snapshot(m), old)["data"]["facts"]["investment"]
        self.assertEqual(result["comparison_facts"][0]["comparison_kind"], "revision_same_observation_date")
        self.assertEqual(result["comparison_facts"][0]["change"], 1)

    def test_sofr_iorb_staleness_is_propagated(self):
        s, i = metric("SOFR"), metric("IORB")
        result = enrich_package(package(s, i), snapshot(s, i))["data"]["facts"]["investment"]
        derived = [r for r in result["trend_facts"] if r["id"] == "SOFR_IORB"]
        self.assertTrue(derived)
        self.assertTrue(all(r["status"] == "stale" for r in derived))
        self.assertTrue(any(r["fact_id"] == "coverage:sofr_iorb_freshness" for r in result["coverage_facts"]))

    def test_anchor_source_stale_is_not_overwritten_with_ok(self):
        s, i = metric("SOFR", count=90), metric("IORB", count=90)
        i["status"] = "stale"
        result = enrich_package(package(s, i), snapshot(s, i))["data"]["facts"]["investment"]
        self.assertTrue(all(r["status"] == "stale" for r in result["trend_facts"] if r["id"] == "SOFR_IORB"))

    def test_unavailable_current_or_prior_comparison_is_not_ok(self):
        m = metric(count=90)
        old = package(copy.deepcopy(m))
        old["data"]["facts"]["canonical_metrics"][0]["status"] = "error"
        result = enrich_package(package(m), snapshot(m), old)["data"]["facts"]["investment"]
        self.assertEqual(result["comparison_facts"][0]["status"], "error")
        old["data"]["facts"]["canonical_metrics"][0]["status"] = "ok"
        m["status"] = "unavailable"
        result = enrich_package(package(m), snapshot(m), old)["data"]["facts"]["investment"]
        self.assertEqual(result["comparison_facts"][0]["status"], "unavailable")

    def test_successful_market_refresh_retains_earlier_same_source_captures(self):
        old = {"price_history": {"SP500": [
            {"date": "2024-01-01", "value": 80, "captured_at_bjt": "2024-01-02"},
            {"date": "2026-10-28", "value": 99, "captured_at_bjt": "2026-10-29"},
            {"date": "2099-01-01", "value": 999}]},
            "series": {"SP500": {"source": "FRED public CSV", "source_url": "https://fred.stlouisfed.org/series/SP500"}}}
        def response(url, **kwargs):
            sid = parse_qs(urlsplit(url).query)["id"][0]
            return f"observation_date,{sid}\n2026-10-28,100\n2026-10-29,101\n"
        with patch("scripts.investment_facts.http_get_text", side_effect=response), patch("pathlib.Path.write_text", side_effect=AssertionError("capture must not write outside isolated run")):
            result = build_market_context("2026-10-30", fetch=True, previous_context=old)
        history = result["price_history"]["SP500"]
        self.assertEqual([(r["date"], r["value"]) for r in history], [("2024-01-01", 80), ("2026-10-28", 100), ("2026-10-29", 101)])
        self.assertEqual(history[0]["captured_at_bjt"], "2024-01-02")
        self.assertNotEqual(history[1]["captured_at_bjt"], "2026-10-29")
        self.assertEqual(result["series"]["SP500"]["retained_earlier_observations"], 1)

    def test_market_refresh_does_not_merge_another_source(self):
        old = {"price_history": {"SP500": [{"date": "2024-01-01", "value": 80}]},
               "series": {"SP500": {"source": "unrelated"}}}
        def response(url, **kwargs):
            sid = parse_qs(urlsplit(url).query)["id"][0]
            return f"DATE,{sid}\n2026-10-29,101\n"
        with patch("scripts.investment_facts.http_get_text", side_effect=response):
            result = build_market_context("2026-10-30", fetch=True, previous_context=old)
        self.assertEqual(len(result["price_history"]["SP500"]), 1)


class CapturedSourceHistory(unittest.TestCase):
    def assert_history_consistent(self, m, values):
        self.assertEqual(m.status, "ok")
        self.assertEqual(m.unit, "USD bn")
        self.assertEqual([r["value"] for r in m.extra["history"]], values)
        self.assertEqual(m.value, m.extra["history"][-1]["value"])
        self.assertEqual(m.as_of, m.extra["history"][-1]["date"])
        self.assertEqual(m.previous, m.extra["history"][-2]["value"])
        self.assertEqual(m.previous_as_of, m.extra["history"][-2]["date"])

    def test_sofr_volume_retains_full_response_in_billions(self):
        payload = {"refRates": [
            {"effectiveDate": "2026-10-29", "percentRate": 4.1, "volumeInBillions": 3000},
            {"effectiveDate": "2026-10-28", "percentRate": 4, "volumeInBillions": 2900}]}
        with patch("scripts.fetchers.http_get_json", return_value=payload) as http:
            m = fetchers.fetch_nyfed_sofr_volume()
        self.assertIn("search.json?startDate=2000-01-01", http.call_args.args[0])
        self.assert_history_consistent(m, [2900, 3000])

    def test_tga_history_and_previous_come_from_response_not_cache(self):
        payload = {"data": [
            {"record_date": "2026-10-29", "account_type": "TGA Opening Balance", "open_today_bal": "950000"},
            {"record_date": "2026-10-29", "account_type": "TGA Closing Balance", "open_today_bal": "1000000"},
            {"record_date": "2026-10-28", "account_type": "TGA Closing Balance", "open_today_bal": "900000"}]}
        with patch("scripts.fetchers.http_get_json", return_value=payload) as http, patch("scripts.fetchers.append_tga_history") as append, patch("scripts.fetchers.read_tga_history", side_effect=AssertionError("cache must not enter captured history")):
            m = fetchers.fetch_tga()
        self.assertIn("page[size]=10000", http.call_args.args[0])
        self.assert_history_consistent(m, [900, 1000])
        self.assertIn("Closing Balance", m.extra["raw_latest"]["account_type"])
        self.assertEqual(append.call_count, 2)

    def test_tga_zero_balance_remains_zero(self):
        payload = {"data": [
            {"record_date": "2026-10-29", "account_type": "TGA Closing Balance", "open_today_bal": 0},
            {"record_date": "2026-10-28", "account_type": "TGA Closing Balance", "open_today_bal": "900000"}]}
        with patch("scripts.fetchers.http_get_json", return_value=payload), patch("scripts.fetchers.append_tga_history"):
            m = fetchers.fetch_tga()
        self.assert_history_consistent(m, [900, 0])

    def test_rrp_response_dollars_become_billions(self):
        payload = {"repo": {"operations": [
            {"operationDate": "2026-10-29", "totalAmtAccepted": "350000000"},
            {"operationDate": "2026-10-28", "totalAmtAccepted": "170000000"}]}}
        with patch("scripts.fetchers.http_get_json", return_value=payload) as http:
            m = fetchers.fetch_nyfed_rrp()
        params = parse_qs(urlsplit(http.call_args.args[0]).query)
        self.assertEqual((date.fromisoformat(params["endDate"][0]) - date.fromisoformat(params["startDate"][0])).days, 120)
        self.assert_history_consistent(m, [.17, .35])

    def test_soma_history_uses_same_unit_as_latest_and_previous(self):
        payload = {"soma": [{"asOfDate": "2026-10-28", "totalParValue": "6000000000000"},
                            {"asOfDate": "2026-10-21", "totalParValue": "6100000000000"}]}
        with patch("scripts.fetchers.http_get_json", return_value=payload):
            m = fetchers.fetch_soma_summary()
        self.assert_history_consistent(m, [6100, 6000])
        self.assertEqual(m.frequency, "weekly")


if __name__ == "__main__":
    unittest.main()

