"""Dummy ProvToolbox ``provconvert`` which mimics the behaviour of 
ProvToolbox ``prov-convert`` when used to compare files.

``provconvert`` returns 0 if:

- Files contain equivalent PROV documents.

``provconvert`` returns 1 if: 

- Either file cannot be found.
- Either file is not a valid PROV document.
- Either format is not supported.

``provconvert`` returns 6 if: 

- Files do not contain equivalent PROV documents.

This script behaves similarly (though it does no PROV validation). 

If the inputs and formats are valid and the file names have
the same contents then it returns 0 else it returns 1

Usage::

    usage: provconvert_dummy.py -infile file1 -compare file2

    Dummy ProvToolbox provconvert.

    positional arguments:
      file1      File 1
      file2      File 2

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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import filecmp
import os
import os.path
import shutil
import sys

def compare(file1, file2):
  """
  Mimic `provconvert` behaviour when comparing files.

  :param file1: File 1
  :type file1: str or unicode
  :param file2: File 2
  :type file2: str or unicode
  """
  formats = ["provn", "ttl", "rdf", "trig", "provx", "xml", "json"]
  for file_name in [file1, file2]:
    if not os.path.isfile(file_name):
      print(("No such file " + file_name))
      sys.exit(1)
    format = os.path.splitext(file_name)[1][1:]
    if format not in formats:
      # Unsupported input file format
      sys.exit(1)
  if not filecmp.cmp(file1, file2, shallow=False):
    # Documents do not match
    sys.exit(6)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Dummy ProvToolbox provconvert.")
  parser.add_argument('-infile', metavar="file", 
                      help="File 1",
                      nargs='?', 
                      required=True)
  parser.add_argument('-compare', metavar="file", 
                      help="File 2",
                      nargs='?', 
                      required=True)
  args = parser.parse_args()
  compare(args.infile, args.compare)
  sys.exit(0)
