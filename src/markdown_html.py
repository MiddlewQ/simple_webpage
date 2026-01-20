import regex as re

# from .htmlnode import HTMLNode
from .textnode import text_node_to_html_node
from .parentnode import ParentNode
from .markdown_extract import markdown_to_blocks
from .block_type import block_to_block_type, BlockType
from .text_to_nodes import TextNode, TextType, text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_block = block_to_html_paragraph(block) 
            case BlockType.HEADING:
                html_block = block_to_html_heading(block)
            case BlockType.CODE:
                html_block = block_to_html_code(block)
            case BlockType.QUOTE:
                html_block = block_to_html_quote(block)
            case BlockType.UNORDERED_LIST:
                html_block = block_to_html_unordered_list(block)
            case BlockType.ORDERED_LIST:
                html_block = block_to_html_ordered_list(block)
        html_node.children.append(html_block)

    return html_node


def block_to_html_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    textnodes = text_to_textnodes(paragraph)
    html_nodes = [text_node_to_html_node(node) for node in textnodes]
    return ParentNode("p", children=html_nodes) 

def block_to_html_heading(block):
    level = len(block) - len(block.lstrip('#'))
    content = block.lstrip('#')[1:]
    tag = f"h{level}"
    textnodes = text_to_textnodes(content)
    html_items = [text_node_to_html_node(node) for node in textnodes]
    return ParentNode(tag, children=html_items)

def block_to_html_unordered_list(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        content = line[2:]
        textnodes = text_to_textnodes(content)
        children = [text_node_to_html_node(node) for node in textnodes]
        html_items.append(ParentNode(tag="li", children=children))
    return ParentNode("ul", children=html_items)

def block_to_html_ordered_list(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        content = line[3:]
        textnodes = text_to_textnodes(content)
        children = [text_node_to_html_node(node) for node in textnodes]
        html_items.append(ParentNode(tag="li", children=children))

    return ParentNode("ol", children=html_items)

def block_to_html_quote(block):
    lines = [line[2:] for line in block.split("\n")]
    content = " ".join(lines)
    textnodes = text_to_textnodes(content)
    html_items = [text_node_to_html_node(node) for node in textnodes]
    return ParentNode("blockquote", children=html_items)


def block_to_html_code(block):
    lines = block.split("\n")
    content = lines[1:-1]
    text = "\n".join(content)
    code_node = text_node_to_html_node(TextNode(text=text, text_type=TextType.TEXT))
    return ParentNode("pre", children=[ParentNode("code", children=[code_node])])