import regex as re

from .textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        # Read node text, if it find a specific symbol we want to split it, 
        # create a new node and add it to text_nodes
        new_texts = node.text.split(delimiter)
        if len(new_texts) == 1:
            nodes.append(node)
            continue
        if len(new_texts) % 2 == 0:
            raise ValueError("unmatched delimiter")

        new_nodes = []
        even = False
        for text in new_texts:
            if text == "":
                even = not even
                continue
            # Even -> text_type=parameter
            # Odd  -> text_type=TextType.TEXT
            new_nodes.append(TextNode(text=text, text_type=text_type if even else TextType.TEXT))
            # Switch even to false
            even = not even
        nodes.extend(new_nodes)

    return nodes

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        curr_text = node.text
        images = extract_markdown_images(curr_text)

        for image_alt, image_link in images:
            markdown = f"![{image_alt}]({image_link})"
            before, after = curr_text.split(markdown, 1)
            if before:
                nodes.append(TextNode(text=before, text_type=TextType.TEXT))
            nodes.append(TextNode(text=image_alt, text_type=TextType.IMAGE, url=image_link))
            curr_text = after
        if curr_text:
            nodes.append(TextNode(text=curr_text, text_type=TextType.TEXT))
    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        curr_text = node.text
        images = extract_markdown_links(curr_text)

        for image_alt, image_link in images:
            markdown = f"[{image_alt}]({image_link})"
            before, after = curr_text.split(markdown, 1)
            if before:
                nodes.append(TextNode(text=before, text_type=TextType.TEXT))
            nodes.append(TextNode(text=image_alt, text_type=TextType.LINK, url=image_link))
            curr_text = after
        if curr_text:
            nodes.append(TextNode(text=curr_text, text_type=TextType.TEXT))
    return nodes

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return  re.findall(link_pattern, text)


