import numpy as np
import pandas as pd

def sklearn_to_df(sklearn_dataset):
    df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
    df['target'] = pd.Series(sklearn_dataset.target)
    return df

def add_intercept(X):
    # X has to be a 2D numpy array
    # appends intercept as the last column
    intercept = np.ones(X.shape[0])
    return np.c_[X, intercept]

def get_np_columns(df, columns, intercept=False):
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
