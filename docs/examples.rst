Examples
=============

Installation
*******************

``pip install regpyhdfe``, simple as that.

Examples
**************************************************

The examples consist of two parts: the python code and the comments.

The python code(s) are minimal examples of a regression. One could simply copy/paste the code, change the dataset and the features of regression and have a working script.

The comments consists of two parts: first part is an identical regression using the reghdfe package in stata. The second part is the output of a corresponding python regression using regPyHDFE. Those comments are there for comparison purposes. 

Timing information is trivial and at this time not included - both stata and python run instantly on a laptop CPU.

Using fixed effects only
------------------------
These examples do not use clustering. As You can see, all that's really needed is a pandas dataframe. Then simply pass in the arguments in appropriate order (or simply pass named arguments. For details on parameters look at the Regpyhdfe object documentation)

.. code-block:: python

	import pandas as pd
	import numpy as np
	from regpyhdfe import Regpyhdfe

	from sklearn.datasets import load_boston

	def sklearn_to_df(sklearn_dataset):
		df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
		df['target'] = pd.Series(sklearn_dataset.target)
		return df

	df = sklearn_to_df(load_boston())

	df.to_stata("boston.dta")
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
	#                                  OLS Regression Results                                
	# =======================================================================================
	# Dep. Variable:                 target   R-squared (uncentered):                   0.183
	# Model:                            OLS   Adj. R-squared (uncentered):              0.158
	# Method:                 Least Squares   F-statistic:                              21.93
	# Date:                Mon, 11 Jan 2021   Prob (F-statistic):                    7.57e-20
	# Time:                        20:30:53   Log-Likelihood:                         -1715.7
	# No. Observations:                 506   AIC:                                      3441.
	# Df Residuals:                     491   BIC:                                      3463.
	# Df Model:                           5                                                  
	# Covariance Type:            nonrobust                                                  
	# ==============================================================================
	#                  coef    std err          t      P>|t|      [0.025      0.975]
	# ------------------------------------------------------------------------------
	# CRIM          -0.2089      0.049     -4.255      0.000      -0.305      -0.112
	# ZN             0.0679      0.018      3.711      0.000       0.032       0.104
	# INDUS         -0.2280      0.086     -2.648      0.008      -0.397      -0.059
	# NOX           -9.4248      5.556     -1.696      0.090     -20.341       1.492
	# AGE           -0.0141      0.018     -0.767      0.443      -0.050       0.022
	# ==============================================================================
	# Omnibus:                      172.457   Durbin-Watson:                   0.904
	# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              532.297
	# Skew:                           1.621   Prob(JB):                    2.59e-116
	# Kurtosis:                       6.839   Cond. No.                         480.
	# ==============================================================================
	# 
	# Notes:
	# [1] R² is computed without centering (uncentered) since the model does not contain a constant.
	# [2] Standard Errors assume that the covariance matrix of the errors is correctly specified.
	model = Regpyhdfe(df, 'target', ['CRIM', 'ZN', 'INDUS', 'NOX', 'AGE'], ['CHAS', 'RAD'])
	results = model.fit()
	print("target~CRIM + ZN + INDUS + NOX + AGE, absorb(CHAS, RAD)")
	print(results.summary())


