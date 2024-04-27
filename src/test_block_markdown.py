import unittest

from block_markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["one_line"] = "this should be one line\neven though there is a newline"
    self.test_results["one_line"] = ["this should be one line\neven though there is a newline"]

    self.test_cases["multiple_lines"] = "this should be multiple lines\n\nbecause there are consecutive newlines\n\n\n\n* testing a list\n* another **list item**\n\n       ![and a tag](https://www.google.com)\n     strip whitespace             "
    self.test_results["multiple_lines"] = ["this should be multiple lines", "because there are consecutive newlines", "* testing a list\n* another **list item**","![and a tag](https://www.google.com)\n     strip whitespace"]

  def test_markdown_to_blocks(self):
    for case in self.test_cases:
      self.assertEqual(markdown_to_blocks(self.test_cases[case]), self.test_results[case])

class TestBlockToBlockType(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["no_type_paragraph"] = "this is a paragraph"
    self.test_results["no_type_paragraph"] = block_type_paragraph

    for i in range(1, 7):
      self.test_cases[f"heading {i}"] = f"{'#' * i} heading"
      self.test_results[f"heading {i}"] = block_type_heading

    self.test_cases["code"] = "```code snippet```"
    self.test_cases["code"] = block_type_code

    self.test_cases["quote"] = ">quote\n> more quote"
    self.test_cases["quote"] = block_type_quote

  def test_block_to_block_type(self):
    pass

if __name__ == "__main__":
  unittest.main()