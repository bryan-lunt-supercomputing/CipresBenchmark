'''
Created on Dec 31, 2013

@author: Bryan Lunt <blunt@sdsc.edu>
'''
from __future__ import print_function

scheduler_conf_varnames = ["jobtype", "mpi_processes","threads_per_process","runhours","node_exclusive","nodes","ppn","queue"]
scheduler_defaults = {}

jobinfo_txt_varnames = ["Task label", "Task ID", "Tool", "created on","JobHandle","User ID","User Name", "email","JOBID", "resource"]
jobinfo_defaults = {"Task label":"BenchmarkJob","JobHandle":"BenchmarkJob"}


from itertools import product as _cartprod

class Benchmark(object):
	"""
	Base class to store/handle benchmarks.
	
	To create a benchmark, you sub-class this in a module in the "./benchmarks" directory of your benchmark system.
	Then you override the "setUp" method in your subclass.
	
	See the included example "example.py"
	
	"""
	
	
	def __init__(self):
		self.name = self.__class__.__name__ #default to using the classname.
		self.INPUT = None
		self.INPUT_EXTENSION = ""
		self.COMMANDLINE = None
		self.vars = dict()
		self.varfuncs = list()
	
	def getVarnames(self):
		return self.vars.keys() + self.varfuncs.keys()
	
	def setUp(self):
		"""
		Users will override this method to create their benchmarks.
		
		In your own benchmark class, you override setUp(self) to set all the vars, name, parameters, etc etc.
		
		Do not override __init__
		
		"""
		print("NOT VIRTUAL!?!?!")
		pass
	
	def setName(self,name):
		"""
		Sets the name of this benchmark, must be a single str, not available to jobs.
		
		@param name: The name of the benchmark.
		@type name: str
		
		"""
		self.name = name
		
	def addVar(self, name, value):
		"""
		Adds a variable for benchmarking.
		
		
		Variables take three types:
		
		1) Simple: A single value, e.g. foo.addVar("I",1) or foo.addVar("myvariable", "hello world")
		
		2) Multiple: A list of values, e.g. foo.addVar("I", [1, 2, 3]) or foo.addVar('J', range(20)) or foo.addVar('K', ['this', 'is', 'a', 'test'])
		
		3) Callable: Anything that implements '__call__' (custom classes, a function, or just lambda x:....)
					Callables must: a) Take only one parameter (other than self?), which is a dict<str,obj> , the dictionary of all values so far.
									b) return a simple value in one of the supported types (str, int, float, or something with a good __repr__ method.)
					
					Callables are interpreted after all other parameters, and in the order they were added in. (So one can depend upon a previous one.)
		
		"""
		if hasattr(value, '__call__'):
			self.varfuncs.append((name, value))
		else: #Not a callable
			if isinstance(value, list) or isinstance(value, tuple):
				self.vars[name] = list(value)
			else: #Singular
				self.vars[name] = [value]
	
	def setInput(self, inputname):
		"""
		Input gets slightly special treatment.
		
		Having a special method also emphasizes that we are input-oriented. (Though input is not always even required.)
		"""
		self.INPUT = inputname
		self.addVar("INPUT",inputname)
	
	def setInputExtension(self,extension):
		"""
		Some programs to be benchmarked may demand that the input actually have a specific file-extension.
		
		AVOID USING WHEN POSSIBLE.
		
		@param extension: The file extension to use, must include any dot or other separator. e.g. ".xml"
		"""
		self.INPUT_EXTENSION = extension
	
	def setCommandline(self,template):
		"""
		Provide a template for the command-line. Currently, you MUST provide this as a python string-format type string, USING NAMED FORMAT.
		
		Example: "echo %(K)i" : Looks for a variable named 'K' in the parameter dictionary, and interprets it as an integer.
		
		There will be a file named "INPUT" (plus the file-extension, if any) in the run directory, this is _not_ a variable. The variable 'INTPUT' will give the original name, if that is somehow needed.
		
		
		"""
		self.COMMANDLINE = template
	
	def get_all(self):
		"""
		Executes the logic of this benchmark to create several parameter dictionaries that can be used to start benchmarks.
		
		@return: A list of dictionaries, each dictionary containing all the parameters for one benchmark run.
		@rtype: list
		
		"""
		
		assert self.COMMANDLINE is not None, "No COMMANDILNE provided"
		assert self.name is not None, "No Name?"
		
		names = self.vars.keys()
		values = [self.vars[n] for n in names]
		
		names = ['NAME'] + names
		values = [[self.name]] + values
		
		def todict(names, one_tup):
			return dict(zip(names, one_tup))
		
		benchdicts = [todict(names, i) for i in _cartprod(*values)]
		
		for funcname, funcfunc in self.varfuncs:
			for onedict in benchdicts:
				onedict[funcname] = funcfunc(onedict)
		
		#templatize the commandline
		for onedict in benchdicts:
			onedict['COMMANDLINE'] = self.COMMANDLINE % onedict
		
		return benchdicts

def Disabled(inclass):
	inclass.disabled = True
	return inclass