.. code-block:: python

	import pandas as pd
	import numpy as np
	from regpyhdfe import Regpyhdfe

	# details about dataset can be found at https://www.kaggle.com/crawford/80-cereals
	df = pd.read_stata('/home/abom/Desktop/regPyHDFE/data/cereal.dta')

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

	# rating ~ fat + protein + carbo + sugars, absorb(shelf)
	#                                  OLS Regression Results                                
	# =======================================================================================
	# Dep. Variable:                 rating   R-squared (uncentered):                   0.759
	# Model:                            OLS   Adj. R-squared (uncentered):              0.734
	# Method:                 Least Squares   F-statistic:                              54.98
	# Date:                Mon, 11 Jan 2021   Prob (F-statistic):                    6.89e-21
	# Time:                        20:45:37   Log-Likelihood:                         -252.82
	# No. Observations:                  77   AIC:                                      513.6
	# Df Residuals:                      70   BIC:                                      523.0
	# Df Model:                           4                                                  
	# Covariance Type:            nonrobust   
	#                  coef    std err          t      P>|t|      [0.025      0.975]
	# ------------------------------------------------------------------------------
	# fat           -5.6842      0.880     -6.458      0.000      -7.440      -3.929
	# protein        3.7404      0.843      4.437      0.000       2.059       5.422
	# carbo         -0.7892      0.204     -3.866      0.000      -1.196      -0.382
	# sugars        -2.0329      0.218     -9.326      0.000      -2.468      -1.598
	# ==============================================================================
	# Omnibus:                        5.613   Durbin-Watson:                   1.801
	# Prob(Omnibus):                  0.060   Jarque-Bera (JB):                7.673
	# Skew:                           0.179   Prob(JB):                       0.0216
	# Kurtosis:                       4.504   Cond. No.                         5.84
	# ==============================================================================

.. code-block:: python

	residualized = Regpyhdfe(df, 'rating', ['fat', 'protein', 'carbo', 'sugars'], ['shelf'])
	results = residualized.fit()
	print("rating ~ fat + protein + carbo + sugars, absorb(shelf)")
	print(results.summary())


	import pandas as pd
	import numpy as np
	from regpyhdfe import Regpyhdfe 
	# show variable labels
	#pd.read_stata('/home/abom/Desktop/regPyHDFE/nlswork.dta', iterator=True).variable_labels()

	# Load data
	df = pd.read_stata('/home/abom/Desktop/regPyHDFE/data/cleaned_nlswork.dta')

	df['hours_log'] = np.log(df['hours'])

	# . reghdfe ln_wage hours_log, absorb(idcode year)
	# (dropped 884 singleton observations)
	# (MWFE estimator converged in 8 iterations)
	# 
	# HDFE Linear regression                            Number of obs   =     12,568
	# Absorbing 2 HDFE groups                           F(   1,   9454) =       0.50
	#                                                   Prob > F        =     0.4792
	#                                                   R-squared       =     0.7314
	#                                                   Adj R-squared   =     0.6430
	#                                                   Within R-sq.    =     0.0001
	#                                                   Root MSE        =     0.2705
	# 
	# ------------------------------------------------------------------------------
	#      ln_wage |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
	# -------------+----------------------------------------------------------------
	#    hours_log |  -.0058555   .0082759    -0.71   0.479     -.022078     .010367
	#        _cons |   1.736618   .0292873    59.30   0.000     1.679208    1.794027
	# ------------------------------------------------------------------------------
	# 
	# Absorbed degrees of freedom:
	# -----------------------------------------------------+
	#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
	# -------------+---------------------------------------|
	#       idcode |      3102           0        3102     |
	#         year |        12           1          11     |
	# -----------------------------------------------------+

	# ln_wage ~ hours_log, absorb(idcode, year)
	#                                  OLS Regression Results                                
	# =======================================================================================
	# Dep. Variable:                ln_wage   R-squared (uncentered):                   0.000
	# Model:                            OLS   Adj. R-squared (uncentered):             -0.329
	# Method:                 Least Squares   F-statistic:                             0.5006
	# Date:                Mon, 11 Jan 2021   Prob (F-statistic):                       0.479
	# Time:                        21:07:22   Log-Likelihood:                          386.59
	# No. Observations:               12568   AIC:                                     -771.2
	# Df Residuals:                    9454   BIC:                                     -763.7
	# Df Model:                           1                                                  
	# Covariance Type:            nonrobust   
	# ==============================================================================
	#                  coef    std err          t      P>|t|      [0.025      0.975]
	# ------------------------------------------------------------------------------
	# hours_log     -0.0059      0.008     -0.708      0.479      -0.022       0.010
	# ==============================================================================
	# Omnibus:                     1617.122   Durbin-Watson:                   2.143
	# Prob(Omnibus):                  0.000   Jarque-Bera (JB):            16984.817
	# Skew:                          -0.215   Prob(JB):                         0.00
	# Kurtosis:                       8.679   Cond. No.                         1.00
	# ==============================================================================


	model = Regpyhdfe(df, "ln_wage", "hours_log", ["idcode", "year"])
	results = model.fit()
	print("ln_wage ~ hours_log, absorb(idcode, year)")
	print(results.summary())

