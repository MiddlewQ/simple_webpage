import unittest

from src.block_type import BlockType, block_to_block_type

class TestBlockTypeConversion(unittest.TestCase):
    def test_simple_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)


    def test_heading_smallest(self):
        block = "###### This is a smaller heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_heading_invalid(self):
        block = "####### This heading has too many '#'"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_heading_missing_space(self):
        block = "#Woops I forgot the space"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_heading_missing_text(self):
        block = "# "
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_code_block(self):
        block = "```\nCODE BLOCK HERE```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_code_block_missing_start(self):
        block = "CODE BLOCK HERE```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_code_block_missing_end(self):
        block = "```\nCODE BLOCK HERE"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_single_quote(self):
        block = "> Me when I quote myself"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_multiple_quotes(self):
        block = "> Greentext start\n> Second Item\n> Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_quotes_missing_startofline(self):
        block = "> This test fails after first item\nItem2\n> Item3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_quotes_no_text(self):
        block = "> "
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_unordered_list(self):
        block = "- This is a list\n- item2\n- item3\n- item4"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_unordered_list_missing_startofline(self):
        block = "- This is not a list\nMissing start\n- item2\n- item3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_unordered_list_no_text(self):
        block = "- "
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)


    def test_ordered_list_single_item(self):
        block = "1. Single Item List"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_ordered_list_multiple_items(self):
        block = "1. Multilist\n2. Second Item\n3. Third Item\n4. Forth Item."
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_ordered_list_missing_item(self):
        block = "1. First item valid\n2. Second item valid\nMissing third"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_orderd_list_wrong_order(self):
        block = "1. First Item\n3. Second Item\n2. Third Item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_ordered_list_repeating_numbers(self):
        block = "1. First Item\n1. Second Item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_paragraph(self):
        block = "This is a normal paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_empty_paragraph(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)