import os as _os
import time as _time
import uuid as _uuid
import json as _json
def _write_property_file(filename, parameter_names, parameter_defaults, parameter_dict):
	
	#Local anonymous function to.
	def _comment_property_name(instr):
		return instr.replace(" ", "\ ")
	
	with open(filename,"w") as PROPERTIESFILE:
		for prop_name in parameter_names:
			prop_value = parameter_dict.get(prop_name, parameter_defaults.get(prop_name, None))
			if prop_value is not None:
				PROPERTIESFILE.write("%s=%s\n" % (_comment_property_name(prop_name), prop_value))



def setup_rundir(top_directory,parameter_dict):
	"""
	Prepares a job directory for CipresSubmit. Returns the final path.
	
	This consists of:
		Creating the directory.
		Creating the properties files that CipresSubmit needs: '_JOBINFO.TXT' and 'scheduler.conf'.
			These are populated with default values, but any value can be overridden by specifying it in the benchmark object.
		Saving the commandline to the file "COMMANDLINE" for other debugging.
		
		It is left to other code to actually copy over the input file to the name 'INPUT'
	
	@param top_directory: The path to the top directory that will contain run-directories. Each job gets a new directory inside this.
	@type top_directory: str
	
	@param parameter_dict: A dict<str,obj> containing parameters for one benchmark
	@type parameter_dict: dict
	
	@return: The full (relative?) path to the job directory that was created.
	@rtype: str
	"""
	
	
	
	#Create the empty directory, giving it a meaningful, unique name.
	
	myUUID = _uuid.uuid1()											#Uniquely identify this job.
	timestr = _time.strftime("%Y_%m_%d_%H%M",_time.localtime())		#The creation time of the job.
	outdirname = "%s_%s__%s__%s" % (parameter_dict['NAME'],parameter_dict.get('INPUT', "NONE"), timestr, myUUID)
	full_outdirname = _os.path.join(top_directory, outdirname)
	
	_os.mkdir(full_outdirname)
	
	#Dump the dictionary
	with open(_os.path.join(full_outdirname, "PARAMETERS.json"),"w") as dumpjsonfile:
		_json.dump(parameter_dict, dumpjsonfile,indent=1)
		dumpjsonfile.write("\n")
		
	#Create the _JOBINFO.TXT
	JOBINFO_FILENAME = _os.path.join(full_outdirname, "_JOBINFO.TXT")
	local_jobinfo_defaults = dict()
	local_jobinfo_defaults.update(jobinfo_defaults)
	local_jobinfo_defaults['JobHandle'] = outdirname #Better default for JobHandle
	_write_property_file(JOBINFO_FILENAME,jobinfo_txt_varnames,local_jobinfo_defaults,parameter_dict)
	
	#Create the scheduler.conf
	SCHEDULER_CONF_FILENAME = _os.path.join(full_outdirname,"scheduler.conf")
	_write_property_file(SCHEDULER_CONF_FILENAME, scheduler_conf_varnames, scheduler_defaults, parameter_dict)
	
	#Create the COMMANDLINE
	with open(_os.path.join(full_outdirname,"COMMANDLINE"),"w") as COMMANDLINE_FILE:
		COMMANDLINE_FILE.write("%s\n" % parameter_dict['COMMANDLINE'] )
	
	return full_outdirname


def create_cipressubmit_cfg(submit_directory, benchmark_sys_dir):
	"""
	Creates a local 'cipressubmit.cfg' that overrides the global configuration for CipresSubmit, this allows you to use an existing (for example, production) installation of CipresSubmit.
	
	@param submit_directory: The path to a job directory.
	@type submit_directory: str
	
	@param benchmark_sys_dir: The top level _absolute_ path to where this particular set of benchmarks, are stored. (The directory that contains ./bin/ ./templates/ etc.)
	@type benchmark_sys_dir: str
	"""
	with open(_os.path.join(submit_directory, "cipressubmit.cfg"),"w") as cconfig_file:
		#overwrite the e-mail so that terry and mark don't get benchmarking e-mails
		print("[general]", file=cconfig_file)
		print("job_status_email=",file=cconfig_file)
		
		print("[templates]", file=cconfig_file)
		print("templatedir=%s"%_os.path.join(benchmark_sys_dir,"templates"), file=cconfig_file)
		
		#placeholder
		#print("[hosts]", file=cconfig_file)
		#print("#resourcexmldir=./hosts", file=cconfig_file)
		
		


import subprocess as _subprocess
def submit_benchmark(submit_directory,COMMANDLINE,submitbinary="submit.py"):
	"""
	Actually submit a benchmark, via CipresSubmit.
	
	@param submit_directory: The path to the job directory, which becomes the CWD when running CipresSubmit
	@type submit_directory: str
	
	@param COMMANDLINE: The commandline of the job you want to run.
	@type COMMANDLINE: str
	
	@param submitbinary: The name of the tool to use to submit, could be an absolute path or not. Defaults to "submit.py"
	@type submitbinary: str
	
	@raise AssertionError: Asserts false and kills everything if any benchmark fails to start.
	"""
	submitproc = _subprocess.Popen([submitbinary,"--", COMMANDLINE], stderr=_subprocess.PIPE, stdout=_subprocess.PIPE, cwd=submit_directory, shell=False)
	stdout, stderr = submitproc.communicate();
	if submitproc.returncode != 0:
		print(stdout)
		print("==========")
		print(stderr)
		assert False