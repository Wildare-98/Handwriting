# Handwriting Batch Renderer v1.1 参考手册

本工具将 `.txt` 文本文件渲染为 A4 手写体 PNG 页面及合并 PDF。
需要用户自行提供手写字体（TTF/OTF/TTC），工具不内置任何字体。

> v1.1 — Pyarmor 加密版本，要求 Python 3.13 (64-bit, Windows)，已更新 License 服务器地址。

---

## 依赖

```bash
pip install Pillow reportlab
# 可选：numpy（用于高斯噪声和晕影效果）
pip install numpy
```

---

## 基本用法

```bash
# 显式指定字体和输出目录
python handwriting.py --input myfile.txt --font my-font.ttf --out output_dir

# 使用预设文件（预设中可含字体路径，无需每次指定）
python handwriting.py --input myfile.txt --preset presets/default.json

# Preview 模式：免 License，但输出页带 "www.wildareplanet.cloud" 水印
python handwriting.py --input myfile.txt --font my-font.ttf --preview
```

---

## License 管理

License 按每千字符计费——一份 2500 字的文档消耗 3 次调用，500 字消耗 1 次。

验证已内置于渲染流程，正常渲染时自动检查。如遇 License 相关错误，脚本会以 `[License]` 前缀输出错误信息。

**首次激活：**
```bash
python handwriting.py --license-setup YOUR-LICENSE-KEY
```

**查询余量（不消耗调用次数）：**
```bash
python handwriting.py --license-info
```

**常见 License 错误：**

| 错误信息 | 原因 |
|----------|------|
| `未设置 License Key` | 尚未激活，需运行 `--license-setup` |
| `无效的 License Key` | Key 错误或已失效 |
| `调用次数已用完` | 配额耗尽，需购买更多 |
| `无法连接服务器` | 网络不通，稍后重试 |

---

## 文本格式规则

- 普通换行符原样保留于输出中。
- 长行自动在右侧边距处换行，无需手动断行。
- 换页符 `\f` 强制从新页开始渲染。
- 输入文件编码支持 UTF-8 和 GBK/GB18030。

---

## 输出

每次渲染在输出目录下生成：
- `page-001.png`、`page-002.png`… — 逐页 PNG
- `handwriting.pdf` — 所有页面的合并 PDF

---

## 预设文件（Presets）

预设文件为 JSON 格式，用于固化常用参数，避免每次手动指定。

CLI 传入的参数会覆盖预设中的同名设置。

```json
{
    "font": "my-handwriting-font.ttf",
    "paper": "white",
    "font_size": 80,
    "line_height": 90,
    "mistake_chance": 0
}
```

> 预设中 `font` 路径相对于运行命令时的**当前工作目录**，而非预设文件所在位置。

---

## 完整参数列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | PATH | — | 输入 `.txt` 文件（UTF-8 / GBK） |
| `--font` | PATH | — | 手写字体文件（TTF/OTF/TTC），**必填**；也可经由 preset 设置 |
| `--out` | PATH | `output` | 输出目录 |
| `--paper` | STYLE | `white` | 纸张样式：`white` / `plain` / `lined` / `grid` |
| `--ink` | HEX | `#000000` | 墨水颜色 |
| `--seed` | INT | 随机 | 固定随机种子，保证每次渲染效果一致 |
| `--preset` | PATH | — | JSON 预设文件 |
| `--preview` | — | 关 | 免 License 预览，输出带水印 |
| `--license-setup` | KEY | — | 激活 License Key |
| `--license-info` | — | — | 查询 License 余量 |
| `--margin` | INT | 220 | 页边距，单位 px |
| `--font-size` | INT | 80 | 基础字号，单位 px |
| `--line-height` | INT | 90 | 行高，单位 px |
| `--wrap-safety` | INT | 80 | 右侧换行安全间距，单位 px |
| `--font-size-jitter` | FLOAT | 0.025 | 字号随机抖动比例 |
| `--line-y-jitter` | FLOAT | 3.0 | 整行垂直随机偏移，单位 px |
| `--char-y-jitter` | FLOAT | 5.0 | 单字符垂直随机偏移，单位 px |
| `--char-x-jitter` | FLOAT | 0.8 | CJK 字符水平随机偏移，单位 px |
| `--latin-y-jitter` | FLOAT | 1.6 | 拉丁字符垂直随机偏移，单位 px |
| `--latin-x-jitter` | FLOAT | 0.35 | 拉丁字符水平随机偏移，单位 px |
| `--char-spacing-min` | FLOAT | -10.5 | 字符间距下限，单位 px |
| `--char-spacing-max` | FLOAT | -4.0 | 字符间距上限，单位 px |
| `--punct-spacing-min` | FLOAT | -24.0 | 标点间距下限，单位 px |
| `--punct-spacing-max` | FLOAT | -15.0 | 标点间距上限，单位 px |
| `--colon-spacing-min` | FLOAT | -8.0 | 冒号间距下限，单位 px |
| `--colon-spacing-max` | FLOAT | 4.0 | 冒号间距上限，单位 px |
| `--baseline-drift-min` | FLOAT | -0.8 | 基线漂移下限，单位 px |
| `--baseline-drift-max` | FLOAT | 0.8 | 基线漂移上限，单位 px |
| `--baseline-drift-limit` | FLOAT | 14.0 | 基线累积漂移最大值，单位 px |
| `--baseline-drift-recovery` | FLOAT | 0.35 | 漂移恢复速率 |
| `--baseline-shock-chance` | FLOAT | 0.16 | 基线突然跳变概率 |
| `--baseline-shock-min` | FLOAT | 5.0 | 跳变幅度下限，单位 px |
| `--baseline-shock-max` | FLOAT | 11.0 | 跳变幅度上限，单位 px |
| `--baseline-shock-cooldown` | INT | 2 | 跳变冷却行数 |
| `--line-slope-chance` | FLOAT | 0.5 | 行倾斜发生概率 |
| `--line-slope-min` | FLOAT | -35.0 | 倾斜量下限，单位 px |
| `--line-slope-max` | FLOAT | 35.0 | 倾斜量上限，单位 px |
| `--line-slope-recovery` | FLOAT | 0.85 | 倾斜恢复速率 |
| `--line-slope-limit` | FLOAT | 40.0 | 倾斜累积最大值，单位 px |
| `--mistake-chance` | FLOAT | 0 | 模拟涂改错误概率（0 = 不模拟） |
| `--mistake-crossout-lines` | INT | 15 | 涂改时划除笔画数 |
| `--mistake-crossout-thickness` | FLOAT | 4.0 | 划除笔画粗细百分比 |

---

## 加密版本说明

工具使用 Pyarmor 加密，`.pyd` 解密运行时绑定 **Python 3.13 (64-bit, Windows)**。使用其他 Python 版本将无法加载解密模块，直接报错。