Clustering:
-----------

Very similar to standard regression, simply add a clustering_ids parameter to the parameter list passed to Regpyhdfe.

.. code-block:: python

	from regpyhdfe import Regpyhdfe
	import pandas as pd
	import numpy as np

	df = pd.read_stata('data/cleaned_nlswork.dta')
	df['hours_log'] = np.log(df['hours'])
	regpyhdfe = Regpyhdfe(df=df,
							target='ttl_exp',
							predictors=['wks_ue', 'tenure'],
							ids=['idcode'],
							cluster_ids=['year', 'idcode'])

	# (dropped 884 singleton observations)
	# (MWFE estimator converged in 1 iterations)
	# 
	# HDFE Linear regression                            Number of obs   =     12,568
	# Absorbing 1 HDFE group                            F(   2,     11) =     114.58
	# Statistics robust to heteroskedasticity           Prob > F        =     0.0000
	#                                                   R-squared       =     0.6708
	#                                                   Adj R-squared   =     0.5628
	# Number of clusters (year)    =         12         Within R-sq.    =     0.4536
	# Number of clusters (idcode)  =      3,102         Root MSE        =     2.8836
	# 
	#                            (Std. Err. adjusted for 12 clusters in year idcode)
	# ------------------------------------------------------------------------------
	#              |               Robust
	#      ttl_exp |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
	# -------------+----------------------------------------------------------------
	#       wks_ue |   .0306653   .0155436     1.97   0.074    -.0035459    .0648765
	#       tenure |   .8513953   .0663892    12.82   0.000     .7052737    .9975169
	#        _cons |   3.784107   .4974451     7.61   0.000     2.689238    4.878976
	# ------------------------------------------------------------------------------
	# 
	# Absorbed degrees of freedom:
	# -----------------------------------------------------+
	#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
	# -------------+---------------------------------------|
	#       idcode |      3102        3102           0    *|
	# -----------------------------------------------------+
	# * = FE nested within cluster; treated as redundant for DoF computation

	#                                  OLS Regression Results                                
	# =======================================================================================
	# Dep. Variable:                ttl_exp   R-squared (uncentered):                   0.454
	# Model:                            OLS   Adj. R-squared (uncentered):           -623.342
	# Method:                 Least Squares   F-statistic:                              114.8
	# Date:                Mon, 11 Jan 2021   Prob (F-statistic):                    4.28e-08
	# Time:                        21:35:07   Log-Likelihood:                         -29361.
	# No. Observations:               12568   AIC:                                  5.873e+04
	# Df Residuals:                      11   BIC:                                  5.874e+04
	# Df Model:                           2                                                  
	# Covariance Type:              cluster                                                  
	# ==============================================================================
	#                  coef    std err          z      P>|z|      [0.025      0.975]
	# ------------------------------------------------------------------------------
	# wks_ue         0.0307      0.016      1.975      0.048       0.000       0.061
	# tenure         0.8514      0.066     12.831      0.000       0.721       0.981
	# ==============================================================================
	# Omnibus:                     2467.595   Durbin-Watson:                   1.819
	# Prob(Omnibus):                  0.000   Jarque-Bera (JB):             8034.980
	# Skew:                           0.993   Prob(JB):                         0.00
	# Kurtosis:                       6.376   Cond. No.                         2.06
	# ==============================================================================

	results = regpyhdfe.fit()
	print(results.summary())
