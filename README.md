Introduction
============

Installation
============

PreReq:

- CipresSubmit (Installed and configured for your system) : https://github.com/bryan-lunt/CipresSubmit 
- git

Installation:

For each benchmarking task, you can clone the CipresBenchmark git repository:
	git clone git@github.com:bryan-lunt/CipresBenchmark.git MyBenchmarks

This will create everything necessary to begin benchmarking, but some settings will not be in-place.

Configuration:
	You will need to add the script "submit.py" from CipresSubmit to your path, either globally (.profile) or in the script ./bin/START.bash in the CipresBenchmark directory.

	Depending on your system, you _may_ need to alter the templates that come with CipresBenchmark .

	You might consider saving these edited configurations in a local copy of the CipresBenchmark git repository, and cloning from that for every new benchmarking task.
	Make sure to keep it up to date with updates on the main repo!

Writing Benchmarks
==================





File hierarchy:

	scripts: Put on the path for the benchmark job. Put either scripts you need, or symbolic links to other stuff you need here.
	templates: Overrides the templates from CipresSubmit . You probably don't need to alter these, but these are the templates your benchmark jobs will use, including various benchmarking stuff.
	output: Each job will get a directory here.
	inputs: Input files will be copied from here.
	benchmarks: Put modules containing benchmarks here.	
