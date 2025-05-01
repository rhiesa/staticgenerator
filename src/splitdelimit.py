from htmlnode import *
from textnode import *
import re

def split_nodes_delimited(old_nodes, delimiter, text_type):
    new_nodes = []
    temptext = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            temptext = node.text.split(delimiter)
            if len(temptext) % 2 == 0:
                raise Exception ("Missing closing delimiter")
            
            else:
                for alt, item in enumerate(temptext):
                    if not item:
                        continue
                    kind = TextType.TEXT if (alt %2 == 0) else text_type
                    new_nodes.append(TextNode(item,kind))
    return new_nodes
            
            
_IMAGE_RE = re.compile(
    r'!\[([^\]]+)\]\('          # ![ alt-text ](
    r'((?:[^()]+|\([^()]*\))*)' # group of (non-parens OR a parenthesized subchunk), repeated
    r'\)'
)

_LINK_RE = re.compile(
    r'\[([^\]]+)\]\('
    r'((?:[^()]+|\([^()]*\))*)'
    r'\)'
)

def extract_markdown_images(text):
    # returns: List[Tuple[str alt_text, str url]]
    return _IMAGE_RE.findall(text)

def extract_markdown_links(text):
    # returns: List[Tuple[str anchor_text, str url]]
    return _LINK_RE.findall(text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text or ""
        images = extract_markdown_images(text)

        # if there are no images (or empty text), just pass the node along
        if not images:
            if text:  
                new_nodes.append(node)
            continue

        # otherwise peel off each image in sequence
        remainder = text
        for alt, url in images:
            if not url:
                continue
            marker = f"![{alt}]({url})"
            before, sep, after = remainder.partition(marker)

            # text before the image
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            # the image itself
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            # continue on with what’s left
            remainder = after

        # any trailing text after the last image
        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text != "" and len(extract_markdown_links(node.text)) == 0:
            new_nodes.append(node)
        else:
            image_tuple = extract_markdown_links(node.text)
            remainder = node.text
            for alt_text, url in image_tuple:
                if not url:
                    continue
                marker = f"[{alt_text}]({url})"
                before,sep,after = remainder.partition(marker)
                if before:
                    new_nodes.append(TextNode(before,TextType.TEXT))
                new_nodes.append(TextNode(alt_text,TextType.LINK, url))
                remainder = after
            if remainder:
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes