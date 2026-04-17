#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path
from PIL import Image

EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}


def main(root: str) -> None:
    root_path = Path(root)
    if not root_path.is_dir():
        print(f"폴더가 존재하지 않습니다: {root}", file=sys.stderr)
        sys.exit(1)

    counter: Counter[str] = Counter()
    errors = 0
    total = 0

    for path in root_path.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        total += 1
        try:
            with Image.open(path) as img:
                counter[f"{img.width}x{img.height}"] += 1
        except Exception:
            errors += 1

    for size, count in sorted(counter.items(), key=lambda x: -x[1]):
        print(f"{size}: {count}개")

    print(f"\n총 {total}개 이미지 처리, 읽기 실패 {errors}개")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/data/cdn/backup/251121/image/news/2026"
    main(target)
