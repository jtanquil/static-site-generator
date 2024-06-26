import re

from textnode import *

text_type_delimiters = {
  # text_type_text: "",
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

def extract_text_with_regex(text, regex_string):
  return re.findall(regex_string, text)

def extract_markdown_images(text):
  image_regex = r"!\[(.*?)\]\((.*?)\)"
  return extract_text_with_regex(text, image_regex)

def extract_markdown_links(text):
  link_regex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
  return extract_text_with_regex(text, link_regex)

def split_nodes_image(old_nodes):
  nodes = []

  for node in old_nodes:
    if node.text_type != text_type_text:
      nodes.append(node)
      continue

    images = extract_markdown_images(node.text)

    if images == []:
      nodes.append(node)
    else:
      current_node_text = node.text

      for image in images:
        image_string_delimiter = f"![{image[0]}]({image[1]})"
        split_node_elements = current_node_text.split(image_string_delimiter, 1)

        if split_node_elements[0] != "":
          nodes.append(TextNode(split_node_elements[0], text_type_text))

        nodes.append(TextNode(image[0], text_type_image, image[1]))
        current_node_text = split_node_elements[-1]

      # if there is text left over, add it to the list
      if current_node_text != "":
        nodes.append(TextNode(current_node_text, text_type_text))

  return nodes

def split_nodes_link(old_nodes):
  nodes = []

  for node in old_nodes:
    if node.text_type != text_type_text:
      nodes.append(node)
      continue

    links = extract_markdown_links(node.text)

    if links == []:
      nodes.append(node)
    else:
      current_node_text = node.text

      for link in links:
        link_string_delimiter = f"[{link[0]}]({link[1]})"
        split_node_elements = current_node_text.split(link_string_delimiter, 1)

        if split_node_elements[0] != "":
          nodes.append(TextNode(split_node_elements[0], text_type_text))

        nodes.append(TextNode(link[0], text_type_link, link[1]))
        current_node_text = split_node_elements[-1]

      if current_node_text != "":
        nodes.append(TextNode(current_node_text, text_type_text))

  return nodes

def text_to_textnodes(text):
  initial_node = [TextNode(text, text_type_text)]
  
  link_nodes = split_nodes_link(initial_node)
  image_nodes = split_nodes_image(link_nodes)

  nodes = image_nodes
  for delimiter in text_type_delimiters:
    nodes = split_nodes_delimiter(nodes, text_type_delimiters[delimiter], delimiter)

  return nodes