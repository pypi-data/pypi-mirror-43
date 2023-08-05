
from tensorflow.python.ops.distributions import distribution
from tensorflow.python.ops.distributions import normal
from tensorflow.python.framework import ops
import tensorflow as tf

class KernelDensity():
  """ Kernel density distribution from data. """

  def __init__(self, loc, scale, weight=None, kernel_dist=normal.Normal,
               validate_args=False, allow_nan_stats=True, name="KernelDensity"):
    """ Constructs KernelDensity with kernels centered at `loc`. """

    parameters = locals()
    self.n_locs = loc.shape[0]
    self.n_dim = loc.shape[1]
    with ops.name_scope(name, values=[loc, scale, weight]):
      self._kernel = kernel_dist(loc, scale)
      self.weight_log = tf.Variable(np.log(float(self.n_locs)), dtype=tf.float64)

      self.x_ph = tf.placeholder(tf.float64, shape=(None, self.n_dim))
      x_query = tf.tile(tf.expand_dims(self.x_ph, axis=1), (1, self.n_locs, 1))
      self._log_prob = tf.reduce_logsumexp(tf.reduce_sum(self._kernel._log_prob(x_query), axis=-1)
                                 - self.weight_log, [1],
                                 keep_dims=False)

      self._prob = tf.exp(self._log_prob)


  def pdf(self, X):
    with tf.Session() as sess:
      tf.global_variables_initializer().run()
      return sess.run(self._prob, feed_dict={self.x_ph: X})

if __name__ == "__main__":
  import numpy as np
  import statsmodels.api as sm
  import time

  X = np.random.normal(loc=np.array([-1, 5]), scale=np.array([1, 3]), size=(4000, 2))
  print(X.shape)
  sm_kde = sm.nonparametric.KDEMultivariate(data=X, var_type='cc')

  print(sm_kde.bw)

  kde = KernelDensity(loc=X, scale=sm_kde.bw)

  X_test = np.random.normal(loc=np.array([-1, 5]), scale=np.array([1, 3]), size=(50000, 2))

  t = time.time()
  likelihood2 = kde.pdf(X_test)
  print('TF time:', time.time() - t)

  time.time()
  likelihood1 = sm_kde.pdf(X_test)
  print('SM time:', time.time() - t)

  print(likelihood1-likelihood2)
