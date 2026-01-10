import unittest
import pprint as p

from src.helper.md_to_html import markdown_to_html_node

class test_md_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_multiple_paragraphs(self):
        md = """
First paragraph line one
line two

Second paragraph here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><p>First paragraph line one line two</p><p>Second paragraph here</p></div>",
        )


    def test_unordered_list(self):
        md = """
- Item one
- Item two
- Item three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )


    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )


    def test_blockquote(self):
        md = """
> This is a quote
> that spans lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans lines</blockquote></div>",
        )


    def test_mixed_blocks(self):
        md = """
Intro paragraph

- List item one
- List item two

> Quoted text here

Final paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><p>Intro paragraph</p><ul><li>List item one</li><li>List item two</li></ul><blockquote>Quoted text here</blockquote><p>Final paragraph</p></div>",
        )

    def test_all_block_types(self):
        self.maxDiff = None
        md = """
This is the _opening paragraph_.
It spans multiple lines **but** should be treated as a single paragraph.

This is the second paragraph, separated by an image ![you](www.link).

### teh fitr ordered list

- _First_ unordered item
- Second unordered item
- Third unordered item

## thekdfs
##### hu

1. First **ordered** item
2. Second ordered item with ![image](link)
3. Third ordered item 

> This is a block quote
> that spans multiple [lines](link)
> and should be merged into one paragraph.
"""

        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<p>This is the <i>opening paragraph</i>. It spans multiple lines <b>but</b> should be treated as a single paragraph.</p>"
            "<p>This is the second paragraph, separated by an image <img src='www.link' alt='you'/>.</p>"
            "<h3>teh fitr ordered list</h3>"
            "<ul><li><i>First</i> unordered item</li><li>Second unordered item</li><li>Third unordered item</li></ul>"
            "<h2>thekdfs</h2>"
            "<ol><li>First <b>ordered</b> item</li><li>Second ordered item with <img src='link' alt='image'/></li><li>Third ordered item</li></ol>"
            "<blockquote>This is a block quote that spans multiple <a href='link'>lines</a> and should be merged into one paragraph.</blockquote>"
            "</div>",
        )

    def test_all_block_types_2(self):
        self.maxDiff = None
        md = """
This is the _opening paragraph_.
It spans multiple lines **but** should be treated as a single paragraph.

This is the second paragraph, separated by an image ![you](www.link).
"""

        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<p>This is the <i>opening paragraph</i>. It spans multiple lines <b>but</b> should be treated as a single paragraph.</p>"
            "<p>This is the second paragraph, separated by an image <img src='www.link' alt='you'/>.</p>"
            "</div>",
        )