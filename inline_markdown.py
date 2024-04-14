import re

from textnode import *

text_type_delimiters = {
  text_type_text: "",
  text_type_bold: "**",
  text_type_italic: "*",
  text_type_code: "`"
}
text_types = {text_type_delimiters[key]:key for key in text_type_delimiters}

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