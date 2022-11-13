import write
import auxil
import consts
import change_case

from random import choice, randint
import argparse
from os import makedirs
import re
from time import time
import json

from loguru import logger

def load_samples(samples_dir):
	with open(samples_dir + "/headers.txt") as headerfile:
		header = headerfile.read().split(";;\n")

	with open(samples_dir + "/names.txt") as namefile:
		name = namefile.read().split(";;\n")

	with open(samples_dir + "/intros.txt") as introfile:
		intro = introfile.read().split(";;\n")

	with open(samples_dir + "/instructions.json") as instructionfile:
		all_instructions = json.load(instructionfile)
		instructions = []

		for _ in range(randint(1, 7)):
			instructions.append(choice(all_instructions))

		# Удаление повторяющихся элементов
		i = []
		for e in instructions:
			if e not in i:
				i.append(e)
		instructions = i

	with open(samples_dir + "/execution_control.txt") as execution_controlfile:
		execution_control = execution_controlfile.read().split('\n')

	with open(samples_dir + "/responsible.txt") as responsiblefile:
		responsible = responsiblefile.read().split(";;\n")

	with open(samples_dir + "/creators.txt") as creatorfile:
		creator = creatorfile.read().split('\n')

	logger.debug(f"[header] length: {len(header)}")
	logger.debug(f"[name] length: {len(name)}")
	logger.debug(f"[intro] length: {len(intro)}")
	logger.debug(f"[all_instructions] length: {len(all_instructions)}")
	logger.debug(f"[execution_control] length: {len(execution_control)}")
	logger.debug(f"[responsible] length: {len(responsible)}")
	logger.debug(f"[creator] length: {len(creator)}")

	return (header, name, intro, instructions, execution_control, responsible, creator)

def generate(data, out, formats, size, samples_dir):
	logger.info(f"Using formats: {formats}")

	try:
		makedirs(out+"/json")
		if 'd' in formats:
			makedirs(out+"/docx")
		if 'p' in formats:
			makedirs(out+"/pdf")
		if 'j' in formats:
			makedirs(out+"/jpg")
	except FileExistsError:
		pass

	measure_time = 1
	count = 0
	start = time()
	while True:
		header = choice(data[0])
		name = choice(data[1])
		intro = choice(data[2])
		instruction = data[3]
		execution_control = choice(data[4])

		# Шанс 33% на наличие ответственных в приказе
		if randint(1, 3) == 1:
			responsible = choice(data[5])
			responsible = change_case.create_responsible(execution_control, responsible)
		else:
			responsible = ""

		creator = choice(data[6])
		date = auxil.generate_date()

		instruction = write.extend_instruction(instruction, samples_dir)

		write.write_json(instruction, responsible, date, out, count)

		if 'd' in formats:
			docx_path = write.write_docx(header, name, intro, instruction,
				responsible, creator, date, out, count)
		if 'p' in formats:
			# write.write_pdf(header, name, intro, instruction,
				# responsible, creator, date, out, count)

			platform = auxil.pltform

			if platform == "windows":
				write.write_pdf_windows(docx_path, out, count)
			elif platform == "linux" or platform == "linux2":
				write.write_pdf_linux(docx_path, out, count)

		if 'j' in formats:
			write.write_jpg(out, count)

		count += 1
		if count % 25 == 0:
			if auxil.getsize(out) >= size:
				logger.warning(f"Size of {out} dir: {auxil.getsize(out)} bytes")
				break

		if measure_time:
			if count % 100 == 0:
				avg_speed = auxil.getsize(out) / (time()-start)
				full_time = round((size) / (avg_speed*60), 2)
				measure_time = 0
				if full_time < 1:
					logger.warning("Approximate generation time: "
								  f"{round(full_time*60, 2)} s.")
				else:
					logger.warning("Approximate generation time: "
								  f"{full_time} min.")


def get_args():
	parser = argparse.ArgumentParser(
		description="Decrees generator",
		epilog="Example: python3 gen.py 50MB -f dp -s samples -o decrees -vv")

	parser.add_argument("size", help="Max size of output dir. For example: 10KB, 10MB, 10GB",
						type=auxil.check_size_format)
	parser.add_argument("-f", "--format", help="Formats to save (docx: d, pdf: p, jpg: j)",
						type=auxil.parse_formats, default="d", metavar="format")
	parser.add_argument("-s", "--samples", help="Path to dir with samples",
						metavar="path", type=str, default="./samples/")
	parser.add_argument("-o", "--out", help="Path for output files",
						metavar="path", type=str, default="./decrees")
	parser.add_argument("-v", "--verbose", action="count", default=0)

	return parser.parse_args()

def main():
	global args

	args = get_args()
	auxil.logger_config(args.verbose)

	data = load_samples(args.samples)
	bytes_size = auxil.size_to_bytes(args.size)

	generate(data, args.out, args.format, bytes_size, args.samples)

	logger.warning("Generation is finished!")

if __name__ == '__main__':
	main()
