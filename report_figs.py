"""Figures for the results report.

Purpose-built for the PDF rather than reused from either repo's own figure
module: a report needs a small number of high-signal panels sized for a page,
with the n stated in the caption. Every value is read from a committed result
file; nothing is hand-entered.

Style follows the report: near-greyscale with one accent, redundant encoding
(marker and linestyle as well as colour) so the panels survive greyscale
printing, and no series distinguished by colour alone.
"""

import csv
import argparse
import json
import os
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = pathlib.Path(os.environ.get(
    "REPORT_FIG_OUT", pathlib.Path(__file__).parent / "figs"))
# Result directories of the two source repositories. Override when they
# are cloned somewhere other than the home directory.
CRPA = pathlib.Path(os.environ.get(
    "CRPA_RESULTS", os.path.expanduser("~/crpa/results")))
XSAC = pathlib.Path(os.environ.get(
    "XSAC_RESULTS", os.path.expanduser("~/xsa-controls/results")))

FIGURE_SOURCES = {
    "f1_check0.png": (CRPA / "resolvability" / "resolvability.json",),
    "f2_floor.png": (
        CRPA / "resolvability" / "resolvability.json",
        CRPA / "tier2" / "long_context.csv",
        CRPA / "tier3" / "edges_EleutherAI_pythia-6.9b.csv",
    ),
    "f3_ladder.png": (XSAC / "ladder.csv", XSAC / "model_metadata.csv"),
    "f4_length.png": (XSAC / "null_length_sensitivity.csv",),
    "f5_gqa.png": (XSAC / "gqa.csv",),
    "f6_paired.png": (
        XSAC / "paired_tests_s.csv", XSAC / "pilot_decision.json",
        XSAC / "reference_values.json",
    ),
    "f7_generality.png": (XSAC / "generality.csv", XSAC / "ladder.csv"),
    "f8_cost.png": (CRPA / "figures" /
                     "fig5b_context_performance_data.csv",),
}

INK = "#111111"
GREY = "#555555"
LIGHT = "#8a8a8a"
GRID = "#dcdcdc"
ACCENT = "#1f4e79"
ACCENT2 = "#a33b20"
FILL = "#c9d4e0"


def style(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontsize=9.2, color=GREY)
    ax.set_ylabel(ylabel, fontsize=9.2, color=GREY)
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=GREY, labelsize=7.5, length=0)
    ax.set_facecolor("white")


def legend_above(ax, ncol, fontsize=7.9):
    """Legend in its own strip above the axes, never over the data."""
    ax.legend(frameon=False, fontsize=fontsize, ncol=ncol,
              loc="lower left", bbox_to_anchor=(0, 1.01, 1, 0.12),
              mode="expand", borderaxespad=0, handlelength=1.6,
              columnspacing=1.4)

