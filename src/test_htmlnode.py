import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", None, {"class": "greeting"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, World!, children=None, props={'class': 'greeting'})")
    def test_repr_with_children(self):
        node = HTMLNode("div", "Hello, World!", [HTMLNode("span", "Child")], {"class": "greeting"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, World!, children=[HTMLNode(tag=span, value=Child, children=None, props=None)], props={'class': 'greeting'})")
    def test_repr_without_props(self):
        node = HTMLNode("div", "Hello, World!", None, None)
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, World!, children=None, props=None)")
    
    
    if __name__ == "__main__":
        unittest.main()