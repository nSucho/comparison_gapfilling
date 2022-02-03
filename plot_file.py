"""
Created on January 2021

@author: Niko Suchowitz
"""
import matplotlib.pyplot as plt
from pylab import rcParams
import pandas as pd
rcParams['figure.figsize'] = 18, 9


def plot_data1(original, avg_week, poly_reg, fedot_forward):
	"""

	:param original: the original series without gaps
	:param avg_week: the series after avg_week filling
	:param poly_reg: the series after poly_reg filling
	:param fedot_forward: the series after fedot_forward filling
	:param fedot_bidirect: the series after fedot_bidirect filling
	:return:
	"""
	"""
	plt.plot(original, c='blue', alpha=0.2, label='Actual values in the gaps')
	plt.plot(avg_week, c='green', alpha=0.8, label='The avg-Week')
	plt.plot(poly_reg, c='purple', alpha=0.8, label='The Poly-Version')
	plt.plot(fedot_forward, c='red', alpha=0.8, label='FEDOT forward')
	#plt.plot(fedot_bidirect, c='#D77214', alpha=0.8, label='FEDOT bi-directional')
	plt.ylabel('Total Load', fontsize=14)
	plt.xlabel('Time Index', fontsize=14)
	plt.legend(fontsize=14)
	plt.grid()
	plt.savefig('test_plot1.png')
	plt.show()
	"""

	plt.plot(original, c='blue', alpha=0.4, label='Actual values in the gaps')
	plt.plot(avg_week, c='green', alpha=0.8, label='Linear interpolation')
	plt.plot(poly_reg, c='purple', alpha=0.8, label='FEDOT one-direction')
	plt.plot(fedot_forward, c='#D77214', alpha=0.8, label='FEDOT bi-directional')
	#plt.plot(masked_array, c='blue', alpha=1.0, linewidth=2)
	plt.ylabel('Total Load', fontsize=14)
	plt.xlabel('Time index', fontsize=14)
	plt.legend(fontsize=14)
	plt.grid()
	plt.savefig('test_plot1.png')
	plt.show()


def plot_data2(original, df_w_gaps, avg_week, poly_reg, fedot_forward, fedot_bidirect):
	"""

	:param original: the original df without gaps
	:param df_w_gaps: original with induced gaps
	:param avg_week: the df after avg_week filling
	:param poly_reg: the df after poly_reg filling
	:param fedot_forward: the series after fedot_forward filling
	:param fedot_bidirect: the series after fedot_bidirect filling
	:return:
	"""

	fig, axes = plt.subplots(5, 1, sharex=True, sharey=True, figsize=(25, 20))
	plt.rcParams.update({'xtick.bottom': False})

	# 1. Original
	original['TotalLoadValue'].plot(title='Actual', ax=axes[0], label='Actual', color='red', style="-")
	df_w_gaps['TotalLoadValue'].plot(title='Actual', ax=axes[0], label='Actual', color='green', style="-")
	axes[0].legend(["Missing Data", "Available Data"])

	# 2. avg-week filling
	avg_week['TotalLoadValue'].plot(title='Avg-Week Fill', ax=axes[1], label='Avg-Week Fill',
	                                style="-")
	#df_w_gaps['TotalLoadValue'].plot(title='Avg-Week Fill', ax=axes[1], label='Actual', color='green', style="-")
	original['TotalLoadValue'].plot(title='Avg-Week Fill', ax=axes[1], label='Actual', color='green', style="-")
	axes[1].legend(["Avg-Week Fill", "Actual"])

	# 3. poly_reg filling
	poly_reg['TotalLoadValue'].plot(title="Poly-Reg Fill", ax=axes[2], label='Poly-Reg Fill',
	                                color='firebrick', style="-")
	#df_w_gaps['TotalLoadValue'].plot(title='Poly-Reg Fill', ax=axes[2], label='Actual', color='green', style="-")
	original['TotalLoadValue'].plot(title='Poly-Reg Fill', ax=axes[2], label='Actual', color='green', style="-")
	axes[2].legend(["Poly-Reg Fill", "Actual"])

	# 4. fedot forward filling
	fedot_df = pd.DataFrame(fedot_forward)
	fedot_df.plot(title="FEDOT Forward Fill", ax=axes[3],
	              label='FEDOT Forward Fill', color='firebrick', style="-")
	#df_w_gaps['TotalLoadValue'].plot(title='FEDOT', ax=axes[3], label='Actual', color='green', style="-")
	original['TotalLoadValue'].plot(title='FEDOT Forward', ax=axes[3], label='Actual', color='green', style="-")
	axes[3].legend(["Fedot Forward Fill", "Actual"])

	# 4. fedot bidirecional filling
	fedot_inv_df = pd.DataFrame(fedot_bidirect)
	fedot_inv_df.plot(title="FEDOT Bidirectional Fill", ax=axes[4],
	                  label='FEDOT Bidirectional Fill', color='firebrick', style="-")
	#df_w_gaps['TotalLoadValue'].plot(title='FEDOT', ax=axes[3], label='Actual', color='green', style="-")
	original['TotalLoadValue'].plot(title='FEDOT Bidirectional', ax=axes[4], label='Actual', color='green', style="-")
	axes[4].legend(["Fedot Bidirectional Fill", "Actual"])

	plt.savefig('test_plot2.png')
	plt.show()
