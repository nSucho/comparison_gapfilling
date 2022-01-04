# Additional imports
import glob
# Additional imports
from gap_creator import create_gaps
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

# Data
from fedot.core.data.data import InputData
from fedot.core.data.data_split import train_test_data_setup
from fedot.core.repository.dataset_types import DataTypesEnum

# Tasks
from fedot.core.repository.tasks import Task, TaskTypesEnum, TsForecastingParams

# Read all the files
# mapcode of country
country_code = 'AT'

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
# combine all df's to one df to train from
df_train = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df8, df9, df10])

# combine all df's to one df to check how accurate
df_test = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df8, df9, df10, df11, df12])


# fill with -100 for fedot, else it can't find gaps
#df_fedot = df_train.fillna(-100) #works
df_fedot = df_test.fillna(-100)

#prepare the dataframe for filling
df_fedot['DateTime'] = pd.to_datetime(df_fedot['DateTime'])
df_fedot.sort_values(by='DateTime', inplace=True)
df_fedot = df_fedot.reset_index(drop=True)

original_series = np.array(df_fedot['TotalLoadValue'])

#save it as csv for debug-reason
df_fedot.to_csv("data/own_data/ActualTotalLoad_edited/test_all.csv", sep='\t', encoding='utf-8', index=False,
                header=["DateTime", "ResolutionCode", "AreaCode",
                        "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

df_fedot.plot('DateTime', 'TotalLoadValue')
plt.savefig('test_AfterReadIn.png')
plt.show()


def versuchsCode():
    """

    :return:
    """

    dfwithgaps = create_gaps(df_fedot)

    missing_data = dfwithgaps['TotalLoadValue'].isna().sum()
    missing_percent = (missing_data/len(dfwithgaps.index))*100
    print('amount of NaN in modified: '+str(missing_data))
    print(round(missing_percent, 2), "Percent is missing Data of "+country_code)

    dfwithgaps = dfwithgaps.fillna(-100.0)
    array_own_gaps = np.array(dfwithgaps['TotalLoadValue'])

    from fedot.utilities.ts_gapfilling import ModelGapFiller

    #pipeline = get_simple_ridge_pipeline()
    pipeline = get_pipeline()
    model_gapfiller = ModelGapFiller(gap_value=-100.0,
                                     pipeline=pipeline)

    # Filling in the gaps
    without_gap_forward = model_gapfiller.forward_filling(array_own_gaps)
    #without_gap_bidirect = model_gapfiller.forward_inverse_filling(array_with_gaps)

    # Todo: benutz ich nur zum prüfen der Genauigkeit
    print(f'Mean absolute error forward: {mean_absolute_error(original_series, without_gap_forward):.3f}')
    #print(f'Mean absolute error bi-direct: {mean_absolute_error(original_series, without_gap_bidirect):.3f}')

def get_pipeline():
    """

    :return:
    """
    node_lagged_1 = PrimaryNode('lagged')
    node_lagged_1.custom_params = {'window_size': 120}
    node_lagged_2 = PrimaryNode('lagged')
    node_lagged_2.custom_params = {'window_size': 10}

    node_first = SecondaryNode('ridge', nodes_from=[node_lagged_1])
    node_second = SecondaryNode('dtreg', nodes_from=[node_lagged_2])
    node_final = SecondaryNode('ridge', nodes_from=[node_first, node_second])
    pipeline = Pipeline(node_final)

    return pipeline


def generate_gaps_in_ts(array_without_gaps, gap_dict, gap_value):
    """
    Function for generating gaps with predefined length in the desired indices
    of an one-dimensional array (time series)

    :param array_without_gaps: an array without gaps
    :param gap_dict: a dictionary with omissions, where the key is the index in
    the time series from which the gap will begin. The key value is the length
    of the gap (elements). -1 in the value means that a skip is generated until
    the end of the array
    :param gap_value: value indicating a gap in the array

    :return: one-dimensional array with omissions
    """

    array_with_gaps = np.copy(array_without_gaps)

    keys = list(gap_dict.keys())
    for key in keys:
        gap_size = gap_dict.get(key)
        if gap_size == -1:
            # Generating a gap to the end of an array
            array_with_gaps[key:] = gap_value
        else:
            array_with_gaps[key:(key + gap_size)] = gap_value

    return array_with_gaps


def get_simple_ridge_pipeline():
    """
    Function for creating pipeline
    :return:
    """
    node_lagged = PrimaryNode('lagged')
    node_lagged.custom_params = {'window_size': 10}

    node_final = SecondaryNode('ridge', nodes_from=[node_lagged])
    pipeline = Pipeline(node_final)

    return pipeline


if __name__ == '__main__':
    versuchsCode()
