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

import unittest

from prov.interop.component import ConfigError
from prov.interop.converter import Converter

class ConverterTestCase(unittest.TestCase):

  def test_init(self):
    converter = Converter()
    self.assertEquals([], converter.input_formats)
    self.assertEquals([], converter.output_formats)

  def test_configure(self):
    converter = Converter()
    converter.configure({Converter.INPUT_FORMATS: ["a", "b"], 
                         Converter.OUTPUT_FORMATS: ["c", "d"]})
    self.assertEquals(["a", "b"], converter.input_formats)
    self.assertEquals(["c", "d"], converter.output_formats)

  def test_configure_non_dict_error(self):
    converter = Converter()
    with self.assertRaises(ConfigError):
      converter.configure(123)

  def test_configure_no_input_formats(self):
    converter = Converter()
    with self.assertRaises(ConfigError):
      converter.configure({Converter.OUTPUT_FORMATS: ["c", "d"]})

  def test_configure_no_output_formats(self):
    converter = Converter()
    with self.assertRaises(ConfigError):
      converter.configure({Converter.INPUT_FORMATS: ["a", "b"]})
