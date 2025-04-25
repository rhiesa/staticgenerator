import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode(("This is a butt node"), TextType.LINK)
        self.assertNotEqual(node, node2)
        
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Sad)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_eq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, Bold, None)")
        
    def test_repr_with_url(self):   
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, Link, http://example.com)")



if __name__ == "__main__":
    unittest.main()