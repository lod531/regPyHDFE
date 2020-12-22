import pandas as pd
import pyhdfe
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from linearmodels.iv.absorbing import AbsorbingLS
import pyhdfe
from utils import add_intercept, get_np_columns
from patsy import dmatrices

class Pyreghdfe:
    def __init__(self, df, target, predictors, ids, cluster_ids=[], drop_singletons=True):
        """
        Args:
            target (string): name of target variable
            predictors (list of strings): names of predictors
            ids (list of strings): names of variables to be absorbed
            df (pandas Dataframe): dataframe containing referenced data
                                    which includes target, predictors and ids
        """
        self.df = df
        self.algo = pyhdfe.create(ids=get_np_columns(df, ids),
                                    cluster_ids=get_np_columns(df, cluster_ids),
                                    drop_singletons=drop_singletons,
                                    degrees_method='pairwise')
        self.all_names = [target]+predictors
        self.residualized = self.algo.residualize(get_np_columns(df, [target]+predictors+cluster_ids))
        self.formula = target + '~' + predictors[0]
        for name in predictors[1:]:
            self.formula = self.formula + '+' + name
        self.formula = self.formula + '-1'
        df_residualized = pd.DataFrame()
        for i, name in enumerate(self.all_names):
            df_residualized[name] = self.residualized[:,i]

        y, X = dmatrices(self.formula, data=df_residualized, return_type='dataframe')            
        self.model = sm.OLS(y, X)
        if cluster_ids == []:
            self.model.df_resid = self.residualized.shape[0]-len(predictors)-self.algo.degrees
        else:
            clusters = get_np_columns(df, cluster_ids)[~self.algo._singleton_indices]
            min_cluster_count = np.unique(clusters[:,0]).shape[0]
            for i in range(1, clusters.shape[1]):
                current_count = np.unique(clusters[:,i]).shape[0]
                if current_count < min_cluster_count:
                    min_cluster_count = current_count
                
            self.model.df_resid = min_cluster_count-len(predictors)

    def fit(self, **kwargs):
        groups_dict={}
        if 'cov_type' in kwargs:
            groups = get_np_columns(self.df, kwargs['groups'])
            cleaned_groups = groups[np.logical_not(self.algo._singleton_indices)]
            temp = self.model.fit()
            return self.model.fit(cov_type='cluster', cov_kwds={'groups': cleaned_groups})
        else:
            return self.model.fit(**kwargs)
                
def main():
	# Load data
	df = pd.read_stata('./data/cleaned_nlswork.dta')
	df = df.dropna()
	#df.info()


	df['hours_log'] = np.log(df['hours'])

	pyreghdfe = Pyreghdfe('ln_wage', ['hours_log', 'ttl_exp'], ['idcode', 'year'], df)
#	pyreghdfe = Pyreghdfe('ln_wage', ['hours_log', 'ttl_exp'], ['idcode', 'year'], df)
	results = pyreghdfe.fit()
	print()
	print("ln_wage ~ hours_log, ttl_exp, absorb(idcode, year)")
	results.summary()
	print(results.summary())
	print("df_model", results.df_model)
	print("df_resid", results.df_resid)

if __name__ == "__main__":
    # execute only if run as a script
    main()
