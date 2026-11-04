# -*- coding: utf-8 -*-
"""Genera el PDF 'Plan para aprender a dibujar desde cero'.

Uso:  python3 generar_plan.py [ruta_salida.pdf]
Requiere: reportlab y las fuentes Liberation Sans y DejaVu Sans instaladas.
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, CondPageBreak, NextPageTemplate,
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle, Polygon
from reportlab.platypus.flowables import Flowable, HRFlowable

OUT = sys.argv[1] if len(sys.argv) > 1 else "Plan_aprender_a_dibujar.pdf"

# ---------------------------------------------------------------- fuentes
LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Body", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", LIB + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", LIB + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", LIB + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", LIB + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sym", DJV + "DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                              italic="Body-Italic", boldItalic="Body-BoldItalic")

# ---------------------------------------------------------------- colores
INK = colors.HexColor("#1F2A44")
MUTED = colors.HexColor("#5B6475")
ACCENT = colors.HexColor("#C8553D")
PAPER = colors.HexColor("#F6F1E9")
RULE = colors.HexColor("#D9D2C5")
GREEN = colors.HexColor("#2E7D5B")
AMBER = colors.HexColor("#B7791F")
GREY = colors.HexColor("#6B7280")
PHASE = {
    0: colors.HexColor("#8A8F98"),
    1: colors.HexColor("#3F6E96"),
    2: colors.HexColor("#5E8445"),
    3: colors.HexColor("#B7792F"),
    4: colors.HexColor("#B5523B"),
    5: colors.HexColor("#6F4A85"),
}
PHASE_TINT = {
    1: colors.HexColor("#E7EEF5"),
    2: colors.HexColor("#ECF2E6"),
    3: colors.HexColor("#F6EEE2"),
    4: colors.HexColor("#F6E7E3"),
    5: colors.HexColor("#EEE8F3"),
}

ARROW = '<font name="Sym">→</font>'
BOX = '<font name="Sym">☐</font>'
DOT = '<font name="Sym">•</font>'

TAG_E = '<font color="#2E7D5B"><b>[EVIDENCIA]</b></font>'
TAG_P = '<font color="#B7791F"><b>[EVIDENCIA PARCIAL]</b></font>'
TAG_O = '<font color="#6B7280"><b>[OPINIÓN]</b></font>'

# ---------------------------------------------------------------- estilos
def S(name, **kw):
    base = dict(fontName="Body", fontSize=10, leading=14.2, textColor=INK,
                spaceAfter=5)
    base.update(kw)
    return ParagraphStyle(name, **base)

sBody = S("body")
sSmall = S("small", fontSize=8.6, leading=11.6, spaceAfter=0)
sSmallMuted = S("smallmuted", fontSize=8.4, leading=11.2, textColor=MUTED, spaceAfter=0)
sCell = S("cell", fontSize=8.7, leading=11.6, spaceAfter=0)
sCellB = S("cellb", fontName="Body-Bold", fontSize=8.7, leading=11.6, spaceAfter=0)
sCellHead = S("cellhead", fontName="Body-Bold", fontSize=8.7, leading=11, textColor=colors.white, spaceAfter=0)
sH1 = S("h1", fontName="Serif-Bold", fontSize=21, leading=25, spaceBefore=4, spaceAfter=10)
sH2 = S("h2", fontName="Body-Bold", fontSize=13.5, leading=17, spaceBefore=10, spaceAfter=5)
sH3 = S("h3", fontName="Body-Bold", fontSize=11, leading=14, spaceBefore=7, spaceAfter=3)
sBullet = S("bullet", leftIndent=12, bulletIndent=2, spaceAfter=3)
sCalloutTitle = S("ctitle", fontName="Body-Bold", fontSize=9.6, leading=12.5, spaceAfter=3)
sCallout = S("callout", fontSize=9.4, leading=13.2, spaceAfter=3)
sCalloutBullet = S("cbullet", fontSize=9.4, leading=13.2, leftIndent=11, bulletIndent=1, spaceAfter=2)


def P(text, style=sBody):
    return Paragraph(text, style)


def bullets(items, style=sBullet):
    return [Paragraph(t, style, bulletText="•") for t in items]


def callout(title, items, color=ACCENT, bg=PAPER, width=17.8 * cm):
    """Caja destacada. items: lista de str (párrafos) o ('b', str) para viñetas."""
    flow = []
    if title:
        flow.append(Paragraph(f'<font color="{color.hexval()}">{title}</font>', sCalloutTitle))
    for it in items:
        if isinstance(it, tuple):
            flow.append(Paragraph(it[1], sCalloutBullet, bulletText="•"))
        else:
            flow.append(Paragraph(it, sCallout))
    t = Table([[flow]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 7)])


def grid_table(rows, widths, head_color=INK, zebra=True, font_style=sCell, head=True, row_heights=None):
    data = []
    for r_i, row in enumerate(rows):
        cells = []
        for c in row:
            if isinstance(c, str):
                st = sCellHead if (head and r_i == 0) else font_style
                cells.append(Paragraph(c, st))
            else:
                cells.append(c)
        data.append(cells)
    t = Table(data, colWidths=widths, rowHeights=row_heights, repeatRows=1 if head else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
    ]
    if head:
        style += [("BACKGROUND", (0, 0), (-1, 0), head_color)]
    if zebra:
        start = 1 if head else 0
        for i in range(start, len(rows)):
            if (i - start) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#FBF8F3")))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- diagramas
W_FULL = 17.8 * cm


def session_diagram(title, segments, total):
    """segments: (minutos, etiqueta, color, texto_claro)."""
    h = 2.55 * cm
    d = Drawing(W_FULL, h)
    d.add(String(0, h - 11, title, fontName="Body-Bold", fontSize=9.5, fillColor=INK))
    bar_y = h - 1.45 * cm
    bar_h = 0.72 * cm
    x = 0
    scale = W_FULL / total
    t = 0
    for mins, label, col, light in segments:
        w = mins * scale
        d.add(Rect(x, bar_y, w - 1.2, bar_h, fillColor=col, strokeColor=None))
        fs = 7.4 if w > 1.6 * cm else 6.4
        txt_col = colors.white if light else INK
        if w > 0.9 * cm:
            d.add(String(x + w / 2, bar_y + bar_h / 2 - 2.6, f"{mins}′",
                         fontName="Sym", fontSize=fs, fillColor=txt_col, textAnchor="middle"))
        d.add(String(x + 1, bar_y - 10, label, fontName="Body", fontSize=6.7,
                     fillColor=MUTED, textAnchor="start"))
        d.add(String(x + 1, bar_y + bar_h + 3, f"{t}", fontName="Body", fontSize=6.3,
                     fillColor=MUTED))
        x += w
        t += mins
    d.add(String(W_FULL - 1, bar_y + bar_h + 3, f"{total} min", fontName="Body",
                 fontSize=6.3, fillColor=MUTED, textAnchor="end"))
    return d


def grid_removal_diagram():
    d = Drawing(W_FULL, 3.7 * cm)
    sq = 2.3 * cm
    gap = (W_FULL - 4 * sq) / 3
    labels = [("Semana 1", "cuadrícula 4×4"), ("Semana 2", "cuadrícula 2×2"),
              ("Semana 3", "solo cruz central"), ("Semana 4", "nada: tú mides")]
    for i, (wk, desc) in enumerate(labels):
        x0 = i * (sq + gap)
        y0 = 0.95 * cm
        d.add(Rect(x0, y0, sq, sq, fillColor=colors.white, strokeColor=INK, strokeWidth=1))
        n = [4, 2, None, 0][i]
        if n:
            for k in range(1, n):
                d.add(Line(x0 + sq * k / n, y0, x0 + sq * k / n, y0 + sq, strokeColor=PHASE[1], strokeWidth=0.7))
                d.add(Line(x0, y0 + sq * k / n, x0 + sq, y0 + sq * k / n, strokeColor=PHASE[1], strokeWidth=0.7))
        elif n is None:
            d.add(Line(x0 + sq / 2, y0, x0 + sq / 2, y0 + sq, strokeColor=PHASE[1], strokeWidth=0.7, strokeDashArray=[2, 2]))
            d.add(Line(x0, y0 + sq / 2, x0 + sq, y0 + sq / 2, strokeColor=PHASE[1], strokeWidth=0.7, strokeDashArray=[2, 2]))
        # una figura sencilla dentro (jarrón esquemático)
        cx = x0 + sq / 2
        d.add(Circle(cx, y0 + sq * 0.62, sq * 0.17, fillColor=None, strokeColor=ACCENT, strokeWidth=1.1))
        d.add(Polygon([cx - sq * 0.12, y0 + sq * 0.47, cx + sq * 0.12, y0 + sq * 0.47,
                       cx + sq * 0.2, y0 + sq * 0.15, cx - sq * 0.2, y0 + sq * 0.15],
                      fillColor=None, strokeColor=ACCENT, strokeWidth=1.1))
        d.add(String(x0 + sq / 2, y0 - 12, wk, fontName="Body-Bold", fontSize=8, fillColor=INK, textAnchor="middle"))
        d.add(String(x0 + sq / 2, y0 - 22, desc, fontName="Body", fontSize=7.4, fillColor=MUTED, textAnchor="middle"))
        if i < 3:
            ax = x0 + sq + gap * 0.25
            d.add(String(ax + gap * 0.25, y0 + sq / 2 - 4, "→", fontName="Sym", fontSize=14,
                         fillColor=MUTED, textAnchor="middle"))
    return d


def vp_diagram():
    w, h = W_FULL, 5.5 * cm
    d = Drawing(w, h)
    H = h * 0.84
    x1, x2 = 0.6 * cm, w - 0.6 * cm
    d.add(Line(0, H, w, H, strokeColor=PHASE[2], strokeWidth=1.2))
    d.add(String(w / 2, H + 5, "LÍNEA DE HORIZONTE  =  altura de tus ojos (o de la cámara)",
                 fontName="Body-Bold", fontSize=7.6, fillColor=PHASE[2], textAnchor="middle"))
    for x, lab in ((x1, "PF 1"), (x2, "PF 2")):
        d.add(Circle(x, H, 3, fillColor=ACCENT, strokeColor=None))
        d.add(String(x, H - 13, lab, fontName="Body-Bold", fontSize=8, fillColor=ACCENT, textAnchor="middle"))

    c = w * 0.47
    b0, b1 = 0.55 * cm, 2.6 * cm  # caja debajo del horizonte

    def toward(px, py, vx, t):
        return px + t * (vx - px), py + t * (H - py)

    tL, tR = 0.30, 0.22
    Lt = toward(c, b1, x1, tL)
    Lb = toward(c, b0, x1, tL)
    Rt = toward(c, b1, x2, tR)
    Rb = toward(c, b0, x2, tR)

    def intersect(p1, p2, p3, p4):
        (xA, yA), (xB, yB), (xC, yC), (xD, yD) = p1, p2, p3, p4
        den = (xA - xB) * (yC - yD) - (yA - yB) * (xC - xD)
        px = ((xA * yB - yA * xB) * (xC - xD) - (xA - xB) * (xC * yD - yC * xD)) / den
        py = ((xA * yB - yA * xB) * (yC - yD) - (yA - yB) * (xC * yD - yC * xD)) / den
        return px, py

    Bt = intersect(Lt, (x2, H), Rt, (x1, H))
    dash = dict(strokeColor=ACCENT, strokeWidth=0.6, strokeDashArray=[3, 2])
    for p, vx in ((Lt, x2), (Rt, x1), ((c, b1), x1), ((c, b1), x2), ((c, b0), x1), ((c, b0), x2),
                  (Lb, x2), (Rb, x1)):
        d.add(Line(p[0], p[1], vx, H, **dash))
    solid = dict(strokeColor=INK, strokeWidth=1.6)
    edges = [((c, b0), (c, b1)), (Lb, Lt), (Rb, Rt), ((c, b1), Lt), ((c, b1), Rt),
             ((c, b0), Lb), ((c, b0), Rb), (Lt, Bt), (Rt, Bt)]
    for a, b in edges:
        d.add(Line(a[0], a[1], b[0], b[1], **solid))
    d.add(String(Rb[0] + 1.0 * cm, b0 + 1.3 * cm, "las verticales siguen verticales", fontName="Sym",
                 fontSize=7, fillColor=MUTED))
    d.add(String(Rb[0] + 1.0 * cm, b0 + 0.97 * cm, "y paralelas  →  2 puntos de fuga", fontName="Sym",
                 fontSize=7, fillColor=MUTED))
    d.add(String(x1 + 0.3 * cm, 0.2 * cm,
                 "Líneas punteadas: prolonga con regla los bordes que en la realidad son paralelos.",
                 fontName="Body", fontSize=7.2, fillColor=MUTED))
    return d


def roadmap_diagram():
    w, h = W_FULL, 3.0 * cm
    d = Drawing(w, h)
    total = 27  # semana 0 + 26
    scale = w / total
    y = 1.25 * cm
    bh = 0.75 * cm
    phases = [(0, 0, 1, "Sem. 0"), (1, 1, 5, "1 · Ver y medir"), (2, 5, 10, "2 · Volumen y perspectiva"),
              (3, 10, 16, "3 · La cabeza"), (4, 16, 23, "4 · La figura"), (5, 23, 27, "5 · Personaje")]
    for ph, a, b, lab in phases:
        x = a * scale
        ww = (b - a) * scale
        d.add(Rect(x, y, ww - 1.5, bh, fillColor=PHASE[ph], strokeColor=None))
        d.add(String(x + ww / 2, y + bh / 2 - 3, lab, fontName="Body-Bold",
                     fontSize=7.2 if ph else 6.2, fillColor=colors.white, textAnchor="middle"))
    for wk in (0, 4, 9, 15, 22, 26):
        x = (wk + 0.5) * scale
        d.add(Polygon([x - 4, y - 3, x + 4, y - 3, x, y - 10], fillColor=ACCENT, strokeColor=None))
        d.add(String(x, y - 20, f"S{wk}", fontName="Body-Bold", fontSize=7, fillColor=ACCENT, textAnchor="middle"))
    d.add(String(0, h - 9, "▼ = diagnóstico (repites los mismos 6 dibujos y comparas)",
                 fontName="Sym", fontSize=7.2, fillColor=MUTED))
    return d


# ---------------------------------------------------------------- plantillas de página
def on_cover(canv, doc):
    W, H = letter
    canv.saveState()
    canv.setFillColor(PAPER)
    canv.rect(0, 0, W, H, fill=1, stroke=0)
    # bandas de fases
    band_h = 0.55 * cm
    for i in range(1, 6):
        canv.setFillColor(PHASE[i])
        canv.rect((i - 1) * W / 5, H - band_h, W / 5, band_h, fill=1, stroke=0)
    # caja en perspectiva decorativa
    canv.setStrokeColor(INK)
    canv.setLineWidth(1.4)
    hx = H * 0.36
    vp1, vp2 = 2.2 * cm, W - 2.2 * cm
    canv.setStrokeColor(PHASE[2])
    canv.setLineWidth(0.8)
    canv.line(1.5 * cm, hx, W - 1.5 * cm, hx)
    canv.setFillColor(ACCENT)
    canv.circle(vp1, hx, 3, fill=1, stroke=0)
    canv.circle(vp2, hx, 3, fill=1, stroke=0)
    c = W * 0.5
    top, bot = hx - 1.6 * cm, hx - 5.6 * cm

    def tw(px, py, vx, t):
        return px + t * (vx - px), py + t * (hx - py)

    Lt, Lb = tw(c, top, vp1, 0.33), tw(c, bot, vp1, 0.33)
    Rt, Rb = tw(c, top, vp2, 0.26), tw(c, bot, vp2, 0.26)

    def isect(p1, p2, p3, p4):
        (xA, yA), (xB, yB), (xC, yC), (xD, yD) = p1, p2, p3, p4
        den = (xA - xB) * (yC - yD) - (yA - yB) * (xC - xD)
        px = ((xA * yB - yA * xB) * (xC - xD) - (xA - xB) * (xC * yD - yC * xD)) / den
        py = ((xA * yB - yA * xB) * (yC - yD) - (yA - yB) * (xC * yD - yC * xD)) / den
        return px, py

    Bt = isect(Lt, (vp2, hx), Rt, (vp1, hx))
    canv.setDash(3, 2)
    canv.setStrokeColor(ACCENT)
    canv.setLineWidth(0.5)
    for p, vx in (((c, top), vp1), ((c, top), vp2), ((c, bot), vp1), ((c, bot), vp2), (Lt, vp2), (Rt, vp1)):
        canv.line(p[0], p[1], vx, hx)
    canv.setDash()
    canv.setStrokeColor(INK)
    canv.setLineWidth(1.6)
    for a, b in (((c, bot), (c, top)), (Lb, Lt), (Rb, Rt), ((c, top), Lt), ((c, top), Rt),
                 ((c, bot), Lb), ((c, bot), Rb), (Lt, Bt), (Rt, Bt)):
        canv.line(a[0], a[1], b[0], b[1])
    # textos
    canv.setFillColor(MUTED)
    canv.setFont("Body-Bold", 10)
    canv.drawString(2.2 * cm, H - 3.0 * cm, "PLAN PERSONAL DE DIBUJO  ·  VERSIÓN 2.0 (DÍA POR DÍA)  ·  NOVIEMBRE 2026")
    canv.setFillColor(INK)
    canv.setFont("Serif-Bold", 38)
    canv.drawString(2.2 * cm, H - 5.0 * cm, "Aprender a dibujar")
    canv.drawString(2.2 * cm, H - 6.5 * cm, "desde cero")
    canv.setFont("Body", 14)
    canv.setFillColor(INK)
    canv.drawString(2.2 * cm, H - 7.9 * cm, "135 sesiones (26 semanas + semana 0) para pasar de copiar con cuadrícula")
    canv.drawString(2.2 * cm, H - 8.6 * cm, "a construir tus propios personajes en perspectiva")
    canv.setFont("Body", 10.5)
    canv.setFillColor(MUTED)
    lines = [
        "1–2 horas al día  ·  pensado para practicar sin internet",
        "Basado en investigación sobre dibujo y aprendizaje, marcando qué es evidencia y qué es opinión",
        "Incluye: qué hacer cada día, materiales, sesiones con descansos, recursos descargables,",
        "hojas de diagnóstico y bitácora para imprimir",
    ]
    for i, ln in enumerate(lines):
        canv.drawString(2.2 * cm, H - 10.0 * cm - i * 0.55 * cm, ln)
    canv.setFillColor(MUTED)
    canv.setFont("Body", 8.5)
    canv.drawString(2.2 * cm, 1.6 * cm, "Elaborado con Claude como tutor. Úsalo, táchalo, rómpelo: es una guía, no una regla.")
    canv.restoreState()


def on_page(canv, doc):
    W, H = letter
    canv.saveState()
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(1.9 * cm, H - 1.35 * cm, W - 1.9 * cm, H - 1.35 * cm)
    canv.setFont("Body", 7.8)
    canv.setFillColor(MUTED)
    canv.drawString(1.9 * cm, H - 1.15 * cm, "Aprender a dibujar desde cero · plan de 26 semanas")
    canv.drawRightString(W - 1.9 * cm, 1.1 * cm, f"{doc.page}")
    canv.restoreState()


class PhaseHeader(Flowable):
    def __init__(self, num, title, weeks, width=W_FULL):
        super().__init__()
        self.num, self.title, self.weeks, self.width = num, title, weeks, width
        self.height = 1.45 * cm

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(PHASE[self.num])
        c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Body-Bold", 9)
        c.drawString(0.45 * cm, self.height - 0.55 * cm, f"FASE {self.num}  ·  {self.weeks}")
        c.setFont("Serif-Bold", 16)
        c.drawString(0.45 * cm, 0.3 * cm, self.title)


# ---------------------------------------------------------------- contenido
story = [NextPageTemplate("normal"), PageBreak()]  # la portada se dibuja en la primera página

# ---- Cómo usar
story.append(P("Cómo usar este documento", sH1))
story += bullets([
    "<b>Léelo completo una vez</b> (unos 40 minutos). Después solo vas a necesitar la tabla de la semana en la que vas (sección 7): ahí dice qué hacer cada día.",
    "<b>Los días son sesiones, no fechas del calendario.</b> Si un día no puedes dibujar, no pierdes nada: la próxima vez haces el día que sigue.",
    "<b>Imprime los anexos</b> (hoja de diagnóstico y bitácora) o cópialos a mano en tu cuaderno.",
    "<b>El día que tengas internet</b>: revisa conmigo tus dibujos de la semana y descarga lo de la semana siguiente (lista en la sección 4).",
    "<b>Cada semana tiene una «Pregunta para ti».</b> No te doy la respuesta a propósito: la tienes que descubrir dibujando. Tráeme tu respuesta cuando revisemos.",
])
story.append(Spacer(1, 4))
story.append(callout("Cómo leer las etiquetas", [
    f"{TAG_E} Hay estudios revisados por pares que lo respaldan.",
    f"{TAG_P} Hay estudios, pero en otra tarea (por ejemplo, teclear secuencias o memorizar textos) o con muestras chicas. Lo estoy extrapolando al dibujo.",
    f"{TAG_O} Práctica docente común o consenso de instructores. Puede ser útil, pero nadie lo ha probado con un experimento.",
], color=INK))

# ---- 1. Antes de empezar
story.append(P("1. Antes de empezar: lo que te tengo que decir", sH1))
story.append(P("1.1 Tu diagnóstico, corregido", sH2))
story.append(P(
    "Dices que tienes «talento» para hacer círculos y líneas. Eso es <b>control motor</b>, y se entrena; no es talento. "
    "Y aquí viene lo importante: en el estudio clásico de Cohen y Bennett (1997), el control motor fue la fuente "
    "<b>más pequeña</b> de errores al dibujar. La más grande fue <b>percibir mal lo que se dibuja</b>. "
    "Chamberlain y Wagemans (2016) revisaron la investigación de los 20 años siguientes y llegaron a algo parecido: "
    f"la precisión depende sobre todo de percibir bien el modelo y tu propio dibujo, y de tus decisiones de representación. {TAG_E}"))
story.append(P("Traducido a tu caso, dibujar bien tiene tres partes distintas:"))
story.append(grid_table([
    ["Habilidad", "Qué es", "Dónde estás", "Dónde se entrena"],
    ["<b>Trazo</b> (motor)", "Líneas limpias, elipses, control", "Ya lo tienes bastante", "Calentamiento diario (5–10 min)"],
    ["<b>Medir / ver</b>", "Comparar tamaños, ángulos y distancias a ojo", "La cuadrícula lo hace por ti; por eso no lo desarrollas", "Fase 1"],
    ["<b>Construir</b>", "Entender todo como volúmenes (cajas, cilindros, esferas) en el espacio, para poder girarlos", "No lo tienes todavía: es lo que llamas «ver en 3D»", "Fases 2, 3 y 4"],
    ["<b>Memoria visual</b>", "Una «biblioteca» mental de formas y proporciones", "Pequeña", "Cierre diario de memoria, fases 3 a 5"],
], [3.1 * cm, 5.0 * cm, 4.9 * cm, 4.8 * cm]))
story.append(Spacer(1, 6))
story.append(P("<b>Copiar bien</b> depende de medir. <b>Dibujar desde cero</b> depende de construir y de la memoria visual. Por eso el plan va en ese orden."))

story.append(P("1.2 «Ver en 3D» no es un don", sH2))
story.append(P(
    "Uttal y colaboradores (2013) juntaron 217 estudios de entrenamiento: las habilidades espaciales <b>mejoran con práctica</b> "
    "(efecto promedio moderado, g = 0.47), la mejora <b>dura</b> y se <b>transfiere</b> a tareas que no se entrenaron. "
    "En ingeniería, el curso de Sheryl Sorby usa justamente bocetos a mano de sólidos para entrenar la visualización espacial de estudiantes "
    f"que salen bajos en esas pruebas. {TAG_E} "
    "Ojo: esos estudios miden pruebas de rotación mental, no «dibujar personajes». Que te sirva para dibujar es una extrapolación razonable, no un hecho medido."))

story.append(P("1.3 Donde no tienes razón (o donde tu petición se puede mejorar)", sH2))
story.append(callout("«Busca todos los recursos que se te ocurran»", [
    "No te conviene, y te doy el mejor argumento. Tienes de 7 a 10 horas por semana. Cada hora viendo tutoriales es una hora sin dibujar, "
    "y ver una explicación <i>se siente</i> como aprender aunque no lo sea. Kornell y Bjork (2008) encontraron que la mayoría de la gente "
    f"juzga mal qué forma de estudiar le funciona: prefiere la que se siente más fácil. {TAG_E}",
    "Por eso este plan tiene un <b>núcleo pequeño</b> de recursos (sección 11) y una lista <b>extra</b> para cuando te atores. "
    "Regla: <b>máximo 20 % del tiempo consumiendo teoría y 80 % dibujando.</b>",
]))
story.append(callout("«Lo más pronto posible»", [
    "Meter 6 horas un sábado no compensa una semana sin dibujar. La práctica distribuida rinde más que la concentrada "
    f"(Donovan y Radosevich, 1999: efecto promedio d ≈ 0.46 en 63 estudios) {TAG_E}, y parte de la mejora motora se consolida "
    f"durmiendo (Walker et al., 2002, en una tarea de teclear secuencias) {TAG_P}.",
    "Lo más rápido que es realista: <b>poco, pero casi todos los días.</b>",
]))
story.append(callout("«Que tú seas mi tutor»", [
    "Lo hago con gusto, con tres límites honestos:",
    ("b", "<b>No siempre recuerdo conversaciones anteriores.</b> Cada vez que me escribas, di en qué semana vas y manda tu bitácora."),
    ("b", "<b>Puedo equivocarme</b> al juzgar proporciones en una foto. Tu prueba de superposición (sección 6) es más confiable que mi ojo."),
    ("b", "<b>No sustituyo a un maestro que te vea dibujar en persona.</b> Aprovecha a tus profesores de la carrera: llévales tu diagnóstico."),
    "Mi forma de corregirte: primero preguntas y pistas. Si te atoras dos veces en lo mismo, te doy la respuesta directa.",
], color=INK))

# ---- 2. Evidencia
story.append(PageBreak())
story.append(P("2. Lo que dice la evidencia, y cómo se usa en el plan", sH1))
story.append(P("Cada decisión del plan sale de uno de estos principios. Si un día quieres saltarte algo, revisa primero de qué principio viene."))
ev_rows = [
    ["#", "Principio", "Qué se sabe", "Nivel", "Cómo se aplica"],
    ["1", "Los errores vienen sobre todo de percibir mal, no de la mano.", "Cohen y Bennett (1997); Chamberlain y Wagemans (2016).", TAG_E, "Fase 1: medición, ángulos, espacios negativos, comparación."],
    ["2", "Lo que «crees» que es un ojo o una mano (esquemas mentales) distorsiona lo que dibujas.", "Chamberlain y Wagemans (2016) lo señalan como factor decisivo.", TAG_E, "Primero dibujar lo que ves; después construir con formas, no con símbolos."],
    ["3", "La visualización espacial se entrena.", "Uttal et al. (2013): g = 0.47, la mejora dura y se transfiere.", TAG_E + "<br/>(en pruebas espaciales)", "Fase 2: cajas, rotaciones, dibujar «a través» de las formas."],
    ["4", "Repartir la práctica rinde más que concentrarla.", "Donovan y Radosevich (1999): d ≈ 0.46.", TAG_E, "5–6 sesiones por semana y un bloque de repaso de fases anteriores en cada sesión."],
    ["5", "Mezclar ejercicios ayuda a retener y a distinguir.", "Shea y Morgan (1979), en tareas motoras; Kornell y Bjork (2008), al aprender estilos de pintores. Los resultados sobre retención son mixtos en revisiones posteriores.", TAG_E + "<br/>(mixta)", "Bloque de repaso mezclado en cada sesión."],
    ["6", "Recordar algo de memoria lo fija mejor que volver a verlo.", "Roediger y Karpicke (2006), en memoria de textos.", TAG_P, "Cierre diario: dibujar de memoria lo que estudiaste ese día."],
    ["7", "El sueño consolida habilidades motoras.", "Walker et al. (2002): unos 20 % más de velocidad tras dormir, en una tarea de teclear secuencias.", TAG_P, "Práctica diaria en vez de maratones. No te desveles para dibujar."],
    ["8", "La práctica deliberada importa, pero no lo explica todo.", "Macnamara et al. (2014): explica cerca de 21 % de las diferencias en música y 18 % en deportes.", TAG_E, "No te comparas con nadie: te mides contra tu yo de la semana 0."],
    ["9", "Aprender arte produce cambios medibles en unos 3 meses.", "Schlegel et al. (2015): estudiantes de un curso de arte de un trimestre mejoraron en dibujo rápido de figura, con cambios cerebrales medibles. Muestra pequeña, y no encontraron cambios en pruebas de percepción.", TAG_P, "Expectativa: cambios claros en unos 3 meses, no en semanas."],
    ["10", "Mito: «dibujar con el hemisferio derecho».", "Nielsen et al. (2013) no encontraron personas «de cerebro izquierdo» o «derecho».", TAG_E + "<br/>(en contra del mito)", "Puedes usar los ejercicios de Betty Edwards, pero ignora su teoría."],
    ["11", "Mito: copiar de cabeza abajo te hace más preciso.", "Cohen y Earls (2010); Ostrofsky et al. (2016): no mejora, e incluso empeora las distancias largas en caras.", TAG_E + "<br/>(en contra)", "No se usa como técnica principal."],
    ["12", "Las pausas cortas reducen la fatiga.", "Albulescu et al. (2022): menos fatiga (d ≈ 0.35) y más vigor. El efecto en el rendimiento es pequeño y solo aparece en tareas poco demandantes.", TAG_E + "<br/>(efecto pequeño)", "Pausa de 5 min cada ~25 min; 15 min a la mitad de la sesión de 2 h."],
    ["13", "Las pausas programadas funcionan mejor que «cuando me canse».", "Biwer et al. (2023): con pausas programadas hubo menos fatiga y distracción, con el mismo avance. Estudio pequeño, de un solo día.", TAG_P, "Usa temporizador; no esperes a estar agotado."],
]
story.append(grid_table(ev_rows, [0.75 * cm, 3.55 * cm, 5.6 * cm, 2.5 * cm, 5.4 * cm]))

# ---- 3. Materiales
story.append(CondPageBreak(9 * cm))
story.append(P("3. Materiales", sH1))
story.append(P(
    "No necesitas material profesional. Lo que te frena no es la herramienta, es la percepción (principio 1). "
    f"Con papel barato practicas más, porque no te da miedo «gastarlo». {TAG_O}"))
story.append(P("Lo que sí necesitas", sH2))
story.append(grid_table([
    ["Material", "Para qué", "Precio aprox. (MXN)"],
    ["Paquete de hojas bond tamaño carta (500)", "Volumen: calentamiento, cajas, gestos.", "$100–180"],
    ["Cuaderno de dibujo carta, hoja lisa", "Estudios con más tiempo y diagnósticos. Todo con fecha.", "$80–200"],
    ["Lápices HB y 2B (o portaminas 0.5 mm HB)", "HB para construir con trazo ligero; 2B para la línea final.", "$30–80"],
    ["Bolígrafo o plumón de punta fina (0.5 mm), negro", "Ejercicios de Drawabox: la tinta no se borra y te obliga a planear la línea antes de trazarla.", "$20–60"],
    ["Goma blanca y goma moldeable", "Borrar o aclarar la construcción.", "$40–90"],
    ["Sacapuntas", "—", "$10–30"],
    ["Tabla con clip, tamaño carta", "Superficie firme para dibujar en el trabajo. Mejor si la puedes inclinar.", "$40–80"],
    ["Regla de 30 cm", "Para dibujar cuadrículas en tu hoja (fase 1) y comprobar puntos de fuga (fase 2). No para trazar los ejercicios.", "$15–30"],
    ["3 micas o acetatos transparentes", "Tus cuadrículas portátiles (ver abajo).", "$15–40"],
    ["Folder o carpeta", "Guardar todo con fecha: es tu evidencia de progreso.", "$20–40"],
    ["<b>Total aproximado</b>", "", "<b>$370–830</b>"],
], [6.2 * cm, 8.4 * cm, 3.2 * cm]))
story.append(P("Los precios son orientativos (papelería en México, 2026). Verifícalos; no tengo precios en tiempo real.", sSmallMuted))
story.append(Spacer(1, 6))
story.append(callout("Micas: tu cuadrícula sin internet", [
    "Recorta 3 micas del tamaño de la pantalla de tu celular. Con plumón permanente y regla, dibuja en una una cuadrícula de 4×4, en otra una de 2×2, y en la última solo una cruz al centro. "
    "Pon la mica sobre la foto en la pantalla (sin cambiar el zoom mientras copias) y dibuja en tu hoja la misma cuadrícula, muy suave, en un rectángulo con la misma proporción que la foto. "
    "Así vas quitando la cuadrícula poco a poco en la fase 1.",
], color=PHASE[1], bg=PHASE_TINT[1]))
story.append(P("<b>Ya tienes:</b> celular (referencias, temporizador, cámara y «espejo» con la cámara frontal), tu propia mano y tu cara como modelos."))
story.append(P("No lo compres todavía", sH2))
story += bullets([
    f"<b>Maniquí de madera:</b> sus articulaciones y proporciones son poco realistas. Tu cuerpo en el espejo y fotos tuyas sirven más. {TAG_O}",
    f"<b>Tableta digital:</b> las habilidades de este plan son las mismas en papel y en digital, y el papel funciona sin internet ni batería. Por tu carrera sí vale la pena pasar ejercicios a digital, pero después de la fase 2. {TAG_O}",
    "<b>Sets caros de lápices o carboncillos:</b> no los necesitas hasta trabajar luz y valores, que viene después de este plan.",
])
story.append(P("Opcional", sH2))
story += bullets([
    "<b>Cabeza de planos</b> (tipo Asaro): ayuda en la fase 3. Hay alternativa gratis con un modelo 3D en Blender (sección 4).",
    "<b>Libros físicos</b> del núcleo (sección 11), si prefieres leer en papel.",
])
story.append(callout("Postura y mano", [
    f"Líneas largas con el hombro, no con la muñeca. Hoja de frente o inclinada. Si te duele la muñeca, para ese día. {TAG_O}",
], color=GREY))

# ---- 4. Preparación offline
story.append(CondPageBreak(9 * cm))
story.append(P("4. Prepararte para practicar sin internet", sH1))
story.append(P("Todo esto se hace en un día con internet, antes de empezar cada fase. Con media hora basta."))
story.append(P("Carpetas en el celular", sH2))
story.append(grid_table([
    ["Carpeta", "Qué guardas ahí"],
    ["Dibujo / 01_Lecturas", "PDFs y EPUB (lista abajo)."],
    ["Dibujo / 02_Notas_de_videos", "Fotos de tus notas a mano de cada video (ver abajo)."],
    ["Dibujo / 03_Referencias", "Subcarpetas: Objetos, Interiores_Calles, Cabezas, Manos, Pies, Poses, Maestros."],
    ["Dibujo / 04_Mis_dibujos", "Fotos de tus hojas con la fecha en el nombre, por ejemplo 2026-11-10_S1_elipses.jpg."],
], [5.6 * cm, 12.2 * cm], zebra=False))
story.append(P("Lecturas (gratis y legales)", sH2))
story += bullets([
    f"{BOX} <b>Harold Speed, <i>The Practice and Science of Drawing</i> (1913).</b> Dominio público. Project Gutenberg #14264: gutenberg.org/ebooks/14264 (descarga el EPUB con imágenes).",
    f"{BOX} <b>George Bridgman, <i>Constructive Anatomy</i> (1920).</b> Escaneos en Internet Archive (archive.org, busca «Constructive Anatomy Bridgman»). También hay edición barata de Dover.",
    f"{BOX} <b>Drawabox</b> (drawabox.com): Lección 0, Lección 1 y el «250 Box Challenge». Es gratis en la web. Guarda cada página desde el navegador con «Imprimir {ARROW} Guardar como PDF».",
    f"{BOX} <b>Este PDF.</b>",
])
story.append(P("Videos", sH2))
story += bullets([
    "La forma <b>legal</b> de ver YouTube sin internet es YouTube Premium (descargas dentro de la app) o cursos de pago que permitan descargar. Los «descargadores» de YouTube violan sus términos de servicio, así que no te los recomiendo.",
    f"<b>Alternativa gratis, y probablemente mejor:</b> el día con internet ve el video y haz una hoja de notas <i>dibujadas</i> en tu cuaderno. Esa hoja es lo que te llevas al trabajo, y resumir con tus palabras ya es práctica de recuperación (principio 6). {TAG_P}",
])
story.append(P("Fotos de referencia", sH2))
story += bullets([
    "<b>Las mejores, y 100 % legales, son las que tomas tú.</b> Cada fase trae su lista de fotos por tomar.",
    "<b>Fotos libres:</b> Unsplash y Pexels (descarga gratis).",
    "<b>Dibujos de maestros en alta resolución y de dominio público:</b> The Met (Open Access), Rijksmuseum y National Gallery of Art (EE. UU.). Sirven para copiar a los maestros en las fases 1, 3 y 4.",
    "<b>Poses de figura:</b> Croquis Cafe (YouTube; sesiones con modelos de dibujo, incluye desnudo artístico) y SenshiStock (DeviantArt; poses gratis para practicar, revisa sus reglas de uso).",
    "<b>Temporizador de gestos sin internet:</b> lo más simple es la galería del celular más un temporizador de intervalos. En Android existe «Gesture Drawing Practice» (Valentin's PowerTools #003, en F-Droid), que muestra tus fotos por tiempos. No lo he probado: verifica que funcione sin conexión antes de depender de él.",
])
story.append(P("3D: tu ventaja por estudiar animación", sH2))
story += bullets([
    f"{BOX} <b>Blender</b> (gratis, funciona sin internet). Úsalo para <b>comprobar</b>, no para calcar: crea un cubo, un cilindro y una esfera, mueve la cámara y compara con tu dibujo. Cambia la distancia focal y observa qué le pasa a la perspectiva.",
    f"{BOX} <b>Modelos gratis de cabeza o de planos de la cabeza</b> en Sketchfab. Revisa la licencia de cada uno antes de descargarlo.",
])

# ---- 5. Sesión
story.append(CondPageBreak(12 * cm))
story.append(P("5. Cómo es una sesión", sH1))
story.append(P("Siempre la misma estructura: calentar, aprender, repasar mezclado y cerrar de memoria. Lo que cambia cada semana es el contenido."))
C_WARM = colors.HexColor("#E9D8B4")
C_NEW = PHASE[1]
C_REV = PHASE[2]
C_BRK = colors.HexColor("#DCDFE4")
C_END = ACCENT
story.append(session_diagram("Sesión de 60 minutos (días con poco tiempo)", [
    (5, "Calentar", C_WARM, False),
    (25, "Bloque 1 · tema de la semana", C_NEW, True),
    (5, "Pausa", C_BRK, False),
    (20, "Bloque 2 · repaso mezclado", C_REV, True),
    (5, "Cierre", C_END, True),
], 60))
story.append(Spacer(1, 8))
story.append(session_diagram("Sesión de 120 minutos (95 minutos dibujando · gris = pausa)", [
    (10, "Calentar", C_WARM, False),
    (25, "Bloque 1 · tema (con referencia)", C_NEW, True),
    (5, "", C_BRK, False),
    (25, "Bloque 2 · tema (variaciones)", C_NEW, True),
    (15, "Pausa larga", C_BRK, False),
    (25, "Bloque 3 · repaso mezclado", C_REV, True),
    (5, "", C_BRK, False),
    (10, "Cierre", C_END, True),
], 120))
story.append(Spacer(1, 4))
story.append(grid_table([
    ["Parte", "Qué haces"],
    ["<b>Calentar</b>", "Líneas «fantasma» (ensayas el movimiento en el aire y luego trazas), elipses, cajas rápidas. No es para dibujar bonito: es para soltar el brazo."],
    ["<b>Bloques 1 y 2</b>", "El tema de la semana. El Bloque 2 solo existe en los días de 2 horas. La teoría se ve el día con internet, no aquí."],
    ["<b>Repaso mezclado</b>", "Ejercicios de semanas o fases anteriores, mezclados (principios 4 y 5)."],
    ["<b>Cierre</b>", "Sin ver nada, dibuja de memoria lo que estudiaste hoy (principio 6). Después compáralo con la referencia y llena la bitácora: 3 líneas."],
], [3.4 * cm, 14.4 * cm], zebra=False))
story.append(Spacer(1, 6))
story.append(callout("Reglas de las pausas", [
    ("b", "<b>Pausa de verdad:</b> levántate, mueve hombros y muñecas, mira algo a más de 6 metros para descansar la vista de cerca. No es momento de ver el celular."),
    ("b", "<b>Usa temporizador</b> (principio 13). Si antes de tiempo ya estás «frito» (las líneas empeoran, te frustras), toma la pausa antes: es fatiga real."),
    ("b", "<b>Si después de la pausa larga sigues agotado,</b> salta directo al cierre de memoria y termina. Un día corto también cuenta."),
    ("b", "<b>Día pesado, mínimo de 15 minutos:</b> 5 de calentamiento, 7 de un ejercicio de la semana y 3 de un dibujo de memoria. Es para no romper el hábito."),
], color=PHASE[2], bg=PHASE_TINT[2]))
story.append(P("Una semana tipo", sH3))
story.append(P(
    "<b>5 sesiones de práctica</b> (1–2 h) + <b>1 día con internet</b> (revisión conmigo, descargas, un poco de teoría) + <b>1 día libre</b>. "
    "Meta: 7–10 horas por semana. Lo que haces en cada bloque, día por día, está en las tablas de la sección 7. "
    "Si el día con internet también puedes dibujar, haz la siguiente sesión y después la revisión."))

# ---- 6. Diagnóstico
story.append(CondPageBreak(14 * cm))
story.append(P("6. Semana 0: tu punto de partida", sH1))
story.append(P(
    "Sin cuadrícula, sin regla y sin borrar mucho. <b>Va a salir mal, y para eso sirve.</b> Ponle fecha y no lo tires: "
    "en la semana 26 vas a querer verlo. Usa la hoja del Anexo A."))
story.append(grid_table([
    ["#", "Dibujo", "Tiempo"],
    ["1", "Una persona de pie, de cuerpo completo, <b>de memoria</b>.", "10 min"],
    ["2", "Una cabeza en 3/4 mirando un poco hacia arriba, <b>de memoria</b>.", "10 min"],
    ["3", "Tu mano no dominante, <b>observándola</b>, en una pose que no sea plana.", "10 min"],
    ["4", "Una caja (de zapatos) vista desde arriba y de lado, <b>de memoria</b>.", "5 min"],
    ["5", "Copia de una foto de una persona de cuerpo completo, <b>sin cuadrícula</b>.", "20 min"],
    ["6", "Sobre una foto impresa de un cuarto o una calle: marca dónde crees que están los puntos de fuga y la línea de horizonte. No uses regla todavía.", "10 min"],
], [0.7 * cm, 14.6 * cm, 2.5 * cm]))
story.append(Spacer(1, 8))
story.append(callout("Prueba de superposición (la usarás todo el plan)", [
    "1. Toma una foto de tu dibujo con el celular <b>paralelo a la hoja</b>. Si lo inclinas, la foto le agrega su propia perspectiva y no vas a poder comparar.",
    "2. Ajusta la foto al mismo tamaño que la referencia. Pasa rápido de una a la otra, o súbele transparencia a una en cualquier editor de fotos (funciona sin internet).",
    "3. Escribe los <b>3 errores más grandes</b>: largo, ancho, ángulo o posición. No anotes detalles.",
    "4. <b>Antes de comparar,</b> escribe dónde crees que te equivocaste. Lo que importa a futuro es que tu predicción le atine cada vez más.",
], color=PHASE[1], bg=PHASE_TINT[1]))
story.append(P(
    "Los mismos 6 dibujos se repiten en las <b>semanas 4, 9, 15, 22 y 26</b>. Mándame las fotos de la semana 0 y te respondo con preguntas, no con correcciones."))
story.append(CondPageBreak(11 * cm))
story.append(P("La semana 0, día por día", sH2))
story.append(P("Los 6 dibujos <b>no van en un solo día</b>: se reparten en los días 1 y 2. Los días 3 a 5 te enseñan la estructura de las sesiones y preparan la fase 1."))
from plan_diario import SEMANA_0
story.append(grid_table([["Día", "Qué haces", "Tiempo"]] + [list(r) for r in SEMANA_0],
                        [2.6 * cm, 13.0 * cm, 2.2 * cm], head_color=PHASE[0]))

# ---- 7. Temario
story.append(PageBreak())
story.append(P("7. El plan, día por día", sH1))
story.append(roadmap_diagram())
story.append(Spacer(1, 6))
story.append(callout("Cómo leer las tablas", [
    ("b", "<b>«Día 1» no es lunes:</b> es tu primera sesión de práctica de esa semana. Si un día no puedes dibujar, no te saltas nada: la próxima vez haces el día que sigue. Cada semana son 5 sesiones, aunque te tome 6, 7 u 8 días del calendario."),
    ("b", "<b>Si tienes 1 hora:</b> calentamiento (5 min) + <b>Bloque 1</b> (25) + pausa (5) + <b>Repaso</b> (20) + <b>Cierre</b> (5)."),
    ("b", "<b>Si tienes 2 horas:</b> calentamiento (10) + <b>Bloque 1</b> (25) + pausa (5) + <b>Bloque 2</b> (25) + pausa larga (15) + <b>Repaso</b> (25) + pausa (5) + <b>Cierre</b> (10)."),
    ("b", "<b>Cierre:</b> dibuja de memoria lo que dice la columna, compáralo con la referencia o el objeto real y llena la bitácora (3 líneas)."),
    ("b", "<b>«Antes de esta semana»</b> es lo que haces el día con internet: estudiar un poco y dejar listas las fotos. Ese mismo día mándame 3 a 5 dibujos de la semana que terminaste."),
    ("b", "<b>Si un ejercicio no te sale, repítelo al día siguiente</b> en vez de avanzar. Terminar el plan en 30 semanas en lugar de 26 está bien. Saltarte el criterio para pasar de fase no está bien, porque cada fase se apoya en la anterior."),
], color=INK))

from plan_diario import SEMANAS, FASES, DIAG, DIAG_TEXTO

D_COLS = [1.0 * cm, 4.9 * cm, 4.4 * cm, 3.9 * cm, 3.6 * cm]
sDayHead = S("dayhead", fontName="Body-Bold", fontSize=8.2, leading=10.2, textColor=colors.white, spaceAfter=0)
sDay = S("day", fontSize=8.3, leading=10.9, spaceAfter=0)
sWeekLine = S("weekline", fontSize=8.8, leading=11.8, spaceAfter=3)


def day_table(phase, dias):
    head = [Paragraph(t, sDayHead) for t in (
        "Día", "Bloque 1 · 25 min", "Bloque 2 · 25 min<br/>(solo si tienes 2 h)",
        "Repaso · 20–25 min", "Cierre · de memoria")]
    data = [head]
    spans = []
    for i, d in enumerate(dias, 1):
        if d == DIAG:
            data.append([Paragraph(f"<b>{i}</b>", sDay), Paragraph(DIAG_TEXTO, sDay), "", "", ""])
            spans.append(("SPAN", (1, i), (4, i)))
            spans.append(("BACKGROUND", (1, i), (4, i), colors.HexColor("#FBEDE8")))
        else:
            data.append([Paragraph(f"<b>{i}</b>", sDay)] + [Paragraph(x, sDay) for x in d])
    t = Table(data, colWidths=D_COLS, repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), PHASE[phase]),
        ("BACKGROUND", (0, 1), (0, -1), PHASE_TINT[phase]),
        ("BACKGROUND", (2, 1), (2, -1), colors.HexColor("#FAFAF7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEBEFORE", (1, 1), (-1, -1), 0.3, RULE),
    ] + spans))
    return t


def week_block(phase, num):
    w = SEMANAS[num]
    band = Table([[Paragraph(f'<font color="white"><b>SEMANA {num}</b> · {w["titulo"]}</font>',
                             S("wb", fontSize=10, leading=13, spaceAfter=0))]], colWidths=[W_FULL])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PHASE[phase]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    info = Table([[Paragraph(f"<b>Antes de esta semana (día con internet):</b> {w['antes']}", sWeekLine)],
                  [Paragraph(f"<b>Pregunta para ti:</b> <i>{w['pregunta']}</i>", sWeekLine)]],
                 colWidths=[W_FULL])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PHASE_TINT[phase]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return KeepTogether([band, info, day_table(phase, w["dias"]), Spacer(1, 12)])


def phase_block(num, title, goal, why, photos, criterion, extra=None):
    a, b = FASES[num]["semanas"]
    out = [CondPageBreak(9 * cm), PhaseHeader(num, title, f"SEMANAS {a}–{b}"), Spacer(1, 6),
           P(f"<b>Meta:</b> {goal}"), P(f"<b>Por qué va aquí:</b> {why}")]
    if extra:
        out += extra
    out.append(callout("En todas las sesiones de esta fase", [
        f"<b>Calentamiento:</b> {FASES[num]['calentamiento']}",
        f"<b>Repaso:</b> {FASES[num]['repaso_regla']}",
        f"<b>Fotos que vas a necesitar:</b> {photos}",
    ], color=PHASE[num], bg=PHASE_TINT[num]))
    for wk in range(a, b + 1):
        out.append(week_block(num, wk))
    out.append(callout(f"Criterio para terminar la fase {num}", [criterion], color=PHASE[num], bg=colors.white))
    return out


story += phase_block(
    1, "Ver y medir",
    "copiar sin cuadrícula con proporciones creíbles y, sobre todo, <b>detectar tus propios errores</b>.",
    "es la fuente principal de errores (principio 1) y todo lo demás depende de saber comparar tamaños y ángulos.",
    "objetos de tu entorno con luz de un solo lado (ventana o lámpara), cada uno desde 3 ángulos: sillas, botellas, herramientas, tu mochila.",
    "Copias sin cuadrícula en las que la superposición muestra errores que <b>tú ya habías anotado antes de comparar</b>. Si todavía no, repite las semanas 3 y 4.",
    extra=[grid_removal_diagram(), Spacer(1, 4)],
)

story += phase_block(
    2, "Volumen y perspectiva",
    "pensar en volúmenes, encontrar puntos de fuga en fotos y dibujar cajas y cilindros convincentes en cualquier ángulo.",
    "aquí es donde se entrena «ver en 3D» (principio 3). La cabeza y el cuerpo son cajas, esferas y cilindros en perspectiva: sin esta fase, las siguientes no se sostienen.",
    "tu cuarto, la calle, pasillos y muebles, cada uno <b>desde arriba, a la altura de tus ojos y desde abajo</b>; edificios desde la banqueta.",
    "En 9 de cada 10 fotos encuentras el número correcto de puntos de fuga, y cuando compruebas tus cajas con regla, las aristas convergen de forma razonable.",
    extra=[callout("Lo mínimo que necesitas saber para empezar (lo demás lo descubres tú)", [
        ("b", "La <b>línea de horizonte</b> siempre está a la altura de tus ojos (o de la cámara)."),
        ("b", "Las líneas que en la realidad son <b>paralelas</b> convergen en el <b>mismo</b> punto de fuga. Cada familia de paralelas tiene el suyo."),
        ("b", "Para saber cuántos puntos hay en una foto: prolonga con regla bordes que sabes que son paralelos (orillas de mesa, marcos de ventana, banquetas) y mira dónde se juntan."),
    ], color=PHASE[2], bg=PHASE_TINT[2]), vp_diagram(), Spacer(1, 6)],
)

story += phase_block(
    3, "La cabeza",
    "dibujar cabezas construidas, con proporciones coherentes, girando e inclinándose.",
    "la cabeza es una esfera con una caja en perspectiva: aplicas la fase 2 a algo más complejo, y es la parte de un personaje que más se nota cuando falla.",
    "tu cara con luz de un solo lado desde 8 ángulos (arriba, abajo, 3/4, perfil); amigos o familia, con su permiso.",
    "Puedes dibujar de memoria una cabeza construida en 3/4, vista desde arriba y desde abajo, con los rasgos bien ubicados aunque sean simples.",
)

story += phase_block(
    4, "La figura",
    "figuras de cuerpo completo con proporciones coherentes: de referencia y, en versión simple, de memoria.",
    "ya sabes medir (fase 1), construir volúmenes (fase 2) y una cabeza, que es la unidad de medida del cuerpo (fase 3).",
    "tú en el espejo en poses básicas (de pie, sentado, caminando, girado); tus manos y pies en 20 poses cada uno.",
    "En la superposición, tus figuras de referencia no tienen errores grandes de proporción. De memoria, una figura simple en 3 poses distintas se sostiene.",
)

story += phase_block(
    5, "Tu primer personaje",
    "un personaje original tuyo, con proporciones coherentes en varias poses y ángulos.",
    "es el objetivo que pediste: dibujar desde cero. Ahora juntas medir, construir y memoria.",
    "referencias de ropa y de poses para tu personaje, y tú mismo actuando sus poses (es lo que hacen los animadores).",
    "Terminas el proyecto final y el diagnóstico. Con eso decidimos juntos el plan de los meses 7 a 12.",
)

# ---- 8. Trabajar conmigo
story.append(CondPageBreak(9 * cm))
story.append(P("8. Cómo trabajar conmigo", sH1))
story.append(P("«¿Está bien?» es una pregunta que no me deja ayudarte mucho. Esta te funciona mejor:"))
story.append(callout("Plantilla para mandarme tus dibujos", [
    "<b>Semana __ · Fase __.</b> Ejercicio: ______. Tiempo: __ min.",
    "Referencia: (adjunta, junto al dibujo).",
    "Lo que creo que salió mal: ______.",
    "Mi respuesta a la «Pregunta para ti»: ______.",
    "Quiero que revises sobre todo: proporción / perspectiva / construcción / gesto.",
], color=INK))
story += bullets([
    "<b>Fotos:</b> luz natural, celular paralelo a la hoja, sin tu sombra encima, con la referencia al lado.",
    "<b>Manda 3 a 5 dibujos representativos por semana</b>, no todo. Incluye uno que te haya salido mal.",
    "<b>Lo que voy a hacer:</b> preguntas y pistas primero. Respuesta directa solo si te atoras dos veces en lo mismo.",
    "<b>Si te estancas en una fase,</b> ajustamos el plan. Es normal.",
    "<b>Busca también crítica humana:</b> tus profesores, compañeros de la carrera, la comunidad de Drawabox. Varias opiniones distintas son mejores que una sola, y eso me incluye a mí.",
])

# ---- 9. Expectativas
story.append(CondPageBreak(10 * cm))
story.append(P("9. Expectativas realistas", sH1))
story.append(P(
    "No existe un estudio que diga «en X horas dibujas personajes». Lo que sigue es una <b>estimación</b> "
    f"{TAG_O}, basada en cómo suelen avanzar los cursos de fundamentos con tu volumen de práctica: de 7 a 10 h por semana, "
    "o sea unas <b>180–260 horas en 26 semanas</b>. El dato duro más cercano es Schlegel et al. (2015), que midieron mejoras en "
    "dibujo después de un curso de unos 3 meses."))
story.append(grid_table([
    ["Momento", "Horas aprox.", "Lo razonable", "Señal de alerta"],
    ["Semana 4", "30–40", "Copias sin cuadrícula aceptables. Detectas tus errores antes de comparar.", "Sigues sin poder copiar sin cuadrícula: más medición, menos teoría."],
    ["Semana 9", "65–90", "Encuentras puntos de fuga en fotos. Cajas y cilindros creíbles.", "Muchas cajas con aristas que se abren: compruébalas siempre con regla."],
    ["Semana 15", "100–150", "Cabezas construidas en varios ángulos, todavía rígidas.", "Caras «planas» en 3/4: regresa a las esferas y las cajas."],
    ["Semana 22", "150–220", "Figuras de referencia bien proporcionadas. De memoria, figuras simples.", "Las proporciones cambian en cada dibujo: vuelve a tu tabla de medidas."],
    ["Semana 26", "180–260", "Un personaje propio coherente en varias poses. Se verá rígido, y es normal.", "—"],
    ["12 meses o más", "400+", "Soltura, dinamismo, anatomía. Empieza a aparecer un estilo propio.", "—"],
], [2.3 * cm, 2.2 * cm, 6.9 * cm, 6.4 * cm]))
story.append(Spacer(1, 6))
story.append(callout("El bache de la fase 2", [
    f"Entre las semanas 5 y 8 es muy común sentir que vas para atrás: la perspectiva frustra a casi todos al principio. Si te pasa, no abandones: es parte del camino. {TAG_O}",
], color=AMBER, bg=colors.HexColor("#FBF3E4")))

# ---- 10. Después
story.append(P("10. Después de las 26 semanas (vista previa)", sH2))
story += bullets([
    "<b>Anatomía:</b> la serie <i>Anatomía artística</i> de Michel Lauricella (Gustavo Gili, en español) y los cursos de anatomía de Proko.",
    "<b>Figura dinámica:</b> Michael Hampton, <i>Figure Drawing: Design and Invention</i>.",
    "<b>Luz y valores:</b> sombreado de formas simples, luego de figuras.",
    "<b>Animación:</b> Richard Williams, <i>The Animator's Survival Kit</i>.",
    "<b>Composición y encuadre:</b> Marcos Mateu-Mestre, <i>Framed Ink</i>.",
    "<b>Perspectiva avanzada:</b> Scott Robertson y Thomas Bertling, <i>Dibujo. Cómo crear objetos y entornos con imaginación</i> (Anaya, ISBN 978-84-415-4294-5).",
])

# ---- 11. Recursos
story.append(CondPageBreak(12 * cm))
story.append(P("11. Recursos: el núcleo y los extras", sH1))
story.append(P("<b>Núcleo:</b> con esto alcanza para las 26 semanas. Antes de buscar algo nuevo, revisa si ya está aquí.", sBody))
story.append(P("Verifiqué en noviembre de 2026 que estos recursos existen. Los sitios cambian: si algo ya no está, pídeme un reemplazo antes de buscar por tu cuenta.", sSmallMuted))
story.append(Spacer(1, 4))
story.append(grid_table([
    ["Recurso", "Tipo / costo", "Cómo tenerlo sin internet", "Fase", "Idioma"],
    ["<b>Drawabox</b> (Lecciones 0–2, 250 Box Challenge)", "Web, gratis", "Guardar cada página como PDF", "1–2", "Inglés"],
    ["<b>Ernest Norling</b>, <i>Perspective Made Easy</i>", "Libro barato (Dover)", "Físico o ebook", "2", "Inglés"],
    ["<b>Harold Speed</b>, <i>The Practice and Science of Drawing</i>", "Gratis, dominio público", "Project Gutenberg #14264", "1", "Inglés"],
    ["<b>Andrew Loomis</b>, <i>Drawing the Head and Hands</i> y <i>Figure Drawing for All It's Worth</i>", "Libros (reediciones de Titan Books)", "Físico. Hay escaneos en Internet Archive, pero su situación legal está en disputa: los herederos de Loomis han enviado avisos legales a sitios que los publicaban.", "3–4", "Inglés"],
    ["<b>Proko</b> (YouTube): cabeza con método Loomis, gesto, proporción", "Gratis", "YouTube Premium o tus notas a mano", "3–4", "Inglés (con subtítulos)"],
    ["<b>George Bridgman</b>, <i>Constructive Anatomy</i>", "Gratis (1920)", "Internet Archive, o la edición de Dover", "4", "Inglés"],
    ["<b>Michel Lauricella</b>, <i>Anatomía artística</i> vol. 2: <i>Cómo dibujar el cuerpo humano de forma esquemática</i>", "Libro (Gustavo Gili)", "Físico", "4–5", "Español"],
    ["<b>Blender</b>", "Gratis", "Se instala; funciona sin internet", "2–5", "Español"],
    ["<b>Dibujos de maestros</b>: The Met Open Access, Rijksmuseum, NGA", "Gratis", "Descargar las imágenes", "1, 3–4", "—"],
    ["<b>Tus propias fotos</b>", "Gratis", "Celular", "Todas", "—"],
], [5.0 * cm, 3.0 * cm, 5.4 * cm, 1.6 * cm, 2.8 * cm]))
story.append(Spacer(1, 8))
story.append(P("Extras (solo si te sobra tiempo o te atoras en algo concreto)", sH2))
story += bullets([
    "<b>Bert Dodson, <i>Keys to Drawing</i>:</b> observación y medición (fase 1).",
    "<b>Betty Edwards, <i>Aprender a dibujar con el lado derecho del cerebro</i>:</b> los ejercicios de contorno y espacio negativo sirven. La teoría de los hemisferios no tiene sustento (Nielsen et al., 2013).",
    "<b>Scott Robertson:</b> perspectiva avanzada, para después de la fase 2.",
    "<b>Michael Hampton:</b> figura, para después de la fase 4.",
    "<b>Canales de YouTube en inglés:</b> Sinix Design (fundamentos y perspectiva), Marco Bucci (gesto y diseño), Aaron Blaise (animación y criaturas; fue animador en Disney), Croquis Cafe (sesiones con modelo).",
    "<b>Canales en español que aparecen en listas de recomendaciones:</b> Domerelly, Crearte Araiza, MiltonCor. No los he evaluado: úsalos para motivarte, no como fuente principal.",
])


# ---- Anexo A: diagnóstico
story.append(PageBreak())
story.append(P("Anexo A · Hoja de diagnóstico (imprime una por diagnóstico)", sH1))
story.append(P("Semana: ____   Fecha: ____________   Horas acumuladas: ____", sBody))
diag_rows = [["#", "Dibujo", "Antes de comparar: dónde creo que fallé", "Después de comparar: 3 errores principales", "Mejoró respecto al diagnóstico anterior"]]
names = ["Persona de pie, de memoria", "Cabeza 3/4 hacia arriba, de memoria", "Mano no dominante, observada",
         "Caja desde arriba y de lado, de memoria", "Copia de foto sin cuadrícula", "Puntos de fuga en foto"]
for i, n in enumerate(names, 1):
    diag_rows.append([str(i), n, "", "", ""])
t = grid_table(diag_rows, [0.6 * cm, 3.6 * cm, 4.6 * cm, 4.6 * cm, 4.4 * cm], zebra=False,
               row_heights=[None] + [2.55 * cm] * 6)
story.append(t)
story.append(Spacer(1, 10))
story.append(P("En una frase, ¿qué es lo que más cambió?", sH3))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceBefore=16, spaceAfter=0))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceBefore=20, spaceAfter=0))

# ---- Anexo B: bitácora
story.append(PageBreak())
story.append(P("Anexo B · Bitácora semanal (imprime una por semana)", sH1))
story.append(P("Semana: ____   Fase: ____   Meta de horas: ____   Horas reales: ____", sBody))
bit = [["Día", "Min.", "Qué practiqué", "Qué falló / qué noté", "Energía 1–5", "De memoria"]]
for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
    bit.append([dia, "", "", "", "", f'<font name="Sym" size="11">☐</font>'])
t = grid_table(bit, [2.0 * cm, 1.3 * cm, 5.4 * cm, 5.4 * cm, 1.9 * cm, 1.8 * cm], zebra=False,
               row_heights=[None] + [2.0 * cm] * 7)
story.append(t)
story.append(Spacer(1, 8))
story.append(P("<b>Mi respuesta a la «Pregunta para ti» de esta semana:</b>", sBody))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceBefore=16, spaceAfter=0))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceBefore=20, spaceAfter=0))

# ---- Anexo C: referencias
story.append(PageBreak())
story.append(P("Anexo C · Referencias", sH1))
story.append(P("Estudios citados en este plan. Los encuentras por título en Google Scholar; varios tienen versión gratuita en PDF.", sBody))
refs = [
    "Albulescu, P., et al. (2022). «Give me a break!» A systematic review and meta-analysis on the efficacy of micro-breaks for increasing well-being and performance. <i>PLOS ONE, 17</i>(8), e0272460.",
    "Biwer, F., Wiradhany, W., oude Egbrink, M. G. A., &amp; de Bruin, A. B. H. (2023). Understanding effort regulation: Comparing «Pomodoro» breaks and self-regulated breaks. <i>British Journal of Educational Psychology</i>.",
    "Chamberlain, R., &amp; Wagemans, J. (2016). The genesis of errors in drawing. <i>Neuroscience &amp; Biobehavioral Reviews, 65</i>, 195–207.",
    "Cohen, D. J., &amp; Bennett, S. (1997). Why can't most people draw what they see? <i>Journal of Experimental Psychology: Human Perception and Performance, 23</i>(3), 609–621.",
    "Cohen, D. J., &amp; Earls, H. (2010). Inverting an image does not improve drawing accuracy. <i>Psychology of Aesthetics, Creativity, and the Arts, 4</i>(3), 168–172.",
    "Donovan, J. J., &amp; Radosevich, D. J. (1999). A meta-analytic review of the distribution of practice effect: Now you see it, now you don't. <i>Journal of Applied Psychology, 84</i>(5), 795–805.",
    "Kornell, N., &amp; Bjork, R. A. (2008). Learning concepts and categories: Is spacing the «enemy of induction»? <i>Psychological Science, 19</i>(6), 585–592.",
    "Macnamara, B. N., Hambrick, D. Z., &amp; Oswald, F. L. (2014). Deliberate practice and performance in music, games, sports, education, and professions: A meta-analysis. <i>Psychological Science, 25</i>(8), 1608–1618.",
    "Nielsen, J. A., Zielinski, B. A., Ferguson, M. A., Lainhart, J. E., &amp; Anderson, J. S. (2013). An evaluation of the left-brain vs. right-brain hypothesis with resting state functional connectivity magnetic resonance imaging. <i>PLOS ONE, 8</i>(8), e71275.",
    "Ostrofsky, J., Kozbelt, A., Cohen, D. J., Conklin, L., &amp; Thomson, K. (2016). Face inversion impairs the ability to draw long-range, but not short-range, spatial relationships between features. <i>Empirical Studies of the Arts</i>. doi:10.1177/0276237416634851",
    "Roediger, H. L., &amp; Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. <i>Psychological Science, 17</i>(3), 249–255.",
    "Schlegel, A., et al. (2015). The artist emerges: Visual art learning alters neural structure and function. <i>NeuroImage, 105</i>, 440–451.",
    "Shea, J. B., &amp; Morgan, R. L. (1979). Contextual interference effects on the acquisition, retention, and transfer of a motor skill. <i>Journal of Experimental Psychology: Human Learning and Memory, 5</i>(2), 179–187.",
    "Sorby, S. A. (2009). Educational research in developing 3-D spatial skills for engineering students. <i>International Journal of Science Education, 31</i>(3), 459–480.",
    "Uttal, D. H., Meadow, N. G., Tipton, E., Hand, L. L., Alden, A. R., Warren, C., &amp; Newcombe, N. S. (2013). The malleability of spatial skills: A meta-analysis of training studies. <i>Psychological Bulletin, 139</i>(2), 352–402.",
    "Walker, M. P., Brakefield, T., Morgan, A., Hobson, J. A., &amp; Stickgold, R. (2002). Practice with sleep makes perfect: Sleep-dependent motor skill learning. <i>Neuron, 35</i>(1), 205–211.",
]
sRef = S("ref", fontSize=8.8, leading=12, leftIndent=14, firstLineIndent=-14, spaceAfter=4)
for r in refs:
    story.append(P(r, sRef))


# ---------------------------------------------------------------- construir
class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        frame = Frame(1.9 * cm, 1.7 * cm, letter[0] - 3.8 * cm, letter[1] - 3.5 * cm, id="f",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=on_cover),
            PageTemplate(id="normal", frames=[frame], onPage=on_page),
        ])


doc = Doc(OUT, pagesize=letter, title="Aprender a dibujar desde cero: plan de 26 semanas",
          author="Plan elaborado con Claude", subject="Plan de aprendizaje de dibujo")
doc.build(story)
print("OK", OUT)
