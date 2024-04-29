import re

import block_markdown
from inline_markdown import *
from htmlnode import LeafNode, ParentNode

def get_heading_number(block):
  counter = 0

  for char in block:
    if char == "#":
      counter += 1
    else:
      break

  return counter

def get_heading_text(block):
  return re.split("^#{1,6} ", block)[1]

def get_code_text(block):
  return block.removeprefix("```").removesuffix("```")

def get_quote_text(block):
  return "\n".join([line.removeprefix("> ") for line in block.split("\n")])

def get_unordered_list_item_text(item):
  if item.startswith("*"):
    return item.removeprefix("* ")
  else:
    return item.removeprefix("- ")

def get_ordered_list_item_text(item):
  # equivalent to removing a digit from 1-9, any number of digits from 0-9 and a ., then whitespace
  return item.lstrip("123456789").lstrip("1234567890").lstrip(".").lstrip()

def block_to_html_node(block, block_type):
  match block_type:
    case block_markdown.block_type_paragraph:
      return LeafNode("p", block)
    case block_markdown.block_type_heading:
      return LeafNode(f"h{get_heading_number(block)}", get_heading_text(block))
    case block_markdown.block_type_code:
      return ParentNode("pre", [LeafNode("code", get_code_text(block))])
    case block_markdown.block_type_quote:
      return LeafNode("blockquote", get_quote_text(block))
    case block_markdown.block_type_unordered_list:
      return ParentNode("ul", [LeafNode("li", get_unordered_list_item_text(line)) for line in block.split("\n")])
    case block_markdown.block_type_ordered_list:
      return ParentNode("ol", [LeafNode("li", get_ordered_list_item_text(line)) for line in block.split("\n")])
    case _:
      raise ValueError("unsupported block type")
    
# given some markdown,
# split the markdown into blocks
# convert each block into an HTMLNode
# for each block, extract the inline elements of any LeafNodes:
# for each block, if it's a ParentNode, extract the inline elements of any child LeafNodes,
# otherwise, if it's a LeafNode, extract any inline elements: given a LeafNode
# if no inline elements, keep the LeafNode as is
# otherwise, the LeafNode is converted to a ParentNode with the same tag, 
# whose children is the list of TextNodes converted into LeafNodes with the appropriate inline tag
def extract_inline_nodes(node):
  new_node = None

  if node.value is None:
    new_node = ParentNode(node.tag, [], node.props)

    for child in node.children:
      new_node.children.append(extract_inline_nodes(child))
  else:
    text_nodes = text_to_textnodes(node.value)

    if len(text_nodes) == 1 and text_nodes[0].text_type == text_type_text:
      new_node = node
    else:
      new_node = ParentNode(node.tag, [text_node_to_html_node(text_node) for text_node in text_nodes], node.props)
    
  return new_node

def markdown_to_html_node(markdown):
  blocks = block_markdown.markdown_to_blocks(markdown)
  root_node = ParentNode("div", [block_to_html_node(block, block_markdown.block_to_block_type(block)) for block in blocks])
  content_nodes = root_node.children

  for i in range(len(content_nodes)):
    content_nodes[i] = extract_inline_nodes(content_nodes[i])

  return root_node