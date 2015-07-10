"""Interoperability tests for ProvPy prov-convert.
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

from nose.tools import istest

from prov_interop.provpy.converter import ProvPyConverter
from prov_interop.interop_tests.converter import ConverterTestCase

@istest
class ProvPyTestCase(ConverterTestCase):

  CONFIGURATION_FILE_ENV = "PROVPY_TEST_CONFIGURATION"
  """str or unicode: environment variable holding ProvPy
  interoperability test harness configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provpy.yaml"
  """str or unicode: default interoperability test harness configuration
  file name
  """

  def setUp(self):
    # TODO initialise converter only once?
    super(ProvPyTestCase, self).setUp()
    self.converter = ProvPyConverter()
    super(ProvPyTestCase, self).configure(
      ProvPyTestCase.CONFIGURATION_FILE_ENV,
      ProvPyTestCase.DEFAULT_CONFIGURATION_FILE)

  def tearDown(self):
    super(ProvPyTestCase, self).tearDown()
