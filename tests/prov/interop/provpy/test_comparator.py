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

from prov.interop import standards
from prov.interop.comparator import ComparisonError
from prov.interop.component import ConfigError
from prov.interop.provpy.comparator import ProvPyComparator

class ProvPyComparatorTestCase(unittest.TestCase):

  def setUp(self):
    self.provpy = ProvPyComparator()
    self.file1 = None
    self.file2 = None
    self.config = {}  
    self.config[ProvPyComparator.EXECUTABLE] = "python"
    script = os.path.join(
      os.path.dirname(os.path.abspath(inspect.getfile(
            inspect.currentframe()))), "prov-compare-dummy.py")
    self.config[ProvPyComparator.ARGUMENTS] = [
      script,
      "-f", ProvPyComparator.FORMAT1, "-F", ProvPyComparator.FORMAT2,
      ProvPyComparator.FILE1, ProvPyComparator.FILE2]
    self.config[ProvPyComparator.FORMATS] = [
      standards.PROVX, standards.JSON]

  def tearDown(self):
    for tmp in [self.file1, self.file2]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals("", self.provpy.executable)
    self.assertEquals([], self.provpy.arguments)
    self.assertEquals([], self.provpy.formats)

  def test_configure(self):
    self.provpy.configure(self.config)
    self.assertEquals(self.config[ProvPyComparator.EXECUTABLE],
                      self.provpy.executable) 
    self.assertEquals(self.config[ProvPyComparator.ARGUMENTS],
                      self.provpy.arguments) 
    self.assertEquals(self.config[ProvPyComparator.FORMATS],
                      self.provpy.formats) 

  def test_configure_no_format1(self):
    self.config[ProvPyComparator.ARGUMENTS].remove(ProvPyComparator.FORMAT1)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_format2(self):
    self.config[ProvPyComparator.ARGUMENTS].remove(ProvPyComparator.FORMAT2)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_file1(self):
    self.config[ProvPyComparator.ARGUMENTS].remove(ProvPyComparator.FILE1)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_configure_no_file2(self):
    self.config[ProvPyComparator.ARGUMENTS].remove(ProvPyComparator.FILE2)
    with self.assertRaises(ConfigError):
      self.provpy.configure(self.config)

  def test_compare(self):
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.file2 = self.file1
    # ProvPy prov-compare dummy script considers files with
    # matching names to be the same.
    self.assertTrue(self.provpy.compare(self.file1, standards.JSON, 
                                        self.file2, standards.JSON))

  def test_compare_non_equivalent(self):
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
    # ProvPy prov-compare dummy script considers files with
    # non-matching names to be different.
    self.assertFalse(self.provpy.compare(self.file1, standards.JSON, 
                                         self.file2, standards.JSON))

  def test_compare_oserror(self):
    self.config[ProvPyComparator.EXECUTABLE] = "/nosuchexecutable"
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
    with self.assertRaises(OSError):
      self.provpy.compare(self.file1, standards.JSON, 
                          self.file2, standards.JSON)

  def test_compare_missing_file1(self):
    self.provpy.configure(self.config)
    self.file1 = "nosuchfile.json"
    (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.file1, standards.JSON, 
                          self.file2, standards.JSON)

  def test_compare_missing_file2(self):
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.file2 = "nosuchfile.json"
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.file1, standards.JSON, 
                          self.file2, standards.JSON)

  def test_compare_invalid_format1(self):
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix=".nosuchformat")
    (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.file1, "nosuchformat", 
                          self.file2, standards.JSON)

  def test_compare_invalid_format2(self):
    self.provpy.configure(self.config)
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    (_, self.file2) = tempfile.mkstemp(suffix=".nosuchformat")
    with self.assertRaises(ComparisonError):
      self.provpy.compare(self.file1, standards.JSON, 
                          self.file2, "nosuchformat")
