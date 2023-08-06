from __future__ import division, print_function, absolute_import

import functools

from .. import convert
from ..da import iterator
from . import logger


def create_training_iters(cnf,
                          data_set,
                          standardizer,
                          crop_size,
                          epoch,
                          parallel=True,
                          cutout=None,
                          data_balancing=True):
  """Creates training iterator to access and augment the dataset.

  Args:
      cnf: configs dict with all training and augmentation params.
      data_set: an instance of the dataset class.
      standardizer: data samples standardization; either samplewise or aggregate.
      crop_size: training time crop_size of the data samples.
      epoch: the current epoch number; used for data balancing.
      parallel: iterator type; either parallel or queued.
      data_balancing: Bool, whether to use data balancing iterator, doesnt support multilabel
        dataset yet, but supports multiclass datasets.
  """
  if parallel:
    if data_balancing:
      training_iterator_maker = iterator.BalancingDAIterator
    else:
      training_iterator_maker = iterator.ParallelDAIterator
    validation_iterator_maker = iterator.ParallelDAIterator
    logger.info('Using parallel iterators')
  else:
    if data_balancing:
      training_iterator_maker = iterator.BalancingQueuedDAIterator
    else:
      training_iterator_maker = iterator.ParallelDAIterator
    validation_iterator_maker = iterator.ParallelDAIterator
    logger.info('Using queued iterators')

  preprocessor = None

  if data_balancing:
    training_iterator = training_iterator_maker(
        batch_size=cnf['batch_size_train'],
        shuffle=True,
        preprocessor=preprocessor,
        crop_size=crop_size,
        is_training=True,
        aug_params=cnf['aug_params'],
        balance_weights=data_set.balance_weights(),
        final_balance_weights=cnf['final_balance_weights'],
        balance_ratio=cnf['balance_ratio'],
        balance_epoch_count=epoch - 1,
        standardizer=standardizer,
        cutout=cutout,
        fill_mode='constant'
        # save_to_dir=da_training_preview_dir
    )
  else:
    training_iterator = training_iterator_maker(
        batch_size=cnf['batch_size_train'],
        shuffle=True,
        preprocessor=preprocessor,
        crop_size=crop_size,
        is_training=True,
        aug_params=cnf['aug_params'],
        standardizer=standardizer,
        cutout=cutout,
        fill_mode='constant'
        # save_to_dir=da_training_preview_dir
    )

  validation_iterator = validation_iterator_maker(
      batch_size=cnf['batch_size_test'],
      shuffle=False,
      preprocessor=preprocessor,
      crop_size=crop_size,
      is_training=False,
      standardizer=standardizer,
      fill_mode='constant')

  return training_iterator, validation_iterator


def convert_preprocessor(im_size):
  return functools.partial(convert.convert, target_size=im_size)


def create_prediction_iter(cnf, standardizer, crop_size, preprocessor=None, sync=False):
  """Creates prediction iterator to access and augment the dataset.

  Args:
      cnf: configs dict with all training and augmentation params
      standardizer: data samples standardization; either samplewise or aggregate
      crop_size: training time crop_size of the data samples
      preprocessor: data processing or cropping function
      sync: a bool, if False, used parallel iterator
  """
  if sync:
    prediction_iterator_maker = iterator.DAIterator
  else:
    prediction_iterator_maker = iterator.ParallelDAIterator

  prediction_iterator = prediction_iterator_maker(
      batch_size=cnf['batch_size_test'],
      shuffle=False,
      preprocessor=preprocessor,
      crop_size=crop_size,
      is_training=False,
      standardizer=standardizer,
      fill_mode='constant')

  return prediction_iterator
