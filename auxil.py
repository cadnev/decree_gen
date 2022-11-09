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

def generate_date():
	day = randint(1, 31)
	month = randint(1, 12)
	year = randint(2000, 2022)

	try:
		date = russian_datetime.date(year, month, day).strftime(choice(consts.formats))
	except ValueError:
		return generate_date()

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
			clauses[indx] = " "*4*nesting_level + str(index) + n_type[1] + clauses[indx]

		elif n_type[0] == "roman":
			clauses[indx] = " "*4*nesting_level + str(to_roman(index)) + n_type[1] + clauses[indx]

		elif n_type[0] == "bullet":
			clauses[indx] = " "*4*nesting_level + n_type[1] + clauses[indx]

		elif n_type[0] == "latin":
			clauses[indx] = " "*4*nesting_level + consts.latin_alphabet[index-1] + n_type[1] + clauses[indx]

	instruction = "".join(clauses)

	return instruction

def check_abiword():
	try:
		sb.call(["abiword", "--help"], stdout=sb.DEVNULL, stderr=sb.DEVNULL)
	except FileNotFoundError:
		logger.critical("abiword is not installed in the system.")
		raise SystemError("abiword is not installed in your system. "
			"If you use apt package manager try \"sudo apt install abiword\".")

	return 0

# Возвращает string с именем платформы, если всё хорошо
# Если чего-то не хватает, вызывает исключение
def check_os():
	global pltform
	pltform = platform 

	logger.info(f"Current platform: {platform}")

	if platform == "windows":
		try:
			from comtypes import client
		except ImportError:
			loggger.critical(f"Can't import comtypes on {platform}.")
			raise ImportError("Can't import comtypes.")
		finally:
			return platform

	elif platform == "linux" or platform == "linux2":
		if check_abiword() == 0:
			return platform

def parse_formats(fmts):
	if ('j' in fmts) and ('p' not in fmts):
		logger.error(f"Invalid formats: {fmts}. You can't use 'j' without 'p'.")
		raise ArgumentTypeError("Invalid value")

	if ('p' in fmts):
		check_os()

	return fmts
