import unittest

from markdown import *
from htmlnode import *
from splitdelimit import *
from textnode import *


class TestHTMLNode(unittest.TestCase):

    # Test for headings
    def test_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

        md = "### Heading 3"
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>Heading 3</h3></div>")

    # Test for paragraphs
    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    # Test for blockquotes
    def test_blockquote(self):
        md = "> This is a blockquote."
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote><p>This is a blockquote.</p></blockquote></div>")

    # Test for inline formatting
    def test_inline_formatting(self):
        md = "This is **bold**, _italic_, and `code`."
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bold</b>, <i>italic</i>, and <code>code</code>.</p></div>")

    # Test for code blocks
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_document(md)
        html = node.to_html()
        print(html)
        print("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
    
    # Test for empty input
    def test_empty_input(self):
        md = ""
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    # Test for inline links
    def test_inline_links(self):
        md = "This is a [link](https://example.com)."
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <a href=\"https://example.com\">link</a>.</p></div>")

    # Test for inline images
    def test_inline_images(self):
        md = "This is an ![image](https://example.com/image.png)."
        node = markdown_to_html_document(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is an <img src=\"https://example.com/image.png\" alt=\"image\" />.</p></div>")
