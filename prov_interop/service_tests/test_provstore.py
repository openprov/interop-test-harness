"""Test class for ProvStore service``.
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

import requests
import unittest
from nose.tools import istest
from nose_parameterized import parameterized

from prov_interop import standards
from prov_interop.provstore import service as service
from prov_interop.service_tests.test_service import ServiceTestCase

@istest
class ProvStoreTestCase(ServiceTestCase):

  CONFIGURATION_FILE_ENV = "PROVSTORE_TEST_CONFIGURATION"
  """str or unicode: environment variable holding ProvStore
  test configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provstore.yaml"
  """str or unicode: default test configuration file name
  """

  CONFIGURATION_KEY="ProvStore"
  """str or unicode: key for ProvStore configuration in
  configuration file
  """

  AUTHORIZATION = "authorization"
  """str or unicode: configuration key for ProvStore Authorization 
  HTTP header value
  """

  def setUp(self):
    super(ProvStoreTestCase, self).setUp()
    self.load_configuration(ProvStoreTestCase.CONFIGURATION_FILE_ENV,
                            ProvStoreTestCase.DEFAULT_CONFIGURATION_FILE,
                            ProvStoreTestCase.CONFIGURATION_KEY)
    self.authorization = self.test_config[ProvStoreTestCase.AUTHORIZATION]

  def tearDown(self):
    super(ProvStoreTestCase, self).tearDown()

  @parameterized.expand(standards.FORMATS)
  def test_store(self, format):
    document = self.get_document(format)
    (response_code, response_text) = service.store(self.url,
                                                   self.__class__.__name__,
                                                   format,
                                                   document,
                                                   self.authorization)
    self.assertEqual(requests.codes.created, response_code) # 201 CREATED
    # Get document in desired format
    doc_url = service.get_stored_url(self.url, response_text)
    (response_code, response_text) = service.get(doc_url,
                                                 format)
    self.assertEqual(requests.codes.ok, response_code) # 200 OK
    # Delete document
    (response_code, response_text) = service.delete(doc_url,
                                                    self.authorization)
    self.assertEqual(requests.codes.no_content, response_code) # 204 NO CONTENT
