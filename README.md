# Scientific Plotting (`scientific-plotting`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

[中文说明](#中文说明) | [English](#english)

---

## 中文说明

面向学术论文、学位论文与技术报告的**出版级科研绘图设计、生成与 LaTeX 排版规范**（Agent Skill）。适用于 IEEE、ACM、Springer、Elsevier、NeurIPS / ICML / CVPR 等主流单栏与双栏模板。

### 核心特性

1. **严格区分两类图形家族（禁止混排）**
   - **A 类：框架图、架构图与流程图**：表达定性结构（系统架构、方法流程、分类体系、筛选漏斗、决策工作流），采用可编辑矢量工具（`.drawio` -> 零边距矢量 `.pdf`）。
   - **B 类：数据可视化与统计图表**：表达定量证据（实验对比、消融实验、分布特征、参数敏感性、帕累托前沿等），采用可复现的独立 Python 脚本（`matplotlib` -> 零边距矢量 `.pdf`）。
2. **现代出版级视觉标准**
   - **色彩预算**：固定现代石板中性色（`#111111` 主文字、`#64748B` 坐标轴、`#E2E8F0` 网格），单图色相族默认 $\le 3$（上限 $\le 5$），提供 5 套预设色板在同篇论文中轮换使用，避免视觉单调。
   - **字体与字重**：按 LaTeX 实际物理宽度 `1.0x` 比例定稿（成图字号落在 `7.5–9.5 pt`），克制字重（仅顶层区域标题用半粗体 `600`，其余正文字重 `400`），嵌入 TrueType 字体（`pdf.fonttype = 42`），支持跨平台拉丁与中文字体自动回退。
   - **零边距裁切**：导出均为四周 `0 pt` 裁切的矢量 PDF，将排版间距完全交由 LaTeX 控制。
3. **规避科研绘图常见陷阱**
   - **架构图**：禁止"加粗标题 + 多行小字"文本卡片与 `A · B · C` 堆砌，容器嵌套严格 `< 3` 层（最多 2 层），保留用户对 `.drawio` 的手动修改，防止 SVG 顶部字形裁切。
   - **统计图**：一图一脚本同目录归档；多子图拆分为独立零边距 PDF 再由 LaTeX `subcaption` 拼排；强制使用 `va="center_baseline"` 实现数字光学垂直居中；反吞值标注规则确保极小非零分段与显式零值均完整呈现。
4. **单双栏排版与视觉质检闭环**
   - 明确双栏模板下单栏 `figure` 与跨栏 `figure*` 的选用标准。
   - 强制要求将独立图 PDF 与编译后的论文页面转为高清 PNG 进行五项视觉验收（零裁切、光学居中、零吞值、字号协调、浮动体整洁）。

### 目录结构

```text
scientific-plotting/
├── LICENSE                                      # MIT 开源协议
├── README.md                                    # 中英双语项目说明
├── SKILL.md                                     # 核心规范与执行准则（Agent Skill 入口）
├── references/
│   ├── drawio_architecture_guide.md             # A 类：draw.io 架构图与流程图几何/配色/导出指南
│   └── chart_types_and_latex_patterns.md        # B 类：统计图选型、1.0x 尺寸标定、色板与 LaTeX subcaption 模板
└── scripts/
    └── mpl_publication_template.py              # 可复用出版级 Matplotlib 工具库与示例脚本
```

### 快速上手

#### 作为 Agent Skill 安装
将本仓库克隆到任意支持 Agent Skills 的 AI 助手的技能目录（`<your-skills-dir>`）中，在需要绘制或优化论文架构图、流程图、实验数据图表及 LaTeX 排版时即可自动触发或显式调用：

```bash
git clone git@github.com:HolgerZhang/scientific-plotting.git <your-skills-dir>/scientific-plotting
```

#### 运行示例图表脚本

依赖：`python3`、`matplotlib`（可选安装 `librsvg` 的 `rsvg-convert` 与 TeX Live 的 `pdfcrop` 以启用最佳矢量零边距裁切；未安装时自动回退至纯 Matplotlib TrueType PDF 导出）。

```bash
# 生成默认色板（cobalt_amber_teal）的示例零边距矢量 PDF
python3 scripts/mpl_publication_template.py --out demo_publication_chart.pdf

# 切换预设色板
python3 scripts/mpl_publication_template.py \
  --out demo_publication_chart.pdf \
  --palette indigo_coral_emerald
```

可选色板：`cobalt_amber_teal`、`indigo_coral_emerald`、`sky_ochre_navy`、`teal_rose_slate`、`violet_amber_cyan`。

### 开源协议

本项目基于 [MIT License](./LICENSE) 开源。

---

## English

Publication-grade **scientific figure design, generation, and LaTeX layout standards** packaged as an Agent Skill for academic papers, theses, and technical reports (IEEE, ACM, Springer, Elsevier, NeurIPS / ICML / CVPR, and single-/two-column templates).

### Key Features

1. **Strict Separation of Two Figure Families**
   - **Category A — Framework, Architecture & Flow Diagrams**: Qualitative structure (system architectures, method pipelines, taxonomies, screening funnels, decision workflows) authored in editable vector tools (`.drawio` -> zero-margin vector `.pdf`).
   - **Category B — Data Visualization & Statistical Charts**: Quantitative evidence (comparisons, ablations, distributions, sensitivity sweeps, Pareto frontiers) generated via reproducible standalone Python scripts (`matplotlib` -> zero-margin vector `.pdf`).
2. **Modern Publication Visual Standards**
   - **Color System & Hue Budget**: Fixed slate neutrals (`#111111` ink, `#64748B` axes, `#E2E8F0` gridlines) with a strict $\le 3$ hue-family default ($\le 5$ hard cap) and 5 curated accent palettes designed to rotate across figures in the same manuscript.
   - **Typography & Sizing**: Calibrated at `1.0x` scale to exact LaTeX physical widths so rendered text lands at `7.5–9.5 pt`, with restrained weights (`600` for top-level headers only, `400` regular elsewhere), embedded TrueType outlines (`pdf.fonttype = 42`), and cross-platform Latin + CJK font auto-detection.
   - **Zero-Margin Vector Output**: Every exported PDF is tightly cropped to `0 pt` outer margins on all sides so LaTeX maintains full control over layout spacing.
3. **Built-In Guards Against Common Pitfalls**
   - **Architecture Diagrams**: Bans prose-heavy "bold title + subtext" cards and `A · B · C` packing, enforces `< 3` container nesting layers (max 2 levels), preserves manual user edits in `.drawio` XML, and prevents top/edge SVG glyph clipping.
   - **Statistical Charts**: Enforces 1-to-1 co-located scripts, decomposes multi-panel figures into standalone subfigure PDFs assembled via LaTeX `subcaption`, mandates `va="center_baseline"` for optical vertical centering of digits, and prevents silent dropping of small non-zero segments or explicit zeros.
4. **LaTeX Float Discipline & Visual QA Gate**
   - Clear criteria for choosing single-column `figure` vs. full-width `figure*` in two-column manuscripts.
   - Mandatory post-render visual inspection workflow (`pdftoppm` -> PNG review) across five gates: zero clipping, optical centering, zero swallowed values, scale harmony, and float hygiene.

### Directory Structure

```text
scientific-plotting/
├── LICENSE                                      # MIT License
├── README.md                                    # Bilingual documentation (ZH / EN)
├── SKILL.md                                     # Core specification & Agent Skill entry point
├── references/
│   ├── drawio_architecture_guide.md             # Category A: draw.io layout, connectors, tokens & CLI export
│   └── chart_types_and_latex_patterns.md        # Category B: chart recipes, 1.0x sizing table, palettes & subcaption
└── scripts/
    └── mpl_publication_template.py              # Reusable publication-grade Matplotlib helper & CLI demo
```

### Quick Start

#### Install as an Agent Skill
Clone this repository into the skills directory (`<your-skills-dir>`) of any AI agent that supports Agent Skills. It activates automatically when designing, generating, or auditing academic figures and LaTeX figure layouts:

```bash
git clone git@github.com:HolgerZhang/scientific-plotting.git <your-skills-dir>/scientific-plotting
```

#### Run the Demo Chart Script

Requirements: `python3` and `matplotlib` (optionally `rsvg-convert` from `librsvg` and `pdfcrop` from TeX Live for optimal zero-margin cropping; automatically falls back to pure-Matplotlib TrueType PDF export if unavailable).

```bash
# Render a zero-margin vector PDF with the default palette (cobalt_amber_teal)
python3 scripts/mpl_publication_template.py --out demo_publication_chart.pdf

# Render with an alternative curated palette
python3 scripts/mpl_publication_template.py \
  --out demo_publication_chart.pdf \
  --palette indigo_coral_emerald
```

Available palettes: `cobalt_amber_teal`, `indigo_coral_emerald`, `sky_ochre_navy`, `teal_rose_slate`, `violet_amber_cyan`.

### License

This project is licensed under the [MIT License](./LICENSE).
