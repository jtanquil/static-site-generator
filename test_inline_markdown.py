import unittest

from textnode import *
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}
    self.exceptions = {}

    self.test_cases["no_inline_elements"] = (TextNode("no inline elements", text_type_text), text_type_bold)
    self.test_results["no_inline_elements"] = [TextNode("no inline elements", text_type_text)]
    
    self.test_cases["entire_element_inline"] = (TextNode("**entire element is inline**", text_type_text), text_type_bold)
    self.test_results["entire_element_inline"] = [TextNode("entire element is inline", text_type_bold)]

    self.test_cases["beginning_inline"] = (TextNode("`beginning` is inline", text_type_text), text_type_code)
    self.test_results["beginning_inline"] = [TextNode("beginning", text_type_code), TextNode(" is inline", text_type_text)]

    self.test_cases["end_inline"] = (TextNode("end is *inline*", text_type_text), text_type_italic)
    self.test_results["end_inline"] = [TextNode("end is ", text_type_text), TextNode("inline", text_type_italic)]

    self.test_cases["multiple_inline"] = (TextNode("**multiple** elements **are** in**line**", text_type_text), text_type_bold)
    self.test_results["multiple_inline"] = [TextNode("multiple", text_type_bold), TextNode(" elements ", text_type_text), TextNode("are", text_type_bold), TextNode(" in", text_type_text), TextNode("line", text_type_bold)]

    self.multiple_nodes = [self.test_cases["no_inline_elements"][0], self.test_cases["multiple_inline"][0]]
    self.multiple_nodes_test_results = self.test_results["no_inline_elements"][:]
    self.multiple_nodes_test_results.extend(self.test_results["multiple_inline"][:])

    self.exceptions["unclosed_inline_beginning"] = (TextNode("`unclosed element", text_type_text), text_type_code)
    self.exceptions["unclosed_inline_end"] = (TextNode("another unclosed element*", text_type_text), text_type_italic)
    self.exceptions["unclosed_inline_mid"] = (TextNode("middle ** unclosed element", text_type_text), text_type_bold)

  def test_split_nodes_delimiter(self):
    for case in self.test_cases:
      text_type = self.test_cases[case][1]
      result = split_nodes_delimiter([self.test_cases[case][0]], text_type_delimiters[text_type], text_type)
      for i in range(len(result)):
        self.assertEqual(result[i], self.test_results[case][i])

    multiple_nodes_result = split_nodes_delimiter(self.multiple_nodes, text_type_delimiters[text_type_bold], text_type_bold)
    for i in range(len(multiple_nodes_result)):
      self.assertEqual(multiple_nodes_result[i], self.multiple_nodes_test_results[i])

    for exception in self.exceptions:
      delimiter = text_type_delimiters[self.exceptions[exception][1]]
      self.assertRaises(ValueError, split_nodes_delimiter, [self.exceptions[exception][0]], delimiter, self.exceptions[exception][1])

if __name__ == "__main__":
  unittest.main()