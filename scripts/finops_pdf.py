#!/usr/bin/env python3
"""
finops_pdf.py — Generates FINOPS_REPORT.pdf from FINOPS_REPORT.md
Requires: pip install reportlab

Usage:
    python3 scripts/finops_pdf.py
    python3 scripts/finops_pdf.py --input reports/FINOPS_REPORT.md --output reports/FINOPS_REPORT.pdf
"""

import re
import sys
import os
import hashlib
import argparse

# ── Patch md5 for Python 3.8 + FIPS-mode OpenSSL compatibility ───────────
_orig_md5 = hashlib.md5
def _patched_md5(*args, **kwargs):
    kwargs.pop('usedforsecurity', None)
    return _orig_md5(*args, **kwargs)
hashlib.md5 = _patched_md5

try:
    import reportlab.pdfbase.pdfdoc as _pdfdoc
    _pdfdoc.md5 = _patched_md5
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, PageBreak
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

# ── Colors ────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#1a2744')
MID_BLUE    = colors.HexColor('#2e5ba8')
LIGHT_BLUE  = colors.HexColor('#dce8f7')
TABLE_HDR   = colors.HexColor('#1a2744')
TABLE_ALT   = colors.HexColor('#f0f5fc')
TABLE_BDR   = colors.HexColor('#9db8d9')
TEXT_DARK   = colors.HexColor('#1c1c1c')
TEXT_LIGHT  = colors.HexColor('#555555')
GREEN       = colors.HexColor('#1d7a3e')
YELLOW      = colors.HexColor('#92400e')
RED         = colors.HexColor('#b91c1c')

PAGE_W, PAGE_H = A4
ML = 2.2 * cm;  MR = 2.2 * cm;  MT = 2.6 * cm;  MB = 2.0 * cm
CW = PAGE_W - ML - MR

def S(n, **k): return ParagraphStyle(n, **k)

STYLES = {
    'h1':  S('h1',  fontName='Helvetica-Bold',        fontSize=15, textColor=DARK_BLUE,  spaceBefore=16, spaceAfter=4,  leading=19),
    'h2':  S('h2',  fontName='Helvetica-Bold',        fontSize=12, textColor=MID_BLUE,   spaceBefore=12, spaceAfter=3,  leading=15),
    'h3':  S('h3',  fontName='Helvetica-Bold',        fontSize=10.5, textColor=DARK_BLUE, spaceBefore=9, spaceAfter=2, leading=13),
    'h4':  S('h4',  fontName='Helvetica-BoldOblique', fontSize=9.5, textColor=MID_BLUE,  spaceBefore=7,  spaceAfter=2,  leading=12),
    'body':S('body',fontName='Helvetica',             fontSize=8.8, textColor=TEXT_DARK,  spaceBefore=2,  spaceAfter=2,  leading=12),
    'bq':  S('bq',  fontName='Helvetica-Oblique',     fontSize=8.5, textColor=TEXT_LIGHT, spaceBefore=3, spaceAfter=3,  leading=11, leftIndent=18),
    'bull':S('bull',fontName='Helvetica',             fontSize=8.8, textColor=TEXT_DARK,  spaceBefore=2,  spaceAfter=2,  leading=12, leftIndent=14),
    'code':S('code',fontName='Courier',               fontSize=7.8, textColor=TEXT_DARK,  backColor=colors.HexColor('#f5f5f5'), spaceBefore=3, spaceAfter=3, leading=10, leftIndent=10, rightIndent=10),
    'th':  S('th',  fontName='Helvetica-Bold',        fontSize=7.8, textColor=colors.white, leading=10),
    'td':  S('td',  fontName='Helvetica',             fontSize=7.8, textColor=TEXT_DARK,  leading=10),
    'tdr': S('tdr', fontName='Helvetica',             fontSize=7.8, textColor=TEXT_DARK,  leading=10, alignment=TA_RIGHT),
    'tdb': S('tdb', fontName='Helvetica-Bold',        fontSize=7.8, textColor=TEXT_DARK,  leading=10),
}

