"""Test classes for prov.interop.provpy.comparator classes.
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

from prov.interop.comparator import ComparisonError
from prov.interop.component import ConfigError
from prov.interop.provpy.comparator import ProvPyComparator

class ProvPyComparatorTestCase(unittest.TestCase):

  def setUp(self):
    self.provpy = ProvPyComparator()
    self.in_file = None
    self.out_file = None
    self.config = {}  
    self.config["executable"] = "python"
    self.config["arguments"] = [
      os.path.join(
        os.path.dirname(os.path.abspath(inspect.getfile(
              inspect.currentframe()))), "prov-compare-dummy.py"),
      "-f", "PROV_EXPECTED_FORMAT", "-F", "PROV_ACTUAL_FORMAT",
      "PROV_EXPECTED_FILE", "PROV_ACTUAL_FILE"]
    self.config["formats"] = ["provx", "json"]

  def tearDown(self):
    for tmp in [self.in_file, self.out_file]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals("", self.provpy.executable)
    self.assertEquals([], self.provpy.arguments)
    self.assertEquals([], self.provpy.formats)

  def test_configure(self):
    self.provpy.configure(self.config)
    self.assertEquals(self.config["executable"], self.provpy.executable)
    self.assertEquals(self.config["arguments"], self.provpy.arguments)
    self.assertEquals(self.config["formats"], self.provpy.formats)

  def test_configure_no_prov_expected_format(self):
    self.config["arguments"].remove("PROV_EXPECTED_FORMAT")
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_prov_actual_format(self):
    self.config["arguments"].remove("PROV_ACTUAL_FORMAT")
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_prov_expected_file(self):
    self.config["arguments"].remove("PROV_EXPECTED_FILE")
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_prov_actual_file(self):
    self.config["arguments"].remove("PROV_ACTUAL_FILE")
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_compare(self):
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".json")
    (_, self.actual_file) = tempfile.mkstemp(suffix=".json")
    self.assertTrue(self.provpy.compare(self.expected_file, "json", 
                                        self.actual_file, "json"))

  def test_compare_non_equivalent(self):
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".json")
    (_, self.actual_file) = tempfile.mkstemp(suffix=".xml")
    # ProvPy prov-compare dummy script considers files with
    # non-matching extensions to be different.
    self.assertFalse(self.provpy.compare(self.expected_file, "json", 
                                         self.actual_file, "xml"))

  def test_compare_oserror(self):
    self.config["executable"] = "/nosuchexecutable"
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".json")
    (_, self.actual_file) = tempfile.mkstemp(suffix=".json")
    with self.assertRaises(OSError):
      self.provpy.compare(self.expected_file, "json", self.actual_file, "json")

  def test_compare_missing_expected_file(self):
    self.provpy.configure(self.config)
    self.expected_file = "nosuchfile.json"
    (_, self.actual_file) = tempfile.mkstemp(suffix=".json")
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.expected_file, "json", self.actual_file, "json")

  def test_compare_missing_actual_file(self):
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".json")
    self.actual_file = "nosuchfile.json"
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.expected_file, "json", self.actual_file, "json")

  def test_compare_invalid_expected_format(self):
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".nosuchformat")
    (_, self.actual_file) = tempfile.mkstemp(suffix=".json")
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.expected_file, "nosuchformat", 
                          self.actual_file, "json")

  def test_compare_invalid_actual_format(self):
    self.provpy.configure(self.config)
    (_, self.expected_file) = tempfile.mkstemp(suffix=".json")
    (_, self.actual_file) = tempfile.mkstemp(suffix=".nosuchformat")
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.expected_file, "json", 
                          self.actual_file, "nosuchformat")
