"""
Created on December 2021

@author: Niko
"""
import pandas as pd
import numpy as np
import glob
import copy
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def fill_missing_data(df, length):
	"""
	The method created by Lovindu Wijesinghe using polynomial linear regression;

	In the original Lovindu only hands the column 'TotalLoadValue' as df. That makes it hard for me to plot it
	later, so
	I change the code a bit, that it now works with the full df I hand to the function 'fill_missing_data'.
	:param df: the full dataframe with gaps (NaN) to fill
	:param length: Quoted from the original Code:
	"Also this returns an integer ('divider') based on the file length to get the energy values
	in a later step. In 15 min interval files this is 4, in 30 min interval files this is 2 and in 1 hour interval
	files this is 1."
	I defined it as 1, because I only use full hours
	:return: the dataframe with the gaps filled by polynomial linear regression
	"""
	# TODO: DTS erstmal weggelassen
	# 1. In the following section, we get the indexes and values of a column of a dataframe to a dictionary called
	# 'column_data'.
	# 2. Then we iterate the "column_data" dictionary line by line until a null value is found (We called this index
	# as 'selected_index').
	# 3. If the index of the value is within the range of after first 3 hours and before the last 3 hours of the
	# column we create a empty list called 'selected_values'.
	# 4. Else if the index is null, but it is not in the above range, we get the mean value of first 3 hours or mean
	# value of last 3 hours according to the position of the index of the null value as the missing null value.
	# 5. In 3, We append the 'selected_values' list with the indexes of the 3 hours before the index of the null value
	# and 3 hours after the index of the null value and respective values of those indexes.
	# 6. In the 6 values of this list if more than 3 are null values and the 'selected_index' is within the range of
	# after first 27 hours and before the last 27 hours of the column we create another empty list called
	# 'selected_values'.
	# 7. Else if more than 3 are null values but not in the range mentioned above, get the mean value of the remaining
	# values in the 'selected_values' list as the missing null value.
	# 8. If both the two conditions in 6 and 7 are not met, get the missing null value by using the polynomial
	# function.
	# 9. In 6, We append the 'selected_values' list with the indexes of the (1,2,3,21,22,23,25,26,27) hours before and
	# after the index of the null value and respective values of those indexes.
	# 10. In the 18 values of this llist, if more than 12 are null values and the 'selected_index' is within the range
	# of after first 51 hours and before the last 51 hours of the column we create another empty list called
	# 'selected_values'.
	# 11. Else if more than 12 are null values but not in the range mentioned above, get the mean value of the
	# remaining values in the 'selected_values' list as the missing null value.
	# 12. If both the two conditions in 10 and 11 are not met, get the missing null value by using the polynomial
	# function.
	# 13. In 10, We append the 'selected_values' list with the indexes of the (1,2,3,21,22,23,25,26,27,45,46,47,49,50,
	# 51) hours before and after the index of the null value and respective values of those indexes.
	# 14. In the 18 values of this list, if more than 24 are null values and not all 30 are null values,
	# get the mean value of the remaining values in the 'selected_values' list as the missing null value.
	# 15. If all 30 are null values, get all the values of that particular time step of that particular day of the
	# week throughout the year (There will be nearly 52 values) and get the missing null value by using the polynomial
	# function.

	# first we make a copy, so we don't change the original df
	df_copy = df.copy()

	for column in df_copy.columns.values:
		# Only check the column with 'TotalLoadValue'
		if column == 'TotalLoadValue':
			column_data = {}
			# add all indexes with their TotalLoadValue into the dict 'column_data'
			for index, value in enumerate(df_copy.loc[:, column]):
				column_data[index] = value

			# now check every pair in the dict for NaN
			for selected_index, selected_value in column_data.items():

				if pd.isnull(column_data[selected_index]) and selected_index in range(3*length, len(df_copy[column])-3*length):
					selected_values = []
					for i in [x for x in range(-3, 4) if x != 0]:
						selected_values.append([selected_index+i*length, column_data[selected_index+i*length]])
					if pd.isnull(selected_values).sum() >= 3 and selected_index in range(27*length,
					                                                                     len(df_copy[column])-27*length):
						selected_values = []
						for i in [x for x in range(-3, 4) if x != 0]:
							for j in [-24, 0, 24]:
								selected_values.append(
									[selected_index+(i+j)*length, column_data[selected_index+(i+j)*length]])
						if pd.isnull(selected_values).sum() >= 14 and selected_index in range(51*length,
						                                                                      len(df_copy[column])-51*length):
							selected_values = []
							for i in [x for x in range(-3, 4) if x != 0]:
								for j in [-48, -24, 0, 24, 48]:
									selected_values.append(
										[selected_index+(i+j)*length, column_data[selected_index+(i+j)*length]])

							#old: if pd.isnull(selected_values).sum() >= 26 and pd.isnull(selected_values).sum() < len(selected_values):
							if 26 <= pd.isnull(selected_values).sum() < len(selected_values):
								prediction = mean([i[1] for i in selected_values])
								df_copy.loc[selected_index, column] = prediction

							elif pd.isnull(selected_values).sum() < 26:
								prediction = polynomial(selected_values, selected_index)
								df_copy.loc[selected_index, column] = prediction

							else:
								selected_values = [[i, column_data[i]] for i in range(len(df_copy[column])) if
								                   (selected_index-i)%(7*24*length) == 0]
								selected_values.sort(key=lambda x: abs(selected_index-x[0]))
								selected_values = selected_values[1:]
								prediction = polynomial(selected_values, selected_index)
								df_copy.loc[selected_index, column] = prediction

						elif pd.isnull(selected_values).sum() >= 14:
							prediction = mean([i[1] for i in selected_values])
							df_copy.loc[selected_index, column] = prediction

						else:
							prediction = polynomial(selected_values, selected_index)
							df_copy.loc[selected_index, column] = prediction

					elif pd.isnull(selected_values).sum() >= 3:
						prediction = mean([i[1] for i in selected_values])
						df_copy.loc[selected_index, column] = prediction

					else:
						prediction = polynomial(selected_values, selected_index)
						df_copy.loc[selected_index, column] = prediction
						#df.iloc[selected_index, [6]] = prediction

				elif pd.isnull(column_data[selected_index]) and selected_index < 3*length:
					selected_values = [[i, column_data[i]] for i in range(6*length)]
					prediction = polynomial(selected_values, selected_index)
					df_copy.loc[selected_index, column] = prediction

				elif pd.isnull(column_data[selected_index]) and selected_index >= (len(df_copy[column])-3*length):
					selected_values = [[i, column_data[i]] for i in range(len(df_copy[column])-6*length, len(df_copy[column]))]
					prediction = polynomial(selected_values, selected_index)
					df_copy.loc[selected_index, column] = prediction
	# df = df.replace(['n/e', np.nan], 0)
	df_copy.to_csv('data/own_data/test.csv', sep='\t', encoding='utf-8', index=False)
	return df_copy


