"""
Created on January 2021

@author: Niko Suchowitz
"""
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 30, 15


# TODO: schöner/übersichtlicher plotten
#   vielleicht nur stellen die leer waren?
#   vielleicht immer tage zusammenfassen?
def plot_data1(original, avg_week, poly_reg):
	"""

	:param original: the original series without gaps
	:param avg_week: the series after avg_week filling
	:param poly_reg: the series after poly_reg filling
	:param fedot_forward: the series after fedot_forward filling
	:param fedot_bidirect: the series after fedot_bidirect filling
	:return:
	"""
	plt.plot(original, c='blue', alpha=0.2, label='Actual values in the gaps')
	plt.plot(avg_week, c='green', alpha=0.8, label='The avg-Week', linestyle='dotted')
	plt.plot(poly_reg, c='purple', alpha=0.8, label='The Poly-Version', linestyle='dotted')
	#plt.plot(fedot_forward, c='red', alpha=0.8, label='FEDOT forward')
	#plt.plot(fedot_bidirect, c='#D77214', alpha=0.8, label='FEDOT bi-directional')
	plt.ylabel('Total Load', fontsize=14)
	plt.xlabel('Time Index', fontsize=14)
	plt.legend(fontsize=14)
	plt.grid()
	plt.savefig('test_plot1.png')
	plt.show()


def plot_data2(original, df_w_gaps, avg_week, avg_week_mae, poly_reg, poly_reg_mae):
	"""

	:param original: the original df without gaps
	:param avg_week: the df after avg_week filling
	:param poly_reg: the df after poly_reg filling
	:param fedot_forward: the series after fedot_forward filling
	:param fedot_bidirect: the series after fedot_bidirect filling
	:return:
	"""

	fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(30, 15))
	plt.rcParams.update({'xtick.bottom': False})

	# 1. Original
	original['TotalLoadValue'].plot(title='Actual', ax=axes[0], label='Actual', color='red', style="-")
	df_w_gaps['TotalLoadValue'].plot(title='Actual', ax=axes[0], label='Actual', color='green', style="-")
	axes[0].legend(["Missing Data", "Available Data"])

	# 2. avg-week filling
	avg_week['TotalLoadValue'].plot(title='Avg-Week Fill (MAE: '+str(avg_week_mae)+")", ax=axes[1], label='Avg-Week Fill',
	                                style=".")
	df_w_gaps['TotalLoadValue'].plot(title='Actual', ax=axes[1], label='Actual', color='green', style="-")
	# 3. poly_reg filling
	poly_reg['TotalLoadValue'].plot(title="Poly-Reg Fill (MSE: "+str(poly_reg_mae)+")", ax=axes[2], label='Poly-Reg Fill',
	                                color='firebrick', style=".")
	df_w_gaps['TotalLoadValue'].plot(title='Actual', ax=axes[2], label='Actual', color='green', style="-")

	plt.savefig('test_plot2.png')
	plt.show()