def on_page(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    yh = PAGE_H - MT + 7
    canvas.setStrokeColor(MID_BLUE); canvas.setLineWidth(0.5)
    canvas.line(ML, yh, PAGE_W - MR, yh)
    canvas.setFont('Helvetica-Bold', 7.5); canvas.setFillColor(DARK_BLUE)
    canvas.drawString(ML, yh + 3, 'AWS FinOps Cost Optimization Report — QC Validated')
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(TEXT_LIGHT)
    canvas.drawRightString(PAGE_W - MR, yh + 3, 'github.com/himanshugohil18/FinOps-Agent')
    yf = MB - 5
    canvas.setStrokeColor(TABLE_BDR); canvas.line(ML, yf, PAGE_W - MR, yf)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(TEXT_LIGHT)
    canvas.drawString(ML, yf - 10, 'Kiro FinOps Agent — READ-ONLY Audit — No resources modified')
    canvas.drawRightString(PAGE_W - MR, yf - 10, f'Page {doc.page}')
    canvas.restoreState()

def inline(txt):
    txt = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', txt)
    txt = re.sub(r'\*\*(.*?)\*\*',     r'<b>\1</b>', txt)
    txt = re.sub(r'\*(.*?)\*',         r'<i>\1</i>', txt)
    txt = re.sub(r'`([^`]+)`',         r'<font name="Courier" size="8">\1</font>', txt)
    txt = re.sub(r'&(?!amp;|lt;|gt;|#)', '&amp;', txt)
    return txt

def strip_emoji(s):
    return re.sub(r'[^\x00-\x7F]+', '', s).strip()

def parse_md_table(lines):
    rows = []
    for ln in lines:
        if re.match(r'^\s*\|[-|: ]+\|\s*$', ln):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    return rows

def build_table(rows):
    if not rows:
        return None
    ncols = max(len(r) for r in rows)
    norm = [r + [''] * (ncols - len(r)) for r in rows]
    cw = CW / ncols
    data = []
    for i, row in enumerate(norm):
        cells = []
        for c in row:
            if i == 0:
                p = Paragraph(inline(strip_emoji(c)), STYLES['th'])
            elif re.match(r'^\s*[\$\-\~]?[\d\.,]+\s*$', c) and c.strip() not in ('', '0'):
                p = Paragraph(inline(c), STYLES['tdr'])
            elif c.startswith('**') and c.endswith('**'):
                p = Paragraph(inline(c), STYLES['tdb'])
            else:
                p = Paragraph(inline(strip_emoji(c)), STYLES['td'])
            cells.append(p)
        data.append(cells)
    ts = TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  TABLE_HDR),
        ('GRID',          (0,0), (-1,-1), 0.35, TABLE_BDR),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, TABLE_ALT]),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ])
    for i, row in enumerate(norm[1:], 1):
        if any('**' in c for c in row):
            ts.add('BACKGROUND', (0,i), (-1,i), LIGHT_BLUE)
            ts.add('FONTNAME',   (0,i), (-1,i), 'Helvetica-Bold')
    t = Table(data, colWidths=[cw]*ncols, repeatRows=1)
    t.setStyle(ts)
    return t

def md_to_story(md):
    elems = []
    lines = md.split('\n')
    i = 0
    in_code, code_buf = False, []
    in_table, tbl_buf = False, []
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            if in_code:
                in_code = False
                elems.append(Paragraph('\n'.join(code_buf).replace('\n','<br/>'), STYLES['code']))
                elems.append(Spacer(1,3)); code_buf = []
            else:
                in_code = True
            i += 1; continue
        if in_code:
            code_buf.append(ln); i += 1; continue
        if '|' in ln and ln.strip().startswith('|'):
            in_table = True; tbl_buf.append(ln); i += 1; continue
        if in_table:
            t = build_table(parse_md_table(tbl_buf))
            if t: elems.extend([Spacer(1,5), t, Spacer(1,5)])
            in_table = False; tbl_buf = []
        if re.match(r'^---+\s*$', ln):
            elems.extend([Spacer(1,3), HRFlowable(width='100%', thickness=0.5, color=TABLE_BDR), Spacer(1,3)])
            i += 1; continue
        m = re.match(r'^(#{1,4}) (.+)', ln)
        if m:
            lvl = len(m.group(1)); txt = strip_emoji(m.group(2))
            key = f'h{lvl}' if lvl <= 4 else 'h4'
            if lvl == 1:
                elems.extend([Spacer(1,6), HRFlowable(width='100%', thickness=1.5, color=DARK_BLUE, spaceAfter=3)])
            elif lvl == 2:
                elems.append(Spacer(1,4))
            elems.append(Paragraph(inline(txt), STYLES[key]))
            if lvl == 2:
                elems.append(HRFlowable(width='100%', thickness=0.6, color=MID_BLUE))
            i += 1; continue
        if ln.startswith('> '):
            elems.append(Paragraph(inline(strip_emoji(ln[2:])), STYLES['bq'])); i += 1; continue
        if re.match(r'^[-*] ', ln):
            txt = strip_emoji(ln[2:])
            if txt:
                elems.append(Paragraph('• ' + inline(txt), STYLES['bull']))
            i += 1; continue
        if re.match(r'^\d+\. ', ln):
            txt = strip_emoji(re.sub(r'^\d+\. ', '', ln))
            elems.append(Paragraph('• ' + inline(txt), STYLES['bull'])); i += 1; continue
        if not ln.strip():
            elems.append(Spacer(1,3)); i += 1; continue
        txt = strip_emoji(ln)
        if txt:
            elems.append(Paragraph(inline(txt), STYLES['body']))
        i += 1
    if in_table and tbl_buf:
        t = build_table(parse_md_table(tbl_buf))
        if t: elems.extend([Spacer(1,5), t, Spacer(1,5)])
    return elems

