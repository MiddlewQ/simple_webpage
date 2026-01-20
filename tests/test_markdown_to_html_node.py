import unittest

from src.markdown_to_html_node import markdown_to_html_node

class TestMarkdownHtmlConversion(unittest.TestCase):

    def test_single_block(self):
        md = """
This is a single block that contains
a basic paragraph with some **bold** and some `code`
as well as some _italics_ yeah
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual("<div><p>This is a single block that contains a basic paragraph with some <b>bold</b> and some <code>code</code> as well as some <i>italics</i> yeah</p></div>", html)


    def test_multiple_block_types(self):
        md = """
# Simple paragraph with a bunch of different types

This is a paragraph
with
a few lines

```
#include <stdio.h>
int main() {
    printf("Hello World!\n");
}
```

**Bold block**

Shared block **bold** _italics_ and `code`

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual('<div><h1>Simple paragraph with a bunch of different types</h1><p>This is a paragraph with a few lines</p><pre><code>#include <stdio.h>\nint main() {\n    printf("Hello World!\n");\n}</code></pre><p><b>Bold block</b></p><p>Shared block <b>bold</b> <i>italics</i> and <code>code</code></p></div>', html)

    def test_empty(self):
        html = markdown_to_html_node("").to_html()
        self.assertEqual("<div></div>", html)

