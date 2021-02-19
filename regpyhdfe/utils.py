import numpy as np
import pandas as pd

def sklearn_to_df(sklearn_dataset):
    """Converts (as well as it can) an sklearn dataset to a Pandas dataframe.

    Args:
       sklearn_dataset (sklearn.utils.Bunch): this parameter is usually the result
            of using sklearn to quickly get a dataset, e.g. the object resulting
            from calling sklearn.load_datasets.load_boston().
    Returns:
        Pandas dataframe df where df['target'] is the target variable in the original
        dataset.
    """
    df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
    df['target'] = pd.Series(sklearn_dataset.target)
    return df

def add_intercept(X):
    """Prepends a column of 1s (an intercept column) to a a 2D numpy array.

    Args:
        X (numpy array): 2D numpy array.
    Returns:
        X with an appended column of 1s. 
    """
    # X has to be a 2D numpy array
    # prepends intercept
    intercept = np.ones(X.shape[0])
    return np.c_[intercept, X]

def get_np_columns(df, columns, intercept=False):
    """Helper used to retreive columns as numpy array.

    Args:
        df (pandas dataframe): dataframe containing desired columns
        columns (list of strings): list of names of desired columns.
                                    Must be a list even if only 1
                                    column is desired.
        intercept (bool): set to True if You'd like resulting numpy array
                            to have a column of 1s appended to it.
    Returns:
        2D numpy array with columns of array consisting of feature vectors,
        i.e. the first column of the result is a numpy vector of the first
        column named in columns argument.

    """
    # dataframe is a pandas datafram
    # columns is a list of column names
    # if intercept is true a column of 1s will be appended to the result matrix
    # returns columns as float64 matrix
    if columns == []:
        return None
    else:
        res = np.expand_dims(a=df[columns[0]].to_numpy().astype('float64'), axis=1)
        if len(columns) > 1:
            for name in columns[1:]:
                res = np.c_[res, np.expand_dims(a=df[name].to_numpy().astype('float64'), axis=1)]
        if intercept:
            res = add_intercept(res)
        return res
