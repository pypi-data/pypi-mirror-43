from __future__ import print_function

import os
import re

cwd = os.getcwd()
tmpDir = cwd + '/../../result/tmp/'
resDir = cwd + '/../../result/'

def parse_expression_profiles(input_file_dir):
	"""Parses miRNA or mRNA expression level files and returns a dictionary.
	Attribute:
		input_file_dir (str): directory path which contains expression level files.
	"""

	filePattern = re.compile("rep(\d+)_tp(.+)\.tsv")
	valDict = {}

	for mRNAfile in os.listdir(input_file_dir):
		m = filePattern.match(mRNAfile)
		if not m:
			continue

		rep = m.group(1)
		time = float(m.group(2))

		infile = open(input_file_dir+'/'+mRNAfile, 'r')
		infile.readline()

		for line in infile:
			temp = line.strip().split('\t')
			geneID = temp[0]
			val = float(temp[1])
			
			if geneID in valDict:
				if rep in valDict[geneID]:
					valDict[geneID][rep][time] = val
				else:
					valDict[geneID][rep] = {time:val}
			else:
				valDict[geneID] = {}
				valDict[geneID][rep] = {time:val}
		infile.close()

	timeList = []
	repDict = {}

	for geneID in mRNAfile.keys():
		firstflag = 0
		avg = {}
		count = {}
		for rep in mRNAfile[geneID].keys():
			for time in mRNAfile[geneID][rep].keys():
				if firstflag == 0:
					if time in repDict:
						repDict[time].add(rep)
					else:
						repDict[time] = set([rep])
					firstflag = 1

				if time in avg:
					avg[time] += valDict[geneID][rep][time]
					count[time] += 1
				else:
					avg[time] = valDict[geneID][rep][time]
					count[time] = 1
		for time in timeList:
			avg[time] /= float(count[time])

		valDict[geneID]['avg'] = avg

	timeList = repDict.keys()
	
	return valDict, repDict, timeList


def parse_target_miRNAlist(miRNAlist_fp):
	"""Parses list of miRNA of interests.
	Attribute:
		miRNAlist_fp (str): File path to a miRNA list file.
	"""

	miRNAlist = []

	infile = open(miRNAlist_fp, 'r')
	for line in infile:
		miRNA = line.strip()
		miRNAlist.append(miRNA)

	return sorted(miRNAlist)


def print_tmps_for_targetExpress_and_degExtraction(expression_dict, time_list, rep_dict, out_tag):
	"""Print average expression value of replicates per mRNA or miRNA.
	Attribute:
		expression_dict (dictionary): Expression profile dictionary
		time_list (list): Time axis list
		rep_dict (dictionary): Replication list
		out_tag (string): File tag
	"""
	os.system('mkdir '+tmpDir+'rep_average')
	os.system('mkdir '+tmpDir+'deg_extraction')

	time0 = time_list[0]
	for time in time_list:
	
		outfile_avg = open(tmpDir+'rep_average/repAverage_tp'+str(time)+'.'+out_tag+'.tsv')
		if time != time0:
			outfile_0_vs_n = open(tmpDir+'deg_extraction/tp'+str(time0)+'_vs_tp'+str(time)+'.'+out_tag+'.tsv')

		for key in expression_dict.keys():
			avg = expression_dict[key]['avg'][time]
			print(key, str(avg), sep='\t', end='\n', file = outfile_avg)

			if time != time0:
				outfile_0_vs_n.write(key)
				for rep in sorted(list(rep_dict[time0])):
					outfile_0_vs_n.write('\t'+str(int(expression_dict[key][rep][time0])))
				for rep in sorted(list(rep_dict[time])):
					outfile_0_vs_n.write('\t'+str(int(expression_dict[key][rep][time])))
				outfile_0_vs_n.write('\n')

		outfile_avg.close()
		if time != time0:
			outfile_0_vs_n.close()


def print_result(final_result_dict, outtag):
	
	for mir in final_result_dict.keys():
		outfile = open(resDir+outtag+'.'+mir+'_targets.tsv', 'w')
		outfile.write('refseq_id\tcorrelation\n')
		for item in sorted(final_result_dict[mir], key=lambda x: x[1]):
			refseqID = item[0]
			corr = item[1]
			print(refseqID, str(corr), sep='\t', end='\n')
		outfile.close()

