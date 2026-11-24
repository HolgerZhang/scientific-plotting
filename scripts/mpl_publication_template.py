#!/usr/bin/env python3
"""Universal publication-grade Matplotlib helper and standalone chart template.

Key features encoded in this module:
1. Cross-platform TrueType font auto-detection (Latin sans-serif + optional CJK
   + rounded numeric highlight font) with `pdf.fonttype = 42` (zero Type 3 fonts).
2. Curated <=3-hue modern scientific palettes for cross-figure variety without
   visual monotony, paired with automatic WCAG luminance text-contrast selection.
3. Clean frameless chart styling (top/right spines hidden, bounded slate axes,
   subtle background gridlines, frameless top legends).
4. Optical vertical centering (`va="center_baseline"`) and anti-swallowing stacked
   bar annotations (every non-zero segment is shown either inline or via a clean
   leader callout; true zeros render an explicit baseline dot).
5. Zero-margin vector PDF export (`rsvg-convert` + `pdfcrop --margins 0` when
   available, with automatic pure-Matplotlib TrueType PDF fallback).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Mapping, Sequence

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath

# ---------------------------------------------------------------------------
# 1. Neutral Tokens & <=3-Hue Palette Presets (Rotate Across Paper Figures)
# ---------------------------------------------------------------------------

NEUTRALS = {
    "ink": "#111111",          # Primary labels, ticks, callouts
    "ink_muted": "#475569",    # Secondary notes, units
    "spine": "#64748B",        # Left/bottom axis spines
    "tick_line": "#94A3B8",    # Subtle tick marks / leader lines
    "grid": "#E2E8F0",         # Background gridlines
    "surface": "#F8FAFC",      # Optional soft band / zebra tint
}

PALETTE_PRESETS: dict[str, tuple[str, str, str]] = {
    "cobalt_amber_teal": ("#2563EB", "#F59E0B", "#0D9488"),
    "indigo_coral_emerald": ("#4F46E5", "#EA580C", "#059669"),
    "sky_ochre_navy": ("#0284C7", "#D97706", "#1E3A8A"),
    "teal_rose_slate": ("#0F766E", "#E11D48", "#334155"),
    "violet_amber_cyan": ("#6D28D9", "#D97706", "#0891B2"),
}


def relative_luminance(hex_color: str) -> float:
    """Compute WCAG relative luminance for a `#RRGGBB` hex string."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return 0.0
    channels = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255.0
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def pick_readable_text_color(
    fill_hex: str,
    dark_ink: str = "#111111",
    light_ink: str = "#FFFFFF",
    threshold: float = 0.34,
) -> str:
    """Return crisp white text on medium/dark fills and near-black on pale fills."""
    return light_ink if relative_luminance(fill_hex) < threshold else dark_ink


# ---------------------------------------------------------------------------
# 2. Cross-Platform Font Detection & Matplotlib rcParams
# ---------------------------------------------------------------------------

LATIN_SANS_CANDIDATES = [
    "Avenir Next",
    "Helvetica Neue",
    "Inter",
    "Arial",
    "Liberation Sans",
    "DejaVu Sans",
]

CJK_SANS_CANDIDATES = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "Microsoft YaHei",
    "WenQuanYi Micro Hei",
]

ROUNDED_NUM_CANDIDATES = [
    "Avenir Next",
    "Helvetica Neue",
    "Inter",
    "Arial",
    "Liberation Sans",
    "DejaVu Sans",
]


def detect_installed_font(candidates: Sequence[str], default: str = "DejaVu Sans") -> str:
    """Return the first font family name present on the current OS."""
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return default


