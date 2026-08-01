from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from reportlab import Version

OUT = 'market/SnapBurst-Global-Technical-Need-and-Product-Response.pdf'
PAGE = landscape(A4)
NAVY = HexColor('#17324D')
BLUE = HexColor('#006EAA')
TEXT = HexColor('#26303C')
MUTED = HexColor('#5C6978')
LIGHT = HexColor('#F5F8FB')
GRID = HexColor('#D7DEE8')
CALLOUT = HexColor('#EAF3F8')
CALLOUT_BORDER = HexColor('#8CB9CF')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Kicker', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=11, textColor=BLUE, spaceAfter=5))
styles.add(ParagraphStyle(name='TitleSB', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=NAVY, alignment=TA_LEFT, spaceAfter=8))
styles.add(ParagraphStyle(name='H1SB', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=NAVY, spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle(name='BodySB', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.2, leading=13.2, textColor=TEXT, spaceAfter=8))
styles.add(ParagraphStyle(name='TableHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name='TableText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.7, leading=9.3, textColor=TEXT))
styles.add(ParagraphStyle(name='MarketName', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.9, leading=9.5, textColor=BLUE))
styles.add(ParagraphStyle(name='CommonKey', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.4, leading=10, textColor=BLUE))
styles.add(ParagraphStyle(name='CommonText', parent=styles['Normal'], fontName='Helvetica', fontSize=8.3, leading=10.2, textColor=TEXT))
styles.add(ParagraphStyle(name='Callout', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=BLUE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='FootnoteSB', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.2, leading=10, textColor=MUTED))

markets = [
('United States',
 'Current Remote ID requirements apply to drones that must be registered. The proposed BVLOS rule would add defined operating areas, C2 coverage, lost-link procedures, traffic separation and DAA, cybersecurity, configuration and flight records, and incident reporting.',
 'SnapBurst binds each aircraft to an individual identity and audit record, supplying the aircraft-specific identity used by the required Remote ID output. Approved routes, altitude limits and operating boundaries become enforceable constraints. SnapBurst detects loss or degradation of command authority, enters bounded FreeFlight Recovery, governs proposed DAA manoeuvres, rejects stale or unauthorised commands, and records the decision-to-execution chain.'),
('European Union / EASA',
 'Specific Category and U-space operations require aircraft identification, geo-awareness, flight authorisation, traffic information and containment within the authorised operation. U-space network identification includes aircraft identity, position, route, speed, operator information and emergency status.',
 'SnapBurst applies geographical zones and authorised four-dimensional operating volumes as live governance constraints. Each action is checked against aircraft identity, current authority, mission state and containment rules. Flight authorisations and traffic information can update those constraints, while the aircraft-specific audit record provides evidence of conformance, decisions and responses.'),
('United Kingdom',
 'UK SORA operations require defined flight, contingency and ground-risk volumes, technical and operational evidence, C2 and recovery procedures, and aircraft records. Direct Remote ID has applied to specified UK aircraft classes since 1 January 2026, with wider application scheduled from 1 January 2028.',
 'SnapBurst encodes the approved flight and contingency volumes within the aircraft\'s operating envelope. It maintains the aircraft identity used for Direct Remote ID, monitors command authority, governs continued behaviour during C2 loss, controls restoration and handback, and records authority, proposal, decision, dispatch and aircraft response as one correlated evidence chain.'),
('Japan',
 'Aircraft weighing 100 g or more generally require registration, a displayed registration ID and Remote ID. Regulated operations require permission where applicable, advance flight-plan reporting, route and altitude information, journey logs, inspection records and maintenance records. Level 4 operations require aircraft certification, pilot certification and operational approval.',
 'SnapBurst maintains a unique identity and operational history for each aircraft and supplies that identity to the aircraft\'s Remote ID output. Approved routes, altitudes and operating times become enforceable conditions. Flight activity, governance decisions and aircraft responses are recorded, while inspection, maintenance and abnormal-event records can be linked to the aircraft-specific operational record.'),
('Australia',
 'New BVLOS and complex-operation applications use AusSORA from 11 May 2026. AusSORA assesses ground risk, containment and operational safety objectives. Complex operations also require aircraft, operational, serviceability and supporting-system evidence.',
 'SnapBurst converts the approved operating volume, risk controls and operational conditions into deterministic command constraints. Aircraft identity, command source, mission state, operating boundary and aircraft response are correlated in the audit record. Serviceability and safety-system status can be required before commands are permitted, while fail-closed authority controls protect the aircraft-command path.'),
('Canada',
 'Standard 922 includes containment, C2-link reliability, predictable lost-link behaviour, DAA, control-station information, operator intervention and a demonstrated environmental operating envelope. Compliance evidence must be documented and available to Transport Canada.',
 'SnapBurst governs containment, C2-loss behaviour and controlled operator handback. Environmental limits and subsystem-health states become conditions within the permitted operating envelope. DAA manoeuvres are governed before execution, and the resulting authority state, decision, command and aircraft response are retained as technical evidence supporting compliance assessment.'),
('India',
 'Current rules require aircraft registration and a Unique Identification Number, together with compliance with the Digital Sky green, yellow and red airspace zones. NPNT, real-time tracking and geofencing are identified as safety features that may be mandated through future notification.',
 'SnapBurst binds the aircraft identity, mission authority and current Digital Sky airspace constraints before execution. Green, yellow, red and temporary restricted zones can be represented as operating-envelope rules. Where permission is required, SnapBurst can prevent execution without valid authority. Aircraft identity, position and activity can be supplied to tracking outputs, while geofencing is enforced at command level.')
]

common = [
('Aircraft identity and Remote ID', 'Every aircraft governed by SnapBurst has its own bound identity and independent audit record. That identity can be supplied to the jurisdiction-required Remote ID broadcast or reporting interface.'),
('Geofencing and containment', 'Approved geographical areas, altitude limits, routes, time windows and contingency volumes are enforced before commands reach the flight controller.'),
('C2-loss behaviour', 'SnapBurst detects when the authorised external command path is lost or degraded and enters bounded FreeFlight Recovery under the remaining valid authority.'),
('Restoration of control', 'Returning command authority is validated before controlled handback. Stale, conflicting or unauthorised commands are rejected.'),
('Audit and incident reconstruction', 'SnapBurst records aircraft identity, command source, authority state, proposed action, Permit/Reject/Hold decision, dispatched command and aircraft response.'),
('Human intervention', 'In Manual Flight, the human operator remains in control. SnapBurst records the command source, aircraft identity, command and aircraft response, but does not alter or overrule manual commands. Governed autonomy operates only when an authorised autonomous mode is selected, or when loss of C2 activates the preauthorised FreeFlight Recovery procedure.'),
('Detect and avoid', 'DAA information and proposed avoidance manoeuvres enter SnapBurst as safety-critical inputs and are governed before execution.'),
('Cybersecurity and command integrity', 'Authority validation, fail-closed decisions, replay resistance, stale-command rejection and evidence-conflict handling protect the governed command path.'),
('Multi-aircraft operation', 'Each aircraft retains its own identity, authority state, command lane, operating envelope and evidence record.'),
('Equipment and serviceability', 'Required aircraft equipment, subsystem health and serviceability states can be enforced as prerequisites for permitted operation.'),
('Configuration and assurance evidence', 'Aircraft, mission, governance policy and system-configuration state can be bound to the resulting execution record.')
]

def P(text, style):
    return Paragraph(text, styles[style])

def footer(canvas, doc):
    canvas.saveState()
    w, h = PAGE
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.4)
    canvas.line(14*mm, 12.5*mm, w-14*mm, 12.5*mm)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(14*mm, 7.5*mm, 'SnapBurst  |  Global Technical Need and Product Response')
    canvas.drawRightString(w-14*mm, 7.5*mm, f'Page {doc.page}')
    canvas.restoreState()

