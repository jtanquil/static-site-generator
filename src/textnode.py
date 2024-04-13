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

# input: a list of TextNodes, a delimiter, and a text type
# output: a list of TextNodes obtained by splitting up each input TextNode based on the given delimiter:
# (ex: "this **is bold** text" => TextNode("this ", text_node_text), TextNode("is bold", text_type_bold), TextNode(" text", text_node_text))
# scope: a single delimiter, one level deep - don't worry about nested delimiters for now
# edge cases: delimiter not found, entire text value is within the delimiter (=> beginning/end are in the delimiter), unclosed delimiters

# given a TextNode with a value val, a delimiter, and a text type,
# set delimiter_is_closed = True; this will represent whether the current delimiter has been closed
# set nodes = []; this will be the list of new nodes returned
# for each node in old_nodes:
# if the node's tag is not text, add it to the list of nodes unchanged
# split the node with the corresponding regex
# test for unclosed tags, raise an error if they are found:
#   - if the length of the list of split nodes is even, raise an error (even split => odd number of matched tags => there is an unclosed tag)
# otherwise, add nodes to the list of nodes:
#   - set last_node_tagged = False; nodes are tagged or untagged in alternating order so this is used to set the tag appropriately
#   - if the first element of the list is the empty string, the first non-empty element is tagged, add it as a node to nodes with that tag and set last_node_tagged = True
#     - => if the first element is the empty string, continue to the next element
#   - otherwise, the first element is untagged, add it to the node as a plain text node, set last_node_tagged = False
#   - alternate between tag/untagged nodes => if last_node_tagged = True, add the current node as a plain text tag, otherwise add it as a tagged tag
#   - if the last element is empty, discard it; in that case, the last element was tagged

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