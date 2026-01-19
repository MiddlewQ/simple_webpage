import regex as re


def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return  re.findall(link_pattern, text)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            final_blocks.append(block)
    return final_blocks