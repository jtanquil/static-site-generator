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
  
class LeafNode(HTMLNode):
  def __init__(self, tag = None, value = None, props = None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("All leaf nodes require a value")
    else:
      if self.tag is None:
        return self.value
      else:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
      
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"