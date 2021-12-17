from numpy import *
import math
import matplotlib.pyplot as plt
import glob
import pandas as pd

def versuchsCode():
    """
    Prepare the data, so we can check it easily for gaps
    :return:
    """
    files = glob.glob('data/own_data/ActualTotalLoad_edited/EE/2018_??_ActualTotalLoad_6.1.A_EECTA.csv', recursive=False)
    files.sort()
    for file in files:
        file_df = pd.read_csv(file, sep='\t', encoding='utf-8')


        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        ax = df1.plot(x='date', y='number', label='beginning')
        df2.plot(x='date', y='number', label='ending', ax=ax)

        plt.show()

if __name__ == '__main__':
    versuchsCode()
