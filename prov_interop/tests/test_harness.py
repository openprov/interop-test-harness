"""Test classes for ``prov_interop.harness``.
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
import shutil
import tempfile
import unittest

from prov_interop import standards
from prov_interop.component import CommandLineComponent
from prov_interop.component import ConfigurableComponent
from prov_interop.component import ConfigError
from prov_interop.converter import Converter
from prov_interop.harness import HarnessResources
from prov_interop.provpy.comparator import ProvPyComparator

class HarnessResourcesTestCase(unittest.TestCase):

  def setUp(self):
    super(HarnessResourcesTestCase, self).setUp()
    self.harness = HarnessResources()
    self.test_cases_dir = tempfile.mkdtemp()
    self.config = {}
    self.config[HarnessResources.TEST_CASES_DIR] = self.test_cases_dir
    self.comparators = {}
    comparator = {}
    comparator[ProvPyComparator.EXECUTABLE] = "python"
    script = "prov-compare"
    comparator[ProvPyComparator.ARGUMENTS] = [
      script,
      "-f", ProvPyComparator.FORMAT1,
      "-F", ProvPyComparator.FORMAT2,
      ProvPyComparator.FILE1,
      ProvPyComparator.FILE2]
    comparator[ProvPyComparator.FORMATS] = [standards.PROVX, standards.JSON]
    comparator[HarnessResources.CLASS] = \
        ProvPyComparator.__module__ + "." + ProvPyComparator.__name__
    self.comparators[ProvPyComparator.__name__] = comparator
    self.config[HarnessResources.COMPARATORS] = self.comparators

  def tearDown(self):
    super(HarnessResourcesTestCase, self).tearDown()
    if self.test_cases_dir != None and os.path.isdir(self.test_cases_dir):
      shutil.rmtree(self.test_cases_dir)

  def test_init(self):
    self.assertEqual({}, self.harness.configuration)
    self.assertEqual("", self.harness.test_cases_dir)
    self.assertEqual({}, self.harness.comparators)
    self.assertEqual({}, self.harness.format_comparators)
    self.assertEqual([], self.harness.test_cases)

  def test_configure(self):
    self.harness.configure(self.config)
    self.assertEqual(self.config, self.harness.configuration)
    self.assertEqual(self.config[HarnessResources.TEST_CASES_DIR],
                     self.harness.test_cases_dir)
    # Check comparators
    comparators = self.harness.comparators
    self.assertEqual(1, len(comparators))
    self.assertTrue(ProvPyComparator.__name__ in comparators)
    comparator = comparators[ProvPyComparator.__name__]
    self.assertIsInstance(comparator, ProvPyComparator)
    # Check comparators indexed by format
    comparators = self.harness.format_comparators
    self.assertEqual(2, len(comparators))
    for format in [standards.PROVX, standards.JSON]:
      self.assertTrue(format in comparators)
      format_comparator = comparators[format]
      self.assertIsInstance(format_comparator, ProvPyComparator)
      self.assertEqual(comparator, format_comparator)

  def test_configure_no_test_cases(self):
    del self.config[HarnessResources.TEST_CASES_DIR]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_configure_no_comparators(self):
    del self.config[HarnessResources.COMPARATORS]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_register_comparators_none(self):
    with self.assertRaises(ConfigError):
      self.harness.register_comparators({})

  def test_register_comparator_class_error(self):
    self.comparators[ProvPyComparator.__name__][
      HarnessResources.CLASS] = "nosuchmodule.Comparator"
    with self.assertRaises(ImportError):
      self.harness.configure(self.config)

  def test_register_comparator_config_error(self):
    del self.comparators[ProvPyComparator.__name__][
      ProvPyComparator.EXECUTABLE]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_register_test_cases_non_existant_directory(self):
    with self.assertRaises(ConfigError):
      self.harness.register_test_cases("nosuchdirectory", [standards.JSON])

  def test_register_test_cases_empty_test_cases_dir(self):
    self.harness.register_test_cases(self.test_cases_dir, [standards.JSON])
    self.assertEqual([], self.harness.test_cases)

  def test_register_test_cases_no_matching_directories(self):
    # Add directory names that do not match testcaseNNNN
    for name in ["one", "testtwo", "testcasethree"]:
      os.mkdir(os.path.join(self.test_cases_dir, name))
    # Add file names do match testcaseNNNN
    for name in ["testcase4", "testcase5"]:
      open(name,'a').close()
    self.harness.register_test_cases(self.test_cases_dir, [standards.JSON])
    self.assertEqual([], self.harness.test_cases)

  def create_cases(self, count, formats):
    for index in list(range(1, count + 1)):
      test_case_dir = os.path.join(self.test_cases_dir, 
                                   HarnessResources.TEST_CASE_PREFIX + 
                                   str(index))
      os.mkdir(test_case_dir)
      for format in formats:
        # Create files both with canonical and non-canonical extensions.
        open(os.path.join(test_case_dir, "file." + format), 'a').close()
        open(os.path.join(test_case_dir, "file.xxx"), 'a').close()
    self.harness.register_test_cases(self.test_cases_dir, formats)

  def check_cases(self, count, formats):
    for index in list(range(1, count + 1)):
      test_case_dir = os.path.join(self.test_cases_dir, 
                                   HarnessResources.TEST_CASE_PREFIX + 
                                   str(index))
      for format1 in formats:
        for format2 in formats:
          self.assertTrue((index, 
                           format1, 
                           os.path.join(test_case_dir, "file." + format1),
                           format2,
                           os.path.join(test_case_dir, "file." + format2)) 
                          in self.harness.test_cases,
                          str(index) + format1 + format2)

  def test_register_test_cases(self):
    self.create_cases(3, standards.FORMATS)
    self.harness.register_test_cases(self.test_cases_dir, standards.FORMATS)
    # 5 formats => 25 tests per test case directory
    # 25 * 3 test case directories => expect 75 test cases
    self.assertEqual((len(standards.FORMATS) ** 2) * 3, 
                     len(self.harness.test_cases))
    self.check_cases(3, standards.FORMATS)

  def test_register_test_cases_single_format(self):
    self.create_cases(3, [standards.JSON])
    self.harness.register_test_cases(self.test_cases_dir, [standards.JSON])
    # 1 format => 1 test per test case directory
    # 1 * 3 test case directories => expect 3 test cases
    self.assertEqual(3, len(self.harness.test_cases))
    self.check_cases(3, [standards.JSON])
