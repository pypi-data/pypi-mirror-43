from __future__ import division, print_function, absolute_import
import tensorflow as tf

from tefla.core import initializers as initz
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import dropout, rms_pool_2d, feature_max_pool_2d
from tefla.core.layers import input, conv2d, fully_connected, max_pool, lrelu, softmax

# sizes - (width, height)
image_size = (512, 512)
crop_size = (448, 448)


def model(x, is_training, reuse, input_size=image_size[0], num_classes=2):
    common_args = common_layer_args(is_training, reuse)
    conv_args = make_args(batch_norm=True, activation=lrelu, w_init=initz.he_normal(
        scale=1), untie_biases=True, **common_args)
    fc_args = make_args(
        activation=lrelu, w_init=initz.he_normal(scale=1), **common_args)
    logit_args = make_args(
        activation=None, w_init=initz.he_normal(scale=1), **common_args)
    pred_args = make_args(
        activation=lrelu, w_init=initz.he_normal(scale=1), **common_args)
    pool_args = make_args(padding='SAME', filter_size=(
        2, 2), stride=(2, 2), **common_args)

    # x = input((None, crop_size[1], crop_size[0], 3), **common_args)
    x = conv2d(x, 64, name="conv1_1", **conv_args)
    x = max_pool(x, name='pool1', **pool_args)
    x = conv2d(x, 64, name="conv1_2", **conv_args)
    x = conv2d(x, 64, name="conv2_1", **conv_args)
    x = conv2d(x, 64, name="conv2_2", **conv_args)
    x = max_pool(x, name='pool2', **pool_args)
    # x = conv2d(x, 64, name="conv2_2", **conv_args)
    # 128
    x = conv2d(x, 96, name="conv3_1", **conv_args)
    x = conv2d(x, 96, name="conv3_2", **conv_args)
    x = conv2d(x, 96, name="conv3_3", **conv_args)
    x = max_pool(x, name='pool3', **pool_args)
    # 64
    x_0 = conv2d(x, 128, name="conv4_1", **conv_args)
    x = conv2d(x_0, 128, name="conv4_2", **conv_args)
    x = conv2d(x, 128, name="conv4_3", **conv_args)
    x = max_pool(x, name='pool4', **pool_args)
    # 32
    x_1 = conv2d(x, 256, name="conv5_1", **conv_args)
    x = conv2d(x_1, 256, name="conv5_2", **conv_args)
    x = conv2d(x, 256, name="conv5_3", **conv_args)
    x = max_pool(x, name='pool5', **pool_args)
    # 16
    x_2 = conv2d(x, 512, name="conv6_1", **conv_args)
    x = conv2d(x_2, 512, name="conv6_2", **conv_args)
    x = conv2d(x, 512, name="conv6_3", **conv_args)
    x = max_pool(x, name='pool6', **pool_args)
    # Skip
    x = conv2d(x, 192, name="conv7_1", **conv_args)
    x_4 = max_pool(x_1, filter_size=(4, 4), stride=(4, 4), name="skip_pool1")
    x_5 = max_pool(x_2, name="skip_pool2", **pool_args)
    x = tf.concat([x, x_4, x_5], 3)

    x_8 = max_pool(x_0, filter_size=(4, 4), stride=(4, 4), name="skip_pool11")
    x_6 = max_pool(x_1, stride=(2, 2), name="skip_pool3")
    x_7 = tf.concat([x_2, x_6, x_8], axis=3)
    x_7 = conv2d(x_7, 512, name="conv8_1", **conv_args)
    x_7 = max_pool(x_7, stride=(2, 2), name="skip_pool4")

    x_7 = dropout(x_7, drop_p=0.5, name="pool_dropout1_2", **common_args)
    x_7 = conv2d(x_7, 1024, name="fc1_2", **fc_args)
    x_7 = feature_max_pool_2d(x_7, name='fp1_2', **common_args)
    x_7 = dropout(x_7, drop_p=0.5, name="pool_dropout2_2", **common_args)
    x_7 = rms_pool_2d(x_7, name="rms_pool1_2", **pool_args)
    x_7 = conv2d(x_7, 1024, name="fc2_2", **fc_args)
    x_7 = feature_max_pool_2d(x_7, name='fp2_2', **common_args)

    # 8
    x = dropout(x, drop_p=0.5, name="pool_dropout1", **common_args)
    x = conv2d(x, 1024, name="fc1", **fc_args)
    x = feature_max_pool_2d(x, name='fp1', **common_args)
    x = dropout(x, drop_p=0.5, name="pool_dropout2", **common_args)
    x = rms_pool_2d(x, name="rms_pool1", **pool_args)
    x = conv2d(x, 1024, name="fc2", **fc_args)
    x = feature_max_pool_2d(x, name='fp2', **common_args)

    x = tf.concat([x, x_7], axis=3)
    logits = fully_connected(x, n_output=num_classes,
                             name="logits", **logit_args)

    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)
