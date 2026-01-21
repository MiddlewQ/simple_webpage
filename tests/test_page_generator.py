import unittest

from src.page_generator import extract_title


class TestPageGeneration(unittest.TestCase):

    def test_extract_title(self):
        md = "# Valid title"
        title = extract_title(md)
        self.assertEqual("Valid title", title)

    def test_invalid_heading(self):
        md = "## Wrong heading"
        with self.assertRaises(ValueError):
            title = extract_title(md)

    def test_missing_heading(self):
        md = "This text is missing its heading"
        with self.assertRaises(ValueError):
            title = extract_title(md)