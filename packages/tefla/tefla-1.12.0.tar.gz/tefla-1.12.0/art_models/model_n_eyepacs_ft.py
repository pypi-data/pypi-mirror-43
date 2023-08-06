from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import softmax, register_to_collections

# Learning hyperaparmeters
_BATCH_NORM_DECAY = 0.997
_BATCH_NORM_EPSILON = 1e-5
# sizes - (width, height)
# image_size = (256, 256)
# crop_size = (224, 224)
# image_size = (128, 128)
# crop_size = (112, 112)
image_size = (512, 512)
crop_size = (448, 448)


def conv(image, filters, strides=1, kernel_size=3, trainable=True):
  """Convolution with default options from the model_n paper."""
  # Use initialization from https://arxiv.org/pdf/1502.01852.pdf

  return tf.layers.conv2d(
      inputs=image,
      filters=filters,
      kernel_size=kernel_size,
      strides=strides,
      activation=tf.identity,
      use_bias=False,
      padding="same",
      kernel_initializer=tf.variance_scaling_initializer(),
      trainable=trainable,
  )


def modelN_block(image, filters, is_training, use_bottleneck=True):
  """Standard BN+Relu+conv block."""
  image = tf.layers.batch_normalization(
      inputs=image,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
  )

  if use_bottleneck:
    # Add bottleneck layer to optimize computation and reduce HBM space
    image = tf.nn.relu(image)
    image = conv(image, 4 * filters, strides=1, kernel_size=1)
    image = tf.layers.batch_normalization(
        inputs=image,
        axis=-1,
        training=is_training,
        fused=True,
        center=True,
        scale=True,
        momentum=_BATCH_NORM_DECAY,
        epsilon=_BATCH_NORM_EPSILON,
    )

  image = tf.nn.relu(image)
  return conv(image, filters)


def transition_layer(image, filters, is_training):
  """Construct the transition layer with specified growth rate."""

  image = tf.layers.batch_normalization(
      inputs=image,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
  )
  image = tf.nn.relu(image)
  conv_img = conv(image, filters=filters, kernel_size=1)
  return tf.layers.average_pooling2d(
      conv_img, pool_size=2, strides=2, padding="same")


def _int_shape(layer):
  return layer.get_shape().as_list()


# Definition of the Imagenet network
def model_n_imagenet_model(image, k, depths, num_classes, is_training, reuse, input_size=image_size[0], name='model_n'):

  common_args = common_layer_args(is_training, reuse)
  outputs_collections = common_args.get('outputs_collections', None)
  with tf.variable_scope(name, reuse=reuse):
    num_channels = 2 * k
    v = conv(image, filters=2 * k, strides=2, kernel_size=7, trainable=False)
    v = tf.layers.batch_normalization(
      inputs=v,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      trainable=False,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
    )
    v = tf.nn.relu(v)
    v = tf.layers.max_pooling2d(v, pool_size=3, strides=2, padding="same")
    for i, depth in enumerate(depths):
      with tf.variable_scope("block-%d" % i):
        for j in xrange(depth):
          with tf.variable_scope("modelNblock-%d-%d" % (i, j)):
            output = modelN_block(v, k, is_training)
            v = tf.concat([v, output], axis=3)
            num_channels += k
        if i != len(depths) - 1:
          num_channels /= 2
          v = transition_layer(v, num_channels, is_training)

    global_pool = tf.reduce_mean(v, axis=(1, 2), name="global_pool")
    modelN_layer = tf.layers.dense(global_pool, units=num_classes)
    logits = register_to_collections(modelN_layer, name='logits', outputs_collections=outputs_collections)
    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)


def model(inputs, is_training, reuse, num_classes=5):
  """DenseNet 121."""
  # depths = [6, 12, 32, 32]
  depths = [6, 12, 32, 38]
  # depths = [6, 12, 48, 32]
  growth_rate = 32
  return model_n_imagenet_model(inputs, growth_rate, depths, num_classes,
                                 is_training, reuse)


def model_n_imagenet_169(inputs, is_training=True, num_classes=1001):
  """DenseNet 121."""
  depths = [6, 12, 32, 32]
  growth_rate = 32
  return model_n_imagenet_model(inputs, growth_rate, depths, num_classes,
                                 is_training, reuse)


def model_n_imagenet_201(inputs, is_training=True, num_classes=1001):
  """DenseNet 121."""
  depths = [6, 12, 48, 32]
  growth_rate = 32
  return model_n_imagenet_model(inputs, growth_rate, depths, num_classes, is_training, reuse)
