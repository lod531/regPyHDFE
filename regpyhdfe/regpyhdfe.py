import pandas as pd
import pyhdfe
import statsmodels.api as sm
import numpy as np
import pyhdfe
from .utils import add_intercept, get_np_columns
from patsy import dmatrices

class Regpyhdfe:
    def __init__(self, df, target, predictors, absorb_ids, cluster_ids=[], drop_singletons=True):
        """Regression wrapper for PyHDFE.

        Args:
            df (pandas Dataframe): dataframe containing referenced data
                    which includes target, predictors and absorb and cluster
            target (string): name of target variable - the y in y = X*b + e
            predictors (string or list of strings): names of predictors, the X in y = X*b + e
            absorb_ids (string or list of strings): names of variables to be absorbed for fixed effects
            cluster_ids (string or list of strings): names of variables to be clustered on
            drop_singletons (bool): indicates whether to drop singleton groups. Defaults is True, same as stata. Setting to False is equivalent to passing keepsingletons to reghdfe
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

        self.algo = pyhdfe.create(ids=get_np_columns(df, absorb_ids),
                                    cluster_ids=get_np_columns(df, cluster_ids),
                                    drop_singletons=drop_singletons,
                                    degrees_method='pairwise')
        # names of all features involved in regression
        self.all_names = [target]+predictors
        # self.residualized contains features adjusted for fixed effects
        # (i.e. means subtracted, singleton groups dropped etc.)
        self.residualized = self.algo.residualize(get_np_columns(df, [target]+predictors+cluster_ids))
        # We construct a formula here to feed it into OLS
        # We do this to make the output prettier and give each coefficient
        # meaningful names (otherwise the regression coefficients are named x1, x2 etc.)
        self.formula = target + '~' + predictors[0]
        for name in predictors[1:]:
            self.formula = self.formula + '+' + name
        # Intercept term is redundant in fixed effects
        self.formula = self.formula + '-1'
        # We recreate self.df with residualized versions of the features
        df_residualized = pd.DataFrame()
        for i, name in enumerate(self.all_names):
            df_residualized[name] = self.residualized[:,i]
        y, X = dmatrices(self.formula, data=df_residualized, return_type='dataframe')            
        self.model = sm.OLS(y, X)

    def fit(self):
        """Generate linear regression coefficients for given data.

        The regression will cluster on variables provided during initialization.

        Returns:
            statsmodels.regression.linear_model.RegressionResults
        """
        # if not empty
        if bool(self.cluster_ids):
            # number of groups - already calculated by pyhdfe so We're just retrieving the value
            n_groups = self.algo._groups_list[0].group_count
            # get numpy representation of cluster groups
            groups_np = get_np_columns(self.df, self.cluster_ids)
            # and remove singleton groups
            groups_np = groups_np[~self.algo._singleton_indices]
            min_cluster_count = np.unique(groups_np[:,0]).shape[0]
            for i in range(1, groups_np.shape[1]):
                current_count = np.unique(groups_np[:,i]).shape[0]
                if current_count < min_cluster_count:
                    min_cluster_count = current_count

            self.model.df_resid = min_cluster_count - len(self.predictors)

            res = self.model.fit(cov_type='cluster', cov_kwds={'df_correction':False, 'groups':groups_np})
            # manually adjusting degrees of freedom of residuals
            #res.df_resid_inference = res.df_resid
            return res
        else:
            #self.model.df_resid = self.residualized.shape[0]-len(predictors)-self.algo.degrees
            self.model.df_resid = np.sum(~self.algo._singleton_indices)-len(self.predictors)-self.algo.degrees
            return self.model.fit()
