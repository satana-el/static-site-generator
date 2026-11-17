import os
from os.path import isdir
import sys
import shutil
from generator import generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_static(src: str, dst: str, is_first=True) -> None:
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    if is_first and os.path.isdir(dst):
        shutil.rmtree(dst)

    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_static(src_path, dst_path, False)
        else:
            shutil.copy2(src_path, dst_path)

if __name__ == "__main__":
    main()
