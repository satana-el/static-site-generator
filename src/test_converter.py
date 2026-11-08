import unittest
from converter import split_nodes_delimiter
from textnode import TextType, TextNode


class TestConverter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), result)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), result)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), result)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


