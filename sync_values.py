"""Generate report_values.py from the source repositories' result files.

The report used to hardcode every number as a literal string. Nothing tied a
figure in the PDF to the CSV it came from, so the two repositories drifted
silently and a stale number could survive any number of edits. Several did.

This reads the committed result files, records the commit each repository was
at when it read them, and writes ``report_values.py``. ``pdf_content.py``
takes its numbers from there, and ``tests/test_no_drift.py`` regenerates and
compares, so a number that no longer matches its source fails the build
rather than reaching a reader.

    python sync_values.py            # rewrite report_values.py
    python sync_values.py --check    # exit 1 if it is out of date

Source repositories are found via XSAC_REPO and CRPA_REPO, defaulting to
~/xsa-controls and ~/crpa.
"""

import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
XSAC = pathlib.Path(os.environ.get("XSAC_REPO",
                                   os.path.expanduser("~/xsa-controls")))
CRPA = pathlib.Path(os.environ.get("CRPA_REPO", os.path.expanduser("~/crpa")))
OUT = HERE / "report_values.py"


def sha(repo):
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(repo),
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def rows(repo, name):
    path = repo / "results" / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_json(repo, name):
    path = repo / "results" / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def pick(rs, **eq):
    for r in rs:
        if all(str(r.get(k)) == str(v) for k, v in eq.items()):
            return r
    return None


def add(store, key, value, source, selector, fmt="{:+.3f}"):
    """Record one number with where it came from and how it is rendered."""
    if value is None:
        return
    try:
        v = float(value)
    except (TypeError, ValueError):
        return
    store[key] = {"value": v, "text": fmt.format(v),
                  "source": source, "selector": selector}


def collect():
    v = {}

    # --- A2: per-head statistic against measured effect -------------------
    a2 = rows(XSAC, "a2_correlations.csv")
    rel = rows(XSAC, "reliability.csv")
    for model in ("gpt2", "EleutherAI/pythia-160m", "EleutherAI/pythia-410m"):
        short = model.split("/")[-1]
        r = pick(rel, model=model)
        if r:
            add(v, "a2.%s.r_delta" % short, r.get("r_delta"),
                "results/reliability.csv", "model=%s" % model)
            add(v, "a2.%s.seq_len" % short, r.get("seq_len"),
                "results/reliability.csv", "model=%s" % model, "{:.0f}")
            v["a2.%s.verdict" % short] = {
                "value": r.get("verdict"), "text": r.get("verdict"),
                "source": "results/reliability.csv",
                "selector": "model=%s" % model}
        for stat in ("cos_self", "excess"):
            c = pick(a2, model=model, statistic=stat)
            if not c:
                continue
            base = "a2.%s.%s" % (short, stat)
            sel = "model=%s,statistic=%s" % (model, stat)
            add(v, base + ".rho", c.get("rho_raw"),
                "results/a2_correlations.csv", sel)
            add(v, base + ".disatt", c.get("rho_disattenuated"),
                "results/a2_correlations.csv", sel)
            add(v, base + ".ceiling", c.get("ceiling"),
                "results/a2_correlations.csv", sel, "{:.3f}")

    # --- GQA --------------------------------------------------------------
    for g in rows(XSAC, "gqa.csv"):
        if str(g.get("is_gqa")).lower() != "true":
            continue
        short = g["model"].split("/")[-1].split("-intermediate")[0]
        sel = "model=%s" % g["model"]
        add(v, "gqa.%s.within" % short, g.get("within_group_excess"),
            "results/gqa.csv", sel, "{:+.4f}")
        add(v, "gqa.%s.across" % short, g.get("across_group_excess"),
            "results/gqa.csv", sel, "{:+.4f}")
        add(v, "gqa.%s.q_heads" % short, g.get("n_query_heads"),
            "results/gqa.csv", sel, "{:.0f}")
        add(v, "gqa.%s.kv_heads" % short, g.get("n_kv_heads"),
            "results/gqa.csv", sel, "{:.0f}")

    # --- paired tests: primary if it exists, else the labelled pilot ------
    for name, tag in (("paired_tests_s.csv", "primary"),
                      ("paired_tests_s_pilot_5e7.csv", "pilot")):
        pr = rows(XSAC, name)
        if not pr:
            continue
        for r in pr:
            base = "paired.%s.%s" % (tag, r["arm"])
            sel = "arm=%s" % r["arm"]
            src = "results/" + name
            add(v, base + ".mean_delta", r.get("mean_delta"), src, sel,
                "{:+.6f}")
            add(v, base + ".ci_low", r.get("ci_low"), src, sel, "{:+.6f}")
            add(v, base + ".ci_high", r.get("ci_high"), src, sel, "{:+.6f}")
            add(v, base + ".t", r.get("t"), src, sel, "{:+.2f}")
            add(v, base + ".p", r.get("p"), src, sel, "{:.3f}")
            add(v, base + ".n_seeds", r.get("n_seeds"), src, sel, "{:.0f}")
            add(v, base + ".sd_paired", r.get("sd_paired"), src, sel,
                "{:.6f}")
            # Realised MDE, computed rather than quoted. 2.9 is the spec's
            # multiplier for 80% power at alpha 0.05.
            try:
                sd = float(r["sd_paired"])
                n = int(float(r["n_seeds"]))
                add(v, base + ".mde", 2.9 * sd / (n ** 0.5), src,
                    "2.9 * sd_paired / sqrt(n_seeds), " + sel, "{:.5f}")
            except (TypeError, ValueError, KeyError):
                pass
        break

    # --- Day-3 planning forecast, explicitly not a measurement ------------
    pilot = load_json(XSAC, "pilot_decision.json")
    add(v, "planning.sigma_paired", pilot.get("sigma_paired"),
        "results/pilot_decision.json", "Day-3 planning forecast", "{:.5f}")
    add(v, "planning.mde", pilot.get("mde"),
        "results/pilot_decision.json", "Day-3 planning forecast", "{:.5f}")

    # --- CRPA long context ------------------------------------------------
    for r in rows(CRPA, "tier2_bounded_v2/long_context.csv"):
        if r.get("status") != "completed":
            continue
        t = r["context_length"]
        sel = "context_length=%s" % t
        src = "results/tier2_bounded_v2/long_context.csv"
        add(v, "crpa.ctx%s.peak_gb" % t,
            float(r["diagnostic_peak_memory_bytes"]) / 1024 ** 3, src, sel,
            "{:.2f}")
        add(v, "crpa.ctx%s.overlap" % t, r.get("realized_overlap"), src, sel,
            "{:.4f}")
        add(v, "crpa.ctx%s.delta_max" % t, r.get("delta_max"), src, sel,
            "{:.2e}")
    return v


