"""Functions to load `YAML <http://yaml.org/>`_ files.
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

import os
import yaml

def load_yaml(env_var, default_file_name, file_name = None):
  """Load the contents of a YAML file.

  - If `file_name` is provided then the contents of the file are
    loaded and returned.
  - Else, if an environment variable with name `env_var` is defined, 
    then the contents of the file named in that variable are loaded.
  - Else, the contents of the default file, `default_file_name`, are
    loaded and returned.
  
  :param env_var: Environment variable with file name
  :type env_var: str or unicode
  :param default_file_name: Default file name
  :type file_name: str or unicode
  :param file_name: File name (optional)
  :type file_name: str or unicode
  :return: content
  :rtype: dict
  :raises IOError: if the file is not found
  :raises YamlError: if the file does not contain a valid YAML document
  """
  if (file_name is None):
    try:
      file_name = os.environ[env_var]
    except KeyError:
      file_name = default_file_name
  with open(file_name, 'r') as f:
    content = yaml.load(f)
    if type(content) is not dict:
      raise YamlError(file_name)
    return content


class YamlError(Exception):
  """File does not contain a valid YAML document."""

  def __init__(self, filename):
    """Create error.

    :param filename: File name
    :type value: str or unicode
    """
    self._filename = filename

  def __str__(self):
    """Get error as a formatted string.

    :return: formatted string
    :rtype: str or unicode
    """
    return repr(self._filename + " does not contain a valid YAML document")

  @property
  def filename(self):
    """Get file name.

    :return: file name
    :rtype: str or unicode
    """
    return self._filename
