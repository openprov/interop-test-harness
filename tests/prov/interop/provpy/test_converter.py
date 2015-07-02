"""Test classes for prov.interop.provpy.converter classes.
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
from prov.interop.converter import ConversionError
from prov.interop.provpy.converter import ProvPyConverter

class ProvPyConverterTestCase(unittest.TestCase):

  def setUp(self):
    self.config = {}  
    self.config["directory"] = "/home/user/prov/scripts"
    self.config["executable"] = "prov-convert"
    self.config["arguments"] = ["-f", "PROV_FORMAT", "PROV_INPUT", "PROV_OUTPUT"]
    self.config["input_formats"] = ["provn", "provx", "json"]
    self.config["output_formats"] = ["provn", "provx", "json"]

  def test_init(self):
    provpy = ProvPyConverter()
    self.assertEquals("", provpy.directory)
    self.assertEquals("", provpy.executable)
    self.assertEquals([], provpy.arguments)
    self.assertEquals([], provpy.input_formats)
    self.assertEquals([], provpy.output_formats)

  def test_configure(self):
    provpy = ProvPyConverter()
    provpy.configure(self.config)
    self.assertEquals(self.config["directory"], provpy.directory)
    self.assertEquals(self.config["executable"], provpy.executable)
    self.assertEquals(self.config["arguments"], provpy.arguments)
    self.assertEquals(self.config["input_formats"], provpy.input_formats)
    self.assertEquals(self.config["output_formats"], provpy.output_formats)

  def test_configure_no_prov_format(self):
    provpy = ProvPyConverter()
    self.config["arguments"].remove("PROV_FORMAT")
    with self.assertRaises(ConfigError):
      provpy.configure(self.config)

  def test_configure_no_prov_format(self):
    provpy = ProvPyConverter()
    self.config["arguments"].remove("PROV_INPUT")
    with self.assertRaises(ConfigError):
      provpy.configure(self.config)

  def test_configure_no_prov_format(self):
    provpy = ProvPyConverter()
    self.config["arguments"].remove("PROV_OUTPUT")
    with self.assertRaises(ConfigError):
      provpy.configure(self.config)

  def test_convert(self):
    provpy = ProvPyConverter()
    provpy.configure(self.config)
    provpy.convert("a", "b", "c", "d")
    self.assertEquals(self.config["directory"], provpy.directory)
    self.assertEquals(self.config["executable"], provpy.executable)
    self.assertEquals(self.config["arguments"], provpy.arguments)
    self.assertEquals(self.config["input_formats"], provpy.input_formats)
    self.assertEquals(self.config["output_formats"], provpy.output_formats)
