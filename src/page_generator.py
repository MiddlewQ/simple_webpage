

def extract_title(markdown):
    first_block = markdown.strip().split("\n\n")[0]
    if not first_block.startswith("# "):
        raise ValueError("Missing title")
    return first_block[2:]

