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
      self.test_cases[f"heading_{i}"] = f"{'#' * i} heading"
      self.test_results[f"heading_{i}"] = block_type_heading

    self.test_cases["heading_multiline"] = "# heading\n## except there are two lines"
    self.test_results["heading_multiline"] = block_type_paragraph

    self.test_cases["code"] = "```code\nsnippet```"
    self.test_results["code"] = block_type_code

    self.test_cases["quote"] = "> quote\n> more quote\n> even more quote"
    self.test_results["quote"] = block_type_quote

    self.test_cases["asterisk_unordered_list"] = "* unordered list\n* with \n* asterisks"
    self.test_results["asterisk_unordered_list"] = block_type_unordered_list

    self.test_cases["dash_unordered_list"] = "- unordered list\n- with \n- dashes"
    self.test_results["dash_unordered_list"] = block_type_unordered_list

    self.test_cases["mixed_unordered_list"] = "* unordered list\n- with \n* asterisks and dashes"
    self.test_results["mixed_unordered_list"] = block_type_paragraph

    self.test_cases["ordered_list"] = "1. ordered\n2. list"
    self.test_results["ordered_list"] = block_type_ordered_list

    self.test_cases["wrong_numbers"] = "2. not\na. an\n1. ordered list"
    self.test_results["wrong_numbers"] = block_type_paragraph

    self.test_cases["no_spaces"] = "1.not\n2. an ordered\n3.list"
    self.test_results["no_spaces"] = block_type_paragraph

  def test_block_to_block_type(self):
    for case in self.test_cases:
      self.assertEqual(block_to_block_type(self.test_cases[case]), self.test_results[case])

if __name__ == "__main__":
  unittest.main()