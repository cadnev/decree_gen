import russian_datetime
import consts

import re
from loguru import logger
from sys import stdout, platform
from random import randint, choice
import os
import subprocess as sb
from argparse import ArgumentTypeError

def logger_config(v):
	logger.remove()
	if int(v) == 0:
		logger.add(stdout, level="WARNING")
	elif int(v) == 1:
		logger.add(stdout, level="INFO")
	elif int(v) >= 2:
		logger.add(stdout, level="DEBUG")

	logger.add("logs/gen.log", level = "INFO", rotation="10 MB")

def generate_date(standart_format=False, unixtime=False):
	day = randint(1, 31)
	month = randint(1, 12)
	year = randint(2000, 2022)

	try:
		if not standart_format:
			date = russian_datetime.date(year, month, day).strftime(choice(consts.formats))
		else:
			date = russian_datetime.date(year, month, day).strftime(consts.formats[0])
	except ValueError:
		return generate_date(standart_format)

	if not unixtime:
		return date[0]
	else:
		return date

def check_size_format(size, pat=re.compile(r"^\d*[KMG]B$")):
	if not pat.match(size):
		logger.error(f"Invalid size argument: {size}")
		raise ArgumentTypeError("Invalid value")
	return size

def size_to_bytes(size):
	s = int(size[:-2])
	if "KB" in size:
		s *= 1024
	elif "MB" in size:
		s *= 1024**2
	elif "GB" in size:
		s *= 1024**3
	else:
		logger.error(f"Invalid size argument: {size}")

	return s

def getsize(out):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(out):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			if not os.path.islink(fp):
				total_size += os.path.getsize(fp)

	return total_size

def to_roman(n):
    result = ''
    for arabic, roman in zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
                             'm     cm   d    cd   c    xc  l   xl  x   ix v  iv i'.split()):
        result += n // arabic * roman
        n %= arabic

    return result

def add_numbering(instruction):
	string_instruction = ""

	for e in instruction:
		string_instruction += e["task_text"]
		string_instruction += '\n'
	instruction = string_instruction[:-1]

	clauses = re.split(r"\{\d*\}", instruction)[1:]
	numbering_types = [choice(consts.numbering_types) for _ in range(3)]
	complete_instruction = [{"clause": clauses[0],
							"index": 1,
							"nesting_level": 0,
							"numbering_type": numbering_types[0]}]
	numbering = [1, 1, 1]

	for indx in range(1, len(clauses)):
		clause = clauses[indx]
		prev_clause = complete_instruction[indx-1]
		prev_nesting_level = prev_clause["nesting_level"]
		nesting_level = randint(0, 1) if prev_nesting_level == 0 else randint(0, 2)
		n_type = numbering_types[nesting_level]

		if prev_nesting_level == nesting_level:
			numbering[nesting_level] += 1
			index = numbering[nesting_level]
		elif prev_nesting_level < nesting_level:
			numbering[nesting_level] = 1
			index = numbering[nesting_level]
		elif prev_nesting_level > nesting_level:
			numbering[nesting_level] += 1
			index = numbering[nesting_level]

		complete_instruction.append({"clause": clause,
									 "index": index,
									 "nesting_level": nesting_level,
									 "numbering_type": n_type})

	for indx in range(len(clauses)):
		index = complete_instruction[indx]["index"]
		nesting_level = complete_instruction[indx]["nesting_level"]
		n_type = complete_instruction[indx]["numbering_type"]
		if n_type[0] == "arabic":
			clauses[indx] = '\t'*nesting_level + str(index) + n_type[1] + clauses[indx]

		elif n_type[0] == "roman":
			clauses[indx] = '\t'*nesting_level + str(to_roman(index)) + n_type[1] + clauses[indx]

		elif n_type[0] == "bullet":
			clauses[indx] = '\t'*nesting_level + n_type[1] + clauses[indx]

		elif n_type[0] == "latin":
			clauses[indx] = '\t'*nesting_level + consts.latin_alphabet[index-1] + n_type[1] + clauses[indx]

	instruction = "".join(clauses)

	# return instruction
	return clauses

