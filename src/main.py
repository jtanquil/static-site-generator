from textnode import TextNode
from htmlnode import HTMLNode

test = HTMLNode("p", "test", None)

print(test, test.props_to_html())