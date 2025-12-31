import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com"')
    
    
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://x.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://x.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()