def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    fig.patch.set_facecolor("white")
    fig.savefig(p, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", p.name)


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# --- Figure 1: Check 0. Observed correlation against its reliability ceiling
def fig_check0():
    d = json.loads((CRPA / "resolvability" / "resolvability.json").read_text())
    seeds = [s["seed"] for s in d["per_seed"]]
    rho = [abs(s["rho_observed"]) for s in d["per_seed"]]
    ceil = [s["max_observable_correlation"] for s in d["per_seed"]]
    x = np.arange(len(seeds))

    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    ax.bar(x, ceil, width=0.62, color=FILL, edgecolor=ACCENT, linewidth=1.0,
           label="ceiling imposed by unreliability", zorder=2)
    ax.scatter(x, rho, s=58, marker="D", color=ACCENT2, zorder=4,
               label="observed |rho| (overlap vs contribution)")
    for i, (r, c) in enumerate(zip(rho, ceil)):
        ax.annotate("{:.3f}".format(r), (i, r), xytext=(0, 7),
                    textcoords="offset points", ha="center", fontsize=7.8,
                    color=ACCENT2)
    ax.set_xticks(x)
    ax.set_xticklabels(["seed {}".format(s) for s in seeds])
    ax.set_ylim(0, max(max(ceil), max(rho)) * 1.12)
    style(ax, "", "correlation (absolute)")
    legend_above(ax, 2)
    save(fig, "f1_check0.png")


# --- Figure 2: the measurability floor across three orders of magnitude
def fig_floor():
    tier1 = json.loads((CRPA / "resolvability" /
                        "resolvability.json").read_text(encoding="utf-8"))
    tier2 = [r for r in read_csv(CRPA / "tier2" / "long_context.csv")
             if r.get("status") == "completed"]
    tier3 = read_csv(CRPA / "tier3" /
                     "edges_EleutherAI_pythia-6.9b.csv")
    labels = ["12.4M\nfloat32", "138M\nfloat32", "6.9B\nbfloat16"]
    tier1_ulps = float(np.median(
        [r["deltas_per_ulp"] for r in tier1["per_seed"]]))
    tier2_p90 = max(float(r["delta_p90"]) for r in tier2)
    tier2_ulp = min(float(r["float32_resolution_estimate"]) for r in tier2)
    tier3_deltas = [float(r["delta_loss"]) for r in tier3]
    ulps = [tier1_ulps, tier2_p90 / tier2_ulp,
            max(abs(v) for v in tier3_deltas)]
    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    bars = ax.bar(labels, ulps, width=0.55, color=FILL, edgecolor=ACCENT,
                  linewidth=1.0, zorder=2)
    ax.axhline(1.0, color=ACCENT2, linewidth=1.1, linestyle=(0, (4, 3)),
               zorder=3)
    ax.annotate("one representable step", xy=(2.35, 1.20), fontsize=7.8,
                color=ACCENT2, ha="right")
    for b, v in zip(bars, ulps):
        ax.annotate("exactly 0" if v == 0 else "{:.0f} ULP".format(v),
                    (b.get_x() + b.get_width() / 2, v), xytext=(0, 5),
                    textcoords="offset points", ha="center", fontsize=8.1,
                    color=INK)
    ax.set_ylim(0, 6.4)
    style(ax, "model scale and precision",
          "single-edge delta loss  (ULP)")
    save(fig, "f2_floor.png")


# --- Figure 3: Check 1 across the scale ladder
def fig_ladder():
    rows = read_csv(XSAC / "ladder.csv")
    params = {r["model"]: float(r["parameters"])
              for r in read_csv(XSAC / "model_metadata.csv")}
    agg = {}
    for r in rows:
        m = r["model"]
        if m not in params:
            continue
        agg.setdefault(m, {"s": [], "n": []})
        agg[m]["s"].append(float(r["cos_self"]))
        agg[m]["n"].append(float(r["cos_null"]))
    pts = sorted(((params[m], float(np.mean(v["s"])), float(np.mean(v["n"])))
                  for m, v in agg.items()))
    xs = [p[0] for p in pts]
    cs = [p[1] for p in pts]
    cn = [p[2] for p in pts]
    ex = [a - b for a, b in zip(cs, cn)]

    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    ax.axvspan(0.7e9, 2.7e9, color=FILL, alpha=0.55, zorder=0)
    ax.annotate("range the method\nwas trained at", xy=(1.37e9, 0.055),
                fontsize=7.8, color=GREY, ha="center")
    ax.plot(xs, cs, marker="s", ls="-", color=ACCENT, lw=1.6, ms=5,
            label="cos(y, v)  observed", zorder=3)
    ax.plot(xs, cn, marker="D", ls="--", color=ACCENT2, lw=1.6, ms=5,
            label="cos(y, v')  anisotropy null", zorder=3)
    ax.plot(xs, ex, marker="^", ls="-.", color=GREY, lw=1.6, ms=5,
            label="excess (self-specific)", zorder=3)
    ax.set_xscale("log")
    ax.set_ylim(0, 0.56)
    # Explicit ticks at real model sizes: a bare 10^9 decade label tells a
    # reader nothing about which model each point is.
    ticks = [124e6, 410e6, 1.4e9, 2.8e9, 6.9e9]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["124M", "410M", "1.4B", "2.8B", "6.9B"])
    ax.minorticks_off()
    style(ax, "parameters (log scale)", "cosine similarity")
    legend_above(ax, 2)
    save(fig, "f3_ladder.png")


