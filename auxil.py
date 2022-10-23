import russian_datetime
import re
from loguru import logger
from sys import stdout
from random import randint, choice
import os

def logger_config(v):
	logger.remove()
	if v:
		logger.add(stdout, level="INFO")
	else:
		logger.add(stdout, level="WARNING")
	logger.add("logs/gen.log", level = "INFO", rotation="10 MB")

def generate_date():
	formats = ["%d %B %Y года", "%d %B %y", "%d %b %Y г.", "%d %b %y", "%d.%m.%Y", "%d.%m.%y"]

	day = randint(1, 31)
	month = randint(1, 12)
	year = randint(2000, 2022)

	try:
		date = russian_datetime.date(year, month, day).strftime(choice(formats))
	except ValueError:
		return generate_date()

	return date

def check_size_format(size, pat=re.compile(r"^\d*[KMG]B$")):
	if not pat.match(size):
		logger.error(f"Invalid size argument: {size}")
		raise argparse.ArgumentTypeError("invalid value")
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