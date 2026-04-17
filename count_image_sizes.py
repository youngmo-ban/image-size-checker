#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path
from PIL import Image
from openpyxl import Workbook

EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}
MIN_WIDTH = 1280
MIN_HEIGHT = 720


def main(root: str, excel_path: str) -> None:
    root_path = Path(root)
    if not root_path.is_dir():
        print(f"폴더가 존재하지 않습니다: {root}", file=sys.stderr)
        sys.exit(1)

    counter: Counter[str] = Counter()
    low_res: list[tuple[str, str, int, int]] = []
    errors = 0
    total = 0

    for path in root_path.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        total += 1
        try:
            with Image.open(path) as img:
                w, h = img.width, img.height
            counter[f"{w}x{h}"] += 1
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                low_res.append((str(path.parent), path.name, w, h))
        except Exception:
            errors += 1

    for size, count in sorted(counter.items(), key=lambda x: -x[1]):
        print(f"{size}: {count}개")

    print(f"\n총 {total}개 이미지 처리, 읽기 실패 {errors}개")
    valid = total - errors
    ratio = (len(low_res) / valid * 100) if valid else 0
    print(f"{MIN_WIDTH}x{MIN_HEIGHT} 미만 이미지: {len(low_res)}개 ({ratio:.2f}%)")

    wb = Workbook()
    ws = wb.active
    ws.title = "low_res"
    ws.append(["경로", "파일명", "width", "height"])
    for row in low_res:
        ws.append(row)
    wb.save(excel_path)
    print(f"엑셀 저장: {excel_path}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/data/cdn/backup/251121/image/news/2026"
    out = sys.argv[2] if len(sys.argv) > 2 else "low_res_images.xlsx"
    main(target, out)
