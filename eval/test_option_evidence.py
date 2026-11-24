"""Verify the units, scope, and direction of reader-facing options evidence."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.evidence import format_fact_evidence


def evidence(fid, value, **fields):
    return format_fact_evidence({"fact_id": fid, "as_of": "2026-11-20", "value": value, "status": "ok", **fields})


class OptionEvidence(unittest.TestCase):
    def test_model_sensitivity_and_change_are_both_delta_percentage_points(self):
        text = evidence("option:SPX:model_delta_change_1pct", 4.41, previous_as_of="2026-11-19", change=-.22)
        for expected in ("2026-11-20", "30天平值", "指数上涨1%", "Delta 约增加4.41个百分点", "2026-11-19的读数减少0.22个百分点"):
            self.assertIn(expected, text)

    def test_decreasing_net_short_moves_toward_long_in_futures_equivalents(self):
        text = evidence("option:SP500_FUTURES:dealer_option_delta", -380, previous_as_of="2026-11-13", change=20)
        self.assertIn("净空380手期货等值", text)
        self.assertIn("向多头方向变化20手期货等值", text)
        self.assertNotIn("Gamma", text)
        self.assertNotIn("较", evidence("option:SP500_FUTURES:dealer_option_delta", 0, change=None))

    def test_chain_dollars_and_concentration_change_use_different_units(self):
        gross = evidence("option:SPX:gross_gamma_1pct", 2.5e8, previous_as_of="2026-11-19", change=-5e7)
        self.assertIn("按绝对值合计2.5亿美元", gross)
        self.assertIn("减少5,000万美元", gross)
        share = evidence("option:SPX:gamma_share_7d", 12, previous_as_of="2026-11-19", change=1.5)
        self.assertIn("12%", share)
        self.assertIn("增加1.5个百分点", share)
        self.assertIn("0%", evidence("option:SPX:gamma_share_0dte", 0))

    def test_unusable_facts_are_not_numbers_and_older_points_are_dated(self):
        for status in ("missing", "invalid", "partial", "redistribution_unconfirmed"):
            self.assertNotIn("123", evidence("option:SPX:gross_gamma_1pct", 123, status=status))
        self.assertIn("未能配对", evidence("option:SPX:model_delta_change_1pct", 6, status="partial_latest"))
        self.assertIn("已过期", evidence("option:SP500_FUTURES:dealer_option_delta", 600, status="stale"))
        self.assertIn("实际对冲成交", format_fact_evidence({"fact_id": "coverage:spx_dealer_gamma",
                                                      "status": "missing", "message": "缺少实际对冲成交。"}))
