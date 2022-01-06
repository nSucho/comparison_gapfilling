"""
Created on January 2021

@author: Niko Suchowitz
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
	# copy the df so we do not change the original
	df_w_nan_copy = data_w_nan.copy()

	# fill the nan with '-100' so fedot can work with it
	df_w_nan_copy = df_w_nan_copy.fillna(-100)

	# TODO: hier einfügen
	# Got univariate time series as numpy array
	time_series = np.array(df_w_nan_copy['TotalLoadValue'])

	# create a pipeline
	#pipeline = get_pipeline()
	pipeline = get_simple_ridge_pipeline()
	model_gapfiller = ModelGapFiller(gap_value=-100.0,
	                                 pipeline=pipeline)

	# Filling in the gaps
	without_gap_forward = model_gapfiller.forward_filling(time_series)
	without_gap_bidirect = model_gapfiller.forward_inverse_filling(time_series)

	#return the filled gaps
	return without_gap_forward, without_gap_bidirect


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


def get_pipeline():
	"""

	:return:
	"""
	node_lagged_1 = PrimaryNode('lagged')
	node_lagged_1.custom_params = {'window_size': 120}
	node_lagged_2 = PrimaryNode('lagged')
	node_lagged_2.custom_params = {'window_size': 2}

	node_first = SecondaryNode('ridge', nodes_from=[node_lagged_1])
	node_second = SecondaryNode('dtreg', nodes_from=[node_lagged_2])
	node_final = SecondaryNode('ridge', nodes_from=[node_first, node_second])
	pipeline = Pipeline(node_final)

	return pipeline
