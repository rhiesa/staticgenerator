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
            
            
def extract_markdown_images(text):
    alt_text = re.findall(r"(?<=!\[).*?(?=\])", text)
    url = re.findall(r"(?<=\]\()(.+?)(?=\)(?:\s|$))", text)
    extracted_tuples = list(zip(alt_text, url))
    return extracted_tuples

def extract_markdown_links(text):
    anchor_text = re.findall(r"(?<=\[).*?(?=\])",text)
    url = re.findall(r"(?<=\]\().*?(?=\))",text)
    extracted_tuples = list(zip(anchor_text,url))
    return extracted_tuples