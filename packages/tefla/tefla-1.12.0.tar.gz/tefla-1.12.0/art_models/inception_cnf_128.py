from __future__ import division, print_function, absolute_import

import tensorflow as tf
import numpy as np
from tefla.core.lr_policy import StepDecayPolicy, PolyDecayPolicy
from tefla.utils import util
from tefla.da.standardizer import SamplewiseStandardizer
from tefla.core import metrics

kappav2 = metrics.KappaV2(num_classes=4, batch_size=32)

cnf = {
    'name': __name__.split('.')[-1],
    'batch_size_train': 32,
    'batch_size_test': 32,
    'balance_ratio': 0.975,
    # 'input_size': (224, 224, 3),
    'input_size': (112, 112, 3),
    # 'balance_weights' via data_set
    'final_balance_weights': np.array([1, 1, 2, 3], dtype=float),
    # 'final_balance_weights': np.array([1, 2, 2, 2, 2], dtype=float),
    # 'final_balance_weights': np.array([1, 5, 2, 10, 10], dtype=float),
    'l2_reg': 0.0005,
    'num_gpus': 1,
    'optname': 'momentum',
    'summary_dir': '/home/ubuntu/data/eyepacs-dr/35k/summary/512_bn',
    'aug_params': {
        'zoom_range': (1 / 1.15, 1.15),
        'rotation_range': (0, 360),
        'shear_range': (0, 0),
        'translation_range': (-40, 40),
        'do_flip': True,
        'allow_stretch': True,
    },
    'standardizer': SamplewiseStandardizer(clip=6),
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
    # 'validation_scores': [('validation accuracy', util.accuracy_wrapper), ('validation kappa', util.kappa_wrapper)],
    # 'validation_scores': [('validation kappa', util.kappa_wrapper)],
    'validation_scores': [('validation accuracy', tf.contrib.metrics.accuracy), ('validation kappa', kappav2.metric)],
}
