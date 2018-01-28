from __future__ import print_function
import sys
import transform
import numpy as np
import tensorflow as tf


def transform_img(img, model_file, device_t='/gpu:0', batch_size=1):
    g = tf.Graph()
    soft_config = tf.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True

    with g.as_default(), g.device(device_t), tf.Session(config=soft_config) as sess:
        img_shape = img.shape

        batch_shape = (batch_size,) + img_shape

        img_placeholder = tf.placeholder(tf.float32, shape=batch_shape,
                                         name='img_placeholder')

        preds = transform.net(img_placeholder)

        saver = tf.train.Saver()
        saver.restore(sess, model_file)

        X = np.zeros(batch_shape, dtype=np.float32)

        X = np.expand_dims(img, axis=0)

        _preds = sess.run(preds, feed_dict={img_placeholder: X})

        return _preds[0]