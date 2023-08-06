from __future__ import division, print_function, absolute_import
import tensorflow as tf

from tefla.core import initializers as initz
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import dropout, rms_pool_2d, feature_max_pool_2d, global_avg_pool
from tefla.core.layers import input, conv2d, fully_connected, max_pool, prelu, softmax

# sizes - (width, height)
image_size = (512, 512)
crop_size = (448, 448)

#image_size = (256, 256)
#crop_size = (224, 224)


def model(is_training, reuse, input_size=image_size[0], num_classes=2):
    common_args = common_layer_args(is_training, reuse)
    conv_args = make_args(batch_norm=True, activation=prelu, w_init=initz.he_normal(
        scale=1), untie_biases=True, **common_args)
    fc_args = make_args(
        activation=prelu, w_init=initz.he_normal(scale=1), **common_args)
    logit_args = make_args(
        activation=None, w_init=initz.he_normal(scale=1), **common_args)
    pred_args = make_args(
        activation=prelu, w_init=initz.he_normal(scale=1), **common_args)
    pool_args = make_args(padding='SAME', **common_args)

    inputs = input((None, crop_size[1], crop_size[0], 3), **common_args)
    x = conv2d(inputs, 32, stride=2, name="conv1_1", **conv_args)
    x = conv2d(x, 48, name="conv1_2", **conv_args)
    # 256
    x = conv2d(x, 96, name="conv1_3", **conv_args)
    x = conv2d(x, 96, stride=2, name="conv1_4", **conv_args)
    x = conv2d(x, 96, name="conv1_5", **conv_args)
    x = conv2d(x, 96, name="conv1_6", **conv_args)
    # 128
    x = conv2d(x, 128, stride=(2, 2), name="conv2_1", **conv_args)
    x = conv2d(x, 128, name="conv2_2", **conv_args)
    x = conv2d(x, 128, name="conv2_3", **conv_args)
    # 64
    x = conv2d(x, 128, stride=(2, 2), name="conv3_1", **conv_args)
    x = conv2d(x, 128, name="conv3_2", **conv_args)
    x = conv2d(x, 128, name="conv3_3", **conv_args)
    x_1 = conv2d(x, 128, name="conv3_4", **conv_args)
    # 32
    if input_size in (256, 512):
        x = conv2d(x_1, 128, stride=(2, 2), name="conv4_1", **conv_args)
        x = conv2d(x, 128, name="conv4_2", **conv_args)
        x = conv2d(x, 128, name="conv4_3", **conv_args)
        x_2 = conv2d(x, 128, name="conv4_4", **conv_args)
        x_4 = max_pool(x_1, filter_size=(4, 4), stride=4, name="skip_pool1", **pool_args)
    # 16
    if input_size == 512:
        x = conv2d(x_2, 192, stride=(2, 2), padding='SAME',
                   name="conv5_1", **conv_args)
        x = conv2d(x, 192, name="conv5_2", **conv_args)
        x = conv2d(x, 192, name="conv5_3", **conv_args)
        x_3 = conv2d(x, 192, name="conv5_4", **conv_args)
        x_5 = max_pool(x_2, filter_size=(3, 3), stride=(
            2, 2), name="skip_pool2", **pool_args)
    # Skip
    if input_size == 256:
        x = tf.concat([x_2, x_4], 3)
    if input_size == 512:
        x = tf.concat([x_3, x_4, x_5], 3)
    x = rms_pool_2d(x, filter_size=(3, 3), stride=(
        2, 2), name="rms_pool1", **pool_args)
    # 4
    x = dropout(x, drop_p=0.5, name="pool_dropout1", **common_args)
    x = conv2d(x, 1024, name="fc1", **conv_args)
    x = feature_max_pool_2d(x, name='fp1', **common_args)
    x = dropout(x, drop_p=0.5, name="pool_dropout2", **common_args)
    x = conv2d(x, 1024, name="fc2", **conv_args)
    x = feature_max_pool_2d(x, name='fp2', **common_args)
    x = conv2d(x, num_classes, name="fc3", **logit_args)
    logits = global_avg_pool(x, name='logits', **pool_args)

    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)
