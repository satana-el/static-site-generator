import os
import shutil
from converter import extract_title, markdown_to_html_node
from textnode import TextType, TextNode

def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def copy_static(src: str, dst: str, is_first=True) -> None:
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    if is_first:
        shutil.rmtree(dst)

    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_static(src_path, dst_path, False)
        else:
            shutil.copy2(src_path, dst_path)


def generate_page(from_path, template_path, dest_path):
    from_path = os.path.abspath(from_path)
    template_path = os.path.abspath(template_path)
    dest_path = os.path.abspath(dest_path)

    print(f"Generation page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md_file = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)

    html_file = template.replace("{{ Title }}", title)
    html_file = html_file.replace("{{ Content }}", html)
    print(html_file)

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_file)

if __name__ == "__main__":
    main()
