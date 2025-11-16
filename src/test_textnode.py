import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteqTEXT(self):
        node = TextNode("This is a image node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_noteqURL(self):
        node = TextNode("This is a text node", TextType.BOLD,"testurl1.com")
        node2 = TextNode("This is a text node", TextType.BOLD,"testurl2.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()