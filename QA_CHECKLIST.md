# QA checklist

For an agent verifying all three deliverables. Every item is a command with an
expected result, so a check either passes or fails on evidence rather than on
judgement. Where a count is given it is the value as of 2026-09-04; if a number
has moved, say so and explain why rather than silently updating this file.

Repositories:

| # | Path | Remote |
|---|---|---|
| 1 | `~/crpa` | `RohanMulay1/crpa`, branch `feat/evidence-scaling`, PR #1 into `ishaannk/crpa` |
| 2 | `~/xsa-controls` | `RohanMulay1/xsa-controls`, branch `feat/sanity-checks-harness-and-day1-gate` |
| 3 | `~/attention-research-report` | local only |

**Ground rule for the whole checklist:** a claim is verified by running
something, not by reading a document that asserts it. Several defects in this
work were found only because a rendered artifact was read back rather than
trusted. If a check cannot be run, record it as NOT RUN. Never record a check as
passing because the code looks correct.

---

## 0. Cross-cutting integrity

- [ ] **No credentials anywhere.** In each repo:
      `git log -p | grep -niE "rpa_[a-z0-9]{18,}|api[_-]?key *= *[\"'][^\"']{16,}"`
      Expect no hits. RunPod helper scripts must not be committed to any repo.
- [ ] **No agent attribution.** `git log --format='%an <%ae>%n%b' | grep -ci claude`
      Expect `0` in both project repos.
- [ ] **Working tree clean and pushed.**
      `git status --porcelain` empty and `git log --oneline @{u}..HEAD` empty.
- [ ] **No result is a converted failure.** Search every results JSON for a
      `status` field and confirm no record with status `oom`, `not_run`,
      `unsupported` or `failed` carries a numeric metric that appears in any
      table or figure. This is the single most important scientific check in
      the repository; an OOM must never surface as a number.
- [ ] **Budget homogeneity.** No aggregate averages across differing
      `max_iters` / `tokens_per_run`. Both repos have a guard; confirm it is
      actually called on the aggregation path, not merely defined.

---

## 1. CRPA (`~/crpa`)

- [ ] `pytest -q` → **266 passed**.
- [ ] `pytest --cov=crpa --cov-report=term-missing -q` → **83%** or higher.
- [ ] `python main.py --max_iters 50 --block_size 64` runs to completion. This
      is the backwards-compatibility contract; it must not require new flags.
- [ ] `python -m experiments.plot_all` → **7 figures rendered, 0 skipped.**
- [ ] `python -m experiments.resolvability --seeds 42 1337 2024 --loss lm --smoke`
      completes and writes a `status` field.
- [ ] **Check 0 verdict is UNRESOLVABLE.** In
      `results/resolvability/resolvability.json`, best `r_delta` is about 0.088
      against the 0.3 threshold, and every observed `|rho|` is inside its own
      ceiling. If this has flipped to reliable, the headline claim changes and
      that is a finding, not a fix.
- [ ] **The withdrawn claim stays withdrawn.** `README.md` and the PR body must
      not assert that structural overlap fails to predict behavioural
      contribution, nor that the retrieval task is learnable. Grep for
      "does not predict" and "learnable".
- [ ] **Chance floor is measured, not asserted.** Confirm 52.78% appears as a
      measured value with its sd and n, and that 5.0% (vocabulary-derived)
      appears nowhere as a floor.
- [ ] **Tier 2 honesty.** `results/tier2` records 32,768 and 65,536 with status
      `oom`. Confirm no latency or memory number for those lengths exists in any
      table, figure or CSV.
- [ ] `pyflakes crpa experiments tests` clean.

## 2. xsa-controls (`~/xsa-controls`)

- [ ] `pytest -q` → **202 passed**.
- [ ] `pytest --cov=xsac --cov-report=term-missing -q` → **90%** or higher, and
      `calibrate.py` at **96%** or higher.
