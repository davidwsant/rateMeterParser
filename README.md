## rateMeterParser

Welcome to rateMeterParser.py. This program has been designed to take an output file from the RateMeter and output a csv file with the average rate per minute.

Example usage: ./rateMeterParser.py -i 'r1234 VTA GABA.txt' -o r1234

optional arguments:

  -i INPUT_FILE, --input_file INPUT_FILE

                        This is the file output by the RateMeter. If spaces are in the name, make
                        sure you put the name in quotes.

  -o OUTPUT_PREFIX, --output_prefix OUTPUT_PREFIX

                        This is the name you would like to use as the prefix to the output files. By default, 
                        the prefix will be 'RateMeter' output files will be 'RateMeter_Per_Minute.csv' and 
                        'RateMeter_Per_Ten_Seconds.csv' with no prefix.
