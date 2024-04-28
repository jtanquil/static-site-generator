import unittest

from block_html import *
from block_markdown import *

class TestBlockToHTMLNode(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["paragraph"] = ("this is a paragraph", block_type_paragraph)
    self.test_results["paragraph"] = LeafNode("p", "this is a paragraph")

    for i in range(1, 7):
      self.test_cases[f"heading_{i}"] = (f"{'#' * i} heading", block_type_heading)
      self.test_results[f"heading_{i}"] = LeafNode(f"h{i}", "heading")

    self.test_cases["code"] = ("```code\nsnippet```", block_type_code)
    self.test_results["code"] = ParentNode("pre", LeafNode("code", "code\nsnippet"))

    self.test_cases["quote"] = ("> quote\n> more quote\n> even more quote", block_type_quote)
    self.test_results["quote"] = LeafNode("blockquote", "quote\nmore quote\neven more quote")

    self.test_cases["asterisk_unordered_list"] = ("* unordered list\n* with \n* asterisks", block_type_unordered_list)
    self.test_results["asterisk_unordered_list"] = ParentNode("ul", [LeafNode("li", "unordered list"), LeafNode("li", "with "), LeafNode("li", "asterisks")])

    self.test_cases["dash_unordered_list"] = ("- unordered list\n- with \n- dashes", block_type_unordered_list)
    self.test_results["dash_unordered_list"] = ParentNode("ul", [LeafNode("li", "unordered list"), LeafNode("li", "with "), LeafNode("li", "dashes")])

    self.test_cases["ordered_list"] = ("1. ordered\n2. list", block_type_ordered_list)
    self.test_results["ordered_list"] = ParentNode("ol", [LeafNode("li", "ordered"), LeafNode("li", "list")])

  def test_block_to_html_node(self):
    for case in self.test_cases:
      self.assertEqual(block_to_html_node(*self.test_cases[case]), self.test_results[case])

class TestMarkdownToHTMLNode(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["nesting"] = "1. ordered list\n2. with **inline** element"
    self.test_results["nesting"] = ParentNode("div", [ParentNode("ol", [LeafNode("li", "ordered list"), ParentNode("li", [LeafNode(None, "with "), LeafNode("b", "inline"), LeafNode(None, " element")])])])

  def test_markdown_to_html_node(self):
    for case in self.test_cases:
      self.assertEqual(markdown_to_html_node(self.test_cases[case]), self.test_results[case])

if __name__ == "__main__":
  unittest.main()