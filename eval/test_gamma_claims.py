import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.analysis_validator import _fact_is_fresh, _unfresh_fact_ids, _validate_option_claims, validate_analysis


MODEL = "option:SPX:model_delta_change_1pct"
POSITION = "option:SP500_FUTURES:dealer_option_delta"
CHAIN = "option:SPX:gross_gamma_1pct"
SHORT = "option:SPX:gamma_share_7d"
FACTS = {MODEL: {"status": "ok", "value": 3.87}, POSITION: {"status": "ok", "value": -14191}}


def check(candidate, facts=FACTS, version="3.2"):
    errors = []
    _validate_option_claims(candidate, {"research_version": version}, facts, errors)
    return errors


class OptionClaims(unittest.TestCase):
    def test_unsupported_market_direction_flows_and_squeeze(self):
        for prose in ("美股已发生Gamma挤压。", "价格反弹说明做市商已处于负 Gamma。",
                      "做市商的净Gamma已经转为负。", "做市商正Gamma已确认并可能放大波动。",
                      "做市商被迫买入标普期货。", "做市商的对冲买盘正在推高股价。",
                      "The gamma squeeze is underway.", "Dealers are short gamma.",
                      "指标仍有缺口，但当前市场进入负Gamma区间。"):
            with self.subTest(text=prose):
                self.assertTrue(check({"stance": {"one_liner": prose}}))

    def test_hedged_observations_missing_evidence_and_unrelated_pressure(self):
        for prose in ("若做市商处于负Gamma，对冲买入可能放大指数反弹。",
                      "现有数据无法确认做市商处于负Gamma。", "期权Gamma挤压尚未得到证实。",
                      "暂不清楚是否已经发生逼空。", "Gamma挤压的风险值得观察。",
                      "交易商在该期货期权周报中的净方向仍是净空，无法据此判断做市商净Gamma符号。",
                      "模型中的标准平值看涨期权和看跌期权均具有正Gamma。",
                      "评级利差走阔，企业的现金流受融资成本挤压。",
                      "缺少未平仓量加权的无符号Gamma，暂时无法判断集中度。",
                      "If dealers are short gamma, their hedging could amplify a rally."):
            with self.subTest(text=prose):
                self.assertFalse(check({"narrative_blocks": {"market_transmission": prose}}))
        self.assertTrue(check({"stance": {"one_liner": "无法确认资金流方向，但做市商已经处于负Gamma。"}}))

    def test_short_squeeze_has_a_market_and_partial_latest_is_historical(self):
        for text in ("日元空头回补引发轧空。", "日元轧空拖累美股。", "美债遭遇逼空。",
                     "Short positions in Japanese Treasuries faced a short squeeze."):
            self.assertFalse(check({"narrative_blocks": {"jpy_carry": {"analysis": text}}}))
        self.assertTrue(check({"stance": {"one_liner": "美股期权已经发生轧空。"}}))
        self.assertTrue(check({"investment_assessment": {"equities": {"summary": "逼空已经发生。"}}}))
        rows = {"option:model": {"as_of": "2026-11-20", "value": 3.87, "status": "partial_latest", "source_status": "ok"},
                "derived:child": {"base_fact_ids": ["option:model"], "value": 2}}
        self.assertFalse(_fact_is_fresh(rows["option:model"]))
        self.assertEqual(_unfresh_fact_ids(rows), set(rows))

    def test_scenario_scope_and_all_narrative_sections(self):
        self.assertFalse(check({"risk_flags": [{"claim_type": "scenario", "title": "Gamma挤压",
                                               "text": "若做市商持有负Gamma，回补可能放大涨幅。",
                                               "condition": "期权逐笔成交和交易商仓位支持这一方向。"}]}))
        for candidate in (
            {"risk_flags": [{"claim_type": "scenario", "title": "Gamma挤压已经发生"}]},
            {"investment_assessment": {"scenarios": {"upside": {"path": "做市商已经处于负Gamma。"}}}},
            {"investment_assessment": {"next_checks": ["做市商正在买入期货对冲。"]}},
            {"key_takeaways": [{"title": "做市商净Gamma为负", "fact_ids": [MODEL, POSITION]}]},
        ):
            self.assertTrue(check(candidate))

    def test_chain_source_and_old_packages(self):
        claim = {"fact_ids": [MODEL, POSITION], "text": "无符号Gamma敞口处于高位。"}
        self.assertTrue(check({"key_takeaways": [claim]}))
        facts = {**FACTS, CHAIN: {"status": "ok", "value": 15}, SHORT: {"status": "ok", "value": 34}}
        self.assertTrue(check({"key_takeaways": [claim]}, facts))
        self.assertFalse(check({"key_takeaways": [{**claim, "fact_ids": [CHAIN]}]}, facts))
        self.assertTrue(check({"key_takeaways": [{**claim, "fact_ids": [CHAIN], "text": "七天内到期合约的Gamma占比上升。"}]}, facts))
        self.assertTrue(check({"stance": {"one_liner": "全市场Gamma敞口处于高位。"}},
                              {CHAIN: {"status": "stale", "value": 15}}))
        self.assertFalse(check({"stance": {"one_liner": "Gamma挤压已经发生。"}}, {}, version="3.1"))
        errors = validate_analysis({"stance": {"one_liner": "Gamma挤压已经发生。"}},
                                   {"research_version": "3.2", "data": {"facts": {}}})
        self.assertTrue(any("对冲流" in error for error in errors))
