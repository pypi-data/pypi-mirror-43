from __future__ import print_function

import os
import sys

import mirtime.clustering as clustering
import mirtime.correlation as corr
import mirtime.firstfilter as ffilter
import mirtime.gplearning as gplearn
import mirtime.util as util

__version__ = '0.1.0'


cwd = os.getcwd()
tmpDir = cwd + '/../../result/tmp/'
logDir = cwd + '/../../result/log/'


def run_mirtime(miRNAfileDir, mRNAfileDir, miRNAlistFile, sequencingType, targetSize, outFile, targetExpressPath):

	raw_miRNAdict, miRNArepDict, miRNAtimeList = util.parse_expression_profiles(miRNAfileDir)
	raw_mRNAdict, mRNArepDict, mRNAtimeList = util.parse_expression_profiles(mRNAfileDir)
	miRNAlist = util.parse_target_miRNAlist(miRNAlistFile)

	### STEP 1. Candidate target gene Extraction
	## Select miRNAs of interests
	filtered_miRNAdict = {}
	for mir in miRNAlist:
		if mir in raw_miRNAdict:
			filtered_miRNAdict[mir] = raw_miRNAdict[mir]
		else:
			sys.exit('miRNA '+mir+' is not in your miRNA expression profiles.')

	## Select candidate target genes
	util.print_tmps_for_targetExpress_and_degExtraction(raw_mRNAdict, mRNAtimeList, mRNArepDict, outFile)

	result_targetExpress = ffilter.run_targetExpress(miRNAlist, mRNAtimeList, targetExpressPath, outFile)

	if sequencingType == 'microarray':
		deg_extract_result = ffilter.run_DESeq_or_limma(outFile, mRNArepDict, mRNAtimeList, "limma")
	elif sequencingType == 'rnaseq':
		deg_extract_result = ffilter.run_DESeq_or_limma(outFile, mRNArepDict, mRNAtimeList, "deseq")
	else:
		sys.exit('wrong sequencing type : '+sequencingType)

	first_filtered_target_result, filtered_mRNAdict = ffilter.first_filter(miRNAlist, raw_mRNAdict, result_targetExpress, deg_extract_result)

	## Regression with Gaussian process
	normalized_miRNAdict = gplearn.z_normalize(filtered_miRNAdict, outFile, 'miRNA')
	normalized_mRNAdict = gplearn.z_normalize(filtered_mRNAdict, outFile, 'mRNA')

	gp_miRNAdict = gplearn.fit_GaussianProcess(normalized_miRNAdict, miRNAtimeList, 'miRNA')
	gp_mRNAdict = gplearn.fit_GaussianProcess(normalized_mRNAdict, mRNAtimeList, 'mRNA')

	npInferTimeList = gplearn.inference_time_list(miRNAtimeList, mRNAtimeList)
	gp_mu_miRNAdict, gp_sigma_miRNAdict = gplearn.inference_new_exprs(gp_miRNAdict, miRNAtimeList, npInferTimeList, outFile)
	gp_mu_mRNAdict, gp_sigma_mRNAdict = gplearn.inference_new_exprs(gp_mRNAdict, mRNAtimeList, npInferTimeList, outFile)

	### STEP 2. Target cluster selection
	weight_miRNAdict = clustering.calc_weight_from_cov(gp_sigma_miRNAdict)
	weight_mRNAdict = clustering.calc_weight_from_cov(gp_sigma_mRNAdict)

	gpWeightVectors_miRNAdict = clustering.gen_weighted_vector(gp_mu_miRNAdict, weight_miRNAdict)
	gpWeightVectors_mRNAdict = clustering.gen_weighted_vector(gp_mu_mRNAdict, weight_mRNAdict)

	clustering_result = clustering.clustering(gpWeightVectors_miRNAdict, gpWeightVectors_mRNAdict, targetSize, first_filtered_target_result, outFile)

	correlation_result = corr.calc_corr(gp_mu_miRNAdict, gp_mu_mRNAdict, weight_miRNAdict, weight_mRNAdict)

	best_cluster_result = corr.select_best_cluster(clustering_result, correlation_result)
	final_result = corr.remove_positiveCorrs(best_cluster_result, correlation_result)

	util.print_result(final_result, outFile)
