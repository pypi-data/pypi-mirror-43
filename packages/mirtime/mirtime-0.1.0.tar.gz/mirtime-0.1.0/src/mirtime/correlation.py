import math

import numpy as np


def weighted_corr(miRNAvec, mRNAvec, miRNAweight, mRNAweight):
	miRNAmean = np.average(miRNAvec, weights = miRNAweight)
	mRNAmean = np.average(mRNAvec, weights = mRNAweight)

	miRNAvar = np.average((miRNAvec - miRNAmean)**2, weights = miRNAweight)
	mRNAvar = np.average((mRNAvec - mRNAmean)**2, weights = mRNAweight)

	coweight = np.sqrt(miRNAweight * mRNAweight)
	covar = np.average((miRNAvec - miRNAmean) * (mRNAvec - mRNAmean), weights = coweight)

	weightPearsons = covar / math.sqrt(miRNAvar * mRNAvar)

	return weightPearsons

def calc_corr(miRNAdict, mRNAdict, miRNAweightDict, mRNAweightDict):
	corrDict = {}
	for miRNA in miRNAdict.keys():
		miRNAexpr = np.asarray(miRNAdict[miRNA])
		miRNAweight = np.asarray(miRNAweightDict[miRNA])

		for mRNA in mRNAdict.keys():
			mRNAexpr = np.asarray(mRNAdict[mRNA])
			mRNAweight = np.asarray(mRNAweightDict[mRNA])

			weightCorr = weighted_corr(miRNAexpr, mRNAexpr, miRNAweight, mRNAweight)

			if miRNA in corrDict:
				corrDict[miRNA][mRNA] = weightCorr
			else:
				corrDict[miRNA] = {mRNA: weightCorr}
	return corrDict

def select_best_cluster(cluster_dict, correlation_dict):
	cluster_corr_dict = {}
	best_cluster_res = {}

	for mir in cluster_dict.keys():
		cluster_corr_dict[mir] = {}
		for clusterID in sorted[cluster_dict[mir].keys()]:
			cluster_corr_dict[mir][clusterID] = 0
			refseqID_list = cluster_dict[mir][clusterID]
			for refseqID in refseqID_list:
				cluster_corr_dict[mir][clusterID] += correlation_dict[mir][refseqID]
			cluster_corr_dict[mir][clusterID] = cluster_corr_dict[mir][clusterID] / len(refseqID_list)
		
		bestClusterID = sorted(cluster_corr_dict.items(), key=lambda x: x[1])[0][0]
		best_cluster_res[mir] = cluster_dict[mir][bestClusterID]

	return best_cluster_res

def remove_positiveCorrs(best_cluster_dict, correlation_dict):
	res = {}
	for mir in best_cluster_dict.keys():
		res[mir] = []
		for refseqID in best_cluster_dict[mir]:
			corr = correlation_dict[mir][refseqID]
			if corr < 0:
				res[mir].append((refseqID, corr))
			else:
				pass
	return res
