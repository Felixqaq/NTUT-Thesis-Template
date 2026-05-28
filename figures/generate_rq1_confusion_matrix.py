from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().with_name("rq1_confusion_matrix.pdf")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("DFKai", str(ROOT / "DFKai-SB.ttf")))


def draw_centered(c, text, x, y, font_name, font_size, fill=colors.black):
    c.setFillColor(fill)
    c.setFont(font_name, font_size)
    c.drawCentredString(x, y, text)


def draw_right(c, text, x, y, font_name, font_size, fill=colors.black):
    c.setFillColor(fill)
    c.setFont(font_name, font_size)
    c.drawRightString(x, y, text)


def main() -> None:
    register_fonts()

    page_w, page_h = 385, 246
    c = canvas.Canvas(str(OUT), pagesize=(page_w, page_h))
    c.setFillColor(colors.white)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    x0, y0 = 138, 26
    cell_w, cell_h = 112, 72
    label_x = x0 - 14
    values = [[21, 0], [4, 29]]
    fills = [
        [colors.HexColor("#3D6FA8"), colors.HexColor("#F2F4F7")],
        [colors.HexColor("#D8E7F3"), colors.HexColor("#244F86")],
    ]

    # Axis labels
    draw_centered(c, "預測類別", x0 + cell_w, y0 + 2 * cell_h + 52, "DFKai", 18)
    draw_centered(c, "Normal", x0 + 0.5 * cell_w, y0 + 2 * cell_h + 23, "Times-Roman", 16)
    draw_centered(c, "Abnormal", x0 + 1.5 * cell_w, y0 + 2 * cell_h + 23, "Times-Roman", 16)

    c.saveState()
    c.translate(34, y0 + cell_h)
    c.rotate(90)
    draw_centered(c, "實際類別", 0, 0, "DFKai", 16)
    c.restoreState()

    draw_right(c, "Normal", label_x, y0 + 1.5 * cell_h - 5, "Times-Roman", 15)
    draw_right(c, "Abnormal", label_x, y0 + 0.5 * cell_h - 5, "Times-Roman", 15)

    # Matrix cells
    for r in range(2):
        for col in range(2):
            x = x0 + col * cell_w
            y = y0 + (1 - r) * cell_h
            value = values[r][col]
            c.setFillColor(fills[r][col])
            c.rect(x, y, cell_w, cell_h, stroke=0, fill=1)

            is_dark = (r, col) in {(0, 0), (1, 1)}
            main_color = colors.white if is_dark else colors.black

            draw_centered(c, str(value), x + cell_w / 2, y + 24, "Times-Bold", 34, main_color)

    # Rules
    c.setStrokeColor(colors.HexColor("#666666"))
    c.setLineWidth(0.7)
    c.rect(x0, y0, 2 * cell_w, 2 * cell_h, stroke=1, fill=0)
    c.line(x0 + cell_w, y0, x0 + cell_w, y0 + 2 * cell_h)
    c.line(x0, y0 + cell_h, x0 + 2 * cell_w, y0 + cell_h)

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
