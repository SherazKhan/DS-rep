import pickle
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

import Gait.Resources.config as c
from Gait.Pipeline.gait_utils import set_filters
from Gait.Pipeline.StepDetection import StepDetection

# params
f = set_filters(exp=2)
algs = ['lhs', 'rhs', 'overlap', 'combined']
with open(join(c.pickle_path, 'sc_alg'), 'rb') as fp:
    sd = pickle.load(fp)
# apdm_metrics = sd.apdm_measures.columns.tolist()
apdm_metrics = ['cadence', 'step_time_asymmetry']
# apdm_metrics = ['cadence', 'step_time_asymmetry', 'stride_time_var_lhs', 'stride_time_var_rhs', 'step_time_var_lhs',
# 'step_time_var_lhs']

# set indices
with open(join(c.pickle_path, 'metadata_sample'), 'rb') as fp:
    sample = pickle.load(fp)
# idx = sample[sample['StepCount'].notnull()].index.tolist()

# 1. Get algorithm gait metrics
# for now start with this
with open(join(c.pickle_path, 'sc_alg'), 'rb') as fp:
    sd = pickle.load(fp)
alg_res = sd.res
alg_res = pd.read_csv(join(c.results_path, 'param_opt', 'gait_measures.csv'), index_col='SampleId')

#for i in range(len(apdm_metrics)):
for i in [0]:
    apdm_vals = sd.apdm_measures[apdm_metrics[i]]
    idx_keep = pd.notnull(apdm_vals)
    apdm_vals = apdm_vals[idx_keep]
    alg_vals = [alg_res[apdm_metrics[i] + '_' + algs[j]][idx_keep] for j in range(len(algs))]

    # Correlation - plot 1
    corr = [pearsonr(apdm_vals, alg_vals[j])[0] for j in range(len(algs))]

    # Plot
    plt.suptitle(apdm_metrics[i], fontsize=12)
    plt.subplot(121)
    y_pos = np.arange(len(corr))
    plt.bar(y_pos, corr, align='center', alpha=0.5)
    plt.xticks(y_pos, algs)
    plt.xlabel('Algorithm')
    plt.ylabel('Pearson correlation (R)')
    plt.title('Algorithm correlation to APDM')

    plt.subplot(122)
    vals = [apdm_vals] + alg_vals
    plt.boxplot(vals)
    y_pos = np.arange(len(vals))
    plt.xticks(y_pos, ['apdm'] + algs)
    plt.xlabel('Algorithm')
    plt.ylabel('Values')
    plt.title('Value distribution')
    plt.show()

