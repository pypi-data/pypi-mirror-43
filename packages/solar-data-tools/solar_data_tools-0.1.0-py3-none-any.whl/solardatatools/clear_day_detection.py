# -*- coding: utf-8 -*-
'''Clear Day Detection Module

This module contains functions for detecting clear days in historical PV solar data sets.

'''

import numpy as np
import cvxpy as cvx

def find_clear_days(data, th=0.1):
    '''
    This function quickly finds clear days in a PV power data set. The input to this function is a 2D array containing
    standardized time series power data. This will typically be the output from
    `solardatatools.data_transforms.make_2d`. The filter relies on two estimates of daily "clearness": the smoothness
    of each daily signal as measured by the l2-norm of the 2nd order difference, and seasonally-adjusted daily
    energy. Seasonal adjustment of the daily energy if obtained by solving a local quantile regression problem, which
    is a convex optimization problem and is solvable with cvxpy. The parameter `th` controls the relative weighting of
    the daily smoothness and daily energy in the final filter in a geometric mean. A value of 0 will rely entirely on
    the daily energy and a value of 1 will rely entirely on daily smoothness.

    :param D: A 2D numpy array containing a solar power time series signal.
    :param th: A parameter that tunes the filter between relying of daily smoothness and daily energy
    :return: A 1D boolean array, with `True` values corresponding to clear days in the data set
    '''
    D = data
    # Take the norm of the second different of each day's signal. This gives a rough estimate of the smoothness of
    # day in the data set
    tc = np.linalg.norm(D[:-2] - 2 * D[1:-1] + D[2:], ord=1, axis=0)
    # Shift this metric so the median is at zero
    tc = np.percentile(tc, 50) - tc
    # Normalize such that the maximum value is equal to one
    tc /= np.max(tc)
    # Take the positive part function, i.e. set the negative values to zero. This is the first metric
    tc = np.clip(tc, 0, None)
    # Calculate the daily energy
    de = np.sum(D, axis=0)
    # Solve a convex minimization problem to roughly fit the local 90th percentile of the data (quantile regression)
    x = cvx.Variable(len(tc))
    obj = cvx.Minimize(
        cvx.sum(0.5 * cvx.abs(de - x) + (.9 - 0.5) * (de - x)) + 1e3 * cvx.norm(cvx.diff(x, k=2)))
    prob = cvx.Problem(obj)
    try:
        prob.solve(solver='MOSEK')
    except Exception as e:
        print(e)
        print('Trying ECOS solver')
        prob.solve(solver='ECOS')
    # x gives us the local top 90th percentile of daily energy, i.e. the very sunny days. This gives us our
    # seasonal normalization.
    de = np.clip(np.divide(de, x.value), 0, 1)
    # Take geometric mean
    weights = np.multiply(np.power(tc, th), np.power(de, 1.-th))
    # Finally, set values less than 0.6 to be equal to zero
    weights[weights < 0.6] = 0.
    return weights >= 1e-3