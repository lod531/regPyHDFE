.. |ss| raw:: html

    <strike>

.. |se| raw:: html

    </strike>

Tutorial
========

Installation
*************

Should work with just ``pip install regpyhdfe``.

Load in data
***********************************

We need a pandas dataframe. For the purposes of this example You can go to ``https://github.com/lod531/regPyHDFE/blob/main/data/cleaned_nlswork.dta`` and download the cleaned nlswork dataset. This dataset contains entries that can be acquired in stata by typing ``use nlswork``, except rows containing NA values have already been dropped (hence cleaned_nlswork.dta, rather than nlswork.dta).

Once You have a file, importing the data is as simple as

.. code-block:: python

    import pandas as pd
    # load dataframe
    df = pd.read_stata('path/to/cleaned_nlswork.dta')

Pandas has other import functions if You have a file in a different format, e.g. ``pd.read_csv``.

Regress
********

Target is of course the target variable.

Predictors are... Predictors.

absorb_ids are names of variables to be absorbed as high dimensional fixed effects

cluster_ids are names of variables containing cluster information (i.e. if there are N clusters, then each row of a cluster variables contains one of N distinct values.)

.. code-block:: python

    target = "ln_wage"
    predictors = ["hours", "tenure", "ttl_exp"]
    absorb_ids = ["year", "idcode"]
    cluster_ids = ["year"]

    from regpyhdfe import Regpyhdfe
    model = Regpyhdfe(df=df, target=target, predictors=predictors,
                        absorb_ids=absorb_ids, 
                        cluster_ids=cluster_ids)
    results = model.fit()

Examine results
***************

At the time of writing, the ``results`` object is of type ``statsmodels.regression.linear_model.RegressionResults``, documentation for which can be viewed `here <https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html>`_.

The `statsmodels.regression.linear_model.RegressionResults`` object has a variety of statistics, but chances are all You're looking is a summary, like so:

.. code-block:: python

    print(results.summary())

The output of that looks like 


.. code-block::

                                    OLS Regression Results                                
	=======================================================================================
	Dep. Variable:                ln_wage   R-squared (uncentered):                   0.059
	Model:                            OLS   Adj. R-squared (uncentered):          -1313.428
	Method:                 Least Squares   F-statistic:                              185.2
	Date:                Thu, 14 Jan 2021   Prob (F-statistic):                    2.09e-08
	Time:                        13:21:24   Log-Likelihood:                          766.62
	No. Observations:               12568   AIC:                                     -1527.
	Df Residuals:                       9   BIC:                                     -1505.
	Df Model:                           3                                                  
	Covariance Type:              cluster                                                  
	==============================================================================
					 coef    std err          z      P>|z|      [0.025      0.975]
	------------------------------------------------------------------------------
	hours         -0.0017      0.001     -3.371      0.001      -0.003      -0.001
	tenure         0.0109      0.003      3.858      0.000       0.005       0.016
	ttl_exp        0.0348      0.003     12.650      0.000       0.029       0.040
	==============================================================================
	Omnibus:                     1709.175   Durbin-Watson:                   2.171
	Prob(Omnibus):                  0.000   Jarque-Bera (JB):            21109.707
	Skew:                          -0.174   Prob(JB):                         0.00
	Kurtosis:                       9.340   Cond. No.                         6.87
	==============================================================================

	Notes:
	[1] R² is computed without centering (uncentered) since the model does not contain a constant.
	[2] Standard Errors are robust to cluster correlation (cluster)
 
And for Your convenience the whole script is

.. code-block:: python

	import pandas as pd
	# load dataframe
	df = pd.read_stata('/path/to/cleaned_nlswork.dta')

	target = "ln_wage"
	predictors = ["hours", "tenure", "ttl_exp"]
	absorb_ids = ["year", "idcode"]
	cluster_ids = ["year"]

	from regpyhdfe import Regpyhdfe
	model = Regpyhdfe(df=df, target=target, 
            predictors = predictors, 
            absorb_ids=absorb_ids, 
            cluster_ids=cluster_ids)
	results = model.fit()
	print(results.summary())

