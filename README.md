# Attention research: results report

Builds `attention-research-results.pdf`, the combined results document for two
projects:

* **CRPA** — is behavioural contribution measurable at all?
  <https://github.com/ishaannk/crpa/pull/1>
* **xsa-controls** — sanity checks for attention surgery
  <https://github.com/RohanMulay1/xsa-controls>

Every number and every figure is read from a committed result file in one of
those two repositories. Nothing in `pdf_content.py` is hand-computed, and no
figure is drawn from a value that is not in a CSV or JSON under `results/`.

## Layout

| File | Role |
|---|---|
| `build_pdf.py` | Document shell: page geometry, styles, spacing scale, table and figure builders |
| `pdf_content.py` | All copy and every table, as plain data |
| `report_figs.py` | Renders the eight figures into `figs/` from the two repos' result files |
| `figs/` | Rendered figures, committed so the PDF builds without both repos present |

## Build

```bash
pip install -r requirements.txt

# Optional: regenerate the figures. Needs both source repos cloned.
python report_figs.py

python build_pdf.py
```

`report_figs.py` reads `~/crpa/results` and `~/xsa-controls/results`. Override
with `CRPA_RESULTS` and `XSAC_RESULTS` if they are cloned elsewhere.
`build_pdf.py` writes beside itself; override with `REPORT_OUT`.

## Design notes

**Spacing.** One unit `U = 9pt` drives every vertical gap: `TIGHT` (1x) inside a
block, `NEAR` (2x) between a block and its figure, `APART` (3x) between
sections. Change `U` in `build_pdf.py` and the whole document rescales while
keeping its rhythm.

**Block gluing.** `sec()` keeps a heading with its table so a heading never sits
alone at a page foot. A block taller than half the frame is deliberately left
loose instead: gluing one of those stalls it to the next page and strands most
of the current one, which reads worse than a table continuing across the break.
Tables repeat their header row when they split.

**Figures.** Sized wide and short rather than scaled down, so their labels stay
legible against the body text while each block costs less vertical space.
Legends sit in a strip above the axes, never inside the plot, because a legend
placed inside a short plot lands on the data or clips the top tick label.

## Verifying a build

The content is checked by reading the rendered PDF back, not by trusting the
source. See `QA_CHECKLIST.md`.
