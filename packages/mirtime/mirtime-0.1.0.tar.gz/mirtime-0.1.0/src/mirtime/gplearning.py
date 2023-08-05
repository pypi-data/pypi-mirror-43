import math
import os

import numpy as np
import scipy
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern
from sklearn.gaussian_process.kernels import WhiteKernel

cwd = os.getcwd()
tmpDir = cwd + '/../../result/tmp/'
logDir = cwd + '/../../result/log/'
dbDir = cwd + '/../../database/'

def check_NaN(mylist):
	for val in mylist:
		if math.isnan(val):
			return True
	return False

def z_normalize(dataDict, outtag, dataType):
        res = {}
        trash = open(tmpDir+outtag+'_fail_to_normalize.'+dataType, 'w')
        for gene in dataDict.keys():
		tempRepDict = {}

                pos = {}
                avg = {}

                for rep in dataDict[gene].keys():
                	if rep == 'avg':
                        	continue

                        times = sorted(dataDict[gene][rep].keys())
                        exprs = map(lambda x: x[1], sorted(dataDict[gene][rep].items(), key = lambda x: x[0]))
                        zVec = scipy.stats.zscore(exprs)
                        if check_NaN(zVec):
                        	trash.write(gene+'\t'+str(rep)+'\t'+str(exprs))
                                continue
                        else:
                        	zVecDict = {}
                                for i in range(len(times)):
                                	zVecDict[times[i]] = zVec[i]
                                        if times[i] in avg:
                                        	avg[times[i]] += zVec[i]
                                                pos[times[i]] += 1
                                        else:
                                                avg[times[i]] = zVec[i]
                                                pos[times[i]] = 1
                                        tempRepDict[rep] = zVecDict

                        if len(tempRepDict) == 0:
                                continue
                        else:
                                res[gene] = tempRepDict
                                for key in pos.keys():
                                        avg[key] /= pos[key]
                                res[gene]['avg'] = avg

        return res


def fit_GaussianProcess(expression_dict, time_list, datatype):
	res_GPdict = {}

	for myid in expression_dict.keys():
		kern = C() * Matern(nu=1.5, length_scale_bounds = (time_list[0], time_list[-1]))+WhiteKernel(noise_level_bounds=(1e-10,1e-1))

		myTimeList = []
		exprList = []
		for rep in expression_dict[myid].keys():
			if rep != 'avg':
				tempTimeList = expression_dict[myid][rep].keys()
				for time in tempTimeList:
					exprList.append(expression_dict[myid][rep][time])
				myTimeList += tempTimeList
		myTimeList = np.asarray(myTimeList).reshape(-1, 1)
		npExprList = np.asarray(exprList)
		m = GaussianProcessRegressor(kernel = kern, normalize_y = True, n_restarts_optimizer = 10)

		m.fit(myTimeList, npExprList)
		res_GPdict[myid] = m

	return res_GPdict

def inference_time_list(miRNA_time_list, mRNA_time_list):
	miRNAintervals = []
	mRNAintervals = []

	for idx in range(len(miRNA_time_list)-1):
		miRNAintervals.append(miRNA_time_list[idx+1] - miRNA_time_list[idx])
	for idx in range(len(mRNA_time_list)-1):
		mRNAintervals.append(mRNA_time_list[idx+1] - mRNA_time_list[idx])
	
	miRNAinterval = min(miRNAintervals)
	mRNAinterval = min(mRNAintervals)
	
	interval = max(miRNAinterval, mRNAinterval)
	start = max(miRNA_time_list[0], mRNA_time_list[0])
	end = min(miRNA_time_list[-1], mRNA_time_list[-1])
	length = end-start

	infer_time_list = np.linspace(start,end,(length/interval)+1).reshape((-1,1))

	return infer_time_list

def inference_new_exprs(gp_dict, time_list, infer_time_list, outtag):
	res_mu = {}
	res_sigma = {}

	for myid in gp_dict.keys():
		model = gp_dict[myid]
		mu, sigma = model.predict(infer_time_list, return_std = True)
		res_mu[myid] = mu
		res_sigma[myid] = sigma

	return res_mu, res_sigma

