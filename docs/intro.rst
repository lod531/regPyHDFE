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

Suspicion here is that the degrees of freedom used to calculate statistics may not always be correct under the hood. 

So, for instance, as part of generating results, statsmodels will ultimately hit line F = np.dot(np.dot(Rbq.T, invcov), Rbq), which can is approximately line 1846 in statsmodels/base/model.py (You can verify this by simply inserting a breakpoint before summary statistics are calculated and stepping through the code until the F value is calculated). 

It seems that although We manually override df_resid in order to force a correct calculation, the underlying code does not use that parameter as part of the calculation.

This results in a slight discrepancy when degrees of freedom should have been adjusted due to using the combination of clustering AND fixed effects. Or at least that's the working theory.

The simplest fix would be to manually calculate these metrics - residuals and coefficients are all correct, which should give us all the information to calculate appropriately adjusted metrics.
