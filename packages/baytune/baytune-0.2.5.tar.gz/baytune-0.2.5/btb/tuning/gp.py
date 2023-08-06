from __future__ import division

import logging

import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor

from btb.tuning.tuner import BaseTuner
from btb.tuning.uniform import Uniform

logger = logging.getLogger('btb')


class GP(BaseTuner):
    """GP tuner

    Args:
        r_minimum (int): the minimum number of past results this selector needs in order to use
            gaussian process for prediction. If not enough results are present during a ``fit``,
            subsequent calls to ``propose`` will revert to uniform selection.
    """

    def __init__(self, tunables, gridding=0, r_minimum=2):
        super(GP, self).__init__(tunables, gridding=gridding)
        self.r_minimum = r_minimum

    def fit(self, X, y):
        super(GP, self).fit(X, y)

        # skip training the process if there aren't enough samples
        if X.shape[0] < self.r_minimum:
            return

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        if y.ndim == 1:
            y = y.reshape(-1, 1)

        self.gp = GaussianProcessRegressor(normalize_y=True)
        self.gp.fit(X, y)

    def predict(self, X):
        if self.X.shape[0] < self.r_minimum:
            # we probably don't have enough
            logger.info('Using Uniform sampler as user specified r_minimum '
                        'threshold is not met to start the GP based learning')
            return Uniform(self.tunables).predict(X)

        y, stdev = self.gp.predict(X, return_std=True)
        return np.array(list(zip(y, stdev)))

    def _acquire(self, predictions):
        """
        Predictions from the GP will be in the form (prediction, error).
        The default acquisition function returns the index with the highest
        predicted value, not factoring in error.
        """
        return np.argmax(predictions[:, 0])


class GPEi(GP):
    """GPEi tuner

    The expected improvement criterion encodes a tradeoff between exploitation (points with high
    mean) and exploration (points with high uncertainty).

    See also::

        http://www.cs.toronto.edu/~kswersky/wp-content/uploads/nips2013transfer.pdf
        https://www.cse.wustl.edu/~garnett/cse515t/spring_2015/files/lecture_notes/12.pdf
    """

    def _acquire(self, predictions):
        Phi = norm.cdf
        N = norm.pdf

        mu, sigma = predictions.T
        y_best = np.max(self.y)

        # because we are maximizing the scores, we do mu-y_best rather than the inverse, as is
        # shown in most reference materials
        z = (mu - y_best) / sigma

        ei = sigma * (z * Phi(z) + N(z))

        return np.argmax(ei)


class GPEiVelocity(GPEi):
    """GCPEiVelocity tuner"""

    MULTIPLIER = -100   # magic number; modify with care
    N_BEST_Y = 5        # number of top values w/w to compute velocity

    def fit(self, X, y):
        """
        Train a gaussian process like normal, then compute a "Probability Of
        Uniform selection" (POU) value.
        """
        # first, train a gaussian process like normal
        super(GPEiVelocity, self).fit(X, y)

        # probability of uniform
        self.POU = 0
        if len(y) >= self.r_minimum:
            # get the best few scores so far, and compute the average distance
            # between them.
            top_y = sorted(y)[-self.N_BEST_Y:]
            velocities = [top_y[i + 1] - top_y[i] for i in range(len(top_y) - 1)]

            # the probability of returning random parameters scales inversely with
            # the "velocity" of top scores.
            self.POU = np.exp(self.MULTIPLIER * np.mean(velocities))

    def predict(self, X):
        """
        Use the POU value we computed in fit to choose randomly between GPEi and
        uniform random selection.
        """
        if np.random.random() < self.POU:
            # choose params at random to avoid local minima
            return Uniform(self.tunables).predict(X)

        return super(GPEiVelocity, self).predict(X)
