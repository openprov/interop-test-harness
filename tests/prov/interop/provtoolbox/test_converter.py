"""Test classes for prov.interop.provtoolbox.converter classes.
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

from prov.interop.component import ConfigError
from prov.interop.converter import ConversionError
from prov.interop.provtoolbox.converter import ProvToolboxConverter

class ProvToolboxConverterTestCase(unittest.TestCase):

  def setUp(self):
    self.provtoolbox = ProvToolboxConverter()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config[ProvToolboxConverter.EXECUTABLE] = "python"
    self.config[ProvToolboxConverter.ARGUMENTS] = [
      os.path.join(
        os.path.dirname(os.path.abspath(inspect.getfile(
              inspect.currentframe()))), "provconvert-dummy.py"),
      "-infile", "PROV_INPUT", "-outfile", "PROV_OUTPUT"]
    self.config[ProvToolboxConverter.INPUT_FORMATS] = [
      "provn", "ttl", "trig", "provx", "json"]
    self.config[ProvToolboxConverter.OUTPUT_FORMATS] = [
      "provn", "ttl", "trig", "provx", "json"]

  def tearDown(self):
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals("", self.provtoolbox.executable)
    self.assertEquals([], self.provtoolbox.arguments)
    self.assertEquals([], self.provtoolbox.input_formats)
    self.assertEquals([], self.provtoolbox.output_formats)

  def test_configure(self):
    self.provtoolbox.configure(self.config)
    self.assertEquals(self.config[ProvToolboxConverter.EXECUTABLE], 
                      self.provtoolbox.executable)
    self.assertEquals(self.config[ProvToolboxConverter.ARGUMENTS], 
                      self.provtoolbox.arguments)
    self.assertEquals(self.config[ProvToolboxConverter.INPUT_FORMATS], 
                      self.provtoolbox.input_formats)
    self.assertEquals(self.config[ProvToolboxConverter.OUTPUT_FORMATS], 
                      self.provtoolbox.output_formats)

  def test_configure_no_prov_input(self):
    self.config[ProvToolboxConverter.ARGUMENTS].remove("PROV_INPUT")
    with self.assertRaises(ConfigError):
      self.provtoolbox.configure(self.config)

  def test_configure_no_prov_output(self):
    self.config[ProvToolboxConverter.ARGUMENTS].remove("PROV_OUTPUT")
    with self.assertRaises(ConfigError):
      self.provtoolbox.configure(self.config)

  def test_convert(self):
    self.provtoolbox.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".json")
    self.out_file = "convert.xml"
    self.provtoolbox.convert(self.in_file, "json", self.out_file, "xml")

  def test_convert_oserror(self):
    self.config[ProvToolboxConverter.EXECUTABLE] = "/nosuchexecutable"
    self.provtoolbox.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".json")
    self.out_file = "convert_oserror.xml"
    with self.assertRaises(OSError):
      self.provtoolbox.convert(self.in_file, "json", self.out_file, "xml")

  def test_convert_missing_input_file(self):
    self.provtoolbox.configure(self.config)
    self.in_file = "nosuchfile.xml"
    self.out_file = "convert_missing_input_file.xml"
    with self.assertRaises(ConversionError):
      self.provtoolbox.convert(self.in_file, "json", self.out_file, "xml")

  def test_convert_invalid_input_format(self):
    self.provtoolbox.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".nosuchformat")
    self.out_file = "convert_invalid_input_format.xml"
    with self.assertRaises(ConversionError):
      self.provtoolbox.convert(self.in_file, "nosuchformat", 
                               self.out_file, "xml")

  def test_convert_invalid_output_format(self):
    self.provtoolbox.configure(self.config)
    (_, self.in_file) = tempfile.mkstemp(suffix=".json")
    self.out_file = "convert_invalid_input_format.nosuchformat"
    with self.assertRaises(ConversionError):
      self.provtoolbox.convert(self.in_file, "json", 
                               self.out_file, "nosuchformat")
