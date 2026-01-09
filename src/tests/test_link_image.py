import unittest

from src.inline_helper import extract_markdown_images, extract_markdown_links, split_nodes_images_or_links
from src.textnode import TextNode, TextType

class test_extract_images(unittest.TestCase):
    def test_1(self): 
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        self.assertListEqual(res,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class test_extract_links(unittest.TestCase):
    def test_1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        self.assertListEqual(res,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


class test_split_images(unittest.TestCase):

    def test_image_at_start(self):
        node = TextNode(
            "![start](https://example.com/start.png) text after",
            TextType.TEXT,
        )
        node1 = TextNode(
            "![end](https://example.com/start.png) text after end",
            TextType.TEXT,
        )
                

        new_nodes = split_nodes_images_or_links([node,node1],TextType.IMAGE)

        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" text after", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" text after end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Text before ![end](https://example.com/end.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node],TextType.IMAGE)

        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_multiple_images_back_to_back(self):
        node = TextNode(
            "![one](a.png)![two](b.png)![three](c.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node],TextType.IMAGE)

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "a.png"),
                TextNode("two", TextType.IMAGE, "b.png"),
                TextNode("three", TextType.IMAGE, "c.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "This is plain text with no images.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node],TextType.IMAGE)

        self.assertListEqual([node], new_nodes)

    def test_adjacent_text_and_image(self):
        node = TextNode(
            "Hello![img](a.png)World",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node],TextType.IMAGE)

        self.assertListEqual(
            [
                TextNode("Hello", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "a.png"),
                TextNode("World", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_image_syntax_raises(self):
        node = TextNode(
            "This is broken ![image](not_closed",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images_or_links([node],TextType.IMAGE)
        self.assertListEqual(
            [
                TextNode(
                "This is broken ![image](not_closed",
                TextType.TEXT,
                )
            ],
            new_nodes,
        )
        
class test_split_links(unittest.TestCase):

    def test_link_at_start(self):
        node = TextNode(
            "[start](https://example.com/start) text after",
            TextType.TEXT,
        )
        node1 = TextNode(
            "[end](https://example.com/start) text after end",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node, node1], TextType.LINK)

        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://example.com/start"),
                TextNode(" text after", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://example.com/start"),
                TextNode(" text after end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Text before [end](https://example.com/end)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node], TextType.LINK)

        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_multiple_links_back_to_back(self):
        node = TextNode(
            "[one](a.com)[two](b.com)[three](c.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node], TextType.LINK)

        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "a.com"),
                TextNode("two", TextType.LINK, "b.com"),
                TextNode("three", TextType.LINK, "c.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "This is plain text with no links.",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node], TextType.LINK)

        self.assertListEqual([node], new_nodes)

    def test_adjacent_text_and_link(self):
        node = TextNode(
            "Hello[link](a.com)World",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node], TextType.LINK)

        self.assertListEqual(
            [
                TextNode("Hello", TextType.TEXT),
                TextNode("link", TextType.LINK, "a.com"),
                TextNode("World", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_link_syntax(self):
        node = TextNode(
            "This is broken [link](not_closed",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_or_links([node], TextType.LINK)

        self.assertListEqual(
            [
                TextNode(
                    "This is broken [link](not_closed",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )

    def test_from_boots(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_images_or_links([node],TextType.LINK)

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()