def market_table(rows):
    data = [[P('Market','TableHead'), P('Principal technical requirements','TableHead'), P('SnapBurst technical response','TableHead')]]
    for market, req, resp in rows:
        data.append([P(market,'MarketName'), P(req,'TableText'), P(resp,'TableText')])
    t = Table(data, colWidths=[34*mm, 89*mm, 139*mm], repeatRows=1, hAlign='LEFT')
    cmds = [
        ('BACKGROUND',(0,0),(-1,0),NAVY),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.45,GRID),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,0),7),
        ('BOTTOMPADDING',(0,0),(-1,0),7),
        ('TOPPADDING',(0,1),(-1,-1),6),
        ('BOTTOMPADDING',(0,1),(-1,-1),6),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(cmds))
    return t

def common_table(rows):
    data = [[P('Regulatory demand','TableHead'), P('SnapBurst capability','TableHead')]]
    for k,v in rows:
        data.append([P(k,'CommonKey'), P(v,'CommonText')])
    t = Table(data, colWidths=[80*mm, 182*mm], repeatRows=1, hAlign='LEFT')
    cmds = [
        ('BACKGROUND',(0,0),(-1,0),NAVY),
        ('GRID',(0,0),(-1,-1),0.45,GRID),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,0),7),
        ('BOTTOMPADDING',(0,0),(-1,0),7),
        ('TOPPADDING',(0,1),(-1,-1),6),
        ('BOTTOMPADDING',(0,1),(-1,-1),6),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(cmds))
    return t

