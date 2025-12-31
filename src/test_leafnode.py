import unittest

from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode(tag="a", value="This is a test text with props", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">This is a test text with props</a>')
    
    
    def test_leaf_no_tag_raw_text(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

        
    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()