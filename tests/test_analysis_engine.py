import unittest

from tools.analysis_engine import analyze_message


class AnalysisEngineTests(unittest.TestCase):
    def test_translate_recognizes_soft_push_language(self):
        result = analyze_message("这个你先看一下，晚点我们再对齐。")

        self.assertIn("不是简单看看", result["actual_meaning"])
        self.assertIn("优先级", result["risk_points"][0])
        self.assertGreaterEqual(result["scores"]["overtime_probability"], 60)

    def test_translate_flags_scope_pressure(self):
        result = analyze_message("这个不复杂吧，你今天先出个方案，明天我们同步一下。")

        self.assertIn("需求还没完全定义", result["actual_meaning"])
        self.assertTrue(
            any("验收标准" in item for item in result["risk_points"]),
            result["risk_points"],
        )
        self.assertGreaterEqual(result["scores"]["blame_risk"], 70)


if __name__ == "__main__":
    unittest.main()
