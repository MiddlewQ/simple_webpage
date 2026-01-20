from src.markdown_to_html_node import block_to_html_quote, markdown_to_blocks
from .textnode import TextNode

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

