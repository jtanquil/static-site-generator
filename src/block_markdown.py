import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
  newline_separator = re.compile("\n{2,}")

  return list(map(lambda block: block.strip(), re.split(newline_separator, markdown)))

def block_to_block_type(block):
  heading_match = re.compile("^#{1,6} ")
  code_match = re.compile("^```.*```$")
  quote_line_match = re.compile("^>.*")
  unordered_line_match = re.compile("^(*|-) ")