# Statistical Chart Recipes, Sizing Calibration & LaTeX `subcaption` Patterns

This reference accompanies [mpl_publication_template.py](../scripts/mpl_publication_template.py) for Category B quantitative figures.

---

## 1. The `1.0x` Scale Principle: Calibrating `figsize` to LaTeX Width

A common mistake in multi-panel figures is giving `(a)` `figsize=(6, 4)` and `(b)` `figsize=(3.5, 4)`, then scaling both to `0.48\textwidth` in LaTeX—causing `(a)`'s text to shrink to half the size of `(b)`'s!

**Rule**: Set `figsize=(width_in, height_in)` in Python to match the **exact physical width (in inches)** the figure or subfigure will occupy on the compiled page. Then `\includegraphics[width=\linewidth]{...}` scales at `~1.0x`, guaranteeing uniform `8.0–9.5 pt` typography across the entire paper.

| Target Manuscript Slot | Typical Physical Width | Recommended `figsize` (inches) | Base Font Size |
| :--- | :--- | :--- | :--- |
| **Two-column template, single-column figure** (`\columnwidth`) | `3.35–3.50 in` | `(3.45, 2.00–2.65)` | `8.5–9.0 pt` |
| **Two-column template, 2 subfigures side-by-side in 1 column** (`0.485\columnwidth`) | `1.62–1.70 in` | `(1.68, 1.55–1.85)` | `7.8–8.4 pt` |
| **Two-column template, 2 subfigures across full page** (`0.485\textwidth`) | `3.35–3.48 in` | `(3.42, 2.10–2.55)` | `8.5–9.0 pt` |
| **Two-column template, 3 subfigures across full page** (`0.318\textwidth`) | `2.20–2.30 in` | `(2.26, 1.85–2.20)` | `8.2–8.8 pt` |
| **Two-column template, 4 subfigures across full page** (`0.238\textwidth`) | `1.65–1.72 in` | `(1.70, 1.60–1.90)` | `7.8–8.3 pt` |
| **Single-column template / thesis** (`\textwidth` $\approx 5.5\text{ in}$) | `5.20–5.60 in` | `(5.20, 2.60–3.20)` or `2x (2.55, 2.10)` | `9.0–9.5 pt` |

> **Tip**: Because `save_zero_margin_pdf()` crops outer whitespace tightly (`bbox_inches="tight"`, `0 pt` margin), keep left y-tick label lengths roughly consistent across side-by-side panels or adjust `figsize` proportionally so plot boxes align cleanly.

---

## 2. Chart-Type Selection & Precision Detailing

### 2.1 Horizontal Bar, Stacked Bar & Lollipop Charts
- **When to use**: Ranking categories, ablation deltas, or part-to-whole breakdowns—especially whenever category labels exceed 6–8 characters (**never tilt x-axis labels at 45° when a horizontal bar chart reads horizontally at 0°**).
- **Precision rules**:
  - Order rows intentionally (descending by total/metric, or canonical stage order—never arbitrary alphabetical order unless lookup-oriented).
  - Center every inline count/percentage optically with `va="center_baseline"`.
  - **Zero swallowed segments**: Never hide small non-zero segments (`1`, `2`, `1.5%`); print them inline on high-contrast fills or attach a clean micro-leader callout.
  - **Explicit zero**: Draw a subtle baseline marker + `0` text for zero-valued categories.

### 2.2 Dumbbell (Cleveland Dot) & Slope Charts
- **When to use**: Paired comparisons (e.g., *Without X* vs. *With X*, *Default* vs. *Calibrated*, *Precision* vs. *Recall* across benchmarks). Far cleaner and higher data-to-ink ratio than paired bar clusters.
- **Precision rules**:
  - Connect paired points with a subtle neutral/tinted bridge (`linewidth=1.8`, `zorder=2`) and plot crisp markers (`s=42–55`, `zorder=4`) in two contrasting hues.
  - Place numeric labels to the left of the minimum dot and right of the maximum dot (`va="center_baseline"`) so labels never collide with the connecting bridge.

### 2.3 Multi-Series Line, Sensitivity & Pareto Frontier Plots
- **When to use**: Hyperparameter sweeps, scaling laws, training/convergence trajectories, or accuracy-latency trade-offs.
- **Precision rules**:
  - Redundantly encode series with **hue + marker shape + linestyle** (`-o`, `--s`, `-.^`, `:D`) for grayscale print legibility.
  - Render variance/confidence intervals as borderless translucent bands (`ax.fill_between(x, lo, hi, color=c, alpha=0.14, linewidth=0)`).
  - Highlight Pareto-optimal frontiers with a crisp step/curve line and subtle reference annotations rather than cluttered arrows on every point.

### 2.4 Distributions (Raincloud, Violin/Box + Jitter, ECDF)
- **When to use**: Latency distributions, per-instance score spreads, or skewed empirical measurements where mean $\pm$ std misleads.
- **Precision rules**:
  - Combine summary quartiles (compact boxplot or median marker) with underlying density or jittered raw observations (`alpha=0.4`, `edgecolor="none"`).
  - Annotate sample size (`n = ...`) cleanly along the axis or legend.

