"""
Created on December 2021

@author: Niko Suchowitz
"""
import interpolate_n_plot as plt
from gap_creator import create_gaps
from nan_index_duplicator import duplicate_nans
from unify_data import unify_monthly, unify_year
import pandas as pd
# deactivates unnecessary warnings of pandas
pd.options.mode.chained_assignment = None  # default='warn'


def readin_n_sort_data():
	"""
	Prepare the data, so it is possible to fill in the gaps; Then fill those gaps and plot it

	:return:
	"""
	# all the countries we want to check in the files and also the areatype
	# Key: Value = Country: MapCode
	countries = {'Estonia': 'EE', 'Austria': 'AT', 'Italy': 'IT'}
	# MBA, BZN, CTA or CTY(most of the time all have the same values, so doesn't matter)
	areatypecode = "CTA"
	# choose the year of which the data gets generalized (earliest 2014)
	# 2014 has the most gaps
	year = "2018"

	# here the wanted data gets unified
	unify_monthly(countries, areatypecode, year)

	# now choose 'mapcode' of the gap-less country (original) to fill with gaps
	mapcode_gapfree = 'AT'
	# if the gaps should be duplicatet from another country, choose the 'mapcode' of the country with gaps here
	mapcode_wgap = 'EE'

	# unify the data to have a df of a whole year
	df_original = unify_year(mapcode_gapfree, year)

	# calc missing data in original in percent
	missing_percent_o = calc_missing_data(df_original)
	print('amount of NaN in original: '+str(missing_percent_o))
	print(round(missing_percent_o, 2), "Percent is missing Data of "+mapcode_gapfree)

	# if there are no gaps in the df, fill in random gaps
	if missing_percent_o == 0:
		# create manually random gaps or duplicate gaps from another country;
		# comment the other out
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
