from __future__ import division, print_function, absolute_import
import tensorflow as tf

from tefla.core import initializers as initz
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import dropout, rms_pool_2d, feature_max_pool_1d
from tefla.core.layers import input, conv2d, fully_connected, max_pool, prelu, softmax

# sizes - (width, height)
image_size = (512, 512)
crop_size = (448, 448)


def model(is_training, reuse):
    common_args = common_layer_args(is_training, reuse, trainable=False)
    common_args_finetune = common_layer_args(is_training, reuse, trainable=True)
    conv_args = make_args(batch_norm=True, activation=prelu, w_init=initz.he_normal(scale=1), untie_biases=True, **common_args)
    conv_args_finetune = make_args(batch_norm=True, activation=prelu, w_init=initz.he_normal(scale=1), untie_biases=True, **common_args_finetune)
    fc_args = make_args(activation=prelu, w_init=initz.he_normal(scale=1), **common_args_finetune)
    logit_args = make_args(activation=None, w_init=initz.he_normal(scale=1), **common_args_finetune)
    pred_args = make_args(activation=prelu, w_init=initz.he_normal(scale=1), **common_args_finetune)
    pool_args = make_args(padding='SAME', **common_args)

    x = input((None, crop_size[1], crop_size[0], 3), **common_args)
    x = conv2d(x, 32, filter_size=(5, 5), stride=(2, 2), name="conv1_1", **conv_args)
    x = conv2d(x, 48, stride=(2, 2), name="conv1_2", **conv_args)
    x = conv2d(x, 48, name="conv1_3", **conv_args)
    x = conv2d(x, 48, name="conv1_4", **conv_args_finetune)
    # 128
    x = conv2d(x, 64, stride=(2, 2), name="conv2_1", **conv_args)
    x = conv2d(x, 64, name="conv2_2", **conv_args_finetune)
    x = conv2d(x, 64, name="conv2_3", **conv_args_finetune)
    # 64
    x = conv2d(x, 80, stride=(2, 2), name="conv3_1", **conv_args_finetune)
    x = conv2d(x, 80, name="conv3_2", **conv_args_finetune)
    x = conv2d(x, 80, name="conv3_3", **conv_args_finetune)
    x_1 = conv2d(x, 80, name="conv3_4", **conv_args_finetune)
    # 32
    x = conv2d(x_1, 128, stride=(2, 2), name="conv4_1", **conv_args_finetune)
    x = conv2d(x, 128, name="conv4_2", **conv_args_finetune)
    x = conv2d(x, 128, name="conv4_3", **conv_args_finetune)
    x_2 = conv2d(x, 128, name="conv4_4", **conv_args_finetune)
    # 16
    x = conv2d(x_2, 192, stride=(2, 2), padding='SAME', name="conv5_1", **conv_args_finetune)
    x = conv2d(x, 192, name="conv5_2", **conv_args_finetune)
    x = conv2d(x, 192, name="conv5_3", **conv_args_finetune)
    x_3 = conv2d(x, 192, name="conv5_4", **conv_args_finetune)
    # Skip
    x_4 = max_pool(x_1, filter_size=(4, 4), stride=(4, 4), name="skip_pool1", **pool_args)
    x_5 = max_pool(x_2, filter_size=(3, 3), stride=(2, 2), name="skip_pool2", **pool_args)
    x = tf.concat([x_3, x_4, x_5], 3)
    x = rms_pool_2d(x, filter_size=(3, 3), stride=(2, 2), name="rms_pool1", **pool_args)
    # 4
    x = dropout(x, drop_p=0.5, name="pool_dropout1", **common_args)
    x = fully_connected(x, n_output=1024, name="fc1", **fc_args)
    x = feature_max_pool_1d(x, name='fp1', **common_args)
    x = dropout(x, drop_p=0.5, name="pool_dropout2", **common_args)
    x = fully_connected(x, n_output=1024, name="fc2", **fc_args)
    x = feature_max_pool_1d(x, name='fp2', **common_args)
    logits = fully_connected(x, n_output=5, name="logits", **logit_args)

    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)
