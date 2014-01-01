#!/usr/bin/env python
'''
Created on Dec 31, 2013

@author: Bryan Lunt <blunt@sdsc.edu>
'''

BENCHMARKDIR="./benchmarks"
OUTPUTDIR="./output"
INPUTDIR="./inputs"

SUBMIT_PY = "submit.py"

from cipresbenchmark import setup_rundir, submit_benchmark
import cipresbenchmark.BenchmarkLoader as BL
import argparse
import shutil
import os

def main():
	parser = argparse.ArgumentParser()
	#parser.add_argument("inputfile", metavar='FILE', type=str, help='Input file to benchmark')
	args = parser.parse_args()
	
	benchmarks = BL.loadBenchmarksFromPath(BENCHMARKDIR)
	
	
	#TODO: find out what resource we're on? Or should that be part of benchmark?
	
	
	for onebench in benchmarks:
		onebench.setUp()
		realizations = onebench.get_all()
		print onebench.name, len(realizations)
		for one_realization in realizations:
			print one_realization
			#setup the rundirectory with all files
			submit_directory = setup_rundir(OUTPUTDIR,one_realization)
			
			#Copy in the input
			#TODO: Replace with symbolic link?
			shutil.copy(os.path.join(INPUTDIR,one_realization['INPUT']), os.path.join(submit_directory,"INPUT"))
			
			#TODO: Submit the job
			submit_benchmark(submit_directory, one_realization['COMMANDLINE'],submitbinary=SUBMIT_PY)


if __name__ == '__main__':
	main()