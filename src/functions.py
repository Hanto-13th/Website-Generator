from textnode import TextType, TextNode
from htmlnode import LeafNode,ParentNode
from blocknode import BlockType
import os
import shutil
import re

"""Here all the functions to transform markdown into HTML (TextNode into Leaf Node, markdown block into Parent Node..),
 copy files from 'content' and 'static' dir into the 'docs' (final directory) and generate the page """

def text_node_to_html_node(text_node):
    #Convert each type of TextNode into LeafNode with correspondants value
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
    """Function to split a TextNode into many textnode using a delimiter to split the basic text from special like Bold (**) or Italic (_)"""
    new_nodes = []
    for node in old_nodes:
        #if node is not a text, add directly in the list of split nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)            
        else:
            #else split the node depending on delimiter and check if the length of text split is even or odd to see if the syntax is correct
            text_split = node.text.split(delimiter)
            if len(text_split) > 1 and len(text_split) % 2 == 0:
                raise Exception("error: Invalid Markdown Syntax")
            #for each part, add into the list the basic text and the special text splitted
            for i,part in enumerate(text_split):
                if not part:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part,TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part,text_type))
                
    return new_nodes

def extract_markdown_images(text):
    #function to find images tag and image link into a text using regex
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    #function to find link tag and link into a text using regex
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches


def split_nodes_image(old_nodes):
    """Function to split a TextNode into many textnode to split the basic text from images using the func 'extract_markdown_images'"""
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
    """Function to split a TextNode into many textnode to split the basic text from links using the func 'extract_markdown_links' """
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
    """Function which combine all previous functions to split all text nodes depending of type and delimiter"""
    node = TextNode(text,TextType.TEXT,)
    node = split_nodes_delimiter([node],"**",TextType.BOLD)
    node = split_nodes_delimiter(node,"_",TextType.ITALIC)
    node = split_nodes_delimiter(node,"`",TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node


def markdown_to_blocks(markdown):
    """Functions to split the markdown text structure into blocks which contains ParentNode.
    
    Markdown Text >>> Split in Blocks >>> Each blocks convert in type (paragraph, header...) >>> convert in ParentNode to contains other Node"""
    split_blocks = []
    markdown = markdown.split("\n\n")
    for block in markdown:
        if block == "":
            continue
        #delete the whitetrails and spaces in the blocks
        block = block.strip()
        split_blocks.append(block)
    
    return split_blocks



def block_to_block_type(block):
    """Detect each type of block:
    start with '#' >>> HEADING,
    start and end with '```' >>> CODE,
    each line starts with '>' >>> QUOTE,
    each line starts with '- ' >>> UNORDERED LIST,
    each line starts with a incrementing number >>> ORDERED LIST"""

    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    """Functions to split all blocks in the markdown text 'markdown_to_blocks' and convert depending of the type in corresponding ParentNode 'block_to_html_node',
    after compact all the children (all converted blocks) into a <div> Parent Node"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

"""The next functions are to convert in corresponding ParentNode each block depending on his type, one function for one type"""
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    

def copy_files_recursive(source_dir_path, dest_dir_path):
    """This function copy all static files (css, images) into the destination directory"""

    #delete the destination dir to clean up
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    #for each filename, copy the struct of source path into the dest path
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            #copy the src directory, not only the file
            shutil.copy(from_path, dest_path)
        else:
            #move forward in the directory tree each iteration
            copy_files_recursive(from_path, dest_path)

def extract_title(markdown):
    """extract the title from the markdown"""

    markdown_header = markdown.split("\n")
    if markdown_header[0].startswith("#"):
        title = markdown_header[0].strip("# ")
        return title
    raise Exception("Error: There is no title in the markdown")

"""This functions are here to generate all pages structure and convert .md into .html, from the src path into the dest path using the models 'template.html',
replace the title and content from the template with the title 'extract_title' func and content 'markdown_to_html_node', add the basepath to set the URL when
deploy the website with Github
"""
def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    #open the markdown file and template to read their contains
    markdown_file = open(from_path,"r")
    markdown_file_text = markdown_file.read()
    template_file = open(template_path,"r")
    template_file_text = template_file.read()

    #convert the markdown into html
    html_node = markdown_to_html_node(markdown_file_text)
    html_string = html_node.to_html()

    #extract the title and replace the template content and title with the markdown contain
    title = extract_title(markdown_file_text)
    template_file_text = template_file_text.replace("{{ Title }}",title)
    template_file_text = template_file_text.replace("{{ Content }}",html_string)

    #set the basepath for each source for the links and images
    template_file_text = template_file_text.replace('href="/', 'href="' + basepath)
    template_file_text = template_file_text.replace('src="/', 'src="' + basepath)

    #with the same structure, add the new files created in the destination directory
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path,exist_ok=True)
    new_file = open(dest_path,"w")
    new_file.write(template_file_text)
    
    markdown_file.close()
    template_file.close()
    new_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    #to add more one page in the website
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path) and from_path.endswith(".md"):
            html_dest = os.path.join(dest_dir_path, "index.html")
            generate_page(from_path, template_path, html_dest,basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, filename)
            #move forward in the directory tree each iteration
            generate_pages_recursive(from_path, template_path, new_dest_dir,basepath)


    
    







