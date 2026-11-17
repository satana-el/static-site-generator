import os
from converter import markdown_to_html_node, extract_title
from pathlib import Path


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
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
    html_file = html_file.replace('href="/', f'href="{basepath}')
    html_file = html_file.replace('src="/', f'src="{basepath}')

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_file)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    dir_path_content = os.path.abspath(dir_path_content)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)

    ls = os.listdir(dir_path_content)

    for item in ls:
        path = os.path.join(dir_path_content, item)
        if os.path.isfile(path):
            if not Path(path).suffix == ".md":
                continue
            name = Path(item).with_suffix(".html")
            html_path = os.path.join(dest_dir_path, name)
            generate_page(path, template_path, html_path, basepath)
            continue
        dest = os.path.join(dest_dir_path, item)
        generate_pages_recursive(path, template_path, dest, basepath)
