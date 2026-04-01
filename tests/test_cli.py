import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
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

            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=Path(__file__).resolve().parents[1],
            )

            output = json.loads(completed.stdout)
            self.assertEqual(output["slug"], "steady-boss")
            self.assertTrue((repo_root / "leaders" / "steady-boss" / "persona.md").exists())


if __name__ == "__main__":
    unittest.main()