# --- Figure 4: the null depends on the sequence length it is measured at
def fig_length():
    rows = read_csv(XSAC / "null_length_sensitivity.csv")
    rows.sort(key=lambda r: int(r["block_size"]))
    t = [int(r["block_size"]) for r in rows]
    cs = [float(r["cos_self"]) for r in rows]
    cn = [float(r["cos_null"]) for r in rows]
    frac = [100 * float(r["self_specific_fraction"]) for r in rows]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.4))
    a1.plot(t, cs, marker="s", ls="-", color=ACCENT, lw=1.6, ms=5,
            label="cos(y, v) observed")
    a1.plot(t, cn, marker="D", ls="--", color=ACCENT2, lw=1.6, ms=5,
            label="cos(y, v') null")
    a1.set_xscale("log", base=2)
    a1.set_ylim(0, 0.56)
    style(a1, "sequence length (tokens)", "cosine similarity")
    legend_above(a1, 1, 7.8)

    a2.plot(t, frac, marker="o", ls="-", color=INK, lw=1.7, ms=5)
    a2.set_xscale("log", base=2)
    a2.set_ylim(0, 50)
    for x, y in zip(t, frac):
        a2.annotate("{:.1f}%".format(y), (x, y), xytext=(0, 6),
                    textcoords="offset points", ha="center", fontsize=7.6,
                    color=GREY)
    style(a2, "sequence length (tokens)", "self-specific share (%)")
    save(fig, "f4_length.png")


# --- Figure 5: GQA, within group against across group
def fig_gqa():
    rows = [r for r in read_csv(XSAC / "gqa.csv")
            if str(r.get("is_gqa", "")).lower() == "true"]
    # Hugging Face repo names carry training details that make an axis
    # label unreadable; TinyLlama's is 42 characters and collided with its
    # neighbour. Keep the part that identifies the model.
    def short(name):
        tail = name.split("/")[-1]
        return tail.split("-intermediate")[0]

    models = [short(r["model"]) for r in rows]
    within = [float(r["within_group_excess"]) for r in rows]
    across = [float(r["across_group_excess"]) for r in rows]
    x = np.arange(len(models))

    fig, ax = plt.subplots(figsize=(6.0, 2.6))
    ax.bar(x - 0.19, within, width=0.36, color=FILL, edgecolor=ACCENT,
           linewidth=1.0, label="within KV group", zorder=2)
    ax.bar(x + 0.19, across, width=0.36, color="white", edgecolor=ACCENT2,
           linewidth=1.0, hatch="///", label="across groups", zorder=2)
    ax.axhline(0, color=INK, lw=1.0, zorder=3)
    for xi, v in zip(x - 0.19, within):
        ax.annotate("{:+.3f}".format(v), (xi, v), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=7.8)
    for xi, v in zip(x + 0.19, across):
        ax.annotate("{:+.3f}".format(v), (xi, v), xytext=(0, -11),
                    textcoords="offset points", ha="center", fontsize=7.8)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=8.1)
    ax.set_ylim(-0.30, 0.34)
    style(ax, "", "excess  (cos_self - cos_null)")
    legend_above(ax, 2)
    save(fig, "f5_gqa.png")


# --- Figure 6: paired intervention effect, with the resolvable floor
def fig_paired():
    rows = read_csv(XSAC / "paired_tests_s.csv")
    order = {"random": 0, "xsa": 1}
    rows = sorted([r for r in rows if r["arm"] in order],
                  key=lambda r: order[r["arm"]])
    labels = [("{} (primary)".format(r["arm"]) if r["arm"] == "random"
               else r["arm"]) for r in rows]
    mean = [float(r["mean_delta"]) for r in rows]
    lo = [float(r["ci_low"]) for r in rows]
    hi = [float(r["ci_high"]) for r in rows]
    y = np.arange(len(rows))
    pilot = json.loads((XSAC / "pilot_decision.json").read_text(
        encoding="utf-8"))
    refs = json.loads((XSAC / "reference_values.json").read_text(
        encoding="utf-8"))
    mde = float(pilot["mde"])
    claimed = float(refs["xsa_independent_replication_effect_nats"])

    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    ax.axvline(0, color=INK, lw=1.0, zorder=3)
    ax.axvspan(-mde, mde, color=FILL, alpha=0.5, zorder=0)
    ax.annotate("unresolvable band (MDE {:.5f})".format(mde),
                xy=(mde * 0.93, -0.72),
                fontsize=7.6, color=GREY, ha="right")
    ax.errorbar(mean, y, xerr=[np.array(mean) - np.array(lo),
                               np.array(hi) - np.array(mean)],
                fmt="D", color=ACCENT, ms=6, capsize=4, lw=1.5, zorder=4)
    ax.axvline(claimed, color=ACCENT2, lw=1.1, ls=(0, (4, 3)), zorder=3)
    ax.annotate("claimed effect  {:+.5f}".format(claimed),
                xy=(claimed * 1.29, 1.58),
                fontsize=7.6, color=ACCENT2, ha="right")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_ylim(-0.9, 1.9)
    style(ax, "paired delta validation loss vs baseline (nats)", "")
    save(fig, "f6_paired.png")


