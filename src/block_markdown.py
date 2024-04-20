import re

def markdown_to_blocks(markdown):
  newline_separator = re.compile("\n{2,}")

  return list(map(lambda block: block.strip(), re.split(newline_separator, markdown)))