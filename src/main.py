import os, shutil, sys

from src.markdown_to_html_node import markdown_to_html_node

def clean_directory(directory):
    if not os.path.isdir(directory):
        print(f"Directory {directory} not found", file=sys.stderr)
        sys.exit(1)
    try:
        shutil.rmtree(directory)
    except OSError as e:
        print(f"Failed to delete {directory}: {e}", file=sys.stderr)
        sys.exit(1)

def copy_directory(source_directory, destination_directory):
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
            shutil.copy(source_filepath, destination_filepath)
        elif os.path.isdir(source_filepath):
            os.mkdir(destination_filepath)
            copy_directory(source_filepath, destination_filepath)


def main():
    source = "static"
    destination = "public"
    clean_directory(destination)
    os.mkdir(destination)
    copy_directory(source, destination)
   
    pass


if __name__ == "__main__":
    main()

