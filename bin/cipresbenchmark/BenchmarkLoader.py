'''
Created on Dec 31, 2013

This code is, conceptually, copied from : https://pypi.python.org/pypi/discover

@author: lunt
'''
from __future__ import print_function

import sys as _sys
import os as _os
import imp as _imp
from cipresbenchmark import Benchmark, Disabled

def load_benchmarks_from_module(module):
	"""
	Searches a module object for all proper-subclasses of Benchmark.
	Creates an instance of each of those classes and returns a list of those instances.
	
	@param module: A module object that may contain subclasses of cipresbenchmark.Benchmark
	
	@return: A list containing instances of all sub-classes of cipresbenchmark.Benchmark contained in module
	
	@raise Exception: If a sub-class is found but cannot be instantiated, or module is invalid, etc
	
	"""
	benchmarks = list()
	
	for name in dir(module):
		obj = getattr(module, name)
		#Benchmark is a subclass of Benchmark, so make sure _not_ to instantiate that.
		#It WILL be present in most modules that contain a sub-class (unless the programmer was cleaver, never require the end user to be cleaver.).
		if isinstance(obj, type) and issubclass(obj, Benchmark) and not obj is Benchmark:
			if not hasattr(obj,"disabled") or not obj.disabled:
				benchmarks.append(obj())
	
	return benchmarks

def load_benchmarks_from_path(benchpath):
	"""
	Load modules from the directory "benchpath" and instantiate all cipresbenchmark.Benchmark subclasses from there.
	Does not recurse into subdirectories.
	
	
	@param benchpath: The path to search for python modules containing subclasses of cipresbenchmark.Benchmark
	@type benchpath: str
	
	@return: A list of instances of subclasses of cipresbenchmark.Benchmark
	
	@raise Exception: Passes some internal exceptions through, does not raise an exception if there is a python module that cannot be loaded/parsed.
	
	"""
	benchmarks = list()
	
	
	allpaths = _os.listdir(benchpath)
	for onepath in allpaths:
		full_path = _os.path.join(benchpath,onepath)
		if _os.path.isfile(full_path) and full_path.endswith(".py"):
			try:
				mymodule = _imp.load_source('benchmarks__' + onepath.replace('.py',''),full_path)
				benchmarks.extend(load_benchmarks_from_module(mymodule))
			except Exception as e:
				print("There was an error : ", e, file=_sys.stderr)
	
	return benchmarks