import auxil
import gen
import change_case

from docx import Document
import json
from fpdf import FPDF
from pdf2jpg import pdf2jpg
import subprocess as sb
from os.path import abspath
from random import randint, choice
import re

from loguru import logger

# Добавляет ответственных и дедлайн в задачу, если их нет
def extend_instruction(instruction, samples_dir):
	for i in range(len(instruction)):
		instr = instruction[i]
		task_responsibles_people = instr["task_responsibles_people"]
		task_responsibles_groups = instr["task_responsibles_groups"]
		task_deadline = instr["task_deadline"]

		if (not task_responsibles_people) and (not task_responsibles_groups):
			
			# Шанс 25%
			if randint(1, 4) == 1:

				# Ответственные в новом предложении или в новом абзаце
				sep_char = ' ' if randint(0, 1) == True else '\n'

				with open(f"{samples_dir}/task_control.txt") as cfile:
					ctrl_list = cfile.read().split('\n')
					ctrl_msg = choice(ctrl_list)

				with open(f"{samples_dir}/responsible.txt") as rfile:
					resp_list = rfile.read().split(';;\n')
					resp = choice(resp_list)

				instruction[i]["task_responsibles_people"] = re.sub(r"{*}*", '', resp)

				resp = change_case.create_responsible(ctrl_msg, resp)
				instruction[i]["task_text"] += sep_char + resp + '.'

		if (not task_deadline):

			# Шанс 25%
			if randint(1, 4) == 1:

				# Дедлайн в новом предложении или в новом абзаце
				sep_char = ' ' if randint(0, 1) == True else '\n'
				deadline = auxil.generate_date(standart_format=True)

				with open(f"{samples_dir}/task_deadline.txt") as ddfile:
					dd_list = ddfile.read().split('\n')
					deadline_msg = choice(dd_list)
					
				instruction[i]["task_deadline"] = deadline
				instruction[i]["task_text"] += sep_char + deadline_msg
				instruction[i]["task_text"] += deadline + '.'

	return instruction

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

	path = f"{out}/docx/{count}.docx"
	document.save(path)
	logger.debug(path)

	return path

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

# Больше не нужна, удалим при мердже в main ветку
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

def write_pdf_linux(docx_path, out, count):
	out_path = f"{out}/pdf/{count}.pdf"
	out_path = abspath(out_path)
	docx_path = abspath(docx_path)

	cmd = ""
	cmd += f"abiword "
	cmd += f"-t pdf "
	cmd += f"-o {out_path} "
	cmd += docx_path
	sb.call(cmd, shell=True, stderr=sb.DEVNULL)
	logger.debug(f"Saved {out_path}")

def write_pdf_windows(docx_path, out, count):
	pass

def write_jpg(out, count):
	
	pdf = f"{out}/pdf/{count}.pdf"
	output = f"{out}/jpg"

	pdf2jpg.convert_pdf2jpg(pdf, output, pages="ALL")
	logger.debug(f"Saved {out}/jpg/{count}.pdf_dir/")
