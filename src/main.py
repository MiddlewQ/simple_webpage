import os, shutil, sys

from .markdown_to_html_node import markdown_to_html_node
from .page_generator import generate_page
def clean_directory(directory):
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)

    except OSError as e:
        print(f"Failed to delete {directory}: {e}", file=sys.stderr)
        sys.exit(1)

def generate_pages_recursively(source_directory, destination_directory, template_path, basepath):
    if not os.path.isdir(source_directory):
        print(f"Source directory {source_directory} not found")
        sys.exit(1)
    if not os.path.isdir(destination_directory):
        print(f"Destination directory {destination_directory} not found")
        sys.exit(1)
    
    for entity in os.listdir(source_directory):
        source_filepath = os.path.join(source_directory, entity)
        destination_filepath = os.path.join(destination_directory, entity)

        if os.path.isfile(source_filepath):
            if source_filepath.endswith(".md"):
                print(destination_filepath)
                destination_filepath = destination_filepath[:-2] + "html"
                generate_page(source_filepath, template_path, destination_filepath, basepath)
            else:
                shutil.copy(source_filepath, destination_filepath)
        
        elif os.path.isdir(source_filepath):
            os.mkdirs(destination_filepath)
            generate_pages_recursively(source_filepath, destination_filepath, template_path)


def main():

    static = "static"
    source = "content"
    destination = "docs"
    template = "template.html"
    basepath = sys.argv[1] if len(sys.argv) >= 2 else "/"



    clean_directory(destination)
    generate_pages_recursively(static, destination, template, basepath)
    generate_pages_recursively(source, destination, template, basepath)


if __name__ == "__main__":
    main()

