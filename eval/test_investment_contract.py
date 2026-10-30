"""Contract regressions for research fields that used to bypass claim checks."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.investment_contract import INVESTMENT_SCHEMA, validate_investment
from scripts.analysis_validator import _validate_schema


def sample_assessment():
    asset = {"liquidity_bias": "分化", "confidence": "中等", "horizon": "2—12周",
             "summary": "即时改善与结构缓冲偏薄并存。", "transmission": "融资和折现率影响风险承担。",
             "confirmation": "价格只提供下游确认。", "invalidation": "融资溢价持续扩大将推翻改善判断。",
             "coverage_limits": "缺增长、盈利和直接资金流数据。", "fact_ids": ["metric:SOFR"]}
    return {"summary": "流动性贡献分化。", "change_summary": "首期没有可比事实。",
            "equities": copy.deepcopy(asset), "bitcoin": copy.deepcopy(asset),
            "expectations": {"status": "数据不足", "summary": "缺直接预期数据。", "fact_ids": ["coverage:EXPECTATIONS"]},
            "scenarios": {key: {"path": text, "trigger": "融资溢价与信用方向同步确认。",
                                "invalidation": "两者反向分化。", "fact_ids": ["metric:SOFR"]}
                          for key, text in (("base", "区间分化。"), ("upside", "压力持续缓和。"), ("downside", "融资压力扩散。"))},
            "next_checks": ["下轮观察融资溢价与实际利率持续性。"]}


class ResearchContract(unittest.TestCase):
    def setUp(self):
        self.value = {"investment_assessment": sample_assessment()}
        self.package = {"research_version": "3.0"}
        self.facts = {"metric:SOFR": {"status": "ok", "value": 4},
                      "coverage:EXPECTATIONS": {"status": "missing"},
                      "metric:VIXCLS": {"status": "ok", "value": 20}}

    def validate(self):
        errors = []
        _validate_schema(self.value["investment_assessment"], INVESTMENT_SCHEMA, "$", errors)
        return errors + validate_investment(self.value, self.package, self.facts)

    def test_valid_qualitative_research(self):
        self.assertEqual([], self.validate())

    def test_required_for_new_method_only(self):
        self.assertTrue(validate_investment({}, self.package, self.facts))
        self.assertEqual([], validate_investment({}, {}, self.facts))

    def test_unknown_citation(self):
        self.value["investment_assessment"]["scenarios"]["upside"]["fact_ids"] = ["invented:id"]
        self.assertTrue(any("未找到" in s for s in self.validate()))

    def test_prices_cannot_create_liquidity_signal(self):
        self.value["investment_assessment"]["equities"]["fact_ids"] = ["metric:VIXCLS"]
        self.assertTrue(any("上游" in s for s in self.validate()))

    def test_stale_driver_is_not_confirmation(self):
        errors = validate_investment(self.value, self.package, self.facts, {"metric:SOFR"})
        self.assertTrue(any("上游" in s for s in errors))

    def test_expectations_proxy_cannot_be_full_coverage(self):
        self.value["investment_assessment"]["expectations"]["status"] = "已覆盖"
        self.assertTrue(any("直接市场" in s for s in self.validate()))

    def test_stale_direct_expectation_is_not_full_coverage(self):
        self.facts['market:future'] = {'value': 4, 'status': 'ok', 'measurement_type': 'direct_market_pricing'}
        self.value['investment_assessment']['expectations'].update(status='已覆盖', fact_ids=['market:future'])
        errors = validate_investment(self.value, self.package, self.facts, {'market:future'})
        self.assertTrue(any('直接市场' in s for s in errors))

    def test_high_confidence_needs_independent_trends(self):
        self.value["investment_assessment"]["bitcoin"]["confidence"] = "高"
        self.assertTrue(any("多期" in s for s in self.validate()))

    def test_policy_anchor_cannot_be_second_vote(self):
        self.facts['metric:IORB'] = {'value': 4, 'status': 'ok'}
        self.facts['trend:SOFR_IORB:20obs'] = {
            'value': 1, 'status': 'ok', 'window_observations': 20,
            'base_fact_ids': ['metric:SOFR', 'metric:IORB']}
        asset = self.value['investment_assessment']['equities']
        asset.update(confidence='高', fact_ids=['trend:SOFR_IORB:20obs'])
        self.assertTrue(any('独立机制' in s for s in self.validate()))

    def test_multiple_curve_tenors_cannot_be_second_mechanism(self):
        for mid in ('DGS5', 'DGS7'):
            self.facts['metric:' + mid] = {'value': 4, 'status': 'ok'}
            self.facts['trend:' + mid + ':20obs'] = {
                'value': 1, 'status': 'ok', 'window_observations': 20,
                'base_fact_ids': ['metric:' + mid]}
        self.value['investment_assessment']['equities'].update(
            confidence='高', fact_ids=['trend:DGS5:20obs', 'trend:DGS7:20obs'])
        self.assertTrue(any('独立机制' in s for s in self.validate()))

    def test_scenario_cannot_omit_invalidation(self):
        del self.value["investment_assessment"]["scenarios"]["upside"]["invalidation"]
        self.assertTrue(any("invalidation" in s for s in self.validate()))

    def test_unsupported_probability_or_price(self):
        self.value["investment_assessment"]["summary"] = "上涨概率80%，目标100000美元。"
        self.assertTrue(any("数值" in s for s in self.validate()))


if __name__ == "__main__":
    unittest.main()
