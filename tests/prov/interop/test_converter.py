"""Test classes for prov.interop.converter classes.
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

import os
import tempfile
import unittest

from prov.interop import standards
from prov.interop.component import ConfigError
from prov.interop.converter import ConversionError
from prov.interop.converter import Converter

class ConverterTestCase(unittest.TestCase):

  def setUp(self):
    self.converter = Converter()
    self.in_file = None
    self.out_file = None

  def tearDown(self):
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals([], self.converter.input_formats)
    self.assertEquals([], self.converter.output_formats)

  def test_configure(self):
    input_formats = [standards.PROVN, standards.JSON]
    output_formats = [standards.PROVX, standards.TTL]
    self.converter.configure({Converter.INPUT_FORMATS: input_formats, 
                         Converter.OUTPUT_FORMATS: output_formats})
    self.assertEquals(input_formats, self.converter.input_formats)
    self.assertEquals(output_formats, self.converter.output_formats)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.converter.configure(123)

  def test_configure_no_input_formats(self):
    output_formats = [standards.PROVX, standards.TTL]
    with self.assertRaises(ConfigError):
      self.converter.configure({Converter.OUTPUT_FORMATS: output_formats})

  def test_configure_non_canonical_input_format(self):
    input_formats = [standards.PROVN, standards.JSON, "invalidFormat"]
    output_formats = [standards.PROVX, standards.TTL]
    with self.assertRaises(ConfigError):
      self.converter.configure({Converter.INPUT_FORMATS: input_formats, 
                                Converter.OUTPUT_FORMATS: output_formats})
    
  def test_configure_no_output_formats(self):
    input_formats = [standards.PROVN, standards.JSON]
    with self.assertRaises(ConfigError):
      self.converter.configure({Converter.INPUT_FORMATS: input_formats})

  def test_configure_non_canonical_output_format(self):
    input_formats = [standards.PROVN, standards.JSON]
    output_formats = [standards.PROVX, standards.TTL, "invalidFormat"]
    with self.assertRaises(ConfigError):
      self.converter.configure({Converter.INPUT_FORMATS: input_formats, 
                                Converter.OUTPUT_FORMATS: output_formats})

  def test_convert_missing_input_file(self):
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.PROVN
    with self.assertRaises(ConversionError):
      self.converter.convert(self.in_file, self.out_file)
