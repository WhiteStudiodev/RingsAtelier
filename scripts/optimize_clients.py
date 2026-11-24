# -*- coding: utf-8 -*-
"""
Оптимизация фото для карусели «Наши гости» (src/components/ClientsCarousel.vue):
исходники -> WebP 600x800 (кроп по центру до 3:4, как у текущих фото в public/clients).

Использование:
    .tmp_venv/Scripts/python.exe scripts/optimize_clients.py <папка_с_исходниками> [папка_назначения]

Пример:
    .tmp_venv/Scripts/python.exe scripts/optimize_clients.py "B:/RingsAtelier/New Folder" "B:/RingsAtelier/public/clients" --force
"""
import re
import sys
from pathlib import Path

from PIL import Image

OUT_W, OUT_H = 600, 800  # 3:4, как у текущих фото гостей и атрибуты width/height в карусели
QUALITY = 82
SRC_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}


def slugify(name: str) -> str:
    """Имя файла -> безопасное: без кавычек/скобок, пробелы в подчёркивания."""
    name = re.sub(r'[«»"“”\']', '', name)
    name = name.replace(' ', '_').replace('(', '').replace(')', '')
    name = re.sub(r'[^\w\-_.]', '', name, flags=re.UNICODE)
    name = re.sub(r'_+', '_', name)
    name = re.sub(r'\.{2,}', '.', name)
    return name.strip('_').strip('.')


def load_rgb(path: Path) -> Image.Image:
    img = Image.open(path)
    if img.mode in ('RGBA', 'P', 'LA'):
        img = img.convert('RGBA')
        bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img).convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    return img


def crop_center(img: Image.Image, ratio: float) -> Image.Image:
    """Кроп по центру до соотношения сторон w/h = ratio."""
    w, h = img.size
    if w / h > ratio:  # слишком широкое — режем ширину
        new_w = round(h * ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = round(w / ratio)  # слишком высокое — режем высоту
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def main(src_dir: Path, dst_dir: Path) -> int:
    if not src_dir.is_dir():
        print(f'Ошибка: папка не найдена: {src_dir}')
        return 1
    files = sorted(
        f for f in src_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SRC_EXTS and not f.name.startswith('.')
    )
    if not files:
        print(f'В {src_dir} нет подходящих файлов ({", ".join(sorted(SRC_EXTS))})')
        return 1
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Не перезаписываем существующие webp в назначении без флага --force
    force = '--force' in sys.argv
    results = []
    skipped = 0
    for f in files:
        out_path = dst_dir / (slugify(f.stem) + '.webp')
        if out_path.exists() and not force:
            print(f'ПРОПУСК (уже есть, используй --force): {out_path.name}')
            skipped += 1
            continue
        img = crop_center(load_rgb(f), OUT_W / OUT_H)
        img = img.resize((OUT_W, OUT_H), Image.LANCZOS)
        img.save(out_path, 'WEBP', quality=QUALITY, method=6)
        orig_kb, new_kb = f.stat().st_size / 1024, out_path.stat().st_size / 1024
        results.append((f.name, out_path.name, orig_kb, new_kb))
        print(f'{f.name:40} -> {out_path.name:40} {orig_kb:9.1f} KB -> {new_kb:7.1f} KB')

    total_orig = sum(r[2] for r in results)
    total_new = sum(r[3] for r in results)
    print(f'\nОбработано: {len(results)}, пропущено: {skipped}')
    if results:
        print(f'Итого: {total_orig / 1024:.1f} MB -> {total_new / 1024:.1f} MB')
    return 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not 1 <= len(args) <= 2:
        print(__doc__)
        sys.exit(1)
    dst = Path(args[1]) if len(args) == 2 else Path('B:/RingsAtelier/public/clients')
    sys.exit(main(Path(args[0]), dst))
