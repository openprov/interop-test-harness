"""Test classes for ``prov_interop.converter``.
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

import unittest

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import ConversionError
from prov_interop.converter import Converter

class ConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ConverterTestCase, self).setUp()
    self.converter = Converter()
    self.in_file = None
    self.out_file = None
    self.input_formats = [standards.PROVN, standards.JSON]
    self.output_formats = [standards.PROVX, standards.TTL]
    self.config = {Converter.INPUT_FORMATS: self.input_formats, 
                   Converter.OUTPUT_FORMATS: self.output_formats}

  def tearDown(self):
    super(ConverterTestCase, self).tearDown()

  def test_init(self):
    self.assertEqual([], self.converter.input_formats)
    self.assertEqual([], self.converter.output_formats)

  def test_configure(self):
    self.converter.configure(self.config)
    self.assertEqual(self.input_formats, self.converter.input_formats)
    self.assertEqual(self.output_formats, self.converter.output_formats)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.converter.configure(123)

  def test_configure_no_input_formats(self):
    del self.config[Converter.INPUT_FORMATS]
    with self.assertRaises(ConfigError):
      self.converter.configure(self.config)

  def test_configure_non_canonical_input_format(self):
    self.config[Converter.INPUT_FORMATS].append("invalidFormat")
    with self.assertRaises(ConfigError):
      self.converter.configure(self.config)
    
  def test_configure_no_output_formats(self):
    del self.config[Converter.OUTPUT_FORMATS]
    with self.assertRaises(ConfigError):
      self.converter.configure(self.config)

  def test_configure_non_canonical_output_format(self):
    self.config[Converter.OUTPUT_FORMATS].append("invalidFormat")
    with self.assertRaises(ConfigError):
      self.converter.configure(self.config)

  def test_convert_missing_input_file(self):
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.PROVN
    with self.assertRaises(ConversionError):
      self.converter.convert(self.in_file, self.out_file)

  def test_check_formats_invalid_input_format(self):
    self.converter.configure(self.config)
    with self.assertRaises(ConversionError):
      self.converter.check_formats(standards.PROVX, "nosuchformat")

  def test_check_formats_invalid_output_format(self):
    self.converter.configure(self.config)
    with self.assertRaises(ConversionError):
      self.converter.check_formats("nosuchformat", standards.PROVX)
