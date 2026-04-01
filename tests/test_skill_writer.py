import json
import tempfile
import unittest
from pathlib import Path

from tools.skill_writer import create_leader_instance


class SkillWriterTests(unittest.TestCase):
    def test_create_leader_instance_writes_expected_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = create_leader_instance(
                root=root,
                slug="visionary-director",
                display_name="愿景型总监",
                analyses=[
                    {
                        "source_label": "manual-text",
                        "actual_meaning": "不是简单看看，而是希望你尽快产出一个可评审版本。",
                        "priority_signal": "今天最好给到初版。",
                        "risk_points": ["优先级没有明说，容易挤占当前排期。"],
                        "reply_suggestion": "我今晚先给你一版可评审内容，明天同步时一起确认范围。",
                        "follow_up_questions": [
                            "你更希望我先给方案、结论，还是一版可直接评审的初稿？",
                            "这次同步最需要对齐的是方向、范围，还是口径和优先级？",
                            "验收标准和截止时间，我要不要先整理成书面版给你确认？",
                        ],
                        "persona_summary": "推进节奏偏快；习惯先推进再补边界。",
                        "persona_tags": ["愿景管理", "口头优先级偏高"],
                        "scores": {
                            "blame_risk": 71,
                            "scope_creep": 80,
                            "overtime_probability": 76,
                        },
                    }
                ],
                sources=[
                    {
                        "type": "text",
                        "label": "manual-text",
                        "preview": "这个你先看一下",
                    }
                ],
            )

            self.assertTrue((output_dir / "persona.md").exists())
            self.assertTrue((output_dir / "intent-map.md").exists())
            self.assertTrue((output_dir / "playbook.md").exists())
            self.assertTrue((output_dir / "sources.json").exists())
            self.assertTrue((output_dir / "corrections.md").exists())
            self.assertTrue((output_dir / "README.md").exists())
            self.assertTrue((output_dir / "versions").exists())

            sources = json.loads((output_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual(sources[0]["label"], "manual-text")
            readme = (output_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("快速速览", readme)


if __name__ == "__main__":
    unittest.main()
