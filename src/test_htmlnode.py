import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType



class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "test123", None, {"href": "x"})
        node2 = HTMLNode("a", "test123", None, {"href": "x"})
        self.assertEqual(node, node2)
    
    def test_noteqTEXT(self):
        node = HTMLNode("<a>","test123","nochild","props1 props2")
        node2 = HTMLNode("<a>","test123","two childs","props1 props2 props3")
        self.assertNotEqual(node, node2)
    
    def test_noteqURL(self):
        node = HTMLNode("<a>","abcde","nochild","props1 props2")
        node2 = HTMLNode("<a>","test123","nochild","props1 props2")
        self.assertNotEqual(node, node2)
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren(self):
        node1 = LeafNode("b", "Bold text")
        node2 = LeafNode(None, "Normal text")
        node3 = LeafNode("i", "italic text")
        node4 = LeafNode(None, "Normal text")

        parent_node = ParentNode("div", [node1,node2,node3,node4])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>",
        )

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
 


if __name__ == "__main__":
    unittest.main()