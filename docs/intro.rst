.. |ss| raw:: html

    <strike>

.. |se| raw:: html

    </strike>

Introduction
============

This package provides a semi-convenient way of performing regression with high dimensional fixed effects in python. 

To use this, Your data must be in a pandas dataframe. Please see Examples and Tutorial sections for instructions.

Limitations
***********

Does not work with Weighting (yet).
-----------------------------------

In order to change address this, one would have to change the underyling model used for regressions. This is currently standard OLS from statsmodels, which does not support weighting. Statsmodels has other linear regression objects which do support weighting, but those have their own issues (Weighted Linear Regression does not support all kinds of weighting, Generalized Linear Models lacks appropriate summary statistics etc.)

Replication of Stata not _quite_ identical when using clustering
-----------------------------------------------------------------------------------

By not quite I mean an F-Value of 114.8 v.s. 114.58 etc.:

.. code-block:: python

    #                                 OLS Regression Results                                
	# =======================================================================================
	# Dep. Variable:                ttl_exp   R-squared (uncentered):                   0.454
	# Model:                            OLS   Adj. R-squared (uncentered):           -623.342
	# Method:                 Least Squares   F-statistic:                              114.8
	# Date:                Sun, 07 Feb 2021   Prob (F-statistic):                    4.28e-08
	# Time:                        19:42:56   Log-Likelihood:                         -29361.
	# No. Observations:               12568   AIC:                                  5.873e+04
	# Df Residuals:                      11   BIC:                                  5.874e+04
	# Df Model:                           2                                                  
	# Covariance Type:              cluster                                                  
	# ==============================================================================
	# 				 coef    std err          t      P>|t|      [0.025      0.975]
	# ------------------------------------------------------------------------------
	# wks_ue         0.0307      0.016      1.975      0.074      -0.004       0.065
	# tenure         0.8514      0.066     12.831      0.000       0.705       0.997
	# ==============================================================================
	# Omnibus:                     2467.595   Durbin-Watson:                   1.819
	# Prob(Omnibus):                  0.000   Jarque-Bera (JB):             8034.980
	# Skew:                           0.993   Prob(JB):                         0.00
	# Kurtosis:                       6.376                                         
	# ==============================================================================
	# ==============================================================================
	#
	# V.S.
	#
	# ==============================================================================
	# ==============================================================================
	# HDFE Linear regression                            Number of obs   =     12,568
	# Absorbing 1 HDFE group                            F(   2,     11) =     114.58
	# Statistics robust to heteroskedasticity           Prob > F        =     0.0000
	#                                                   R-squared       =     0.6708
	#                                                   Adj R-squared   =     0.5628
	# Number of clusters (idcode)  =      3,102         Within R-sq.    =     0.4536
	# Number of clusters (year)    =         12         Root MSE        =     2.8836
	# 
	#                            (Std. Err. adjusted for 12 clusters in idcode year)
	# ------------------------------------------------------------------------------
	#              |               Robust
	#      ttl_exp |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
	# -------------+----------------------------------------------------------------
	#       wks_ue |   .0306653   .0155436     1.97   0.074    -.0035459    .0648765
	#       tenure |   .8513953   .0663892    12.82   0.000     .7052737    .9975169
	#        _cons |   3.784107   .4974451     7.61   0.000     2.689238    4.878976
	# ------------------------------------------------------------------------------
 


A note of interest is that the fewer degrees of freedom are involved, the worse this discrepancy is, here is an example where clustering leads to just two degrees of freedom in the residuals, so basically as bad as the discrepancy can be:

