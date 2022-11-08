import auxil

from docx import Document
import json
from fpdf import FPDF
from pdf2jpg import pdf2jpg

from loguru import logger

def write_docx(header, name, intro, instruction,
	responsible, creator, date, out, count):
	document = Document()

	headerp = document.add_paragraph()
	headerp.alignment = 1
	headerp.add_run(header + '\n\n').bold = True
	
	namep = document.add_paragraph()
	namep.alignment = 1
	namep.add_run(name)

	document.add_paragraph(intro)
	
	document.add_paragraph(auxil.add_numbering(instruction)+'\n')

	document.add_paragraph(responsible)

	datep = document.add_paragraph(creator+'\n')
	datep.add_run(date)
	datep.alignment = 2

	document.save(f"{out}/docx/{count}.docx")
	logger.debug(f"Saved {out}/docx/{count}.docx")

def write_json(instruction, responsible, date, out, count):
	json_dict = {
		"Tasks": {}
	}

	for i in range(len(instruction)):
		instr = instruction[i]
		task_text = instr["task_text"][4:].strip()
		task_responsibles_people = instr["task_responsibles_people"]
		task_responsibles_groups = instr["task_responsibles_groups"]
		task_deadline = instr["task_deadline"]

		json_dict["Tasks"][f"Task{i+1}"] = {"task_text": task_text}
		json_dict["Tasks"][f"Task{i+1}"]["task_responsibles_people"] = task_responsibles_people
		json_dict["Tasks"][f"Task{i+1}"]["task_responsibles_groups"] = task_responsibles_groups
		json_dict["Tasks"][f"Task{i+1}"]["task_deadline"] = task_deadline


	json_dict["Tasks"]["Global_supervisor"] = responsible
	json_dict["Tasks"]["Global_deadline"] = date

	with open(f"{out}/json/{count}.json", "w") as jsonf:
		json.dump(json_dict, jsonf, ensure_ascii=False, indent=4)
		logger.debug(f"Saved {out}/json/{count}.json")

def write_pdf(header, name, intro, instruction,
              responsible, creator, date, out, count):
	pdf = FPDF()
	pdf.add_page()

	pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
	pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
	pdf.set_font('DejaVu', 'B', 14)

	pdf.multi_cell(0, 10, txt = header+"\n\n", align="C")
	
	pdf.set_font("DejaVu", size=14)
	
	pdf.multi_cell(0, 10, txt=name+'\n', align="C")
	pdf.multi_cell(0, 10, txt=intro, align="J")
	pdf.multi_cell(0, 10, txt=instruction+'\n')
	pdf.multi_cell(0, 10, txt=responsible)
	pdf.multi_cell(0, 10, txt=creator, align="R")
	pdf.multi_cell(0, 10, txt=date, align="R")

	pdf.output(f"{out}/pdf/{count}.pdf")
	logger.debug(f"Saved {out}/pdf/{count}.pdf")

def write_pdf_linux(docx_path):
	pass

def write_pdf_windows(docx_path):
	pass

def write_jpg(out, count):
	
	pdf = f"{out}/pdf/{count}.pdf"
	output = f"{out}/jpg"

	pdf2jpg.convert_pdf2jpg(pdf, output, pages="ALL")
	logger.debug(f"Saved {out}/jpg/{count}.pdf_dir/")
