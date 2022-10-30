import russian_datetime
import consts

import re
from loguru import logger
from sys import stdout
from random import randint, choice
import os
from argparse import ArgumentTypeError

def logger_config(v):
	logger.remove()
	if v:
		logger.add(stdout, level="INFO")
	else:
		logger.add(stdout, level="WARNING")
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
		raise ArgumentTypeError("invalid value")
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

	logger.info(f"Max size of output dir: {size}, {s}B")
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
