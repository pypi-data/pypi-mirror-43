import os

import numpy as np
from spherecluster import SphericalKMeans as skmeans

cwd = os.getcwd()
tmpDir = cwd + '/../../result/tmp/'
logDir = cwd + '/../../result/log/'
dbDir = cwd + '/../../database/'


def parse_singleIsoform_refFlat(swap):
        infile = open(dbDir+'human_singleIsoform_refSeqList.grch38.tsv', 'r')
        res = {}
        for line in infile:
                temp = line.strip().split()
                geneSymbol = temp[0]
                refseqID = temp[1]
                if swap == 0:
                        res[refseqID] = geneSymbol
                else:
                        res[geneSymbol] = refseqID
        infile.close()
        return res


def calc_weight_from_cov(sigma_dict):
	res = {}
	for myid in sigma_dict.keys():
		sigmaVec = sigma_dict[myid]

		if 0 in sigmaVec:
			eps = min(i for i in sigmaVec if i>0)
			sigmaVec2 = [eps if i==0. else i for i in sigmaVec]
		else:
			sigmaVec2 = sigmaVec
	
		res[myid] = map(lambda x: 1/x, sigmaVec2)
	return res

def gen_weighted_vector(mu_dict, weight_dict):
	res = {}
	for key in mu_dict:
		muVec = np.asarray(mu_dict[key])
		weightVec = np.asarray(weight_dict[key])
		res[key] = list(muVec * weightVec)
	return res

def clustering(miRNA_dict, mRNA_dict, targetSize, ffilter_result_dict, outtag):
	res = {}
	
	geneSymbol2refseqID_dict = parse_singleIsoform_refFlat(1)

	for mir in miRNA_dict:
		if mir in ffilter_result_dict:
			first_target_gene_set = ffilter_result_dict[mir]
		else:
			continue

		targetGeneExprList = []
		for gene in list(first_target_gene_set):
			refseqID = geneSymbol2refseqID_dict[gene]
			if refseqID in mRNA_dict:
				exprList = mRNA_dict[refseqID]
				targetGeneExprList.append((refseqID, exprList))

		if len(targetGeneExprList) == 0:
			continue
		
		geneIDlist = map(lambda x: x[0], targetGeneExprList)
		geneExprList = map(lambda x: x[1], targetGeneExprList)

		k = len(geneIDlist) / targetSize
		if k < 2:
			k = 2

		skm = skmeans(n_clusters=k)
		skm.fit(geneExprList)
		clusterRes = skm.labels_

		res[mir] = {}
		for idx in range(len(clusterRes)):
			clusterNum = clusterRes[idx]
			if clusterNum in res[mir]:
				res[mir][clusterNum].append(geneIDlist[idx])
			else:
				res[mir][clusterNum] = [geneIDlist[idx]]

	return res

