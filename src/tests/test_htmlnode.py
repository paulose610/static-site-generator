import unittest

from src.htmlnode import HtmlNode, LeafNode, ParentNode

class test_HtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("p","text para",[HtmlNode("h1","heading"),HtmlNode("a","link",[],{'href': 'https://www.google.com'})])
        self.assertEqual(node.props_to_html(),"")
        print(node)

    def test_props_to_html2(self):
        node = HtmlNode("p","text para",[],{
                                            "href": "https://www.google.com",
                                            "target": "_blank",
                                            }
                        )
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')
        print(node)


class test_leafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "jiu", None, {'href':'fkdnhekrwh'})
        self.assertEqual(node.to_html(), '<a href="fkdnhekrwh">jiu</a>')


class test_ParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", None, [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", None, [grandchild_node])
        parent_node = ParentNode("div", None, [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        children = [
            LeafNode("span", "one"),
            LeafNode("b", "two"),
            LeafNode("i", "three"),
        ]
        parent = ParentNode("div", None, children)
        self.assertEqual(
            parent.to_html(),
            "<div><span>one</span><b>two</b><i>three</i></div>",
        )

    def test_deeply_nested_tree(self):
        node = ParentNode(
            "div",
            None,
            [
                ParentNode(
                    "section",
                    None,
                    [
                        ParentNode(
                            "article",
                            None,
                            [
                                LeafNode("p", "deep"),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>deep</p></article></section></div>",
        )

    def test_mixed_leaf_and_parent_children(self):
        node = ParentNode(
            "div",
            None,
            [
                LeafNode("p", "text"),
                ParentNode(
                    "span",
                    None,
                    [
                        LeafNode("b", "bold"),
                        LeafNode("i", "italic"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>text</p><span><b>bold</b><i>italic</i></span></div>",
        )

    def test_sibling_parent_nodes(self):
        node = ParentNode(
            "div",
            None,
            [
                ParentNode("ul", None, [
                    LeafNode("li", "a"),
                    LeafNode("li", "b"),
                ]),
                ParentNode("ol", None, [
                    LeafNode("li", "1"),
                    LeafNode("li", "2"),
                ]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>a</li><li>b</li></ul><ol><li>1</li><li>2</li></ol></div>",
        )

    def test_single_child_parent(self):
        child = ParentNode("span", None, [LeafNode("code", "x")])
        parent = ParentNode("div", None, [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><code>x</code></span></div>",
        )


if __name__ == "__main__":
    unittest.main()