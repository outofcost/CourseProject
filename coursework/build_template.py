"""
Build generic HSE term-paper .docx template (TASK-A-24).

Specs per HSE Article (Empirical) guideline:
- Times New Roman 14pt body, 1.5 line spacing
- A4 page, 2 cm margins (top/bottom/left/right)
- Page numbers (bottom center)
- Sample heading styles (Heading 1/2/3) at TNR 14pt bold

Usage:
    python3 coursework/build_template.py

Produces coursework/hse_template.docx — pass to pandoc via
    pandoc ... --reference-doc=coursework/hse_template.docx
"""

from docx import Document
from docx.shared import Pt, Cm, Mm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_default_font(doc, name='Times New Roman', size_pt=14):
    style = doc.styles['Normal']
    style.font.name = name
    # Set East-Asian and complex-script font names too (Word stores them separately)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), name)
    style.font.size = Pt(size_pt)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)


def set_page_size_and_margins(doc):
    for section in doc.sections:
        section.page_height = Mm(297)  # A4
        section.page_width = Mm(210)
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)


def add_page_number_footer(doc):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        # PAGE field
        fld_begin = OxmlElement('w:fldChar')
        fld_begin.set(qn('w:fldCharType'), 'begin')
        run._r.append(fld_begin)
        instr = OxmlElement('w:instrText')
        instr.text = 'PAGE'
        run._r.append(instr)
        fld_end = OxmlElement('w:fldChar')
        fld_end.set(qn('w:fldCharType'), 'end')
        run._r.append(fld_end)


def style_headings(doc):
    for level in (1, 2, 3):
        style = doc.styles[f'Heading {level}']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(14)
        style.font.bold = True
        rpr = style.element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts')
            rpr.append(rfonts)
        for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rfonts.set(qn(attr), 'Times New Roman')
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE


def main():
    doc = Document()
    set_default_font(doc)
    set_page_size_and_margins(doc)
    add_page_number_footer(doc)
    style_headings(doc)

    # Sample content so styles are visible if anyone opens the file directly
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_title.add_run('HSE Term Paper Template — Times New Roman 14pt, 1.5 spacing, A4, 2 cm margins')
    r.bold = True

    doc.add_paragraph()
    doc.add_heading('Глава 1. Образец заголовка первого уровня', level=1)
    doc.add_paragraph(
        'Это пример основного текста с настройками по умолчанию: '
        'Times New Roman, 14 пт, межстрочный интервал 1,5. '
        'Используйте этот файл как --reference-doc для pandoc, '
        'чтобы получить компиляции в нужном формате HSE.'
    )

    doc.add_heading('1.1. Заголовок второго уровня', level=2)
    doc.add_paragraph(
        'Раздел второго уровня для разделения главы на подсекции. '
        'Numbering можно делать вручную (1.1, 1.2, …) или через '
        'auto-numbering в Word/LibreOffice.'
    )

    doc.add_heading('1.1.1. Заголовок третьего уровня', level=3)
    doc.add_paragraph('Самый глубокий уровень типичный для разделов методов.')

    out = 'coursework/hse_template.docx'
    doc.save(out)
    print(f'Saved {out}')


if __name__ == '__main__':
    main()
