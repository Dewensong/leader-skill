import tempfile
import unittest
from pathlib import Path

from tools.version_manager import restore_version, snapshot_leader_state


class VersionManagerTests(unittest.TestCase):
    def test_restore_version_recovers_previous_file_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            leader_dir = Path(temp_dir) / "leaders" / "steady-manager"
            leader_dir.mkdir(parents=True)
            (leader_dir / "persona.md").write_text("v1 persona", encoding="utf-8")
            (leader_dir / "intent-map.md").write_text("v1 intent", encoding="utf-8")
            (leader_dir / "playbook.md").write_text("v1 playbook", encoding="utf-8")
            (leader_dir / "sources.json").write_text("[]", encoding="utf-8")
            (leader_dir / "corrections.md").write_text("# Corrections\n", encoding="utf-8")

            version_id = snapshot_leader_state(leader_dir, note="initial")
            (leader_dir / "persona.md").write_text("v2 persona", encoding="utf-8")

            restore_version(leader_dir, version_id)

            self.assertEqual(
                (leader_dir / "persona.md").read_text(encoding="utf-8"),
                "v1 persona",
            )


if __name__ == "__main__":
    unittest.main()
