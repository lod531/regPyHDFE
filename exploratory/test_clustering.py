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
#results = smf.ols(formula='ttl_exp~wks_ue', data=df).fit()
# results = results.get_robustcov_results(cov_type='cluster',
#                                         groups=get_np_columns(df, ['idcode']))
# print(np.sum(results.resid))
# import pdb; pdb.set_trace()
pyreghdfe = Pyreghdfe(df=df,
                        target='hours_log',
                        predictors=['union'],
                        ids=['year'], 
                        cluster_ids=['idcode'])
results = pyreghdfe.fit(cov_type='cluster', groups=['idcode'])

# . reghdfe hours_log union, absorb(year idcode) cluster(idcode)
# variable hours_log not found
# r(111);
# 
# . gen hours_log = log(hours)
# 
# . reghdfe hours_log union, absorb(year idcode) cluster(idcode)
# (dropped 884 singleton observations)
# (MWFE estimator converged in 8 iterations)
# 
# HDFE Linear regression                            Number of obs   =     12,568
# Absorbing 2 HDFE groups                           F(   1,   3101) =      43.38
# Statistics robust to heteroskedasticity           Prob > F        =     0.0000
#                                                   R-squared       =     0.5333
#                                                   Adj R-squared   =     0.3795
#                                                   Within R-sq.    =     0.0069
# Number of clusters (idcode)  =      3,102         Root MSE        =     0.3351
# 
#                              (Std. Err. adjusted for 3,102 clusters in idcode)
# ------------------------------------------------------------------------------
#              |               Robust
#    hours_log |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
# -------------+----------------------------------------------------------------
#        union |   .0922909   .0140118     6.59   0.000     .0648175    .1197643
#        _cons |   3.505433   .0032499  1078.63   0.000     3.499061    3.511805
# ------------------------------------------------------------------------------
# 
# Absorbed degrees of freedom:
# -----------------------------------------------------+
#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
# -------------+---------------------------------------|
#         year |        12           0          12     |
#       idcode |      3102        3102           0    *|
# -----------------------------------------------------+
# * = FE nested within cluster; treated as redundant for DoF computation


print(results.summary())
#print("df_model", results.df_model)
#print("df_resid", results.df_resid)
