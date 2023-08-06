from __future__ import division, print_function, absolute_import

import numpy as np
from tefla.core.lr_policy import StepDecayPolicy, PolyDecayPolicy
from tefla.da.standardizer import AggregateStandardizer
from tefla.utils import util
from tefla.da.standardizer import SamplewiseStandardizer

cnf = {
    'name': __name__.split('.')[-1],
    'batch_size_train': 32,
    'batch_size_test': 32,
    'balance_ratio': 0.975,
    # 'balance_weights' via data_set
    'final_balance_weights': np.array([1, 5, 3, 3, 3], dtype=float),
    # 'final_balance_weights': np.array([1, 2, 2, 2, 2], dtype=float),
    # 'final_balance_weights': np.array([1, 5, 2, 10, 10], dtype=float),
    'l2_reg': 0.0005,
    'optname': 'momentum',
    'summary_dir': '/home/lalit/data/eyepacs-dr/35k/summary/512_bn',
    'aug_params': {
        'zoom_range': (1 / 1.15, 1.15),
        'rotation_range': (0, 360),
        'shear_range': (0, 0),
        'translation_range': (-40, 40),
        'do_flip': True,
        'allow_stretch': True,
    },
    'standardizer': AggregateStandardizer(
        mean=np.array([108.64628601, 75.86886597, 54.34005737], dtype=np.float32),
        std=np.array([70.53946096, 51.71475228, 43.03428563], dtype=np.float32),
        u=np.array([[-0.56543481, 0.71983482, 0.40240142],
                    [-0.5989477, -0.02304967, -0.80036049],
                    [-0.56694071, -0.6935729, 0.44423429]], dtype=np.float32),
        ev=np.array([1.65513492, 0.48450358, 0.1565086], dtype=np.float32),
        sigma=0.5
    ),
    'num_epochs': 551,
    'lr_policy': PolyDecayPolicy(0.01),
    'classification': True,
    #'lr_policy': StepDecayPolicy(
    #    schedule={
    #        0: 0.01,
    #        30: 0.001,
    #        90: 0.0003,
    #        110: 0.003,
    #        120: 0.0003,
    #        200: 0.00003,
    #    }
    #),
    'validation_scores': [('validation accuracy', util.accuracy_wrapper), ('validation kappa', util.kappa_wrapper)],
    # 'validation_scores': [('validation kappa', util.kappa_wrapper)],
}
