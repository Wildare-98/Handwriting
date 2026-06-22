"""Batch convert HEIC to JPG."""
import os
import sys
from pathlib import Path

# venv 路径
venv_dir = Path(r"C:\Users\Xu\.workbuddy\binaries\python\envs\default")
site_packages = str(venv_dir / "Lib" / "site-packages")
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

from pillow_heif import register_heif_opener
register_heif_opener()
from PIL import Image

# 配置
SOURCE_DIR = Path(r"D:\AIFile\workbuddy\workflow-scan\心内科病例")
OUTPUT_DIR = Path(r"D:\AIFile\workbuddy\workflow-scan\心内科病例_jpg")
JPEG_QUALITY = 40  # 小体积优先，病例文字仍可辨

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

heic_files = sorted(SOURCE_DIR.glob("*.HEIC"))
print(f"找到 {len(heic_files)} 个 HEIC 文件\n")

for heic_path in heic_files:
    jpg_name = heic_path.stem + ".jpg"
    jpg_path = OUTPUT_DIR / jpg_name
    print(f"转换: {heic_path.name} -> {jpg_name}")

    img = Image.open(heic_path)
    # HEIC 通常有 RGBA → JPEG 不支持透明通道, 转 RGB
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(jpg_path, "JPEG", quality=JPEG_QUALITY)
    size_kb = jpg_path.stat().st_size / 1024
    print(f"  完成: {jpg_path} ({img.size[0]}x{img.size[1]}, {size_kb:.1f} KB)")

print(f"\n全部 {len(heic_files)} 个文件已转换到 {OUTPUT_DIR}")
