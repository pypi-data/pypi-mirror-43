from __future__ import division, print_function, absolute_import
import tensorflow as tf

from tefla.core import initializers as initz
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import dropout, avg_pool_2d, prelu
from tefla.core.layers import input, conv2d, fully_connected, max_pool, softmax

# sizes - (width, height)
# image_size = (256, 256)
# crop_size = (224, 224)
image_size = (512, 512)
crop_size = (448, 448)


def block_inception_a(inputs, name='block_a', **kwargs):
    """Builds Inception-A block for Inception v4 network."""
    # By default use stride=1 and SAME padding
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'BlockInceptionA', [inputs], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            branch_0 = conv2d(inputs, 96, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            branch_1 = conv2d(inputs, 64, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_1 = conv2d(branch_1, 96, name='Conv2d_0b_3x3', **kwargs)
        with tf.variable_scope('Branch_2'):
            branch_2 = conv2d(inputs, 64, filter_size=(
                1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 96, name='Conv2d_0b_3x3', **kwargs)
            branch_2 = conv2d(
                branch_2, 96, name='Conv2d_0c_3x3', **kwargs)
        with tf.variable_scope('Branch_3'):
            branch_3 = avg_pool_2d(
                inputs, stride=(1, 1), name='AvgPool_0a_3x3')
            branch_3 = conv2d(branch_3, 96, filter_size=(
                1, 1), name='Conv2d_0b_1x1', **kwargs)
        return tf.concat([branch_0, branch_1, branch_2, branch_3], 3)


def block_reduction_a(inputs, name='reduction_block_a', **kwargs):
    """Builds Reduction-A block for Inception v4 network."""
    # By default use stride=1 and SAME padding
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'BlockReductionA', [inputs], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            branch_0 = conv2d(inputs, 384, stride=(
                2, 2), name='Conv2d_1a_3x3', **kwargs)
        with tf.variable_scope('Branch_1'):
            branch_1 = conv2d(
                inputs, 192, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_1 = conv2d(
                branch_1, 224, name='Conv2d_0b_3x3', **kwargs)
            branch_1 = conv2d(branch_1, 256, stride=(
                2, 2), name='Conv2d_1a_3x3', **kwargs)
        with tf.variable_scope('Branch_2'):
            branch_2 = max_pool(inputs, stride=(
                2, 2), name='MaxPool_1a_3x3')
        return tf.concat([branch_0, branch_1, branch_2], 3)


def block_inception_b(inputs, name='block_b', **kwargs):
    """Builds Inception-B block for Inception v4 network."""
    # By default use stride=1 and SAME padding
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'BlockInceptionB', [inputs], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            branch_0 = conv2d(
                inputs, 384, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            branch_1 = conv2d(
                inputs, 192, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_1 = conv2d(
                branch_1, 224, filter_size=(1, 7), name='Conv2d_0b_1x7', **kwargs)
            branch_1 = conv2d(
                branch_1, 256, filter_size=(7, 1), name='Conv2d_0c_7x1', **kwargs)
        with tf.variable_scope('Branch_2'):
            branch_2 = conv2d(
                inputs, 192, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 192, filter_size=(7, 1), name='Conv2d_0b_7x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 224, filter_size=(1, 7), name='Conv2d_0c_1x7', **kwargs)
            branch_2 = conv2d(
                branch_2, 224, filter_size=(7, 1), name='Conv2d_0d_7x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 256, filter_size=(1, 7), name='Conv2d_0e_1x7', **kwargs)
        with tf.variable_scope('Branch_3'):
            branch_3 = avg_pool_2d(
                inputs, stride=(1, 1), name='AvgPool_0a_3x3')
            branch_3 = conv2d(
                branch_3, 128, filter_size=(1, 1), name='Conv2d_0b_1x1', **kwargs)
        return tf.concat([branch_0, branch_1, branch_2, branch_3], 3)


def block_reduction_b(inputs, name='reduction_block_b', **kwargs):
    """Builds Reduction-B block for Inception v4 network."""
    # By default use stride=1 and SAME padding
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'BlockReductionB', [inputs], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            branch_0 = conv2d(
                inputs, 192, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_0 = conv2d(branch_0, 192, filter_size=(
                3, 3), stride=(2, 2), name='Conv2d_1a_3x3', **kwargs)
        with tf.variable_scope('Branch_1'):
            branch_1 = conv2d(
                inputs, 256, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_1 = conv2d(
                branch_1, 256, filter_size=(1, 7), name='Conv2d_0b_1x7', **kwargs)
            branch_1 = conv2d(
                branch_1, 320, filter_size=(7, 1), name='Conv2d_0c_7x1', **kwargs)
            branch_1 = conv2d(branch_1, 320, filter_size=(
                3, 3), stride=(2, 2), name='Conv2d_1a_3x3', **kwargs)
        with tf.variable_scope('Branch_2'):
            branch_2 = max_pool(inputs, filter_size=(
                3, 3), stride=(2, 2), name='MaxPool_1a_3x3')
        return tf.concat([branch_0, branch_1, branch_2], 3)


def block_inception_c(inputs, name='block_c', **kwargs):
    """Builds Inception-C block for Inception v4 network."""
    # By default use stride=1 and SAME padding
    reuse = kwargs.get('reuse')
    with tf.variable_scope(name, 'BlockInceptionC', [inputs], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            branch_0 = conv2d(
                inputs, 256, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
        with tf.variable_scope('Branch_1'):
            branch_1 = conv2d(
                inputs, 384, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_1 = tf.concat([
                conv2d(branch_1, 256, filter_size=(1, 3),
                       name='Conv2d_0b_1x3', **kwargs),
                conv2d(branch_1, 256, filter_size=(3, 1), name='Conv2d_0c_3x1', **kwargs)], 3)
        with tf.variable_scope('Branch_2'):
            branch_2 = conv2d(
                inputs, 384, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 448, filter_size=(3, 1), name='Conv2d_0b_3x1', **kwargs)
            branch_2 = conv2d(
                branch_2, 512, filter_size=(1, 3), name='Conv2d_0c_1x3', **kwargs)
            branch_2 = tf.concat([
                conv2d(branch_2, 256, filter_size=(1, 3),
                       name='Conv2d_0d_1x3', **kwargs),
                conv2d(branch_2, 256, filter_size=(3, 1), name='Conv2d_0e_3x1', **kwargs)], 3)
        with tf.variable_scope('Branch_3'):
            branch_3 = avg_pool_2d(
                inputs, filter_size=(3, 3), stride=(1, 1), name='AvgPool_0a_3x3')
            branch_3 = conv2d(
                branch_3, 256, filter_size=(1, 1), name='Conv2d_0b_1x1', **kwargs)
        return tf.concat([branch_0, branch_1, branch_2, branch_3], 3)


def inception_v4_base(inputs, name='inception_4', input_size=512, num_block_a=4, num_block_b=7, num_block_c=3, **kwargs):
    """Creates the Inception V4 network up to the given final endpoint.

    Args:
      inputs: a 4-D tensor of size [batch_size, height, width, 3].
      final_endpoint: specifies the endpoint to construct the network up to.
        It can be one of [ 'Conv2d_1a_3x3', 'Conv2d_2a_3x3', 'Conv2d_2b_3x3',
        'Mixed_3a', 'Mixed_4a', 'Mixed_5a', 'Mixed_5b', 'Mixed_5c', 'Mixed_5d',
        'Mixed_5e', 'Mixed_6a', 'Mixed_6b', 'Mixed_6c', 'Mixed_6d', 'Mixed_6e',
        'Mixed_6f', 'Mixed_6g', 'Mixed_6h', 'Mixed_7a', 'Mixed_7b', 'Mixed_7c',
        'Mixed_7d']
      scope: Optional variable_scope.

    Returns:
      end_points: the set of end_points from the inception model.

    Raises:
      ValueError: if final_endpoint is not set to one of the predefined values,
    """
    finetune_kwargs=dict(kwargs)
    finetune_kwargs.update({'trainable': False})
    with tf.variable_scope(name, 'InceptionV4', [inputs]):
        # 448 x 448 x 3
        net = conv2d(inputs, 32, filter_size=(3, 3), stride=(
            2, 2), name='Conv2d_1a_3x3', **finetune_kwargs)
        # 224 x 224 x 32
        net = conv2d(net, 32, name='Conv2d_2a_3x3', **finetune_kwargs)
        # 224 x 224 x 32
        net = max_pool(net, name='MaxPool_2a_3x3')
        # 112 x 112 x 32
        net = conv2d(net, 64, name='Conv2d_2b_3x3', **kwargs)
        # 112 x 112 x 64
        with tf.variable_scope('Mixed_3a'):
            with tf.variable_scope('Branch_0'):
                branch_0 = max_pool(net, filter_size=(
                    3, 3), stride=(2, 2), name='MaxPool_0a_3x3')
            with tf.variable_scope('Branch_1'):
                branch_1 = conv2d(net, 96, filter_size=(3, 3), stride=(
                    2, 2), name='Conv2d_0a_3x3', **kwargs)
            net = tf.concat([branch_0, branch_1], 3)

        # 64 x 64 x 160
        with tf.variable_scope('Mixed_4a'):
            with tf.variable_scope('Branch_0'):
                branch_0 = conv2d(
                    net, 64, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
                branch_0 = conv2d(branch_0, 96, filter_size=(
                    3, 3), name='Conv2d_1a_3x3', **kwargs)
            with tf.variable_scope('Branch_1'):
                branch_1 = conv2d(
                    net, 64, filter_size=(1, 1), name='Conv2d_0a_1x1', **kwargs)
                branch_1 = conv2d(
                    branch_1, 64, filter_size=(1, 7), name='Conv2d_0b_1x7', **kwargs)
                branch_1 = conv2d(
                    branch_1, 64, filter_size=(7, 1), name='Conv2d_0c_7x1', **kwargs)
                branch_1 = conv2d(branch_1, 96, filter_size=(
                    3, 3), name='Conv2d_1a_3x3', **kwargs)
            net = tf.concat([branch_0, branch_1], 3)

        # 64 x 64 x 192
        with tf.variable_scope('Mixed_5a'):
            with tf.variable_scope('Branch_0'):
                branch_0 = conv2d(net, 192, filter_size=(3, 3), stride=(
                    2, 2), name='Conv2d_1a_3x3', **kwargs)
            with tf.variable_scope('Branch_1'):
                branch_1 = max_pool(net, filter_size=(3, 3), stride=(
                    2, 2), name='MaxPool_1a_3x3')
            net = tf.concat([branch_0, branch_1], 3)

        if input_size in (256, 512):
            # 32 x 32 x 384
            # num_block_a x Inception-A blocks
            for idx in range(num_block_a):
                block_name = 'Mixed_5' + chr(ord('b') + idx)
                net = block_inception_a(net, block_name, **kwargs)
            # 32 x 32 x 384
            # Reduction-A block
            net = block_reduction_a(net, 'Mixed_6a', **kwargs)
        if input_size == 512:
            # 16 x 16 x 1024
            # num_block_b x Inception-B blocks
            for idx in range(num_block_b):
                block_name = 'Mixed_6' + chr(ord('b') + idx)
                net = block_inception_b(net, block_name, **kwargs)
            # 16 x 16 x 1024
            # Reduction-B block
            net = block_reduction_b(net, 'Mixed_7a', **kwargs)
        # 8 x 8 x 1536
        # num_block_c x Inception-C blocks
        for idx in range(num_block_c):
            block_name = 'Mixed_7' + chr(ord('b') + idx)
            net = block_inception_c(net, block_name, **kwargs)
        return net


def model(inputs, is_training, reuse, input_size=image_size[0], num_block_a=4, num_block_b=5, num_block_c=3, num_classes=5,
          dropout_keep_prob=0.8,
          name='InceptionV4'):
    common_args = common_layer_args(is_training, reuse)
    conv_args = make_args(batch_norm=True, activation=prelu, trainable=True, w_init=initz.he_normal(
        scale=1), untie_biases=True, **common_args)
    logit_args = make_args(
        activation=None, w_init=initz.he_normal(scale=1), **common_args)
    # inputs = input((None, crop_size[1], crop_size[0], 3), **common_args)
    with tf.variable_scope(name, 'InceptionV4'):
        net = inception_v4_base(inputs, name=name, input_size=input_size, num_block_a=num_block_a,
                                num_block_b=num_block_b, num_block_c=num_block_c, **conv_args)
        # Final pooling and prediction
        with tf.variable_scope('Logits'):
            # 8 x 8 x 1536
            net = avg_pool_2d(net, net.get_shape().as_list()[1:3], name='AvgPool_1a')
            # 1 x 1 x 1536
            net = dropout(
                net, is_training, drop_p=1 - dropout_keep_prob, name='Dropout_1b')
            logits = fully_connected(net, num_classes,
                                     name='logits', **logit_args)
            predictions = softmax(logits, name='predictions', **common_args)
        return end_points(is_training)
