#!/usr/bin/env python3
"""Convert a script publishing-package markdown file into a formatted PDF."""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def apply_bold(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

def convert(md_path, pdf_path):
    raw = Path(md_path).read_text(encoding="utf-8")
    lines = raw.split("\n")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("DocTitle", parent=styles["Title"], fontSize=18, spaceAfter=14)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceBefore=16, spaceAfter=8, textColor="#1a1a1a")
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5, leading=15, spaceAfter=10, alignment=TA_LEFT)
    meta_style = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=10.5, leading=15, spaceAfter=4, textColor="#333333")

    story = []
    para_buffer = []

    def flush_paragraph(style=body_style):
        if para_buffer:
            text = apply_bold(escape(" ".join(para_buffer).strip()))
            if text:
                story.append(Paragraph(text, style))
            para_buffer.clear()

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("# "):
            flush_paragraph()
            story.append(Paragraph(escape(line[2:].strip()), title_style))
        elif line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(escape(line[3:].strip()), h2_style))
        elif line.strip() == "---":
            flush_paragraph()
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.75, color="#cccccc"))
            story.append(Spacer(1, 6))
        elif line.strip() == "":
            flush_paragraph()
        else:
            para_buffer.append(line.strip())
    flush_paragraph()

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=Path(md_path).stem,
    )
    doc.build(story)

if __name__ == "__main__":
    md_file, pdf_file = sys.argv[1], sys.argv[2]
    convert(md_file, pdf_file)
    print(f"Wrote {pdf_file}")
