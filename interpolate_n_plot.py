"""
Created on December 2021

@author: Niko
"""
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 18, 7
from sklearn.metrics import mean_absolute_error
from interpolation_avgweek import averageWeek as avgweek
from interpolation_polyreg import fill_missing_data as polyreg
from interpolation_fedot import fedot_method as fedot_f

#TODO: immer wenn predicted wird smape oder mape berechnen


def plotTheData(original, final_df, save_name, mapcode, missing_data_perc):
	"""
	interpolate and plot the data
	:param original: the original df without gaps
	:param final_df: dataframe with the data to plot (with missing values as NaN)
	:param save_name: the name of the country to save it more precise as csv
	:param mapcode: map code of the country we plot
	:param missing_data_perc: amount of missing-data of 'final_df' in percentage
	:return:
	"""
	# if there are missing values, do first an interpolation and than plot it
	if missing_data_perc != 0:
		original_series = np.array(original['TotalLoadValue'])
		# interpolation with average week; standard
		avg_week = avgweek(final_df)
		# save the filled df as csv
		avg_week.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/avg_week/'+save_name+'_filled_avg.csv',
		                sep='\t', encoding='utf-8', index=False,
		                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		                        "MapCode", "TotalLoadValue", "UpdateTime", "Week"])
		# create an array to calculate the mean absolute error
		avg_week_series = np.array(avg_week['TotalLoadValue'])

		# interpolation with polynomial linear regression; master-thesis
		poly_reg = polyreg(final_df, 1)
		# save the filled df as csv
		poly_reg.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/poly_reg/'+save_name+'_filled_poly.csv',
		                sep='\t', encoding='utf-8', index=False,
		                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		                        "MapCode", "TotalLoadValue", "UpdateTime"])
		# create an array to calculate the mean absolute error
		poly_reg_series = np.array(poly_reg['TotalLoadValue'])

		# interpolation with fedot; autoML
		# TODO: fedot zum laufen bringen
		fedot = fedot_f(final_df)
		# save the filled df as csv
		#fedot.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/fedot/'+save_name+'_filled_fedot.csv',
		#             sep='\t', encoding='utf-8', index=False,
		#             header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		#                     "MapCode", "TotalLoadValue", "UpdateTime"])

		# print the mape
		print(f'Mean absolute error avg-week: {mean_absolute_error(original_series, avg_week_series):.3f}')
		print(f'Mean absolute error poly-reg: {mean_absolute_error(original_series, poly_reg_series):.3f}')
		print(f'Mean absolute error fedot: {mean_absolute_error(original_series, fedot):.3f}')

		plt.plot(original_series, c='blue', alpha=0.4, label='Actual values in the gaps')
		plt.plot(avg_week_series, c='green', alpha=0.8, label='The avg-Week')
		plt.plot(poly_reg_series, c='purple', alpha=0.8, label='The Poly-Version')
		plt.plot(fedot, c='#D77214', alpha=0.8, label='FEDOT bi-directional')
		plt.ylabel('Total Load', fontsize=14)
		plt.xlabel('Time Index', fontsize=14)
		plt.legend(fontsize=14)
		plt.grid()
		plt.savefig('gaps_filled_plot.png')
		plt.show()

	else:
		print('There are no errors to interpolate')
