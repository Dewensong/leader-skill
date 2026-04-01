import tempfile
import unittest
from pathlib import Path

from tools.source_router import load_source


class SourceRouterTests(unittest.TestCase):
    def test_markdown_document_is_loaded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "note.md"
            source_path.write_text("# title\n这个需求先看一下", encoding="utf-8")

            payload = load_source(source_path)

            self.assertEqual(payload["type"], "document")
            self.assertIn("这个需求先看一下", payload["text"])

    def test_eml_file_is_loaded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "mail.eml"
            source_path.write_text(
                "Subject: sync\nContent-Type: text/plain; charset=utf-8\n\n这个方案明天同步一下",
                encoding="utf-8",
            )

            payload = load_source(source_path)

            self.assertEqual(payload["type"], "email")
            self.assertIn("明天同步一下", payload["text"])


if __name__ == "__main__":
    unittest.main()