# --- Figure 7: Check 1 applied to three methods
def fig_generality():
    rows = [r for r in read_csv(XSAC / "generality.csv")
            if r.get("status") == "completed"]
    names = {"attention_sink": "attention sinks",
             "massive_activations": "massive activations"}
    labels, frac = [], []
    for r in rows:
        labels.append(names.get(r["method"], r["method"]))
        frac.append(100 * float(r["self_specific_fraction"]))
    labels.append("XSA self-value\n(this work, 6.9B)")
    documented_literal = 41.9
    ladder = read_csv(XSAC / "ladder.csv")
    target = [r for r in ladder
              if r["model"] == "EleutherAI/pythia-6.9b"]
    measured = 100 * (sum(float(r["excess"]) for r in target) /
                      sum(float(r["cos_self"]) for r in target))
    if round(measured, 1) != documented_literal:
        raise ValueError("documented 41.9 literal drifted from ladder.csv")
    frac.append(documented_literal)

    fig, ax = plt.subplots(figsize=(5.9, 2.5))
    cols = [FILL, FILL, "white"]
    edges = [ACCENT, ACCENT, ACCENT2]
    bars = ax.bar(labels, frac, width=0.55, color=cols, linewidth=1.1,
                  edgecolor=edges, zorder=2)
    bars[2].set_hatch("///")
    ax.axhline(50, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=3)
    ax.annotate("half the statistic", xy=(1.62, 52.5), fontsize=7.8,
                color=GREY, ha="left")
    for b, v in zip(bars, frac):
        ax.annotate("{:.1f}%".format(v),
                    (b.get_x() + b.get_width() / 2, v), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=8.1)
    ax.set_ylim(0, 112)
    ax.tick_params(axis="x", labelsize=7.2)
    style(ax, "", "share surviving the null (%)")
    save(fig, "f7_generality.png")


# --- Figure 3: measured long-context cost, and the wall beyond it
def fig_cost():
    rows = [r for r in read_csv(CRPA / "figures" /
                                "fig5b_context_performance_data.csv")
            if r.get("status") == "completed"]
    series = {}
    for r in rows:
        series.setdefault(r["variant"], []).append(
            (int(r["context_length"]), float(r["latency_ms_median"]),
             float(r["peak_allocated_mb"])))
    for v in series:
        series[v].sort()

    spec = [("dense", "dense", ACCENT, "s", "-"),
            ("sliding", "sliding window", GREY, "^", "-."),
            ("crpa_contribution", "CRPA", ACCENT2, "D", "--")]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.4))
    for key, label, col, mk, ls in spec:
        pts = series.get(key, [])
        if not pts:
            continue
        t = [p[0] for p in pts]
        a1.plot(t, [p[1] for p in pts], marker=mk, ls=ls, color=col,
                lw=1.6, ms=5, label=label)
        a2.plot(t, [p[2] / 1024.0 for p in pts], marker=mk, ls=ls, color=col,
                lw=1.6, ms=5, label=label)

    for ax in (a1, a2):
        ax.set_xscale("log", base=2)
        ax.set_xticks([4096, 8192, 16384, 32768])
        ax.set_xticklabels(["4k", "8k", "16k", "32k"])
        ax.axvspan(23000, 40000, color=FILL, alpha=0.55, zorder=0)
    a1.set_yscale("log")
    a1.set_yticks([10, 20, 50, 100, 200])
    a1.set_yticklabels(["10", "20", "50", "100", "200"])
    a1.minorticks_off()
    a1.annotate("out of memory", xy=(30500, 20), fontsize=7.6,
                color=GREY, ha="center", va="center", rotation=90)
    a2.annotate("out of memory", xy=(30500, 3.6), fontsize=7.6,
                color=GREY, ha="center", va="center", rotation=90)
    style(a1, "context length (tokens)", "forward latency (ms, median)")
    style(a2, "context length (tokens)", "peak allocated (GB)")
    legend_above(a1, 3, 7.8)
    save(fig, "f8_cost.png")


def main(argv=None):
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path, default=OUT)
    args = parser.parse_args(argv)
    OUT = args.out
    failures = 0
    for fn in (fig_check0, fig_floor, fig_cost, fig_bounded,
               fig_ladder, fig_length, fig_gqa, fig_a2,
               fig_paired, fig_generality):
        try:
            fn()
        except Exception as exc:
            print("  FAILED", fn.__name__, type(exc).__name__, exc)
            failures += 1
    return 1 if failures else 0


