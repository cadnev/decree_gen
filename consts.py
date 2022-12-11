from docx.shared import Mm, Pt
from docx.enum.text import WD_LINE_SPACING

numbering_types = [["arabic", "."], ["arabic", ")"], ["roman", "."], ["roman", ")"],
				   ["bullet", "●"], ["bullet", "○"], ["latin", "."], ["latin", ")"]]

formats = ["%d %B %Y года", "%d %B %y", "%d %b %Y г.", "%d %b %y", "%d.%m.%Y", "%d.%m.%y"]

latin_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
				  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
				  'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak',
				  'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av',
				  'aw', 'ax', 'ay', 'az']

top_margin = Mm(20)
bottom_margin =Mm(20)
left_margin = Mm(30)
right_margin = Mm(15)

font_name = "Times New Roman"
font_size = Pt(14)

line_spacing = WD_LINE_SPACING.ONE_POINT_FIVE
font_height = 2.8 # mm
spacing = 2.2 # mm

logo_w = Mm(20)
logo_h = Mm(20)
logo_offset = 4 # px

sign_w = Mm(20)
sign_h = Mm(10)
PDFunits_offset = (-20, 10) # sign offset in PDF units

seal_w = Mm(20)
seal_h = Mm(20)
seal_offset = (0, 60) # seal offset in px

first_line_indent = Mm(12.5)

page_w = 612 # PDFUnits
page_h = 792 # PDFUnits
