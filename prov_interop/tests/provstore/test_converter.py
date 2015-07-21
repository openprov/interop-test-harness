"""Test classes for ``prov_interop.provstore.converter``.
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
import requests_mock
import tempfile
import unittest
from nose.tools import nottest
from nose_parameterized import parameterized

from prov_interop import http
from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import ConversionError
from prov_interop.provstore.converter import ProvStoreConverter

@nottest
def test_case_name(testcase_func, param_num, param):
  """``nose_parameterized`` callback function to create custom
  test function names.

  :param testcase__func: test function
  :type testcase__func: function
  :param param_num: number of parameters in ``param``
  :type param_num: int
  :param param: tuple of arguments to test function of form (FORMAT, _)
  :type param: tuple, assumed to be of form (str or unicode, _)
  :returns: test function name of form ``testcase_func_FORMAT``
  :rtype: str or unicode
  """
  (format, _) = param.args
  return "%s_%s" %(
    testcase_func.__name__,
    parameterized.to_safe_name(str(format)))


class ProvStoreConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ProvStoreConverterTestCase, self).setUp()
    self.provstore = ProvStoreConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvStoreConverter.URL] = \
        "https://" + self.__class__.__name__ + "/converter"
    self.config[ProvStoreConverter.AUTHORIZATION] = "ApiKey user:12345qwerty"
    self.config[ProvStoreConverter.INPUT_FORMATS] = list(
      standards.FORMATS)
    self.config[ProvStoreConverter.OUTPUT_FORMATS] = list(
      standards.FORMATS)

  def tearDown(self):
    super(ProvStoreConverterTestCase, self).tearDown()
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEqual("", self.provstore.url)
    self.assertEqual("", self.provstore.authorization)
    self.assertEqual([], self.provstore.input_formats)
    self.assertEqual([], self.provstore.output_formats)

  def test_configure(self):
    self.provstore.configure(self.config)
    self.assertEqual(self.config[ProvStoreConverter.URL],
                     self.provstore.url)
    self.assertEqual(self.config[ProvStoreConverter.AUTHORIZATION],
                     self.provstore.authorization)
    self.assertEqual(self.config[ProvStoreConverter.INPUT_FORMATS],
                     self.provstore.input_formats)
    self.assertEqual(self.config[ProvStoreConverter.OUTPUT_FORMATS],
                     self.provstore.output_formats)

  def test_configure_no_authorization(self):
    del(self.config[ProvStoreConverter.AUTHORIZATION])
    with self.assertRaises(ConfigError):
      self.provstore.configure(self.config)

  def test_convert_missing_input_file(self):
    self.provstore.configure(self.config)
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.JSON
    with self.assertRaises(ConversionError):
      self.provstore.convert(self.in_file, self.out_file)

  def test_convert_invalid_input_format(self):
    self.provstore.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".nosuchformat")
    self.out_file = "convert_invalid_input_format." + standards.PROVX
    with self.assertRaises(ConversionError):
      self.provstore.convert(self.in_file, self.out_file)

  def test_convert_invalid_output_format(self):
    self.provstore.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_invalid_output_format.nosuchformat"
    with self.assertRaises(ConversionError):
      self.provstore.convert(self.in_file, self.out_file)

  def create_files(self, format):
    (_, self.in_file) = tempfile.mkstemp(suffix="." + format)
    (_, self.out_file) = tempfile.mkstemp(suffix="." + format)

  def register_post(self, mocker, content_type, doc_id, 
                    status_code = requests.codes.created):
    headers={http.CONTENT_TYPE: content_type,
             http.ACCEPT: ProvStoreConverter.CONTENT_TYPES[standards.JSON],
             http.AUTHORIZATION: self.config[ProvStoreConverter.AUTHORIZATION]}
    mocker.register_uri("POST", 
                        self.config[ProvStoreConverter.URL],
                        json={"id": doc_id},
                        request_headers=headers,
                        status_code=status_code)

  def register_get(self, mocker, content_type, doc_id, doc, format,
                   status_code = requests.codes.ok):
    doc_url = self.config[ProvStoreConverter.URL] + str(doc_id)
    headers={http.ACCEPT: content_type}
    mocker.register_uri("GET", 
                        doc_url + "." + format,
                        request_headers=headers,
                        text=doc,
                        status_code=status_code)

  def register_delete(self, mocker, doc_id, 
                      status_code=requests.codes.no_content):
    doc_url = self.config[ProvStoreConverter.URL] + str(doc_id)
    headers={http.AUTHORIZATION: self.config[ProvStoreConverter.AUTHORIZATION]}
    mocker.register_uri("DELETE", 
                        doc_url,
                        request_headers=headers,
                        status_code=status_code)

  @parameterized.expand([
      (standards.PROVN, ProvStoreConverter.CONTENT_TYPES[standards.PROVN]),
      (standards.TTL, ProvStoreConverter.CONTENT_TYPES[standards.TTL]),
      (standards.TRIG, ProvStoreConverter.CONTENT_TYPES[standards.TRIG]),
      (standards.PROVX, ProvStoreConverter.CONTENT_TYPES[standards.PROVX]),
      (standards.JSON, ProvStoreConverter.CONTENT_TYPES[standards.JSON])
      ], testcase_func_name=test_case_name)
  def test_convert(self, format, content_type):
    self.provstore.configure(self.config)
    self.create_files(format)
    doc = "mockDocument"
    doc_id = 123
    # Set up mock service response.
    with requests_mock.Mocker(real_http=False) as mocker:
      self.register_post(mocker, content_type, doc_id)
      self.register_get(mocker, content_type, doc_id, doc, format)
      self.register_delete(mocker, doc_id)
      self.provstore.convert(self.in_file, self.out_file)
      with open(self.out_file, 'r') as f:
        self.assertEqual(doc, f.read(), "Unexpected output file content")

  def test_convert_post_server_error(self):
    self.provstore.configure(self.config)
    format = standards.JSON
    self.create_files(format)
    content_type = ProvStoreConverter.CONTENT_TYPES[format]
    # Set up mock service response with POST causing server error.
    with requests_mock.Mocker(real_http=False) as mocker:
      self.register_post(mocker, 
                         content_type,
                         123,
                         status_code=requests.codes.internal_server_error)
      with self.assertRaises(ConversionError):
        self.provstore.convert(self.in_file, self.out_file)

  def test_convert_get_server_error(self):
    self.provstore.configure(self.config)
    format = standards.JSON
    self.create_files(format)
    content_type = ProvStoreConverter.CONTENT_TYPES[format]
    doc = "mockDocument"
    doc_id = 123
    # Set up mock service response with GET causing server error.
    with requests_mock.Mocker(real_http=False) as mocker:
      self.register_post(mocker, content_type, doc_id)
      self.register_get(mocker, content_type, doc_id, doc, format,
                        status_code=requests.codes.internal_server_error)
      with self.assertRaises(ConversionError):
        self.provstore.convert(self.in_file, self.out_file)

  def test_convert_delete_server_error(self):
    self.provstore.configure(self.config)
    format = standards.JSON
    self.create_files(format)
    content_type = ProvStoreConverter.CONTENT_TYPES[format]
    doc = "mockDocument"
    doc_id = 123
    # Set up mock service response with DELETE causing server error.
    with requests_mock.Mocker(real_http=False) as mocker:
      self.register_post(mocker, content_type, doc_id)
      self.register_get(mocker, content_type, doc_id, doc, format)
      self.register_delete(mocker, doc_id,
                           status_code=requests.codes.internal_server_error)
      with self.assertRaises(ConversionError):
        self.provstore.convert(self.in_file, self.out_file)
