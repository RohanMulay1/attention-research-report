from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

import fitz
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CRPA = Path(os.environ.get("CRPA_RESULTS", ROOT.parent / "crpa" / "results"))
XSAC = Path(os.environ.get("XSAC_RESULTS", ROOT.parent / "xsa-controls" / "results"))


@pytest.fixture(scope="session")
def built_report(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("rendered-report")
    pdf = out_dir / "attention-research-results.pdf"
    figs = out_dir / "figs"
    env = os.environ.copy()
    env.update({
        "REPORT_OUT": str(pdf),
        "REPORT_FIG_DIR": str(figs),
        "REPORT_REGENERATE_FIGURES": "1",
        "CRPA_RESULTS": str(CRPA),
        "XSAC_RESULTS": str(XSAC),
    })
    proc = subprocess.run(
        [sys.executable, "build_pdf.py"], cwd=ROOT, env=env,
        text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert pdf.exists()
    return pdf, figs


def test_structure_and_caption_order(built_report):
    pdf, _ = built_report
    doc = fitz.open(pdf)
    assert len(doc) == 9
    assert sum(len(page.get_images(full=True)) for page in doc) == 8
    text = "\n".join(page.get_text() for page in doc)
    captions = re.findall(r"Figure\s+([1-8])\.", text)
    assert captions == list("12345678")


def test_rendered_text_has_no_markup_or_placeholders(built_report):
    pdf, _ = built_report
    doc = fitz.open(pdf)
    text = "\n".join(page.get_text() for page in doc)
    forbidden = ("&nbsp", "&ldquo", "&ndash", "<b>", "<i>",
                 "\\u", "\ufffd", "TODO", "TBD", "XXX")
    assert not [token for token in forbidden if token in text]
    assert not re.search(r"\b(?:nan|None)\b", text, re.IGNORECASE)


def _horizontal_rules(page):
    rules = []
    for drawing in page.get_drawings():
        for item in drawing["items"]:
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) < 0.2 and abs(p2.x - p1.x) > 400:
                    rules.append(float(p1.y))
    return rules


def test_section_spacing_is_uniform_in_rendered_pdf(built_report):
    pdf, _ = built_report
    doc = fitz.open(pdf)
    gaps = []
    for page in doc:
        rules = _horizontal_rules(page)
        for block in page.get_text("blocks"):
            text = block[4].strip()
            if re.match(r"^[12]\.\d\s", text):
                above = [y for y in rules if y < block[1] - 0.5]
                if above:
                    gap = float(block[1]) - max(above)
                    # Only headings immediately following a drawn rule express
                    # this rhythm; intervening prose/figures are not spacing
                    # samples for the rule-to-heading invariant.
                    if gap < 50:
                        gaps.append(gap)
    assert len(gaps) >= 3
    assert all(26.0 <= gap <= 26.5 for gap in gaps), gaps
    assert max(gaps) - min(gaps) <= 0.2, gaps


def test_page_fill_and_no_overflow(built_report):
    pdf, _ = built_report
    doc = fitz.open(pdf)
    fills = []
    for page in doc:
        bottoms = [b[3] for b in page.get_text("blocks") if b[1] < 790]
        image_rects = [fitz.Rect(info["bbox"])
                       for info in page.get_image_info()]
        bottoms.extend(rect.y1 for rect in image_rects if rect.y0 < 790)
        assert bottoms
        fills.append(max(bottoms) / page.rect.height)
        assert max(bottoms) < 790, "content crossed the footer boundary"
    assert all(fill >= 0.60 for fill in fills[:-1]), fills


def test_every_figure_source_exists_and_every_figure_is_built(built_report):
    _, figs = built_report
    env = os.environ.copy()
    env.update({"CRPA_RESULTS": str(CRPA), "XSAC_RESULTS": str(XSAC)})
    code = ("import os, report_figs; "
            "missing=[str(p) for ps in report_figs.FIGURE_SOURCES.values() "
            "for p in ps if not p.exists()]; print('\\n'.join(missing))")
    proc = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                          text=True, capture_output=True)
    assert proc.returncode == 0 and not proc.stdout.strip(), proc.stdout
    assert sorted(p.name for p in figs.glob("*.png")) == [
        "f{}_{}.png".format(i, name) for i, name in enumerate(
            ("check0", "floor", "ladder", "length", "gqa", "paired",
             "generality", "cost"), 1)]


def test_report_figs_has_only_the_documented_measurement_literal():
    source = (ROOT / "report_figs.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    literals = [node.value for node in ast.walk(tree)
                if isinstance(node, ast.Constant)
                and isinstance(node.value, (int, float))]
    assert sum(value == 41.9 for value in literals) == 1
    for forbidden in ("ulps = [5.0", "axvspan(-0.00518", "axvline(-0.00076",
                      '"gpt2": 124e6'):
        assert forbidden not in source


def test_key_report_numbers_trace_to_results():
    import csv
    import json

    floor = json.loads((CRPA / "chance_floor.json").read_text())
    assert round(floor["strongest_mean_percent"], 2) == 52.78
    assert round(floor["strongest_sd_percent"], 2) == 0.08

    pilot = json.loads((XSAC / "pilot_decision.json").read_text())
    assert round(pilot["mde"], 5) == 0.00518

    with (CRPA / "tier3" / "edges_EleutherAI_pythia-6.9b.csv").open(
            newline="", encoding="utf-8") as fh:
        edges = list(csv.DictReader(fh))
    assert len(edges) == 192
    assert all(float(row["delta_loss"]) == 0.0 for row in edges)

    with (CRPA / "figures" / "fig5b_context_performance_data.csv").open(
            newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by_context = {}
    for row in rows:
        if row["status"] == "completed":
            by_context.setdefault(int(row["context_length"]), {})[
                row["variant"]] = float(row["latency_ms_median"])
    ratios = [by_context[t]["crpa_contribution"] / by_context[t]["dense"]
              for t in (4096, 8192, 16384)]
    assert [round(value, 2) for value in ratios] == [2.40, 2.00, 1.65]


def test_committed_figures_match_regenerated_pixels(built_report):
    _, figs = built_report
    from PIL import Image
    for generated in figs.glob("*.png"):
        committed = ROOT / "figs" / generated.name
        assert committed.exists()
        with Image.open(generated) as ga, Image.open(committed) as cb:
            aspect_a = ga.width / ga.height
            aspect_b = cb.width / cb.height
            assert abs(aspect_a - aspect_b) / aspect_b < 0.01, (
                "committed figure aspect drift: {}".format(generated.name))
            # Tight bounding boxes inherit platform font metrics. Resample to
            # a canonical canvas before comparing the rendered visual content.
            canvas = (640, 320)
            a = np.asarray(ga.convert("RGBA").resize(
                canvas, Image.Resampling.LANCZOS), dtype=float) / 255.0
            b = np.asarray(cb.convert("RGBA").resize(
                canvas, Image.Resampling.LANCZOS), dtype=float) / 255.0
        # Bound both total and spatial visual drift; separate source-trace
        # tests enforce every plotted measurement.
        delta = np.abs(a - b)
        mean_delta = float(delta.mean())
        changed = float(np.mean(np.max(delta, axis=2) > (8.0 / 255.0)))
        assert mean_delta < 0.01 and changed < 0.05, (
            "committed figure drift: {} (mean={:.6f}, changed={:.4%})".format(
                generated.name, mean_delta, changed))
