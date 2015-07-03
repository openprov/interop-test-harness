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

import unittest

from prov.interop.component import ConfigError
from prov.interop.comparator import Comparator

class ComparatorTestCase(unittest.TestCase):

  def test_init(self):
    comparator = Comparator()
    self.assertEquals([], comparator.formats)

  def test_configure(self):
    comparator = Comparator()
    comparator.configure({Comparator.FORMATS: ["a", "b"]})
    self.assertEquals(["a", "b"], comparator.formats)

  def test_configure_non_dict_error(self):
    comparator = Comparator()
    with self.assertRaises(ConfigError):
      comparator.configure(123)

  def test_configure_no_formats(self):
    comparator = Comparator()
    with self.assertRaises(ConfigError):
      comparator.configure({})
