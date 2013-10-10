#!/usr/bin/env python

import os
import sys
import argparse
import commands
import subprocess



def main(infile, min): 
	fw, rw, transcripts, experiment = file_reader(infile)
	print "Forward reads file: ", fw
	lines_fw = get_lines(fw)
	print "Reverse reads file: ", rw
	lines_rw = get_lines(rw)
	if not lines_fw[0] == lines_rw[0]: 
		print "forward and reverse fastq file do not match"
	print transcripts
	subset_list = get_subsets(lines_fw, transcripts, min)
	write_file(subset_list, fw, rw, experiment)


def write_file(fastq_list, fw, rw, name):
	i=1
	fw_files = []
	rw_files = []
	
	for subset in fastq_list:
		print "Writing subset " + str(i) + ", corresponding to " + str(int(subset)) + " fastq lines to file"
		p = subprocess.Popen(["head", "-n", str(int(subset)), fw], stdout=subprocess.PIPE)
		out = p.communicate()
		outfile = name + "_" + str(i) + "_R1.fastq"
		file_handle = open(outfile, "w")
		file_handle.write(repr(out))
		file_handle.close()
		fw_files.append(outfile)
		
		p = subprocess.Popen(["head", "-n", str(int(subset)), rw], stdout=subprocess.PIPE)
		out = p.communicate()
		outfile = name + "_" + str(i) + "_R2.fastq"
		file_handle = open(outfile, "w")
		file_handle.write(repr(out))
		file_handle.close()
		rw_files.append(outfile)
		
		i += 1
		
		print fw_files
		print rw_files
	

def get_lines(fastq_file): 
	lines = commands.getoutput('wc -l "%s"' % (fastq_file))
	lines = lines.split()
	print lines[0]
	return lines[0]

def get_subsets(lines, transcripts, min):
	subset_transcript_list = []
	subset_fastq_list = []
	subset = min
	lines_per_transcript = float(lines)/float(transcripts)
	print lines_per_transcript
	while subset < transcripts: 
		subset_transcript_list.append(subset)
		subset_fastq_list.append(subset * lines_per_transcript - ((subset * lines_per_transcript) % 4))
		subset = subset * 2
		
	print "This will create the following subsets: ", subset_transcript_list
	print "Corresponding to the following number of lines in a fastq file: ", subset_fastq_list
	continue_or_new_list = raw_input("Continue? Press yes to continue, or insert the subsets you want to use instead in a list format (e.g. 12 645 89357)")
	if continue_or_new_list == "yes":
		pass
	else:
		subset_fastq_list = continue_or_new_list.split()
	return subset_fastq_list


def file_reader(infile):
	print "Reading file: ", infile
	for ln in open(infile, 'r'): 
		if ln.startswith("Forward reads file"): 
			ln = ln.split(':')
			fw = ln[1].strip()
		elif ln.startswith("Reverse reads file"): 
			ln = ln.split(':')
			rw = ln[1].strip()
		elif ln.startswith("Number of Transcripts with Barcode present"): 
			ln = ln.split(':')
			transcripts = int(ln[1])
		elif ln.startswith("Experiment"): 
			ln = ln.split(':')
			experiment_name = ln[1].split()
			experiment_name = experiment_name[0]
		else:
			continue
	print "Done"
	return fw, rw, transcripts, experiment_name

if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-s', '--statsfile', help='Stat file for the experiment for which to create a diversity plot', required=True)
	parser.add_argument('-f', '--first', type=int, help='First datapoint')
	
	args = parser.parse_args()
	main(args.statsfile, args.first)