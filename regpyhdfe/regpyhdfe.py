import pandas as pd
import pyhdfe
import statsmodels.api as sm
import numpy as np
import pyhdfe
from .utils import add_intercept, get_np_columns
from patsy import dmatrices

class Regpyhdfe:
    def __init__(self, df, target, predictors, absorb_ids=[], cluster_ids=[], drop_singletons=True,
                    intercept=False):
        """Regression wrapper for PyHDFE.

        Args:
            df (pandas Dataframe): dataframe containing referenced data
                    which includes target, predictors and absorb and cluster.
            target (string): name of target variable - the y in y = X*b + e.
            predictors (string or list of strings): names of predictors, the X in y = X*b + e.
            absorb_ids (string or list of strings): names of variables to be absorbed for fixed effects.
            cluster_ids (string or list of strings): names of variables to be clustered on.
            drop_singletons (bool): indicates whether to drop singleton groups. Defaults is True, same as stata. Setting to False is equivalent to passing keepsingletons to reghdfe.
        """
        self.df = df
        # in case user has not wrapped singular strings in a list
        if isinstance(predictors, str):
            predictors = [predictors]
        if isinstance(absorb_ids, str):
            absorb_ids = [absorb_ids]
        if isinstance(cluster_ids, str):
            cluster_ids = [cluster_ids]
            
        self.target = target
        self.predictors = predictors
        self.absorb_ids = absorb_ids
        self.cluster_ids = cluster_ids
        self.drop_singletons = drop_singletons
        # names of all features involved in regression
        self.all_names = [target]+predictors

        # We construct a formula here to feed it into OLS
        # We do this to make the output prettier and give each coefficient
        # meaningful names (otherwise the regression coefficients are named x1, x2 etc.)
        self.formula = target + '~' + predictors[0]
        for name in predictors[1:]:
            self.formula = self.formula + '+' + name

        # if there's stuff to be absorbed
        if absorb_ids:
            # Intercept term is redundant in fixed effects
            self.formula = self.formula + '-1'
            self.algo = pyhdfe.create(ids=get_np_columns(df, absorb_ids),
                                        cluster_ids=get_np_columns(df, cluster_ids),
                                        drop_singletons=drop_singletons,
                                        degrees_method='pairwise')
            # self.residualized contains features adjusted for fixed effects
            # (i.e. means subtracted, singleton groups dropped etc.)
            self.data = self.algo.residualize(get_np_columns(df, [target]+predictors))
        else:
            # otherwise just get np columns as is
            self.data = get_np_columns(df, self.all_names)
            if not intercept:
                self.formula = self.formula + '-1'
                

        df_data = pd.DataFrame()
        for i, name in enumerate(self.all_names):
            df_data[name] = self.data[:,i]
        y, X = dmatrices(self.formula, data=df_data, return_type='dataframe')            
        # now We prepare the cluster groups if they exist
        # We do this here rather than later in fit() since it can be convenient to have
        # access to these groups as early as possible
        # if not empty

        self.model = sm.OLS(y, X)
        if bool(self.cluster_ids):
            # numpy array of group data
            self.groups_np = get_np_columns(self.df, self.cluster_ids)
            if bool(self.absorb_ids):
                # number of groups - already calculated by pyhdfe so We're just retrieving the value
                n_groups = self.algo._groups_list[0].group_count
                # get numpy representation of cluster groups
                # and remove singleton groups (if fixed effects were used)
                self.groups_np = self.groups_np[~self.algo._singleton_indices]
                min_cluster_count = np.unique(self.groups_np[:,0]).shape[0]
                for i in range(1, self.groups_np.shape[1]):
                    current_count = np.unique(self.groups_np[:,i]).shape[0]
                    if current_count < min_cluster_count:
                        min_cluster_count = current_count

                self.min_cluster_count = min_cluster_count
                self.model.df_resid = min_cluster_count - len(self.predictors)+1
                self.model._df_resid = self.model.df_resid


    def fit(self):
        """Generate linear regression coefficients for given data.

        The regression will cluster on variables provided during initialization.

        Returns:
            statsmodels.regression.linear_model.RegressionResults.
        """
        if bool(self.cluster_ids):
            self.res = self.model.fit(cov_type='cluster', use_t=False, cov_kwds={'df_correction':True, 'groups':self.groups_np})
            # manually adjusting degrees of freedom of residuals
            #res.df_resid_inference = res.df_resid
            self.res.summary = lambda yname=None, xname=None, title=None, alpha=.05:summary(self.res._results, self, yname=None, xname=None, title=None, alpha=.05)
            return self.res
        else:
            # is stuff has been absorbed adjust degrees of freedom
            if bool(self.absorb_ids and self.drop_singletons):
                a = 1234
                import pdb; pdb.set_trace()
                self.model.df_resid = np.sum(~self.algo._singleton_indices)-len(self.predictors)-self.algo.degrees
            return self.model.fit()

