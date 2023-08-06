from __future__ import division, print_function, absolute_import

import numpy as np
import tensorflow as tf
from tefla.core.lr_policy import PolyDecayPolicy, StepDecayPolicy
from tefla.da.standardizer import SamplewiseStandardizer
from tefla.da.standardizer import AggregateStandardizer
from tefla.utils import util
from tefla.da.cutout import Cutout
from tefla.core import metrics

kappav2 = metrics.KappaV2(num_classes=5, batch_size=16)
cnf = {
    'name': __name__.split('.')[-1],
    'batch_size_train': 32,
    'batch_size_test': 32,
    'balance_ratio': 0.975,
    'image_size': (256, 256),
    'crop_size': (224, 224),
    'tfrecords_im_size': (128, 128, 3),
     # 'input_size': (112, 112, 3),
    #'input_size': (112, 112, 3),
    'input_size': (448, 448, 3),
    'num_gpus': 2,
    'init_probs': [0.9999, 0.0696, 0.1507, 0.0248, 0.0201],
    'TOWER_NAME': 'tower',
    'standardizer': SamplewiseStandardizer(clip=6),
    # 'balance_weights' via data_set
    'final_balance_weights': np.array([1, 5, 5, 5, 5], dtype=float),
    'l2_reg': 0.0005,
    'optname': 'momentum',
    'opt_kwargs': {'decay': 0.9},
    'summary_dir': '/home/data/eyepacs/summary/512_bn',
    'cutout': Cutout(5, 15),
    'aug_params': {
        'zoom_range': (1 / 1.15, 1.15),
        'rotation_range': (0, 360),
        'shear_range': (0, 0),
        'translation_range': (-40, 40),
        'do_flip': True,
        'allow_stretch': True,
    },
    'num_epochs': 2,
    'lr_policy': PolyDecayPolicy(0.00005),
    # 'lr_policy': StepDecayPolicy({0: 0.0002, 100: 0.0002, 200: 0.0002, 400: 0.0002, 500: 0.0001}),
    'classification': True,
    'validation_scores': [('validation accuracy', tf.contrib.metrics.accuracy), ('validation kappa', kappav2.metric)],
}
