import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(HTMLNode):
  def setUp(self):
    self.leaf_node = LeafNode("b", "hi")
    self.parent_node_only_leaf = ParentNode("p", [self.leaf_node])
    self.parent_node_no_children = ParentNode("div")
    self.parent_node_no_tag = ParentNode()
    self.parent_node_recurse = ParentNode("article", [self.leaf_node, self.parent_node_only_leaf], {"href": "https://www.google.com", "target": "_blank"})

  def test_to_html(self):
    self.assertRaises(ValueError, self.parent_node_no_children.to_html())
    self.assertRaises(ValueError, self.parent_node_no_tag.to_html())

    self.assertEqual(self.parent_node_only_leaf.to_html(), "<p><b>hi</b></p>")
    self.assertEqual(self.parent_node_recurse.to_html(), '<article href="https://www.google.com" target="_blank"><b>hi</b><p><b>hi</b></p></article>')

if __name__ == "__main__":
  unittest.main()