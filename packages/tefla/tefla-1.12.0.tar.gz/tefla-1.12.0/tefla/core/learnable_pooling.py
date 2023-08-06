from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import six
import math
import tensorflow as tf
from collections import namedtuple

from .layers import batch_norm_tf as batch_norm

NamedOutputs = namedtuple('NamedOutputs', ['name', 'outputs'])


@six.add_metaclass(abc.ABCMeta)
class PoolingBaseModel(object):
  """Inherit from this class when implementing new models.

  Reference:
      Learnable pooling method with Context Gating for video classification
      Antoine Miech, Ivan Laptev, Josef Sivic
  credit: modified version of original implementation https://github.com/antoine77340/LOUPE
  """

  def __init__(self,
               feature_size,
               max_samples,
               cluster_size,
               output_dim,
               gating=True,
               add_batch_norm=True,
               is_training=True,
               name='LearnablePooling',
               outputs_collections=None):
    """Initialize a NetVLAD block.

    Args:
        feature_size: Dimensionality of the input features.
        max_samples: The maximum number of samples to pool.
        cluster_size: The number of clusters.
        output_dim: size of the output space after dimension reduction.
        add_batch_norm: (bool) if True, adds batch normalization.
        is_training: (bool) Whether or not the graph is training.
        gating: (bool) Whether or not to use gating operation
        name: a string, name of the layer
        outputs_collections: The collections to which the outputs are added.
    """

    self.feature_size = feature_size
    self.max_samples = max_samples
    self.output_dim = output_dim
    self.is_training = is_training
    self.gating = gating
    self.add_batch_norm = add_batch_norm
    self.cluster_size = cluster_size
    self.name = name
    self.outputs_collections = outputs_collections

  @abc.abstractmethod
  def forward(self, reshaped_input):
    raise NotImplementedError("Models should implement the forward pass.")

  def context_gating(self, input_layer):
    """Context Gating.

    Args:
        input_layer: Input layer in the following shape:
        'batch_size' x 'number_of_activation'

    Returns:
        activation: gated layer in the following shape:
        'batch_size' x 'number_of_activation'
    """

    input_dim = input_layer.get_shape().as_list()[1]

    gating_weights = tf.get_variable(
        "gating_weights", [input_dim, input_dim],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(input_dim)))

    gates = tf.matmul(input_layer, gating_weights)

    if self.add_batch_norm:
      gates = batch_norm(
          gates, center=True, scale=True, is_training=self.is_training, scope="gating_bn")
    else:
      gating_biases = tf.get_variable(
          "gating_biases", [input_dim],
          initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(input_dim)))
      gates += gating_biases

    gates = tf.sigmoid(gates)

    activation = tf.multiply(input_layer, gates)

    return _collect_named_outputs(self.outputs_collections, self.name, activation)


