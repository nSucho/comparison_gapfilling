"""
Created on January 2021

@author: Niko Suchowitz
"""
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import date
import calendar
import os


def checkForGaps(raw_df, f_df_name, areatypecode, areaname, mapcode):
	"""
	the main function to check for missing data in the csv files
	:param raw_df: the dataframe of the csv-file
	:param f_df_name: name for saving
	:param areatypecode: MBA, BZN, CTA or CTY
	:param areaname: mapcode + areatypecode
	:param mapcode: code for the country
	:return:
	"""

	# gaps are: missing 'DateTime' for that day/hour
	# DateTime is in 'YYYY-MM-DD HH:MM:00:00.000' and once per full hour

	# to cut down by more than one attr
	sorted_df = raw_df.loc[(raw_df["MapCode"] == mapcode) & (raw_df["AreaTypeCode"] == areatypecode)]
	sorted_df["DateTime"] = pd.to_datetime(sorted_df["DateTime"])
	# sort by DateTime-column
	sorted_df.sort_values(by='DateTime', inplace=True)

	# if the 'DateTime' is not in hourly steps, we downsample to hours
	# first we have to set the 'DateTime' as index
	sorted_df = sorted_df.set_index(['DateTime'])
	# now resample
	sorted_df['TotalLoadValue'] = round(sorted_df.resample('H').mean()['TotalLoadValue'], 2)
	# now drop the unnecessary rows
	sorted_df.dropna(subset=["TotalLoadValue"], inplace=True)
	# now set 'DateTime' back as column
	sorted_df.reset_index(inplace=True)

	# now we also set up ResolutionCode and ResolutionCode, so we can later save the csv properly
	resolutioncode = sorted_df['ResolutionCode'].iloc[1]
	areacode = sorted_df['AreaCode'].iloc[1]

	"""check if start and end of month is in data"""
	# find out if first day is in list- first fill days, then hours
	firsttimestamp = (sorted_df['DateTime']).iloc[0]
	# check if 'firsttimestamp' is not first of the month
	if firsttimestamp.day != 1 or firsttimestamp.hour != 0:
		# if so create a datetime obj of the first day of month
		dayone = firsttimestamp.replace(day=1, hour=0)
		# now add to the sorted DF sorted_df, add in -1 pos and then add one to overall-index
		sorted_df.loc[-1] = (dayone, resolutioncode, areacode, areatypecode, areaname, mapcode, np.nan,
		                     dt.now())
		sorted_df.index = sorted_df.index+1
		sorted_df.sort_values(by='DateTime', inplace=True)
	# just to check if if-clause is working
	#else:
	#	print("first of the month is in list")

	# now we check for the last of the month
	lastindex = len(sorted_df.index)-1
	last_timestamp = sorted_df['DateTime'].iloc[lastindex]
	#  calendar.monthrange return a tuple
	#  (weekday of first day of the month, number of days in month)
	last_day_of_month = calendar.monthrange(last_timestamp.year, last_timestamp.month)[1]
	# checks if date is not last day of month or not last hour
	if last_timestamp.date() != date(last_timestamp.year, last_timestamp.month, last_day_of_month) or \
		last_timestamp.hour != int('23'):
		# if so we create a datetime with the last day and add it to the dataframe
		last_day_as_date = dt(last_timestamp.year, last_timestamp.month, last_day_of_month, 23)
		sorted_df.loc[-1] = (last_day_as_date, resolutioncode, areacode, areatypecode, areaname, mapcode,
		                     np.nan, dt.now())
		sorted_df.index = sorted_df.index+1
		sorted_df.sort_values(by='DateTime', inplace=True)
	# just to check if if-clause is working
	#else:
	#	print("last of the month is in list")

	# print the auxiliary-dataframe into a csv
	sorted_df.to_csv("data/own_data/sortedTotalLoad.csv", sep='\t', encoding='utf-8', index=False,
	                 header=["DateTime", "ResolutionCode", "AreaCode",
	                         "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

	"""iterate to find the gaps"""
	# compare the date then time
	# init old datetime as first datetime of dataframe and create gap-list
	old_date = firsttimestamp
	gap_list = []
	# loop over every datetime-obj check if gap by comparing new and old
	for datetime in sorted_df['DateTime']:
		# set new_date to current datetime
		new_date = datetime
		# compare the time of the dates
		gap_list = gap_list_creator(old_date, new_date, gap_list, resolutioncode, areacode, areatypecode,
		                            areaname, mapcode)
		# set the current datetime as old
		old_date = datetime

	"""create a csv with all gaps included"""
	# convert list with the gaps to a dataframe
	gap_df = pd.DataFrame(gap_list)
	# check if the gap-df is empty
	if gap_df.empty:
		#print("there are no gaps")
		gap_df.to_csv('data/own_data/gaplists/'+f_df_name+'_gap.csv', sep='\t', encoding='utf-8', index=False)
		# no gaps so final-version stays the same
		final_df = sorted_df
	else:
		gap_df.to_csv('data/own_data/gaplists/'+f_df_name+'_gap.csv', sep='\t', encoding='utf-8', index=False,
		              header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		                      "MapCode", "TotalLoadValue", "UpdateTime"])
		# concat both csv to have a list with filled in gaps then save as csv
		sorted_totalload_csv = pd.read_csv("data/own_data/sortedTotalLoad.csv", sep='\t', encoding='utf-8')
		gap_list_csv = pd.read_csv('data/own_data/gaplists/'+f_df_name+'_gap.csv', sep='\t', encoding='utf-8')
		dataframes = [sorted_totalload_csv, gap_list_csv]
		final_df = pd.concat(dataframes)

	# sort everything on the DateTime-column and save as csv
	final_df.sort_values(by='DateTime', inplace=True)
	final_df.reset_index(drop=True, inplace=True)
	# save the final df as csv, check first if folder exists
	isExist = os.path.exists('data/own_data/ActualTotalLoad_edited/'+mapcode)
	if not isExist:
		os.makedirs('data/own_data/ActualTotalLoad_edited/'+mapcode)
		print("The new directory for "+mapcode+" is created!")
	# now safe
	final_df.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/'+f_df_name+'.csv', sep='\t', encoding='utf-8',
	                index=False,
	                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
	                        "MapCode", "TotalLoadValue", "UpdateTime"])


def gap_list_creator(old_date, new_date, gap_list, resolutioncode, areacode, areatypecode, areaname, mapcode):
	"""
	find gaps between the start and end datetime and return the whole list of gaps

	:param old_date: the date from which we start to check for gaps
	:param new_date: the final date
	:param gap_list: list with already found gaps

	The following inputs are just for proper saving
	:param resolutioncode:
	:param areacode:
	:param areatypecode: MBA, BZN, CTA or CTY
	:param areaname: mapcode + areatypecode
	:param mapcode: code for the country
	:return: updated list of gaps found in data
	"""
	# add an hour to check for gap
	old_h_added = old_date+pd.Timedelta(1, unit='H')

	# if old_h_added is same or bigger than new_date we have no gap
	if old_h_added >= new_date:
		return gap_list
	else:
		# add every missing datetime between start(old_date) and end(new_date); start exclusive
		for timestamp in pd.date_range(old_date, new_date, freq='H', closed='right'):
			# because end is inclusive we have to check if we reached the end
			if timestamp != new_date:
				# create a datetime obj from the timestamp
				datetime_obj = timestamp.to_pydatetime()
				# saves the gap with null-value
				gap_list.append((datetime_obj, resolutioncode, areacode, areatypecode, areaname, mapcode,
				                 np.nan, dt.now()))
		return gap_list
