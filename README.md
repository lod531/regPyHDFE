# regPyHDFE


## To do:

Okay, so, is it true that regHDFE is just linear regression with fixed effects.



<pre>
------------------------------------------------------------
                      (1)             (2)             (3)   
                    price           price           price   
------------------------------------------------------------
weight              5.741***        5.703***        5.741***
                   (5.44)          (5.17)          (5.44)   

Length Con~s          Yes             Yes             Yes   

Turn FE               Yes             Yes             Yes   

foreign               Yes              No             Yes   
------------------------------------------------------------
N                      74              74              74   
------------------------------------------------------------
t statistics in parentheses
* p < 0.05, ** p < 0.01, *** p < 0.001
</pre>

<pre>
(dropped 884 singleton observations)
(MWFE estimator converged in 8 iterations)

HDFE Linear regression                            Number of obs   =     12,568
Absorbing 2 HDFE groups                           F(   1,   9454) =      65.21
                                                  Prob > F        =     0.0000
                                                  R-squared       =     0.5333
                                                  Adj R-squared   =     0.3796
                                                  Within R-sq.    =     0.0069
                                                  Root MSE        =     0.3351

------------------------------------------------------------------------------
   hours_log |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
-------------+----------------------------------------------------------------
       union |   .0922909   .0114286     8.08   0.000     .0698884    .1146934
       _cons |   3.505433   .0039948   877.49   0.000     3.497602    3.513264
------------------------------------------------------------------------------

Absorbed degrees of freedom:
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
        year |        12           0          12     |
      idcode |      3102           1        3101     |
-----------------------------------------------------+

</pre>

<pre>
. reghdfe hours_log union, absorb(year idcode) keepsingletons
WARNING: Singleton observations not dropped; statistical significance is biased (link)
(MWFE estimator converged in 8 iterations)

HDFE Linear regression                            Number of obs   =     13,452
Absorbing 2 HDFE groups                           F(   1,   9454) =      65.21
                                                  Prob > F        =     0.0000
                                                  R-squared       =     0.5754
                                                  Adj R-squared   =     0.3959
                                                  Within R-sq.    =     0.0069
                                                  Root MSE        =     0.3351

------------------------------------------------------------------------------
   hours_log |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
-------------+----------------------------------------------------------------
       union |   .0922909   .0114286     8.08   0.000     .0698884    .1146934
       _cons |   3.502792   .0038949   899.33   0.000     3.495157    3.510427
------------------------------------------------------------------------------

Absorbed degrees of freedom:
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
        year |        12           0          12     |
      idcode |      3986           1        3985     |
-----------------------------------------------------+

</pre>


Two things they'd like are (1) Weighting and (2) Clustering of Standard Errors

### What the hell is weighting:

Let's see if the solution for week 3 homework has anything on it

https://www.stata.com/support/faqs/statistics/analytical-weights-with-linear-regression/

