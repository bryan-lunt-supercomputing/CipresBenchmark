'''
Created on Dec 31, 2013

@author: lunt
'''

#TODO: Example should contain a list of all the necessary elements of _JOBINFO and scheduler.conf

from  cipresbenchmark import Benchmark

class Example(Benchmark):
	def setUp(self):
		self.setName("EXAMPLE")
		self.setInput("baz")
		
		self.addVar("runhours",20)
		
		self.addVar("I", [1,2,3,4,5])
		self.addVar('resource','gordon')
		self.addVar('mpi_processes',16)
		
		
		self.setCommandline("echo %(I)i")