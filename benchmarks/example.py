'''
Created on Dec 31, 2013

@author: lunt
'''

from  cipresbenchmark import Benchmark

class Example(Benchmark):
	def setUp(self):
		self.setName("EXAMPLE")
		self.setInput("baz")
		self.addVar("I", [1,2,3,4,5])
		self.setCommandline("echo %(I)i")
		self.addVar('resource','gordon')
		self.addVar('mpi_processes',16)