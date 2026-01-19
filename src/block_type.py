import regex as re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block):
    # Headings
    if re.match(r"^#{1,6} .+?", block):
        return BlockType.HEADING
    
    # Code Blocks
    elif re.match(r"^```\n.*?```$", block, re.DOTALL):
        return BlockType.CODE
        
    # Quotes
    elif re.match(r"^> ", block):
        lines = block.split('\n')
        is_quote = True
        for line in lines:
            if not line.startswith("> "):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    # Unordered Lists
    elif block.startswith("- "):
        lines = block.split('\n')
        is_list = True
        for line in lines:
            if not line.startswith("- "):
                is_list = False
                break
        if is_list:
            return BlockType.UNORDERED_LIST

    # Ordered Lists
    elif block.startswith("1. "):
        lines = block.split('\n')
        is_list = True
        for i in range(1, len(lines)):
            line = lines[i]
            if not line.startswith(f"{i+1}."):
                is_list = False
                break
        if is_list:
            return BlockType.ORDERED_LIST

    # Paragraphs (default)
    return BlockType.PARAGRAPH