def build_cover():
    elems = [Spacer(1, 1.8*cm)]
    bar = Table([[Paragraph('AWS FinOps Analysis Agent',
                 ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=24,
                                textColor=colors.white, alignment=TA_CENTER, leading=30))]],
                colWidths=[CW])
    bar.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),
                              ('TOPPADDING',(0,0),(-1,-1),16),('BOTTOMPADDING',(0,0),(-1,-1),16)]))
    elems.append(bar)
    sub = Table([[Paragraph('Cost Optimization Report  ·  QC-Validated  ·  Read-Only',
                 ParagraphStyle('cs', fontName='Helvetica', fontSize=11,
                                textColor=MID_BLUE, alignment=TA_CENTER, leading=14))]],
                colWidths=[CW])
    sub.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT_BLUE),
                              ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    elems.append(sub)
    elems.append(Spacer(1, 0.8*cm))
    ml = ParagraphStyle('ml', fontName='Helvetica-Bold', fontSize=9, textColor=DARK_BLUE, alignment=TA_RIGHT, leading=12)
    mv = ParagraphStyle('mv', fontName='Helvetica',      fontSize=9, textColor=TEXT_DARK,  alignment=TA_LEFT,  leading=12)
    meta = [
        ['Report Date',    '2026-10-04'],
        ['Audit Period',   'Oct 2026 MTD (Oct 1-4) + Sep 2026 (full)'],
        ['Access Level',   'READ-ONLY — No resources modified'],
        ['Report Author',  'Kiro FinOps Agent'],
        ['Repository',     'github.com/himanshugohil18/FinOps-Agent'],
        ['QC Status',      'PASS — Reconciliation difference $0.00 both months'],
    ]
    md = [[Paragraph(k, ml), Paragraph(v, mv)] for k,v in meta]
    mt = Table(md, colWidths=[4.5*cm, CW-4.5*cm])
    mt.setStyle(TableStyle([
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,-2),0.3,TABLE_BDR),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,TABLE_ALT]),
        ('BACKGROUND',(0,0),(0,-1),LIGHT_BLUE),
        ('BOX',(0,0),(-1,-1),0.5,TABLE_BDR),
    ]))
    elems.append(mt)
    elems.append(Spacer(1, 0.8*cm))
    kl = ParagraphStyle('kl', fontName='Helvetica',      fontSize=8.5, textColor=TEXT_LIGHT, alignment=TA_LEFT,  leading=11)
    kv = ParagraphStyle('kv', fontName='Helvetica-Bold', fontSize=10,  textColor=DARK_BLUE,  alignment=TA_RIGHT, leading=13)
    kpis = [
        ['Sep 2026 Net Cost (CE Total)',   '~$0.00',     'Oct 2026 MTD Net Cost (CE Total)',   '~$0.00'],
        ['Sep 2026 Gross (before credits)','$0.4342',    'Oct 2026 MTD Gross',                 '$0.0328'],
        ['Total Resources in Inventory',  '10',          'Active Anomalies',                   '0'],
        ['Confirmed Current Savings',     '$0.00',       'Conditional Exposure (if credits expire)','$2.80/mo'],
    ]
    kd = [[Paragraph(r[0],kl),Paragraph(r[1],kv),Paragraph(r[2],kl),Paragraph(r[3],kv)] for r in kpis]
    kt = Table(kd, colWidths=[5.2*cm, 3.2*cm, 5.2*cm, 4.4*cm])
    kt.setStyle(TableStyle([
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,-2),0.3,TABLE_BDR),
        ('LINEBEFORE',(2,0),(2,-1),0.5,TABLE_BDR),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,TABLE_ALT]),
        ('BOX',(0,0),(-1,-1),0.5,TABLE_BDR),
    ]))
    elems.append(kt)
    elems.append(Spacer(1,0.8*cm))
    disc = Table([[Paragraph(
        'READ-ONLY mode. No AWS resources were created, modified, stopped, or deleted. '
        'All remediation requires explicit human approval. '
        'All costs are AWS Cost Explorer UnblendedCost values.',
        ParagraphStyle('d', fontName='Helvetica-Oblique', fontSize=7.8, textColor=TEXT_LIGHT,
                       alignment=TA_CENTER, leading=11))]],
        colWidths=[CW])
    disc.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f9f9f9')),
        ('BOX',(0,0),(-1,-1),0.4,TABLE_BDR),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    elems.append(disc)
    elems.append(PageBreak())
    return elems

def main():
    parser = argparse.ArgumentParser(description='Generate FinOps PDF from Markdown')
    parser.add_argument('--input',  default='reports/FINOPS_REPORT.md',  help='Input .md file')
    parser.add_argument('--output', default='reports/FINOPS_REPORT.pdf', help='Output .pdf file')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)

    with open(args.input, encoding='utf-8') as f:
        md = f.read()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    doc = SimpleDocTemplate(
        args.output, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title='AWS FinOps Cost Optimization Report',
        author='Kiro FinOps Agent',
        subject='AWS FinOps Audit — github.com/himanshugohil18/FinOps-Agent',
    )
    story = build_cover() + md_to_story(md)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

    sz = os.path.getsize(args.output)
    print(f"✓ PDF generated : {args.output}")
    print(f"  Size          : {sz:,} bytes")
    if sz < 5000:
        print("ERROR: PDF too small — generation may have failed"); sys.exit(1)
    print("  Status        : OK")

if __name__ == '__main__':
    main()
