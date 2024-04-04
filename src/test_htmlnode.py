import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
  def setUp(self):
    self.node_with_props = HTMLNode("p", "test", None, {"href": "https://www.google.com", "target": "_blank"})
    self.node_one_prop = HTMLNode("p", "test", None, {"href": "https://www.google.com"})
    self.node_no_props = HTMLNode("p", "test")

  def test_props_to_html(self):
    node_with_props_str = ' href="https://www.google.com" target="_blank"'
    node_one_prop_str = ' href="https://www.google.com"'
    node_no_props_str = ""

    self.assertEqual(self.node_with_props.props_to_html(), node_with_props_str)
    self.assertEqual(self.node_one_prop.props_to_html(), node_one_prop_str)
    self.assertEqual(self.node_no_props.props_to_html(), node_no_props_str)


class TestLeafNode(unittest.TestCase):
  def setUp(self):
    self.plain_leaf_node = LeafNode(None, "hi")
    self.leaf_node_with_tag = LeafNode("p", "hello")
    self.leaf_node_tag_props = LeafNode("p", "hello", {"href": "https://www.google.com", "target": "_blank"})

  def test_to_html(self):
    plain_leaf_node_text = "hi"
    leaf_node_with_tag_text = "<p>hello</p>"
    leaf_node_tag_props_text = '<p href="https://www.google.com" target="_blank">hello</p>'

    self.assertEqual(self.plain_leaf_node.to_html(), plain_leaf_node_text)
    self.assertEqual(self.leaf_node_with_tag.to_html(), leaf_node_with_tag_text)
    self.assertEqual(self.leaf_node_tag_props.to_html(), leaf_node_tag_props_text)

if __name__ == "__main__":
  unittest.main()