from src.markdown_extract import markdown_to_blocks
from src.markdown_html import block_to_html_quote
from .textnode import TextNode
from .text_to_nodes import text_to_textnodes

def main():
        md = """
> a line
> b line
> c line
"""
        block = markdown_to_blocks(md)[0]
        node = block_to_html_quote(block)
        html = node.to_html()
        print(node)
        # self.assertEqual("<blockquote>a line\nb line\nc line</blockquote>", html)


if __name__ == "__main__":
    main()

