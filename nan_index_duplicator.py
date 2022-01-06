"""
Created on January 2021

@author: Niko Suchowitz
"""
import pandas as pd
import numpy as np
import glob


def duplicate_nans(df_wout_nan, code_gap_data):
	"""
	duplicates the empty rows into a gapfree dataframe
	:param df_wout_nan: the dataframe we want to fill with gaps
	:param code_gap_data: mapcode of the dataframe we want to duplicate the gaps from
	:return: dataframe with the duplicated gaps
	"""
	# copy so we don't modify the original
	df_wout_copy = df_wout_nan.copy()
	# read in the data with gaps
	df_w_nan = readin_gap_file(code_gap_data)

	# create an array of the indexes with nan
	nan_indexes = pd.isnull(df_w_nan).any(1).to_numpy().nonzero()

	# duplicate gaps in gap-less file
	for gap_index in nan_indexes[0]:
		df_wout_copy.loc[gap_index, "TotalLoadValue"] = np.nan

	return df_wout_copy


def readin_gap_file(code_gap_data):
	"""
	Read in data with the gaps you want to duplicate by choosing a mapcode

	:return: file with gaps df
	"""
	# choose mapcode of the data you want to read in
	country_code = code_gap_data

	# read in all the monthly csv-files of this country
	files = glob.glob('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_??_ActualTotalLoad_6.1.A_'
	                  +country_code+'CTA.csv', recursive=False)
	files.sort()

	# concat to one dataframe and reset index
	raw_df = pd.concat([pd.read_csv(file, sep='\t', encoding='utf-8') for file in files])
	raw_df["DateTime"] = pd.to_datetime(raw_df["DateTime"])
	df_finished = raw_df.reset_index(drop=True)

	return df_finished
