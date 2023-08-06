"""
This is a module containing time series regressors
"""
import numpy as np
import pandas as pd
from sklearn.utils.validation import check_is_fitted
from sktime.utils.validation import check_ts_X_y, check_ts_array
from sklearn.ensemble import RandomForestRegressor
from sktime.regressors.base import BaseRegressor


class TSDummyRegressor(BaseRegressor):
    """ A dummy regressor to be used as a reference implementation.

    Parameters
    ----------
    strategy : str, default='constant'
        A parameter defining the prediction strategy of the dummy regressor
        constant: always predicts the constant value supplied
        average: predicts the average of training targets
    constant : float, default="42.0"
        The parameter to be always predicted, if that's the strategy
    """

    def __init__(self, strategy='constant', constant=42.0):
        self.strategy = strategy
        self.constant = constant

    def fit(self, X, y):
        """ A reference implementation of a fitting function.

        Parameters
        ----------
        X : array-like, pandas DataFrame or Series, shape (n_samples, ...)
            The training input samples.
        y : array-like, pandas dataFrame series, shape (n_samples,)
            The target values (class labels in classification)

        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_ts_X_y(X, y)
        # fitting (finding the value of dummy prediction theta_) the model based on strategy
        if self.strategy == 'constant':
            self.theta_ = self.constant
        elif self.strategy == 'average':
            self.theta_ = np.mean(y)
        else:
            raise ValueError('Unknown Strategy')
        # let the model know that it is fitted
        self.is_fitted_ = True
        # `fit` should always return `self`
        return self

    def predict(self, X):
        """ A reference implementation of a predicting function.

        Parameters
        ----------
        X : array-like, pandas DataFrame or Series, shape (n_samples, ...)
            The training input samples.
        Returns
        -------
        y : ndarray, shape (n_samples,)
            Returns the dummy predictions
        """
        X = check_ts_array(X)
        check_is_fitted(self, 'is_fitted_')
        return np.ones(X.shape[0], dtype=np.int64) * self.theta_


class TSExampleRegressor(BaseRegressor):
    """ An example regressor that makes use of the xpandas input.
    """

    def __init__(self, func=np.mean, columns=None, estimator=RandomForestRegressor()):
        self.func = func
        self.columns = columns
        self.estimator = estimator

    def fit(self, X, y):
        """ A reference implementation of a fitting function.

        Parameters
        ----------
        X : array-like, pandas DataFrame or Series, shape (n_samples, ...)
            The training input samples.
        y : array-like, pandas dataFrame series, shape (n_samples,)
            The target values (class labels in classification)

        Returns
        -------
        self : object
            Returns self.
        """

        # simple feature extraction
        X = pd.DataFrame([X[col].apply(self.func) for col in self.columns]).T

        X, y = check_ts_X_y(X, y)
        # fitting (finding the value of dummy prediction theta_) the model based on strategy

        # fitting
        self.estimator.fit(X, y)

        # let the model know that it is fitted
        self.is_fitted_ = True
        # `fit` should always return `self`
        return self

    def predict(self, X):
        """ A reference implementation of a predicting function.

        Parameters
        ----------
        X : array-like, pandas DataFrame or Series, shape (n_samples, ...)
            The training input samples.
        Returns
        -------
        y : ndarray, shape (n_samples,)
            Returns the dummy predictions
        """
        X = pd.DataFrame([X[col].apply(self.func) for col in self.columns]).T

        X = check_ts_array(X)

        check_is_fitted(self, 'is_fitted_')

        return self.estimator.predict(X)
