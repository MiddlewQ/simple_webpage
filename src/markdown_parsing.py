from htmlnode import HTMLNode
from textnode import TextNode, text_node_to_html_node, TextType
import regex as re


def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return  re.findall(link_pattern, text)


