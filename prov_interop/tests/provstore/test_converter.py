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

import inspect
import os
import tempfile
import unittest

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import ConversionError
from prov_interop.provstore.converter import ProvStoreConverter

class ProvStoreConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ProvStoreConverterTestCase, self).setUp()
    self.provstore = ProvStoreConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvStoreConverter.URL] = "http://myurl"
    self.config[ProvStoreConverter.API_KEY] = "user 12345qwerty"
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
    self.assertEquals("", self.provstore.url)
    self.assertEquals("", self.provstore.api_key)
    self.assertEquals([], self.provstore.input_formats)
    self.assertEquals([], self.provstore.output_formats)

  def test_configure(self):
    self.provstore.configure(self.config)
    self.assertEquals(self.config[ProvStoreConverter.URL],
                      self.provstore.url)
    self.assertEquals(self.config[ProvStoreConverter.API_KEY],
                      self.provstore.api_key)
    self.assertEquals(self.config[ProvStoreConverter.INPUT_FORMATS],
                      self.provstore.input_formats)
    self.assertEquals(self.config[ProvStoreConverter.OUTPUT_FORMATS],
                      self.provstore.output_formats)

  def test_configure_no_api_key(self):
    del(self.config[ProvStoreConverter.API_KEY])
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
