"""Lean results PDF: tables only, one or two lines of explanation each."""

import os
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                               PageBreak, PageTemplate, Paragraph, Spacer,
                               Table, TableStyle)

# Output path. Defaults beside this file so a clone builds with no setup;
# override with REPORT_OUT to write elsewhere.
OUT = os.environ.get(
    "REPORT_OUT",
    str(pathlib.Path(__file__).parent / "attention-research-results.pdf"))

INK = colors.HexColor("#111111")
GREY = colors.HexColor("#5a5a5a")
LIGHT = colors.HexColor("#8a8a8a")
RULE = colors.HexColor("#111111")
HAIR = colors.HexColor("#cccccc")
BAND = colors.HexColor("#f4f4f4")

U = 9          # spacing unit; every vertical gap is a multiple of it
TIGHT = U      # inside a block: heading to note, note to table
NEAR = U * 2   # a block and the figure that belongs to it
APART = U * 3  # between sections

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 20 * mm, 18 * mm, 20 * mm, 18 * mm
W = PAGE_W - ML - MR
FRAME_H = PAGE_H - MT - MB


def st(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=10, leading=14.5,
                textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(**base)


TITLE = st("t", fontName="Helvetica-Bold", fontSize=21, leading=24,
           spaceAfter=TIGHT / 2)
SUBTITLE = st("s", fontSize=10.8, leading=15, textColor=GREY)
H1 = st("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=18, spaceAfter=TIGHT / 3)
H1NUM = st("hn", fontName="Helvetica-Bold", fontSize=8.6, leading=11,
           textColor=LIGHT, spaceAfter=TIGHT / 2)
APPROACH = st("ap", fontName="Helvetica-Oblique", fontSize=10.2, leading=14.5,
              textColor=GREY, spaceAfter=0)
H2 = st("h2", fontName="Helvetica-Bold", fontSize=11.4, leading=15.5,
        spaceBefore=APART, spaceAfter=TIGHT)
NOTE = st("n", fontSize=9.3, leading=14, textColor=GREY, spaceAfter=0)
CELL = st("c", fontSize=9.1, leading=12.8)
CELLB = st("cb", fontName="Helvetica-Bold", fontSize=9.1, leading=12.8)
CELLR = st("cr", fontSize=9.1, leading=12.8, alignment=2)
CELLBR = st("cbr", fontName="Helvetica-Bold", fontSize=9.1, leading=12.8,
            alignment=2)
HEADC = st("hc", fontName="Helvetica-Bold", fontSize=8.3, leading=11.5)
HEADR = st("hr", fontName="Helvetica-Bold", fontSize=8.3, leading=11.5,
           alignment=2)


def P(t, s=NOTE):
    return Paragraph(t, s)


def table(header, rows, widths, aligns=None, band=(), bold=()):
    aligns = aligns or (["l"] + ["r"] * (len(header) - 1))

    def mk(txt, a, b=False):
        if a == "r":
            return Paragraph(txt, CELLBR if b else CELLR)
        return Paragraph(txt, CELLB if b else CELL)

    data = [[Paragraph(h, HEADR if a == "r" else HEADC)
             for h, a in zip(header, aligns)]]
    for i, row in enumerate(rows):
        data.append([mk(c, a, i in bold) for c, a in zip(row, aligns)])
    style = [("TOPPADDING", (0, 0), (-1, -1), U * 0.85),
             ("BOTTOMPADDING", (0, 0), (-1, -1), U * 0.85),
             ("LEFTPADDING", (0, 0), (-1, -1), 0),
             ("RIGHTPADDING", (0, 0), (-1, -1), U),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEABOVE", (0, 0), (-1, 0), 0.9, RULE),
             ("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE),
             ("LINEBELOW", (0, -1), (-1, -1), 0.9, RULE)]
    for r in band:
        style.append(("BACKGROUND", (0, r + 1), (-1, r + 1), BAND))
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def hrule(thick=0.9):
    t = Table([[""]], colWidths=[W], rowHeights=[0.1])
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), thick, RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


CAPTION = st("cap", fontSize=8.5, leading=12.6, textColor=GREY,
             spaceAfter=0)
FIGDIR = pathlib.Path(__file__).parent / "figs"


def figure(name, caption, width=0.85):
    """An image with its caption, kept on one page.

    Width is a fraction of the text column. reportlab needs an explicit
    height, so it is derived from the file's own aspect ratio rather than
    guessed, which keeps the plot from being stretched.
    """
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Image

    path = FIGDIR / name
    iw, ih = ImageReader(str(path)).getSize()
    w = W * width
    img = Image(str(path), width=w, height=w * ih / iw)
    img.hAlign = "LEFT"
    return [KeepTogether([Spacer(1, NEAR), img, Spacer(1, TIGHT),
                          P(caption, CAPTION)])]


def block_height(parts):
    """Height the flowables need, for deciding whether to glue them."""
    h = 0.0
    for f in parts:
        try:
            h += f.wrap(W, FRAME_H)[1]
        except Exception:
            h += 12
    return h


def sec(heading, note, tbl, band=(), bold=(), after=None):
    """Heading, a line or two, table, and optional trailing commentary.

    Short blocks are glued so a heading never sits alone at a page foot. A
    block taller than half the frame is left loose instead: gluing one of
    those stalls it to the next page and strands most of the current one,
    which reads worse than a table continuing over the break. The table
    repeats its header row when it does split.
    """
    parts = [P(heading, H2), P(note), Spacer(1, TIGHT), tbl]
    if after:
        parts += [Spacer(1, TIGHT), P(after)]
    if block_height(parts) > 0.5 * FRAME_H:
        return [KeepTogether(parts[:3] + [Spacer(1, 0)])] + parts[3:]
    return [KeepTogether(parts)]


def project(num, title, approach):
    return KeepTogether([P(num, H1NUM), P(title, H1), P(approach, APPROACH),
                         Spacer(1, TIGHT), hrule()])


def on_page(c, d):
    c.saveState()
    c.setFont("Helvetica", 7.4)
    c.setFillColor(LIGHT)
    c.drawString(ML, MB - 11, "Attention research: results")
    c.drawRightString(PAGE_W - MR, MB - 11, str(c.getPageNumber()))
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.4)
    c.line(ML, MB - 6, PAGE_W - MR, MB - 6)
    c.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR,
                      topMargin=MT, bottomMargin=MB,
                      title="Attention research: results",
                      author="Rohan Mulay")
