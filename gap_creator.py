"""
Created on January 2022

@author: Niko
"""
import numpy as np

np.random.seed(150)


def create_gaps(data_without_gaps):
	"""
	creates a df with 'frac' amount of gaps (as np.nan) from the original
	:param data_without_gaps: original df without gaps
	:return: df with gaps
	"""
	# save first the original
	data_without_gaps.to_csv("data/own_data/original_2018.csv", sep='\t', encoding='utf-8',
	                         index=False, header=["DateTime", "ResolutionCode", "AreaCode",
	                                              "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

	#TODO: funktioniert nur mit frac bis 0.05;

	df_w_gaps = data_without_gaps.copy()
	# randomly set 0.6% (0.006) of the data to np.nan
	for col in df_w_gaps.columns:
		if col == 'TotalLoadValue':
			df_w_gaps.loc[df_w_gaps.sample(frac=0.05).index, col] = np.nan

	# save with the gaps inserted
	df_w_gaps.to_csv("data/own_data/modified_2018.csv", sep='\t', encoding='utf-8',
	                 index=False, header=["DateTime", "ResolutionCode", "AreaCode",
	                                      "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

	return df_w_gaps
