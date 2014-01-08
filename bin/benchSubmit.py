#!/usr/bin/env python
'''
Created on Dec 31, 2013

@author: Bryan Lunt <blunt@sdsc.edu>
'''
from __future__ import print_function

SUBMIT_PY = "submit.py"

from cipresbenchmark import setup_rundir, submit_benchmark, create_cipressubmit_cfg
import cipresbenchmark.BenchmarkLoader as BL
import argparse
import shutil
import os



def main():
	parser = argparse.ArgumentParser()
	#parser.add_argument("inputfile", metavar='FILE', type=str, help='Input file to benchmark')
	args = parser.parse_args()
	
	script_abs_path = os.path.realpath(__file__)
	script_abs_dir  = os.path.dirname(script_abs_path)
	benchmark_system_dir   = os.path.realpath(os.path.join(script_abs_dir,'..'))
	
	#setup directories
	output_dir = os.path.join(benchmark_system_dir,"output")
	input_dir  = os.path.join(benchmark_system_dir,"inputs")
	benchmark_dir = os.path.join(benchmark_system_dir,"benchmarks")
	
	#load all benchmarks
	benchmarks = BL.loadBenchmarksFromPath(benchmark_dir)
	
	
	#TODO: find out what resource we're on? Or should that be part of benchmark?
	
	
	for onebench in benchmarks:
		onebench.setUp()
		realizations = onebench.get_all()
		print( "NAME: %s Number of tests: %i" % ( onebench.name, len(realizations)) )
		for one_realization in realizations:
			print( one_realization )
			#setup the rundirectory with all files
			submit_directory = setup_rundir(output_dir,one_realization)
			
			#Copy in the input
			#TODO: Use a symbolic link to the input? That might save on disk-space.
			shutil.copy(os.path.join(input_dir,one_realization['INPUT']), os.path.join(submit_directory,"INPUT"))
			
			create_cipressubmit_cfg(submit_directory,benchmark_system_dir)
			
			submit_benchmark(submit_directory, one_realization['COMMANDLINE'],submitbinary=SUBMIT_PY)


if __name__ == '__main__':
	main()