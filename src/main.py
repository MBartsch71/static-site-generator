from textnode import TextNode, TextType
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType
import os
import shutil
import sys


def clean_public_dir():
    """Remove all files and subdirectories in the public directory."""
    public_dir = os.path.join(os.path.dirname(__file__), '../public')
    if os.path.exists(public_dir):
        # Remove the entire directory and its contents
        shutil.rmtree(public_dir)
    # Recreate empty public directory
    os.makedirs(public_dir)

def generate_pages_recursive(content_dir, template_path, public_dir, base_path="/"):
    """
    Recursively generate HTML pages from markdown files in content directory.
    
    Args:
        content_dir: Path to the content directory containing markdown files
        template_path: Path to the template HTML file
        public_dir: Path to the public directory where generated files will be placed
    """
    # Get absolute paths
    content_dir = os.path.abspath(content_dir)
    public_dir = os.path.abspath(public_dir)
    
    for root, dirs, files in os.walk(content_dir):
        # Calculate the relative path from content directory
        rel_path = os.path.relpath(root, content_dir)
        
        # Create corresponding directory in public
        if rel_path != '.':
            os.makedirs(os.path.join(public_dir, rel_path), exist_ok=True)
        
        # Process markdown files
        for file in files:
            if file.endswith('.md'):
                # Construct paths
                from_path = os.path.join(root, file)
                # Replace .md with .html and handle index.md specially
                if file == 'index.md':
                    dest_file = 'index.html'
                else:
                    dest_file = file[:-3] + '.html'  # Remove .md, add .html
                
                dest_path = os.path.join(public_dir, rel_path, dest_file)
                
                # Generate the page, passing base_path through
                generate_page(from_path=from_path, template_path=template_path, dest_path=dest_path, base_path=base_path)

def main():
    # Get base path from command line argument, default to '/'
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    # Ensure base_path starts and ends with /
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    if not base_path.endswith("/"):
        base_path = base_path + "/"

    clean_public_dir()
    copy_static_to_public()
    
    # Generate all pages recursively
    content_dir = os.path.join(os.path.dirname(__file__), '../content')
    template_path = os.path.join(os.path.dirname(__file__), '../template.html')
    public_dir = os.path.join(os.path.dirname(__file__), '../docs')
    
    generate_pages_recursive(content_dir, template_path, public_dir, base_path)

def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown) 

    with open(template_path, 'r') as f:
        template = f.read()

    full_html = template.replace("{{ Content }}", html_node )
    full_html = full_html.replace("{{ Title }}", title)
    # Optional base path replacement for templates that include {{ Base }}
    full_html = full_html.replace("href=/\"", "href=\"base_path")
    full_html = full_html.replace("src=/\"", "src=\"base_path")

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, 'w') as f:
        f.write(full_html)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if BlockType.HEADING in [block_to_block_type(block) for block in blocks]:   
        for block in blocks:
            if block_to_block_type(block) == BlockType.HEADING:
                lines = block.split("\n")
                if not lines[0].startswith("# "):
                    raise Exception("No first level heading found in markdown.")
                return lines[0][2:].strip()
    raise Exception("No heading found in markdown.") 



def copy_static_to_public():
    static_dir = os.path.join(os.path.dirname(__file__), '../static')
    print(f"Static Dir: {static_dir}")
    public_dir = os.path.join(os.path.dirname(__file__), '../docs')
    print(f"Public Dir: {public_dir}")

    if not os.path.exists(public_dir):
        os.makedirs(public_dir)

    for item in os.listdir(static_dir):
        s = os.path.join(static_dir, item)
        d = os.path.join(public_dir, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            for sub_item in os.listdir(s):
                sub_s = os.path.join(s, sub_item)
                sub_d = os.path.join(d, sub_item)
                if os.path.isfile(sub_s):
                    with open(sub_s, 'rb') as fsrc:
                        with open(sub_d, 'wb') as fdst:
                            fdst.write(fsrc.read())
        else:
            with open(s, 'rb') as fsrc:
                with open(d, 'wb') as fdst:
                    fdst.write(fsrc.read())




if __name__ == "__main__":
    main()