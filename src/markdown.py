from enum import Enum
from htmlnode import *
from splitdelimit import *
import re

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered list"
    ORDERED_LIST = "Ordered list"

def block_to_block_type(text):
    heading_matches = re.findall(r"(^\#{1,6} )", text)
    code_matches = re.findall(r"^(`{3})(?!`)([\s\S]*?)(?<!`)(`{3})$", text)
    quote_matches = re.findall(r"^\>", text, flags=re.MULTILINE)
    unordered_list_matches = re.findall(r"^- ", text, flags=re.MULTILINE)
    ordered_list_matches = [int(m.group(1)) for m in re.finditer(r'(?m)^(\d+)\.\s+', text)]
    text_lines = text.splitlines()
    
    if len(heading_matches) > 0:
        return BlockType.HEADING
    if len(code_matches) > 0:
        return BlockType.CODE
    if len(quote_matches) > 0:
        return BlockType.QUOTE
    if len(unordered_list_matches) > 0:
        if len(unordered_list_matches) == len(text_lines):
            return BlockType.UNORDERED_LIST

    if ordered_list_matches == list(range(1, len(text_lines)+1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(block):
    block_type = block_to_block_type(block)
    ### paragraph is simply wrapped in p
    if block_type == BlockType.PARAGRAPH:
        text_nodes = text_to_textnodes(block)
        return ParentNode(tag="p", children=[text_node_to_html(node) for node in text_nodes])
    ### quote blocks get split, the first > is removed, then rejoined to wrap in blockquote
    if block_type == BlockType.QUOTE:
        text_lines = [line[1:].strip() for line in block.splitlines()]
        children = [
            ParentNode(tag="p", children=[text_node_to_html(node) for node in text_to_textnodes(line)])
            for line in text_lines if line
        ]
        return ParentNode(tag="blockquote", children=children)
    ### headings determine the number of the heading, then adds h+that number to wrap it
    if block_type == BlockType.HEADING:
        heading_number = len(block.split()[0])
        heading_text = block[heading_number + 1:]
        children = [text_node_to_html(node) for node in text_to_textnodes(heading_text)]
        return ParentNode(tag=f"h{heading_number}", children=children)
    ### code block handling
    if block_type == BlockType.CODE:
        # Remove the first and last 3 backticks, but preserve internal newlines
        cleaned_text = block[3:-3]  # Do not strip newlines or process inline Markdown
        code_node = LeafNode(tag="code", value=cleaned_text)  # Treat content as raw text
        return ParentNode(tag="pre", children=[code_node])  # Wrap directly in <pre>
    ### unordered list handling
    if block_type == BlockType.UNORDERED_LIST:
        text_lines = block.splitlines()
        list_items = [
            ParentNode(tag="li", children=[text_node_to_html(node) for node in text_to_textnodes(line[2:].strip())])
            for line in text_lines
        ]
        return ParentNode(tag="ul", children=list_items)

    if block_type == BlockType.ORDERED_LIST:
        text_lines = block.splitlines()
        list_items = [
            ParentNode(tag="li", children=[text_node_to_html(node) for node in text_to_textnodes(line.split(". ", 1)[1].strip())])
            for line in text_lines
        ]
        return ParentNode(tag="ol", children=list_items)


def markdown_to_html_document(text):
    blocks = markdown_to_blocks(text)
    children = [markdown_to_html_node(block) for block in blocks]
    return ParentNode(tag="div", children = children)