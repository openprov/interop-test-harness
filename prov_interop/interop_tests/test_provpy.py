"""Interoperability tests for ProvPy ``prov-convert``.
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

from nose.tools import istest

from prov_interop.provpy.converter import ProvPyConverter
from prov_interop.interop_tests.test_converter import ConverterTestCase

@istest
class ProvPyTestCase(ConverterTestCase):
  """Interoperability tests for ProvPy ``prov-convert``.
 
  Its configuration, loaded via
  :meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.configure`,
  is expected to be in a YAML file: 
  
  - Either provided as the value of a ``ProvPy`` key in the
    :class:`prov_interop.harness.HarnessResource` configuration. 
  - Or, named in an environment variable, 
    ``PROVPY_TEST_CONFIGURATION``.
  - Or in ``localconfig/provpy.yaml``.

  The configuration itself, within this file, is expected to have the
  key `ProvPy``. 

  A valid YAML configuration file is::

    ---
    ProvPy:
      executable: prov-convert
      arguments: -f FORMAT INPUT OUTPUT
      input-formats: [json]
      output-formats: [provn, provx, json]
      skip-tests: []
  """

  CONFIGURATION_FILE_ENV = "PROVPY_TEST_CONFIGURATION"
  """str or unicode: environment variable holding configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provpy.yaml"
  """str or unicode: default configuration file name
  """

  CONFIGURATION_KEY="ProvPy"
  """str or unicode: key for ProvPy configuration in configuration
  file"""

  def setUp(self):
    super(ProvPyTestCase, self).setUp()
    self.converter = ProvPyConverter()
    super(ProvPyTestCase, self).configure(
      ProvPyTestCase.CONFIGURATION_KEY,
      ProvPyTestCase.CONFIGURATION_FILE_ENV,
      ProvPyTestCase.DEFAULT_CONFIGURATION_FILE)

  def tearDown(self):
    super(ProvPyTestCase, self).tearDown()
