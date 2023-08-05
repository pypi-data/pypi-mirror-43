from cde.density_simulation.EconDensity import EconDensity
from cde.density_estimator import *
import tensorflow as tf
from cde.evaluation.plotting import *


density = EconDensity(heteroscedastic=True, random_seed=2)
X, Y = density.simulate(n_samples=1600)

with tf.Session():
  model = NN("MDN", 1, 1, n_centers=20, y_noise_std=None, x_noise_std=None, random_seed=2)
  model.fit(X, Y)

  comparison_plot2d_sim_est(model, density, x_cond=[0.5, 2.0])

