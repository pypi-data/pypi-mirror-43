import pandas as pd
import numpy as np


def tabularize(X, return_array=False):
    """
    Helper function to turn nested pandas DataFrames or Series with numpy arrays or pandas Series in cells into tabular
    data with only primitives in cells, i.e. a matrix with the same number of rows as the input data and one column of
    primitive values for each observation in all nested series. For each column, time-series must have the same index.

    Parameters
    ----------
    param X : nested pandas DataFrame or nested Series
    param return_array : boolean
        - If True, returns a numpy array of the tabular data.
        - If False, returns a pandas dataframe with row and column names.

    Returns
    -------
     Xt : pandas DataFrame
        Transformed dataframe in tabular format
    """

    # TODO does not handle dataframes with both nested series columns and standard columns containing only primitives

    if X.ndim == 1:
        Xt = np.array(X.tolist())
    else:
        Xt = np.hstack([col.tolist() for _, col in X.items()])

    if return_array:
        return Xt

    Xt = pd.DataFrame(Xt)
    Xt.index = X.index
    if X.ndim == 1:
        tsindex = X.iloc[0].index if hasattr(X.iloc[0], 'index') else np.arange(X.iloc[0].shape[0])
        columns = [f'{X.name}_{i}' for i in tsindex]
    else:
        columns = []
        for colname, col in X.items():
            tsindex = col.iloc[0].index if hasattr(col.iloc[0], 'index') else np.arange(col.iloc[0].shape[0])
            columns.extend([f'{colname}_{i}' for i in tsindex])
    Xt.columns = columns
    return Xt


tabularise = tabularize


def concat_nested_arrays(arrs, return_arrays=False):
    """
    Helper function to nest tabular arrays from nested list of arrays.

    Parameters
    ----------
    param arrs : list of numpy arrays
        Arrays must have the same number of rows, but can have varying number of columns.
    param return_arrays: boolean
        - If True, return pandas DataFrame with nested numpy arrays.
        - If False, return pandas DataFrame with nested pandas Series.

    Returns
    -------
    Xt : pandas DataFrame
        Transformed dataframe with nested column for each input array.
    """
    if return_arrays:
        Xt = pd.DataFrame(np.column_stack(
            [pd.Series([np.array(vals) for vals in interval])
             for interval in arrs]))
    else:
        Xt = pd.DataFrame(np.column_stack(
            [pd.Series([pd.Series(vals) for vals in interval])
             for interval in arrs]))
    return Xt
