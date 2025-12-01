"""Here all HTMLNode class and instances, HTMLNode is the parent class and ParentNode is a child node which can
contains others HTMLNode, LeafNode is the last child which contains no Node"""

class HTMLNode():
    """A HTMLNode is composed with a tag (a = <a>, p = <p> ...) which structures the html,
    a value,the text contained into the Node,
    the childrens, the other nodes could be contain into this node,
    and the props are the property like a reference into a link (formated in a python dictionnary)
    """
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    #method to convert props dictionnary into a HTML format (e.g: {"href": "https://www.google.com"} >> href="https://www.google.com")
    def props_to_html(self):
        if not self.props:
            return ""
        parts = [f' {k}="{v}"' for k, v in self.props.items()]
        return "".join(parts)
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag},value:{self.value},children:{self.children},props:{self.props})"

class LeafNode(HTMLNode):
    """A LeafNode is composed with a tag (a = <a>, p = <p> ...) which structures the html,
    a value,the text contained into the Node,
    and the props are the property like a reference into a link (formated in a python dictionnary)
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    #method to transform the LeafNode into HTML format
    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """A ParentNode is composed with a tag (a = <a>, p = <p> ...) which structures the html,
    the childrens, the other nodes could be contain into this node,
    and the props are the property like a reference into a link (formated in a python dictionnary)
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    #method to convert ParentNode into HTML format with all childrens added in his body
    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        
        all_childs = ""
        for child in self.children:
            all_childs += child.to_html()

        return f"<{self.tag}>{all_childs}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
