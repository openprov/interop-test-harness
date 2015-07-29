"""Replace values in a YAML file.

Usage::

    usage: set_yaml_value.py [-h] file replacements [replacements ...]

    Replace values in a YAML file

    positional arguments:
      file          File
      replacements  Replacements of form NAME=VALUE where name is a path of keys
                    through a YAML file e.g.
                    comparators.ProvPyComparator.executable

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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import os
import yaml

def replace_value(key, value, content):
  """
  Replace value in a multi-dimensional dict given a fully-qualified
  path to the value to be replaced e.g. calling::

    replace_value('comparators.ProvPyComparator.executable', 
                  'run',
                  content)

  is equivalent to doing::

    content['comparators']['ProvPyComparator']['executable'] = 'run'

  If there is no matching key then this is a no-op.

  :param key: Fully-qualified key
  :type key: str or unicode
  :param value: Replacement value
  :type value: str or unicode
  :param content: Dictionary in which value is to be updated
  :type content: dict
  """
  key_path = key.split(".")
  replace_key = key_path.pop()
  sub_content = content
  for k in key_path:
    if k not in sub_content:
      return
    sub_content = sub_content[k]
  if replace_key not in sub_content:
      return
  sub_content[replace_key] = value

def set_yaml_value(file_name, replacements):
  """
  Replace values in a YAML file. Each replacement value is of form
  ``NAME=VALUE`` where ``NAME`` is a path of keys through a YAML file
  e.g. ``comparators.ProvPyComparator.executable`` and ``VALUE``
  is a replacement value for the current value of the final key in
  the path.

  :param file_name: File name
  :type file_name: str or unicode
  :param replacements: Replacement values
  :type replacements: list of str or unicode
  """
  with open(file_name, 'r') as f:
    content = yaml.load(f)

  for replacement in replacements:
    [key,value] = replacement.split("=", 1)
    replace_value(key, value, content)

  with open(file_name, 'w') as f:
    f.write(str(yaml.safe_dump(content)))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Replace values in a YAML file")
  parser.add_argument("file", help="File")
  parser.add_argument(
    "replacements", 
    nargs="+", 
    help="Replacements of form NAME=VALUE where name is a path of keys through a YAML file e.g. comparators.ProvPyComparator.executable")
  args = parser.parse_args()
  set_yaml_value(args.file, args.replacements)
