"""Dummy ProvPy prov-convert. 
Mimics the behaviour of ProvPy prov-convert. 

prov-convert returns 2 if: 
- No input file.
- Input file is not a valid PROV document.
- Output format is not supported.

prov-convert returns 0 if: 
- Conversion is successful.

For:

- Input file is not a valid PROV document.
- Output format is not supported.

provconvert creates an empty output file. 

This script behaves similarly (though it does no PROV validation). 

If the inputs are valid it just copies the input file to the output file. 

Usage:

    usage: prov-convert-dummy.py [-h] -f [FORMAT] infile outfile

    Mock ProvPy prov-convert.

    positional arguments:
      infile       Input file
      outfile      Output file

    optional arguments:
      -h, --help   show this help message and exit
      -f [FORMAT]  Output format - one of provn, xml, json
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
import shutil
import sys

parser = argparse.ArgumentParser(description="Dummy ProvPy prov-convert.")
parser.add_argument("-f", metavar="FORMAT", 
                    help="Output format - one of provn, xml, json", 
                    nargs="?", 
                    required=True)
parser.add_argument("infile", help="Input file")
parser.add_argument("outfile", help="Output file")
args = parser.parse_args()
print("Running dummy ProvPy prov-convert...")
if not os.path.isfile(args.infile):
  print(("No such file " + args.infile))
  sys.exit(2)
formats = ["provn", "xml", "json"]
if args.f not in formats:
  print(("Unsupported format " + args.f))
  with open(args.outfile, "w+"):
    pass
  sys.exit(2)
shutil.copyfile(args.infile, args.outfile)
sys.exit(0)
