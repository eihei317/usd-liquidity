"""Reader-facing evidence always belongs to the selected frozen run."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.daily_brief import build_daily_brief, brief_markdown

CAPTURE_META = {"generated_at_bjt": "2026-11-24 14:43:15 UTC+08:00"}


def comparison(mid, **changes):
    return {
        "id": mid, "fact_id": "comparison:" + mid, "unit": "%", "status": "ok",
        "previous": 3.52, "value": 3.76, "change": 0.24, "as_of": "2026-11-20",
        "previous_as_of": "2026-11-19", "previous_package_generated_at_bjt": "2026-11-22",
        "comparison_kind": "new_observation", **changes,
    }


class DailyBrief(unittest.TestCase):
    def test_changed_evidence_prefers_explicit_comparisons_and_shows_its_dates(self):
        analysis = {"meta": CAPTURE_META, "key_takeaways": [
            {"fact_ids": ["derived:SOFR_ANCHOR", "comparison:BAMLH0A0HYM2"]},
            {"fact_ids": ["derived:SOFR_ANCHOR"]},
        ]}
        facts = {
            "comparison_facts": [comparison("BAMLH0A0HYM2"), comparison("SOFR")],
            "catalog": {"derived:SOFR_ANCHOR": {"base_fact_ids": ["metric:SOFR"]}},
        }
        brief = build_daily_brief(analysis, facts)
        self.assertEqual([item["fact_id"] for item in brief["evidence"]],
                         ["comparison:BAMLH0A0HYM2", "comparison:SOFR"])
        text = brief["evidence"][0]["text"]
        for expected in ("2026-11-19", "2026-11-20", "2026-11-22", "3.52%", "3.76%", "24基点"):
            self.assertIn(expected, text)

    def test_missing_stale_cached_and_future_baselines_never_become_changes(self):
        for changes in ({"status": "stale"}, {"previous_source_status": "cached_after_fetch_failure"},
                        {"previous_package_generated_at_bjt": "2026-11-16"}, {"previous": None}):
            with self.subTest(changes=changes):
                brief = build_daily_brief({"meta": CAPTURE_META, "key_takeaways": [{"fact_ids": ["metric:SOFR"]}],
                                          "investment_assessment": {"change_summary": "有新增观测"}},
                                         {"comparison_facts": [comparison("SOFR", **changes)]})
                self.assertEqual([], brief["evidence"])
                self.assertIn("没有可直接比较", brief["comparison"])

    def test_new_reports_show_only_change_summary_references_in_the_chosen_order(self):
        refs = ["comparison:IORB", "comparison:SOFR"]
        fixed = comparison("IORB", previous=3.76, change=0, previous_as_of="2026-11-20", comparison_kind="unchanged")
        revised = comparison("SOFR", previous_as_of="2026-11-20", comparison_kind="revision_same_observation_date")
        facts = {"comparison_facts": [revised, fixed, comparison("EFFR")]}
        research = {"change_fact_ids": refs, "change_summary": "昨天的融资利率有修订。"}
        analysis = {"meta": CAPTURE_META, "investment_assessment": research,
                    "key_takeaways": [{"fact_ids": ["comparison:EFFR"]}]}
        brief = build_daily_brief(analysis, facts)
        self.assertEqual(refs, [item["fact_id"] for item in brief["evidence"]])
        self.assertEqual(research["change_summary"], brief["comparison"])
        self.assertIn("相同", brief["evidence"][0]["text"])
        self.assertIn("24基点", brief["evidence"][1]["text"])
        research["change_fact_ids"] = []
        self.assertEqual([], build_daily_brief(analysis, facts)["evidence"])

    def test_only_same_dates_and_unchanged_values_replace_older_model_comment(self):
        analysis = {"meta": CAPTURE_META, "investment_assessment": {"change_summary": "已公布新一期数据"}}
        same = comparison("SOFR", previous=3.76, change=0,
                          previous_as_of="2026-11-20", comparison_kind="unchanged")
        self.assertIn("均未变化", build_daily_brief(analysis, {"comparison_facts": [same]})["comparison"])
        new_date = dict(same, previous_as_of="2026-11-19", comparison_kind="new_observation")
        self.assertEqual("已公布新一期数据", build_daily_brief(analysis, {"comparison_facts": [new_date]})["comparison"])

    def test_baseline_must_be_a_distinct_earlier_capture(self):
        analysis = {"meta": CAPTURE_META, "key_takeaways": [{"fact_ids": ["metric:SOFR"]}]}
        for stamp in ("2026-11-24T06:43:15Z", "2026-11-24 14:43:16 UTC+08:00", None, "invalid"):
            with self.subTest(stamp=stamp):
                row = comparison("SOFR", previous_package_generated_at_bjt=stamp)
                brief = build_daily_brief(analysis, {"comparison_facts": [row]})
                self.assertEqual([], brief["evidence"])
                self.assertIn("没有可直接比较", brief["comparison"])
        earlier = comparison("SOFR", previous_package_generated_at_bjt="2026-11-24T06:43:14Z")
        self.assertEqual(1, len(build_daily_brief(analysis, {"comparison_facts": [earlier]})["evidence"]))

    def test_legacy_partials_and_conditional_alert_do_not_drop_the_condition(self):
        analysis = {"investment_assessment": {"equities": {"summary": "融资成本回落"}},
                    "risk_flags": [{"priority": "P0", "text": "融资可能收紧", "condition": "利差继续扩大"}]}
        text = brief_markdown(build_daily_brief(analysis, {}))
        for expected in ("利差继续扩大", "美股", "融资成本回落", "(dashboard.html)"):
            self.assertIn(expected, text)