def summary(self, regpyhdfe, yname=None, xname=None, title=None, alpha=.05):
    """
    Summarize the Regression Results.

    Parameters
    ----------
    yname : str, optional
        Name of endogenous (response) variable. The Default is `y`.
    xname : list[str], optional
        Names for the exogenous variables. Default is `var_##` for ## in
        the number of regressors. Must match the number of parameters
        in the model.
    title : str, optional
        Title for the top table. If not None, then this replaces the
        default title.
    alpha : float
        The significance level for the confidence intervals.

    Returns
    -------
    Summary
        Instance holding the summary tables and text, which can be printed
        or converted to various output formats.

    See Also
    --------
    statsmodels.iolib.summary.Summary : A class that holds summary results.
    """
    ##########################################################################################################
    ##########################################################################################################
    # https://apithymaxim.wordpress.com/2020/03/16/clustering-standard-errors-by-hand-using-python/
    # http://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015_February.pdf
    #N,k,Nclusts = len(df.index),3,50 # Number of observations, right hand side columns counting constant, number of clusters
    #X = np.hstack( (np.random.random((N,k-1)), np.ones((N,1)) ) )
    #X = get_np_columns(df, ['wks_ue', 'tenure'], intercept=True)
    X = regpyhdfe.data[:,1:]
    #y = get_np_columns(df, ['ttl_exp'])
    y = np.expand_dims(regpyhdfe.data[:,0], 1)


    # Calculate (X'X)^-1 and the vector of coefficients, beta
    XX_inv = np.linalg.inv(X.T.dot(X))
    beta = (XX_inv).dot(X.T.dot(y))
    resid = y - X.dot(beta)

    #ID = np.random.choice([x for x in range(Nclusts)],N) # Vector of cluster IDs
    #ID = np.squeeze(get_np_columns(df, ['delete_me']))
    ID = np.squeeze(regpyhdfe.groups_np)
    c_list = np.unique(ID) # Get unique list of clusters

    N, k, Nclusts = X.shape[0], X.shape[1], int(c_list.shape[0])

    sum_XuuTX = 0
    for c in range(0,Nclusts):
        in_cluster = (ID==c_list[c]) # Indicator for given cluster value
        resid_c = resid[in_cluster]
        uuT = resid_c.dot(resid_c.T)
        Xc = X[in_cluster]
        XuuTX = Xc.T.dot(uuT).dot(Xc)
        sum_XuuTX += XuuTX

    adj = (Nclusts/(Nclusts-1))*((N-1)/(N-k)) # Degrees of freedom correction from https://www.stata.com/manuals13/u20.pdf p. 54

    # TODO: actually check if the fixed effects are nested
    df_a_nested = 1
    adj = ((N-1)/(N-df_a_nested-k))*(Nclusts/(Nclusts-1))
    V_beta = adj*(XX_inv.dot(sum_XuuTX).dot(XX_inv))
    se_beta = np.sqrt(np.diag(V_beta))

    # Output data for Stata
    for_stata = pd.DataFrame(X)
    for_stata.columns = ["X" + str(i) for i in range(k)]
    for_stata['ID'] = ID
    for_stata['y'] = y

    ##for_stata.to_stata("resid_test.dta")
    print('B', beta,'\n SE: \n', se_beta)
    beta = np.squeeze(beta)
    t_values = beta/se_beta
    print('T values', t_values)

    from scipy.stats import t
    p_values = 2*t.cdf(-np.abs(t_values), regpyhdfe.model.df_resid)
    # confidence interval size
    t_interval = np.asarray(t.interval(alpha=(1-alpha), df=regpyhdfe.model.df_resid))
    print("t_interval", t_interval)
    intervals = np.empty(shape=(beta.shape[0], 2))
    # for each variables
    for i in range(0, intervals.shape[0]):
        intervals[i] = t_interval*se_beta[i] + beta[i]


    print('intervals', intervals)
    tmp1 = np.linalg.solve(V_beta, np.mat(beta).T)
    tmp2 = np.dot(np.mat(beta), tmp1)
    fvalue = tmp2[0, 0] / k
    import pdb; pdb.set_trace()
    print('fvalue', fvalue)

