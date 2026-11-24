import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.analysis import _compact_jpy_carry_payload
from scripts.analysis_validator import _validate_p0, format_fact_evidence
from scripts.jpy_carry import _decompose_cftc_net


def observation(fid, value, previous, unit="%", **extra):
    return {"fact_id": fid, "id": fid.split(":")[1], "as_of": "2026-11-20",
            "previous_as_of": "2026-11-19", "value": value, "previous": previous,
            "change": value - previous, "unit": unit, "status": "ok", **extra}


def check_alarm(rows, title="回购融资承压", refs=None, claim_type="observed"):
    facts = {row["fact_id"]: row for row in rows}
    risk = {"priority": "P0", "type": "market", "severity": "high", "claim_type": claim_type,
            "title": title, "fact_ids": list(facts),
            "evidence_refs": [{"fact_id": fid} for fid in (refs or facts)]}
    errors = []
    _validate_p0({"risk_flags": [risk]}, facts, errors, "2026-11-24")
    return errors


class Alarm(unittest.TestCase):
    def setUp(self):
        self.repo = [observation("metric:SOFR", 5, 4.5), observation("metric:SRP_RATE", 4.9, 4.9),
                     observation("metric:SRP_ACCEPTED", 2, 0, "USD bn")]

    def test_secured_and_unsecured_confirmed(self):
        self.assertFalse(check_alarm(self.repo))
        self.assertFalse(check_alarm([observation("metric:EFFR", 5, 4.5),
                                     observation("metric:DFEDTARU", 4.9, 4.9), self.repo[-1]]))

    def test_normal_market_and_no_use(self):
        small_spread = observation("derived:SOFR_ANCHOR", 2, 1, "bp", base_fact_ids=["metric:SOFR"])
        no_usage = observation("metric:SRP_ACCEPTED", 0, .001, "USD bn", as_of="2026-11-23")
        self.assertTrue(check_alarm([self.repo[0], small_spread, no_usage]))
        for row, field, val in [(0, "value", 4.9), (1, "as_of", "2026-11-19"),
                                (2, "as_of", "2026-11-25"), (2, "value", 0),
                                (2, "previous_as_of", "2026-11-13"), (2, "window_observations", 5),
                                (2, "source_status", "cached_after_fetch_failure")]:
            with self.subTest(row=row, field=field):
                observed = copy.deepcopy(self.repo)
                observed[row][field] = val
                self.assertTrue(check_alarm(observed))
        self.assertTrue(check_alarm(self.repo, refs=["metric:SOFR", "metric:SRP_ACCEPTED"]))
        self.assertTrue(check_alarm(self.repo, claim_type="inference"))

    def test_severe_nonfunding_case_and_independence(self):
        equities = observation("market:SP500:level", 93, 100, "index")
        credit = observation("metric:BAMLH0A0HYM2", 4.5, 4)
        self.assertFalse(check_alarm([equities, credit], "信用和股票市场承压"))
        self.assertTrue(check_alarm([dict(equities, value=99), credit], "信用和股票市场承压"))
        self.assertTrue(check_alarm([dict(row, previous_as_of="2026-10-19") for row in (equities, credit)],
                                    "信用和股票市场承压"))
        same = observation("market:SP500:5obs", -9, 0, "%", base_fact_ids=[equities["fact_id"]])
        self.assertTrue(check_alarm([equities, same], "股票市场承压"))
        auction = observation("metric:TBILL_AUCTION_BTC", 0.8, 1.5, "x")
        self.assertFalse(check_alarm([auction, credit], "短债拍卖投标不足"))


class Evidence(unittest.TestCase):
    def test_money_and_window(self):
        weekly = observation("metric:WRESBAL", 2979.656, 2960.603, "USD bn",
                             as_of="2026-11-18", previous_as_of="2026-11-10")
        window = observation("trend:WRESBAL:5obs", 2979.656, 3022.14, "USD bn",
                             as_of="2026-11-18", previous_as_of="2026-10-14",
                             window_start="2026-10-14", window_end="2026-11-18", window_label="5个有效周频观测间隔")
        self.assertIn("增加190.53亿美元", format_fact_evidence(weekly))
        text = format_fact_evidence(window)
        for token in ["2026-10-14", "2026-11-18", "5个有效周频观测间隔", "减少424.84亿美元"]:
            self.assertIn(token, text)

    def test_rates_fractions_and_returns(self):
        oas = observation("metric:BAMLH0A0HYM2", 3.76, 3.52)
        self.assertIn("增加24基点", format_fact_evidence(oas))
        share = observation("jpy:CFTC_JPY_SHORT_SHARE", .35, .33, "short/(short+long)")
        self.assertIn("增加2个百分点", format_fact_evidence(share))
        ret = observation("market:SP500:5obs", -8.61, 0, measurement="price_return", window_label="5个有效日频观测间隔")
        text = format_fact_evidence(ret)
        self.assertIn("累计价格涨跌幅为-8.61%", text)
        self.assertNotIn("从0", text)
        repo = observation("metric:SRP_ACCEPTED", 0, .001, "USD bn")
        self.assertIn("减少0.01亿美元", format_fact_evidence(repo))

    def test_jpy_position_crossings_and_archive(self):
        self.assertIn("净多持仓收窄6,796手", _decompose_cftc_net(15793, 8997, .0186, -6796, 116317)["text"])
        self.assertIn("由净多转为净空2手", _decompose_cftc_net(10, 0, .02, -10, -2)["text"])
        self.assertIn("净空持仓收窄", _decompose_cftc_net(-10, 0, -.02, 10, -2)["text"])
        values = {"GROSS_LONG": (249759, 258756), "GROSS_SHORT": (126646, 142439), "SHORT_SHARE": (.33646, .35504)}
        history = {"CFTC_JPY_" + name: [{"date": d, "value": v} for d, v in zip(("2026-11-10", "2026-11-17"), pair)]
                   for name, pair in values.items()}
        payload = {"jpy_carry": {"history": history, "cftc_decomposition": {"text": "旧版净空解读", "carry_usd_support": True}}}
        with patch("scripts.analysis.load_jpy_carry_history_payload", return_value=payload):
            compact, _ = _compact_jpy_carry_payload()
            fact = compact["cftc_decomposition"]
            self.assertEqual(fact["as_of"], "2026-11-17")
            self.assertEqual(fact["net_contracts"], 116317)
            self.assertFalse(fact["carry_usd_support"])
            self.assertIn("净多持仓收窄6,796手", fact["text"])
            history["CFTC_JPY_SHORT_SHARE"][-1]["date"] = "2026-11-18"
            self.assertEqual(_compact_jpy_carry_payload()[0]["cftc_decomposition"]["driver"], "unknown")

    def test_calendar_is_a_schedule_and_returns_keep_source_status(self):
        calendar = {"fact_id": "calendar:7d", "as_of": "2026-11-24", "window_start": "2026-11-24",
                    "window_end": "2026-11-30", "event_count": 5, "unknown_amount_count": 1,
                    "gross_announced_offering_usd_bn": 286, "net_cash_impact_usd_bn": None}
        rendered = format_fact_evidence(calendar)
        for token in ("截至2026-11-24", "至 2026-11-30 结算", "2,860亿美元", "1笔金额待公布", "净筹资额未知"):
            self.assertIn(token, rendered)
        ret = observation("market:SP500:5obs", -8.61, 0, measurement="price_return")
        self.assertIn("过期", format_fact_evidence(dict(ret, status="stale")))
        self.assertIn("留存", format_fact_evidence(dict(ret, source_status="cached_after_fetch_failure")))
