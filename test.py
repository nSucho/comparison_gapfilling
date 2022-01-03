# Additional imports
import glob
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
# Imports for creating plots
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 18, 7
# Pipeline and nodes
from fedot.core.pipelines.pipeline import Pipeline
from fedot.core.pipelines.node import PrimaryNode, SecondaryNode
from fedot.utilities.ts_gapfilling import ModelGapFiller


# Read all the files
# mapcode of country
country_code = 'EE'
"""
# read in all the monthly csv-files
files = glob.glob('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_??_ActualTotalLoad_6.1.A_'
                  +country_code+'CTA.csv', recursive=False)
files.sort()
# concat to one dataframe and reset index
df_total = pd.concat([pd.read_csv(file, sep='\t', encoding='utf-8') for file in files])
df_total = df_total.reset_index(drop=True)
"""

# readin all df's for debug reasons
df1 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_01_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df2 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_02_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df3 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_03_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df4 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_04_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df5 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_05_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df6 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_06_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df7 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_07_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df8 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_08_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df9 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_09_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df10 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_10_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df11 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_11_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
df12 = pd.read_csv('data/own_data/ActualTotalLoad_edited/'+country_code+'/2018_12_ActualTotalLoad_6.1.A_'
                       + country_code+'CTA.csv', sep='\t', encoding='utf-8')
# combine all df's to one df
df_total = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df8, df9, df10, df11, df12])

# fill with -100 for fedot, else it can't find gaps
df_fedot = df_total.fillna(-100)

#prepare the dataframe for filling
df_fedot['DateTime'] = pd.to_datetime(df_fedot['DateTime'])
df_fedot.sort_values(by='DateTime', inplace=True)
df_total = df_total.reset_index(drop=True)

#save it as csv for debug-reason
df_fedot.to_csv("data/own_data/ActualTotalLoad_edited/test_all.csv", sep='\t', encoding='utf-8', index=False,
                header=["DateTime", "ResolutionCode", "AreaCode",
                        "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

#df_fedot.plot('DateTime', 'TotalLoadValue')
#plt.savefig('raw_data.png')
#plt.show()


def versuchsCode():
    """

    :return:
    """

    # Got univariate time series as numpy array
    time_series = np.array(df_fedot['TotalLoadValue'])
    pipeline = get_simple_ridge_pipeline()
    model_gapfiller = ModelGapFiller(gap_value=-100.0, pipeline=pipeline)

    # Filling in the gaps
    without_gap_forward = model_gapfiller.forward_filling(time_series)
    without_gap_bidirect = model_gapfiller.forward_inverse_filling(time_series)

    #print(f'Mean absolute error forward: {mean_absolute_error(time_series, without_gap_forward):.3f}')
    print(f'Mean absolute error bidirect: {mean_absolute_error(time_series, without_gap_bidirect):.3f}')

    plt.plot(time_series, c='blue', alpha=0.4, label='Actual values in the gaps')
    plt.plot(without_gap_forward, c='purple', alpha=0.8, label='FEDOT one-direction')
    plt.plot(without_gap_bidirect, c='#D77214', alpha=0.8, label='FEDOT bi-directional')
    plt.ylabel('TotalLoad', fontsize=14)
    plt.xlabel('DateTime', fontsize=14)
    plt.legend(fontsize=14)
    plt.grid()
    plt.show()

# Let's prepare a function for visualizing forecasts
def get_simple_ridge_pipeline():
    """
    asd
    :return:
    """
    node_lagged = PrimaryNode('lagged')
    node_lagged.custom_params = {'window_size': 14}

    node_final = SecondaryNode('ridge', nodes_from=[node_lagged])
    pipeline = Pipeline(node_final)

    return pipeline


if __name__ == '__main__':
    versuchsCode()
