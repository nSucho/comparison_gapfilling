"""
Created on December 2021

@author: Niko Suchowitz
"""
import glob
import pathlib
import interpolate_n_plot as plt
from gap_creator import create_gaps
from gap_finder import checkForGaps
from nan_index_duplicator import duplicate_nans
import pandas as pd
# deactivates unnecessary warnings of pandas
pd.options.mode.chained_assignment = None  # default='warn'


def readin_n_sort_data():
	"""
	Prepare the data, so its possible to fill in the gaps; Then fill those gaps and plot it

	:return:
	"""
	# all the countries we want to check in the files and also the areatype
	# Key: Value = Country: MapCode
	countries = {'Estonia': 'EE', 'Austria': 'AT'}
	# MBA, BZN, CTA or CTY(most of the time all have the same values, so doesn't matter)
	areatypecode = "CTA"

	# read in all file names of the year 20XX(the earliest possible is 2014) with ActualTotalLoad as a list
	# recursive = false -> don't check subfolder
	# also sort on name, so we have it in monthly-order
	files = glob.glob('data/ActualTotalLoad_6.1.A/2018_??_ActualTotalLoad_6.1.A.csv', recursive=False)
	files.sort()

	# run over every file (every file = every month) in 'files' with every country given in 'countries'
	for file in files:
		for key in countries:

			# read in the csv-file
			file_df = pd.read_csv(file, sep='\t', encoding='utf-8')

			# set the vars we need
			areaname = countries[key]+" "+areatypecode  #e.g. "EE CTA"
			mapcode = countries[key]

			# get the name and format it to save files with proper names
			f_df_path = pathlib.PurePath(file)
			areaname_nospace = areaname.replace(' ', '')  # get rid of whitespace
			f_df_name = f_df_path.name[:29]+'_'+areaname_nospace

			# now check for gaps and fill them with np.nan
			checkForGaps(file_df, f_df_name, areatypecode, areaname, mapcode)

	# 'mapcode' of country we want to fill gaps
	# AT is a perfekt file without gaps
	mapcode_gapfree = 'AT'
	# set the 'mapcode' you want to duplicate the gaps from
	mapcode_wgap = 'EE'

	# read in all the monthly csv-files of this country
	files = glob.glob('data/own_data/ActualTotalLoad_edited/'+mapcode_gapfree+'/2018_??_ActualTotalLoad_6.1.A_'
	                  + mapcode_gapfree+'CTA.csv', recursive=False)
	files.sort()

	# concat to one dataframe and reset index
	df_original = pd.concat([pd.read_csv(file, sep='\t', encoding='utf-8') for file in files])
	df_original["DateTime"] = pd.to_datetime(df_original["DateTime"])
	df_original = df_original.reset_index(drop=True)

	# calc missing data in Original in percent
	missing_percent_o = calc_missing_data(df_original)
	print('amount of NaN in original: '+str(missing_percent_o))
	print(round(missing_percent_o, 2), "Percent is missing Data of "+mapcode_gapfree)

	# if there are no gaps in the df, fill in random gaps
	if missing_percent_o == 0:
		# create manually random gaps or duplicate gaps from another country
		# manually
		data_with_gaps = create_gaps(df_original)
		# duplicate
		#data_with_gaps = duplicate_nans(df_original, mapcode_wgap)

		# calc missing data in modified in percent
		missing_percent_m = calc_missing_data(data_with_gaps)
		print('amount of NaN in modified: '+str(missing_percent_m))
		print(round(missing_percent_m, 2), "Percent is missing Data of "+mapcode_gapfree)

		# fill and plot data_with_gaps
		# also hand the original, so we can calc the error
		data_with_gaps["DateTime"] = pd.to_datetime(data_with_gaps["DateTime"])
		save_name = '2018_ActualTotalLoad_6.1.A_'+mapcode_gapfree+'CTA.csv'
		plt.plotTheData(df_original, data_with_gaps, save_name, mapcode_gapfree, missing_percent_m)
	else:
		print('There are already gaps, so we do not have a gap-less data to validate our gapfilling')


def calc_missing_data(df_to_check):
	"""
	calculates the missing data
	:param df_to_check: the df you want to check for missing data
	:return: missing data in percent
	"""

	missing_data_o = df_to_check['TotalLoadValue'].isna().sum()
	missing_percent = (missing_data_o/len(df_to_check.index))*100

	return missing_percent


if __name__ == '__main__':
	readin_n_sort_data()
