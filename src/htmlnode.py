class HTMLNode():
    def __init__(self, tag: str | None = None, value:str | None = None, children:list[str] | None = None, props:dict[str, str] | None = None) -> None:
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


