#!/usr/bin/env python3
"""news-image-20261122 entry: copy the bundled front-page image to /output/entry.png.

The image sums up the world news of Sunday 22 November 2026: Iran's
strikes on US bases in Bahrain and Kuwait, Russian missiles hitting Lviv
and the war spilling into Poland and the Baltic, the magnitude 6.9 quake
in Peru's Andes, the COP31 climate talks deadlocked over fossil fuels,
and the EU-Indonesia trade deal signed after ten years, plus the day's
other stories in the ticker.

Deterministic and offline: the image is drawn by draw_news.py and shipped
in this repository as entry.png, so every run writes the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
