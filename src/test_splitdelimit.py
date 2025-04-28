import unittest

from htmlnode import *
from textnode import *
from splitdelimit import *
import re


class TestSplitNodesDelimited(unittest.TestCase):
    def assertNodeListsEqual(self, got, expected):
        self.assertEqual(
            len(got), len(expected),
            f"List lengths differ: got {len(got)}, expected {len(expected)}"
        )
        for idx, (g, e) in enumerate(zip(got, expected)):
            self.assertIsInstance(
                g, TextNode,
                f"Element {idx} is not a TextNode (got {type(g)})"
            )
            self.assertEqual(
                g.text, e.text,
                f"Text mismatch at idx {idx}: got {g.text!r}, expected {e.text!r}"
            )
            self.assertEqual(
                g.text_type, e.text_type,
                f"TextType mismatch at idx {idx}: got {g.text_type}, expected {e.text_type}"
            )

    def test_basic_split_bold(self):
        old = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        got = split_nodes_delimited(old, "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase",       TextType.BOLD),
            TextNode(" in the middle",      TextType.TEXT),
        ]
        self.assertNodeListsEqual(got, expected)

    def test_multiple_spans(self):
        old = [TextNode("a **b** c **d** e", TextType.TEXT)]
        got = split_nodes_delimited(old, "**", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b",  TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d",  TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertNodeListsEqual(got, expected)

    def test_skips_empty_slices(self):
        # leading and trailing delimiters produce empty parts that should be skipped
        old = [TextNode("**hi**", TextType.TEXT)]
        got = split_nodes_delimited(old, "**", TextType.ITALIC)
        expected = [ TextNode("hi", TextType.ITALIC) ]
        self.assertNodeListsEqual(got, expected)

    def test_non_text_nodes_pass_through(self):
        # any node with a non-TEXT type should be appended unchanged
        class FakeNode:
            def __init__(self):
                self.text_type = TextType.LINK
            def __repr__(self):
                return "<FakeLinkNode>"
        fake = FakeNode()
        old = [fake]
        got = split_nodes_delimited(old, "**", TextType.BOLD)
        # should be exactly the same object
        self.assertEqual(len(got), 1)
        self.assertIs(got[0], fake)

    def test_missing_closing_delimiter_raises(self):
        old = [TextNode("Unbalanced **bold", TextType.TEXT)]
        with self.assertRaises(Exception) as cm:
            split_nodes_delimited(old, "**", TextType.BOLD)
        self.assertIn("Missing closing delimiter", str(cm.exception))
    
    if __name__ == "__main__":
            unittest.main()