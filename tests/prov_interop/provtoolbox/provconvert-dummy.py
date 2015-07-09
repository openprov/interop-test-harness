"""Dummy ProvToolbox provconvert. 
Mimics the behaviour of ProvToolbox prov-onvert. 

provconvert returns 1 if: 
- No input file.
- Input file is not a valid PROV document.
- Input format is not supported.

provconvert returns 0 if:
- Conversion is successful.
- Output file format is not supported.

For:
- No input file.
- Input file is not a valid PROV document.
- Input format is not supported.
- Output file format is not supported.

no output files are created.

This script behaves similarly (though it does no PROV validation). 

If the inputs are valid it just copies the input file to the output file. 

Usage:

    usage: provconvert-dummy.py -infile infile -outfile outfile

    Mock ProvToolbox provconvert.

    positional arguments:
      infile       Input file
      outfile      Output file

    optional arguments:
      -h, --help   show this help message and exit
"""
# Copyright (c) 2015 University of Southampton
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions: 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.  

import argparse
import os
import os.path
import shutil
import sys

parser = argparse.ArgumentParser(description="Dummy ProvToolbox provconvert.")
parser.add_argument('-infile', metavar="file", 
                    help="Input file",
                    nargs='?', 
                    required=True)
parser.add_argument('-outfile', metavar="file", 
                    help="Output file",
                    nargs='?', 
                    required=True)
args = parser.parse_args()
print("Running dummy ProvToolbox provconvert...")
if not os.path.isfile(args.infile):
  print("No such file " + args.infile)
  sys.exit(1)
formats = ["provn", "ttl", "rdf", "trig", "provx", "xml", "json"]
in_format = os.path.splitext(args.infile)[1][1:]
if in_format not in formats:
  print("Unsupported input file format " + in_format)
  sys.exit(1)
out_format = os.path.splitext(args.outfile)[1][1:]
if out_format not in formats:
  print("Unsupported output file format " + out_format)
  sys.exit(0)
shutil.copyfile(args.infile, args.outfile)
sys.exit(0)
