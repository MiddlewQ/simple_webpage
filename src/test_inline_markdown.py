from markdown_parsing import *
import unittest

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_empty(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)


    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images("![this is a text](wow almost fit")
        self.assertListEqual([], matches)

    def test_extract_markdown_missing_delimiter(self):
        matches = extract_markdown_images(
            "This is text missing delimter with an ![image](https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_missing_exclamation_mark(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) but no '!'"
        )
        self.assertListEqual([], matches)
    
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_single(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com")], matches)


    def test_extract_markdown_empty(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)



