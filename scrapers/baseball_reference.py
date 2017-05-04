## TODO: 
## - CREATE URL FROM PARAMS: DATERANGE, TEAM, STAT-TYPE
## - 

from pandas import DataFrame
import numpy as np

from spytball.scrapers.base import ScraperBase
from spytball.utils.data import format_dataframe_columns, to_numeric, dict_to_object

class BaseballReferenceScraper(ScraperBase):
	"""
	Scraper class to pull data from the Baseball Reference website.
	"""
	BASE_URL = 'http://www.baseball-reference.com'

	def __init__(self, *args, **kwargs):
		super(BaseballReferenceScraper, self).__init__(*args, **kwargs)

	@classmethod
	def url_from_params(self, player_id=None, team_id=None, season_id=None, year_id=None):
		url = self.BASE_URL	
		return url

	def format_values(self, x):
		"""
		Apply formatting for Baseball Reference data
		"""
		if '%' in x:  # special case: values returned as percentages
			return .01 * to_numeric(x.replace('%',''))
		elif ':' in x:  # special case: times
			hour, minutes = x.split(':')
			hour = to_numeric(hour)
			minutes = float(to_numeric(minutes))/60
			return hour + minutes
		else:
			return to_numeric(x)

	def is_valid_table(self, tag):
		"""
		BR-specific checks for valid tables
		"""

		# if "class" not in tag:
		if not tag.has_key("class"):  # strange bug: deprecated behavior works, but not standard
			return False
		return tag.name == "table" and "stats_table" in tag["class"] and "sortable" in tag["class"]

	def is_valid_row(self, tag):
		"""
		BR-specific checks for valid rows
		"""
		if not tag.name == "tr": 
			return False
		if "class" not in tag: 
			return True  # permissive
		return "league_average_table" not in tag["class"] and "stat_total" not in tag["class"]

	
	def data_from_url(self, url, table_ids=None):
		"""
		BR-specific data parsing
		"""
		
		# get all tables
		tables = self.parse_tables_from_url(url)

		# compile dataset {key, DataFrame} pairs
		data = {}
		for idx, table in enumerate(tables):

			# key collision, so don't overwrite	data
			# include info about position on page for 
			# back-reference
			table_id = table['id']
			if table_id in data:
				table_id += ' (table %d)' % (idx+1)
			
			# skip non-requested tables
			if table_ids is not None and table_id not in table_ids:  
				continue

			columns = self.parse_table_columns(table)
			rows = self.parse_rows(table)
			
			# detect if there's a hierarchical organization,
			# use last column names for data column headers
			num_xtra_columns = len(columns) - len(rows[0])
			if num_xtra_columns > 0:
				print 'WARNING: extra columns for table `%s`:' % table_id
				print ','.join(columns[:num_xtra_columns])
				columns = columns[num_xtra_columns:]
			
			# create pandas dataframe from data
			df = DataFrame(rows, columns=columns)
			
			# if more than half of columns in a row are bad, we ignore them
			df.dropna(thresh=np.floor(len(df.columns)/2), inplace=True)
			
			# make columns useable and store in dataset
			data[table_id] = format_dataframe_columns(df, self.format_values)

		return dict_to_object(data)