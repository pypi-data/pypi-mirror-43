
import math
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


def round_int(x):
  """Rounds `x` and then converts to an int."""
  return int(math.floor(x + 0.5))

def batch_norm(inputs, is_training, name):
  return tf.layers.batch_normalization(
      inputs=inputs,
      axis=-1,
      training=is_training,
      fused=True,
      center=True,
      scale=True,
      momentum=_BATCH_NORM_DECAY,
      epsilon=_BATCH_NORM_EPSILON,
      name=name
  )

def shortcut(x, output_filters, stride):
  """Applies strided avg pool or zero padding to make output_filters match x."""
  num_filters = int(x.shape[3])
  if stride == 2:
    x = tf.nn.avg_pool(x, [1, 2, 2, 1], strides=[1, stride, stride, 1], padding='SAME')
  if num_filters != output_filters:
    diff = output_filters - num_filters
    assert diff > 0
    # Zero padd diff zeros
    padding = [[0, 0], [0, 0], [0, 0], [0, diff]]
    x = tf.pad(x, padding)
  return x


def calc_prob(curr_layer, total_layers, p_l):
  """Calculates drop prob depending on the current layer."""
  return 1 - (float(curr_layer) / total_layers) * p_l


def bottleneck_layer(x, n, stride, prob, is_training, alpha, beta):
  """Bottleneck layer for shake drop model."""
  assert alpha[1] > alpha[0]
  assert beta[1] > beta[0]
  with tf.variable_scope('bottleneck_{}'.format(prob)):
    input_layer = x
    x = batch_norm(x, is_training, name='bn_1_pre')
    x = conv2d(x, n, 1, name='1x1_conv_contract')
    x = batch_norm(x, is_training, name='bn_1_post')
    x = tf.nn.relu(x)
    x = conv2d(x, n, 3, stride=stride, name='3x3')
    x = batch_norm(x, is_training, name='bn_2')
    x = tf.nn.relu(x)
    x = conv2d(x, n * 4, 1, name='1x1_conv_expand')
    x = batch_norm(x, is_training, name='bn_3')

    # Apply regularization here
    # Sample bernoulli with prob
    if is_training:
      batch_size = tf.shape(x)[0]
      bern_shape = [batch_size, 1, 1, 1]
      random_tensor = prob
      random_tensor += tf.random_uniform(bern_shape, dtype=tf.float32)
      binary_tensor = tf.floor(random_tensor)

      alpha_values = tf.random_uniform(
          [batch_size, 1, 1, 1], minval=alpha[0], maxval=alpha[1],
          dtype=tf.float32)
      beta_values = tf.random_uniform(
          [batch_size, 1, 1, 1], minval=beta[0], maxval=beta[1],
          dtype=tf.float32)
      rand_forward = (
          binary_tensor + alpha_values - binary_tensor * alpha_values)
      rand_backward = (
          binary_tensor + beta_values - binary_tensor * beta_values)
      x = x * rand_backward + tf.stop_gradient(x * rand_forward -
                                               x * rand_backward)
    else:
      expected_alpha = (alpha[1] + alpha[0])/2
      # prob is the expectation of the bernoulli variable
      x = (prob + expected_alpha - prob * expected_alpha) * x

    res = shortcut(input_layer, n * 4, stride)
    return x + res


def build_model(images, num_classes, is_training, reuse, depth=272, image_size=256, name='ModelSD'):
  # ShakeDrop Hparams
  p_l = 0.5
  alpha_shake = [-1, 1]
  beta_shake = [0, 1]

  # PyramidNet Hparams
  alpha = 200
  # This is for the bottleneck architecture specifically
  n = int((depth - 2) / 15)
  start_channel = 16
  add_channel = alpha / (3 * n)

  common_args = common_layer_args(is_training, reuse)
  outputs_collections = common_args.get('outputs_collections', None)
  # Building the models
  x = images
  with tf.variable_scope(name, reuse=reuse):
    x = conv2d(x, 16, 3, name='init_conv')
    x = batch_norm(x, is_training, name='init_bn')

    layer_num = 1
    total_layers = n * 5
    start_channel += add_channel
    prob = calc_prob(layer_num, total_layers, p_l)
    x = bottleneck_layer(
	x, round_int(start_channel), 2, prob, is_training, alpha_shake,
	beta_shake)
    layer_num += 1
    for _ in range(1, n):
      start_channel += add_channel
      prob = calc_prob(layer_num, total_layers, p_l)
      x = bottleneck_layer(
	  x, round_int(start_channel), 1, prob, is_training, alpha_shake,
	  beta_shake)
      layer_num += 1

    start_channel += add_channel
    prob = calc_prob(layer_num, total_layers, p_l)
    x = bottleneck_layer(
	x, round_int(start_channel), 2, prob, is_training, alpha_shake,
	beta_shake)
    layer_num += 1
    for _ in range(1, n):
      start_channel += add_channel
      prob = calc_prob(layer_num, total_layers, p_l)
      x = bottleneck_layer(
	  x, round_int(start_channel), 1, prob, is_training, alpha_shake,
	  beta_shake)
      layer_num += 1

    start_channel += add_channel
    prob = calc_prob(layer_num, total_layers, p_l)
    x = bottleneck_layer(
	x, round_int(start_channel), 2, prob, is_training, alpha_shake,
	beta_shake)
    layer_num += 1
    for _ in range(1, n):
      start_channel += add_channel
      prob = calc_prob(layer_num, total_layers, p_l)
      x = bottleneck_layer(
	  x, round_int(start_channel), 1, prob, is_training, alpha_shake,
	  beta_shake)
      layer_num += 1

    start_channel += add_channel
    prob = calc_prob(layer_num, total_layers, p_l)
    x = bottleneck_layer(
	x, round_int(start_channel), 2, prob, is_training, alpha_shake,
	beta_shake)
    layer_num += 1
    for _ in range(1, n):
      start_channel += add_channel
      prob = calc_prob(layer_num, total_layers, p_l)
      x = bottleneck_layer(
	  x, round_int(start_channel), 1, prob, is_training, alpha_shake,
	  beta_shake)
      layer_num += 1

    if image_size == 512:
      start_channel += add_channel
      prob = calc_prob(layer_num, total_layers, p_l)
      x = bottleneck_layer(
	  x, round_int(start_channel), 2, prob, is_training, alpha_shake,
	  beta_shake)
      layer_num += 1
      for _ in range(1, n):
	start_channel += add_channel
	prob = calc_prob(layer_num, total_layers, p_l)
	x = bottleneck_layer(
	    x, round_int(start_channel), 1, prob, is_training, alpha_shake,
	    beta_shake)
	layer_num += 1

    x = batch_norm(x, is_training, name='final_bn')
    x = tf.nn.relu(x)
    global_pool = tf.reduce_mean(x, axis=(1, 2), name="global_pool")
    modelSD_layer = tf.layers.dense(global_pool, units=num_classes)
    logits = register_to_collections(modelSD_layer, name='logits', outputs_collections=outputs_collections)
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
  depth = 272
  image_size = 256
  #512
  #strides = [2, 2, 2, 2, 2, 2]
  #k = 7
  #depth = 146
  return build_model(inputs, num_classes, is_training, reuse, depth, image_size, name='ModelSD')


def test():
  im = tf.random_normal((32, 224, 224, 3))
  logits = model(im, True, None)
  print(logits['logits'].shape)


if __name__=='__main__':
  test()
