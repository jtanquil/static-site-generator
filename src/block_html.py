import re

import block_markdown
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

def block_to_htmlnode(block, block_type):
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
    