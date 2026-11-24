---
name: scientific-plotting
description: >-
  Publication-grade scientific figure design, generation, and LaTeX layout standards
  for academic papers, theses, and technical reports. Use this skill whenever creating,
  redesigning, or auditing research figures—explicitly distinguishing conceptual
  framework/architecture/flow diagrams (draw.io / vector diagrams) from quantitative
  data charts (Python Matplotlib scripts)—or integrating figures and subfigures into
  single-column or double-column manuscripts (科研绘图、论文架构图、方法流程图、实验数据图表与排版优化).
---

# Scientific Plotting & Publication Figure Specification

This skill defines universal visual, structural, programmatic, and typesetting rules for publication-ready academic figures across disciplines and templates (IEEE, ACM, Springer, Elsevier, NeurIPS/ICML/CVPR, theses, and technical reports).

---

## 1. Fundamental Classification: Never Mix the Two Figure Families

Every research figure belongs to one of two distinct families with separate toolchains and visual rules. **Never combine a conceptual diagram and a statistical data chart inside the same composite canvas.**

| Dimension | Category A: Framework, Architecture & Flow Diagrams | Category B: Data Visualization & Statistical Charts |
| :--- | :--- | :--- |
| **Communicative Goal** | Qualitative structure: system architectures, method pipelines, taxonomies, screening funnels, decision workflows | Quantitative evidence: experimental comparisons, ablations, distributions, parameter sensitivity, scaling trends, set overlaps |
| **Primary Toolchain** | Editable vector diagramming (`.drawio` -> cropped vector `.pdf`, or clean SVG/TikZ) | Reproducible Python script (`matplotlib` -> cropped vector `.pdf`) |
| **Source Archival** | `<fig_name>.drawio` stored alongside `<fig_name>.pdf` in `figures/` | One standalone `<fig_name>.py` stored alongside `<fig_name>.pdf` in `figures/` |
| **Multi-Panel Rule** | Unified conceptual canvas structured by clean visual zones ($\le 2$ container layers) | Split every panel into its own zero-margin PDF (`figXa.pdf`, `figXb.pdf`) and assemble via LaTeX `subcaption` |

---

## 2. Universal Design Standards (Applicable to All Figures)

### 2.1 Self-Contained Readability & Narrative Integrity
1. **Stand-Alone Comprehension**: A reader inspecting **only the figure and its caption** must grasp the core mechanism or quantitative takeaway without hunting through body text to decode symbols.
2. **Ban Cryptic Shorthand & Prose Walls Simultaneously**:
   - Do **not** label nodes or axes with unexplained symbols (`M_1`, `C_3`, `\phi`) or ad-hoc abbreviations.
   - Do **not** paste multi-line explanatory sentences inside figure boxes; use concise, self-explanatory phrases and place methodological details in the caption or body.
3. **Overview-First Ordering**: Introduce a high-level **System / Paper Overview** figure early in the manuscript to establish the global mental model before presenting zoomed-in module or step-level figures.
4. **No Hindsight Bias or Mechanical Chores**:
   - Do **not** hardcode post-hoc outcomes as a priori workflow rules (e.g., write *"Iterative refinement until convergence"* rather than *"3-round refinement"* when `3` was an empirical outcome; annotate empirical counts as instance badges instead).
   - Model **conceptual scientific/engineering operations**, never mechanical file chores (e.g., never draw *"Read files"* or *"Save CSV"* as pipeline stages).

### 2.2 Color System & Hue Budget
1. **Modern Slate Neutrals + Crisp Accents**:
   - Primary text: deep near-black (`#111111` or `#1E293B`), never washed-out gray.
   - Structural strokes, axes, and secondary text: slate tones (`#475569`, `#64748B`, `#94A3B8`) and subtle grid/fill neutrals (`#E2E8F0`, `#F8FAFC`).
   - Avoid harsh uncalibrated primaries (`#FF0000`, `#00FF00`, `#0000FF`).
2. **Strict Hue-Family Cap ($\le 3$ Default, $\le 5$ Hard Ceiling)**:
   - Use **at most 3 distinct hue families** per figure (light/dark shades of one hue count as 1 hue family). Even in dense multi-category charts, **never exceed 5 hue families**.
3. **Cross-Figure Palette Rotation within a Unified Style**:
   - Across a multi-figure paper, keep stroke weights, corner radii, and typography identical, **but rotate accent hue pairings across figures** (e.g., Cobalt + Amber in Fig. 2, Teal + Indigo in Fig. 3, Slate-Blue + Coral in Fig. 4) to prevent visual monotony.
