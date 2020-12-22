import pandas as pd
from tensorflow import keras
import pyhdfe
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from linearmodels.iv.absorbing import AbsorbingLS
import pyhdfe
from utils import add_intercept, get_np_columns

# show variable labels
#pd.read_stata('/home/abom/Desktop/regPyHDFE/nlswork.dta', iterator=True).variable_labels()

# Load data
df = pd.read_stata('/home/abom/Desktop/regPyHDFE/nlswork.dta')
df = df.dropna()
df.info()

df.to_stata("cleaned_nlswork.dta")


df['hours_log'] = np.log(df['hours'])

df['intercept'] = 1

#                           OLS Regression Results
#==============================================================================
#Dep. Variable:                ln_wage   R-squared:                      0.007
#Model:                            OLS   Adj. R-squared:                 0.007
#Method:                 Least Squares   F-statistic:                    92.18
#Date:                Sat, 05 Dec 2020   Prob (F-statistic):          9.29e-22
#Time:                        13:46:40   Log-Likelihood:               -8581.9
#No. Observations:               13452   AIC:                        1.717e+04
#Df Residuals:                   13450   BIC:                        1.718e+04
#Df Model:                          1
#Covariance Type:           nonrobust
#==============================================================================
#                 coef    std err          t      P>|t|      [0.025     0.975]
#------------------------------------------------------------------------------
#Intercept      1.4036      0.033     43.158      0.000       1.340      1.467
#hours_log      0.0880      0.009      9.601      0.000       0.070      0.106
#==============================================================================
#Omnibus:                      473.900   Durbin-Watson:                  1.007
#Prob(Omnibus):                  0.000   Jarque-Bera (JB):            1002.563
#Skew:                           0.234   Prob(JB):                   1.98e-218
#Kurtosis:                       4.253   Cond. No.                        31.5
#==============================================================================

results = smf.ols(formula='ln_wage~hours_log', data=df).fit()

print(np.mean(df['ln_wage'].to_numpy().astype('float64')))

results = smf.ols(formula='ln_wage~1', data=df).fit()

print(results.summary())
#                            OLS Regression Results
#==============================================================================
#Dep. Variable:              log_hours   R-squared:                       0.009
#Model:                            OLS   Adj. R-squared:                  0.009
#Method:                 Least Squares   F-statistic:                     121.8
#Date:                Sat, 05 Dec 2020   Prob (F-statistic):           3.38e-28
#Time:                        11:30:44   Log-Likelihood:                -7706.6
#No. Observations:               13452   AIC:                         1.542e+04
#Df Residuals:                   13450   BIC:                         1.543e+04
#Df Model:                           1
#Covariance Type:            nonrobust
#==============================================================================
#                 coef    std err          t      P>|t|      [0.025      0.975]
#------------------------------------------------------------------------------
#Intercept      3.5017      0.004    831.204      0.000       3.493       3.510
#union          0.0972      0.009     11.036      0.000       0.080       0.115
#==============================================================================
#Omnibus:                     8564.470   Durbin-Watson:                   1.335
#Prob(Omnibus):                  0.000   Jarque-Bera (JB):            95943.887
#Skew:                          -2.974   Prob(JB):                         0.00
#Kurtosis:                      14.654   Cond. No.                         2.53
#==============================================================================
#
#dep = df['log_hours']
#
##exog = df['intercept'].astype('float64')
#exog = pd.concat([df['intercept'], df['union']], 1).astype('float64')
##absorb = pd.concat([df['year'], df['idcode']], 1).astype('float64')
##absorb = pd.concat([df['year'], df['idcode']], 1).astype('float64')
#
#
##model = AbsorbingLS(dep, exog, absorb=absorb)
##model = AbsorbingLS(dep, exog)
##res = model.fit()
##
##print(res.summary)
#
######################################################################### PYHDFE TEST

for a in list(enumerate(list(df))):
    print(a)

df_np = df.to_numpy()

