"""Test class for ProvValidator service``.
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
import requests
import tempfile
import unittest
from nose.tools import istest
from nose_parameterized import parameterized

from prov_interop import standards
from prov_interop.provvalidator import service as service
from prov_interop.service_tests.test_service import ServiceTestCase

@istest
class ProvValidatorTestCase(ServiceTestCase):

  CONFIGURATION_FILE_ENV = "PROVVALIDATOR_TEST_CONFIGURATION"
  """str or unicode: environment variable holding ProvValidator
  test configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provvalidator.yaml"
  """str or unicode: default test configuration file name
  """

  CONFIGURATION_KEY="ProvValidator"
  """str or unicode: key for ProvValidator configuration in
  configuration file
  """

  def setUp(self):
    super(ProvValidatorTestCase, self).setUp()
    self.load_configuration(ProvValidatorTestCase.CONFIGURATION_FILE_ENV,
                            ProvValidatorTestCase.DEFAULT_CONFIGURATION_FILE,
                            ProvValidatorTestCase.CONFIGURATION_KEY)
    self.docs = os.path.join(os.getcwd(), "documents")

  def tearDown(self):
    super(ProvValidatorTestCase, self).tearDown()

  @parameterized.expand(standards.FORMATS)
  def test_validate(self, format):
    self.in_file = os.path.join(self.docs, "primer." + format)
    with open(self.in_file, "r") as f:
      document = f.read()
    (response_code, response_text) = service.validate(self.url,
                                                      format,
                                                      document)
    self.assertEqual(requests.codes.ok, response_code) # 200 OK
