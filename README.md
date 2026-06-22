# real-handwriting

将文本文件渲染为真实手写体效果的 A4 PNG / PDF 文档。专为门诊病历等医疗文书设计，也适用于任何需要手写风格的文本渲染场景。

## 特性

- 基于用户提供的手写字体（TTF / OTF / TTC），不内置任何字体
- 字符级抖动：字号、间距、基线随机偏移，模拟真实手写的不规则感
- 行级特性：行倾斜、基线漂移、偶然冲击，避免机械排列
- 多种纸张样式：纯白、白底黑字、横线、网格
- 支持 UTF-8 和 GBK / GB18030 编码
- 单文件输入 → 多页 PNG + 合并 PDF 输出
- 可选 Preview 模式（带水印）用于评估效果

## 目录结构

```
real-handwriting/
├── SKILL.md                         # AI 技能入口文档
├── README.md                        # 本文件
├── assets/
│   └── 门诊病例模板.txt              # 门诊病历输出模板
├── references/
│   ├── filling-rules.md             # 18 项字段填充规则
│   └── handwriting-tool.md          # 手写渲染工具完整参数参考
└── tools/
    ├── convert_heic_to_jpg.py       # HEIC → JPG 批量转换
    ├── merge_pdf.py                 # 多 PDF 合并
    └── Handwritingv1.1/             # 手写渲染引擎（Pyarmor 加密）
        ├── handwriting.py           # 主程序
        ├── presets/default.json     # 默认渲染预设
        ├── examples/                # 示例文件
        └── pyarmor_runtime_000000/  # 解密运行时
```

## 环境要求

- **Python 3.13（64-bit，Windows）** — 渲染引擎使用 Pyarmor 加密，仅绑定此版本
- 依赖库：Pillow、reportlab（numpy 可选）

```bash
pip install Pillow reportlab
pip install numpy  # 可选，用于高斯噪声和晕影效果
```

## 快速开始

### 1. 准备字体

准备一个手写风格字体文件（TTF / OTF / TTC），如常见的硬笔书法字体。

### 2. 准备文本

创建一个 `.txt` 文件，内容为你希望渲染的文本。支持 UTF-8 和 GBK 编码。

### 3. 首次设置 License

```bash
python tools/Handwritingv1.1/handwriting.py --license-setup YOUR-KEY
```

### 4. 渲染

```bash
python tools/Handwritingv1.1/handwriting.py \
    --input myfile.txt \
    --font my-handwriting-font.ttf \
    --out output \
    --paper white \
    --seed 42
```

输出目录将包含逐页 PNG 和合并后的 PDF。

### Preview 模式（免 License，带水印）

```bash
python tools/Handwritingv1.1/handwriting.py \
    --input myfile.txt \
    --font my-handwriting-font.ttf \
    --preview
```

### 使用预设文件

可以将常用参数保存为 JSON 预设，避免每次重复输入：

```bash
python tools/Handwritingv1.1/handwriting.py \
    --input myfile.txt \
    --preset tools/Handwritingv1.1/presets/default.json
```

## 自定义渲染参数

完整参数列表见 `references/handwriting-tool.md`，涵盖字体抖动、行倾斜、基线漂移、字间距、涂改模拟等 40+ 个可调参数。

## 辅助工具

| 工具 | 用途 |
|------|------|
| `tools/convert_heic_to_jpg.py` | 将 iPhone 拍摄的 HEIC 病例图片批量转为 JPG |
| `tools/merge_pdf.py` | 将多个手写 PDF 合并为单个文件 |

## License

手写渲染引擎按每千字符计费，Preview 模式免费但输出带水印。

---

## 免责声明

> **重要警示**：本技能仅提供手写体渲染的技术模拟，不内置任何字体文件，用户需自行提供合法获取的手写字体。

- **不参与**：本技能不参与任何形式的假冒文书、伪造签名、仿制处方等违法行为。
- **不内置**：本技能不内置任何第三方字体，不存在字体版权侵权行为。
- **不用于**：本技能不用于任何欺诈、造假、以假乱真之目的。
- **不上传**：本技能不上传任何数据，所有处理均在本地完成，不构成任何隐私侵犯。
- **责任**：使用者应确保其对所渲染文档拥有合法权利，并在法律法规允许的范围内使用本技能。对于任何违法或不当使用所造成的后果，技能提供方不承担任何责任。
