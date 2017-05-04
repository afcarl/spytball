from spytball.utils.html import parse_tables_from_url, parse_table_rows, parse_table_columns

class ScraperBase(object):
	def __init__(self, parser='lxml'):
		self.parser = parser

	def parse_tables_from_url(self, url):
		"""
		PUll all tables from HTML source
		"""
		return parse_tables_from_url(url, self.is_valid_table, parser=self.parser)

	def parse_rows(self, table):
		"""
		Parse a table, based on the current scraper's validity critereon
		"""
		return parse_table_rows(table, self.is_valid_row)

	def parse_table_columns(self, table):
		return parse_table_columns(table)


	def format_values(self, x):
		"""
		Overload me to apply site-specific formatting.
		"""
		return x

	def is_valid_row(self):
		"""
		Overload logic to determine if a row parsed from a HTML
		table contains valid data.
		"""
		return True


	def is_valid_table(self):
		"""
		Overload logic to determine if a table parsed from a site
		contains valid data.
		"""
		return True

	def data_from_url(self, url):
		"""
		Overload logic to pull site-specific data from an url. 
		Should return data as {stat_type, DataFrame} pairs
		"""
		pass