- [ ] `python scripts/selftest_arms.py --json results/selftest.json` → **10/10**,
      with measured step-0 deviation exactly `0.000e+00` across all five arms.
      A non-zero value means the arms do not start from a common point and every
      paired comparison downstream is invalid.
- [ ] `python scripts/verify_day.py --all` → gates 1, 2, 3, 8, 9, 10 pass.
      Days 4-6 at 4/5 and Day 7 at 3/4 are the known, documented state.
- [ ] `python scripts/a4_recompute.py` runs on CPU with no downloads.
- [ ] **The diagmask bf16 regression tests exist and pass.** This defect crashed
      every GPU run while CPU tests passed. Confirm there are autocast tests, not
      only CPU ones.
- [ ] **Calibration is consumed.** Confirm `run_factorial.py` reads
      `results/calibration.json` and does not fall back to a hardcoded default
      when the file is present.
- [ ] **The cost ceiling is enforced in code**, not merely defined in config.
      Grep for the stop threshold constant and confirm a code path compares
      against it.
- [ ] **Day-3 is reported as a power failure.** MDE 0.00518 against the 0.00076
      target, roughly sevenfold underpowered. It must not be presented as a null
      result.
- [ ] **GPT-2 Check-1 is left failing on purpose.** `results/gpt2_diagnosis.csv`
      holds all thirteen conventions, unselected, and no configuration is
      presented as "the" method. If someone has selected a row that matches the
      reference, that is a regression in integrity, not progress.
- [ ] `python scripts/make_figures.py` → **5 figures, none skipped.**

## 3. Report (`~/attention-research-report`)

Content checks read the rendered PDF back with PyMuPDF. Do not verify these by
reading `pdf_content.py`; a previous build shipped stale content that the source
looked correct for.

- [ ] `python build_pdf.py` succeeds from a clean clone with only
      `requirements.txt` installed, writing beside itself with no `REPORT_OUT`.
- [ ] **Structure:** 9 pages, 8 embedded images, captions `Figure 1.` through
      `Figure 8.` each present exactly once and in order.
- [ ] **No unrendered markup** in the extracted text: no `&nbsp`, `&ldquo`,
      `&ndash`, `<b>`, `<i>`, or a literal backslash-u escape. A `“` shipped
      once and was invisible to every source-level check.
- [ ] **No placeholder values:** no `nan`, `None`, `TODO`, `TBD`, `XXX`.
- [ ] **Spacing rhythm:** the gap from a rule to the next section heading is the
      same on every page, currently 26.2-26.3pt. Measure with `get_drawings()`,
      not by eye.
- [ ] **Page fill:** no page ends below 60% except the last, and none overflows.
      Mean fill is currently 79%.
- [ ] **Figure regeneration:** with both source repos present,
      `python report_figs.py` rewrites all 8 PNGs and `build_pdf.py` then
      produces a PDF with the same page count.
- [ ] **Every figure traces to committed data.** For each of the 8, identify the
      CSV or JSON under `~/crpa/results` or `~/xsa-controls/results` it reads.
      `report_figs.py` must contain no hand-entered measurement. The one
      permitted literal is `41.9` in `fig_generality`, which restates a value
      shown in the adjacent table and in `ladder.csv`; confirm it still matches.
- [ ] **Every table number traces to a result file.** Spot-check at least six
      across both projects, including the 52.78% floor, the 0.00518 MDE, the
      6.9B `0.000e+00`, and the 2.39x/2.00x/1.65x latency ratios.
- [ ] **Read the rendered pages.** Render each page to PNG and look at it for
      label collisions, clipped axis labels, legends overlapping data, wrapped
      table headers and orphaned headings. Three defects in this document were
      caught only this way and were invisible to every text-level check.

---

## Reporting

For each item: PASS, FAIL or NOT RUN, with the command output for anything that
is not a PASS. Do not fix and re-report in one pass; list findings first, and
treat any item whose expected value has moved as a finding to explain rather
than a number to update.
