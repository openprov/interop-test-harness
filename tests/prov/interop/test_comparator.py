"""Test classes for prov.interop.comparator classes.
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
from prov.interop.comparator import Comparator
from prov.interop.comparator import ComparisonError

class ComparatorTestCase(unittest.TestCase):

  def setUp(self):
    self.comparator = Comparator()
    self.file1 = None
    self.file2 = None

  def tearDown(self):
    for tmp in [self.file1, self.file2]:
      if tmp != None and os.path.isfile(tmp):
        os.remove(tmp)

  def test_init(self):
    self.assertEquals([], self.comparator.formats)

  def test_configure(self):
    formats = [standards.PROVN, standards.JSON]
    self.comparator.configure({Comparator.FORMATS: formats})
    self.assertEquals(formats, self.comparator.formats)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.comparator.configure(123)

  def test_configure_no_formats(self):
    with self.assertRaises(ConfigError):
      self.comparator.configure({})

  def test_configure_non_canonical_format(self):
    formats = [standards.PROVN, standards.JSON, "invalidFormat"]
    with self.assertRaises(ConfigError):
      self.comparator.configure({Comparator.FORMATS: formats})

  def test_compare_missing_file1(self):
    self.file1 = "nosuchfile." + standards.JSON
    (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
    with self.assertRaises(ComparisonError):
      self.comparator.compare(self.file1, self.file2)

  def test_compare_missing_file2(self):
    (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
    self.file2 = "nosuchfile." + standards.JSON
    with self.assertRaises(ComparisonError):
      self.comparator.compare(self.file1, self.file2)
