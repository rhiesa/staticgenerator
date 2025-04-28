import unittest

from htmlnode import *
from textnode import *


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
    def test_leaf_node_repr_without_value(self):
        node = LeafNode("p", None, {"class": "greeting"})
        with self.assertRaises(ValueError):
            node.to_html()
            
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
    
    def test_parentnode_no_tag(self):
        # Test ParentNode with no tag
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", "child")]).to_html()
        self.assertEqual(str(context.exception), "ParentNode tag cannot be None")

    def test_parentnode_no_children(self):
        # Test ParentNode with no children
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()
        self.assertEqual(str(context.exception), "ParentNode children cannot be None")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        

    
    
    if __name__ == "__main__":
        unittest.main()