#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import io
from argparse import ArgumentParser
import glob
import os
import sys

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

df = dataframe.rolling(6).mean()
df = df.iloc[::6, :]
# The first line will be NaN because it combines the first time (time 0) with 5 non-existent lines.
# That line will be removed later, but it works well for combining only times 10s-60s and not 0s-50s

def get_minute(df):
	index = df.name
	minute = index/6
	df['Minute'] = minute
	return df

df = df.apply(get_minute, axis = 1)
df = df[df['Minute'] > 0]
df = df[['Minute', 'rate']].set_index('Minute')
df.to_csv(output_prefix+'_Per_Minute.csv')
