from textnode import TextNode, TextType
from regexer import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text):
    text_to_investigate = TextNode(text, TextType.TEXT)
    new_nodes = [text_to_investigate]
    new_nodes = split_nodes_at_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    new_nodes = split_nodes_at_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_at_delimiter(new_nodes, "_", TextType.ITALIC) 

    return new_nodes
    
def split_nodes_at_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if isinstance(old_nodes, TextNode):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            new_nodes.append(node)
            continue
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes    

def split_nodes_links(old_nodes):
    new_nodes = []
    if isinstance(old_nodes, TextNode):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        
        current_index = 0
        for link_text, link_url in links:
            TextNode(link_text, TextType.LINK, link_url)
            link_start = node.text.find(f"[{link_text}]({link_url})", current_index)
            if link_start == -1:
                continue    
            if link_start > current_index:
                preceding_text = node.text[current_index:link_start]
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_index = link_start + len(f"[{link_text}]({link_url})")
        if current_index < len(node.text):
            remaining_text = node.text[current_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes
    
def split_nodes_images(old_nodes):
    new_nodes = []
    if isinstance(old_nodes, TextNode):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        
        current_index = 0
        for alt_text, img_url in images:
            img_start = node.text.find(f"![{alt_text}]({img_url})", current_index)
            if img_start == -1:
                continue    
            if img_start > current_index:
                preceding_text = node.text[current_index:img_start]
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))
            current_index = img_start + len(f"![{alt_text}]({img_url})")
        if current_index < len(node.text):
            remaining_text = node.text[current_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes    