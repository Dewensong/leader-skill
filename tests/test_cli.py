import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, args: list[str]) -> subprocess.CompletedProcess:
        completed = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=False,
            cwd=Path(__file__).resolve().parents[1],
        )
        completed.stdout = completed.stdout.decode("utf-8")
        completed.stderr = completed.stderr.decode("utf-8")
        return completed

    def test_create_leader_command_generates_instance(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / "leaders").mkdir()
            command = [
                sys.executable,
                "-m",
                "tools.cli",
                "create-leader",
                "--root",
                str(repo_root),
                "--slug",
                "steady-boss",
                "--name",
                "稳健型老板",
                "--text",
                "这个不复杂吧，你今天先出个方案。",
            ]

            completed = self.run_cli(command)

            output = json.loads(completed.stdout)
            self.assertEqual(output["slug"], "steady-boss")
            self.assertTrue((repo_root / "leaders" / "steady-boss" / "persona.md").exists())

    def test_translate_command_supports_markdown_output(self):
        command = [
            sys.executable,
            "-m",
            "tools.cli",
            "translate",
            "--text",
            "这个你先看一下，晚点我们再对齐。",
        ]

        completed = self.run_cli(command)

        self.assertIn("## 实际意思", completed.stdout)
        self.assertIn("## 画像摘要", completed.stdout)
        self.assertIn("## 风险点", completed.stdout)
        self.assertIn("## 建议回复", completed.stdout)

    def test_show_leader_command_supports_markdown_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / "leaders").mkdir()
            create_command = [
                sys.executable,
                "-m",
                "tools.cli",
                "create-leader",
                "--root",
                str(repo_root),
                "--slug",
                "steady-boss",
                "--name",
                "稳健型老板",
                "--text",
                "这个不复杂吧，你今天先出个方案。",
            ]
            self.run_cli(create_command)

            show_command = [
                sys.executable,
                "-m",
                "tools.cli",
                "show-leader",
                "--root",
                str(repo_root),
                "--slug",
                "steady-boss",
            ]
            completed = self.run_cli(show_command)

            self.assertIn("# 稳健型老板", completed.stdout)
            self.assertIn("## 画像", completed.stdout)
            self.assertIn("## 生存手册", completed.stdout)

    def test_persona_command_highlights_leader_style(self):
        command = [
            sys.executable,
            "-m",
            "tools.cli",
            "persona",
            "--text",
            "这个你先看一下，晚点我们再对齐。",
        ]

        completed = self.run_cli(command)

        self.assertIn("# 领导画像", completed.stdout)
        self.assertIn("愿景管理", completed.stdout)
        self.assertIn("口头优先级偏高", completed.stdout)

    def test_priority_command_supports_markdown_output(self):
        command = [
            sys.executable,
            "-m",
            "tools.cli",
            "priority",
            "--text",
            "这个不复杂吧，你今天先出个方案，明天我们同步一下。",
        ]

        completed = self.run_cli(command)

        self.assertIn("# 优先级判断", completed.stdout)
        self.assertIn("高优先级", completed.stdout)
        self.assertIn("今晚加班概率", completed.stdout)

    def test_reply_command_defaults_to_markdown(self):
        command = [
            sys.executable,
            "-m",
            "tools.cli",
            "reply",
            "--text",
            "这个你灵活处理一下。",
        ]

        completed = self.run_cli(command)

        self.assertIn("# 建议回复", completed.stdout)
        self.assertIn("## 建议追问", completed.stdout)


if __name__ == "__main__":
    unittest.main()
