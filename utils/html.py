from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup

def make_soup(url, parser='lxml'):
	"""
	Request response from `url` and instantiate a BeuatifulSoup
	parsing engine.
	"""
	try:
		resp = urlopen(url)
	except URLError as e:
		print 'An error occured fetching %s \n %s' % (url, e.reason)   
		return None
	return BeautifulSoup(resp.read(), parser)


def parse_table_cell(cell):
	"""
	Parse the contents of a HTML table cell
	"""
	cell_contents = cell.contents
	content_str = ''
	if cell_contents is not None:
		for c in cell_contents:
			if c.name is None or c.name == 'a':
				content_str += c.string.strip()
	return content_str

def parse_table_rows(table, valid_row_criterion):
	"""
	Parse the rows of an HTML table
	"""
	rows = table.find("tbody").find_all(valid_row_criterion)
	data = []
	for row in rows:
		cells = row.find_all("td")
		row_data = [parse_table_cell(cell) for cell in cells]            
		data.append(row_data)
			
	return data

def parse_tables_from_url(url, valid_table_criterion, parser='lxml'):
	"""
	Extract all HTML tables from the source associated with `url`
	"""
	soup = make_soup(url, parser)

	# get tables
	try:
		# deterimine if tables have useful data
		tables = soup.find_all(valid_table_criterion)
		return tables
	except AttributeError as e:
		print 'No tables found, exiting'
		print e
		return None


def parse_table_columns(table, verbose=False):
	"""
	Parse the columns of an HTML `table`.
	"""
	headers = table.find("thead").find_all("th")
	column_names = []
	for header in headers:
		if header.string is None: 
			base_column_name = ''.join([v.string.strip() for v in header.contents])
		else: 
			base_column_name = header.string.strip()
		if base_column_name in column_names:
			i = 1
			column_name = base_column_name + "_%s" % str(i)
			while column_name in column_names:
				i += 1
				column_name = base_column_name + "_%s" % str(i)
			if verbose: 
				if base_column_name == "":
					print "Empty header relabeled as %s" % column_name
				else:
					print "Header %s relabeled as %s" % (base_column_name, column_name)
		else:
			column_name = base_column_name
		column_names.append(column_name)
	return column_names

