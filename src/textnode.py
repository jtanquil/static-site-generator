import re

from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
text_type_delimiters = {
  text_type_text: "",
  text_type_bold: "**",
  text_type_italic: "*",
  text_type_code: "`"
}
text_types = {text_type_delimiters[key]:key for key in text_type_delimiters}

class TextNode():
  def __init__(self, text, text_type, url = None):
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, other):
    return self.text == other.text and self.text_type == other.text_type and self.url == other.url
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
  
def text_node_to_html_node(text_node):
  if text_node.text_type == text_type_text:
    return LeafNode(None, text_node.text)
  elif text_node.text_type == text_type_bold:
    return LeafNode("b", text_node.text)
  elif text_node.text_type == text_type_italic:
    return LeafNode("i", text_node.text)
  elif text_node.text_type == text_type_code:
    return LeafNode("code", text_node.text)
  elif text_node.text_type == text_type_link:
    return LeafNode("a", text_node.text, {"href" : text_node.url})
  elif text_node.text_type == text_type_image:
    return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
  else:
    raise ValueError(f"TextNode type must be one of {text_type_text}, {text_type_bold}, {text_type_italic}, {text_type_code}, {text_type_link}, {text_type_image}.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  text_type_regexes = {
    text_type_delimiters[text_type_bold]: re.compile(r"\*\*"),
    text_type_delimiters[text_type_italic]: re.compile(r"\*(?!=\*)"),
    text_type_delimiters[text_type_code]: re.compile("`")
  }

  nodes = []

  for node in old_nodes:
    if node.text_type != text_type_text:
      nodes.append(node)
    else:
      split_node = text_type_regexes[delimiter].split(node.text)
      last_node_tagged = True

      if len(split_node) % 2 == 0:
        raise ValueError("TextNode contains an unclosed tag.")

      for node_element in split_node:
        if node_element != '':
          if last_node_tagged:
            nodes.append(TextNode(node_element, text_type_text))
          else:
            nodes.append(TextNode(node_element, text_types[delimiter]))

        last_node_tagged = not last_node_tagged

  return nodes