from typing import Any


class HTMLNode():
    def __init__(self, tag: str | None = None, value:str | None = None, children:list[HTMLNode] | None = None, props:dict[str, Any] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        html = ''
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str, Any] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, Any] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("no children present")
        children = ''
        for child in self.children:
            children += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"

