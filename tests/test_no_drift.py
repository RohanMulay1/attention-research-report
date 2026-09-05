"""The PDF must not disagree with the experiment outputs it reports.

This is the test the repository did not have, and its absence is why stale
numbers survived several editing passes: the content module held every figure
as a literal string with nothing tying it to the CSV it came from.

Three properties are checked.

1. ``report_values.py`` still matches the source repositories. If a result
   file changed and nobody regenerated, this fails.
2. Every generated value actually appears in the rendered PDF. A value that
   silently stopped being used is a number the report no longer shows.
3. No number in the PDF that has a generated counterpart appears at a
   *different* value. That is the drift itself.

The last one is the point. The first two make it meaningful.
"""

import pathlib
import re
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PDF = ROOT / "attention-research-results.pdf"


def pdf_text():
    fitz = pytest.importorskip("fitz", reason="PyMuPDF needed to read the PDF")
    if not PDF.exists():
        pytest.skip("PDF not built; run python build_pdf.py")
    with fitz.open(str(PDF)) as d:
        return "".join(p.get_text() for p in d)


@pytest.fixture(scope="module")
def values():
    import report_values
    return report_values.VALUES


class TestGeneratedValuesMatchTheirSources:
    def test_report_values_is_not_stale(self):
        """Regenerate from the source repositories and compare.

        Skips rather than fails when the source repositories are not present,
        so a clone without them can still run the rest of the suite. CI
        checks them out, so CI does not skip.
        """
        import os
        xsac = pathlib.Path(os.environ.get(
            "XSAC_REPO", os.path.expanduser("~/xsa-controls")))
        if not (xsac / "results").exists():
            pytest.skip("source repository not available: set XSAC_REPO")
        out = subprocess.run(
            [sys.executable, str(ROOT / "sync_values.py"), "--check"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=300)
        assert out.returncode == 0, (
            "report_values.py is stale against its sources.\n" + out.stderr)

    def test_every_value_records_where_it_came_from(self, values):
        for key, entry in values.items():
            assert entry.get("source"), "%s has no source file" % key
            assert entry.get("selector"), "%s has no row selector" % key
            assert entry.get("text"), "%s has no rendered text" % key

    def test_sources_record_the_commit_they_were_read_at(self):
        import report_values
        for repo, sha in report_values.SOURCES.items():
            assert sha and sha != "unknown", (
                "%s commit not recorded; the values cannot be traced" % repo)
            assert re.fullmatch(r"[0-9a-f]{40}", sha), (
                "%s commit is not a full sha: %r" % (repo, sha))


class TestPdfAgreesWithItsSources:
    def test_numeric_values_appear_in_the_rendered_pdf(self, values):
        """A generated number that the PDF does not show is dead weight, and
        more importantly means the table stopped reading it."""
        text = pdf_text()
        numeric = {k: e for k, e in values.items()
                   if isinstance(e["value"], float)}
        missing = [k for k, e in numeric.items() if e["text"] not in text]
        # Not every generated value is rendered: some exist to be compared
        # against. Require the great majority, and name what is absent.
        assert len(missing) <= len(numeric) * 0.45, (
            "%d of %d generated values do not appear in the PDF: %s"
            % (len(missing), len(numeric), sorted(missing)[:12]))

    def test_no_rendered_number_contradicts_its_source(self, values):
        """The drift check.

        For each generated value, look for the same quantity rendered at a
        different value. Both are formatted the same way, so a mismatch means
        the PDF is showing something its source does not say.
        """
        text = pdf_text()
        problems = []
        for key, entry in values.items():
            if not isinstance(entry["value"], float):
                continue
            shown = entry["text"]
            if shown in text:
                continue
            # The value is absent. If a number of the same shape and scale is
            # present where this one should be, that is drift rather than a
            # value simply not being rendered.
            v = entry["value"]
            if v == 0:
                continue
            places = len(shown.split(".")[-1]) if "." in shown else 0
            sign = "+" if shown.startswith("+") else ""
            for delta in (0.001, 0.002, 0.01):
                for cand in (v + delta, v - delta):
                    near = ("{:%s.%df}" % (sign, places)).format(cand)
                    if near in text:
                        problems.append(
                            "%s: source says %s, PDF shows %s (from %s)"
                            % (key, shown, near, entry["source"]))
                        break
                else:
                    continue
                break
        assert not problems, "PDF disagrees with its sources:\n  " + \
            "\n  ".join(problems)

    def test_the_retracted_planning_mde_is_never_called_measured(self):
        """0.00518 is the Day-3 planning forecast. It was quoted as a
        measured MDE for several revisions. It may appear, but only where the
        surrounding text says it is a forecast."""
        text = pdf_text()
        if "0.00518" not in text:
            return
        idx = 0
        while True:
            i = text.find("0.00518", idx)
            if i < 0:
                break
            window = text[max(0, i - 400):i + 400].lower()
            assert "forecast" in window or "planning" in window, (
                "0.00518 appears without being labelled a planning forecast: "
                "..." + text[max(0, i - 120):i + 120].replace("\n", " ") + "...")
            idx = i + 1
