import pandas as pd
import pyhdfe
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from linearmodels.iv.absorbing import AbsorbingLS
import pyhdfe
from utils import add_intercept, get_np_columns


from sklearn.datasets import load_boston

def sklearn_to_df(sklearn_dataset):
    df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
    df['target'] = pd.Series(sklearn_dataset.target)
    return df

#0  CRIM per capita crime rate by town
#1  ZN proportion of residential land zoned for lots over 25,000 sq.ft.
#2  INDUS proportion of non-retail business acres per town
#3  CHAS Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#4  NOX nitric oxides concentration (parts per 10 million)
#5  RM average number of rooms per dwelling
#6  AGE proportion of owner-occupied units built prior to 1940
#7  DIS weighted distances to five Boston employment centres
#8  RAD index of accessibility to radial highways
#9  TAX full-value property-tax rate per $10,000
#10 PTRATIO pupil-teacher ratio by town
#11 B 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
#12 LSTAT % lower status of the population
#13 target Median value of owner-occupied homes in $1000’s
df = sklearn_to_df(load_boston())

df.to_stata("boston.dta")
print(list(df))

# results = smf.ols(formula='target~CRIM + ZN + INDUS + NOX + AGE', data=df).fit()
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                 target   R-squared:                       0.294
# Model:                            OLS   Adj. R-squared:                  0.287
# Method:                 Least Squares   F-statistic:                     41.72
# Date:                Sun, 06 Dec 2020   Prob (F-statistic):           6.69e-36
# Time:                        14:18:02   Log-Likelihood:                -1752.0
# No. Observations:                 506   AIC:                             3516.
# Df Residuals:                     500   BIC:                             3541.
# Df Model:                           5
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept     28.8476      2.282     12.644      0.000      24.365      33.330
# CRIM          -0.2423      0.045     -5.391      0.000      -0.331      -0.154
# ZN             0.0553      0.019      2.950      0.003       0.018       0.092
# INDUS         -0.3796      0.082     -4.622      0.000      -0.541      -0.218
# NOX           -3.0646      5.340     -0.574      0.566     -13.557       7.428
# AGE           -0.0021      0.019     -0.107      0.915      -0.040       0.036
# ==============================================================================
# Omnibus:                      199.582   Durbin-Watson:                   0.750
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              705.755
# Skew:                           1.838   Prob(JB):                    5.59e-154
# Kurtosis:                       7.467   Cond. No.                     1.24e+03
# ==============================================================================
# print(results.summary())

# Sanity check passes 

# . reghdfe target CRIM ZN INDUS NOX AGE, absorb(CHAS RAD)
# (MWFE estimator converged in 3 iterations)
# 
# HDFE Linear regression                            Number of obs   =        506
# Absorbing 2 HDFE groups                           F(   5,    491) =      21.93
#                                                   Prob > F        =     0.0000
#                                                   R-squared       =     0.3887
#                                                   Adj R-squared   =     0.3712
#                                                   Within R-sq.    =     0.1825
#                                                   Root MSE        =     7.2929
# 
# ------------------------------------------------------------------------------
#       target |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
# -------------+----------------------------------------------------------------
#         CRIM |  -.2089114   .0491012    -4.25   0.000    -.3053857   -.1124371
#           ZN |   .0679261   .0183051     3.71   0.000       .03196    .1038922
#        INDUS |  -.2279553   .0860909    -2.65   0.008    -.3971074   -.0588033
#          NOX |  -9.424849   5.556005    -1.70   0.090    -20.34133     1.49163
#          AGE |  -.0140739   .0183467    -0.77   0.443    -.0501215    .0219738
#        _cons |   31.24755    2.53596    12.32   0.000     26.26487    36.23022
# ------------------------------------------------------------------------------
# 
# Absorbed degrees of freedom:
# -----------------------------------------------------+
#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
# -------------+---------------------------------------|
#         CHAS |         2           0           2     |
#          RAD |         9           1           8     |
# -----------------------------------------------------+

# target~CRIM + ZN + INDUS + NOX + AGE, absorb(CHAS, RAD)
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                      y   R-squared:                       0.183
# Model:                            OLS   Adj. R-squared:                  0.174
# Method:                 Least Squares   F-statistic:                     22.33
# Date:                Sun, 06 Dec 2020   Prob (F-statistic):           3.14e-20
# Time:                        14:58:02   Log-Likelihood:                -1715.7
# No. Observations:                 506   AIC:                             3443.
# Df Residuals:                     500   BIC:                             3469.
# Df Model:                           5                                         
# Covariance Type:            nonrobust                                         
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# x1            -0.2089      0.049     -4.294      0.000      -0.305      -0.113
# x2             0.0679      0.018      3.745      0.000       0.032       0.104
# x3            -0.2280      0.085     -2.672      0.008      -0.396      -0.060
# x4            -9.4248      5.506     -1.712      0.088     -20.242       1.392
# x5            -0.0141      0.018     -0.774      0.439      -0.050       0.022
# const      -6.592e-17      0.321  -2.05e-16      1.000      -0.631       0.631
# ==============================================================================
# Omnibus:                      172.457   Durbin-Watson:                   0.904
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              532.297
# Skew:                           1.621   Prob(JB):                    2.59e-116
# Kurtosis:                       6.839   Cond. No.                         480.
# ==============================================================================
# algo = pyhdfe.create(get_np_columns(df, ['CHAS', 'RAD'], False))
# 
# residualized = algo.residualize(get_np_columns(df, ['target', 'CRIM', 'ZN', 'INDUS', 'NOX', 'AGE'], False))
# model = sm.OLS(residualized[:,0], add_intercept(residualized[:, [1, 2, 3, 4, 5]]))
# results = model.fit()
# print("target~CRIM + ZN + INDUS + NOX + AGE, absorb(CHAS, RAD)")
# print(results.summary())
print(np.mean(get_np_columns(df, ['target'], False)))
