import pandas as pd
from tensorflow import keras
import pyhdfe
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from linearmodels.iv.absorbing import AbsorbingLS
import pyhdfe
from utils import add_intercept, get_np_columns


from sklearn.datasets import load_boston

# details about dataset can be found at https://www.kaggle.com/crawford/80-cereals
df = pd.read_csv('/home/abom/Downloads/dataset_cereal/cereal.csv')

print(list(df))

#results = smf.ols(formula='rating ~ fat + protein + carbo + sugars', data=df).fit()
#print(results.summary())

print(get_np_columns(df, ['cups'], False)[:10])


algo = pyhdfe.create(get_np_columns(df, ['shelf'], False))

#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                      y   R-squared:                       0.759
# Model:                            OLS   Adj. R-squared:                  0.745
# Method:                 Least Squares   F-statistic:                     56.55
# Date:                Mon, 07 Dec 2020   Prob (F-statistic):           1.71e-21
# Time:                        09:15:25   Log-Likelihood:                -252.82
# No. Observations:                  77   AIC:                             515.6
# Df Residuals:                      72   BIC:                             527.4
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# x1            -5.6842      0.868     -6.550      0.000      -7.414      -3.954
# x2             3.7404      0.831      4.500      0.000       2.083       5.397
# x3            -0.7892      0.201     -3.920      0.000      -1.191      -0.388
# x4            -2.0329      0.215     -9.459      0.000      -2.461      -1.604
# const        1.36e-15      0.760   1.79e-15      1.000      -1.516       1.516
# ==============================================================================
# Omnibus:                        5.613   Durbin-Watson:                   1.801
# Prob(Omnibus):                  0.060   Jarque-Bera (JB):                7.673
# Skew:                           0.179   Prob(JB):                       0.0216
# Kurtosis:                       4.504   Cond. No.                         5.84
# ==============================================================================

# . reghdfe rating fat protein carbo sugars, absorb(shelf)
# (MWFE estimator converged in 1 iterations)
# 
# HDFE Linear regression                            Number of obs   =         77
# Absorbing 1 HDFE group                            F(   4,     70) =      54.98
#                                                   Prob > F        =     0.0000
#                                                   R-squared       =     0.7862
#                                                   Adj R-squared   =     0.7679
#                                                   Within R-sq.    =     0.7586
#                                                   Root MSE        =     6.7671
# 
# ------------------------------------------------------------------------------
#       rating |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
# -------------+----------------------------------------------------------------
#          fat |  -5.684196   .8801468    -6.46   0.000    -7.439594   -3.928799
#      protein |   3.740386   .8430319     4.44   0.000     2.059012     5.42176
#        carbo |  -.7892276   .2041684    -3.87   0.000    -1.196429   -.3820266
#       sugars |   -2.03286   .2179704    -9.33   0.000    -2.467588   -1.598132
#        _cons |   64.49503    4.92674    13.09   0.000     54.66896     74.3211
# ------------------------------------------------------------------------------
# 
# Absorbed degrees of freedom:
# -----------------------------------------------------+
#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
# -------------+---------------------------------------|
#        shelf |         3           0           3     |
# -----------------------------------------------------+


residualized = algo.residualize(get_np_columns(df, ['rating', 'fat', 'protein', 'carbo', 'sugars'], False))
model = sm.OLS(residualized[:,0], add_intercept(residualized[:, [1, 2, 3, 4]]))
results = model.fit()
print("rating ~ fat + protein + carbo + sugars, absorb(shelf)")
print(results.summary())
