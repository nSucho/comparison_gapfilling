"""
Created on January 2021

@author: Niko Suchowitz
"""
import pandas as pd


def duplicate_nans(df_w_nan, df_wout_nan):
	"""
	duplicates the empty rows into a gapfree dataframe
	:param df_w_nan: dataframe one with the gaps to duplicate
	:param df_wout_nan: dataframe two without any gaps
	:return: dataframe two with the gaps of dataframe one inserted
	"""
	# first copy both so we do not change the original df's
	df_w_copy = df_w_nan.copy()
	df_wout_copy = df_wout_nan.copy()

	nan_indexes = get_index_of_nan(df_w_nan)

	print(nan_indexes)

def get_index_of_nan(df_w_nan):
	"""
	creates a array with the indexes of the gaps
	:param df_w_nan: the dataframe with empty rows
	:return: array with the indexes of the empty rows
	"""
	nan_indexes = pd.isnull(df_w_nan).any(1).nonzero()[0]

	return nan_indexes
