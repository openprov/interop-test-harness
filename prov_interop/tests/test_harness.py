"""Unit tests for :mod:`prov_interop.harness`.
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

import os
import shutil
import tempfile
import unittest

from prov_interop import standards
from prov_interop.comparator import Comparator
from prov_interop.component import ConfigurableComponent
from prov_interop.component import ConfigError
from prov_interop.harness import HarnessResources

class DummyComparator(Comparator):
  """Dummy comparator.
  """

  def __init__(self):
    """Create comparator.
    """
    super(DummyComparator, self).__init__()

  def configure(self, config):
    """Configure comparator. The configuration must hold:

    - ``formats``: formats supported by the comparator, each of which
      must be one of those in :mod:`prov_interop.standards`.

    A valid configuration is::

      {
        "formats": ["provx", "json"]
      }

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if `config` does not hold the above entries
    """
    super(DummyComparator, self).configure(config)

  def compare(self, file1, file2):
    """This does nothing but return ``True`` always.

    :param file1: File
    :type file1: str or unicode
    :param file2: File
    :type file2: str or unicode
    :return: ``True`` always
    """
    return True


class HarnessResourcesTestCase(unittest.TestCase):

  def setUp(self):
    super(HarnessResourcesTestCase, self).setUp()
    self.harness = HarnessResources()
    self.test_cases_dir = tempfile.mkdtemp()
    self.config = {}
    self.config[HarnessResources.TEST_CASES_DIR] = self.test_cases_dir
    self.comparators = {}
    comparator = {}
    comparator[Comparator.FORMATS] = [standards.PROVX, standards.JSON]
    comparator[HarnessResources.CLASS] = \
        DummyComparator.__module__ + "." + DummyComparator.__name__
    self.comparators[DummyComparator.__name__] = comparator
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

  def test_configure(self):
    self.harness.configure(self.config)
    self.assertEqual(self.config, self.harness.configuration)
    self.assertEqual(self.config[HarnessResources.TEST_CASES_DIR],
                     self.harness.test_cases_dir)
    # Check comparators
    comparators = self.harness.comparators
    self.assertEqual(1, len(comparators))
    self.assertTrue(DummyComparator.__name__ in comparators)
    comparator = comparators[DummyComparator.__name__]
    self.assertIsInstance(comparator, DummyComparator)
    # Check comparators indexed by format
    comparators = self.harness.format_comparators
    self.assertEqual(2, len(comparators))
    for format in [standards.PROVX, standards.JSON]:
      self.assertTrue(format in comparators)
      format_comparator = comparators[format]
      self.assertIsInstance(format_comparator, DummyComparator)
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
    self.harness.register_comparators({})
    self.assertEqual({}, self.harness.comparators)
    self.assertEqual({}, self.harness.format_comparators)
    
  def test_register_comparator_class_error(self):
    self.comparators[DummyComparator.__name__][
      HarnessResources.CLASS] = "nosuchmodule.Comparator"
    with self.assertRaises(ImportError):
      self.harness.configure(self.config)

  def test_register_comparator_config_error(self):
    del self.comparators[DummyComparator.__name__][Comparator.FORMATS]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_register_test_cases_non_existant_directory(self):
    with self.assertRaises(ConfigError):
      for test_case in self.harness.test_cases_generator():
        pass

  def test_register_test_cases_empty_test_cases_dir(self):
    self.harness.configure(self.config)
    num_test_cases = 0
    for test_case in self.harness.test_cases_generator():
      num_test_cases += 1
    self.assertEqual(0, num_test_cases)

  def test_register_test_cases_no_matching_directories(self):
    # Add directory names that do not match testcaseNNNN
    for name in ["one", "testtwo", "testcasethree"]:
      os.mkdir(os.path.join(self.test_cases_dir, name))
    # Add file names do match testcaseNNNN
    for name in ["test-case4", "test-case5"]:
      open(os.path.join(self.test_cases_dir, name), "a").close()
    self.harness.configure(self.config)
    num_test_cases = 0
    for test_case in self.harness.test_cases_generator():
      num_test_cases += 1
    self.assertEqual(0, num_test_cases)

  def create_cases(self, count, formats):
    """Create test case directories and files.

    Create `count` directories, named ``testcaseNNNN``. In each,
    create files ``file.FORMAT`` where ``FORMAT`` is in `formats`,
    and a file ``file.xxx``.

    :param count: Number of directories to create
    :type formats: int
    :param formats: Formats, each of which must be in 
      :mod:`prov_interop.standards`
    :type formats: list of str or unicode
    """
    for index in list(range(1, count + 1)):
      test_case_dir = os.path.join(self.test_cases_dir, 
                                   HarnessResources.TEST_CASE_PREFIX + 
                                   str(index))
      os.mkdir(test_case_dir)
      for format in formats:
        # Create files both with canonical and non-canonical extensions.
        open(os.path.join(test_case_dir, "file." + format), "a").close()
      open(os.path.join(test_case_dir, "file.xxx"), "a").close()

  def check_cases(self, count, formats, test_cases):
    """Check test cases returned by
    :meth:`prov_interop.harness.HarnessResources.test_cases_generator`.
   
    This method complements :meth:`create_cases`.

    :param count: Number of test case directories expected
    :type formats: int
    :param formats: Formats, each of which must be in 
      :mod:`prov_interop.standards`, of files in test case directories 
    :type formats: list of str or unicode
    :param test_cases: list of test case tuples of form 
      `(test case index, format1, file1, format2, file2)`
    :type test_cases: list of tuple of (int, str or unicode, str or
      unicode, str or unicode, str or unicode)
    """
    for index in list(range(1, count + 1)):
      test_case_dir = os.path.join(self.test_cases_dir, 
                                   HarnessResources.TEST_CASE_PREFIX + 
                                   str(index))
      for format1 in formats:
        for format2 in formats:
          expected_test_case = (
            str(index),
            format1, os.path.join(test_case_dir, "file." + format1),
            format2, os.path.join(test_case_dir, "file." + format2)
          )
          self.assertIn(expected_test_case, test_cases,
                        'Test case %s, %s, %s is not found' % (index, format1, format2))

  def test_test_cases_generator(self):
    self.config[HarnessResources.COMPARATORS][DummyComparator.__name__] \
        [Comparator.FORMATS] = standards.FORMATS
    self.harness.configure(self.config)
    self.create_cases(3, standards.FORMATS)
    test_cases = []
    for test_case in self.harness.test_cases_generator():
      test_cases.append(test_case)
    # 5 formats => 25 tests per test case directory
    # 25 * 3 test case directories => expect 75 test cases
    self.assertEqual((len(standards.FORMATS) ** 2) * 3, len(test_cases))
    self.check_cases(3, standards.FORMATS, test_cases)

  def register_test_cases_single_format(self):
    self.harness.configure(self.config)
    self.create_cases(3, [standards.JSON])
    test_cases = []
    for test_case in self.harness.test_cases_generator():
      test_cases.append(test_case)
    # 1 format => 1 test per test case directory
    # 1 * 3 test case directories => expect 3 test cases
    self.assertEqual(3, len(test_cases))
    self.check_cases(3, [standards.JSON], test_cases)
