"""Dummy ProvPy prov-compare. 
Mimics the behaviour of ProvPy prov-compare. 

prov-compare returns 2 if: 
- No files.
- Files are not valid PROV documents.

prov-compare returns 1 if: 
- Files are valid PROV documents but not equivalent.

prov-compare returns 0 if: 
- Files are valid PROV documents and are equivalent.

This script behaves similarly (though it does no PROV validation). 

If the inputs and formats are valid and the file names (after removal
of their extensions) are equal then it returns 0 else it returns 1
(mimicing two non-equivalent files).

Usage:

    usage: prov-compare-dummy.py [-h] -f [FORMAT] infile outfile

    Mock ProvPy prov-compare.

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

parser = argparse.ArgumentParser(description="Dummy ProvPy prov-compare.")
parser.add_argument("-f", metavar="FORMAT1",
                    help="File 1 format - one of xml, json", 
                    nargs="?", 
                    required=True)
parser.add_argument("-F", metavar="FORMAT2", 
                    help="Fole 2 format - one of xml, json", 
                    nargs="?", 
                    required=True)
parser.add_argument("file1", help="File 1")
parser.add_argument("file2", help="File 2")
args = parser.parse_args()
print("Running dummy ProvPy prov-compare...")
for file_name in [args.file1, args.file2]:
  if not os.path.isfile(file_name):
    print("No such file " + file_name)
    sys.exit(2)
formats = ["xml", "json"]
for format in [args.f, args.F]:
  if format not in formats:
    print("Unsupported format " + format)
    sys.exit(2)
name1, _ = os.path.splitext(args.file1)
name2, _ = os.path.splitext(args.file2)
if name1 != name2:
  print("Documents do not match")
  sys.exit(1)
sys.exit(0)
