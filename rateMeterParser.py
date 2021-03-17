#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import io
from argparse import ArgumentParser
import glob
import os
import sys
import numpy as np
import math

args = ArgumentParser('./rateMeterParser.py', description='''This script is designed to take an output file from the RateMeter and output a csv file
with the average rate per minute.
Example usage: ./rateMeterParser.py -i "r1234_VTA_GABA.txt" -o r1234''')

args.add_argument(
	'-i',
	'--input_file',
	help="""This is the file output by the RateMeter. If spaces are in the name, make sure you put the name in quotes.""",
	default=None,
)

args.add_argument(
	'-o',
	'--output_prefix',
	help="""This is the name you would like to use as the prefix to the output files. By default, the prefix will be 'RateMeter' output files will be 'RateMeter_Per_Minute.csv'
	and 'RateMeter_Per_Ten_Seconds.csv' with no prefix.""",
	default="RateMeter",
)

def error_message():
	print()
	print("""\tWelcome to rateMeterParser.py. This program has been designed to take an output file from the RateMeter and output a csv file
	with the average rate per minute. Example usage: ./rateMeterParser.py -i 'r1234_VTA_GABA.txt' """)
	print()

args = args.parse_args()
if args.input_file == None:
	error_message()
	print("\tNo input file was entered. Please add a config file using the -i option.")
	txt_files =glob.glob('*.txt')
	if len(txt_files) == 0:
		print("\tNo .txt files were present in your working directory.")
	else:
		print("\tText files in your present working directory are:")
		for file in txt_files:
			print("\t\t"+file)
	print()
	sys.exit(1)

input_file = args.input_file
output_prefix = args.output_prefix

data_lines = []
with io.open(input_file, 'r', encoding='windows-1252') as file:
	state = False
	start_line = 100
	for i, line in enumerate(file):
		if line.startswith('Time'):
			header_line = line.split('\t')[0:-1]
			start_line = i
		if i == (start_line+2):
			state = True
		if state == True:
			data_lines.append(line.split('\t')[0:-1])

dataframe = pd.DataFrame(data_lines)
dataframe.columns = header_line
first_two_rows = dataframe[['Time (sec)', 'rate']]
first_two_rows = first_two_rows.set_index('Time (sec)')
first_two_rows.to_csv(output_prefix+'_Per_Ten_Seconds.csv')

# Now I want to get the average, standard deviation and standard error per minute
# The first line will be NaN because it combines the first time (time 0) with 5 non-existent lines.

df = dataframe[dataframe.index > 0]
# Now use this and loop through each six values
minute = 1
i = 0
results = []
rates = []
for rate in df['rate'].values:
	if i < 6:
		rates.append(float(rate))
		i += 1
	elif i == 6:
		avg = np.mean(rates)
		stdev = np.std(rates)
		stderr = stdev/(math.sqrt(6))

		tmp_dict = {'Minute': minute,
			'Average': avg,
			'Standard Deviation': stdev,
			'Standard Error (Error Bar)': stderr}
		results.append(tmp_dict)
		minute += 1
		rates = [float(rate)]
		i = 1

# There will typically be some readings that didn't complete a the i ==6 part of the loop
if len(rates) > 0:
	avg = np.mean(rates)
	stdev = np.std(rates)
	stderr = stdev/(math.sqrt(len(rates)))
	tmp_dict = {'Minute': minute,
		'Average': avg,
		'Standard Deviation': stdev,
		'Standard Error (Error Bar)': stderr}
	results.append(tmp_dict)

# Now put it into a dataframe and save it
minutes_df = pd.DataFrame(results)
minutes_df = minutes_df.set_index('Minute')
minutes_df.to_csv(output_prefix+'_Per_Minute.csv')
