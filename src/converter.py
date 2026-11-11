from textnode import TextType, TextNode, text_node_to_html_node
from extract import split_nodes_link, split_nodes_image
from enum import Enum
from htmlnode import HTMLNode, ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph block"
    HEADING = "heading block"
    CODE = "code block"
    QUOTE = "quote block"
    UNORDERED_LIST = "unordered_list block"
    ORDERED_LIST = "ordered_list block"


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


def block_to_block_type(block: str) -> BlockType:
    headings = (
        "# ",
        "## ",
        "### ",
        "#### ",
        "##### ",
        "###### ",
    )
    if block.startswith(headings):
        return BlockType.HEADING

    lines = block.split('\n')

    if lines[0] == '```' and lines[-1] == '```':
        if (len(lines) > 1):
            return BlockType.CODE

    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    o_list = False
    for i, line in enumerate(lines):
        if line.startswith(f"{i+1}. "):
            o_list = True
            continue
        o_list = False
        break

    if o_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        node = None
        match type:
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_block = ""
                for line in lines:
                    if line.startswith("> "):
                        new_block += f"{line[2:]}\n"
                        continue
                    new_block += f"{line[1:]}\n"
                node = ParentNode("blockquote", text_to_children(new_block.strip()))
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                c_nodes = []
                for item in items:
                    c_nodes.append(ParentNode("li", text_to_children(item[2:])))
                node = ParentNode("ul", c_nodes)
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                c_nodes = []
                for item in items:
                    n, i = item.split(". ", 1)
                    c_nodes.append(ParentNode("li", text_to_children(i)))
                node = ParentNode("ol", c_nodes)
            case BlockType.CODE:
                tmp = text_node_to_html_node(TextNode(block[4:-3], TextType.CODE))
                node = ParentNode("pre", [tmp])
            case BlockType.HEADING:
                n, text = block.split(" ", 1)
                node = ParentNode(f"h{len(n)}", text_to_children(text))
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                print(repr(block))
                text = ""
                for line in lines:
                    text += f"{line.strip()} "
                node = ParentNode("p", text_to_children(text.strip()))
        children.append(node)
    return ParentNode("div", children)


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    child_nodes = []
    for node in nodes:
        child_nodes.append(text_node_to_html_node(node))

    return child_nodes
