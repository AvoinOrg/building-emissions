import pandas as pd


def read_datasets(directory, dataset_names, dataset_extensions):
	'''Reads all datasets into csv from a directory specfied.

	Params
	------
	directory: string, relative directory to where the function is called,
	specifies the location of the datasets
	dataset_names: list of dataset names (used as keys in returned object)
	dataset_extensions: list of file extensions of datasets

	Returns
	--------
	Dictionary with dataset names as keys and dataframes as values
	'''

	datasets = {}

	for name, ext in zip(dataset_names, dataset_extensions):
		try:
			datasets[name] = pd.read_csv(directory+name+ext)
		except Exception as e:
			print(e)

	return datasets


def sel_cols(old_names, new_names, df):
	'''Selects columns based on old_names, updates their names to new_names,
	and returns a dataframe with these columns.

	Params
	------
	old_names: list, columns of the original dataset to select
	new_names: list, columns names to use for the selected columns
	df: dataframe containing the data

	Returns
	-------
	Dataframe with selected columns that have been renamed
	'''
	if len(old_names) != len(new_names):
		raise Exception('length of name arrays should match: {} != {}'
			.format(len(old_names), len(new_names)))

	mapper = {}

	for key, name in zip(old_names, new_names):
		mapper[key] = name

	return pd.DataFrame(df[old_names]).rename(columns=mapper, errors='raise')


def col_types(desired_types, df, v=True):
	'''Checks the column types of df and changes them to the desired type if possible.

	Params
	------
	desired_types: list of desired columns types for df (should be in the same order as columns)

	Returns
	-------
	Dataframe with correct types if possible, or an error
	'''

	if len(desired_types) != len(df.columns):
	raise Exception('length of name arrays should match: {} != {}'
		.format(len(desired_types), len(df.columns)))

	for col, dt in zip(df.columns, desired_types):

		if not df[col].dtype == dt:
			try:
				df = df.astype({col: dt})
			except Exception as e:
				print('{} not converted to {}'. format(col, dt))
				print(e)

	v and print(df.dtypes)

	return df


def parse_datasets(original_cols, renamed_cols, col_dtypes, df, v=True):
	'''Parses a dataset by selecting columns, renaming them, checking column datatypes.

	Params
	------
	original_cols: list, columns of the original dataset to select
	renamed_cols: list, columns names to use for the selected columns
	col_dtypes:  list of desired columns types for df (should be in the same order as columns)
	df: dataframe containing the data


	Returns:
	--------
	Dictionary with dataset names as keys and dataframes as values
	'''

	_df = sel_cols(original_cols, renamed_cols, df)
	return col_types(col_dtypes, _df, v=v)