import numpy as np


def dict_to_object(item):
    """
    Recursively convert a dictionary to an object.
    """
    def convert(item):
        if isinstance(item, dict):
            return type('SpytballDict', (), {k: convert(v) for k, v in item.iteritems()})
        if isinstance(item, list):
            def yield_convert(item):
                for index, value in enumerate(item):
                    yield convert(value)
            return list(yield_convert(item))
        else:
            return item
    return convert(item)

def is_numeric(x):
	"""
	Determine if `x` can be cast as a number.
	"""

	if x == '':
		return True  # cast empty values as this as a nan

	if isinstance(x, int) or isinstance(x, float):
		return True
	else:
		try:
			float(x.replace(',','').replace('$',''))
			return True
		except:
			return False

def as_numeric(x):
	"""
	Return `x` as a number
	"""

	if x == '':
		return np.NaN 
	try:
		return int(x)
	except:
		return float(x)
	
def to_numeric(x):
	"""
	If possible, convert `x` to a number, otherwise 
	"""
	if is_numeric(x):
		if isinstance(x, basestring):
			return as_numeric(x.replace(',','').replace('$',''))
		else:
			return x
	else:
		if isinstance(x, basestring):
			# x.replace('\n','').replace('\t','')
			return x.strip()


def format_dataframe_columns(df, format_fun=lambda x: x):
	"""
	Apply formatting function `format_fun` to all columns in the
	dataframe `df`.
	"""
	for col in df.columns:
		df[col] = df[col].apply(format_fun)
	return df