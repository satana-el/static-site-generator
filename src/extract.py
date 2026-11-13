import re
from textnode import TextType, TextNode
import textnode

def extract_markdown_images(text: str) -> list:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_images(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for link in links:
            text = remaining_text.split(f"![{link[0]}]({link[1]})", maxsplit=1)
            if text[0] != "":
                new_nodes.append(TextNode(text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.IMAGE, link[1]))
            remaining_text = text[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for link in links:
            text = remaining_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if text[0] != "":
                new_nodes.append(TextNode(text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = text[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
