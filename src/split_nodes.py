from textnode import TextNode, TextType

def split_nodes_image(old_nodes):
    pass

def split_nodes_links(old_nodes):
    pass

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
            raise ValueError("delimiter not found")
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