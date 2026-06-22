"""
PDF 合并工具
支持将多个 PDF 文件合并为一个 PDF。
用法:
  python merge_pdf.py file1.pdf file2.pdf ... -o merged.pdf     # 指定文件合并
  python merge_pdf.py -d ./目录 -o merged.pdf                    # 合并目录下所有 PDF
  python merge_pdf.py -d ./目录 -p "前缀_" -o merged.pdf         # 合并目录下指定前缀的 PDF
"""

import argparse
import os
import sys
from pathlib import Path
from pypdf import PdfWriter

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def natural_sort_key(name: str) -> tuple:
    """按自然顺序排序（如 file2.pdf 排在 file10.pdf 前面）"""
    import re
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', name)]


def collect_pdfs_from_dir(directory: str, prefix: str = None, recursive: bool = False) -> list[str]:
    """从目录收集所有 PDF 文件，按自然顺序排序"""
    pdf_files = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            dirs.sort()  # 保证遍历顺序一致
            for f in sorted(files):
                if f.lower().endswith('.pdf'):
                    if prefix is None or f.startswith(prefix):
                        pdf_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(directory):
            if f.lower().endswith('.pdf'):
                if prefix is None or f.startswith(prefix):
                    pdf_files.append(os.path.join(directory, f))
        pdf_files.sort(key=lambda p: natural_sort_key(os.path.basename(p)))
    return pdf_files


def merge_pdfs(pdf_paths: list[str], output_path: str, base_dir: str = None) -> int:
    """
    合并 PDF 文件。
    返回合并后的总页数。
    """
    writer = PdfWriter()
    total_pages = 0

    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"[SKIP] 跳过不存在的文件: {pdf_path}")
            continue
        try:
            writer.append(pdf_path)
            # 获取页数
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            pages = len(reader.pages)
            total_pages += pages
            # 显示文件名（有 base_dir 时显示相对路径）
            if base_dir:
                display = os.path.relpath(pdf_path, base_dir)
            else:
                display = os.path.basename(pdf_path)
            print(f"  已添加: {display} ({pages} 页)")
        except Exception as e:
            print(f"[WARN] 无法读取文件 {pdf_path}: {e}")
            continue

    if total_pages == 0:
        print("错误: 没有成功添加任何 PDF 页面。")
        return 0

    writer.write(output_path)
    writer.close()
    return total_pages


def main():
    parser = argparse.ArgumentParser(
        description="将多个 PDF 文件合并为一个 PDF。",
        usage="python merge_pdf.py [文件列表...] [-d 目录] [-p 前缀] -o 输出文件"
    )
    parser.add_argument('files', nargs='*', help='要合并的 PDF 文件路径（可多个）')
    parser.add_argument('-d', '--dir', help='要合并的 PDF 所在目录')
    parser.add_argument('-p', '--prefix', default=None, help='文件名前缀过滤（仅与 -d 配合使用）')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归扫描子目录（仅与 -d 配合使用）')
    parser.add_argument('-o', '--output', required=True, help='输出 PDF 文件路径')

    args = parser.parse_args()

    # 收集 PDF 文件
    pdf_paths = list(args.files)

    if args.dir:
        dir_pdfs = collect_pdfs_from_dir(args.dir, args.prefix, args.recursive)
        pdf_paths.extend(dir_pdfs)
        base_dir = args.dir if args.recursive else None
    else:
        base_dir = None

    if not pdf_paths:
        print("错误: 未指定任何 PDF 文件。请提供文件名或使用 -d 指定目录。")
        print("示例: python merge_pdf.py a.pdf b.pdf -o output.pdf")
        print("示例: python merge_pdf.py -d ./儿科病例 -o 合并病例.pdf")
        sys.exit(1)

    # 去重并保持顺序
    seen = set()
    unique_paths = []
    for p in pdf_paths:
        abs_p = os.path.abspath(p)
        if abs_p not in seen:
            seen.add(abs_p)
            unique_paths.append(p)

    print(f"\n合并 {len(unique_paths)} 个文件 → {args.output}")
    print("-" * 40)

    total = merge_pdfs(unique_paths, args.output, base_dir)

    if total > 0:
        size = os.path.getsize(args.output)
        print("-" * 40)
        print(f"[OK] 合并完成: {total} 页, {size / 1024:.1f} KB -> {args.output}")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
