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


# sanity check: cluster standard errors without absorption
#results = smf.ols(formula='wks_work~1', data=df).fit()
# y = np.asarray([[-100, 100, -100, 1234]]).T
# X = np.asarray([[1,2 ,3, 4], [1, 1, 1, 1]]).T
# results = sm.OLS(y, X).fit()
model = smf.ols(formula='ttl_exp~wks_ue', data=df)
results = model.fit()
import pdb; pdb.set_trace()
print(results.predict()[-10:])
print(results.summary())
#results = smf.wls(formula='wks_work~ttl_exp', data=df, weights=np.linspace(1, 13452, 13452)).fit()
model = smf.glm(formula='ttl_exp~wks_ue',
                    freq_weights=np.linspace(1, 13452, 13452),
                    data=df)
results = model.fit()
print(results.summary())
lin_pred = model.mu
target = get_np_columns(df, ['ttl_exp']).squeeze()
resid = target-lin_pred
mse_resid = np.sum(resid**2)/90484876
explained_sum_of_squares = np.sum((target-np.mean(target))**2)-np.sum(resid**2)
#that 1 there is df.model
mse_model = explained_sum_of_squares/1
F = mse_model/mse_resid
print(F)
import pdb; pdb.set_trace()
#print("df_model", results.df_model)
#print("df_resid", results.df_resid)
