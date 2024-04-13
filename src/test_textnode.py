import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    test_text = ["text1", "text2"]
    test_style = ["bold", "italics"]
    test_url = ["https://www.google.com", None]

    # exhausts possible combinations of properties being equal or not
    for text_pair in [[text1, text2] for text1 in test_text for text2 in test_text]:
      for style_pair in [[style1, style2] for style1 in test_style for style2 in test_style]:
        for url_pair in [[url1, url2] for url1 in test_url for url2 in test_url]:
          node1 = TextNode(text_pair[0], style_pair[0], url_pair[0])
          node2 = TextNode(text_pair[1], style_pair[1], url_pair[1])
          
          self.assertEqual(node1 == node2, text_pair[0] == text_pair[1] and style_pair[0] == style_pair[1] and url_pair[0] == url_pair[1])


  def test_repr(self):
    node = TextNode("test node", "italics", "https://www.google.com")
    node2 = TextNode("test node 2", "strikethrough")
    self.assertEqual(repr(node), "TextNode(test node, italics, https://www.google.com)")
    self.assertEqual(repr(node2), "TextNode(test node 2, strikethrough, None)")

class TestTextNodeToHTMLNode(unittest.TestCase):
  def setUp(self):
    self.plain_text_node = TextNode("test", text_type_text)
    self.bold_text_node = TextNode("test", text_type_bold)
    self.italic_text_node = TextNode("test", text_type_italic)
    self.code_text_node = TextNode("test", text_type_code)
    self.text_type_link = TextNode("test", text_type_link, "https://www.google.com")
    self.text_type_image = TextNode("test", text_type_image, "https://www.google.com")
    self.text_type_invalid = TextNode("test", "test")

  def test_text_node_to_html_node(self):
    self.assertEqual(text_node_to_html_node(self.plain_text_node).to_html(), "test")
    self.assertEqual(text_node_to_html_node(self.bold_text_node).to_html(), "<b>test</b>")
    self.assertEqual(text_node_to_html_node(self.italic_text_node).to_html(), "<i>test</i>")
    self.assertEqual(text_node_to_html_node(self.code_text_node).to_html(), "<code>test</code>")
    self.assertEqual(text_node_to_html_node(self.text_type_link).to_html(), '<a href="https://www.google.com">test</a>')
    self.assertEqual(text_node_to_html_node(self.text_type_image).to_html(), '<img src="https://www.google.com" alt="test">')
    self.assertRaises(ValueError, text_node_to_html_node, self.text_type_invalid)

# test:
# text node with no inline elements
# text node with one inline element surrounding the entire text value (ex: "*bold*")
# text node with inline elements at the beginning/end of the line
# text node with multiple inline elements
# text node with a unclosed inline element (ex: "here is `some code") at beginning/mid/end
# multiple text nodes with each property above ^
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