"""
Created on January 2021

@author: Niko
"""

# Todo: gap value ist anscheinend -100 oder so
import numpy as np
# Pipeline and nodes
from fedot.core.pipelines.pipeline import Pipeline
from fedot.core.pipelines.node import PrimaryNode, SecondaryNode
from fedot.utilities.ts_gapfilling import ModelGapFiller


def fedot_method(data_w_nan):
	"""
	The third method, the autoML solution fedot
	:param data_w_nan: the data with gaps (NaN) to fill
	:return: the data with filled gaps (NaN)
	"""
	df_w_nan_copy = data_w_nan.copy()
	# fill the nan with '-100' so fedot can work with it
	df_w_nan_copy = df_w_nan_copy.fillna(-100)

	# TODO: hier einfügen
	# Got univariate time series as numpy array
	time_series = np.array(df_w_nan_copy['TotalLoadValue'])

	from fedot.utilities.ts_gapfilling import ModelGapFiller

	pipeline = get_simple_ridge_pipeline()
	model_gapfiller = ModelGapFiller(gap_value=-100.0,
	                                 pipeline=pipeline)

	# Filling in the gaps
	without_gap_forward = model_gapfiller.forward_filling(time_series)

	return without_gap_forward


def get_simple_ridge_pipeline():
	"""
    Function for creating pipeline
    :return:
    """
	node_lagged = PrimaryNode('lagged')
	node_lagged.custom_params = {'window_size': 50}

	node_final = SecondaryNode('ridge', nodes_from=[node_lagged])
	pipeline = Pipeline(node_final)

	return pipeline
