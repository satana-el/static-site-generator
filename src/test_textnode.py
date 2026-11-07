import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node_noteq = TextNode("This is a sentence.", TextType.TEXT)
        node_noteq2 = TextNode("This is another sentence.", TextType.TEXT)
        self.assertNotEqual(node_noteq, node_noteq2)

        node_diff = TextNode("aaa", TextType.LINK, "http://example.com")
        node_diff2 = TextNode("bbb", TextType.TEXT)
        self.assertNotEqual(node_diff, node_diff2)


if __name__ == "__main__":
    unittest.main()
