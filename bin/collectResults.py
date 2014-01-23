#!/usr/bin/env python
'''
Created on Jan 23, 2014

@author: Bryan Lunt <blunt@sdsc.edu>
'''
from __future__ import print_function

import argparse
import os
import json

import sqlite3

def main():
	parser = argparse.ArgumentParser()
	args = parser.parse_args()
	
	script_abs_path = os.path.realpath(__file__)
	script_abs_dir  = os.path.dirname(script_abs_path)
	benchmark_system_dir   = os.path.realpath(os.path.join(script_abs_dir,'..'))
	
	#setup directories
	output_dir = os.path.join(benchmark_system_dir,"output")
	input_dir  = os.path.join(benchmark_system_dir,"inputs")
	benchmark_dir = os.path.join(benchmark_system_dir,"benchmarks")
	
	
	MemDB = sqlite3.connect(":memory:")
	
	
	#load all benchmarks (We need this in order to build the table)
	benchmarks = BL.load_benchmarks_from_path(benchmark_dir)
	
	for onebench in benchmarks:
		print foobar
		#create an appropriate table to hold the results of this benchmark
		schemaString = "create table %s(INPUT varchar, COMMANDLINE varchar, UUID, %s, EXECUTION_TIME);" % (onebench.name, ",".join(onebench.getVarnames()))
		MemDB.execute(schemaString)
		
		import pdb
		pdb.set_trace()
		

if __name__ == "__main__":
	main()