def configure_publication_rcparams(
    enable_cjk: bool = False,
    base_fontsize: float = 9.0,
) -> dict[str, str]:
    """Configure clean, portable vector rcParams and return selected font names."""
    installed = {f.name for f in fm.fontManager.ttflist}
    sans_chain = [f for f in LATIN_SANS_CANDIDATES if f in installed]
    if enable_cjk:
        cjk_hits = [f for f in CJK_SANS_CANDIDATES if f in installed]
        # Place CJK-capable sans right after primary Latin font for mixed labels
        sans_chain = sans_chain[:1] + cjk_hits + sans_chain[1:]
    if "DejaVu Sans" not in sans_chain:
        sans_chain.append("DejaVu Sans")

    primary_font = sans_chain[0]
    num_font = detect_installed_font(ROUNDED_NUM_CANDIDATES, default=primary_font)

    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": sans_chain,
            "font.size": base_fontsize,
            "font.weight": "normal",
            "axes.labelsize": base_fontsize + 0.5,
            "axes.labelweight": "normal",
            "axes.titlesize": base_fontsize + 1.0,
            "axes.titleweight": "600",
            "xtick.labelsize": base_fontsize,
            "ytick.labelsize": base_fontsize,
            "legend.fontsize": base_fontsize,
            "pdf.fonttype": 42,       # Embed TrueType outlines (required by IEEE/ACM)
            "ps.fonttype": 42,
            "svg.fonttype": "none",   # Preserve live text for rsvg-convert vector PDF
            "axes.edgecolor": NEUTRALS["spine"],
            "axes.linewidth": 0.85,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    return {"primary": primary_font, "numeric": num_font}


# ---------------------------------------------------------------------------
# 3. Frameless Axes & Optical-Centered Rounded Bar Primitives
# ---------------------------------------------------------------------------


