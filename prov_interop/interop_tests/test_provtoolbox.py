"""Interoperability tests for ProvToolbox provconvert.
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

from prov_interop.provtoolbox.converter import ProvToolboxConverter
from prov_interop.interop_tests.test_converter import ConverterTestCase

@istest
class ProvToolboxTestCase(ConverterTestCase):

  CONFIGURATION_FILE_ENV = "PROVTOOLBOX_TEST_CONFIGURATION"
  """str or unicode: environment variable holding ProvToolbox
  interoperability test harness configuration file name
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provtoolbox.yaml"
  """str or unicode: default interoperability test harness configuration
  file name
  """

  CONFIGURATION_KEY="ProvToolbox"
  """str or unicode: key for ProvToolbox configuration in configuration
  file"""

  def setUp(self):
    super(ProvToolboxTestCase, self).setUp()
    self.converter = ProvToolboxConverter()
    super(ProvToolboxTestCase, self).configure(
      ProvToolboxTestCase.CONFIGURATION_KEY,
      ProvToolboxTestCase.CONFIGURATION_FILE_ENV,
      ProvToolboxTestCase.DEFAULT_CONFIGURATION_FILE)

  def tearDown(self):
    super(ProvToolboxTestCase, self).tearDown()
