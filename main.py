#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261120.

Writes the one-page summary of Friday 20 November 2026's world news to
/output/entry.png. The image ships in this repository as entry.png; this
program copies it, byte for byte, to the output path. (generate.py is the
program that drew the image; it is kept in the repository for the record.)
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
