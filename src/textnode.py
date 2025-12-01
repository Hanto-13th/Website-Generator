from enum import Enum

"""Here the differents type of TextNode we can have to convert after into LeafNode"""

class TextType(Enum):
    TEXT = "text"
    IMAGE = "img"
    LINK = "link"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"

"""The class for each TextNode from markdown file, with text, type and URL if it's an image or a link"""
class TextNode():
    def __init__(self,text,type,url=None):
        self.text = text
        self.text_type = type
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"

    