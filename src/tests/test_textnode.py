import unittest

from src.textnode import TextType, TextNode
#from src.htmlnode import LeafNode
from src.main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK, 'asdad')
        node2 = TextNode("This is a text node", TextType.LINK, 'asdad')
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node),'TextNode(This is a text node, bold, None)')


class TestTexttoHtml(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.val, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.val, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.val, "italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.val, "print('hi')")

    def test_link(self):
        node = TextNode(
            "OpenAI",
            TextType.LINK,
            url="https://openai.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.val, "OpenAI")
        self.assertEqual(html_node.props, {"href": "https://openai.com"})

    def test_image(self):
        node = TextNode(
            None,
            TextType.IMAGE,
            url="image.png",
            alt="an image"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.val, None)
        self.assertEqual(
            html_node.props,
            {"src": "image.png", "alt": "an image"}
        )


if __name__ == "__main__":
    unittest.main()