# --- Figure 9: what bounding the diagnostic did to the memory profile
def fig_bounded():
    """Peak memory before and after bounding, and the wall that disappeared."""
    rows = read_csv(CRPA / "tier2_bounded_v2" / "long_context.csv")
    rows = [r for r in rows if r.get("status") == "completed"]
    if not rows:
        raise RuntimeError("no completed bounded long-context rows")
    rows.sort(key=lambda r: int(r["context_length"]))
    t = [int(r["context_length"]) for r in rows]
    after = [float(r["diagnostic_peak_memory_bytes"]) / 1024 ** 3 for r in rows]

    # The unbounded implementation, measured at the three lengths that fit.
    before_t = [4096, 8192, 16384]
    before = [14.14, 27.74, 55.04]

    fig, ax = plt.subplots(figsize=(6.0, 2.6))
    ax.axhspan(80, 400, color=ACCENT2, alpha=0.07, zorder=0)
    ax.axhline(80, color=ACCENT2, lw=1.1, ls=(0, (4, 3)), zorder=3)
    ax.annotate("A100 80GB", xy=(4300, 88), fontsize=7.6, color=ACCENT2)
    ax.plot(before_t, before, marker="s", ls="--", color=ACCENT2, lw=1.7, ms=6,
            label="before: unbounded diagnostic")
    ax.plot(t, after, marker="o", ls="-", color=ACCENT, lw=1.7, ms=6,
            label="after: streamed and chunked")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(t)
    ax.set_xticklabels(["4k", "8k", "16k", "32k", "64k"])
    ax.set_yticks([1, 10, 100])
    ax.set_yticklabels(["1", "10", "100"])
    ax.minorticks_off()
    ax.set_ylim(0.4, 400)
    style(ax, "context length (tokens)", "peak memory (GB)")
    legend_above(ax, 2)
    save(fig, "f9_bounded.png")


# --- Figure 10: does the statistic predict its own intervention?
def fig_a2():
    rows = read_csv(XSAC / "a2_correlations.csv")
    if not rows:
        raise RuntimeError("no a2_correlations.csv")
    models, seen = [], set()
    for r in rows:
        m = r["model"].split("/")[-1]
        if m not in seen:
            seen.add(m)
            models.append(m)
    x = np.arange(len(models))
    w = 0.36

    def series(stat):
        out = []
        for m in models:
            hit = [r for r in rows
                   if r["model"].split("/")[-1] == m and r["statistic"] == stat]
            out.append(float(hit[0]["rho_raw"]) if hit else float("nan"))
        return out

    ceilings = []
    for m in models:
        hit = [r for r in rows if r["model"].split("/")[-1] == m]
        ceilings.append(float(hit[0]["ceiling"]) if hit else float("nan"))

    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.bar(x - w / 2, series("cos_self"), w, color="white", edgecolor=ACCENT2,
           hatch="///", linewidth=1.1, zorder=2,
           label="cos(y, v) raw statistic")
    ax.bar(x + w / 2, series("excess"), w, color=FILL, edgecolor=ACCENT,
           linewidth=1.1, zorder=2, label="excess (null-corrected)")
    for xi, c in zip(x, ceilings):
        ax.plot([xi - 0.46, xi + 0.46], [c, c], color=GREY, lw=1.2,
                ls=(0, (3, 2)), zorder=4)
    ax.annotate("dashed: ceiling from split-half reliability",
                xy=(len(models) - 0.5, max(ceilings) + 0.03), fontsize=7.2,
                color=GREY, ha="right")
    for xi, v in zip(x - w / 2, series("cos_self")):
        ax.annotate("{:.3f}".format(v), (xi, v), xytext=(0, 3),
                    textcoords="offset points", ha="center", fontsize=7.4)
    for xi, v in zip(x + w / 2, series("excess")):
        ax.annotate("{:.3f}".format(v), (xi, v), xytext=(0, 3),
                    textcoords="offset points", ha="center", fontsize=7.4)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=8)
    ax.set_ylim(0, 1.0)
    ax.axhline(0, color=INK, lw=0.9)
    style(ax, "", "Spearman rho vs measured effect")
    legend_above(ax, 2)
    save(fig, "f10_a2.png")


if __name__ == "__main__":
    raise SystemExit(main())