.. code-block:: python

	#                                 OLS Regression Results                                
	#=======================================================================================
	#Dep. Variable:                ttl_exp   R-squared (uncentered):                   0.454
	#Model:                            OLS   Adj. R-squared (uncentered):          -6866.766
	#Method:                 Least Squares   F-statistic:                          1.354e+04
	#Date:                Sun, 07 Feb 2021   Prob (F-statistic):                     0.00608
	#Time:                        20:32:41   Log-Likelihood:                         -29361.
	#No. Observations:               12568   AIC:                                  5.873e+04
	#Df Residuals:                       1   BIC:                                  5.874e+04
	#Df Model:                           2                                                  
	#Covariance Type:              cluster                                                  
	#==============================================================================
	#                 coef    std err          t      P>|t|      [0.025      0.975]
	#------------------------------------------------------------------------------
	#wks_ue         0.0307      0.004      7.483      0.085      -0.021       0.083
	#tenure         0.8514      0.013     66.321      0.010       0.688       1.015
	#==============================================================================
	#Omnibus:                     2467.595   Durbin-Watson:                   1.819
	#Prob(Omnibus):                  0.000   Jarque-Bera (JB):             8034.980
	#Skew:                           0.993   Prob(JB):                         0.00
	#Kurtosis:                       6.376                                         
	#==============================================================================
	#==============================================================================
	#
	# v.s.
	#
	#==============================================================================
	#==============================================================================
	# HDFE Linear regression                            Number of obs   =     12,568
	# Absorbing 1 HDFE group                            F(   2,      1) =    7212.19
	# Statistics robust to heteroskedasticity           Prob > F        =     0.0083
	#                                                   R-squared       =     0.6708
	#                                                   Adj R-squared   =     0.5628
	# Number of clusters (union)   =          2         Within R-sq.    =     0.4536
	# Number of clusters (idcode)  =      3,102         Root MSE        =     2.8836
	# 
	#                            (Std. Err. adjusted for 2 clusters in union idcode)
	# ------------------------------------------------------------------------------
	#              |               Robust
	#      ttl_exp |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
	# -------------+----------------------------------------------------------------
	#       wks_ue |   .0306653   .0043113     7.11   0.089     -.024115    .0854455
	#       tenure |   .8513953   .0132713    64.15   0.010     .6827674    1.020023
	#        _cons |   3.784107   .0531894    71.14   0.009     3.108272    4.459942
	# ------------------------------------------------------------------------------
	# 
	# Absorbed degrees of freedom:
	# -----------------------------------------------------+
	#  Absorbed FE | Categories  - Redundant  = Num. Coefs |
	# -------------+---------------------------------------|
	#       idcode |      3102        3102           0    *|
	# -----------------------------------------------------+

The T-values are still quite similar, but the F-statistic is completely wrong. It is my understanding that one is not really supposed to use clustering when fewer than 30 clusters are present. This yields:


.. code-block:: python

    #HDFE Linear regression                            Number of obs   =     12,568
    #Absorbing 1 HDFE group                            F(   2,     29) =    5953.94
    #Statistics robust to heteroskedasticity           Prob > F        =     0.0000
    #                                                  R-squared       =     0.6708
    #                                                  Adj R-squared   =     0.5628
    #                                                  Within R-sq.    =     0.4536
    #Number of clusters (delete_me) =         30       Root MSE        =     2.8836

    #                             (Std. Err. adjusted for 30 clusters in delete_me)
    #------------------------------------------------------------------------------
    #             |               Robust
    #     ttl_exp |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
    #-------------+----------------------------------------------------------------
    #      wks_ue |   .0306653   .0054123     5.67   0.000     .0195959    .0417346
    #      tenure |   .8513953   .0078384   108.62   0.000     .8353639    .8674267
    #       _cons |   3.784107   .0467015    81.03   0.000     3.688592    3.879622
    #------------------------------------------------------------------------------

    #Absorbed degrees of freedom:
    #-----------------------------------------------------+
    # Absorbed FE | Categories  - Redundant  = Num. Coefs |
    #-------------+---------------------------------------|
    #      idcode |      3102           0        3102     |
    #-----------------------------------------------------+

    #                                 OLS Regression Results                                
    #=======================================================================================
    #Dep. Variable:                ttl_exp   R-squared (uncentered):                   0.454
    #Model:                            OLS   Adj. R-squared (uncentered):           -235.820
    #Method:                 Least Squares   F-statistic:                              7905.
    #Date:                Sun, 07 Feb 2021   Prob (F-statistic):                    2.03e-40
    #Time:                        22:00:43   Log-Likelihood:                         -29361.
    #No. Observations:               12568   AIC:                                  5.873e+04
    #Df Residuals:                      29   BIC:                                  5.874e+04
    #Df Model:                           2                                                  
    #Covariance Type:              cluster                                                  
    #==============================================================================
    #                 coef    std err          t      P>|t|      [0.025      0.975]
    #------------------------------------------------------------------------------
    #wks_ue         0.0307      0.005      6.529      0.000       0.021       0.040
    #tenure         0.8514      0.007    125.159      0.000       0.837       0.865
    #==============================================================================
    #Omnibus:                     2467.595   Durbin-Watson:                   1.819
    #Prob(Omnibus):                  0.000   Jarque-Bera (JB):             8034.980
    #Skew:                           0.993   Prob(JB):                         0.00
    #Kurtosis:                       6.376                                         
    #==============================================================================


Oh dear. What about 100?



The simplest fix would be to manually calculate these metrics - residuals and coefficients are all correct, which should give us all the information to calculate appropriately adjusted metrics. This would involve finding the method that Stata packages use, finding a reference for the method and implementing it as specified.


