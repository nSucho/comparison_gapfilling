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

df_test = pd.read_csv('data/own_data/modified_2018.csv', sep='\t', encoding='utf-8')

df_original = pd.read_csv('data/own_data/original_2018.csv', sep='\t', encoding='utf-8')
original_series = np.array(df_original['TotalLoadValue'])

#save it as csv for debug-reason
df_test.to_csv("data/own_data/ActualTotalLoad_edited/test_all.csv", sep='\t', encoding='utf-8', index=False,
                header=["DateTime", "ResolutionCode", "AreaCode",
                        "AreaTypeCode", "AreaName", "MapCode", "TotalLoadValue", "UpdateTime"])

df_test.plot('DateTime', 'TotalLoadValue')
plt.savefig('test_AfterReadIn.png')
plt.show()


def versuchsCode():
    """

    :return:
    """

    dfwithgaps = create_gaps(df_original)

    missing_data = dfwithgaps['TotalLoadValue'].isna().sum()
    missing_percent = (missing_data/len(dfwithgaps.index))*100
    print('amount of NaN in modified: '+str(missing_data))
    print(round(missing_percent, 2), "Percent is missing Data")

    # fill with -100 for fedot, else it can't find gaps
    df_fedot = dfwithgaps.fillna(-100)
    df_fedot['DateTime'] = pd.to_datetime(df_fedot['DateTime'])
    df_fedot.sort_values(by='DateTime', inplace=True)
    df_fedot = df_fedot.reset_index(drop=True)

    # np array erstellen
    array_own_gaps = np.array(df_fedot['TotalLoadValue'])
    arr_with_gaps = np.array([2, 4, 2, 3, 5, 6, -100, 4, 5, -100, 8, 7, -100,
                              9, 15, 10, 11, -100, -100, 50, -100, -100])

    from fedot.utilities.ts_gapfilling import ModelGapFiller

    pipeline = get_simple_ridge_pipeline()
    model_gapfiller = ModelGapFiller(gap_value=-100.0,
                                     pipeline=pipeline)

    # Filling in the gaps
    without_gap_forward = model_gapfiller.forward_filling(array_own_gaps)
    without_gap_bidirect = model_gapfiller.forward_inverse_filling(array_own_gaps)

    print(f'Mean absolute error forward: {mean_absolute_error(original_series, without_gap_forward):.3f}')
    print(f'Mean absolute error bi-direct: {mean_absolute_error(original_series, without_gap_bidirect):.3f}')


def get_simple_ridge_pipeline():
    """
    Function for creating pipeline
    :return:
    """
    node_lagged = PrimaryNode('lagged')
    node_lagged.custom_params = {'window_size': 150}

    node_final = SecondaryNode('ridge', nodes_from=[node_lagged])
    pipeline = Pipeline(node_final)

    return pipeline


if __name__ == '__main__':
    versuchsCode()