doc = SimpleDocTemplate(
    OUT,
    pagesize=PAGE,
    leftMargin=14*mm,
    rightMargin=14*mm,
    topMargin=13*mm,
    bottomMargin=17*mm,
    title='SnapBurst - Global Technical Need and Product Response',
    author='SnapBurst',
    subject='Technical mapping of major drone-market requirements to SnapBurst capabilities',
)

story = []
story += [P('SNAPBURST','Kicker'), P('Global Technical Need and Product Response','TitleSB')]
line = Table([['']], colWidths=[262*mm], rowHeights=[1.2*mm])
line.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLUE),('BOX',(0,0),(-1,-1),0,BLUE)]))
story += [line, Spacer(1, 6*mm)]
story += [
    P('Major drone markets use different regulatory frameworks, but higher-risk and BVLOS operations increasingly depend on the same technical capabilities: aircraft identification, authorised-area containment, dependable command-and-control behaviour, predictable responses when communications fail, human intervention, and evidence showing what occurred.','BodySB'),
    P('SnapBurst answers these requirements through one reusable governed-autonomy architecture. Each aircraft has its own identity, authority state, operating envelope and audit record. Mission autonomy proposes actions, SnapBurst determines whether those actions are permitted, and the flight controller executes only permitted commands.','BodySB'),
    P('Market requirements and SnapBurst response','H1SB'),
    market_table(markets[:3]),
    PageBreak(),
    P('Market requirements and SnapBurst response - continued','H1SB'),
    market_table(markets[3:]),
    PageBreak(),
    P('Common technical coverage','H1SB'),
    common_table(common[:6]),
    PageBreak(),
    P('Common technical coverage - continued','H1SB'),
    common_table(common[6:]),
    Spacer(1, 5*mm),
    P('Global product relevance','H1SB'),
    P('SnapBurst does not require a different governance core for each territory. Local airspace data, authority formats, Remote ID protocols, reporting interfaces and approval processes may change, but the underlying technical functions remain consistent.','BodySB'),
    P('Across the United States, Europe, the United Kingdom, Japan, Australia, Canada and India, regulators are repeatedly asking how autonomous aircraft can remain identifiable, contained, controllable and accountable when operating conditions or communications change.','BodySB'),
    P('SnapBurst provides one governed-autonomy architecture designed to answer those recurring technical requirements.','BodySB'),
]
call = Table([[P('Different markets. Different regulatory frameworks. The same underlying need for authorised, bounded and auditable aircraft behaviour.','Callout')]], colWidths=[262*mm])
call.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),CALLOUT),
    ('BOX',(0,0),(-1,-1),0.8,CALLOUT_BORDER),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
]))
story += [call, Spacer(1, 3*mm), P('This document describes technical product capability and regulatory relevance. Territory-specific aircraft certification, operational approval and physical-flight evidence remain separate approval activities.','FootnoteSB')]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f'Built {OUT} with ReportLab {Version}')
