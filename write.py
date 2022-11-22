import auxil
import gen
import change_case

from docx import Document
import json
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

				with open(f"{samples_dir}/responsible.json") as rfile:
					resp_list = json.load(rfile)
					resp = choice(resp_list)

				if resp[-1] != "group":
					instruction[i]["task_responsibles_people"] = resp[1:]
				else:
					instruction[i]["task_responsibles_groups"] = resp[1:-1]

				resp_to_doc = change_case.create_responsible(ctrl_msg, resp[0])
				instruction[i]["task_text"] += sep_char + resp_to_doc + '.'

				if ("оставляю за собой" in resp_to_doc):
					instruction[i]["task_responsibles_people"] = "Автор приказа."

		if (not task_deadline):

			# Шанс 25%
			if randint(1, 4) == 1:

				# Дедлайн в новом предложении или в новом абзаце
				sep_char = ' ' if randint(0, 1) == True else '\n'
				deadline = auxil.generate_date(unixtime=True)

				with open(f"{samples_dir}/task_deadline.txt") as ddfile:
					dd_list = ddfile.read().split('\n')
					deadline_msg = choice(dd_list)
					
				instruction[i]["task_deadline"] = deadline
				instruction[i]["task_text"] += sep_char + deadline_msg
				instruction[i]["task_text"] += deadline[0] + '.'

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

def write_json(instruction, responsible_arr, date, out, count):
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


	json_dict["Tasks"]["Global_supervisor"] = responsible_arr
	json_dict["Tasks"]["Global_deadline"] = date

	with open(f"{out}/json/{count}.json", "w") as jsonf:
		json.dump(json_dict, jsonf, ensure_ascii=False, indent=4)
		logger.debug(f"Saved {out}/json/{count}.json")

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
