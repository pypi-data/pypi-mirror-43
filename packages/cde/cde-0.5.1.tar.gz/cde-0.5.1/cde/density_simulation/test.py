from cde.density_simulation import *
import numpy as np

sim = EconDensity()
X, Y = sim.simulate(10000)
stds = X.std(X)
print(np.mean(stds))