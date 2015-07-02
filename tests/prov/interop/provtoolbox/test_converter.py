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

import unittest

from prov.interop.component import ConfigError
from prov.interop.converter import ConversionError
from prov.interop.provtoolbox.converter import ProvToolboxConverter

class ProvToolboxConverterTestCase(unittest.TestCase):

  def setUp(self):
    self.config = {}  
    self.config["executable"] = "/home/user/provToolbox/bin/provconvert"
    self.config["arguments"] = ["-infile", "PROV_INPUT", "-outfile", "PROV_OUTPUT"]
    self.config["input_formats"] = ["provn", "ttl", "trig", "provx", "json"]
    self.config["output_formats"] = ["provn", "ttl", "trig", "provx", "json"]

  def test_init(self):
    provtoolbox = ProvToolboxConverter()
    self.assertEquals("", provtoolbox.executable)
    self.assertEquals([], provtoolbox.arguments)
    self.assertEquals([], provtoolbox.input_formats)
    self.assertEquals([], provtoolbox.output_formats)

  def test_configure(self):
    provtoolbox = ProvToolboxConverter()
    provtoolbox.configure(self.config)
    self.assertEquals(self.config["executable"], provtoolbox.executable)
    self.assertEquals(self.config["arguments"], provtoolbox.arguments)
    self.assertEquals(self.config["input_formats"], provtoolbox.input_formats)
    self.assertEquals(self.config["output_formats"], provtoolbox.output_formats)

  def test_configure_no_prov_format(self):
    provtoolbox = ProvToolboxConverter()
    self.config["arguments"].remove("PROV_INPUT")
    with self.assertRaises(ConfigError):
      provtoolbox.configure(self.config)

  def test_configure_no_prov_format(self):
    provtoolbox = ProvToolboxConverter()
    self.config["arguments"].remove("PROV_OUTPUT")
    with self.assertRaises(ConfigError):
      provtoolbox.configure(self.config)

  def test_convert(self):
    provtoolbox = ProvToolboxConverter()
    provtoolbox.configure(self.config)
    provtoolbox.convert("a", "b", "c", "d")
    self.assertEquals(self.config["executable"], provtoolbox.executable)
    self.assertEquals(self.config["arguments"], provtoolbox.arguments)
    self.assertEquals(self.config["input_formats"], provtoolbox.input_formats)
    self.assertEquals(self.config["output_formats"], provtoolbox.output_formats)
