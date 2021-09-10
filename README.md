CipresBenchmark
============

## Introduction ##
This group of programs facilitates benchmarking (other) programs on queued cluster systems (such as those that use PBS/Torque or SGE/Open Grid Engine).

Along with the CipresSubmit ( https://github.com/bryan-lunt-supercomputing/CipresSubmit ) I hope these programs will take a lot of the drudgery and the potential for misplaced input files, etc out of benchmarking.

This tool is intended to make preparing benchmarks similar to the process of preparing unit-tests. It should make benchmarks similarly reproducible.
 

## Installation ##

### Requirements ###

- CipresSubmit (Installed and configured for your system) : https://github.com/bryan-lunt-supercomputing/CipresSubmit 
- git

### Installation ###

For each benchmarking project (potentially composed of multiple benchmarks (each composed of multiple runs)), you can clone the CipresBenchmark git repository:
	git clone git@github.com:bryan-lunt/CipresBenchmark.git MyBenchmarks

This will create everything necessary to begin benchmarking, but some settings will not be in-place.

### Configuration ###
You will need to add the script "submit.py" from CipresSubmit to your path, either globally (.profile) or in the script ./bin/START.bash in the CipresBenchmark directory.

Depending on your system, you _may_ need to alter the templates that come with CipresBenchmark .

You might consider saving these edited configurations in a local copy of the CipresBenchmark git repository, and cloning from that for every new benchmarking task.
Make sure to keep it up to date with updates on the main repo!

## Writing Benchmarks ##

Benchmarks are created by writing a python class that extends the "cipresbenchmark.Benchmark" class, and overwriting the "setUp(self)" method. Multiple benchmarks can be stored in the same module.

Benchmarks take the cartesian product of all values of their variables and input, so a simple benchmark file can run several possible combinations of inputs.

See the file ./benchmarks/example.py for an example.

### Name of benchmark ###
A benchmark is named for its class name.

### Benchmark setup ###
Implement the "setUp(self)" method of your benchmark class, and make calls to:

- self.setInput(file_or_directory_name)
- self.addVar(variable_name,variable_value)
- self.setCommandline("This is a python format string, it should used named formats that use the names of the variables you defined. %(I)i")

#### Setting Inputs ####
The method "cipresbenchmark.Benchmark.setInput(self, inputs)" sets the input(s) for a benchmark.
- A single string gives the name of a single file or directory (for multiple input files that need to be grouped) that should be copied out of the ./inputs directory into the working directory of the benchmark job.
- A list of strings give multiple files to each be treated as above in their respective jobs.

#### Setting Variables ####
The method "cipresbenchmark.Benchmark.setVar(self, name, value)" sets variables to be used in formatting the command-line.
- A single value (string, int, float, etc) can be assigned to this variable name.
- A list of values can be assigned, in which case every combination of this variable's values will be used in Cartesian Product with all input values and all values of all other variables.
- A funtion that calculates a variable from all variables so far can be provided. For details please examine the code of "cipresbenchmark.Benchmark"

#### Setting the Commandline ####
The method "cipresbenchmark.Benchmark.setCommandline(self, cmdline_str)" is used to provide a template to use for the commandline.
The template is a python template string, using named template values " like this %(I)i ". It's provided with all of the variable values, including those reserved for CipresSubmit (such as "mpi_processes" etc.).
The input file (or directory) is copied into the run directory as "INPUT".

## Running Benchmarks ##
Run the script ./bin/START.bash and it will submit all benchmarks that are not disabled with the "cipresbenchmark.Benchmark.Disabled" annotation.
This also lets you start a few benchmarks sequentially or add more later, or whatever. See the example benchmark.

## Getting Results ##
Once benchmarks are finished, running the ./bin/RESULTS.bash file will result in a directory called "reports" containing Comma Separated Values files, one for each benchmark.
These files have a header line that describes their contents, which is all veriables, the total number of cores, and the final command-line used. It should be appropriate for direct use with most spreadsheet and plotting softare.

### Gnuplot commands to use these files ###
	set datafile commentschars "#!%"
	set datafile separator ","


## File hierarchy ##

	scripts: Put on the path for the benchmark job. Put either scripts you need, or symbolic links to other stuff you need here.
	templates: Overrides the templates from CipresSubmit . You probably don't need to alter these, but these are the templates your benchmark jobs will use, including various benchmarking stuff.
	output: Each job will get a directory here.
	inputs: Input files will be copied from here.
	benchmarks: Put modules containing benchmarks here.

## License ##
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

