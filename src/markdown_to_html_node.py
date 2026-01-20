from .markdown_to_blocks import markdown_to_blocks
from .blocks_to_html_node import block_to_html_node
from .parentnode import ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_parent_node = ParentNode("div", [])
    for block in blocks:
        html_node = block_to_html_node(block) 
        html_parent_node.children.append(html_node)
    return html_parent_node