#    from statsmodels.stats.stattools import (
#        jarque_bera, omni_normtest, durbin_watson)

#    jb, jbpv, skew, kurtosis = jarque_bera(self.wresid)
#    omni, omnipv = omni_normtest(self.wresid)

#    eigvals = self.eigenvals
#    condno = self.condition_number

    # TODO: Avoid adding attributes in non-__init__
#    self.diagn = dict(jb=jb, jbpv=jbpv, skew=skew, kurtosis=kurtosis,
#                      omni=omni, omnipv=omnipv, condno=condno,
#                      mineigval=eigvals[-1])
    # TODO not used yet
    # diagn_left_header = ['Models stats']
    # diagn_right_header = ['Residual stats']

    # TODO: requiring list/iterable is a bit annoying
    #   need more control over formatting
    # TODO: default do not work if it's not identically spelled

    top_left = [('Dep. Variable:', None),
                ('Model:', None),
                ('Method:', ['Least Squares']),
                ('Date:', None),
                ('Time:', None),
                ('No. Observations:', None),
                ('Df Residuals:', None),
                ('Df Model:', None),
                ]

    if hasattr(self, 'cov_type'):
        top_left.append(('Covariance Type:', [self.cov_type]))

    rsquared_type = '' if self.k_constant else ' (uncentered)'
    top_right = [('R-squared' + rsquared_type + ':',
                  ["%#8.3f" % self.rsquared]),
                 ('Adj. R-squared' + rsquared_type + ':',
                  ["%#8.3f" % self.rsquared_adj]),
                 ('F-statistic:', ["%#8.4g" % self.fvalue]),
                 ('Prob (F-statistic):', ["%#6.3g" % self.f_pvalue]),
                 ]

#    diagn_left = [('Omnibus:', ["%#6.3f" % omni]),
#                  ('Prob(Omnibus):', ["%#6.3f" % omnipv]),
#                  ('Skew:', ["%#6.3f" % skew]),
#                  ('Kurtosis:', ["%#6.3f" % kurtosis])
#                  ]
#
#    diagn_right = [('Durbin-Watson:',
#                    ["%#8.3f" % durbin_watson(self.wresid)]
#                    ),
#                   ('Jarque-Bera (JB):', ["%#8.3f" % jb]),
#                   ('Prob(JB):', ["%#8.3g" % jbpv]),
#                   ]
    if title is None:
        title = self.model.__class__.__name__ + ' ' + "Regression Results"

    # create summary table instance
    from statsmodels.iolib.summary import Summary
    smry = Summary()
    smry.add_table_2cols(self, gleft=top_left, gright=top_right,
                         yname=yname, xname=xname, title=title)
    smry.add_table_params(self, yname=yname, xname=xname, alpha=alpha,
                          use_t=self.use_t)

#    smry.add_table_2cols(self, gleft=diagn_left, gright=diagn_right,
#                         yname=yname, xname=xname,
#                         title="")

    # add warnings/notes, added to text format only
    etext = []
    if not self.k_constant:
        etext.append(
            "R² is computed without centering (uncentered) since the "
            "model does not contain a constant."
        )
    if hasattr(self, 'cov_type'):
        etext.append(self.cov_kwds['description'])
    if self.model.exog.shape[0] < self.model.exog.shape[1]:
        wstr = "The input rank is higher than the number of observations."
        etext.append(wstr)
#    if eigvals[-1] < 1e-10:
#        wstr = "The smallest eigenvalue is %6.3g. This might indicate "
#        wstr += "that there are\n"
#        wstr += "strong multicollinearity problems or that the design "
#        wstr += "matrix is singular."
#        wstr = wstr % eigvals[-1]
#        etext.append(wstr)
#    elif condno > 1000:  # TODO: what is recommended?
#        wstr = "The condition number is large, %6.3g. This might "
#        wstr += "indicate that there are\n"
#        wstr += "strong multicollinearity or other numerical "
#        wstr += "problems."
#        wstr = wstr % condno
#        etext.append(wstr)

    if etext:
        etext = ["[{0}] {1}".format(i + 1, text)
                 for i, text in enumerate(etext)]
        etext.insert(0, "Notes:")
        smry.add_extra_txt(etext)

    return smry


