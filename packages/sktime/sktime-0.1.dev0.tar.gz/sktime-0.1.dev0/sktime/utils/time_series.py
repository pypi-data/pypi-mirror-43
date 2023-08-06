import numpy as np
from sklearn.utils.validation import check_random_state


def rand_intervals_rand_n(x, random_state=None):
    """
    Computes a random number of intervals from index (x) with
    random starting points and lengths. Intervals are unique, but may overlap.

    param x : array_like, shape = [n_observations]
    param random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    return : array-like, shape = [n, 2]
        2d array containing start and end points of intervals


    References
    ----------
    [1] Deng, Houtao, et al. "A time series forest for classification and feature extraction."
    Information Sciences 239 (2013): 142-153.


    See also
    --------
    rand_intervals_fixed_n
    """

    rng = check_random_state(random_state)
    starts = []
    ends = []
    m = x.shape[0]  # series length
    W = rng.randint(1, m, size=int(np.sqrt(m)))
    for w in W:
        size = m - w + 1
        start = rng.randint(size, size=int(np.sqrt(size)))
        starts.extend(start)
        for s in start:
            end = s + w
            ends.append(end)
    return np.column_stack([starts, ends])


def rand_intervals_fixed_n(x, n='sqrt', min_length=1, random_state=None):
    """
    Computes a fixed number (n) of intervals from index (x) with
    random starting points and lengths. Intervals may overlap and may not be unique.

    param x : array_like, shape = [n_observations]
        Array containing the time-series index.
    param n : 'sqrt' or int
        Number of random intervals to compute.

        - If int, n random intervals are generated.
        - If 'sqrt', int(sqrt(m)) intervals are generated where m is the length of the time-series.

        The default is 'sqrt'.
    param random_state : int, RandomState instance or None, optional (default=None)

        - If int, random_state is the seed used by the random number generator;
        - If RandomState instance, random_state is the random number generator;
        - If None, the random number generator is the RandomState instance used by `np.random`.

    return : array-like, shape = [n, 2]
        2d array containing start and end points of intervals


    See also
    --------
    rand_intervals_rand_n
    """

    rng = check_random_state(random_state)

    m = x.size  # series length
    if n == 'sqrt':
        n = int(np.sqrt(m))  # number of random intervals
    elif not (np.issubdtype(type(n), np.integer) and (n > 0)):
        raise ValueError(f'n must be either "sqrt" or positive integer, but found {type(n)}')

    starts = rng.randint(m - min_length + 1, size=n)

    if n == 1:
        starts = [starts]  # make it an iterable

    ends = [start + rng.randint(min_length, m - start + 1) for start in starts]
    return np.column_stack([starts, ends])


def time_series_slope(y, axis=0):
    """
    Compute slope of time series (y) using ordinary least squares.

    :param y : array_like
        Time-series.
    :param axis : int
        Axis along which the time-series slope is computed.
    :return : float
        Slope of time-series.
    """

    n, m = np.atleast_2d(y).shape
    if m < 2:
        return np.zeros(n) if n > 1 else 0
    else:
        x = np.arange(m) + 1
        x_mean = (m + 1) / 2  # x.mean()
        return (np.mean(x * y, axis=axis) - x_mean * np.mean(y, axis=axis)) / (np.mean(x ** 2) - x_mean ** 2)