doc.addPageTemplates([PageTemplate(
    id="b", frames=[Frame(ML, MB, W, PAGE_H - MT - MB, leftPadding=0,
                          rightPadding=0, topPadding=0, bottomPadding=0)],
    onPage=on_page)])

S = []
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pdf_content import (CLOSING, P1_APPROACH, P1_SECTIONS, P1_TITLE,
                         P2_APPROACH, P2_SECTIONS, P2_TITLE)


def build(spec):
    if "figure" in spec:
        return figure(spec["figure"], spec["caption"],
                      spec.get("width", 0.85))
    return sec(spec["head"], spec["note"],
               table(spec["header"], spec["rows"],
                     [W * w for w in spec["widths"]],
                     aligns=spec.get("aligns"), band=spec.get("band", ()),
                     bold=spec.get("bold", ())),
               after=spec.get("after"))


S.append(P("Attention Research", TITLE))
S.append(P("Results across two projects", SUBTITLE))
S.append(Spacer(1, APART))

S.append(project("PROJECT 1", P1_TITLE, P1_APPROACH))
for spec in P1_SECTIONS:
    S.extend(build(spec))

S.append(PageBreak())
S.append(project("PROJECT 2", P2_TITLE, P2_APPROACH))
for spec in P2_SECTIONS:
    S.extend(build(spec))

S.extend(build(CLOSING))

grouped, buf = [], []


def flush():
    if not buf:
        return
    if len(buf) == 1:
        grouped.append(buf[0])
    else:
        h = 0.0
        for f in buf:
            try:
                h += f.wrap(W, FRAME_H)[1]
            except Exception:
                h += 12
        grouped.extend(buf) if h > 0.5 * FRAME_H else grouped.append(
            KeepTogether(list(buf)))
    buf.clear()


for f in S:
    if isinstance(f, (PageBreak, KeepTogether)):
        flush()
        grouped.append(f)
        continue
    buf.append(f)
flush()

doc.build(grouped)
print("wrote", OUT)
