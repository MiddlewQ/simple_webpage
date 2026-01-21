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
<<<<<<< HEAD
            title = extract_title(md)
=======
            _ = extract_title(md)
>>>>>>> 3c69d67 (add: extract title function)

    def test_missing_heading(self):
        md = "This text is missing its heading"
        with self.assertRaises(ValueError):
<<<<<<< HEAD
            title = extract_title(md)
=======
            _ = extract_title(md)
>>>>>>> 3c69d67 (add: extract title function)