def render(values):
    lines = [
        '"""Numbers for the report, generated from the source repositories.',
        "",
        "DO NOT EDIT. Regenerate with `python sync_values.py`.",
        "",
        "Every entry records the file it came from and the row that selected",
        "it, so a number in the PDF can be traced to a committed measurement",
        "without trusting this file.",
        '"""',
        "",
        "GENERATED = %r" % dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "SOURCES = {",
        "    'xsa_controls': %r," % sha(XSAC),
        "    'crpa': %r," % sha(CRPA),
        "}",
        "",
        "VALUES = {",
    ]
    for k in sorted(values):
        lines.append("    %r: %r," % (k, values[k]))
    lines += ["}", "", "", "def V(key):",
              '    """Rendered text for one value, or a loud marker if absent."""',
              "    entry = VALUES.get(key)",
              "    if entry is None:",
              "        raise KeyError(",
              "            'no generated value for %r; run sync_values.py' % key)",
              "    return entry['text']", "", "",
              "def num(key):",
              '    """The raw value, for arithmetic in the content module."""',
              "    return VALUES[key]['value']", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if report_values.py is out of date")
    args = ap.parse_args(argv)

    values = collect()
    if not values:
        print("no source results found; is XSAC_REPO set?", file=sys.stderr)
        return 1
    text = render(values)

    if args.check:
        if not OUT.exists():
            print("report_values.py does not exist", file=sys.stderr)
            return 1
        old = OUT.read_text(encoding="utf-8")
        # GENERATED and SOURCES move on every run; compare the VALUES block.
        def body(s):
            return s[s.index("VALUES = {"):] if "VALUES = {" in s else s
        if body(old) != body(text):
            print("report_values.py is STALE: a source result has changed. "
                  "Run python sync_values.py", file=sys.stderr)
            return 1
        print("report_values.py matches its sources (%d values)" % len(values))
        return 0

    OUT.write_text(text, encoding="utf-8")
    print("wrote %s with %d values" % (OUT.name, len(values)))
    print("  xsa-controls %s" % sha(XSAC)[:8])
    print("  crpa         %s" % sha(CRPA)[:8])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
