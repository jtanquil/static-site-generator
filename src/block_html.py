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
  return block.strip("```")

def get_quote_text(block):
  return "\n".join([line.lstrip("> ") for line in block.split("\n")])

def get_unordered_list_item_text(item):
  return item.lstrip("*- ")

def get_ordered_list_item_text(item):
  return item.lstrip("1234567890. ")

def block_to_html_node(block, block_type):
  match block_type:
    case block_markdown.block_type_paragraph:
      return LeafNode("p", block)
    case block_markdown.block_type_heading:
      return LeafNode(f"h{get_heading_number(block)}", get_heading_text(block))
    case block_markdown.block_type_code:
      return ParentNode("pre", LeafNode("code", get_code_text(block)))
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
# if no children, keep the LeafNode as is
# otherwise, the LeafNode is converted to a ParentNode with the same tag, 
# whose children is the list of TextNodes converted into LeafNodes with the appropriate inline tag
def markdown_to_html_node(markdown):
  blocks = block_markdown.markdown_to_blocks(markdown)
  root_node = ParentNode("div", [block_to_html_node(block, block_markdown.block_to_block_type(block)) for block in blocks])
  markdown_node = root_node.children[0]

  for i in range(len(markdown_node.children)):
    if markdown_node.children[i].value == "":
      continue
    else:
      text_nodes = text_to_textnodes(markdown_node.children[i].value)

      if len(text_nodes) == 1 and text_nodes[0].text_type == text_type_text:
        continue
      else:
        markdown_node.children[i] = ParentNode(markdown_node.children[i].tag, [text_node_to_html_node(node) for node in text_nodes])

  return root_node