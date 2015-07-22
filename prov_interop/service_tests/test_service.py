"""Base class for service tests``.
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

import inspect
import os
import requests
import tempfile
import unittest
from nose.tools import istest
from nose.tools import nottest
from nose_parameterized import parameterized

from prov_interop import standards
from prov_interop.files import load_yaml

@nottest
class ServiceTestCase(unittest.TestCase):

  URL = "url"
  """str or unicode: configuration key for REST endpoint URL"
  """

  def setUp(self):
    super(ServiceTestCase, self).setUp()
    self.test_config = {}
    self.url = ""

  def load_configuration(self, env_var, default_file_name, config_key):
    """
    Get test configuration. Configuration must hold entries::

        url: ...REST endpoint URL...

    :param env_var: Environment variable with configuration file name
    :type env_var: str or unicode
    :param default_file_name: Default configuration file name
    :type file_name: str or unicode
    :param config_key: Key to access test class-specific configuration
    :type config_key: str or unicode
    :raises IOError: if the file is not found
    :raises YamlError: if the configuration file does not parse
    into a dict
    """
    test_config = load_yaml(env_var,
                            default_file_name)
    self.test_config = test_config[config_key]
    self.url = self.test_config[ServiceTestCase.URL]

  def get_document(self, format):
    """Load document with given extension from "documents" directory
    assumed to be in the same directory as the calling test class.
    
    :param format: file format as defined in ``prov.standards```
    :type format: str or unicode
    :returns: document in requested format
    :rtype: str or unicode
    :raises OSError: if there are problems accessing the directory
    or loading the file
    """
    directory = os.path.join(
      os.path.dirname(os.path.abspath(inspect.getfile(
            inspect.currentframe()))), "documents")
    for file_name in os.listdir(directory):
      if os.path.splitext(file_name)[1][1:] == format:
        with open(os.path.join(directory, file_name), "r") as f:
          return f.read()
