import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode(text="This is a code `code block` test", text_type=TextType.TEXT)
        actual = split_nodes_delimiter(old_nodes=[node], delimiter='`', text_type=TextType.CODE)
        expected = [
            TextNode("This is a code ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" test", TextType.TEXT)
        ]
        self.assertEqual(expected, actual)


    def test_nested_delimiters(self):
        node = TextNode(text="This is a **nested _italics block_** wow", text_type=TextType.TEXT)
        actual = split_nodes_delimiter([node], delimiter='**', text_type=TextType.BOLD)
        expected = [
            TextNode("This is a ", text_type=TextType.TEXT),
            TextNode("nested _italics block_", text_type=TextType.BOLD),
            TextNode(" wow" ,TextType.TEXT)
        ]   
        self.assertEqual(expected, actual)

    def test_multiple_delimiter(self):
        node = TextNode(text="first **bold** node", text_type=TextType.TEXT)
        node2 = TextNode(text="second **bold** node", text_type=TextType.TEXT)
        actual = split_nodes_delimiter([node, node2], delimiter='**', text_type=TextType.BOLD)
        expected = [
            TextNode("first ", text_type=TextType.TEXT),
            TextNode("bold", text_type=TextType.BOLD),
            TextNode(" node" ,TextType.TEXT),
            TextNode("second ", text_type=TextType.TEXT),
            TextNode("bold", text_type=TextType.BOLD),
            TextNode(" node" ,TextType.TEXT),
        ]
        self.assertEqual(expected, actual)

    def test_delimiter_at_start(self):
        node = TextNode("`code block` test", text_type=TextType.TEXT)
        actual = split_nodes_delimiter([node], delimiter='`', text_type=TextType.CODE)
        expected = [
            TextNode("code block", text_type=TextType.CODE),
            TextNode(" test", text_type=TextType.TEXT)
        ]
        self.assertEqual(expected, actual)
        

    def test_delimiter_at_end(self):
        node = TextNode("this is a `code block`", text_type=TextType.TEXT)
        actual = split_nodes_delimiter([node], delimiter='`', text_type=TextType.CODE)
        expected = [
            TextNode("this is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(expected, actual)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code block`", text_type=TextType.TEXT)
        actual = split_nodes_delimiter([node], delimiter="`", text_type=TextType.CODE) 
        expected = [TextNode("code block", text_type=TextType.CODE)]
        self.assertEqual(expected, actual)
    
    def test_non_text_nodes_unchanged(self):
        text_node = TextNode("this is **bold**", TextType.TEXT)
        bold_node = TextNode("already bold", TextType.BOLD)

        actual = split_nodes_delimiter([text_node, bold_node], "**", text_type=TextType.BOLD)
        expected = [
            TextNode(text="this is ", text_type=TextType.TEXT),
            TextNode(text="bold", text_type=TextType.BOLD),
            TextNode(text="already bold", text_type=TextType.BOLD)
        ] 
        self.assertEqual(expected, actual)
    
    def test_invalid_delimiter(self):
        node = TextNode(text="This is a code `code block` test", text_type=TextType.TEXT)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], 'x', TextType.CODE)

    def test_unmatched_delimiter(self):
        node = TextNode(text="this text is _italics delimiter", text_type=TextType.TEXT)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], delimiter="_", text_type=TextType.ITALIC)


class TestSplitNodeImages(unittest.TestCase):
    pass

class TestSplitNodeLinks(unittest.TestCase):
    pass