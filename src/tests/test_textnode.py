import unittest

from src.helper.textnode import TextType, TextNode
#from src.htmlnode import LeafNode
from src.helper.inline_helper import text_node_to_html_node, splits_nodes_delimiter, text_to_textnodes


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
            "an image",
            TextType.IMAGE,
            url="image.png",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.val, None)
        self.assertEqual(
            html_node.props,
            {"src": "image.png", "alt": "an image"}
        )



class test_text_splitter(unittest.TestCase):

    def test_single_text_node_split(self):
        nodes = [TextNode("hello **world**", TextType.TEXT)]
        result = splits_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ])

    def test_non_text_node_unchanged(self):
        nodes = [TextNode("bold", TextType.BOLD)]
        result = splits_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, nodes)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("hello **world**!", TextType.TEXT),
            TextNode("This is text with a **code block** word", TextType.TEXT)
        ]

        result = splits_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_unclosed_delimiter_raises(self):
        nodes = [TextNode("hello **world", TextType.TEXT)]

        with self.assertRaises(ValueError):
            splits_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_multiple_text_nodes(self):
        nodes = [
            TextNode("**hello**", TextType.TEXT),
            TextNode(" **world**", TextType.TEXT)
        ]

        result = splits_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("hello", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ])

class test_text_to_node(unittest.TestCase):
    def test1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"    
        nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],nodes)


    def test_multiple_adjacent_formats(self):
        text = (
            "**Bold**_Italic_`Code`"
            " then text and a [link](https://example.com)"
            "![img](https://img.com/a.png)"
        )

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("Italic", TextType.ITALIC),
                TextNode("Code", TextType.CODE),
                TextNode(" then text and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("img", TextType.IMAGE, "https://img.com/a.png"),
            ],
            nodes,
        )

    def test_repeated_and_interleaved_patterns(self):
        text = (
            "Start **bold1** mid _italic1_ "
            "**bold2** and `code1` then "
            "![image1](https://a.com) text "
            "[link1](https://b.com) end"
        )

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold1", TextType.BOLD),
                TextNode(" mid ", TextType.TEXT),
                TextNode("italic1", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" then ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://a.com"),
                TextNode(" text ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()