### 2.5 Annotated Heatmaps & Confusion Matrices
- **When to use**: Pairwise interactions, confusion matrices, hyperparameter 2D grids, or cross-setting transfer matrices.
- **Precision rules**:
  - Use perceptually uniform sequential palettes (single-hue slate-to-cobalt or viridis/cividis variants) for magnitude, and diverging palettes (`#2563EB` <-> `#F8FAFC` <-> `#DC2626`) centered strictly at `0` (`TwoSlopeNorm(vcenter=0)`) for signed deltas.
  - Center every cell value with `ha="center", va="center_baseline"`, switching dynamically between `#FFFFFF` and `#111111` via `pick_readable_text_color()` so neither dark nor light cells lose contrast.

### 2.6 Set Overlap (Venn vs. UpSet)
- **When to use**: Phenomenon co-occurrence, bug/feature overlap across tools, or dataset coverage intersections.
- **Precision rules**:
  - Use geometric Venn circles **only for 2 or 3 sets**, routing leader lines to narrow lens regions so counts never touch circle boundaries.
  - For **4 or more sets**, always draw an **UpSet plot** (dot-matrix intersection indicator + marginal bar counts).

---

## 3. Curated $\le 3$-Hue Palettes for Cross-Figure Variety

Keep neutral tokens fixed across the entire manuscript (`#111111` ink, `#64748B` spines, `#E2E8F0` grid), and rotate among these accent triads across successive figures:

| Palette ID | Primary Accent | Secondary Contrast | Tertiary / Highlight | Best Suited For |
| :--- | :--- | :--- | :--- | :--- |
| **Set 1: Cobalt / Amber / Teal** | `#2563EB` | `#F59E0B` | `#0D9488` | Stacked breakdowns, primary vs. secondary comparisons |
| **Set 2: Indigo / Coral / Emerald** | `#4F46E5` | `#EA580C` | `#059669` | Paired dumbbell gaps, baseline vs. proposed trajectories |
| **Set 3: Sky-Blue / Ochre / Navy** | `#0284C7` | `#D97706` | `#1E3A8A` | Multi-tier hierarchical or 3-stage proportions |
| **Set 4: Teal / Rose / Slate** | `#0F766E` | `#E11D48` | `#334155` | Pass vs. failure rates, error/ablation sensitivity |
| **Set 5: Violet / Amber / Cyan** | `#6D28D9` | `#D97706` | `#0891B2` | Temporal emergence, multi-group distributions |

---

## 4. LaTeX Layout & `subcaption` Integration Patterns

Always load `\usepackage{graphicx}` and `\usepackage{subcaption}` in the preamble. Export every subfigure **without** internal `(a)`, `(b)` titles so `\caption{...}` inside `subfigure` handles numbering, cross-referencing (`\ref{fig:exp_a}`), and bottom alignment uniformly.

### 4.1 Single-Column Standalone Figure (Preferred Default in Two-Column Papers)
```latex
\begin{figure}[!t]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig_ablation.pdf}
  \caption{Throughput gain across optimization configurations. Compile-time and runtime contributions are shown separately alongside combined totals.}
  \label{fig:ablation}
\end{figure}
```

### 4.2 Single-Column Stacked Two-Panel Figure (Compact Vertical Pair)
```latex
\begin{figure}[!t]
  \centering
  \begin{subfigure}[b]{\columnwidth}
    \centering
    \includegraphics[width=\linewidth]{figures/fig_sensitivity_a.pdf}
    \caption{Latency distribution across batch sizes.}
    \label{fig:sensitivity_a}
  \end{subfigure}
  \vspace{4pt}

  \begin{subfigure}[b]{\columnwidth}
    \centering
    \includegraphics[width=\linewidth]{figures/fig_sensitivity_b.pdf}
    \caption{Peak memory footprint under identical workloads.}
    \label{fig:sensitivity_b}
  \end{subfigure}
  \caption{Sensitivity of runtime latency and memory footprint to batch size.}
  \label{fig:sensitivity}
\end{figure}
```

### 4.3 Double-Column Multi-Panel Figure (Reserved for 3+ Horizontal Panels or Wide Architectures)
```latex
\begin{figure*}[!t]
  \centering
  \begin{subfigure}[b]{0.32\textwidth}
    \centering
    \includegraphics[width=\linewidth]{figures/fig_bench_a.pdf}
    \caption{Accuracy vs.\ parameter budget.}
    \label{fig:bench_a}
  \end{subfigure}\hfill
  \begin{subfigure}[b]{0.32\textwidth}
    \centering
    \includegraphics[width=\linewidth]{figures/fig_bench_b.pdf}
    \caption{Cross-setting generalization gap.}
    \label{fig:bench_b}
  \end{subfigure}\hfill
  \begin{subfigure}[b]{0.32\textwidth}
    \centering
    \includegraphics[width=\linewidth]{figures/fig_bench_c.pdf}
    \caption{End-to-end inference latency.}
    \label{fig:bench_c}
  \end{subfigure}
  \caption{Comprehensive multi-dimensional evaluation across resource, generalization, and latency axes.}
  \label{fig:bench_overview}
\end{figure*}
```
