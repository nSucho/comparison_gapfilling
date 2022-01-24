"""
Created on January 2022

- you have to use the version 0.5 of FEDOT
- if there is a gap between data point 2 and 7 hands error (last day checked: 6. January 2022)

@author: Niko Suchowitz
"""
import numpy as np

np.random.seed(15)


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
	# create copy so we do not change original
	df_w_gaps = data_without_gaps.copy()

	# randomly set frac-amount of the data to np.nan
	# frac = 0.1 means 10% of the data will be gaps
	for col in df_w_gaps.columns:
		if col == 'TotalLoadValue':
			df_w_gaps.loc[df_w_gaps.sample(frac=0.05).index, col] = np.nan

	# save with the gaps inserted
	df_w_gaps.to_csv("data/own_data/modified_2018.csv", sep='\t', encoding='utf-8',
	                 index=False, header=["DateTime", "ResolutionCode", "AreaCode",
	                                      "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

	return df_w_gaps
