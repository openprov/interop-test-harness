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

import unittest

from prov_interop import standards
from prov_interop.component import CommandLineComponent
from prov_interop.component import ConfigurableComponent
from prov_interop.component import ConfigError
from prov_interop.converter import Converter
from prov_interop.harness import HarnessResources
from prov_interop.provpy.comparator import ProvPyComparator

def get_sample_configuration():
  """Return sample 
  :class:`~prov_interop.harness.HarnessResources`-compliant dict.

  :returns: configuration
  :rtype: dict
  """
  config = {}
  config[HarnessResources.TEST_CASES] = "/home/user/test-cases"
  comparators = {}
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
  comparators[ProvPyComparator.__name__] = comparator
  config[HarnessResources.COMPARATORS] = comparators
  return config

class HarnessResourcesTestCase(unittest.TestCase):

  def setUp(self):
    super(HarnessResourcesTestCase, self).setUp()
    self.harness = HarnessResources()
    self.config = get_sample_configuration()
    
  def test_init(self):
    self.assertEqual({}, self.harness.configuration)
    self.assertEqual("", self.harness.test_cases)
    self.assertEqual({}, self.harness.comparators)
    self.assertEqual({}, self.harness.format_comparators)

  def test_configure(self):
    self.harness.configure(self.config)
    self.assertEqual(self.config, self.harness.configuration)
    self.assertEqual(self.config[HarnessResources.TEST_CASES],
                     self.harness.test_cases)
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
    del self.config[HarnessResources.TEST_CASES]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_configure_no_comparators(self):
    del self.config[HarnessResources.COMPARATORS]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_configure_zero_comparators(self):
    self.config[HarnessResources.COMPARATORS] = {}
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)

  def test_configure_comparator_class_error(self):
    self.config[HarnessResources.COMPARATORS][
      ProvPyComparator.__name__][HarnessResources.CLASS] = "nosuchmodule.Comparator"
    with self.assertRaises(ImportError):
      self.harness.configure(self.config)

  def test_configure_comparator_config_error(self):
    del self.config[HarnessResources.COMPARATORS][
      ProvPyComparator.__name__][ProvPyComparator.EXECUTABLE]
    with self.assertRaises(ConfigError):
      self.harness.configure(self.config)
