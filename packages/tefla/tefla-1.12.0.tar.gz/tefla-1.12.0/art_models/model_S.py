from __future__ import print_function

import tensorflow as tf
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import softmax, register_to_collections

# Learning hyperaparmeters
_BATCH_NORM_DECAY = 0.997
_BATCH_NORM_EPSILON = 1e-5
# sizes - (width, height)
image_size = (256, 256)
crop_size = (224, 224)


def conv2d(image, filters, kernel_size, stride=1, name=None):
  """Convolution with default options from the model_n paper."""
  # Use initialization from https://arxiv.org/pdf/1502.01852.pdf

  return tf.layers.conv2d(
      inputs=image,
      filters=filters,
      kernel_size=kernel_size,
      strides=stride,
      activation=tf.identity,
      use_bias=False,
      padding="same",
      kernel_initializer=tf.variance_scaling_initializer(),
      name=name,
  )


def stride_arr(stride_h, stride_w):
  return [1, stride_h, stride_w, 1]


def _shake_shake_skip_connection(x, output_filters, stride, is_training):
  """Adds a residual connection to the filter x for the shake-shake model."""
  curr_filters = int(x.shape[3])
  if curr_filters == output_filters:
    return x
  stride_spec = stride_arr(stride, stride)
  # Skip path 1
  path1 = tf.nn.avg_pool(
      x, [1, 1, 1, 1], stride_spec, 'VALID', data_format='NHWC')
  path1 = conv2d(path1, int(output_filters / 2), 1, name='path1_conv')

  # Skip path 2
  # First pad with 0's then crop
  pad_arr = [[0, 0], [0, 1], [0, 1], [0, 0]]
  path2 = tf.pad(x, pad_arr)[:, 1:, 1:, :]
  concat_axis = 3

  path2 = tf.nn.avg_pool(
      path2, [1, 1, 1, 1], stride_spec, 'VALID', data_format='NHWC')
  path2 = conv2d(path2, int(output_filters / 2), 1, name='path2_conv')

  # Concat and apply BN
  final_path = tf.concat(values=[path1, path2], axis=concat_axis)
  final_path = tf.layers.batch_normalization(
      inputs=final_path,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
      name='final_path_bn'
  )
  return final_path


def _shake_shake_branch(x, output_filters, stride, rand_forward, rand_backward,
                        is_training):
  """Building a 2 branching convnet."""
  x = tf.nn.relu(x)
  x = conv2d(x, output_filters, 3, stride=stride, name='conv1')
  x = tf.layers.batch_normalization(
      inputs=x,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
      name='bn1'
  )
  x = tf.nn.relu(x)
  x = conv2d(x, output_filters, 3, name='conv2')
  x = tf.layers.batch_normalization(
      inputs=x,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
      name='bn2'
  )
  if is_training:
    x = x * rand_backward + tf.stop_gradient(x * rand_forward -
                                             x * rand_backward)
  else:
    x *= 1.0 / 2
  return x


def _shake_shake_block(x, output_filters, stride, is_training):
  """Builds a full shake-shake sub layer."""
  batch_size = tf.shape(x)[0]

  # Generate random numbers for scaling the branches
  rand_forward = [
      tf.random_uniform(
          [batch_size, 1, 1, 1], minval=0, maxval=1, dtype=tf.float32)
      for _ in range(2)
  ]
  rand_backward = [
      tf.random_uniform(
          [batch_size, 1, 1, 1], minval=0, maxval=1, dtype=tf.float32)
      for _ in range(2)
  ]
  # Normalize so that all sum to 1
  total_forward = tf.add_n(rand_forward)
  total_backward = tf.add_n(rand_backward)
  rand_forward = [samp / total_forward for samp in rand_forward]
  rand_backward = [samp / total_backward for samp in rand_backward]
  zipped_rand = zip(rand_forward, rand_backward)

  branches = []
  for branch, (r_forward, r_backward) in enumerate(zipped_rand):
    with tf.variable_scope('branch_{}'.format(branch)):
      b = _shake_shake_branch(x, output_filters, stride, r_forward, r_backward,
                              is_training)
      branches.append(b)
  res = _shake_shake_skip_connection(x, output_filters, stride, is_training)
  return res + tf.add_n(branches)


def _shake_shake_layer(x, output_filters, num_blocks, stride,
                       is_training):
  """Builds many sub layers into one full layer."""
  for block_num in range(num_blocks):
    curr_stride = stride if (block_num == 0) else 1
    with tf.variable_scope('layer_{}'.format(block_num)):
      x = _shake_shake_block(x, output_filters, curr_stride,
                             is_training)
  return x


def build_model(images, num_classes, is_training, reuse, depth, k, strides, name='ModelS'):
  n = int((depth - 2) / 6)
  x = images

  common_args = common_layer_args(is_training, reuse)
  outputs_collections = common_args.get('outputs_collections', None)
  with tf.variable_scope(name, reuse=reuse):
    x = conv2d(x, 32, 3, name='init_conv1')
    x = conv2d(x, 64, 3, stride=2, name='init_conv2')
    x = conv2d(x, 128, 3, name='init_conv3')
    x = conv2d(x, 128, 3, name='init_conv4')
    x = conv2d(x, 256, 3, stride=2, name='init_conv5')
    x = tf.layers.batch_normalization(
	inputs=x,
	axis=-1,
	training=is_training,
	fused=True,
	center=True,
	scale=True,
	momentum=_BATCH_NORM_DECAY,
	epsilon=_BATCH_NORM_EPSILON,
	name='init_bn'
    )
    inc_factor = 1
    for idx, stride in enumerate(strides):
      with tf.variable_scope("block-%d" % idx):
        inc_factor = inc_factor * stride
        x = _shake_shake_layer(x, 16 * k * inc_factor, n, stride, is_training)
    x = tf.nn.relu(x)
    global_pool = tf.reduce_mean(x, axis=(1, 2), name="global_pool")
    modelS_layer = tf.layers.dense(global_pool, units=num_classes)
    logits = register_to_collections(modelS_layer, name='logits', outputs_collections=outputs_collections)
    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)

# 128
def model(inputs, is_training, reuse, num_classes=5):
  """DenseNet 121."""
  #128
  #strides = [2, 2, 2, 2]
  #k = 6
  #depth = 98
  #256
  strides = [2, 2, 2]
  k = 7
  depth = 89
  #512
  #strides = [2, 2, 2, 2, 2, 2]
  #k = 7
  #depth = 146
  return build_model(inputs, num_classes, is_training, reuse, depth, k, strides, name='ModelS')


def test():
  im = tf.random_normal((32, 224, 224, 3))
  logits = model(im, True, None)
  print(logits['logits'].shape)


if __name__=='__main__':
  test()