def style_clean_axes(
    ax: mpl.axes.Axes,
    x_bounds: tuple[float, float] | None = None,
    y_bounds: tuple[float, float] | None = None,
    grid_axis: str | None = "x",
) -> None:
    """Apply clean frameless publication styling to a Matplotlib Axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(NEUTRALS["spine"])
    ax.spines["bottom"].set_color(NEUTRALS["spine"])
    ax.spines["left"].set_linewidth(0.85)
    ax.spines["bottom"].set_linewidth(0.85)

    if x_bounds is not None:
        ax.spines["bottom"].set_bounds(*x_bounds)
    if y_bounds is not None:
        ax.spines["left"].set_bounds(*y_bounds)

    ax.tick_params(
        axis="both",
        colors=NEUTRALS["ink"],
        width=0.8,
        length=3.0,
        pad=3.5,
    )
    if grid_axis in ("x", "y", "both"):
        ax.grid(
            axis=grid_axis,
            color=NEUTRALS["grid"],
            linestyle="-",
            linewidth=0.65,
            zorder=1,
        )
        ax.set_axisbelow(True)


def _right_rounded_rect_path(
    x0: float,
    y_center: float,
    width: float,
    height: float,
    rx: float,
    ry: float,
) -> MplPath:
    """Build a rectangle Path flat on the left (`x0`) and rounded on the right."""
    y0 = y_center - height / 2.0
    y1 = y_center + height / 2.0
    x1 = x0 + width
    rx_eff = min(rx, width * 0.48)
    ry_eff = min(ry, height * 0.48)
    k = 0.55228475

    verts = [
        (x0, y0),
        (x1 - rx_eff, y0),
        (x1 - rx_eff * (1 - k), y0),
        (x1, y0 + ry_eff * (1 - k)),
        (x1, y0 + ry_eff),
        (x1, y1 - ry_eff),
        (x1, y1 - ry_eff * (1 - k)),
        (x1 - rx_eff * (1 - k), y1),
        (x1 - rx_eff, y1),
        (x0, y1),
        (x0, y0),
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CLOSEPOLY,
    ]
    return MplPath(verts, codes)


def draw_stacked_rounded_hbar(
    ax: mpl.axes.Axes,
    y_center: float,
    segments: Sequence[float],
    colors: Sequence[str],
    x_span: float,
    height: float = 0.58,
    rx_frac: float = 0.014,
    ry: float = 0.19,
    num_font: str | None = None,
    fontsize: float = 8.4,
    total_formatter: str | None = "{total:g}",
    x_pad_frac: float = 0.018,
) -> None:
    """Draw a scale-invariant horizontal stacked bar with optical digit centering.

    - All horizontal tolerances (`rx_frac`, `x_pad_frac`, inline-fit width) scale
      automatically with `x_span` so the helper works identically on `[0, 1]`,
      `[0, 100]`, or `[0, 10000]` axes.
    - Uses `va="center_baseline"` so digits sit optically centered inside segments.
    - Never silently drops small non-zero segments: segments too narrow for their
      digit string receive a clean staggered micro-leader callout.
    - Renders an explicit baseline dot + `0` label when the row total is zero.
    """
    total = sum(segments)
    font_kw = {"fontfamily": num_font} if num_font else {}
    rx = rx_frac * x_span
    x_pad = x_pad_frac * x_span

    if total <= 0:
        ax.scatter(
            [0.008 * x_span],
            [y_center],
            s=18,
            color=NEUTRALS["tick_line"],
            zorder=4,
            clip_on=False,
        )
        ax.text(
            0.026 * x_span,
            y_center,
            "0",
            ha="left",
            va="center_baseline",
            fontsize=fontsize,
            color=NEUTRALS["ink_muted"],
            **font_kw,
        )
        return

    nonzero_indices = [i for i, v in enumerate(segments) if v > 0]
    last_idx = nonzero_indices[-1]
    overlap = 0.0006 * x_span

    cursor = 0.0
    narrow_slot = 0
    for idx, (val, color) in enumerate(zip(segments, colors)):
        if val <= 0:
            continue
        if idx == last_idx:
            path = _right_rounded_rect_path(cursor, y_center, val, height, rx=rx, ry=ry)
            patch = mpatches.PathPatch(
                path, facecolor=color, edgecolor="none", zorder=3
            )
            ax.add_patch(patch)
        else:
            rect = mpatches.Rectangle(
                (cursor, y_center - height / 2.0),
                val + overlap,
                height,
                facecolor=color,
                edgecolor="none",
                zorder=3,
            )
            ax.add_patch(rect)

        label_str = f"{val:g}"
        min_fit_width = x_span * (
            0.024 * len(label_str) + (0.020 if idx == last_idx else 0.012)
        )
        if val >= min_fit_width:
            nudge = -0.06 * val if (idx == last_idx and val < 1.8 * min_fit_width) else 0.0
            ax.text(
                cursor + val / 2.0 + nudge,
                y_center,
                label_str,
                ha="center",
                va="center_baseline",
                fontsize=fontsize,
                fontweight="normal",
                color=pick_readable_text_color(color),
                zorder=5,
                **font_kw,
            )
        else:
            direction = 1.0 if narrow_slot % 2 == 0 else -1.0
            narrow_slot += 1
            y_edge = y_center + direction * (height * 0.50)
            y_tip = y_center + direction * (height * 0.64)
            x_mid = cursor + val / 2.0
            ax.plot(
                [x_mid, x_mid],
                [y_edge, y_tip],
                color=NEUTRALS["tick_line"],
                linewidth=0.65,
                zorder=4,
            )
            ax.text(
                x_mid,
                y_tip + direction * 0.02,
                label_str,
                ha="center",
                va="bottom" if direction > 0 else "top",
                fontsize=max(7.2, fontsize - 1.0),
                fontweight="normal",
                color=NEUTRALS["ink"],
                zorder=5,
                **font_kw,
            )
        cursor += val

    if total_formatter:
        ax.text(
            total + x_pad,
            y_center,
            total_formatter.format(total=total),
            ha="left",
            va="center_baseline",
            fontsize=fontsize + 0.2,
            fontweight="normal",
            color=NEUTRALS["ink"],
            zorder=5,
            **font_kw,
        )


# ---------------------------------------------------------------------------
# 4. Zero-Margin Vector PDF Export Pipeline (with Portable Fallback)
# ---------------------------------------------------------------------------


def save_zero_margin_pdf(fig: mpl.figure.Figure, pdf_path: str | Path) -> Path:
    """Export `fig` as a tightly cropped (`0 pt` margin) TrueType vector PDF.

    Preferred route: Matplotlib SVG -> `rsvg-convert -f pdf` -> `pdfcrop --margins 0`.
    Portable fallback: Matplotlib TrueType PDF (`bbox_inches="tight", pad_inches=0.005`),
    followed by `pdfcrop --margins 0` if available on PATH.
    """
    out_path = Path(pdf_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.patch.set_alpha(0.0)

    rsvg_bin = shutil.which("rsvg-convert")
    pdfcrop_bin = shutil.which("pdfcrop")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        if rsvg_bin:
            svg_tmp = tmp / "raw.svg"
            pdf_tmp = tmp / "raw.pdf"
            fig.savefig(svg_tmp, format="svg", bbox_inches="tight", pad_inches=0.02)
            subprocess.run(
                [rsvg_bin, "-f", "pdf", "-o", str(pdf_tmp), str(svg_tmp)],
                check=True,
            )
            if pdfcrop_bin:
                subprocess.run(
                    [pdfcrop_bin, "--margins", "0", str(pdf_tmp), str(out_path)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
            else:
                shutil.copyfile(pdf_tmp, out_path)
        else:
            pdf_tmp = tmp / "raw.pdf"
            fig.savefig(pdf_tmp, format="pdf", bbox_inches="tight", pad_inches=0.01)
            if pdfcrop_bin:
                subprocess.run(
                    [pdfcrop_bin, "--margins", "0", str(pdf_tmp), str(out_path)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
            else:
                shutil.copyfile(pdf_tmp, out_path)

    return out_path


# ---------------------------------------------------------------------------
# 5. Generic Self-Test / Reference Single-Column Chart Example
# ---------------------------------------------------------------------------


def build_demo_chart(out_pdf: Path, palette_name: str = "cobalt_amber_teal") -> Path:
    """Render a generic single-column stacked comparison chart for verification."""
    fonts = configure_publication_rcparams(enable_cjk=False, base_fontsize=8.8)
    c1, c2, _ = PALETTE_PRESETS[palette_name]

    # Generic synthetic benchmark categories (ordered descending)
    rows: list[tuple[str, tuple[float, float]]] = [
        ("Configuration A", (18, 12)),
        ("Configuration B", (14, 5)),
        ("Configuration C", (7, 4)),
        ("Configuration D", (6, 1.5)),
        ("Configuration E (Baseline)", (0, 0)),
    ]

    # Target single-column width (~3.45 in in two-column IEEE/ACM templates)
    fig, ax = plt.subplots(figsize=(3.55, 2.25))
    n = len(rows)
    y_positions = list(range(n - 1, -1, -1))

    x_span = 35.0
    for y, (_, segs) in zip(y_positions, rows):
        draw_stacked_rounded_hbar(
            ax,
            y_center=y,
            segments=segs,
            colors=(c1, c2),
            x_span=x_span,
            height=0.56,
            ry=0.18,
            num_font=fonts["numeric"],
            fontsize=8.3,
            total_formatter="{total:g}",
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(
        [label for label, _ in rows],
        va="center_baseline",
        color=NEUTRALS["ink"],
    )
    ax.set_xlim(0, x_span)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_ylim(-0.55, n - 0.35)
    ax.set_xlabel("Throughput Gain (Normalized Units)", labelpad=4)

    style_clean_axes(ax, x_bounds=(0, 30), y_bounds=(0, n - 1), grid_axis="x")
    ax.spines["left"].set_bounds(-0.4, n - 0.6)

    legend_handles = [
        mpatches.Patch(facecolor=c1, edgecolor="none", label="Compile-Time Opt."),
        mpatches.Patch(facecolor=c2, edgecolor="none", label="Runtime Scheduling"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=2,
        frameon=False,
        handlelength=1.0,
        handleheight=0.9,
        columnspacing=1.2,
        handletextpad=0.45,
        borderaxespad=0.0,
    )

    saved = save_zero_margin_pdf(fig, out_pdf)
    plt.close(fig)
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Render generic publication chart demo.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("demo_publication_chart.pdf"),
        help="Destination path for zero-margin vector PDF.",
    )
    parser.add_argument(
        "--palette",
        choices=sorted(PALETTE_PRESETS.keys()),
        default="cobalt_amber_teal",
    )
    args = parser.parse_args()
    out = build_demo_chart(args.out, palette_name=args.palette)
    print(f"Exported zero-margin vector PDF -> {out}")


if __name__ == "__main__":
    main()
