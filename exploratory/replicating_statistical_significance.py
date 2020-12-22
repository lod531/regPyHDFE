import pandas as pd
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
df = pd.read_stata('./data/cleaned_nlswork.dta')
df = df.dropna()
#df.info()


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

# results = smf.ols(formula='ln_wage~hours_log', data=df).fit()
# 
# print(np.mean(df['ln_wage'].to_numpy().astype('float64')))
# 
# results = smf.ols(formula='ln_wage~1', data=df).fit()
# 
# import pdb; pdb.set_trace()
# print(results.summary())
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

# for a in list(enumerate(list(df))):
#     print(a)

df_np = df.to_numpy()

# just a sanity check of straight forward regression
#print("ln_wage ~ hours_log")
#model = sm.OLS(get_np_columns(df, ['ln_wage'], False), get_np_columns(df, ['hours_log']))
#results = model.fit()
#print(results.summary())


algo = pyhdfe.create(get_np_columns(df, ['idcode', 'year'], False),
                        degrees_method='pairwise')
residualized = algo.residualize(get_np_columns(df, ['ln_wage', 'hours_log'], False))

print(algo.degrees)

import pdb; pdb.set_trace()



#model = sm.OLS(residualized[:,0], np.ones((residualized.shape[0], 1)))
model = sm.OLS(residualized[:,0], add_intercept(residualized[:, 1]))

#print(add_intercept(residualized[:,1])[:10])

ids = get_np_columns(df, ['idcode', 'year'], False)

all_group_indices = []
for i in range(ids.shape[1]):
    col = ids[:, i]
    # col_n[0] = sorted unique values
    # col_n[1] = unique_indices 
    # col_n[2] = unique_inverse
    unique_values, standardized_ids = np.unique(col, return_inverse=True)

    # Okay I have a column with unique values in indices, call it a.
    # I want a list of lists b such that the first list contains
    # indices into a,r

    groups = [[] for _ in range(unique_values.shape[0])]
    for j in range(standardized_ids.shape[0]):
        groups[standardized_ids[j]].append(j)

    all_group_indices = all_group_indices + groups

seen = set()
import pdb; pdb.set_trace()
uniq = []
for x in all_group_indices:
	xt = tuple(x)
	if xt not in seen:
		uniq.append(xt)
		seen.add(xt)



import pdb; pdb.set_trace()

# let's think about what do these degrees of freedom mean
# they mean that an additional coefficient, a mean, was found
# So We are creating columns of 1s and 0s if You will
# all We're looking for is a duplicate row, right? 
# like let's say first half of first column is 1s
# if We have another column in the matrix that is the same
# We should get rid of it in the degrees of freedom calculation
# Instead of these columns all exploded, We have another representation
# In particular We have it all basically collapsed into a single
# column, and We have a bunch of N unique values present in
# the column to represent N partitions 
# So what We could do is for each column c, produce a list of lists
# c_n such that c_n[i] contains the indices of the i'th group
# in column c. 
# We produce a bunch of such list of lists and then merge them all
# and look for duplicates.


model.df_resid = 9454
results = model.fit()
RSS = np.sum(np.square(results.resid))
print()
print("ln_wage ~ hours_log, absorb(idcode, year)")
results.summary()
print(results.summary())
print("df_model", results.df_model)
print("df_resid", results.df_resid)
