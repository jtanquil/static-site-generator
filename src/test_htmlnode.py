import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def setUp(self):
    self.node_with_props = HTMLNode("p", "test", None, {"href": "https://www.google.com", "target": "_blank"})
    self.node_one_prop = HTMLNode("p", "test", None, {"href": "https://www.google.com"})
    self.node_no_props = HTMLNode("p", "test")

  def test_props_to_html(self):
    node_with_props_str = 'href="https://www.google.com" target="_blank"'
    node_one_prop_str = 'href="https://www.google.com"'
    node_no_props_str = ""

    self.assertEqual(self.node_with_props.props_to_html(), node_with_props_str)
    self.assertEqual(self.node_one_prop.props_to_html(), node_one_prop_str)
    self.assertEqual(self.node_no_props.props_to_html(), node_no_props_str)

if __name__ == "__main__":
  unittest.main()