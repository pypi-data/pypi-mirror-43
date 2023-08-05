# mirTime

A new pipeline, mirTime, that predicts microRNA targets by integrating sequence features and time-series expression
profiles in a specific experimental condition.

## Installation

```python
pip install mirtime
```

## Usage

mirTime supports command-line invocation as below:

```shell
usage: mirtime [-h] -i MIRNAFILEDIR -m MRNAFILEDIR -l MIRNALIST -t SEQTYPE -s CLUSTERSIZE -o OUTPUT -p TARGETEXPRESSPATH

optional arguments:
  -h, --help	show this help message and exit
  -i MIRNAFILEDIR, --mirna MIRNAFILEDIR	
		miRNA expression profile file directory
  -m MRNAFILEDIR, --mrna MRNAFILEDIR	
		mRNA expression profile file directory
  -l MIRNALIST, --mirlist MIRNALIST	
		File path of miRNA of interests
  -t SEQTYPE, --seqtype SEQTYPE
		Must be 'microarray' or 'rnaseq'. Sequencing type of expression profiles
  -s CLUSTERSIZE, --size CLUSTERSIZE	
		int, Number of targets per miRNA
  -o OUTPUT, --output OUTPUT
		Output file tag
  -p TARGETEXPRESSPATH, --tepath TARGETEXPRESSPATH
		Path where TargetExpress.pl is located
  
```

**MicroRNA/mRNA Files**, which are included in microRNA File Directory or mRNA File Directory given with `-i/--mirna` or `-m/--mrna` option must be formatted as below. The file name should be `repN_tpM.tsv`, where N and M should be int type and float type for each. N and M represent the Nth replication and the time point M of the data file. mRNA ID must be refseq ID, and miRNA ID must be miRBase ID. `mirtime` will simply ignore the header by skipping a single line.

microRNA File rep0_tp1.tsv in MIRNAFILEDIR:

    miRNA_ID	expression_value               # Header
    miRNA1	10
    miRNA2	20
    miRNA3	30
    ...

mRNA File rep2_tp3.tsv in MRNAFILEDIR:

    mRNA_ID	expression_value               # Header
    mRNA1	10
    mRNA2	20
    mRNA3	30
    ...


**MicroRNA list**, which should be given with `-l/--mirlist` option file must have the format below. Please be warned that this file should **not** have a header. miRNA ID must be miRBase ID.

    miRNA1
    miRNA2
    miRNA3
    ...



