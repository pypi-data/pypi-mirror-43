
import os
import re
import subprocess

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

def run_targetExpress(miRNAlist, mRNAtimeList, targetExpressPath, outtag):
        avgFilePattern = re.compile('repAverage_tp(.+)\.'+outtag+'\.tsv')
        avgDir = tmpDir+'rep_average'
        targetExpressDir = tmpDir+'target_express_result_'+outtag

        os.system('mkdir '+targetExpressDir)

	## Read singleIsoform_refFlat file
	refseqID2geneSymbolDict = parse_singleIsoform_refFlat(0)
	
	## Run Target Express
	for avgFile in avgDir:
                m = avgFilePattern.match(avgFile)
                if not m:
                        continue

                time = m.group(1)
		procs = []
                for miRNA in miRNAlist:
                        os.system('mkdir '+targetExpressDir+'/tp'+time+'/'+miRNA)
                        outfile = targetExpressDir+'/tp'+time+'/'+miRNA+'/'+'_'.join([miRNA, time])
                        logfile = logDir + '_'.join([miRNA, time, 'targetExpressRes.txt'])
                        proc = subprocess.Popen(['nohup', 'perl', targetExpressPath, miRNA, '1', '1', '1', avgDir+avgFile, outfile, '&>', logfile+'&'])
			procs.append(proc)

		for proc in procs:
			proc.communicate()

	## Union TargetExpress result
	unionRes = {}
	for time in mRNAtimeList:
		for miRNA in os.listdir(os.path.join(targetExpressDir, 'tp'+str(time))):
			if miRNA not in unionRes:
				unionRes[miRNA] = set([])

			infile = open(os.path.join(targetExpressDir, 'tp'+str(time), miRNA, '.'.join([miRNA,str(time)])), 'r')
			infile.readline()
			for line in infile:
				temp = line.strip().split()
				refseqID = temp[0]
				geneSymbol = refseqID2geneSymbolDict[refseqID]
				score = float(temp[2])
				if score > 0:
					unionRes[miRNA].add(geneSymbol)
			infile.close()

	return unionRes


def run_DESeq_or_limma(outtag, rep_dict, time_list, label):

	refseqID2geneSymbol_dict = parse_singleIsoform_refFlat(0)
	time0 = time_list[0]
	result_dir = tmpDir+outtag+'_'+label+'_result/'
	procs = []

	for time in time_list[1:]:
		input_file = tmpDir+'deg_extraction/tp'+str(time0)+'_vs_tp'+str(time)+'.'+outtag+'.tsv'
		outfile_name = result_dir+'tp'+str(time0)+'_vs_tp'+str(time)+'.tsv'

		label = ('s1;'*len(rep_dict[time0])+'s2;'*len(rep_dict[time])).rstrip(';')
		sample_name = ''
		for x in range(0, len(label.split(';'))):
			sample_name += 's'+str(x)+';'
		sample_name.rstrip(';')

		if label == 'limma':
			process = subprocess.Popen(['Rscript','run_limma_with_expression_table.R','-s',sample_name, '-r',result_dir, '-o', outfile_name, '-l', label, '-c', input_file])
			procs.append(process)
		if label == 'deseq':
			process = subprocess.Popen(['Rscript', 'run_DESeq.R', '-s', sample_name, '-r', result_dir, '-o', outfile_name, '-l', label, '-c', input_file])
			procs.append(process)
	
	for proc in procs:
		proc.communicate()
	
	deg_set = set([])
	for time in time_list[1:]:
		result_file = result_dir+'tp'+str(time0)+'_vs_tp'+str(time)+'.tsv'
		infile = open(result_file, 'r')
		infile.readline()
		for line in infile:
			temp = line.strip().split()
			refseqID = temp[0]
			pval = float(temp[4])
			if pval < 0.01:
				geneSymbol = refseqID2geneSymbol_dict[refseqID]
				deg_set.add(geneSymbol)
		infile.close()
	
	return deg_set


def first_filter(miRNAlist, raw_mRNAdict, targetExpress_dict, deg_set):
	first_filtered_dict = {}
	filtered_mRNAdict = {}
	refseqID2geneSymbol_dict = parse_singleIsoform_refFlat(0)

	def parse_dbfiles(fileptr):
		infile = open(fileptr, 'r')
		res = {}
		for line in infile:
			temp = line.strip().split()
			miRNA = temp[0]
			gene = temp[1]
			if miRNA in res:
				res[miRNA].add(gene)
			else:
				res[miRNA] = set([gene])
		return res

	miRDB_dict = parse_dbfiles(dbDir+'miRDB_v5.0_prediction_result.hsa.geneSymbol')
	mirTarget_dict = parse_dbfiles(dbDir+'MirTarget_3.0_prediction_result_all_humans.hsa.geneSymbol')
	targetScan_mirTarBase_dict = parse_dbfiles(dbDir+'targetScan_mirTarBase.union.pairList')

	totalUnionGeneSet = set([])
	for miRNA in miRNAlist:
		unionGeneSet = set([])
		for predDict in [miRDB_dict, mirTarget_dict, targetScan_mirTarBase_dict, targetExpress_dict]:
			unionGeneSet |= predDict[miRNA]
		totalUnionGeneSet |= unionGeneSet & deg_set
		first_filtered_dict[miRNA] = unionGeneSet & deg_set


	for refseqID in raw_mRNAdict.keys():
		geneSymbol = refseqID2geneSymbol_dict[refseqID]
		if geneSymbol in totalUnionGeneSet:
			filtered_mRNAdict[refseqID] = raw_mRNAdict[refseqID]



	return first_filtered_dict, filtered_mRNAdict



