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
        
    def test_extract_images(self):
        matches = extract_markdown_images(
             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        self.assertEqual(extract_markdown_images("no images here"), [])

    def test_single_image(self):
        text = "Here is an image ![alt text](http://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "http://example.com/img.png")]
        )

    def test_multiple_images(self):
        text = "![first](http://a.com/a.png) some text ![second](https://b.org/b.jpg)"
        expected = [
            ("first",  "http://a.com/a.png"),
            ("second", "https://b.org/b.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_parentheses_in_alt_and_url(self):
        text = "![Alt (with parens)](http://example.com/img_(1).png)"
        expected = [("Alt (with parens)", "http://example.com/img_(1).png")]
        self.assertEqual(extract_markdown_images(text), expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_no_links(self):
        self.assertEqual(extract_markdown_links("no links here"), [])

    def test_single_link(self):
        text = "Visit [Google](https://google.com) for more."
        self.assertEqual(
            extract_markdown_links(text),
            [("Google", "https://google.com")]
        )

    def test_multiple_links(self):
        text = "Links: [one](http://one) and [two](http://two)."
        expected = [("one", "http://one"), ("two", "http://two")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestCombined(unittest.TestCase):
    def test_images_and_links_together(self):
        text = "![img](http://img) and [lnk](http://lnk)"
        # images only
        self.assertEqual(extract_markdown_images(text), [("img", "http://img")])
        # links picks up both bracketed items
        self.assertEqual(
            extract_markdown_links(text),
            [("img", "http://img"), ("lnk", "http://lnk")]
        )
class TestExtractors(unittest.TestCase):
    def test_extract_images(self):
        self.assertEqual(
            extract_markdown_images("A![one](u1)B![two](u2)C"),
            [("one","u1"),("two","u2")]
        )

    def test_extract_links(self):
        self.assertEqual(
            extract_markdown_links("go [here](url) and [there](url2)"),
            [("here","url"),("there","url2")]
        )

class DummyNode:
    def __init__(self, text, text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

def node_to_tuple(n):
    return (n.text, n.text_type, getattr(n, "url", None))

def test_extract_markdown_images_multiple(self):
    self.assertEqual(
        extract_markdown_images("A![one](u1)B![two](u2)C"),
        [("one", "u1"), ("two", "u2")]
    )

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = [DummyNode("hello ![alt](http://x) world")]
        out = split_nodes_image(nodes)
        expected = [
            ("hello ", TextType.TEXT, None),
            ("alt",    TextType.IMAGE, "http://x"),
            (" world", TextType.TEXT, None),
        ]
        self.assertEqual([node_to_tuple(n) for n in out], expected)

    def test_multiple_images(self):
        nodes = [DummyNode("A![one](u1)B![two](u2)C")]
        out = split_nodes_image(nodes)
        expected = [
            ("A",   TextType.TEXT,  None),
            ("one", TextType.IMAGE, "u1"),
            ("B",   TextType.TEXT,  None),
            ("two", TextType.IMAGE, "u2"),
            ("C",   TextType.TEXT,  None),
        ]
        self.assertEqual([node_to_tuple(n) for n in out], expected)
        
    def test_parentheses_in_url_and_alt(self):
        txt = "![Look (here)](http://foo.com/x_(1).png)"

        out = split_nodes_image([DummyNode(txt)])
        expected = [
            ("Look (here)",    TextType.IMAGE, "http://foo.com/x_(1).png"),
        ]
        self.assertEqual([node_to_tuple(n) for n in out], expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_plain_text_passes_through(self):
        nodes = [DummyNode("no links!"), DummyNode("")]
        out = split_nodes_link(nodes)
        self.assertEqual([node_to_tuple(n) for n in out],
                         [("no links!", TextType.TEXT, None)])

    def test_single_link_splitting(self):
        nodes = [DummyNode("go to [site](https://ex) now")]
        out = split_nodes_link(nodes)
        expected = [
            ("go to ",   TextType.TEXT,  None),
            ("site",     TextType.LINK,  "https://ex"),
            (" now",     TextType.TEXT,  None),
        ]
        self.assertEqual([node_to_tuple(n) for n in out], expected)

    def test_multiple_links(self):
        txt = "[A](uA) then [B](uB) end"
        out = split_nodes_link([DummyNode(txt)])
        expected = [
            ("A",   TextType.LINK,  "uA"),
            (" then ", TextType.TEXT, None),
            ("B",   TextType.LINK,  "uB"),
            (" end", TextType.TEXT, None),
        ]
        self.assertEqual([node_to_tuple(n) for n in out], expected)
        
class TestSplitTexttoTextNodes(unittest.TestCase):
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
            
    def test_combined_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        got = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),

        ]
        self.assertNodeListsEqual(got, expected)
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here     
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here     \nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )
        
    if __name__ == "__main__":
            unittest.main()