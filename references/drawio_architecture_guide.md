# Framework, Architecture & Flow Diagram Guide (`draw.io` & Vector Workflows)

This reference details how to design, structure, and export Category A qualitative figures: **system architectures, method pipelines, conceptual taxonomies, screening/selection funnels, and decision workflows**.

---

## 1. Visual Grammar: Show Structure with Shapes, Icons & Arrows

1. **Replace Prose Cards with Visual Structure**:
   - **Anti-Pattern 1 (Card-of-Text)**: A rectangle containing a **Bold Title** on line 1 and 2–3 lines of tiny gray explanatory text underneath. *Fix*: Keep only the self-explanatory 2–5 word concept title in regular weight (`400`, `#111111`) paired with a meaningful icon, and express relationships via arrows and spatial grouping.
   - **Anti-Pattern 2 (Middle-Dot / Slash Soup)**: Stuffing parallel items into one box (`Feature Extraction · Normalization · Pruning`). *Fix*: Split distinct steps or modules into separate connected or aligned visual nodes.
   - **Anti-Pattern 3 (False Dichotomy)**: Drawing a left-vs-right `vs.` layout when two modules are sequential or complementary rather than contrasting alternatives.
2. **Semantic Icon Discipline**:
   - Every icon must correspond directly to its domain operation (e.g., cylinder for storage, funnel/filter for screening, tree/graph for structural modeling, gear/chip for compute kernel, checkmark/cross for validation branches).
   - Never reuse the same generic icon across unrelated stages or add purely decorative clipart.
3. **Conceptual Actions Only (No Hindsight, No Mechanical Chores)**:
   - Describe generalizable scientific/system logic (e.g., *"Iterative Expansion until Convergence"*), annotating dataset-specific run counts as subtle instance badges rather than hardcoding post-hoc numbers into the rule name.
   - Never depict low-level clerical actions (*"Open PDF"*, *"Load JSON"*, *"Write Log File"*) as architectural stages.

---

## 2. Container Hierarchy & Spatial Layout Rules

1. **Hard Nesting Ceiling (`< 3` Rectangle Layers — Maximum 2 Levels)**:
   - **Level 1 (Optional Outer Zone)**: High-level stage, layer, or subsystem container with a soft background tint (`#F8FAFC` or `#F1F5F9`), subtle border (`#CBD5E1`, `1 pt`), and a `600`-weight zone header aligned cleanly at top-left.
   - **Level 2 (Component / Step Node)**: Crisp white (`#FFFFFF`) or light-accent rounded rectangle (`rounded=1;arcSize=12;strokeWidth=1.1`) holding the icon and concise label.
   - **Forbidden Level 3+**: Never place sub-boxes inside Level 2 boxes. If sub-components exist, promote Level 2 to the outer zone (eliminating the outer wrapper) or place sub-components side by side at Level 2.
2. **Unambiguous Badge & Callout Ownership**:
   - Count pills (`N = 120`), status tags, or mathematical annotations must either sit flush on the target box border/header or connect via a short, crisp leader line—never float in empty space between two boxes where ownership is ambiguous.
3. **High Canvas Density & Balanced Aspect Ratio**:
   - Match canvas aspect ratio to target placement:
     - **Single-column figure (`\columnwidth`, ~3.4 in)**: Design around `520–640 px` width with compact vertical flow.
     - **Double-column overview (`\textwidth`, ~7.0 in)**: Design around `1040–1280 px` width with left-to-right multi-stage flow and tight vertical height (`280–460 px`) so no dead space accumulates at the bottom.

---

## 3. Grid Alignment, Connectors & Decision Logic

1. **Snap Everything to a `10 px` Grid**:
   - Keep node `x`, `y`, `width`, and `height` on clean multiples of `10` (or `5`) so horizontal centers (`y + height / 2`) and vertical centers (`x + width / 2`) match exactly.
