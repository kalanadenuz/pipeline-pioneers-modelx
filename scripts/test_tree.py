from hydropulse.models.regressor import FastRegressionTree
import numpy as np
t = FastRegressionTree()
t.fit(np.random.randn(50, 5), np.random.randn(50))
print('Tree fit OK')
