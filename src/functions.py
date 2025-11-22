from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Type used is unknown")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None,text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b",text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i",text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code",text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a",text_node.text,{"href": f"{text_node.url}"})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img","",{"src": f"{text_node.url}","alt": f"{text_node.text}"})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)            
        else:
            text_split = node.text.split(delimiter)
            if len(text_split) > 1 and len(text_split) % 2 == 0:
                raise Exception("error: Invalid Markdown Syntax")
            for i,part in enumerate(text_split):
                if not part:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part,TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part,text_type))
                
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text,TextType.TEXT,)
    node = split_nodes_delimiter([node],"**",TextType.BOLD)
    node = split_nodes_delimiter(node,"_",TextType.ITALIC)
    node = split_nodes_delimiter(node,"`",TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node


text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

text_to_textnodes(text)






