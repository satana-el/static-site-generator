import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("<a>", "test1", None, {
                        "href": "http://www.example.com",
                        "target": "_blank"
        })
        node_result = ' href="http://www.example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node_result)

        node_empty = HTMLNode()
        self.assertEqual(node_empty.props_to_html(), "")

        node_empty_prop = HTMLNode(props={})
        self.assertEqual(node_empty_prop.props_to_html(), "")

        node_one_prop = HTMLNode(props={"bramhan": "reality"})
        node_one_prop_result = ' bramhan="reality"'
        self.assertEqual(node_one_prop.props_to_html(), node_one_prop_result)

if __name__ == "__main__":
    unittest.main()
