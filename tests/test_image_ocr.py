import tempfile
import unittest
from pathlib import Path

from tools.image_ocr import extract_text_from_image


class ImageOcrTests(unittest.TestCase):
    def test_sidecar_text_is_used_when_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "boss.png"
            sidecar_path = Path(temp_dir) / "boss.txt"
            image_path.write_bytes(b"fake-image")
            sidecar_path.write_text("这个你先看一下", encoding="utf-8")

            result = extract_text_from_image(image_path)

            self.assertEqual(result["method"], "sidecar")
            self.assertEqual(result["text"], "这个你先看一下")


if __name__ == "__main__":
    unittest.main()
