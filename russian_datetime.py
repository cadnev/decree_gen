from datetime import date as dt

Bs = ["января", "февраля", "марта", "апреля", "мая", "июня",
	"июля", "августа", "сентября", "октября", "ноября", "декабря"]
bs = ["янв", "фев", "мар", "апр", "мая", "июня",
	"июля", "авг", "сен", "окт", "ноя", "дек"]

class date(dt):
	def __init__(self, year, month, day):
		dt(year, month, day)
		
	def strftime(self, format):
		if ("%b" in format):
			format = format.replace("%b", bs[self.month-1])
			return dt(self.year, self.month, self.day).strftime(format)
		elif ("%B" in format):
			format = format.replace("%B", Bs[self.month-1])
			return dt(self.year, self.month, self.day).strftime(format)
		else:
			return dt(self.year, self.month, self.day).strftime(format)