2. **Explicit Port Anchoring & Minimal Bends**:
   - Always bind arrows using explicit normalized ports (`exitX=1;exitY=0.5;entryX=0;entryY=0.5;` etc.) instead of floating center-to-center auto-routing.
   - Prefer **straight horizontal/vertical arrows**. When orthogonal routing is unavoidable, use **at most 1 clean 90° turn** (or a clean fork bus) with `rounded=1;arcSize=8;strokeWidth=1.25;strokeColor=#475569;` and **zero line crossings**.
3. **Complete Decision & Filtering Branches**:
   - In selection funnels, routing trees, or verification loops, never show an unexplained count drop (`500 -> 80`). Explicitly draw the **filtering criteria** and the **excluded/rejected branch** alongside the retained branch so the logic closes quantitatively and conceptually.

---

## 4. Typography & Color Tokens in `.drawio`

- **Font Family**: `Helvetica Neue`, `Avenir Next`, `Inter`, or `Arial` (for CJK/bilingual diagrams: `PingFang SC` or `Noto Sans CJK SC`).
- **Font Weights & Sizes** (at `~1100 px` double-column or `~560 px` single-column canvas):
  - Zone Header: `13–14 px`, semi-bold (`fontStyle=1` sparingly on zone title only), `#1E293B`.
  - Node Label: `12–13 px`, regular (`fontStyle=0`), `#111111`.
  - Edge Condition / Badge: `11 px`, regular (`fontStyle=0`), `#334155` or `#FFFFFF` on deep pill fill.
- **Hue Budget**: Pick **2–3 hue families max** per diagram (e.g., Slate neutral structure + Cobalt primary flow + Amber decision/highlight, or Teal + Indigo + Slate). Rotate accent pairs across different diagrams in the same manuscript.

---

## 5. Source Archival, User-Edit Preservation & Anti-Clipping Export

### 5.1 Co-Location & Respecting Manual Edits
- Always store `figures/<fig_name>.drawio` alongside `figures/<fig_name>.pdf`.
- **Before any automated edit**: Check `git status` / file modification time and read the current `.drawio` XML. When a user has manually adjusted node coordinates, spacing, or styling in the `draw.io` GUI, patch only the requested attributes in place—**never regenerate from scratch and clobber manual refinements**.

### 5.2 Preventing Top/Edge Glyph Clipping
- When embedding custom SVG icons/mini-graphics (`image=data:image/svg+xml,...`) or placing text near canvas edges:
  - SVG `<text x="..." y="...">` treats `y` as the **alphabetic baseline**, meaning uppercase letters and digits extend `~0.75 * font_size` **above** `y`! Always set `y >= font_size` (or expand `viewBox` top `min-y`) so ascenders never cross `y = 0`.
  - Avoid negative coordinates or unpadded borderless text boxes flush against the outermost boundary before cropping.

### 5.3 Command-Line Vector Export Recipes
1. **macOS (`draw.io.app` installed)**:
   ```bash
   /Applications/draw.io.app/Contents/MacOS/draw.io \
     --export --format pdf --crop \
     --output figures/fig_overview.pdf \
     figures/fig_overview.drawio
   pdfcrop --margins 0 figures/fig_overview.pdf figures/fig_overview.pdf
   ```
2. **Linux (Desktop or Headless CI)**:
   ```bash
   # Direct CLI (or prefix with `xvfb-run -a` on headless servers)
   drawio --export --format pdf --crop \
     --output figures/fig_overview.pdf \
     figures/fig_overview.drawio
   pdfcrop --margins 0 figures/fig_overview.pdf figures/fig_overview.pdf
   ```
3. **Mandatory Raster Verification**:
   ```bash
   pdftoppm -png -r 300 figures/fig_overview.pdf /tmp/fig_overview_check
   ```
   Inspect `/tmp/fig_overview_check-1.png` visually to verify crisp `0 pt` crop, intact outer strokes/ascenders, straight connectors, and balanced typography.
