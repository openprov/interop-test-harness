"""Dummy ProvPy ``prov-compare`` which mimics the behaviour of 
ProvPy ``prov-compare``. 

``prov-compare`` returns 2 if: 

- No files.
- Files are not valid PROV documents.

``prov-compare`` returns 1 if: 

- Files are valid PROV documents but not equivalent.

``prov-compare`` returns 0 if: 

- Files are valid PROV documents and are equivalent.

This script behaves similarly (though it does no PROV validation). 

If the inputs and formats are valid and the file names have
the same contents then it returns 0 else it returns 1

Usage::

    usage: prov_compare_dummy.py [-h] -f [FORMAT] infile outfile

    Dummy ProvPy prov-compare.

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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import filecmp
import os
import shutil
import sys

def compare(file1, format1, file2, format2):
  """
  Mimic `prov-compare` behaviour.

  :param file1: File
  :type file1: str or unicode
  :param format1: `file1` format
  :type format1: str or unicode
  :param file2: File
  :type file2: str or unicode
  :param format2: `file2` format
  :type format2: str or unicode
  """
  for file_name in [file1, file2]:
    if not os.path.isfile(file_name):
      print(("No such file " + file_name))
      sys.exit(2)
  formats = ["xml", "json"]
  for format in [format1, format2]:
    if format not in formats:
      # Unsupported format
      sys.exit(2)
  if not filecmp.cmp(file1, file2, shallow=False):
    # Documents do not match
    sys.exit(1)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Dummy ProvPy prov_compare.")
  parser.add_argument("-f", metavar="FORMAT1",
                      help="File 1 format - one of xml, json", 
                      nargs="?", 
                      required=True)
  parser.add_argument("-F", metavar="FORMAT2", 
                      help="File 2 format - one of xml, json", 
                      nargs="?", 
                      required=True)
  parser.add_argument("file1", help="File 1")
  parser.add_argument("file2", help="File 2")
  args = parser.parse_args()
  compare(args.file1, args.f, args.file2, args.F)
  sys.exit(0)
