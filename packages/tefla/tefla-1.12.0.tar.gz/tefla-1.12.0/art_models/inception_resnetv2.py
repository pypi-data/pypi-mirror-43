from __future__ import division, print_function, absolute_import

import tensorflow as tf
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import conv2d, fully_connected, max_pool, prelu, repeat
from tefla.core.layers import input, softmax, dropout, avg_pool_2d, batch_norm_tf as batch_norm


# Block with 3x3 and 5x5 filters
def block35(net, activation=prelu, scale=0.17, name=None, **kwargs):
    is_training = kwargs.get('is_training')
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'block35'):
        with tf.variable_scope('Branch_0'):
            tower_conv = conv2d(net, 16, filter_size=(1, 1),
                                name='Conv2d_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = conv2d(net, 16, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            tower_conv1_1 = conv2d(
                tower_conv1_0, 16, name='Conv2d_0b_3x3', **kwargs)
        with tf.variable_scope('Branch_2'):
            tower_conv2_0 = conv2d(net, 16, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            tower_conv2_1 = conv2d(
                tower_conv2_0, 16, name='Conv2d_0b_3x3', **kwargs)
            tower_conv2_2 = conv2d(
                tower_conv2_1, 16, name='Conv2d_0c_3x3', **kwargs)
        mixed = tf.concat([tower_conv, tower_conv1_1, tower_conv2_2], 3)
        up = conv2d(mixed, net.get_shape()[3], is_training, reuse, filter_size=(
            1, 1), batch_norm=None, activation=None, name='Conv2d_1x1')
        net += scale * up
        if activation:
            net = activation(net, reuse)
    return net


# Block with 1x7 and 7x1 filters
def block17(net, activation=prelu, scale=1.0, name=None, **kwargs):
    is_training = kwargs.get('is_training')
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'block17'):
        with tf.variable_scope('Branch_0'):
            tower_conv = conv2d(net, 32, filter_size=(
                1, 1), name='Conv2d_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = conv2d(net, 32, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            tower_conv1_1 = conv2d(tower_conv1_0, 32, filter_size=(
                1, 7), name='Conv2d_0b_1x7', **kwargs)
            tower_conv1_2 = conv2d(tower_conv1_1, 32, filter_size=(
                7, 1), name='Conv2d_0c_7x1', **kwargs)
        mixed = tf.concat([tower_conv, tower_conv1_2], 3)
        up = conv2d(mixed, net.get_shape()[3], is_training, reuse, filter_size=(
            1, 1), batch_norm=None, activation=None, name='Conv2d_1x1')
        net += scale * up
        if activation:
            net = activation(net, reuse)
    return net


# Block with 1x3 and 3x1 filters
def block13(net, activation=prelu, scale=1.0, name=None, **kwargs):
    is_training = kwargs.get('is_training')
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'block13'):
        with tf.variable_scope('Branch_0'):
            tower_conv = conv2d(net, 32, filter_size=(
                1, 1), name='Conv2d_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = conv2d(net,32, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            tower_conv1_1 = conv2d(tower_conv1_0, 32, filter_size=(
                1, 3), name='Conv2d_0b_1x3', **kwargs)
            tower_conv1_2 = conv2d(tower_conv1_1, 32, filter_size=(
                3, 1), name='Conv2d_0c_3x1', **kwargs)
        mixed = tf.concat([tower_conv, tower_conv1_2], 3)
        up = conv2d(mixed, net.get_shape()[3], is_training, reuse, filter_size=(
            1, 1), batch_norm=None, activation=None, name='Conv2d_1x1')
        net += scale * up
        if activation:
            net = activation(net, reuse)
    return net


# sizes - (width, height)
# image_size = (339, 339)
# crop_size = (299, 299)
image_size = (128, 128)
crop_size = (112, 112)