class NetVLAD(PoolingBaseModel):
  """Creates a NetVLAD class."""

  def __init__(self, feature_size, max_samples, cluster_size, output_dim, **kwargs):
    """Initialize a NetVLAD block.

    Args:
        feature_size: Dimensionality of the input features.
        max_samples: The maximum number of samples to pool.
        cluster_size: The number of clusters.
        output_dim: size of the output space after dimension reduction.
        add_batch_norm: (bool) if True, adds batch normalization.
        is_training: (bool) Whether or not the graph is training.
        gating: (bool) Whether or not to use gating operation
        name: a string, name of the layer
        outputs_collections: The collections to which the outputs are added.
    """
    super(NetVLAD, self).__init__(feature_size, max_samples, cluster_size, output_dim, **kwargs)

  def forward(self, reshaped_input):
    """Forward pass of a NetVLAD block.

    Args:
        reshaped_input: The input in reshaped in the following form:
        'batch_size' x 'max_samples' x 'feature_size'.

    Returns:
        vlad: the pooled vector of size: 'batch_size' x 'output_dim'
    """

    cluster_weights = tf.get_variable(
        "cluster_weights", [self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    activation = tf.matmul(reshaped_input, cluster_weights)

    if self.add_batch_norm:
      activation = batch_norm(
          activation, center=True, scale=True, is_training=self.is_training, scope="cluster_bn")
    else:
      cluster_biases = tf.get_variable(
          "cluster_biases", [cluster_size],
          initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))
      activation += cluster_biases

    activation = tf.nn.softmax(activation)

    activation = tf.reshape(activation, [-1, self.max_samples, self.cluster_size])

    a_sum = tf.reduce_sum(activation, -2, keep_dims=True)

    cluster_weights2 = tf.get_variable(
        "cluster_weights2", [1, self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    a = tf.multiply(a_sum, cluster_weights2)

    activation = tf.transpose(activation, perm=[0, 2, 1])

    reshaped_input = tf.reshape(reshaped_input, [-1, self.max_samples, self.feature_size])

    vlad = tf.matmul(activation, reshaped_input)
    vlad = tf.transpose(vlad, perm=[0, 2, 1])
    vlad = tf.subtract(vlad, a)

    vlad = tf.nn.l2_normalize(vlad, 1)

    vlad = tf.reshape(vlad, [-1, self.cluster_size * self.feature_size])
    vlad = tf.nn.l2_normalize(vlad, 1)

    hidden1_weights = tf.get_variable(
        "hidden1_weights", [self.cluster_size * self.feature_size, self.output_dim],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.cluster_size)))

    vlad = tf.matmul(vlad, hidden1_weights)

    if self.gating:
      vlad = super(NetVLAD, self).context_gating(vlad)

    return vlad


class NetRVLAD(PoolingBaseModel):
  """Creates a NetRVLAD class (Residual-less NetVLAD)."""

  def __init__(self, feature_size, max_samples, cluster_size, output_dim, **kwargs):
    """Initialize a NetVLAD block.

    Args:
        feature_size: Dimensionality of the input features.
        max_samples: The maximum number of samples to pool.
        cluster_size: The number of clusters.
        output_dim: size of the output space after dimension reduction.
        add_batch_norm: (bool) if True, adds batch normalization.
        is_training: (bool) Whether or not the graph is training.
        gating: (bool) Whether or not to use gating operation
        name: a string, name of the layer
        outputs_collections: The collections to which the outputs are added.
    """
    super(NetRVLAD, self).__init__(feature_size, max_samples, cluster_size, output_dim, **kwargs)

  def forward(self, reshaped_input):
    """Forward pass of a NetRVLAD block.

    Args:
        reshaped_input: The input in reshaped in the following form:
        'batch_size' x 'max_samples' x 'feature_size'.

    Returns:
        vlad: the pooled vector of size: 'batch_size' x 'output_dim'
    """

    cluster_weights = tf.get_variable(
        "cluster_weights", [self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    activation = tf.matmul(reshaped_input, cluster_weights)

    if self.add_batch_norm:
      activation = batch_norm(
          activation, center=True, scale=True, is_training=self.is_training, scope="cluster_bn")
    else:
      cluster_biases = tf.get_variable(
          "cluster_biases", [cluster_size],
          initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))
      tf.summary.histogram("cluster_biases", cluster_biases)
      activation += cluster_biases

    activation = tf.nn.softmax(activation)

    activation = tf.reshape(activation, [-1, self.max_samples, self.cluster_size])

    activation = tf.transpose(activation, perm=[0, 2, 1])

    reshaped_input = tf.reshape(reshaped_input, [-1, self.max_samples, self.feature_size])
    vlad = tf.matmul(activation, reshaped_input)

    vlad = tf.transpose(vlad, perm=[0, 2, 1])
    vlad = tf.nn.l2_normalize(vlad, 1)

    vlad = tf.reshape(vlad, [-1, self.cluster_size * self.feature_size])
    vlad = tf.nn.l2_normalize(vlad, 1)

    hidden1_weights = tf.get_variable(
        "hidden1_weights", [self.cluster_size * self.feature_size, self.output_dim],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.cluster_size)))

    vlad = tf.matmul(vlad, hidden1_weights)

    if self.gating:
      vlad = super(NetRVLAD, self).context_gating(vlad)

    return vlad


class SoftDBoW(PoolingBaseModel):
  """Creates a Soft Deep Bag-of-Features class."""

  def __init__(self, feature_size, max_samples, cluster_size, output_dim, **kwargs):
    """Initialize a NetVLAD block.

    Args:
        feature_size: Dimensionality of the input features.
        max_samples: The maximum number of samples to pool.
        cluster_size: The number of clusters.
        output_dim: size of the output space after dimension reduction.
        add_batch_norm: (bool) if True, adds batch normalization.
        is_training: (bool) Whether or not the graph is training.
        gating: (bool) Whether or not to use gating operation
        name: a string, name of the layer
        outputs_collections: The collections to which the outputs are added.
    """
    super(SoftDBoW, self).__init__(feature_size, max_samples, cluster_size, output_dim, **kwargs)

  def forward(self, reshaped_input):
    """Forward pass of a Soft-DBoW block.

    Args:
        reshaped_input: The input in reshaped in the following form:
        'batch_size' x 'max_samples' x 'feature_size'.

    Returns:
        bof: the pooled vector of size: 'batch_size' x 'output_dim'
    """

    cluster_weights = tf.get_variable(
        "cluster_weights", [self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    activation = tf.matmul(reshaped_input, cluster_weights)

    if self.add_batch_norm:
      activation = batch_norm(
          activation, center=True, scale=True, is_training=self.is_training, scope="cluster_bn")
    else:
      cluster_biases = tf.get_variable(
          "cluster_biases", [self.cluster_size],
          initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))
      activation += cluster_biases

    activation = tf.nn.softmax(activation)

    activation = tf.reshape(activation, [-1, self.max_samples, self.cluster_size])

    bof = tf.reduce_sum(activation, 1)
    bof = tf.nn.l2_normalize(bof, 1)

    hidden1_weights = tf.get_variable(
        "hidden1_weights", [self.cluster_size, self.output_dim],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.cluster_size)))

    bof = tf.matmul(bof, hidden1_weights)

    if self.gating:
      bof = super(SoftDBoW, self).context_gating(bof)

    return bof


