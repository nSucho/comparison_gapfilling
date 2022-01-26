"""
Created on December 2021

@author: Niko Suchowitz
"""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from interpolation_avgweek import averageWeek as avgweek
from interpolation_polyreg import fill_missing_data as polyreg
from interpolation_fedot import fedot_method as fedot
from plot_file import *


def fill_and_valid(original, df_w_gaps, save_name, mapcode, missing_data_perc):
	"""
	interpolate and afterwards plot the data
	:param original: the original df without gaps
	:param df_w_gaps: dataframe with the data to plot (with missing values as NaN)
	:param save_name: the name of the country to save it more precise as csv
	:param mapcode: map code of the country we plot
	:param missing_data_perc: amount of missing-data of 'final_df' in percentage
	:return:
	"""
	# if there are missing values, do first an interpolation and then plot it
	if missing_data_perc != 0:
		original_series = np.array(original['TotalLoadValue'])
		# interpolation with average week; standard
		avg_week = avgweek(df_w_gaps, mapcode, save_name)
		# create an array to calculate the mean absolute error
		avg_week_series = np.array(avg_week['TotalLoadValue'])

		# interpolation with polynomial linear regression; master-thesis
		poly_reg = polyreg(df_w_gaps, 1, mapcode, save_name)
		# create an array to calculate the mean absolute error
		poly_reg_series = np.array(poly_reg['TotalLoadValue'])

		# interpolation with fedot; autoML
		fedot_forward, fedot_bidirect = fedot(df_w_gaps, mapcode, save_name)

		# print the MAE for validation; represents the difference between the original and predicted values
		with open("results.txt", "a") as file_object:
			file_object.write(
				f'Mean absolute error avg-week: {mean_absolute_error(original_series, avg_week_series):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Mean absolute error poly-reg: {mean_absolute_error(original_series, poly_reg_series):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Mean absolute error fedot-forward: {mean_absolute_error(original_series, fedot_forward):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Mean absolute error fedot-bidirect: {mean_absolute_error(original_series, fedot_bidirect):.3f}')
			file_object.write("\n")
			file_object.write("-----")
			file_object.write("\n")
		# print the RMSE for validation; is the error rate by the square root of MSE
			file_object.write(
				f'Root Mean Squared Error avg-week: {np.sqrt(mean_squared_error(original_series, avg_week_series)):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Root Mean Squared Error poly-reg: {np.sqrt(mean_squared_error(original_series, poly_reg_series)):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Root Mean Squared Error fedot-forward: {np.sqrt(mean_squared_error(original_series, fedot_forward)):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Root Mean Squared Error fedot-bidirect: {np.sqrt(mean_squared_error(original_series, fedot_bidirect)):.3f}')
			file_object.write("\n")
			file_object.write("-----")
			file_object.write("\n")
		# print the R^2 for validation; represents the difference between the original and predicted values
			file_object.write(
				f'Coefficient of determination avg-week: {r2_score(original_series, avg_week_series):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Coefficient of determination poly-reg: {r2_score(original_series, poly_reg_series):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Coefficient of determination fedot-forward: {r2_score(original_series, fedot_forward):.3f}')
			file_object.write("\n")
			file_object.write(
				f'Coefficient of determination fedot-bidirect: {r2_score(original_series, fedot_bidirect):.3f}')
			file_object.write("\n")
			file_object.write("-----")
			file_object.write("\n")

		#plot_data1(original_series, avg_week_series, poly_reg_series, fedot_forward)
		#plot_data2(original, df_w_gaps, avg_week, poly_reg, fedot_forward, fedot_bidirect)

	else:
		print('There are no errors to interpolate')
