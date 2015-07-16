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
import tempfile
import unittest

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import ConversionError
from prov_interop.provtranslator.converter import ProvTranslatorConverter

class ProvTranslatorConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ProvTranslatorConverterTestCase, self).setUp()
    self.provtranslator = ProvTranslatorConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvTranslatorConverter.URL] = "http://myurl"
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

  def test_convert_bad_url(self):
    self.config[ProvTranslatorConverter.URL] = "http://nosuchurl"
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_bad_url." + standards.PROVN
    with self.assertRaises(ConnectionError):
      self.provtranslator.convert(self.in_file, self.out_file)

  def test_convert_missing_input_file(self):
    self.provtranslator.configure(self.config)
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.JSON
    with self.assertRaises(ConversionError):
      self.provtranslator.convert(self.in_file, self.out_file)

  def test_convert_invalid_output_format(self):
    self.provtranslator.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_invalid_output_format.nosuchformat"
    with self.assertRaises(ConversionError):
      self.provtranslator.convert(self.in_file, self.out_file)