4. **Luminance Contrast & Print Safety**:
   - Never place white text over pale/pastel fills; use medium-to-deep fills for white text or switch to dark `#111111` text on light fills. Pair color distinctions with line styles or marker shapes in multi-series curves.

### 2.3 Typography, Font Weights & Sizing
1. **Calibrate to Final Rendered Size**: Design figure dimensions against the target LaTeX width (`\columnwidth` or `\textwidth`) so rendered text lands at **`7.5–9.5 pt` on the compiled page** (never `< 6.5 pt` microscopic or `> 11 pt` oversized).
2. **Restrained Font Weights**:
   - **Never bold everything.** Reserve semi-bold (`600`) strictly for top-level zone/stage headers.
   - Keep node labels, axis labels, tick labels, legends, and numeric annotations in **regular weight (`400`)** for a crisp, modern appearance.
3. **Cross-Platform Font Stack**:
   - Use clean sans-serif fonts with safe OS fallbacks (e.g., `Avenir Next` / `Helvetica Neue` / `Inter` / `Arial` / `Liberation Sans` / `DejaVu Sans`; for Chinese/bilingual figures add `PingFang SC` / `Noto Sans CJK SC` / `Source Han Sans SC` / `Microsoft YaHei`). Optionally pair a smooth rounded or tabular-numeral sans-serif for callout numbers.
   - Embed TrueType outlines (`pdf.fonttype = 42`, `ps.fonttype = 42`)—never Type 3 bitmap fonts.

### 2.4 Space Utilization & Zero-Margin Cropping
- Eliminate dead whitespace inside and around the canvas.
- Export every final PDF as a **vector graphic cropped to `0 pt` outer margins** on all four sides (`pdfcrop --margins 0` or tight SVG/PDF bounds) so LaTeX controls all layout spacing and figures utilize 100% of allocated column width.

---

## 3. Category A Specification: Framework, Architecture & Flow Diagrams

For detailed `.drawio` layout geometry, container rules, and CLI export recipes, read [drawio_architecture_guide.md](./references/drawio_architecture_guide.md).

1. **Co-Locate Editable Source & Respect User Edits**:
   - Store `<fig_name>.drawio` right beside `<fig_name>.pdf` in `figures/`.
   - **Critical**: Before modifying an existing `.drawio` file, inspect its current XML/timestamp. If the user manually refined positions, colors, or wording in `draw.io`, preserve their layout and edit incrementally—never overwrite from an older generator script.
2. **Communicate with Semantic Icons + Shapes + Arrows, Not Text Cards**:
   - **Ban "Bold Title + Small Subtext" Cards**: Nodes must hold concise, self-explanatory titles—never a bold header followed by 2–3 lines of tiny gray explanation.
   - **Ban Middle-Dot / Slash Packing (`A · B · C`)**: Never cram multiple distinct items or sub-steps into one box separated by `·` or `/`. Split distinct concepts into separate visual shapes/nodes.
   - **Every Icon Must Earn Its Place**: Each icon must accurately depict its concept (e.g., database, filter, tree, neural layer, clock). Never copy-paste decorative/mismatched icons, and never force `vs.` comparison layouts unless a genuine conceptual contrast exists.
3. **Strict Container Nesting Limit (`< 3` Layers — Max 2 Levels)**:
   - Avoid unnecessary wrapper boxes. Use outer stage/layer containers only when grouping meaningful phases, and **never nest rectangles more than 2 levels deep** (Outer Zone -> Component Node; no 3rd inner box).
   - Every count badge, tag, or callout must visually belong to a specific node or arrow—never leave floating numbers with ambiguous attachment.
4. **Connector Hygiene & Decision Completeness**:
   - Align nodes on strict horizontal and vertical grids so connectors remain **straight lines** or use **at most one clean orthogonal bend**, with zero line crossings or awkward detours.
   - Screening, routing, or branching diagrams must explicitly show **decision criteria and branch outcomes** (e.g., why items pass vs. get filtered out), not bare stage names.
5. **Anti-Clipping Padding Before Tight Crop**:
   - Ensure text boxes and embedded SVG snippets leave vertical headroom for font ascenders/descenders before running `draw.io --crop` or `pdfcrop --margins 0` so top/edge glyphs are never sliced off.

---

## 4. Category B Specification: Data Visualization & Statistical Charts

Use the reusable cross-platform script [mpl_publication_template.py](./scripts/mpl_publication_template.py) and consult [chart_types_and_latex_patterns.md](./references/chart_types_and_latex_patterns.md) for chart-type recipes and palettes.

1. **1-to-1 Standalone Script Co-Location**:
   - Every exported chart PDF must have **exactly one standalone, self-contained `.py` script** in the same directory (`figures/fig_ablation_a.py` -> `figures/fig_ablation_a.pdf`).
   - Hardcode or cleanly load verified summary data inside the script with deterministic styling so any figure can be regenerated independently in one command.