def model(inputs, is_training, reuse, input_size=image_size[0], num_classes=5, drop_prob=0.2, scope='InceptionResnet'):
    common_args = common_layer_args(is_training, reuse)
    rest_conv_params = make_args(
        untie_biases=True, batch_norm=batch_norm, **common_args)
    rest_logit_params = make_args(activation=prelu, **common_args)
    rest_pool_params = make_args(padding='SAME', **common_args)
    rest_dropout_params = make_args(drop_p=drop_prob, **common_args)

    with tf.variable_scope(scope, 'InceptionResnetV2'):
        # 448 x 448
        net = conv2d(inputs, 16, name='Conv2d_1a_3x3', **rest_conv_params)
        # 112 x 112
        net = conv2d(net, 32, stride=2, name='Conv2d_2a_3x3', **rest_conv_params)
        # 112 x 112
        net = conv2d(net, 32, name='Conv2d_2b_3x3', **rest_conv_params)
        # 112 x 112
        net = max_pool(net, name='MaxPool_3a_3x3', **rest_pool_params)
        # 64 x 64
        net = conv2d(net, 32, filter_size=(1, 1),
                     name='Conv2d_3b_1x1', **rest_conv_params)
        # 64 x 64
        net = conv2d(net, 32, name='Conv2d_4a_3x3', **rest_conv_params)
        # 64 x 64
        net = max_pool(net, stride=(2, 2),
                       name='maxpool_5a_3x3', **rest_pool_params)

        # 32 x 32
        with tf.variable_scope('Mixed_5b'):
            with tf.variable_scope('Branch_0'):
                tower_conv = conv2d(net, 32, filter_size=(
                    1, 1), name='Conv2d_1x1', **rest_conv_params)
            with tf.variable_scope('Branch_1'):
                tower_conv1_0 = conv2d(net, 32, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv1_1 = conv2d(tower_conv1_0, 32, filter_size=(
                    5, 5), name='Conv2d_0b_5x5', **rest_conv_params)
            with tf.variable_scope('Branch_2'):
                tower_conv2_0 = conv2d(net, 32, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv2_1 = conv2d(
                    tower_conv2_0, 32, name='Conv2d_0b_3x3', **rest_conv_params)
                tower_conv2_2 = conv2d(
                    tower_conv2_1, 32, name='Conv2d_0c_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_3'):
                tower_pool = avg_pool_2d(net, stride=(
                    1, 1), name='avgpool_0a_3x3', **rest_pool_params)
                tower_pool_1 = conv2d(tower_pool, 32, filter_size=(
                    1, 1), name='Conv2d_0b_1x1', **rest_conv_params)
            net = tf.concat([tower_conv, tower_conv1_1,
                             tower_conv2_2, tower_pool_1], 3)

        net = repeat(net, 5, block35, name='repeat35', **rest_conv_params)
        if input_size == 339:
	    net = max_pool(net, name='MaxPool_repeat35', **rest_pool_params)

        # 32 x 32
        with tf.variable_scope('Mixed_6a'):
            with tf.variable_scope('Branch_0'):
                tower_conv = conv2d(net, 64, stride=(
                    2, 2), name='Conv2d_1a_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_1'):
                tower_conv1_0 = conv2d(net, 64, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv1_1 = conv2d(
                    tower_conv1_0, 64, name='Conv2d_0b_3x3', **rest_conv_params)
                tower_conv1_2 = conv2d(tower_conv1_1, 64, stride=(
                    2, 2), name='Conv2d_1a_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_2'):
                tower_pool = max_pool(
                    net, name='maxpool_1a_3x3', **rest_pool_params)
            net = tf.concat([tower_conv, tower_conv1_2, tower_pool], 3)

        net = repeat(net, 4, block17, name='repeat17',
                     scale=0.10, **rest_conv_params)
        # 16 x 16
        # Auxillary tower
        with tf.variable_scope('auxlogits'):
            aux = avg_pool_2d(net, filter_size=(5, 5), stride=(
                3, 3), name='Conv2d_1a_3x3', **rest_pool_params)
            aux = conv2d(aux, 32, filter_size=(1, 1),
                         name='Conv2d_1b_1x1', **rest_conv_params)
            aux = conv2d(aux, 32, filter_size=aux.get_shape().as_list()[
                         1:3], name='Conv2d_2a_5x5', **rest_conv_params)
            aux = fully_connected(
                aux, num_classes, name='logits', **rest_logit_params)

        with tf.variable_scope('mixed_7a'):
            with tf.variable_scope('Branch_0'):
                tower_conv = conv2d(net, 128, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv_1 = conv2d(tower_conv, 128, stride=(
                    2, 2), name='Conv2d_1a_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_1'):
                tower_conv1 = conv2d(net, 64, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv1_1 = conv2d(tower_conv1, 128, stride=(
                    2, 2), name='Conv2d_1a_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_2'):
                tower_conv2 = conv2d(net, 64, filter_size=(
                    1, 1), name='Conv2d_0a_1x1', **rest_conv_params)
                tower_conv2_1 = conv2d(
                    tower_conv2, 128, name='Conv2d_0b_3x3', **rest_conv_params)
                tower_conv2_2 = conv2d(tower_conv2_1, 128, stride=(
                    2, 2), name='Conv2d_1a_3x3', **rest_conv_params)
            with tf.variable_scope('Branch_3'):
                tower_pool = max_pool(
                    net, name='maxpool_1a_3x3', **rest_pool_params)
            net = tf.concat([tower_conv_1, tower_conv1_1,
                             tower_conv2_2, tower_pool], 3)
        # 8 x 8
        if input_size == 339:
		net = repeat(net, 5, block13, name='repeat13',
			     scale=0.20, **rest_conv_params)
		net = block13(net, activation=None, **rest_conv_params)

		net = conv2d(net, 1536, filter_size=(1, 1),
			     name='Conv2d_7b_1x1', **rest_conv_params)

        with tf.variable_scope('logits'):
            net = avg_pool_2d(net, filter_size=net.get_shape().as_list()[
                              1:3], name='avgpool_1a_8x8', **rest_pool_params)
            net = dropout(net, name='dropout', **rest_dropout_params)
            logits = fully_connected(
                net, n_output=num_classes, name='logits', **rest_logit_params)
            predictions = softmax(logits, name='predictions',
                                  **common_args)

    return end_points(is_training)
