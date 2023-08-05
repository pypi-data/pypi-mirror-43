"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mmirtime` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``mirtime.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``mirtime.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

import mirtime

parser = argparse.ArgumentParser(description='MicroRNA target prediction using time-series data.')
parser.add_argument('-i', '--mirna', required=True, help='miRNA expression profile file directory')
parser.add_argument('-m', '--mrna', required=True, help='mRNA expression profile file directory')
parser.add_argument('-l', '--mirlist', required=True, help='File path of miRNA of interests')
parser.add_argument('-t', '--seqtype', required=True, help='Sequencing type of expression profiles')
parser.add_argument('-s', '--size', required=True, help='Number of targets per miRNA')
parser.add_argument('-o', '--output', required=True, help='Output file tag')
parser.add_argument('-p', '--tepath', required=True, help='Path where TargetExpress.pl is located')


def main(args=None):
	args = parser.parse_args(args=args)
	mirtime.run_mirtime(args.mirna, args.mrna, args.mirlist, args.seqtype, args.size, args.output, args.tepath)
