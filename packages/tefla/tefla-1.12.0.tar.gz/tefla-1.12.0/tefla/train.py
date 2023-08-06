# -------------------------------------------------------------------#
# Tool to train on images
# Contact: mrinalhaloi11@gmail.com
# Copyright 2018 The Tefla Authors. All Rights Reserved.
# -------------------------------------------------------------------#
from __future__ import division, print_function, absolute_import

import click
import numpy as np

np.random.seed(127)
import tensorflow as tf

tf.set_random_seed(127)

from tefla.core.dir_dataset import DataSet
from tefla.core.iter_ops import create_training_iters
from tefla.core.learning import SupervisedLearner
from tefla.da.standardizer import NoOpStandardizer
from tefla.utils import util

# pylint: disable=no-value-for-parameter


@click.command()
@click.option('--model', default=None, show_default=True, help='Relative path to model.')
@click.option(
    '--training_cnf', default=None, show_default=True, help='Relative path to training config file.')
@click.option('--data_dir', default=None, show_default=True, help='Path to training directory.')
@click.option('--parallel', default=True, show_default=True, help='parallel or queued.')
@click.option(
    '--start_epoch',
    default=1,
    show_default=True,
    help='Epoch number from which to resume training.')
@click.option(
    '--num_classes', default=5, show_default=True, help='Number of classes to use for training.')
@click.option(
    '--gpu_memory_fraction',
    default=0.92,
    show_default=True,
    help='Epoch number from which to resume training.')
@click.option(
    '--weights_from', default=None, show_default=True, help='Path to initial weights file.')
@click.option('--weights_dir', default=None, show_default=True, help='Path to save weights file.')
@click.option('--resume_lr', default=0.01, show_default=True, help='Path to initial weights file.')
@click.option('--loss_type', default='cross_entropy', show_default=True, help='Loss fuction type.')
@click.option('--weighted', default=False, show_default=True, help='Whether to use weighted loss.')
@click.option('--log_file_name', default='train_seg.log', show_default=True, help='Log file name.')
@click.option('--is_summary', default=False, show_default=True, help='Path to initial weights file.')
def main(model, training_cnf, data_dir, parallel, start_epoch, weights_from, weights_dir, resume_lr,
         gpu_memory_fraction, num_classes, is_summary, loss_type, weighted, log_file_name):
  model_def = util.load_module(model)
  model = model_def.model
  cnf = util.load_module(training_cnf).cnf

  if weights_from:
    weights_from = str(weights_from)

  data_set = DataSet(
      data_dir,
      model_def.image_size[0],
      mode=cnf.get('mode'),
      multilabel=cnf.get('multilabel', False))
  standardizer = cnf.get('standardizer', NoOpStandardizer())
  cutout = cnf.get('cutout', None)

  training_iter, validation_iter = create_training_iters(
      cnf,
      data_set,
      standardizer,
      model_def.crop_size,
      start_epoch,
      parallel=parallel,
      cutout=cutout,
      data_balancing=cnf.get('data_balancing', False))
  learner = SupervisedLearner(
      model,
      cnf,
      training_iterator=training_iter,
      validation_iterator=validation_iter,
      resume_lr=resume_lr,
      classification=cnf['classification'],
      gpu_memory_fraction=gpu_memory_fraction,
      num_classes=num_classes,
      is_summary=is_summary,
      loss_type=loss_type,
      weighted=weighted,
      log_file_name=log_file_name)
  learner.fit(
      data_set, weights_from, start_epoch=start_epoch, weights_dir=weights_dir, summary_every=399)


if __name__ == '__main__':
  main()
