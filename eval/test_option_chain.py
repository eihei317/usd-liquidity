"""Synthetic local inputs only. No real option quotes, provider credentials, or downloads."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import option_chain as chain

ASOF = "2026-11-23 05:45:00 UTC-05:00"
CUTOFF = "2026-11-24 20:00:00 UTC+08:00"


def contract(expiration="2026-11-25", **changes):
    return {"root": "SPXW", "expiration": expiration, "right": "C", "strike": 5000, "gamma": .001,
            "open_interest": 10, **changes}


def capture(rows, **changes):
    return {"schema_version": 1, "source": "Example Exchange", "source_url": "https://example.com/options",
            "allowed_aggregate_destination": chain.DESTINATION, "observed_at": ASOF, "available_at": ASOF,
            "underlying": "SPX", "scope": chain.SCOPE, "complete_chain": True, "spot": 5000,
            "gamma_unit": "delta_per_index_point", "open_interest_as_of": "2026-11-20",
            "contract_multiplier": 100, "contracts": rows, **changes}


def facts(row):
    return {v["fact_id"].split(":")[-1]: v["value"] for v in row["facts"]}


class LocalOptionChain(unittest.TestCase):
    def test_usd_notional_and_share_count_each_call_and_put_once(self):
        c = contract()
        p = contract("2026-11-30", right="P", open_interest=20)
        later = contract("2026-12-01", root="SPX", strike=5100, open_interest=30)
        row = chain.summarize_chain(capture([c, p, later, dict(p)]), CUTOFF)
        self.assertEqual(row["status"], "ok")
        self.assertEqual(row["as_of"], "2026-11-23")
        self.assertEqual(facts(row), {"gross_gamma_1pct": 1500000, "gamma_share_7d": 50})
        self.assertEqual(row["strike_distribution"], [
            {"strike": 5000, "gross_gamma_usd_1pct": 750000, "share_pct": 50},
            {"strike": 5100, "gross_gamma_usd_1pct": 750000, "share_pct": 50}])
        self.assertEqual(row["coverage"]["duplicate_rows"], 1)

    def test_zero_observed_and_unknown_are_distinct(self):
        zero = chain.summarize_chain(capture([contract(open_interest=0)]), CUTOFF)
        self.assertEqual((zero["status"], facts(zero)), ("ok", {"gross_gamma_1pct": 0}))
        missing = chain.summarize_chain(capture([contract(), contract(right="P", open_interest=None)]), CUTOFF)
        self.assertEqual((missing["status"], missing["facts"], missing["coverage"]["missing_contracts"]), ("partial", [], 1))
        absent = chain.summarize_chain(capture([]), CUTOFF)
        self.assertEqual((absent["status"], absent["facts"]), ("missing", []))
        unknown = chain.summarize_chain(capture([contract()], complete_chain=False), CUTOFF)
        self.assertEqual((unknown["status"], unknown["strike_distribution"]), ("partial", []))

    def test_scope_units_rights_and_conflicting_contract_rows(self):
        source = capture([contract()])
        for patch_dict in ({"schema_version": True}, {"underlying": "SPY"}, {"gamma_unit": "per_pct"},
                           {"contract_multiplier": 10}, {"contracts": [contract(root="XSP")]},
                           {"contracts": [contract(open_interest=1.1)]}, {"contracts": [contract(gamma=-.001)]},
                           {"contracts": [contract(gamma=float("nan"))]}, {"contracts": [contract(strike=-10)]},
                           {"contracts": [contract(), contract(open_interest=0)]}):
            with self.subTest(patch=patch_dict):
                r = chain.summarize_chain({**source, **patch_dict}, CUTOFF)
                self.assertEqual((r["status"], r["facts"]), ("invalid", []))
        denied = chain.summarize_chain({**source, "allowed_aggregate_destination": "local_only"}, CUTOFF)
        self.assertEqual((denied["status"], denied["source"], denied["facts"]), ("redistribution_unconfirmed", None, []))

    def test_same_day_requires_active_session_and_series_timing(self):
        morning = contract("2026-11-23", root="SPX", expires_at="2026-11-23T09:40:00-05:00",
                           last_trade_at="2026-11-20T17:00:00-05:00")
        afternoon = contract("2026-11-23", expires_at="2026-11-23T16:00:00-05:00",
                             last_trade_at="2026-11-23T16:00:00-05:00")
        weekly = contract("2026-11-25", open_interest=20)
        data = capture([morning, afternoon, weekly], session_open_at_observation=True)
        r = chain.summarize_chain(data, CUTOFF)
        # Before the AM fixing the AM contract has gamma, although its last session ended Friday.
        self.assertEqual(facts(r)["gamma_share_0dte"], 25)
        self.assertEqual(facts(r)["gross_gamma_1pct"], 1000000)
        now = "2026-11-23T09:45:00-05:00"
        r = chain.summarize_chain({**data, "observed_at": now, "available_at": now}, CUTOFF)
        self.assertAlmostEqual(facts(r)["gamma_share_0dte"], 100/3)
        self.assertEqual(r["coverage"]["expired_contracts"], 1)
        for session in (None, False):
            self.assertNotIn("gamma_share_0dte", facts(chain.summarize_chain({**data, "session_open_at_observation": session}, CUTOFF)))
        del afternoon["expires_at"]
        r = chain.summarize_chain(data, CUTOFF)
        self.assertNotIn("gamma_share_0dte", facts(r))
        self.assertIn("gamma_share_7d", facts(r))

    def test_not_yet_available_invalid_times_and_staleness(self):
        data = capture([contract()])
        for patch_dict in ({"available_at": "2026-11-20T09:00:00-05:00"}, {"observed_at": "2026-11-23"},
                           {"open_interest_as_of": "2026-11-25"},
                           {"contracts": [contract("2026-11-23", expires_at="2026-11-24T16:00:00-05:00")]},
                           {"contracts": [contract("2026-11-23", expires_at="2026-11-23T13:00:00-05:00",
                                                   last_trade_at="2026-11-23T16:00:00-05:00")]}):
            self.assertEqual(chain.summarize_chain({**data, **patch_dict}, CUTOFF)["status"], "invalid")
        future = chain.summarize_chain({**data, "available_at": "2026-11-25T08:00:00-05:00"}, CUTOFF)
        self.assertEqual((future["status"], future["facts"], future["as_of"]), ("unavailable_at_cutoff", [], None))
        future_denied = {**data, "available_at": "2026-11-25T08:00:00-05:00", "allowed_aggregate_destination": None}
        self.assertEqual(chain.summarize_chain(future_denied, CUTOFF)["status"], "unavailable_at_cutoff")
        stale = chain.summarize_chain(data, "2026-12-01T18:00:00-05:00")
        self.assertEqual((stale["status"], stale["facts"][0]["status"], stale["coverage"]["quote_stale"]), ("stale", "stale", True))
        stale_oi = chain.summarize_chain({**data, "open_interest_as_of": "2026-11-13"}, CUTOFF)
        self.assertTrue(stale_oi["coverage"]["oi_stale"])

    def test_new_york_date_not_utc_date_in_summer_or_winter(self):
        with patch.object(chain, "NEW_YORK", None):
            for instant, expected in [("2026-07-02T04:30:00Z", "2026-07-02"), ("2026-11-24T04:30:00Z", "2026-11-23")]:
                data = capture([contract("2026-12-18")], observed_at=instant, available_at=instant, open_interest_as_of=expected)
                self.assertEqual(chain.summarize_chain(data, instant)["as_of"], expected)

    def test_history_releases_are_sorted_conflicts_visible_and_rows_never_returned(self):
        data = capture([contract()])
        private = copy.deepcopy(data)
        private["source_url"] = "https://example.com/private-download-path"
        private["api_key"] = "SECRET_CONTENT"
        private["contracts"][0]["account"] = "PRIVATE_ACCOUNT"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            def store(name, record):
                (path / name).write_text(json.dumps(record), encoding="utf-8")
            store("first.json", private)
            store("revision.json", {**data, "available_at": "2026-11-24T06:00:00-05:00", "contracts": [contract(open_interest=11)]})
            store("future.json", {**data, "available_at": "2026-11-26T05:00:00-05:00"})
            results = chain.load_chain_history(path, CUTOFF)
            self.assertEqual([facts(r)["gross_gamma_1pct"] for r in results], [250000, 275000])
            exported = json.dumps(results)
            for token in ("SECRET_CONTENT", "PRIVATE_ACCOUNT", "private-download-path", "first.json"):
                self.assertNotIn(token, exported)
            store("conflict.json", {**data, "contracts": [contract(open_interest=12)]})
            conflict = chain.load_chain_history(path, CUTOFF)[0]
            self.assertEqual((conflict["status"], conflict["facts"], conflict["coverage"]["reason"]), ("invalid", [], "conflicting_snapshot"))
            (path / "broken.json").write_text("{incomplete", encoding="utf-8")
            self.assertEqual(chain.summarize_chain_file(path / "broken.json", CUTOFF)["status"], "invalid")
            (path / "ambiguous.json").write_text('{"gamma":1, "gamma":2}', encoding="utf-8")
            self.assertEqual(chain.summarize_chain_file(path / "ambiguous.json", CUTOFF)["status"], "invalid")
            self.assertEqual(chain.summarize_chain_file(path / "absent.json", CUTOFF)["status"], "missing")


if __name__ == "__main__":
    unittest.main()
