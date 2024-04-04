import unittest

from textnode import TextNode

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

if __name__ == "__main__":
  unittest.main()