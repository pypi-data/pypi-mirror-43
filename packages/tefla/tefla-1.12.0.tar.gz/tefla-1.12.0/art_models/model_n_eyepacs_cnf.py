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
    'batch_size_train': 16,
    'batch_size_test': 16,
    'balance_ratio': 0.975,
    'image_size': (256, 256),
    'crop_size': (224, 224),
    'tfrecords_im_size': (128, 128, 3),
     # 'input_size': (112, 112, 3),
    # 'input_size': (224, 224, 3),
    'input_size': (448, 448, 3),
    'num_gpus': 1,
    'init_probs': [0.9999, 0.0696, 0.1507, 0.0248, 0.0201],
    'TOWER_NAME': 'tower',
    # 'standardizer': SamplewiseStandardizer(clip=6),
    'standardizer': AggregateStandardizer(
        mean=np.array([108.64628601, 75.86886597, 54.34005737], dtype=np.float32),
        std=np.array([70.53946096, 51.71475228, 43.03428563], dtype=np.float32),
        u=np.array([[-0.56543481, 0.71983482, 0.40240142],
                    [-0.5989477, -0.02304967, -0.80036049],
                    [-0.56694071, -0.6935729, 0.44423429]], dtype=np.float32),
        ev=np.array([1.65513492, 0.48450358, 0.1565086], dtype=np.float32),
        sigma=0.5
    ),
    # 'balance_weights' via data_set
    'final_balance_weights': np.array([1, 2, 2, 2, 2], dtype=float),
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
    'num_epochs': 451,
    'lr_policy': PolyDecayPolicy(0.00005),
    # 'lr_policy': StepDecayPolicy({0: 0.0002, 100: 0.0002, 200: 0.0002, 400: 0.0002, 500: 0.0001}),
    'classification': True,
    'validation_scores': [('validation accuracy', tf.contrib.metrics.accuracy), ('validation kappa', kappav2.metric)],
}
