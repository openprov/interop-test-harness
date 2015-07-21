"""Test classes for ``prov_interop.provtranslator.converter``.
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
from prov_interop.provtranslator.converter import ProvTranslatorConverter

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


class ProvTranslatorConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ProvTranslatorConverterTestCase, self).setUp()
    self.provtranslator = ProvTranslatorConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvTranslatorConverter.URL] = \
        "https://" + self.__class__.__name__ + "/converter"
    self.config[ProvTranslatorConverter.INPUT_FORMATS] = list(
      standards.FORMATS)
    self.config[ProvTranslatorConverter.OUTPUT_FORMATS] = list(
      standards.FORMATS)

  def tearDown(self):
    super(ProvTranslatorConverterTestCase, self).tearDown()
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals("", self.provtranslator.url)
    self.assertEquals([], self.provtranslator.input_formats)
    self.assertEquals([], self.provtranslator.output_formats)

  def test_configure(self):
    self.provtranslator.configure(self.config)
    self.assertEquals(self.config[ProvTranslatorConverter.URL], 
                      self.provtranslator.url)
    self.assertEquals(self.config[ProvTranslatorConverter.INPUT_FORMATS], 
                      self.provtranslator.input_formats)
    self.assertEquals(self.config[ProvTranslatorConverter.OUTPUT_FORMATS], 
                      self.provtranslator.output_formats)

  def test_convert_missing_input_file(self):
    self.provtranslator.configure(self.config)
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.JSON
    with self.assertRaises(ConversionError):
      self.provtranslator.convert(self.in_file, self.out_file)

  def test_convert_invalid_input_format(self):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".nosuchformat")
    self.out_file = "convert_invalid_input_format." + standards.PROVX
    with self.assertRaises(ConversionError):
      self.provtranslator.convert(self.in_file, self.out_file)

  def test_convert_invalid_output_format(self):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_invalid_output_format.nosuchformat"
    with self.assertRaises(ConversionError):
      self.provtranslator.convert(self.in_file, self.out_file)

  def test_convert(self):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    (_, self.out_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    doc = "mockDocument"
    # Set up mock service response.
    headers={http.CONTENT_TYPE: 
             ProvTranslatorConverter.CONTENT_TYPES[standards.JSON],
             http.ACCEPT: 
             ProvTranslatorConverter.CONTENT_TYPES[standards.JSON]}
    with requests_mock.Mocker(real_http=False) as mocker:
      mocker.register_uri("POST", 
                          self.config[ProvTranslatorConverter.URL],
                          text=doc)
      self.provtranslator.convert(self.in_file, self.out_file)
      with open(self.out_file, 'r') as f:
        self.assertEqual(doc, f.read(), "Unexpected output file content")

  @parameterized.expand([
      (standards.PROVN, ProvTranslatorConverter.CONTENT_TYPES[standards.PROVN]),
      (standards.TTL, ProvTranslatorConverter.CONTENT_TYPES[standards.TTL]),
      (standards.TRIG, ProvTranslatorConverter.CONTENT_TYPES[standards.TRIG]),
      (standards.PROVX, ProvTranslatorConverter.CONTENT_TYPES[standards.PROVX]),
      (standards.JSON, ProvTranslatorConverter.CONTENT_TYPES[standards.JSON])
      ], testcase_func_name=test_case_name)
  def test_convert(self, format, content_type):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + format)
    (_, self.out_file) = tempfile.mkstemp(suffix="." + format)
    doc = "mockDocument"
    # Set up mock service response.
    headers={http.CONTENT_TYPE: content_type,
             http.ACCEPT: content_type}
    with requests_mock.Mocker(real_http=False) as mocker:
      mocker.register_uri("POST", 
                          self.config[ProvTranslatorConverter.URL],
                          request_headers=headers,
                          text=doc)
      self.provtranslator.convert(self.in_file, self.out_file)
      with open(self.out_file, 'r') as f:
        self.assertEqual(doc, f.read(), "Unexpected output file content")

  def test_convert_server_error(self):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    (_, self.out_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    # Set up mock service response with server error.
    with requests_mock.Mocker(real_http=False) as mocker:
      mocker.register_uri("POST", 
                          self.config[ProvTranslatorConverter.URL],
                          status_code=requests.codes.internal_server_error)
      with self.assertRaises(ConversionError):
        self.provtranslator.convert(self.in_file, self.out_file)
