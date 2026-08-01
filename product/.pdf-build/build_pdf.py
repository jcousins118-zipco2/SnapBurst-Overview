from pathlib import Path
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable, ListFlowable, ListItem

ROOT = Path(__file__).resolve().parent
SRC = ''.join((ROOT / f'part-{i:02}.txt').read_text(encoding='utf-8') for i in range(1,5))
OUT = ROOT.parent / 'SnapBurst-Product-Overview.pdf'
NAVY=colors.HexColor('#17324D'); BLUE=colors.HexColor('#116E8A'); PALE=colors.HexColor('#EAF2F5')
MID=colors.HexColor('#647482'); DARK=colors.HexColor('#17212B'); LINE=colors.HexColor('#D5DEE5')
styles=getSampleStyleSheet()
body=ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=12.2, textColor=DARK, spaceAfter=5)
title=ParagraphStyle('TitleSB', parent=styles['Title'], fontName='Helvetica', fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6)
subtitle=ParagraphStyle('SubtitleSB', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14.2, leading=17, textColor=BLUE, spaceAfter=12)
h1=ParagraphStyle('H1SB', parent=styles['Heading1'], fontName='Helvetica', fontSize=17.5, leading=21, textColor=NAVY, spaceBefore=13, spaceAfter=5, keepWithNext=True)
h2=ParagraphStyle('H2SB', parent=styles['Heading2'], fontName='Helvetica', fontSize=13.2, leading=16, textColor=BLUE, spaceBefore=9, spaceAfter=3, keepWithNext=True)
callout=ParagraphStyle('Callout', parent=body, fontName='Helvetica-Bold', fontSize=10.3, leading=13, textColor=NAVY, backColor=PALE, leftIndent=8, rightIndent=8, borderPadding=(4,6,4,6), spaceBefore=4, spaceAfter=7)
bullet_style=ParagraphStyle('BulletText', parent=body, spaceAfter=1.4, leading=11.2)
num_style=ParagraphStyle('NumberText', parent=body, spaceAfter=1.8, leading=11.2)
def inline(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)
def header_footer(canvas, doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5)
    canvas.line(20*mm,h-16*mm,w-20*mm,h-16*mm); canvas.line(20*mm,14*mm,w-20*mm,14*mm)
    canvas.setFont('Helvetica-Bold',7.4); canvas.setFillColor(BLUE)
    canvas.drawString(20*mm,h-12.8*mm,'SNAPBURST  |  PRODUCT OVERVIEW')
    canvas.setFont('Helvetica-Bold',7.2); canvas.setFillColor(MID); canvas.drawCentredString(w/2,9.2*mm,'SnapBurst')
    canvas.setFont('Helvetica',7.4); canvas.drawRightString(w-20*mm,9.2*mm,f'Page {doc.page}')
    canvas.restoreState()
story=[]; first_h2=True; bullets=[]; numbers=[]
def flush():
    global bullets,numbers
    if bullets:
        story.append(ListFlowable([ListItem(Paragraph(inline(x),bullet_style),leftIndent=8) for x in bullets],bulletType='bullet',start='circle',leftIndent=12,bulletFontName='Helvetica',bulletFontSize=7,bulletOffsetY=1.5,spaceAfter=4)); bullets=[]
    if numbers:
        story.append(ListFlowable([ListItem(Paragraph(inline(x),num_style),leftIndent=9) for x in numbers],bulletType='1',leftIndent=15,bulletFontName='Helvetica',bulletFontSize=8.5,bulletOffsetY=1,spaceAfter=4)); numbers=[]
for raw in SRC.splitlines():
    line=raw.rstrip()
    if not line or line=='---': flush(); continue
    if line.startswith('* '):
        if numbers: flush()
        bullets.append(line[2:]); continue
    if re.match(r'^\d+\.\s+',line):
        if bullets: flush()
        numbers.append(re.sub(r'^\d+\.\s+','',line)); continue
    flush()
    if line.startswith('# '): story += [Paragraph(inline(line[2:]),title),HRFlowable(width='100%',thickness=2.2,color=BLUE,spaceBefore=1,spaceAfter=7)]
    elif line.startswith('## '):
        text=line[3:]
        if first_h2: story.append(Paragraph(inline(text),subtitle)); first_h2=False
        else: story += [Paragraph(inline(text),h1),HRFlowable(width='100%',thickness=.55,color=LINE,spaceAfter=5)]
    elif line.startswith('### '): story.append(Paragraph(inline(line[4:]),h2))
    elif line.startswith('**') and line.endswith('**'): story.append(Paragraph(inline(line),callout))
    else: story.append(Paragraph(inline(line),body))
flush()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=20*mm,bottomMargin=18*mm,title='SnapBurst Product Overview',author='SnapSpace Labs',subject='Governed Autonomy for Unmanned Aircraft',pageCompression=1)
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
