from pyreghdfe import Pyreghdfe
from sklearn.datasets import load_boston
from utils import sklearn_to_df
import pandas as pd
import numpy as np
from utils import get_np_columns
import statsmodels.formula.api as smf
import econtools
import econtools.metrics as mt
import statsmodels.api as sm

df = pd.read_stata('data/cleaned_nlswork.dta')
df['hours_log'] = np.log(df['hours'])
pyreghdfe = Pyreghdfe(df=df,
                        target='ttl_exp',
                        predictors=['wks_ue', 'tenure'],
                        ids=['idcode'],
                        cluster_ids=['idcode'])

results = pyreghdfe.fit()
#results = pyreghdfe.fit(cov_type='cluster', groups=['idcode'])

print(results.summary())
#print("params")
#print(results.params)
#print(results.resid[-10:])
#print(np.sum(results.resid))
#print("df_model", results.df_model)
#print("df_resid", results.df_resid)
