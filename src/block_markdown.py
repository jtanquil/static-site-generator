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
  heading_match = re.compile("^#{1,6} .*")
  code_match = re.compile("^```.*```.{0}", flags = re.DOTALL)
  quote_line_match = re.compile("^> .*$")
  asterisk_unordered_line_match = re.compile(r"^\* .*$")
  dash_unordered_line_match = re.compile("^- .*$")

  if len(block.split("\n")) == 1 and re.match(heading_match, block):
    return block_type_heading
  elif re.match(code_match, block):
    return block_type_code
  else:
    lines = block.split("\n")

    if all(re.match(quote_line_match, line) for line in lines):
      return block_type_quote
    elif all(re.match(asterisk_unordered_line_match, line) for line in lines) or all(re.match(dash_unordered_line_match, line) for line in lines):
      return block_type_unordered_list

    for i in range(len(lines)):
      ordered_list_line_match = re.compile(rf"^{i + 1}\. .*$")

      if not re.match(ordered_list_line_match, lines[i]):
        return block_type_paragraph
      
    return block_type_ordered_list