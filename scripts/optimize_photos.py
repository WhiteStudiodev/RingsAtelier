# -*- coding: utf-8 -*-
"""
Оптимизация фото для каталога: исходники (JPG/PNG/WEBP/TIFF/HEIC/BMP)
 -> WebP, максимум 1480 px по длинной стороне, качество 85.

Пайплайн тот же, что использовался для public/rings_new (см. .tmp_venv/convert_photos.py).

Использование:
    .tmp_venv/Scripts/python.exe scripts/optimize_photos.py <папка_с_исходниками> <папка_назначения>

Пример:
    .tmp_venv/Scripts/python.exe scripts/optimize_photos.py "B:/RingsAtelier/фото новые" "B:/RingsAtelier/public/pomolvochnye"
"""
import re
import sys
from pathlib import Path

from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_OK = True
except ImportError:
    HEIC_OK = False

MAX_SIZE = 1480
QUALITY = 85
SRC_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}
if HEIC_OK:
    SRC_EXTS |= {'.heic', '.heif'}


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
        img = load_rgb(f)
        w, h = img.size
        if max(w, h) > MAX_SIZE:
            scale = MAX_SIZE / max(w, h)
            img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
        img.save(out_path, 'WEBP', quality=QUALITY, method=6)
        orig_kb, new_kb = f.stat().st_size / 1024, out_path.stat().st_size / 1024
        results.append((f.name, out_path.name, orig_kb, new_kb))
        print(f'{f.name:60} -> {out_path.name:60} {orig_kb:9.1f} KB -> {new_kb:7.1f} KB')

    total_orig = sum(r[2] for r in results)
    total_new = sum(r[3] for r in results)
    print(f'\nОбработано: {len(results)}, пропущено: {skipped}')
    if results:
        print(f'Итого: {total_orig / 1024:.1f} MB -> {total_new / 1024:.1f} MB')

    report = dst_dir / '_conversion_report.txt'
    with report.open('w', encoding='utf-8') as out:
        out.write(f'Converted {len(results)} files\n')
        out.write(f'Total: {total_orig / 1024:.1f} MB -> {total_new / 1024:.1f} MB\n\n')
        for orig, new, orig_kb, new_kb in results:
            out.write(f'{orig} -> {new} ({orig_kb:.1f} KB -> {new_kb:.1f} KB)\n')
    print(f'Отчёт: {report}')
    return 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(Path(args[0]), Path(args[1])))