2. **Decompose Multi-Panel Figures into Standalone Subfigure PDFs**:
   - Do **not** assemble `(a)`, `(b)`, `(c)` multi-panel grids inside a single monolithic `matplotlib` figure with baked-in panel titles.
   - Export each panel as its own zero-margin PDF (`fig_exp_a.pdf`, `fig_exp_b.pdf`) and compose them in LaTeX with `\usepackage{subcaption}` (`\begin{subfigure}[b]{...}\caption{...}\end{subfigure}`), placing `(a)`, `(b)` captions cleanly underneath each panel.
3. **Frameless, Minimalist Chart Geometry**:
   - Hide top and right spines (`ax.spines["top"].set_visible(False)`, `ax.spines["right"].set_visible(False)`).
   - Style left/bottom spines in subtle slate (`0.8–0.9 pt`) bounded to the data range (`set_bounds`), with light gridlines behind data (`zorder=1`).
   - **Never** draw outer rectangular borders around charts, **never** put stroke outlines around value text (`edgecolor="none"`), and keep legends frameless (`frameon=False`) and compact above or inside open chart space.
4. **Optical Vertical Centering of Digits (`va="center_baseline"`)**:
   - **Bug to Avoid**: Matplotlib's `va="center"` centers the full `[descent, ascent]` font bounding box. Because digits (`0–9`) have zero descenders below the baseline, `va="center"` visually pushes numbers **upward off-center** inside horizontal bars, stacked segments, badges, and heatmap cells!
   - **Mandatory Fix**: Always use `va="center_baseline"` for numeric and single-line labels inside bars, pills, heatmap cells, and horizontal tick alignments. If digits look vertically cramped, increase bar thickness slightly or reduce label font size by `0.5–1.0 pt`. On rounded bar caps with narrow width, nudge the label slightly inward away from the curved corner.
5. **Anti-Swallowing Rule for Small Non-Zero Values & Explicit Zeros**:
   - **Never silently drop small non-zero values** via high width cutoffs (e.g., `if width >= 6:` hiding segments of size `1`, `2`, or `3` so visible segment labels fail to sum to the bar total!).
   - **Solutions**:
     1. Use medium-deep segment fills with high luminance contrast and a slightly smaller crisp font (`7.5–8.5 pt`) so narrow non-zero segments still print their exact values inside the bar.
     2. If a non-zero segment is physically narrower than a single glyph (`< 2%` of axis span), attach a clean offset callout/leader annotation rather than omitting the number.
     3. Render true `0` bars explicitly (e.g., a subtle baseline dot + `0` / `0 (0.0%)` label) to distinguish measured zero from missing data.

---

## 5. LaTeX Sizing, Column Choice & Mandatory Visual QA

### 5.1 Single-Column (`figure`) vs. Double-Column (`figure*`) Selection
In two-column templates (`IEEEtran`, two-column `acmart`, etc.), **do not default every figure to `\begin{figure*}`**:
- **Use Single-Column `\begin{figure}[!t]` (`\columnwidth`)** for single-panel charts, 2-panel vertical stacks, compact 2-panel side-by-side plots, and narrow vertical flowcharts. Single-column floats stay closer to their in-text citations and preserve reading flow.
- **Reserve Double-Column `\begin{figure*}[!t]` (`\textwidth`)** strictly for wide multi-stage system architectures, 3+ horizontal subfigures, or dense wide comparisons that would shrink below `7 pt` text in a single column.

### 5.2 Mandatory Post-Render Visual Inspection Checklist
Never declare a figure or manuscript layout finished based solely on exit code `0`. Convert both the standalone PDF (`pdftoppm -png -r 300 fig.pdf preview`) and the compiled manuscript pages (`pdftoppm -png -r 200 main.pdf page`) and visually inspect them with `read_file` against all five gates:
1. **Zero Clipping**: Are top ascenders, rightmost labels, bottom axis titles, and leftmost ticks completely intact with `0 pt` tight crop?
2. **Optical Centering**: Does every number inside horizontal bars, stacked segments, badges, and cells sit dead-center vertically (no upward drift)?
3. **Zero Swallowed Values**: Is every non-zero segment/point accounted for, and do stacked segment labels sum identically to totals?
4. **Scale Harmony**: On the full compiled manuscript page, are figure fonts balanced against body prose (`~80%–100%` of body text size) and consistent across sibling subfigures?
5. **Float Hygiene**: Do floats avoid colliding on the same page awkwardly or stranding orphan headings/whitespace gaps?
