"""Test class for ProvTranslator service``.
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
from prov_interop.provtranslator import service
from prov_interop.service_tests.test_service import ServiceTestCase

@istest
class ProvTranslatorTestCase(ServiceTestCase):

  CONFIGURATION_FILE_ENV = "PROVTRANSLATOR_TEST_CONFIGURATION"
  """str or unicode: environment variable holding ProvTranslator
  test configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provtranslator.yaml"
  """str or unicode: default test configuration file name
  """

  CONFIGURATION_KEY="ProvTranslator"
  """str or unicode: key for ProvTranslator configuration in
  configuration file
  """

  def setUp(self):
    super(ProvTranslatorTestCase, self).setUp()
    self.load_configuration(ProvTranslatorTestCase.CONFIGURATION_FILE_ENV,
                            ProvTranslatorTestCase.DEFAULT_CONFIGURATION_FILE,
                            ProvTranslatorTestCase.CONFIGURATION_KEY)
    print(os.path.dirname(os.path.realpath(__file__)))
    print(os.getcwd())
    self.docs = os.path.join(os.getcwd(), "documents")

  def tearDown(self):
    super(ProvTranslatorTestCase, self).tearDown()

  @parameterized.expand(standards.FORMATS)
  def test_translate(self, format):
    self.in_file = os.path.join(self.docs, "primer." + format)
    with open(self.in_file, "r") as f:
      doc_str = f.read()
    (response_code, _) = service.translate(self.url,
                                           format,
                                           format, 
                                           doc_str)
    self.assertEqual(requests.codes.ok, response_code) # 200 OK
