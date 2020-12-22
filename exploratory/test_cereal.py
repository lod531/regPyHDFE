from pyreghdfe import Pyreghdfe
import pandas as pd

df = pd.read_stata('data/cereal.dta')

pyreghdfe = Pyreghdfe(target='rating',
                        predictors=['fat', 'protein', 'carbo', 'sugars'],
                        ids=['shelf'], df=df)
results = pyreghdfe.fit()

# Output:
#                                  OLS Regression Results                                
# =======================================================================================
# Dep. Variable:                      y   R-squared (uncentered):                   0.759
# Model:                            OLS   Adj. R-squared (uncentered):              0.734
# Method:                 Least Squares   F-statistic:                              54.98
# Date:                Mon, 14 Dec 2020   Prob (F-statistic):                    6.89e-21
# Time:                        07:04:35   Log-Likelihood:                         -252.82
# No. Observations:                  77   AIC:                                      513.6
# Df Residuals:                      70   BIC:                                      523.0
# Df Model:                           4                                                  
# Covariance Type:            nonrobust                                                  
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# x1            -5.6842      0.880     -6.458      0.000      -7.440      -3.929
# x2             3.7404      0.843      4.437      0.000       2.059       5.422
# x3            -0.7892      0.204     -3.866      0.000      -1.196      -0.382
# x4            -2.0329      0.218     -9.326      0.000      -2.468      -1.598
# ==============================================================================
# Omnibus:                        5.613   Durbin-Watson:                   1.801
# Prob(Omnibus):                  0.060   Jarque-Bera (JB):                7.673
# Skew:                           0.179   Prob(JB):                       0.0216
# Kurtosis:                       4.504   Cond. No.                         5.84
# ==============================================================================

# Stata Output:
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



print(results.summary())
print("df_model", results.df_model)
print("df_resid", results.df_resid)
