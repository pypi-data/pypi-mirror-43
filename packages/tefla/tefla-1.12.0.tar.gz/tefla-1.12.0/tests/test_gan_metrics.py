"""Tests for GAN metrics."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile
import tempfile

import numpy as np
import tensorflow as tf
from scipy import linalg as scp_linalg

from google.protobuf import text_format

from tefla.core import gan_metrics

mock = tf.test.mock


def _numpy_softmax(x):
  e_x = np.exp(x - np.max(x, axis=1)[:, None])
  return e_x / np.sum(e_x, axis=1)[:, None]


def _expected_inception_score(logits):
  p = _numpy_softmax(logits)
  q = np.expand_dims(np.mean(p, 0), 0)
  per_example_logincscore = np.sum(p * (np.log(p) - np.log(q)), 1)
  return np.exp(np.mean(per_example_logincscore))


def _expected_fid(real_imgs, gen_imgs):
  m = np.mean(real_imgs, axis=0)
  m_v = np.mean(gen_imgs, axis=0)
  sigma = np.cov(real_imgs, rowvar=False)
  sigma_v = np.cov(gen_imgs, rowvar=False)
  sqcc = scp_linalg.sqrtm(np.dot(sigma, sigma_v))
  mean = np.square(m - m_v).sum()
  trace = np.trace(sigma + sigma_v - 2 * sqcc)
  fid = mean + trace
  return fid


def _expected_trace_sqrt_product(sigma, sigma_v):
  return np.trace(scp_linalg.sqrtm(np.dot(sigma, sigma_v)))


# A dummy GraphDef string with the minimum number of Ops.
graphdef_string = """
node {
  name: "Mul"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 299
        }
        dim {
          size: 299
        }
        dim {
          size: 3
        }
      }
    }
  }
}
node {
  name: "logits"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 1001
        }
      }
    }
  }
}
node {
  name: "pool_3"
  op: "Placeholder"
  attr {
    key: "dtype"
    value {
      type: DT_FLOAT
    }
  }
  attr {
    key: "shape"
    value {
      shape {
        dim {
          size: -1
        }
        dim {
          size: 2048
        }
      }
    }
  }
}
versions {
  producer: 24
}
"""


def _get_dummy_graphdef():
  dummy_graphdef = tf.GraphDef()
  text_format.Merge(graphdef_string, dummy_graphdef)
  return dummy_graphdef


def _run_with_mock(function, *args, **kwargs):
  with mock.patch.object(gan_metrics, 'get_graph_def_from_url_tarball') as mock_tarball_getter:
    mock_tarball_getter.return_value = _get_dummy_graphdef()
    return function(*args, **kwargs)


class ClassifierMetricsTest(tf.test.TestCase):

  def test_run_inception_graph(self):
    """Test `run_inception` graph construction."""
    batch_size = 7
    img = tf.ones([batch_size, 299, 299, 3])
    logits = _run_with_mock(gan_metrics.run_inception, img)

    self.assertTrue(isinstance(logits, tf.Tensor))
    logits.shape.assert_is_compatible_with([batch_size, 1001])

    # Check that none of the model variables are trainable.
    self.assertListEqual([], tf.trainable_variables())

  def test_run_inception_graph_pool_output(self):
    """Test `run_inception` graph construction with pool output."""
    batch_size = 3
    img = tf.ones([batch_size, 299, 299, 3])
    pool = _run_with_mock(
        gan_metrics.run_inception, img, output_tensor=gan_metrics.INCEPTION_FINAL_POOL)

    self.assertTrue(isinstance(pool, tf.Tensor))
    pool.shape.assert_is_compatible_with([batch_size, 2048])

    # Check that none of the model variables are trainable.
    self.assertListEqual([], tf.trainable_variables())

  def test_inception_score_graph(self):
    """Test `inception_score` graph construction."""
    score = _run_with_mock(gan_metrics.inception_score, tf.zeros([6, 299, 299, 3]), num_batches=3)
    self.assertTrue(isinstance(score, tf.Tensor))
    score.shape.assert_has_rank(0)

    # Check that none of the model variables are trainable.
    self.assertListEqual([], tf.trainable_variables())

  def test_frechet_inception_distance_graph(self):
    """Test `frechet_inception_distance` graph construction."""
    img = tf.ones([7, 299, 299, 3])
    distance = _run_with_mock(gan_metrics.frechet_inception_distance, img, img)

    self.assertTrue(isinstance(distance, tf.Tensor))
    distance.shape.assert_has_rank(0)

    # Check that none of the model variables are trainable.
    self.assertListEqual([], tf.trainable_variables())

  def test_run_inception_multicall(self):
    """Test that `run_inception` can be called multiple times."""
    for batch_size in (7, 3, 2):
      img = tf.ones([batch_size, 299, 299, 3])
      _run_with_mock(gan_metrics.run_inception, img)

  def test_invalid_input(self):
    """Test that functions properly fail on invalid input."""
    with self.assertRaisesRegexp(ValueError, 'Shapes .* are incompatible'):
      gan_metrics.run_inception(tf.ones([7, 50, 50, 3]))

    p = tf.zeros([8, 10])
    p_logits = tf.zeros([8, 10])
    q = tf.zeros([10])
    with self.assertRaisesRegexp(ValueError, 'must be floating type'):
      gan_metrics._kl_divergence(tf.zeros([8, 10], dtype=tf.int32), p_logits, q)

    with self.assertRaisesRegexp(ValueError, 'must be floating type'):
      gan_metrics._kl_divergence(p, tf.zeros([8, 10], dtype=tf.int32), q)

    with self.assertRaisesRegexp(ValueError, 'must be floating type'):
      gan_metrics._kl_divergence(p, p_logits, tf.zeros([10], dtype=tf.int32))

    with self.assertRaisesRegexp(ValueError, 'must have rank 2'):
      gan_metrics._kl_divergence(tf.zeros([8]), p_logits, q)

    with self.assertRaisesRegexp(ValueError, 'must have rank 2'):
      gan_metrics._kl_divergence(p, tf.zeros([8]), q)

    with self.assertRaisesRegexp(ValueError, 'must have rank 1'):
      gan_metrics._kl_divergence(p, p_logits, tf.zeros([10, 8]))

  def test_inception_score_value(self):
    """Test that `inception_score` gives the correct value."""
    logits = np.array([np.array([1, 2] * 500 + [4]), np.array([4, 5] * 500 + [6])])
    unused_image = tf.zeros([2, 299, 299, 3])
    incscore = _run_with_mock(gan_metrics.inception_score, unused_image)

    with self.test_session(use_gpu=True) as sess:
      incscore_np = sess.run(incscore, {'concat:0': logits})

    self.assertAllClose(_expected_inception_score(logits), incscore_np)

  def test_frechet_classifier_distance_value(self):
    """Test that `frechet_classifier_distance` gives the correct value."""
    np.random.seed(0)

    # Make num_examples > num_features to ensure scipy's sqrtm function
    # doesn't return a complex matrix.
    test_pool_real_a = np.float32(np.random.randn(512, 256))
    test_pool_gen_a = np.float32(np.random.randn(512, 256))

    fid_op = _run_with_mock(
        gan_metrics.frechet_classifier_distance,
        test_pool_real_a,
        test_pool_gen_a,
        classifier_fn=lambda x: x)

    with self.test_session() as sess:
      actual_fid = sess.run(fid_op)

    expected_fid = _expected_fid(test_pool_real_a, test_pool_gen_a)

    self.assertAllClose(expected_fid, actual_fid, 0.0001)

  def test_trace_sqrt_product_value(self):
    """Test that `trace_sqrt_product` gives the correct value."""
    np.random.seed(0)

    # Make num_examples > num_features to ensure scipy's sqrtm function
    # doesn't return a complex matrix.
    test_pool_real_a = np.float32(np.random.randn(512, 256))
    test_pool_gen_a = np.float32(np.random.randn(512, 256))

    cov_real = np.cov(test_pool_real_a, rowvar=False)
    cov_gen = np.cov(test_pool_gen_a, rowvar=False)

    trace_sqrt_prod_op = _run_with_mock(gan_metrics.trace_sqrt_product, cov_real, cov_gen)

    with self.test_session() as sess:
      # trace_sqrt_product: tsp
      actual_tsp = sess.run(trace_sqrt_prod_op)

    expected_tsp = _expected_trace_sqrt_product(cov_real, cov_gen)

    self.assertAllClose(actual_tsp, expected_tsp, 0.01)

  def test_preprocess_image_graph(self):
    """Test `preprocess_image` graph construction."""
    incorrectly_sized_image = tf.zeros([520, 240, 3])
    correct_image = gan_metrics.preprocess_image(images=incorrectly_sized_image)
    _run_with_mock(gan_metrics.run_inception, tf.expand_dims(correct_image, 0))

  def test_get_graph_def_from_url_tarball(self):
    """Test `get_graph_def_from_url_tarball`."""
    # Write dummy binary GraphDef to tempfile.
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
      tmp_file.write(_get_dummy_graphdef().SerializeToString())
    relative_path = os.path.relpath(tmp_file.name)

    # Create gzip tarball.
    tar_dir = tempfile.mkdtemp()
    tar_filename = os.path.join(tar_dir, 'tmp.tar.gz')
    with tarfile.open(tar_filename, 'w:gz') as tar:
      tar.add(relative_path)

    with mock.patch.object(gan_metrics, 'urllib') as mock_urllib:
      mock_urllib.request.urlretrieve.return_value = tar_filename, None
      graph_def = gan_metrics.get_graph_def_from_url_tarball('unused_url', relative_path)

    self.assertIsInstance(graph_def, tf.GraphDef)
    self.assertEqual(_get_dummy_graphdef(), graph_def)


if __name__ == '__main__':
  tf.test.main()
