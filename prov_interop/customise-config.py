"""Copy files/directories, replacing tokens with values in the process.

Usage::

    usage: customise-config.py [-h] original copy replacements

    Copy file/directory of files and replace tokens

    positional arguments:
      original      Original file/directory
      copy          Output file/directory
      replacements  File of TOKEN=VALUE pairs, one on each line

    optional arguments:
      -h, --help    show this help message and exit
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

def customise_file(old_file_name, new_file_name, replacements):
  old_file = open(old_file_name,"r")
  new_file = open(new_file_name, "w")
  for line in old_file:
    new_line = line
    for old in replacements:
      if old in line:
        new_line = new_line.replace(old, replacements[old])
    new_file.write(new_line)
  new_file.close()
  old_file.close()

parser = argparse.ArgumentParser(
    description="Copy file/directory of files and replace tokens")
parser.add_argument("original", help="Original file/directory")
parser.add_argument("copy", help="Output file/directory")
parser.add_argument("replacements", help="File of TOKEN=VALUE pairs, one on each line")
args = parser.parse_args()
original = args.original
copy = args.copy

replacements = {}
with open(args.replacements) as f:
  for line in f:
    line = line.rstrip()
    [old, new] = line.split("=")
    replacements[old] = new

if os.path.isfile(original):
  customise_file(original, copy, replacements)
else:
  if not os.path.isdir(copy):
    os.mkdir(copy)
  for f in os.listdir(original):
    file_name = os.path.join(original, f)
    if os.path.isfile(file_name):
      customise_file(file_name, os.path.join(copy, f), replacements)
