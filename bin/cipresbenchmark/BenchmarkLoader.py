'''
Created on Dec 31, 2013

This code is, conceptually, blatantly copied from : https://pypi.python.org/pypi/discover

@author: lunt
'''

import os
import imp
from cipresbenchmark import *

def loadBenchmarksFromModule(module):
	benchmarks = list()
	
	for name in dir(module):
		obj = getattr(module, name)
		if isinstance(obj, type) and issubclass(obj, Benchmark) and not obj is Benchmark:
			benchmarks.append(obj())
	
	return benchmarks

def loadBenchmarksFromPath(benchpath):
	benchmarks = list()
	
	
	allpaths = os.listdir(benchpath)
	for onepath in allpaths:
		full_path = os.path.join(benchpath,onepath)
		if os.path.isfile(full_path):
			try:
				mymodule = imp.load_source('ANONYMOUS',full_path)
				benchmarks.extend(loadBenchmarksFromModule(mymodule))
			except:
				pass
	
	return benchmarks