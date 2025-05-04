from textnode import TextType,TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag == None:
            return self.value
        if self.tag == "img":
            props = self.props_to_html()
            return f"<{self.tag} {props} />"
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children == None:
            raise ValueError("ParentNode children cannot be None")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{children_html}</{self.tag}>"
    
def text_node_to_html(node):
    if node.text_type == TextType.TEXT:
        return LeafNode(value=node.text)
    elif node.text_type == TextType.BOLD:
        return LeafNode(tag = "b", value = node.text)
    elif node.text_type == TextType.ITALIC:
        return LeafNode(tag = "i", value = node.text)
    elif node.text_type == TextType.CODE:
        return LeafNode(tag = "code", value = node.text)
    elif node.text_type == TextType.LINK:
        return LeafNode(tag = "a", value = node.text, props = {"href": node.url})
    elif node.text_type == TextType.IMAGE:
        return LeafNode(tag = "img", value = "", props={"src": node.url, "alt": node.text})
    else:
        raise ValueError(f"Unknown text type: {node.text_type}")