def polynomial(selected_values, selected_index):
	"""
	The function to calculate the best fitting polynomial linear regression
	:param selected_values: The values in front and after the one (the NaN-value) we want to predict
	:param selected_index: the index of the NaN-Value we want to predict
	:return: the predicted value for the selected_index
	"""
	# We get all the indexes in the 'selected_values' to a 2D numpy array 'X'.
	# We get all the values in the 'selected_values'to a 1D numpy array 'y'
	# Then we fill the null values in array 'y' with the mean value of the array.
	# Then we divide 'X' and 'y' values in the ratio of 30% test and 70% train data.
	# We create an array of degree values from 1 to 10.
	# Then we iterate the 'degrees' one by one and create polynomial values of 'x_train' data called 'x_poly_train'
	# based on the value of the degree
	# Then we fit the polynomial linear regression function using 'x_poly_train' data and 'y_train' data.
	# Then based on the polynomial function, using the 'x_poly_test' data we predict the values of the 'y_test' data
	# Then based on the predicted values and 'y_test" data we calculate the Root Mean Square Error.
	# Applying the last 4 steps for each degree value, we select the degree value which gives the Lowest Root Mean
	# Square Error.
	# Then we fit the polynomial linear regression function again using that degree which gives the Lowest Root Mean
	# Square Error.
	# Based on the polynomial function we get the predicted value of the null value.

	#print(selected_values, selected_index)

	X = np.array([i[0] for i in selected_values]).reshape(len(selected_values), 1)
	y = [i[1] for i in selected_values]
	if pd.isnull(y).all():
		mean_value = 0
	else:
		mean_value = np.nanmean(y)
	y = [mean_value if pd.isna(x) else x for x in y]

	x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=1/3)

	degrees = np.arange(1, 11)
	min_rmse, min_deg = 1e10, 0

	for degree in degrees:
		# Preparing polynomial Train features based on x_train
		poly_features = PolynomialFeatures(degree=degree, include_bias=False)
		x_poly_train = poly_features.fit_transform(x_train)

		# Polynomial linear regression based on train data
		poly_reg = LinearRegression()
		poly_reg.fit(x_poly_train, y_train)

		# Predicting y values and getting root mean squared error based on predicted y values and y_test values
		x_poly_test = poly_features.fit_transform(x_test)
		poly_predict = poly_reg.predict(x_poly_test)
		poly_mse = mean_squared_error(y_test, poly_predict)
		poly_rmse = np.sqrt(poly_mse)

		# Selecting the best degree of the polynomial function based on lowest root mean squared error
		if min_rmse > poly_rmse:
			min_rmse = poly_rmse
			min_deg = degree

	# Fitting the regression function again based on the selected best degree above
	poly_features = PolynomialFeatures(degree=min_deg, include_bias=False)
	x_poly_train = poly_features.fit_transform(x_train)
	poly_reg = LinearRegression()
	poly_reg.fit(x_poly_train, y_train)

	prediction = poly_reg.predict(poly_features.fit_transform([[selected_index]]))[0]
	if prediction < 0:
		prediction = 0

	#return round(prediction, 2)
	return prediction


def mean(selected_values):
	"""
	Function to calculate the mean of the 'selected_values'
	:param selected_values: the values we use to calculate the mean
	:return: the mean
	"""
	# if 'selected_values' is empty return 0
	if pd.isnull(selected_values).all():
		prediction = 0
	# if 'selected_values' is not empty return the mean of it
	else:
		mean_value = np.nanmean(selected_values)
		selected_values = [mean_value if pd.isna(x) else x for x in selected_values]
		prediction = np.mean(np.array(selected_values))

	#return round(prediction, 2)
	return prediction
