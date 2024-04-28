class HTMLNode():
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("to_html method not implemented for HTMLNode")
  
  def props_to_html(self):
    if self.props is None:
      return ""
    else:
      return "".join([f' {key}="{self.props[key]}"' for key in self.props.keys()])
  
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

  def __eq__(self, other):
    return (self.tag == other.tag 
      and self.value == other.value 
      and self.children == other.children 
      and self.props == other.props)
  
class LeafNode(HTMLNode):
  def __init__(self, tag = None, value = None, props = None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      if self.tag == "img":
        return f"<{self.tag}{self.props_to_html()}>"
      else:
        raise ValueError("All leaf nodes require a value")
    else:
      if self.tag is None:
        return self.value
      else:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
      
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"
  
class ParentNode(HTMLNode):
  def __init__(self, tag = None, children = None, props = None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("Parent nodes require a tag")
    elif self.children is None or len(self.children) == 0:
      raise ValueError("Parent nodes require at least one child")
    else:
      return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
  def __repr__(self):
    return f"ParentNode({self.tag}, children: {self.children}, props: {self.props})"