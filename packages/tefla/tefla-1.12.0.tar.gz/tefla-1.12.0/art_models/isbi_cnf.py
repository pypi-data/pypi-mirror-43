from __future__ import division, print_function, absolute_import

import numpy as np
from tefla.core.lr_policy import StepDecayPolicy, PolyDecayPolicy
from tefla.da.standardizer import AggregateStandardizer
from tefla.utils import util
from tefla.da.standardizer import SamplewiseStandardizer

cnf = {
    'name': __name__.split('.')[-1],
    'batch_size_train': 24,
    'batch_size_test': 24,
    'balance_ratio': 0.975,
    # 'balance_weights' via data_set
    'final_balance_weights': np.array([1, 10], dtype=float),
    'l2_reg': 0.0005,
    'summary_dir': '/home/lalit/data/eyepacs-dr/35k/summary/512_bn',
    'aug_params': {
        'zoom_range': (1 / 1.15, 1.15),
        'rotation_range': (0, 360),
        'shear_range': (0, 0),
        'translation_range': (-40, 40),
        'do_flip': True,
        'allow_stretch': True,
    },
    'standardizer': SamplewiseStandardizer(clip=6),
    'num_epochs': 451,
    'lr_policy': PolyDecayPolicy(0.01),
    #'lr_policy': StepDecayPolicy({0:0.01, 60: 0.001, 150: 0.0001}),
    'classification': True,
    'validation_scores': [('validation accuracy', util.accuracy_wrapper), ('validation kappa', util.kappa_wrapper)],
    # 'validation_scores': [('validation kappa', util.kappa_wrapper)],
}
