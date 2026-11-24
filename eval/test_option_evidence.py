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

    def test_volatility_gap_uses_volatility_points_and_previous_only_percentile(self):
        ref = {"window": 252, "count": 252, "at_or_below": 189, "percentile": 75, "high": 9.6,
               "start": "2025-11-19", "end": "2026-11-19"}
        fields = {"vix_pct": 18, "realized_vol_pct": 20, "previous_as_of": "2026-11-19", "change": -1.3}
        text = evidence("option:SPX:iv_minus_rv21", -2, reference=ref, **fields)
        for phrase in ("-2个波动率点", "18%", "20%", "减少1.3个波动率点", "不含本期", "75%", "最高为9.6个波动率点"):
            self.assertIn(phrase, text)
        for invalid in (dict(ref, count=251), dict(ref, end="2026-11-20"), dict(ref, high=None)):
            limited = evidence("option:SPX:iv_minus_rv21", -2, reference=invalid, **fields)
            self.assertIn("-2个波动率点", limited)
            self.assertNotIn("最高为", limited)

    def test_oi_share_uses_total_contracts_and_percentage_point_changes(self):
        ref = {"window": 52, "count": 52, "at_or_below": 26, "percentile": 50, "high": 30,
               "start": "2025-11-14", "end": "2026-11-13"}
        text = evidence("option:SP500_FUTURES:option_oi_share", 25, combined_oi=100000, futures_only_oi=75000,
                        previous_as_of="2026-11-13", change=2, reference=ref)
        for phrase in ("25%", "100,000手期货等值", "75,000手", "增加2个百分点", "不含本期", "最高为30%"):
            self.assertIn(phrase, text)
        self.assertNotIn("交易商", text)

    def test_published_share_comparisons_preserve_units_and_identify_revisions(self):
        base = {"fact_id": "comparison:option_oi_share", "unit": "%", "as_of": "2026-11-17", "value": 25,
                "previous_as_of": "2026-11-10", "previous": 23.5, "change": 1.5,
                "previous_package_generated_at_bjt": "2026-11-16"}
        self.assertIn("增加1.5个百分点", format_fact_evidence(base))
        revised = dict(base, previous_as_of=base["as_of"], previous_package_generated_at_bjt="2026-11-20")
        self.assertIn("修订为25%，上修1.5个百分点", format_fact_evidence(revised))
        self.assertIn("沿用", format_fact_evidence(dict(revised, previous=25, change=0)))
        vol = dict(base, fact_id="comparison:iv_minus_rv21", unit="波动率点", previous=-1, value=.5)
        self.assertIn("增加1.5个波动率点", format_fact_evidence(vol))
