"""
Created on December 2021

@author: Niko Suchowitz
"""
import pandas as pd
import os


def averageWeek(data_w_nan, mapcode, save_name):
	"""
	The method which is used until now
	'The gaps in this filtered data set are filled using an average week for each border.
	For each month and border, the hourly time series then is scaled such that the aggregate corresponds to the
	monthly value published on the Power Statistics web page.'
	:param data_w_nan: the data with gaps (NaN) to fill
	:param mapcode: mapcode to save file properly
	:param save_name: name to save file properly
	:return: the data with the gaps filled by the average of the corresponding week
	"""
	"""
	How they call it in the original code
	"if interpolate_data == True:\n",
    "    #generate an average week for each link\n",
    "    bc_average_week = aux.transform_to_average_week(cbf_processed)\n",
    "    #fill nan with average week data\n",
    "    cbf_processed = cbf_processed.fillna(bc_average_week)"
	
	the original code (did not work for my code): 
	groups = [data_w_nan.index.dayofweek, data_w_nan.index.hour]
	return data_w_nan.groupby(groups).transform('mean')
	"""
	# TODO: small gaps (up to 3 hours) fill with linear interpolation
	# first we make a copy, so we don't change the original df
	new_data_w_nan = data_w_nan.copy()

	# we add the week of the month to the rows
	new_data_w_nan['Week'] = pd.factorize(new_data_w_nan['DateTime'].dt.isocalendar().week)[0]+1

	# now we fill all NaN's with the mean of this week;
	# rounded to two numbers for testing reason;
	# inplace=True -> so it writes the value directly into the df new_data_w_nan
	new_data_w_nan['TotalLoadValue'].fillna(new_data_w_nan.groupby('Week')['TotalLoadValue'].transform('mean'),
	                                        inplace=True)

	#first check if folder exists
	isExist = os.path.exists('data/own_data/ActualTotalLoad_edited/'+mapcode+'/avg_week')
	if not isExist:
		os.makedirs('data/own_data/ActualTotalLoad_edited/'+mapcode+'/avg_week')
	# save the filled df as csv
	new_data_w_nan.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/avg_week/'+save_name+'_filled_avg.csv',
	                      sep='\t', encoding='utf-8', index=False,
	                      header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
	                              "MapCode", "TotalLoadValue", "UpdateTime", "Week"])

	return new_data_w_nan
