import unittest
from sprechzeit import calculate


class SprechzeitTests(unittest.TestCase):
    def test_known_duration_with_pauses(self):
        text = " ".join(["Wort"] * 120) + " [Pause: 30 s] [Pause: 0,5 min]"
        result = calculate(text, 60, 120)
        self.assertEqual(result["words"], 120)
        self.assertEqual(result["pause_seconds"], 60)
        self.assertEqual(result["shortest_seconds"], 120)
        self.assertEqual(result["longest_seconds"], 180)

    def test_nonspoken_parts(self):
        result = calculate("# Meine Überschrift\n[Regie: leise lesen]\nEin kurzer Sprechtext.", 60, 60)
        self.assertEqual(result["words"], 3)
        self.assertEqual(result["longest_seconds"], 3)

    def test_unicode_and_hyphenated_words(self):
        result = calculate("Äußere Ruhe. Ein PDF-Dokument.", 60, 60)
        self.assertEqual(result["words"], 4)

    def test_malformed_pause_is_not_silently_ignored(self):
        for marker in ["[Pause: -10 s]", "[Pause: zehn Sekunden]", "[Pause: 5 h]", "[Pause: 10 s"]:
            with self.subTest(marker=marker), self.assertRaises(ValueError):
                calculate(marker)

    def test_invalid_speeds(self):
        for slow, fast in [(0, 100), (-1, 100), (100, 90), (float("nan"), 100), (90, float("inf"))]:
            with self.subTest(slow=slow, fast=fast), self.assertRaises(ValueError):
                calculate("Text", slow, fast)

    def test_empty_file_and_pause_only(self):
        self.assertEqual(calculate("")["longest_seconds"], 0)
        self.assertEqual(calculate("[Pause: 12.5 s]")["longest_seconds"], 13)


if __name__ == "__main__":
    unittest.main()
