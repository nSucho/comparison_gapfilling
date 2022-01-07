"""
Created on January 2022

@author: Niko Suchowitz
"""
from gap_finder import checkForGaps
import pathlib
import glob
import pandas as pd


def unify_monthly(country_dict, areatypecode, year):
	"""
	Unifies the data to make it comparable
	Unifies means:
	- filling all missing values with gaps
	- creating proper csv-files for the months

	:param country_dict: the countries which gets generalized
	:param areatypecode: the wanted areatype
	:param year: the year of the data
	:return:
	"""

	# recursive = false -> don't check subfolder
	# also sort on name, so we have it in monthly-order
	files = glob.glob('data/ActualTotalLoad_6.1.A/'+year+'_??_ActualTotalLoad_6.1.A.csv', recursive=False)
	files.sort()

	# run over every file (every file = every month) in 'files' with every country given in 'countries'
	for file in files:
		for key in country_dict:
			# read in the csv-file
			file_df = pd.read_csv(file, sep='\t', encoding='utf-8')

			# set the vars we need
			areaname = country_dict[key]+" "+areatypecode  #e.g. "EE CTA"
			mapcode = country_dict[key]

			# get the name and format it to save files with proper names
			f_df_path = pathlib.PurePath(file)
			areaname_nospace = areaname.replace(' ', '')  # get rid of whitespace
			f_df_name = f_df_path.name[:29]+'_'+areaname_nospace

			# now check for gaps and fill them with np.nan
			checkForGaps(file_df, f_df_name, areatypecode, areaname, mapcode)


def unify_year(mapcode_gapfree, year):
	"""
	Creates a df of the whole year from the csv created in unify_monthly

	:param mapcode_gapfree: mapcode of the country
	:param year: year which is wanted
	:return: df of the whole year
	"""
	# read in all the monthly csv-files of this country
	files = glob.glob('data/own_data/ActualTotalLoad_edited/'+mapcode_gapfree+'/'+year+'_??_ActualTotalLoad_6.1.A_'
	                  +mapcode_gapfree+'CTA.csv', recursive=False)
	files.sort()

	# concat to one dataframe and reset index
	df_original = pd.concat([pd.read_csv(file, sep='\t', encoding='utf-8') for file in files])
	df_original["DateTime"] = pd.to_datetime(df_original["DateTime"])
	df_original = df_original.reset_index(drop=True)

	# safe whole year as csv
	df_original.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode_gapfree+'/'+year+'_'+mapcode_gapfree+'_original.csv'
	                   , sep='\t', encoding='utf-8',
	                index=False,
	                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
	                        "MapCode", "TotalLoadValue", "UpdateTime"])

	return df_original