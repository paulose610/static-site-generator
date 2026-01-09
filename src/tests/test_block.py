import unittest

from src.block_helper import markdown_to_blocks, block_to_block_type, BlockType


class test_md_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )   
    def test_markdown_with_multiple_blank_lines_and_spacing(self):
        md = """

# Heading one


This is a paragraph with **bold**
and _italic_ on a new line.



- Item one

- Item two
- Item three

This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev),
Another paragraph after list
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "# Heading one",
                "This is a paragraph with **bold**\nand _italic_ on a new line.",
                "- Item one",
                "- Item two\n- Item three",
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev),\nAnother paragraph after list",
            ],
        ) 


class test_md_to_BlockType(unittest.TestCase):

    def test_heading(self):
        block = "## Heading level 2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_quote_block(self):
        block = "> quote line one\n> quote line two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_ordered_list(self):
        block = "1. first item\n2. second item\n3. third item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.O_LIST
        )

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UO_LIST
        )

    def test_paragraph(self):
        block = "This is a normal paragraph\nwith multiple lines."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA
        )
