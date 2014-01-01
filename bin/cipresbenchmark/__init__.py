'''
Created on Dec 31, 2013

@author: Bryan Lunt <blunt@sdsc.edu>
'''

scheduler_conf_varnames = ["jobtype", "mpi_processes","threads_per_process","runhours","node_exclusive","nodes","ppn","queue"]
jobinfo_txt_varnames = ["Task label", "Task ID", "Tool", "created on","JobHandle","User ID","User Name", "email","JOBID", "resource"]

from itertools import product as cartprod

class Benchmark(object):
	def __init__(self):
		self.name = None
		self.INPUT = None
		self.COMMANDLINE = None
		self.vars = dict()
		self.varfuncs = list()
	
	def setUp(self):
		print "NOT VIRTUAL!?!?!"
		pass
	
	def setName(self,name):
		self.name = name
		
	def addVar(self, name, value):
		if hasattr(value, '__call__'):
			self.varfuncs.append((name, value))
		else: #Not a callable
			if isinstance(value, list) or isinstance(value, tuple):
				self.vars[name] = list(value)
			else: #Singular
				self.vars[name] = [value]
	
	def setInput(self, inputname):
		self.INPUT = inputname
		self.addVar("INPUT",inputname)
	
	def setCommandline(self,template):
		self.COMMANDLINE = template
	
	def get_all(self):
		
		assert self.COMMANDLINE is not None, "No COMMANDILNE provided"
		assert self.INPUT is not None, "No INPUT provided"
		assert self.name is not None, "No Name?"
		
		names = self.vars.keys()
		values = [self.vars[n] for n in names]
		
		names = ['NAME'] + names
		values = [[self.name]] + values
		
		def todict(names, one_tup):
			return dict(zip(names, one_tup))
		
		benchdicts = [todict(names, i) for i in cartprod(*values)]
		
		for funcname, funcfunc in self.varfuncs:
			for onedict in benchdicts:
				onedict[funcname] = funcfunc(onedict)
		
		#templatize the commandline
		for onedict in benchdicts:
			onedict['COMMANDLINE'] = self.COMMANDLINE % onedict
		
		return benchdicts


def __comment_property_name(instr):
	return instr.replace(" ", "\ ")

import os
import time
import uuid
import json
def setup_rundir(top_directory,parameter_dict):
	myUUID = uuid.uuid1()
	timestr = time.strftime("%Y_%m_%d_%H:%M",time.localtime())
	outdirname = "%s_%s__%s__%s" % (parameter_dict['NAME'],parameter_dict['INPUT'], timestr, myUUID)
	full_outdirname = os.path.join(top_directory, outdirname)
	
	os.mkdir(full_outdirname)
	
	#Dump the dictionary
	with open(os.path.join(full_outdirname, "PARAMETERS.json"),"w") as dumpjsonfile:
		json.dump(parameter_dict, dumpjsonfile,indent=1)
		dumpjsonfile.write("\n")
		
	#Create the _JOBINFO.TXT
	with open(os.path.join(full_outdirname, "_JOBINFO.TXT"),"w") as JOBINFOFILE:
		for ji_name in jobinfo_txt_varnames:
			if parameter_dict.has_key(ji_name):
				JOBINFOFILE.write("%s=%s\n" % (__comment_property_name(ji_name), parameter_dict[ji_name]) )
				
	#Create the scheduler.conf
	with open(os.path.join(full_outdirname,"scheduler.conf"),"w") as SCHEDULER_CONF:
		for sc_name in scheduler_conf_varnames:
			if parameter_dict.has_key(sc_name):
				SCHEDULER_CONF.write("%s=%s\n" % (__comment_property_name(sc_name), parameter_dict[sc_name]) )
	
	#Create the COMMANDLINE
	with open(os.path.join(full_outdirname,"COMMANDLINE"),"w") as COMMANDLINE_FILE:
		COMMANDLINE_FILE.write("%s\n" % (parameter_dict['COMMANDLINE']) )
	
	return full_outdirname
	
def submit_benchmark(submit_directory,COMMANDLINE):
	pass