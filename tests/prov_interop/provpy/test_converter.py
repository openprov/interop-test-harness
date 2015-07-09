"""Test classes for ``prov_interop.provpy.converter``.
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
from prov_interop.provpy.converter import ProvPyConverter

class ProvPyConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ProvPyConverterTestCase, self).setUp()
    self.provpy = ProvPyConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvPyConverter.EXECUTABLE] = "python"
    script = os.path.join(
      os.path.dirname(os.path.abspath(inspect.getfile(
            inspect.currentframe()))), "prov-convert-dummy.py")
    self.config[ProvPyConverter.ARGUMENTS] = [
      script,
      "-f", ProvPyConverter.FORMAT, 
      ProvPyConverter.INPUT, ProvPyConverter.OUTPUT]
    self.config[ProvPyConverter.INPUT_FORMATS] = [
      standards.JSON]
    self.config[ProvPyConverter.OUTPUT_FORMATS] = [
      standards.PROVN, standards.PROVX, standards.JSON]

  def tearDown(self):
    super(ProvPyConverterTestCase, self).tearDown()
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals("", self.provpy.executable)
    self.assertEquals([], self.provpy.arguments)
    self.assertEquals([], self.provpy.input_formats)
    self.assertEquals([], self.provpy.output_formats)

  def test_configure(self):
    self.provpy.configure(self.config)
    self.assertEquals(self.config[ProvPyConverter.EXECUTABLE], 
                      self.provpy.executable)
    self.assertEquals(self.config[ProvPyConverter.ARGUMENTS], 
                      self.provpy.arguments)
    self.assertEquals(self.config[ProvPyConverter.INPUT_FORMATS], 
                      self.provpy.input_formats)
    self.assertEquals(self.config[ProvPyConverter.OUTPUT_FORMATS], 
                      self.provpy.output_formats)

  def test_configure_no_format(self):
    self.config[ProvPyConverter.ARGUMENTS].remove(ProvPyConverter.FORMAT)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_input(self):
    self.config[ProvPyConverter.ARGUMENTS].remove(ProvPyConverter.INPUT)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_output(self):
    self.config[ProvPyConverter.ARGUMENTS].remove(ProvPyConverter.OUTPUT)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_convert(self):
    self.provpy.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert." + standards.PROVN
    self.provpy.convert(self.in_file, self.out_file)

  def test_convert_non_canonical_output(self):
    self.provpy.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert." + standards.PROVX
    self.provpy.convert(self.in_file, self.out_file)

  def test_convert_oserror(self):
    self.config[ProvPyConverter.EXECUTABLE] = "/nosuchexecutable"
    self.provpy.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_oserror." + standards.PROVN
    with self.assertRaises(OSError):
      self.provpy.convert(self.in_file, self.out_file)

  def test_convert_missing_input_file(self):
    self.provpy.configure(self.config)
    self.in_file = "nosuchfile.json"
    self.out_file = "convert_missing_input_file." + standards.JSON
    with self.assertRaises(ConversionError):
      self.provpy.convert(self.in_file, self.out_file)

  def test_convert_invalid_output_format(self):
    self.provpy.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.out_file = "convert_invalid_output_format.nosuchformat"
    with self.assertRaises(ConversionError):
      self.provpy.convert(self.in_file, self.out_file)
