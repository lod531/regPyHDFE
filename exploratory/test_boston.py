from pyreghdfe import Pyreghdfe
from sklearn.datasets import load_boston
from utils import sklearn_to_df

df = sklearn_to_df(load_boston())

pyreghdfe = Pyreghdfe(target='target',
                        predictors=['CRIM', 'ZN', 'INDUS', 'NOX', 'AGE'],
                        ids=['CHAS', 'RAD'], df=df)
results = pyreghdfe.fit()

# Output:
#                                  OLS Regression Results                                
# =======================================================================================
# Dep. Variable:                      y   R-squared (uncentered):                   0.183
# Model:                            OLS   Adj. R-squared (uncentered):              0.158
# Method:                 Least Squares   F-statistic:                              21.93
# Date:                Mon, 14 Dec 2020   Prob (F-statistic):                    7.57e-20
# Time:                        06:46:17   Log-Likelihood:                         -1715.7
# No. Observations:                 506   AIC:                                      3441.
# Df Residuals:                     491   BIC:                                      3463.
# Df Model:                           5                                                  
# Covariance Type:            nonrobust                                                  
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# x1            -0.2089      0.049     -4.255      0.000      -0.305      -0.112
# x2             0.0679      0.018      3.711      0.000       0.032       0.104
# x3            -0.2280      0.086     -2.648      0.008      -0.397      -0.059
# x4            -9.4248      5.556     -1.696      0.090     -20.341       1.492
# x5            -0.0141      0.018     -0.767      0.443      -0.050       0.022
# ==============================================================================
# Omnibus:                      172.457   Durbin-Watson:                   0.904
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              532.297
# Skew:                           1.621   Prob(JB):                    2.59e-116
# Kurtosis:                       6.839   Cond. No.                         480.
# ==============================================================================

# Stata Output:
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

print(results.summary())
print("df_model", results.df_model)
print("df_resid", results.df_resid)
