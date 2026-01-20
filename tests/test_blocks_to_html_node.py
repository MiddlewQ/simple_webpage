import unittest
from src.markdown_to_blocks import markdown_to_blocks
from src.blocks_to_html_node import block_to_html_paragraph, block_to_html_heading, block_to_html_code, block_to_html_quote, block_to_html_ordered_list, block_to_html_unordered_list

class TestMarkdownHtmlParagraph(unittest.TestCase):


    def test_singleline(self):
        md = """This is a block with a bunch of text"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_paragraph(block)
        html = node.to_html()
        self.assertEqual("<p>This is a block with a bunch of text</p>", html)

    def test_multiline(self):
        md = """
This is a block with a bunch of text
Single block with multiple lines of code
Contains only text
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_paragraph(block)
        html = node.to_html()
        self.assertEqual("<p>This is a block with a bunch of text Single block with multiple lines of code Contains only text</p>", html)
    


    def test_markdown_parsing(self):
        md = """
This is **bolded** paragraph
this is some _italics_ and some `code`
wow, incredible 
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_paragraph(block)
        html = node.to_html()
        self.assertEqual("<p>This is <b>bolded</b> paragraph this is some <i>italics</i> and some <code>code</code> wow, incredible</p>", html)

    def test_multiline_with_inline(self):
        md = """
Hello **bold**
and _italics_
"""
        block = markdown_to_blocks(md)[0]
        html = block_to_html_paragraph(block).to_html()
        self.assertEqual("<p>Hello <b>bold</b> and <i>italics</i></p>", html)



# Markdown text is always on a single line, does not allow multiline heading
class TestMarkdownHtmlHeading(unittest.TestCase):

    def test_h1(self):
        block = "# This is a large heading!"
        node = block_to_html_heading(block) 
        html = node.to_html()
        self.assertEqual("<h1>This is a large heading!</h1>", html)


    def test_h2(self):
        block = "## This is a smaller heading"
        node = block_to_html_heading(block)
        html = node.to_html()
        self.assertEqual("<h2>This is a smaller heading</h2>", html)

    def test_h6(self):
        block = "###### This is the smallest heading!"
        node = block_to_html_heading(block)
        html = node.to_html()
        self.assertEqual("<h6>This is the smallest heading!</h6>", html)

    def test_markdown_parsing(self):
        block = "# **Bold** `and` _Italics_ in heading"
        node = block_to_html_heading(block)
        html = node.to_html()
        self.assertEqual("<h1><b>Bold</b> <code>and</code> <i>Italics</i> in heading</h1>", html)

class TestMarkdownHtmlCode(unittest.TestCase):
    def test_singleline(self):
        md = """```
Code block with a singleline
```
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_code(block)
        html = node.to_html()
        self.assertEqual("<pre><code>Code block with a singleline</code></pre>", html)

    def test_multiline(self):
        md = """```
a line test
b line
c line
```
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_code(block)
        html = node.to_html()
        self.assertEqual("<pre><code>a line test\nb line\nc line</code></pre>", html)

    def test_code_block_does_not_parse_inline_markdown(self):
        md = """```
a **bolded**
b _italics_
c `this should also be fine`
```
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_code(block)
        html = node.to_html()
        self.assertEqual("<pre><code>a **bolded**\nb _italics_\nc `this should also be fine`</code></pre>", html)

class TestMarkdownHtmlUnorderedList(unittest.TestCase):
    def test_singleline(self):
        block = "- single item list"
        node = block_to_html_unordered_list(block)
        html = node.to_html()
        self.assertEqual("<ul><li>single item list</li></ul>", html)

    def test_multiline(self):
        md = """
- a item
- b item
- c item
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_unordered_list(block)
        html = node.to_html()
        self.assertEqual("<ul><li>a item</li><li>b item</li><li>c item</li></ul>", html)

    def test_markdown_parsing(self):
        md = """
- _a_ **item**
- b `item`
- c item
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_unordered_list(block)
        html = node.to_html()
        self.assertEqual("<ul><li><i>a</i> <b>item</b></li><li>b <code>item</code></li><li>c item</li></ul>", html)

class TestMarkdownHtmlOrderedList(unittest.TestCase):
    def test_single_item(self):
        block  = "1. singleline list"
        node = block_to_html_ordered_list(block)
        html = node.to_html()
        self.assertEqual("<ol><li>singleline list</li></ol>", html)



    def test_multi_item(self):
        md = """
1. a line
2. b line
3. c line
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_ordered_list(block)
        html = node.to_html()
        self.assertEqual("<ol><li>a line</li><li>b line</li><li>c line</li></ol>", html)

    def test_markdown_parsing(self):
        md = """
1. `a line`
2. **b** line
3. _c line_
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_ordered_list(block)
        html = node.to_html()
        self.assertEqual("<ol><li><code>a line</code></li><li><b>b</b> line</li><li><i>c line</i></li></ol>", html)


class TestMarkdownHtmlQuote(unittest.TestCase):
    def test_singleline(self):
        block = "> Greentext"
        node = block_to_html_quote(block)
        html = node.to_html()
        self.assertEqual("<blockquote>Greentext</blockquote>", html)

    def test_multiline(self):
        md = """
> a line
> b line
> c line
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_quote(block)
        html = node.to_html()
        self.assertEqual("<blockquote>a line b line c line</blockquote>", html)

    def test_markdown_parsing(self):
        md = """
> `a` line
> **b l**ine
> _c lin_e
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_quote(block)
        html = node.to_html()
        self.assertEqual("<blockquote><code>a</code> line <b>b l</b>ine <i>c lin</i>e</blockquote>", html)

    def test_adjacent_inline(self):
        block = "> **a**_b_"
        html = block_to_html_quote(block).to_html()
        self.assertEqual("<blockquote><b>a</b><i>b</i></blockquote>", html)

