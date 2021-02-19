from regpyhdfe import Regpyhdfe
from regpyhdfe.utils import get_np_columns
import FixedEffectModel.api as FEM
import pandas as pd
import numpy as np

df = pd.read_stata('data/test.dta')
#df = pd.read_stata('data/cleaned_nlswork.dta')
#df['hours_log'] = np.log(df['hours'])
#df['fifty_clusts'] = np.random.choice(50, size=len(df.index))
#df['sixty_clusts'] = np.random.choice(60, size=len(df.index))
#
#df.to_stata('data/test.dta')

#reghdfe ttl_exp wks_ue tenure, absorb(idcode) cluster(year idcode)
regpyhdfe = Regpyhdfe(df=df,
                        target='ttl_exp',
                        predictors=['wks_ue', 'tenure'],
                        absorb_ids=['idcode'],
#                        absorb_ids=['year'],
                        cluster_ids=['idcode'])
results = regpyhdfe.fit()
import pdb; pdb.set_trace()
print(results.summary())
#results = pyreghdfe.fit()
#print(results.summary())

##########################################################################################################
##########################################################################################################
#or you can define the model through defining each part
#consist_input = ['wks_ue','tenure']
#output_input = ['ttl_exp']
#category_input = ['sixty_clusts']
#cluster_input = ['fifty_clusts']
#result1 = FEM.ols_high_d_category(df,consist_input,output_input,category_input,cluster_input,formula=None,robust=False,c_method = 'cgm',epsilon = 1e-8,max_iter = 1e6)
# 
#result1.summary()
 
##########################################################################################################
##########################################################################################################
# https://apithymaxim.wordpress.com/2020/03/16/clustering-standard-errors-by-hand-using-python/
# http://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015_February.pdf
#N,k,Nclusts = len(df.index),3,50 # Number of observations, right hand side columns counting constant, number of clusters
#X = np.hstack( (np.random.random((N,k-1)), np.ones((N,1)) ) )
#X = get_np_columns(df, ['wks_ue', 'tenure'], intercept=True)
##X = regpyhdfe.data[:,1:]
###y = get_np_columns(df, ['ttl_exp'])
##y = np.expand_dims(regpyhdfe.data[:,0], 1)
##
## 
### Calculate (X'X)^-1 and the vector of coefficients, beta
##XX_inv = np.linalg.inv(X.T.dot(X))
##beta = (XX_inv).dot(X.T.dot(y))
##resid = y - X.dot(beta)
## 
###ID = np.random.choice([x for x in range(Nclusts)],N) # Vector of cluster IDs
###ID = np.squeeze(get_np_columns(df, ['delete_me']))
##ID = np.squeeze(regpyhdfe.groups_np)
##c_list = np.unique(ID) # Get unique list of clusters
##
##N, k, Nclusts = X.shape[0], X.shape[1], int(c_list.shape[0])
## 
##sum_XuuTX = 0
##for c in range(0,Nclusts):
##    in_cluster = (ID==c_list[c]) # Indicator for given cluster value
##    resid_c = resid[in_cluster]
##    uuT = resid_c.dot(resid_c.T)
##    Xc = X[in_cluster]
##    XuuTX = Xc.T.dot(uuT).dot(Xc)
##    sum_XuuTX += XuuTX
## 
##adj = (Nclusts/(Nclusts-1))*((N-1)/(N-k)) # Degrees of freedom correction from https://www.stata.com/manuals13/u20.pdf p. 54
##
### TODO: actually check if the fixed effects are nested
##df_a_nested = 0
##adj = ((N-1)/(N-df_a_nested-k))*(Nclusts/(Nclusts-1))
##V_beta = adj*(XX_inv.dot(sum_XuuTX).dot(XX_inv))
##se_beta = np.sqrt(np.diag(V_beta))
## 
### Output data for Stata
##for_stata = pd.DataFrame(X)
##for_stata.columns = ["X" + str(i) for i in range(k)]
##for_stata['ID'] = ID
##for_stata['y'] = y
##
####for_stata.to_stata("resid_test.dta")
###print('B', beta,'\n SE: \n', se_beta)
##beta = np.squeeze(beta)
##t_values = beta/se_beta
##
##from scipy.stats import t
##p_values = 2*t.cdf(-np.abs(t_values), regpyhdfe.model.df_resid)
### confidence interval size
##alpha = 0.95
##t_interval = np.asarray(t.interval(alpha=alpha, df=regpyhdfe.model.df_resid))
###print("t_interval", t_interval)
##intervals = np.empty(shape=(beta.shape[0], 2))
### for each variables
##for i in range(0, intervals.shape[0]):
##    intervals[i] = t_interval*se_beta[i] + beta[i]
##
###print("intervals", intervals)
##tmp1 = np.linalg.solve(V_beta, np.mat(beta).T)
##tmp2 = np.dot(np.mat(beta), tmp1)
##fvalue = tmp2[0, 0] / k

## k = 2
## Nclusts = len(df.index)
## SSEF = np.sum(np.square(results.resid))
## target = pyreghdfe.data[:,0]
## SSER = np.sum(np.square(target - np.mean(target)))
## dff = pyreghdfe.model.df_resid
## dfr = dff + k
## F1 = ((SSER-SSEF)/k)/(SSEF/dff)
## 
## 
## SSM = np.sum(np.square(results.fittedvalues - np.mean(target)))
## SSE = np.sum(np.square(results.resid))
## SST = np.sum(np.square(target - np.mean(target)))
## 
## DFM = k
## DFE = Nclusts-k-1
## DFT = Nclusts-1
## 
## MSM = SSM/DFM
## MSE = SSE/DFE
## MST = SST/DFT
## 
## F = MSM/MSE
## a = 123

##########################################################################################################
##########################################################################################################

# SSE = np.sum(np.square(results.resid))
# n = 13452
# p=3
# sigma_squared = (1/(n-p))*SSE
# sigma = np.sqrt(sigma_squared)
# data = get_np_columns(df, ["wks_ue", "tenure"], intercept=True)
# data = np.matmul(np.transpose(data), data)
# data = np.linalg.inv(data)
# variance = sigma_squared * data
# import pdb;pdb.set_trace()
# a=1234

SSE = np.sum(np.square(results.resid))
n = 9346
p=2
sigma_squared = (1/(n-p))*SSE
sigma = np.sqrt(sigma_squared)
data = regpyhdfe.data[:, 1:]
data = np.matmul(np.transpose(data), data)
data = np.linalg.inv(data)
variance = sigma_squared * data
import pdb; pdb.set_trace()
a = 1234
#print(results.resid[-10:])
#print(np.sum(results.resid))
#print("df_model", results.df_model)
#print("df_resid", results.df_resid)