class NetFV(PoolingBaseModel):
  """Creates a NetFV class."""

  def __init__(self, feature_size, max_samples, cluster_size, output_dim, **kwargs):
    """Initialize a NetVLAD block.

    Args:
        feature_size: Dimensionality of the input features.
        max_samples: The maximum number of samples to pool.
        cluster_size: The number of clusters.
        output_dim: size of the output space after dimension reduction.
        add_batch_norm: (bool) if True, adds batch normalization.
        is_training: (bool) Whether or not the graph is training.
        gating: (bool) Whether or not to use gating operation
        name: a string, name of the layer
        outputs_collections: The collections to which the outputs are added.
    """
    super(NetFV, self).__init__(feature_size, max_samples, cluster_size, output_dim, **kwargs)

  def forward(self, reshaped_input):
    """Forward pass of a NetFV block.

    Args:
        reshaped_input: The input in reshaped in the following form:
        'batch_size' x 'max_samples' x 'feature_size'.

    Returns:
        fv: the pooled vector of size: 'batch_size' x 'output_dim'
    """

    cluster_weights = tf.get_variable(
        "cluster_weights", [self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    covar_weights = tf.get_variable(
        "covar_weights", [self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(mean=1.0, stddev=1 / math.sqrt(self.feature_size)))

    covar_weights = tf.square(covar_weights)
    eps = tf.constant([1e-6])
    covar_weights = tf.add(covar_weights, eps)

    activation = tf.matmul(reshaped_input, cluster_weights)
    if self.add_batch_norm:
      activation = batch_norm(
          activation, center=True, scale=True, is_training=self.is_training, scope="cluster_bn")
    else:
      cluster_biases = tf.get_variable(
          "cluster_biases", [self.cluster_size],
          initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))
      activation += cluster_biases

    activation = tf.nn.softmax(activation)

    activation = tf.reshape(activation, [-1, self.max_samples, self.cluster_size])

    a_sum = tf.reduce_sum(activation, -2, keep_dims=True)

    cluster_weights2 = tf.get_variable(
        "cluster_weights2", [1, self.feature_size, self.cluster_size],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.feature_size)))

    a = tf.multiply(a_sum, cluster_weights2)

    activation = tf.transpose(activation, perm=[0, 2, 1])

    reshaped_input = tf.reshape(reshaped_input, [-1, self.max_samples, self.feature_size])
    fv1 = tf.matmul(activation, reshaped_input)

    fv1 = tf.transpose(fv1, perm=[0, 2, 1])

    # computing second order FV
    a2 = tf.multiply(a_sum, tf.square(cluster_weights2))

    b2 = tf.multiply(fv1, cluster_weights2)
    fv2 = tf.matmul(activation, tf.square(reshaped_input))

    fv2 = tf.transpose(fv2, perm=[0, 2, 1])
    fv2 = tf.add_n([a2, fv2, tf.scalar_mul(-2, b2)])

    fv2 = tf.divide(fv2, tf.square(covar_weights))
    fv2 = tf.subtract(fv2, a_sum)

    fv2 = tf.reshape(fv2, [-1, self.cluster_size * self.feature_size])

    fv2 = tf.nn.l2_normalize(fv2, 1)
    fv2 = tf.reshape(fv2, [-1, self.cluster_size * self.feature_size])
    fv2 = tf.nn.l2_normalize(fv2, 1)

    fv1 = tf.subtract(fv1, a)
    fv1 = tf.divide(fv1, covar_weights)

    fv1 = tf.nn.l2_normalize(fv1, 1)
    fv1 = tf.reshape(fv1, [-1, self.cluster_size * self.feature_size])
    fv1 = tf.nn.l2_normalize(fv1, 1)

    fv = tf.concat([fv1, fv2], 1)

    hidden1_weights = tf.get_variable(
        "hidden1_weights", [2 * self.cluster_size * self.feature_size, self.output_dim],
        initializer=tf.random_normal_initializer(stddev=1 / math.sqrt(self.cluster_size)))

    fv = tf.matmul(fv, hidden1_weights)

    if self.gating:
      fv = super(NetFV, self).context_gating(fv)

    return fv


def _collect_named_outputs(outputs_collections, name, output):
  if outputs_collections is not None:
    tf.add_to_collection(outputs_collections, NamedOutputs(name, output))
  return output
