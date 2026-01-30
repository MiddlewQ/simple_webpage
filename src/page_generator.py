import os

from .markdown_to_html_node import markdown_to_html_node

def extract_title(markdown):
    first_block = markdown.strip().split("\n\n")[0]
    if not first_block.startswith("# "):
        raise ValueError("Missing title")
    return first_block[2:]


def generate_page(source_path, template_path, destination_path, basepath):
    print(f"Generating: {source_path:40} -> {destination_path}")

    if not os.path.isfile(source_path):
        print("No source")
        return

    if not os.path.isfile(template_path):
        print("No template")
        return 

    with open(source_path, encoding="utf-8") as f_source:
        source_content = f_source.read()

    with open(template_path, encoding="utf-8") as f_template:
        template_content = f_template.read() 
    
    html = markdown_to_html_node(source_content).to_html()
    title = extract_title(source_content)

    new_content = template_content.replace("{{ Title }}", title)
    new_content = new_content.replace("{{ Content }}", html)
    new_content = new_content.replace('href="/', f'href="{basepath}')
    new_content = new_content.replace('src="/', f'src="{basepath}')

    destination_dir = os.path.dirname(destination_path)

    if destination_dir:
        os.makedirs(destination_dir, exist_ok=True)    

    with open(destination_path, "w", encoding="utf-8") as f_destination:
        f_destination.write(new_content)