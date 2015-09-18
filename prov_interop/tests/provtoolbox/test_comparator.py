"""Unit tests for :mod:`prov_interop.provtoolbox.comparator`.

These tests rely on the
:mod:`prov_interop.tests.provtoolbox.provconvert_dummy.py` script

(that mimics ProvToolbox's ``provconvert`` executable
in terms of parameters and return codes when used to compare
PROV documents) being available in the same directory as this module.

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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import os
import tempfile
import unittest

from prov_interop import standards
from prov_interop.comparator import ComparisonError
from prov_interop.component import ConfigError
from prov_interop.provtoolbox.comparator import ProvToolboxComparator

class ProvToolboxComparatorTestCase(unittest.TestCase):

    def setUp(self):
        super(ProvToolboxComparatorTestCase, self).setUp()
        self.comparator = ProvToolboxComparator()
        self.file1 = None
        self.file2 = None
        self.config = {
            ProvToolboxComparator.EXECUTABLE: "python",
            ProvToolboxComparator.ARGUMENTS: " ".join(
                 [os.path.join(
                   os.path.dirname(os.path.abspath(inspect.getfile(
                     inspect.currentframe()))), "provconvert_dummy.py"),
                 "-infile", ProvToolboxComparator.FILE1,
                 "-compare", ProvToolboxComparator.FILE2]
            ),
            ProvToolboxComparator.FORMATS: [
                standards.PROVN, standards.TRIG, standards.PROVX, standards.JSON
            ]
        }

    def tearDown(self):
        super(ProvToolboxComparatorTestCase, self).tearDown()
        for tmp in [self.file1, self.file2]:
            if tmp != None and os.path.isfile(tmp):
                os.remove(tmp)

    def test_init(self):
        self.assertEqual("", self.comparator.executable)
        self.assertEqual([], self.comparator.arguments)
        self.assertEqual([], self.comparator.formats)

    def test_configure(self):
        self.comparator.configure(self.config)
        self.assertEqual(self.config[ProvToolboxComparator.EXECUTABLE].split(),
                         self.comparator.executable)
        self.assertEqual(self.config[ProvToolboxComparator.ARGUMENTS].split(),
                         self.comparator.arguments)
        self.assertEqual(self.config[ProvToolboxComparator.FORMATS],
                         self.comparator.formats)

    def test_configure_no_file1(self):
        self.config[ProvToolboxComparator.ARGUMENTS] = " ".join(
            ["-compare", ProvToolboxComparator.FILE2]
        )
        with self.assertRaises(ConfigError):
            self.comparator.configure(self.config)

    def test_configure_no_file2(self):
        self.config[ProvToolboxComparator.ARGUMENTS] = " ".join(
            ["-compare", ProvToolboxComparator.FILE2]
        )

        with self.assertRaises(ConfigError):
            self.comparator.configure(self.config)

    def test_compare(self):
        self.comparator.configure(self.config)
        _, self.file1 = tempfile.mkstemp(suffix="." + standards.JSON)
        _, self.file2 = tempfile.mkstemp(suffix="." + standards.JSON)
        with open(self.file1, 'a') as f1:
            f1.write("{}")
        with open(self.file2, 'a') as f2:
            f2.write("{}")
        self.assertTrue(self.comparator.compare(self.file1, self.file2))

    def test_compare_non_equivalent(self):
        self.comparator.configure(self.config)
        (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
        (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
        with open(self.file1, 'a') as f1:
            f1.write("FILE")
        with open(self.file2, 'a') as f2:
            f2.write("{}")
        self.assertFalse(self.comparator.compare(self.file1, self.file2))

    def test_compare_oserror(self):
        self.config[ProvToolboxComparator.EXECUTABLE] = "/nosuchexecutable"
        self.comparator.configure(self.config)
        (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
        (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
        with self.assertRaises(OSError):
            self.comparator.compare(self.file1, self.file2)

    def test_compare_missing_file1(self):
        self.comparator.configure(self.config)
        self.file1 = "nosuchfile." + standards.JSON
        (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
        with self.assertRaises(ComparisonError):
            self.comparator.compare(self.file1, self.file2)

    def test_compare_missing_file2(self):
        self.comparator.configure(self.config)
        (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
        self.file2 = "nosuchfile." + standards.JSON
        with self.assertRaises(ComparisonError):
            self.comparator.compare(self.file1, self.file2)

    def test_compare_invalid_format1(self):
        self.comparator.configure(self.config)
        (_, self.file1) = tempfile.mkstemp(suffix=".nosuchformat")
        (_, self.file2) = tempfile.mkstemp(suffix="." + standards.JSON)
        with self.assertRaises(ComparisonError):
            self.comparator.compare(self.file1, self.file2)

    def test_compare_invalid_format2(self):
        self.comparator.configure(self.config)
        (_, self.file1) = tempfile.mkstemp(suffix="." + standards.JSON)
        (_, self.file2) = tempfile.mkstemp(suffix=".nosuchformat")
        with self.assertRaises(ComparisonError):
            self.comparator.compare(self.file1, self.file2)
