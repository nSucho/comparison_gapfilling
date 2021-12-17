"""
Created on December 2021

@author: Niko
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from interpolation_avgweek import averageWeek as avgweek
from interpolation_polyreg import fill_missing_data as polyreg
from interpolation_fedot import fedot_method as fedot_f


def plotTheData(final_df, f_df_name, mapcode, month_no, months, missing_data_perc):
	"""
	plot the data
	:param final_df: dataframe with the data to plot (can have missing values as NaN)
	:param f_df_name: the name of the country to save it more precise as csv
	:param mapcode: map code of the country we plot
	:param month_no: the month we plot
	:param months: list with all months
	:param missing_data_perc: amount of missing-data of 'final_df' in percentage
	:return:
	"""
	# plot the original as axs[0], the avg_week as axs[1], the poly_reg as axs[2] and fedot as axs[3]
	fig, axs = plt.subplots(3, sharex='all')
	fig.suptitle('Total Load Value of '+months[month_no]+' '+mapcode)
	x = final_df['DateTime']
	axs[0].plot(x, final_df['TotalLoadValue'])
	#axs[0].set_xlabel('Date')
	axs[0].set_ylabel('Value')

	# if there are missing values, do an interpolation and plot it as axs[2]
	if missing_data_perc != 0:
		# interpolation with average week; standard
		avg_week = avgweek(final_df)
		# save the filled df as csv
		avg_week.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/avg_week/'+f_df_name+'_filled_avg.csv',
		                sep='\t', encoding='utf-8', index=False,
		                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		                        "MapCode", "TotalLoadValue", "UpdateTime", "Week"])

		# interpolation with polynomial linear regression; master-thesis
		poly_reg = polyreg(final_df, 1)
		# save the filled df as csv
		poly_reg.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/poly_reg/'+f_df_name+'_filled_poly.csv',
		                sep='\t', encoding='utf-8', index=False,
		                header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		                        "MapCode", "TotalLoadValue", "UpdateTime"])

		# interpolation with fedot; machine learning
		# TODO: fedot zum laufen bringen und plotten
		#fedot = fedot_f(final_df)
		# save the filled df as csv
		#fedot.to_csv('data/own_data/ActualTotalLoad_edited/'+mapcode+'/fedot/'+f_df_name+'_filled_fedot.csv',
		#             sep='\t', encoding='utf-8', index=False,
		#             header=["DateTime", "ResolutionCode", "AreaCode", "AreaTypeCode", "AreaName",
		#                     "MapCode", "TotalLoadValue", "UpdateTime"])

		axs[1].plot(x, avg_week['TotalLoadValue'])
		axs[1].set_xlabel('Dates of the month')
		axs[1].set_ylabel('Value')
		axs[2].plot(x, poly_reg['TotalLoadValue'])
		axs[2].set_xlabel('Dates of the month')
		axs[2].set_ylabel('Value')
		# only label the x of axs[2]
		for ax in axs:
			ax.label_outer()
	#else:
	#	inter_meth = final_df
	#	axs[1].plot(x, inter_meth['TotalLoadValue'])
	#	axs[1].set_xlabel('Dates of the month')
	#	axs[1].set_ylabel('Value')
		# only label the x of axs[2]
		for ax in axs:
			ax.label_outer()

	# format the dates
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

	# makes x axis overviewable
	plt.gcf().autofmt_xdate()
	plt.show()


"""
final_df.plot(x='DateTime', y='TotalLoadValue', label='Original Data', title='Total Load Value of '+months[month_no]+' '+mapcode)
avg_week['DateTime'] = pd.to_datetime(avg_week['DateTime'])
poly_reg['DateTime'] = pd.to_datetime(poly_reg['DateTime'])
avg_week.plot(x='DateTime', y='TotalLoadValue', label='Avg Week Data', ax=ax)
poly_reg.plot(x='DateTime', y='TotalLoadValue', label='Poly Reg Data', ax=ax)
plt.show()
"""