[This seems to contain everything on weights](https://www.reed.edu/psychology/stata/gs/tutorials/weights.html)

Looks like weighting might be something We can just apply to the design matrix before anything is done, e.g.

for frequency weighting You just duplicate rows.


### What the hell is clustering of standard errors:

'kay, so, the idea is that You have categorical variables - prices of massages in different cities for instance.

The idea is that homoscedasticity is violated here - the errors terms may be homo within the group of each city,
but hetero between different cities.

Apparently the estimator is still consistent given this wackery, but the estimate for standard errors of 
coefficients is wrong given this assumption. Clustering accounts for this. 


### Get a regression going

We want a dataset that is accessible in both stata and python


Okay so We've tried a bunch of stuff and pyhdfe seems to be the most promising. 

### Intercepts not matching

So We have from stata:

<pre>
. reghdfe ln_wage hours_log, keepsingletons absorb(year)
WARNING: Singleton observations not dropped; statistical significance is biased (link)
(MWFE estimator converged in 1 iterations)

HDFE Linear regression                            Number of obs   =     13,452
Absorbing 1 HDFE group                            F(   1,  13439) =      69.89
                                                  Prob > F        =     0.0000
                                                  R-squared       =     0.0469
                                                  Adj R-squared   =     0.0460
                                                  Within R-sq.    =     0.0052
                                                  Root MSE        =     0.4488

------------------------------------------------------------------------------
     ln_wage |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
-------------+----------------------------------------------------------------
   hours_log |    .076009   .0090917     8.36   0.000      .058188      .09383
       _cons |   1.445715    .032271    44.80   0.000     1.382459    1.508971
------------------------------------------------------------------------------

Absorbed degrees of freedom:
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
        year |        12           0          12     |
-----------------------------------------------------+
</pre>


and from pyhdfe

<pre>
ln_wage ~ hours_log, absorb(year)
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.005
Model:                            OLS   Adj. R-squared:                  0.005
Method:                 Least Squares   F-statistic:                     69.95
Date:                Sun, 06 Dec 2020   Prob (F-statistic):           6.67e-17
Time:                        12:06:36   Log-Likelihood:                -8305.1
No. Observations:               13452   AIC:                         1.661e+04
Df Residuals:                   13450   BIC:                         1.663e+04
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
x1             0.0760      0.009      8.364      0.000       0.058       0.094
const       1.735e-17      0.004   4.48e-15      1.000      -0.008       0.008
==============================================================================
Omnibus:                      404.490   Durbin-Watson:                   1.005
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              916.777
Skew:                           0.158   Prob(JB):                    8.40e-200
Kurtosis:                       4.239   Cond. No.                         2.35
==============================================================================
</pre>

So things are looking good aside from this cons and const thing. As a rando try, let's try absorbing two things:

<pre>
. reghdfe ln_wage hours_log, keepsingletons absorb(year idcode)
WARNING: Singleton observations not dropped; statistical significance is biased (link)
(MWFE estimator converged in 9 iterations)

HDFE Linear regression                            Number of obs   =     13,452
Absorbing 2 HDFE groups                           F(   1,   9454) =       0.50
                                                  Prob > F        =     0.4792
                                                  R-squared       =     0.7564
                                                  Adj R-squared   =     0.6534
                                                  Within R-sq.    =     0.0001
                                                  Root MSE        =     0.2705

------------------------------------------------------------------------------
     ln_wage |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
-------------+----------------------------------------------------------------
   hours_log |  -.0058555   .0082759    -0.71   0.479     -.022078     .010367
       _cons |   1.734197   .0292564    59.28   0.000     1.676848    1.791545
------------------------------------------------------------------------------

Absorbed degrees of freedom:
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
        year |        12           0          12     |
      idcode |      3986           1        3985     |
-----------------------------------------------------+
</pre>

<pre>
ln_wage ~ hours_log, absorb(idcode, year)
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.000
Model:                            OLS   Adj. R-squared:                 -0.000
Method:                 Least Squares   F-statistic:                    0.6654
Date:                Sun, 06 Dec 2020   Prob (F-statistic):              0.415
Time:                        12:24:58   Log-Likelihood:                 386.59
No. Observations:               12568   AIC:                            -769.2
Df Residuals:                   12566   BIC:                            -754.3
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
x1            -0.0059      0.007     -0.816      0.415      -0.020       0.008
const      -1.172e-18      0.002   -5.6e-16      1.000      -0.004       0.004
==============================================================================
Omnibus:                     1617.122   Durbin-Watson:                   2.143
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            16984.817
Skew:                          -0.215   Prob(JB):                         0.00
Kurtosis:                       8.679   Cond. No.                         3.43
==============================================================================
</pre>

Okay well the coefficients seem to be working out. Should try another dataset.

### Another dataset:

What dataset, though

Three datasets added.

### Manually calculate significance in order to be able to adjust it

Okay so there is this results statsmodels.regression.linear_model.RegressionResultsWrapper and maybe I can just manually edit the parameters? 

Well, first let's check the the residual sum of squares is the same

Okay so We need to figure out a way to compute redundant degrees of freedom. A suspicion
is that when partitioning based on features to be absorbed on, if they end up singletons
or have an identical partition, then they are redundant.

Let's start with the singletons. 

Okay so We have degrees of freedom. 


### Clustering

So a problem is that if We absorb and cluster the same variable, things work, and if We 
absorb x and cluster y then We get a mismatch.

Okay Stata is a fucking joke and an absurdity. Jesus H. Christ.

So, no absorption and clustering on single variable is identical
Clustering on two still super close, to the point where it might work
Clustering on three is just a failure and won't be delivered.

Absorbing year and clustering on idcode works

I think everything works _close enough_.

### Weighting

<pre>
. range weights 1 13452

. reghdfe wks_work ttl_exp [fweight=weights], noabsorb 
(MWFE estimator converged in 1 iterations)

HDFE Linear regression                            Number of obs   = 90,484,878
Absorbing 1 HDFE group                            F(   1,90484876)=   2.75e+07
                                                  Prob > F        =     0.0000
                                                  R-squared       =     0.2330
                                                  Adj R-squared   =     0.2330
                                                  Within R-sq.    =     0.2330
                                                  Root MSE        =    18.8790

------------------------------------------------------------------------------
    wks_work |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
-------------+----------------------------------------------------------------
     ttl_exp |   2.348477    .000448  5242.18   0.000     2.347599    2.349355
       _cons |   34.61035   .0036131  9579.02   0.000     34.60327    34.61743
------------------------------------------------------------------------------
</pre>

okay so We're gonna try to emulate the F scores for GLM lol.

We need SSR - some of squared residuals I think. They are whitened though, idk
what that means. Just squared lol.

Okay - the standard results just returns

return self.mse_model/self.mse_resid

mse_model is simple = explained sum of squares / df.model

explained sum of squares is just SSE with mean or whatever

mse_resid is self.ssr/self.df_resid

self.ssr is sum of squared residuals

Well We are having trouble just extracting predictions from the GLM model. 

Nevermind. Okay. 





### Stata Commands

<pre>
use data/cleaned_nlswork.dta
gen hours_log = log(hours)
reghdfe ln_wage hours_log, absorb(idcode year) residuals(res)
list res
</pre>




## Useful links:

[regHDFE paper](http://scorreia.com/research/hdfe.pdf)

[pyHDFE docs](https://pyhdfe.readthedocs.io/en/stable/introduction.html)
