import unittest

from  src.markdown_to_blocks import markdown_to_blocks

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


