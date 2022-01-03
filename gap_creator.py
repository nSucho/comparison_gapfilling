"""
Created on January 2022

@author: Niko
"""
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import glob
np.random.seed(12)

def create_gaps(data_without_gaps):
	for col in data_without_gaps.columns:
		if col == 'TotalLoadValue':
			data_without_gaps.loc[data_without_gaps.sample(frac=0.2).index, col] = np.nan

	df_w_gaps = data_without_gaps

	return df_w_gaps


if __name__ == '__main__':
	country_code = 'AT'

	# read in all the monthly csv-files
	files = glob.glob('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_??_ActualTotalLoad_6.1.A_'
	                  +country_code+'CTA.csv', recursive=False)
	files.sort()
	# concat to one dataframe and reset index
	df_total = pd.concat([pd.read_csv(file, sep='\t', encoding='utf-8') for file in files])
	df_total = df_total.reset_index(drop=True)
	create_gaps(df_total)