from .textnode import TextNode
from .text_to_nodes import text_to_textnodes

def main():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(text_to_textnodes(md))
if __name__ == "__main__":
    main()