def check_abiword():
	try:
		sb.call(["abiword", "--help"], stdout=sb.DEVNULL, stderr=sb.DEVNULL)
	except FileNotFoundError:
		logger.critical("abiword is not installed in the system.")
		raise SystemError("abiword is not installed in your system. "
			"If you use apt package manager try \"sudo apt install abiword\".")

	return 0

def check_os():
	global pltform
	pltform = platform 

	if platform == "linux" or platform == "linux2":
		if check_abiword() == 0:
			return platform

def parse_formats(fmts):
	if ('j' in fmts) and ('p' not in fmts):
		logger.error(f"Invalid formats: {fmts}. You can't use 'j' without 'p'.")
		raise ArgumentTypeError("Invalid value")

	if ('p' in fmts) and ('d' not in fmts):
		logger.error(f"Invalid formats: {fmts}. You can't use 'p' without 'd'.")
		raise ArgumentTypeError("Invalid value")

	if ('p' in fmts):
		check_os()

	return fmts

def mm_to_px(mm, dpi=300):
	return int((mm * (dpi/25.4)))

def PDFunits_to_px(units, dpi=300):
	inch = units / 72
	mm = inch * 25.4
	return mm_to_px(mm, dpi)

def calculate_logo_coords():
	logo_coords = []
	logo_coords.append([int(mm_to_px(consts.left_margin.mm)) - consts.logo_offset,
		int(mm_to_px(consts.top_margin.mm)) - consts.logo_offset])
	logo_coords.append([int(mm_to_px(consts.left_margin.mm + consts.logo_w.mm)),
		int(mm_to_px(consts.top_margin.mm + consts.logo_h.mm))])

	return logo_coords

def calculate_sign_coords(tmx, tmy, new_page=False):
	sign_coords = []

	if not new_page:
		(x1, y1) = (tmx+consts.PDFunits_offset[0], tmy+consts.PDFunits_offset[1]) # PDF units
			
		x1 = PDFunits_to_px(x1)
		y1 = PDFunits_to_px(y1)
		x0 = mm_to_px(consts.sign_w.mm)
		y0 = mm_to_px(consts.sign_h.mm)

		(x2, y2) = (x1 + x0, y1 + y0)

	else:
		offset = 4 # px

		x0 = mm_to_px(consts.sign_w.mm)
		y0 = mm_to_px(consts.sign_h.mm)

		x2 = PDFunits_to_px(consts.page_w) - mm_to_px(consts.right_margin.mm) - offset
		y1 = mm_to_px(consts.top_margin.mm) - offset

		x1 = x2 - x0 - offset
		y2 = y1 + y0 + offset
	
	sign_coords.append([x1, y1])
	sign_coords.append([x2, y2])

	return sign_coords

def calculate_seal_coords(sign_coords, new_page=False):
	if not new_page:

		x1 = sign_coords[0][0] + consts.seal_offset[0]
		y1 = sign_coords[1][1] + consts.seal_offset[1]

		x0 = mm_to_px(consts.seal_w.mm)
		y0 = mm_to_px(consts.seal_h.mm) + 25 # оффсет для нижней границы

		(x2, y2) = (x1 + x0, y1 + y0)

		seal_coords = [[x1, y1], [x2, y2]]

	else:
		offset = 4

		x0 = mm_to_px(consts.seal_w.mm) + offset
		y0 = mm_to_px(consts.seal_h.mm) + offset

		x2 = PDFunits_to_px(consts.page_w) - mm_to_px(consts.right_margin.mm) - offset
		y1 = mm_to_px(consts.top_margin.mm) - offset

		x1 = x2 - x0 - offset
		y2 = y1 + y0 + offset

		seal_coords = [[x1, y1], [x2, y2]]

	return seal_coords