# just a sanity check of straight forward regression
#print("ln_wage ~ hours_log")
#model = sm.OLS(get_np_columns(df, ['ln_wage'], False), get_np_columns(df, ['hours_log']))
#results = model.fit()
#print(results.summary())


algo = pyhdfe.create(get_np_columns(df, ['idcode', 'year'], False))
residualized = algo.residualize(get_np_columns(df, ['ln_wage', 'hours_log'], False))

#model = sm.OLS(residualized[:,0], add_intercept(residualized[:,1]))
#ln_wage ~ hours_log, absorb(year)
#                            OLS Regression Results
#==============================================================================
#Dep. Variable:                      y   R-squared:                       0.005
#Model:                            OLS   Adj. R-squared:                  0.005
#Method:                 Least Squares   F-statistic:                     69.95
#Date:                Sat, 05 Dec 2020   Prob (F-statistic):           6.67e-17
#Time:                        13:04:23   Log-Likelihood:                -8305.1
#No. Observations:               13452   AIC:                         1.661e+04
#Df Residuals:                   13450   BIC:                         1.663e+04
#Df Model:                           1
#Covariance Type:            nonrobust
#==============================================================================
#                 coef    std err          t      P>|t|      [0.025      0.975]
#------------------------------------------------------------------------------
#x1             0.0760      0.009      8.364      0.000       0.058       0.094
#const       1.735e-17      0.004   4.48e-15      1.000      -0.008       0.008
#==============================================================================
#Omnibus:                      404.490   Durbin-Watson:                   1.005
#Prob(Omnibus):                  0.000   Jarque-Bera (JB):              916.777
#Skew:                           0.158   Prob(JB):                    8.40e-200
#Kurtosis:                       4.239   Cond. No.                         2.35
#==============================================================================


#model = sm.OLS(residualized[:,0], np.ones((residualized.shape[0], 1)))
model = sm.OLS(residualized[:,0], add_intercept(residualized[:, 1]))

#print(add_intercept(residualized[:,1])[:10])

results = model.fit()
print()
print("ln_wage ~ hours_log, absorb(idcode, year)")
print(results.summary())
print(np.mean(residualized[:,0]))
print(np.mean(get_np_columns(df, ['ln_wage'], False)))


###################################################################################
# fastreg test

#import fastreg
#from fastreg.summary import param_table
#
# PYHDFE TEST

# PYHDFE TEST

# PYHDFE TEST

# PYHDFE TEST

# PYHDFE TEST

# PYHDFE TEST

#print("hewwo")
# PYHDFE TEST

#
## just standard regression
##results = fastreg.linear.ols(formula='log_hours~union', data=df)
##print(results)
##print(param_table(results['beta'], results['sigma'], results['x_names']))
#
## regressing on jus the intercept as a sanity check
##results = fastreg.linear.ols(formula='log_hours~1', data=df)
##print(results)
#
## . reghdfe hours_log union, absorb(idcode) keepsingletons
## WARNING: Singleton observations not dropped; statistical significance is biased (link)
## (MWFE estimator converged in 1 iterations)
##
## HDFE Linear regression                            Number of obs   =     13,452
## Absorbing 1 HDFE group                            F(   1,   9465) =      62.11
##                                                   Prob > F        =     0.0000
##                                                   R-squared       =     0.5669
##                                                   Adj R-squared   =     0.3845
##                                                   Within R-sq.    =     0.0065
##                                                   Root MSE        =     0.3382
##
## ------------------------------------------------------------------------------
##    hours_log |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
## -------------+----------------------------------------------------------------
##        union |   .0907251    .011512     7.88   0.000     .0681591    .1132912
##        _cons |    3.50315   .0039278   891.89   0.000     3.495451    3.510849
## ------------------------------------------------------------------------------
##
## Absorbed degrees of freedom:
## -----------------------------------------------------+
##  Absorbed FE | Categories  - Redundant  = Num. Coefs |
## -------------+---------------------------------------|
##       idcode |      3986           0        3986     |
## -----------------------------------------------------+
##
#
#results = fastreg.linear.ols(formula='log_hours~union + C(union) ', data=df)
#print(results)
