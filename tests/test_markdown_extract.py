from src.markdown_extract import *
import unittest

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple(self):
        matches = extract_markdown_images(
            "Text with multiple ![png](https://imgur.com/zjjcJKZ) and ![jpeg](https://i.imgur.com/CXxBBqW.jpeg)"
        )
        self.assertListEqual([("png", "https://imgur.com/zjjcJKZ"), ("jpeg","https://i.imgur.com/CXxBBqW.jpeg")], matches)


    def test_extract_markdown_empty(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_empty_alt(self):
        matches = extract_markdown_images("![](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

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
    
    def test_images_should_not_match_links(self):
        matches = extract_markdown_images("[alt](https://img.com/a.png)")
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_single(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com")], matches)

    def test_extract_markdown_multiple(self):
        matches = extract_markdown_links(
            "This text contains multiple [youtube link](https://youtube.com) an [instagram link](https://instagram.com)"
        )
        self.assertListEqual([("youtube link", "https://youtube.com"), ("instagram link", "https://instagram.com")], matches)

    def test_extract_markdown_empty(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_empty_alt(self):
        matches = extract_markdown_links("[](https://youtube.com)")
        self.assertListEqual([("", "https://youtube.com")], matches)

    def test_extract_markdown_missing_delimiter(self):
        matches = extract_markdown_links(
            "This text contains a missing [wow](https://test.com and cool](https://youtube.com)"
        )
        self.assertListEqual([], matches)
    
    def test_links_should_not_match_images(self):
        matches = extract_markdown_links("![alt](https://img.com/a.png)")
        self.assertListEqual([], matches)

    # def test_link_url_with_parentheses(self):
        # matches = extract_markdown_links("[x](https://en.wikipedia.org/wiki/Function_(mathematics))")
        # self.assertListEqual([("x", "https://en.wikipedia.org/wiki/Function_(mathematics))")], matches)


class TestMarkdownConvertBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks
        )

    def test_empty_markdown(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [],
            blocks
        )

    def test_markdown_heading(self):
        md = """
# Title: Chapter 2

There once was a boy, he died.

The end.
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "# Title: Chapter 2",
                "There once was a boy, he died.",
                "The end."
            ],
            blocks
        )
    def test_single_spacing(self):
        md = """
this
should
only
be
one
block
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "this\n"
                "should\n"
                "only\n"
                "be\n"
                "one\n"
                "block"
            ],
            blocks
        )

    def test_excessive_newlines(self):
        md = "a\n\n\nb\n\n\n\n\nc"
        blocks = markdown_to_blocks(md)
        self.assertListEqual(["a", "b", "c"], blocks)
