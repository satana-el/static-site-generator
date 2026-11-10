from textnode import TextType, TextNode
from extract import split_nodes_link, split_nodes_image

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f"invalid markdown syntax: {delimiter} was not closed")
        nodes = old_node.text.split(delimiter)
        for i, text in enumerate((nodes)):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    nodes_pass1 = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_pass2 = split_nodes_delimiter(nodes_pass1, "_", TextType.ITALIC)
    nodes_pass3 = split_nodes_delimiter(nodes_pass2, "`", TextType.CODE)
    nodes_pass4 = split_nodes_image(nodes_pass3)
    return split_nodes_link(nodes_pass4)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            stripped_blocks.append(stripped)
    return stripped_blocks 
