import unittest

from textnode import *
from inline_markdown import *

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

class TestExtractMarkdownImages(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["no_images"] = "this text has no images"
    self.test_results["no_images"] = []

    self.test_cases["no_alt_text"] = "this ![](https://www.test.com/test.jpg) has no alt text"
    self.test_results["no_alt_text"] = [("", "https://www.test.com/test.jpg")]

    self.test_cases["alt_text"] = "this ![hi](https://www.test.com/test1.jpg) has some ![alt text](https://www.test.com/test2.png)"
    self.test_results["alt_text"] = [("hi", "https://www.test.com/test1.jpg"), ("alt text", "https://www.test.com/test2.png")]

  def test_extract_markdown_images(self):
    for case in self.test_cases:
      self.assertEqual(extract_markdown_images(self.test_cases[case]), self.test_results[case])

class TestExtractLinks(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["no_links"] = "this text has no links"
    self.test_results["no_links"] = []

    self.test_cases["links"] = "this text [has](https://www.google.com) [links](https://www.yahoo.com)"
    self.test_results["links"] = [("has", "https://www.google.com"), ("links", "https://www.yahoo.com")]

  def test_extract_markdown_links(self):
    for case in self.test_cases:
      self.assertEqual(extract_markdown_links(self.test_cases[case]), self.test_results[case])

class TestSplitNodesImage(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["no_images"] = [TextNode("no images", text_type_text)]
    self.test_results["no_images"] = [TextNode("no images", text_type_text)]

    self.test_cases["image_at_ends"] = [TextNode("![image](https://www.google.com/test1.jpg) at beginning and ![end](https://www.yahoo.com/test2.png)", text_type_text)]
    self.test_results["image_at_ends"] = [TextNode("image", text_type_image, "https://www.google.com/test1.jpg"), TextNode(" at beginning and ", text_type_text), TextNode("end", text_type_image, "https://www.yahoo.com/test2.png")]

    self.test_cases["multiple_images"] = [TextNode("multiple ![images](https://www.google.com/test3.bmp) ![here](https://www.yahoo.com/test4.gif)![test no space](https://www.google.com/test5.png) here", text_type_text)]
    self.test_results["multiple_images"] = [TextNode("multiple ", text_type_text), TextNode("images", text_type_image, "https://www.google.com/test3.bmp"), TextNode(" ", text_type_text), TextNode("here", text_type_image, "https://www.yahoo.com/test4.gif"), TextNode("test no space", text_type_image, "https://www.google.com/test5.png"), TextNode(" here", text_type_text)]

  def test_split_nodes_image(self):
    for case in self.test_cases:
      self.assertEqual(split_nodes_image(self.test_cases[case]), self.test_results[case])

class TestSplitNodesLink(unittest.TestCase):
  def setUp(self):
    self.test_cases = {}
    self.test_results = {}

    self.test_cases["no_links"] = [TextNode("no links", text_type_text)]
    self.test_results["no_links"] = [TextNode("no links", text_type_text)]

    self.test_cases["links_at_ends"] = [TextNode("[link](https://www.google.com) at the beginning and at the [end](https://www.yahoo.com)", text_type_text)]
    self.test_results["links_at_ends"] = [TextNode("link", text_type_link, "https://www.google.com"), TextNode(" at the beginning and at the ", text_type_text), TextNode("end", text_type_link, "https://www.yahoo.com")]

    self.test_cases["multiple_links"] = [TextNode("multiple [links](https://www.google.com) [here](https://www.yahoo.com)[no space](https://www.google.com) here", text_type_text)]
    self.test_results["multiple_links"] = [TextNode("multiple ", text_type_text), TextNode("links", text_type_link, "https://www.google.com") , TextNode(" ", text_type_text), TextNode("here", text_type_link, "https://www.yahoo.com"), TextNode("no space", text_type_link, "https://www.google.com"), TextNode(" here", text_type_text)]

  def test_split_nodes_link(self):
    for case in self.test_cases:
      self.assertEqual(split_nodes_link(self.test_cases[case]), self.test_results[case])

if __name__ == "__main__":
  unittest.main()