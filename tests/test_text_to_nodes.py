import unittest

from src.textnode import TextNode, TextType
from src.text_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_delimiter_not_present(self):
        node = TextNode(text="This text should just return itself", text_type=TextType.TEXT)
        actual = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        expected = [node]
        self.assertEqual(expected, actual)


    def test_unmatched_delimiter(self):
        node = TextNode(text="this text is _italics delimiter", text_type=TextType.TEXT)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], delimiter="_", text_type=TextType.ITALIC)


class TestSplitNodeImages(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            text="This is a test with an ![image](https://i.imgur.com/zjjcJKZ.png).",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="This is a test with an ", text_type=TextType.TEXT),
                TextNode(text="image", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text=".", text_type=TextType.TEXT)
            ],
            new_nodes
        )
    def test_multiple_images(self):
        node = TextNode(
            text="This is a test with two images: ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://youtube.com). Cool right?!",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="This is a test with two images: ", text_type=TextType.TEXT),
                TextNode(text="image1", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text=" and ", text_type=TextType.TEXT), 
                TextNode(text="image2", text_type=TextType.IMAGE, url="https://youtube.com"),
                TextNode(text=". Cool right?!", text_type=TextType.TEXT)
            ],
            new_nodes
        )

    def test_multiple_nodes(self):
        node1 = TextNode(
            text="This is node one with an image: ![node1 image](https://i.imgur.com/zjjcJKZ.png).",
            text_type=TextType.TEXT
        )
        node2 = TextNode(
            text="This second node has a node called ![node2 image](https://youtube.com).",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode(text="This is node one with an image: ", text_type=TextType.TEXT),
                TextNode(text="node1 image", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text=".", text_type=TextType.TEXT),
                TextNode(text="This second node has a node called ", text_type=TextType.TEXT),
                TextNode(text="node2 image", text_type=TextType.IMAGE, url="https://youtube.com"),
                TextNode(text=".", text_type=TextType.TEXT) 
            ],
            new_nodes
        )

    def test_other_node_type(self):
        node1 = TextNode(
            text="This is a BOLD node",
            text_type=TextType.BOLD
        )
        node2 = TextNode(
            text="int main() { // ... }",
            text_type=TextType.CODE
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [node1, node2],
            new_nodes
        )

    def test_image_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
       )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with an ", text_type=TextType.TEXT),
                TextNode(text="image", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_image_start(self):
        node = TextNode(
            text="![image](https://i.imgur.com/zjjcJKZ.png) this is a node with an image as a start",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="image", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text=" this is a node with an image as a start", text_type=TextType.TEXT)
            ],
            new_nodes
        )

    def test_image_only(self):
        node = TextNode(
            text="![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="image", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )

    def test_no_images(self):
        node = TextNode(
            text="This test contains no images but it does contain: THE UNSTOPPABLE EXOODIA!",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes
        )
        
    def test_adjacent_images(self):
        node = TextNode(
            text="![a](https://a.com)![b](https://b.com)",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="a", text_type=TextType.IMAGE, url="https://a.com"),
                TextNode(text="b", text_type=TextType.IMAGE, url="https://b.com"),
            ],
            new_nodes,
        )
        

class TestSplitNodeLinks(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            text="This is a test with an [link text](https://youtube.com).",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is a test with an ", text_type=TextType.TEXT),
                TextNode(text="link text", text_type=TextType.LINK, url="https://youtube.com"),
                TextNode(text=".", text_type=TextType.TEXT)
            ],
            new_nodes
        )
    def test_multiple_links(self):
        node = TextNode(
            text="This is a test with two links: [link1](https://instagram.com) and [link2](https://youtube.com). Cool right?!",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is a test with two links: ", text_type=TextType.TEXT),
                TextNode(text="link1", text_type=TextType.LINK, url="https://instagram.com"),
                TextNode(text=" and ", text_type=TextType.TEXT), 
                TextNode(text="link2", text_type=TextType.LINK, url="https://youtube.com"),
                TextNode(text=". Cool right?!", text_type=TextType.TEXT)
            ],
            new_nodes
        )

    def test_multiple_nodes(self):
        node1 = TextNode(
            text="This is node one with a link: [link1 text](https://imgur.com).",
            text_type=TextType.TEXT
        )
        node2 = TextNode(
            text="This second node has a node called [link2 text](https://youtube.com).",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode(text="This is node one with a link: ", text_type=TextType.TEXT),
                TextNode(text="link1 text", text_type=TextType.LINK, url="https://imgur.com"),
                TextNode(text=".", text_type=TextType.TEXT),
                TextNode(text="This second node has a node called ", text_type=TextType.TEXT),
                TextNode(text="link2 text", text_type=TextType.LINK, url="https://youtube.com"),
                TextNode(text=".", text_type=TextType.TEXT) 
            ],
            new_nodes
        )

    def test_other_node_type(self):
        node1 = TextNode(
            text="This is a BOLD node",
            text_type=TextType.BOLD
        )
        node2 = TextNode(
            text="int main() { // ... }",
            text_type=TextType.CODE
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [node1, node2],
            new_nodes
        )

    def test_link_end(self):
        node = TextNode(
            "This is text with an [link](https://google.com)",
            TextType.TEXT,
       )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with an ", text_type=TextType.TEXT),
                TextNode(text="link", text_type=TextType.LINK, url="https://google.com"),
            ],
            new_nodes,
        )


    def test_link_start(self):
        node = TextNode(
            text="[link](https://chatgpt.com) this is a node with an link as a start",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="link", text_type=TextType.LINK, url="https://chatgpt.com"),
                TextNode(text=" this is a node with an link as a start", text_type=TextType.TEXT)
            ],
            new_nodes
        )

    def test_link_only(self):
        node = TextNode(
            text="[link](https://imgur.com)",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="link", text_type=TextType.LINK, url="https://imgur.com")
            ],
            new_nodes
        )

    def test_no_links(self):
        node = TextNode(
            text="AH EXODIA?! ITS NOT POSSIBLE",
            text_type=TextType.TEXT
        ) 
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes
        )
        
    def test_adjacent_links(self):
        node = TextNode(
            text="[a](https://a.com)[b](https://b.com)",
            text_type=TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="a", text_type=TextType.LINK, url="https://a.com"),
                TextNode(text="b", text_type=TextType.LINK, url="https://b.com"),
            ],
            new_nodes,
        )
    
class TestTextToNodes(unittest.TestCase):
    def test_full_example_all_types(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, actual)

    def test_plain_text_only(self):
        text = "just normal text"
        expected = [TextNode("just normal text", TextType.TEXT)]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_multiple_bold_and_italic(self):
        text = "**a** _b_ **c** _d_"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("a", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("b", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("c", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("d", TextType.ITALIC),
        ]
        self.assertListEqual(expected, actual)

    def test_multiple_links_and_images(self):
        text = (
            "Pics: ![p1](https://a.com/1.png) and ![p2](https://b.com/2.png). "
            "Links: [a](https://a.com) and [b](https://b.com)"
        )
        actual = text_to_textnodes(text)
        expected = [
            TextNode("Pics: ", TextType.TEXT),
            TextNode("p1", TextType.IMAGE, "https://a.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("p2", TextType.IMAGE, "https://b.com/2.png"),
            TextNode(". Links: ", TextType.TEXT),
            TextNode("a", TextType.LINK, "https://a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.LINK, "https://b.com"),
        ]
        self.assertListEqual(expected, actual)

    def test_unmatched_delimiter_raises(self):
        # If your delimiter splitters raise on invalid markdown,
        # text_to_textnodes should also raise.
        text = "this is **broken bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)