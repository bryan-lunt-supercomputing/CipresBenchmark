#!/usr/bin/env python
'''
Created on Jan 23, 2014

@author: Bryan Lunt <blunt@sdsc.edu>
'''
from __future__ import print_function

import cipresbenchmark.BenchmarkLoader as BL

import argparse
import sys
import os
import re
import json

import csv

import sqlite3

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--sqlitefile", default=":memory:")
	args = parser.parse_args()
	
	script_abs_path = os.path.realpath(__file__)
	script_abs_dir  = os.path.dirname(script_abs_path)
	benchmark_system_dir   = os.path.realpath(os.path.join(script_abs_dir,'..'))
	
	#setup directories
	output_dir = os.path.join(benchmark_system_dir,"output")
	input_dir  = os.path.join(benchmark_system_dir,"inputs")
	benchmark_dir = os.path.join(benchmark_system_dir,"benchmarks")
	report_dir = os.path.join(benchmark_system_dir, "reports")
	try:
		os.mkdir(report_dir)#make sure that such a directory exists
	except:
		pass
	
	
	MemDB = sqlite3.connect(args.sqlitefile)
	
	
	#load all benchmarks (We need this in order to build the table)
	benchmarks = BL.load_benchmarks_from_path(benchmark_dir)
	
	for onebench in benchmarks:
		onebench.setUp();
		#create an appropriate table to hold the results of this benchmark (Since each benchmark has different parameters, we can't just use one format, unless we want to sacrifice the ability to have a variable be a column.
		
		NAME = onebench.name
		varnames = onebench.getVarnames()
		
		
		schemaString = "create table %s( %s, UUID, EXECUTION_TIME, CORES, COMMANDLINE varchar);" % (NAME, ",".join(varnames) )
		MemDB.execute(schemaString)
		
		individual_outputs = [i for i in os.listdir(output_dir) if i.startswith(NAME + "_") and os.path.isdir(os.path.join(output_dir, i))]
		for one_output in individual_outputs:
			UUID = re.sub('.*__','',one_output)
			
			start = 0
			end = 0
			try:
				with open(os.path.join(output_dir, one_output,'start.txt')) as startfile:
					start = int(startfile.read())
			except:
				print("JOB: ", one_output, " not started", file=sys.stderr)
				continue
			
			try:
				with open(os.path.join(output_dir, one_output,'done.txt')) as endfile:
					end = int(endfile.read())
			except:
				print("JOB: ", one_output, " not finished", file=sys.stderr)
				continue
			
			EXECUTION_TIME = end - start
			
			with open(os.path.join(output_dir, one_output, 'PARAMETERS.json')) as paramfile:
				other_parameters = json.load(paramfile)
			
			all_params = dict()
			all_params.update(other_parameters)
			all_params['EXECUTION_TIME'] = EXECUTION_TIME
			all_params['UUID'] = UUID
			all_params['CORES'] = int(all_params.get('mpi_processes',1))*int(all_params.get('threads_per_process',1))
			all_params.pop("NAME")
			
			all_names = all_params.keys()
			all_values = ['"' + str(all_params[i]) + '"' for i in all_names]
			
			insertString = "insert into %s( %s ) values ( %s )" % ( NAME, ','.join(all_names), ','.join(all_values))
			MemDB.execute(insertString)
		
		#Prepare a .csv report
		#TODO finish this.
		with open(os.path.join(report_dir,NAME + ".csv"),"w") as one_report:
			#print commented header
			
			
			print("#%s" % (','.join(varnames))," UUID, EXECUTION_TIME, CORES, COMMANDLINE", file=one_report)
			
			
			#begin writing results
			mywriter = csv.writer(one_report)
			
			myResults = MemDB.execute("select * from %s;" % (NAME))
			
			for one_result in myResults:
				mywriter.writerow(one_result)
			
	

if __name__ == "__main__":
	main()