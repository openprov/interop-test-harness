"""Interoperability test harness resources.
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
import re
import yaml

from prov_interop import factory
from prov_interop import standards
from prov_interop.comparator import Comparator
from prov_interop.component import ConfigError
from prov_interop.component import ConfigurableComponent

class HarnessResources(ConfigurableComponent):
  """Interoperability test harness resources."""

  TEST_CASES_DIR = "test-cases"
  """str or unicode: configuration key for test cases directory"""

  COMPARATORS = "comparators"
  """str or unicode: configuration key list of comparators"""

  CLASS = "class"
  """str or unicode: configuration key for comparator class names"""

  TEST_CASE_PREFIX="testcase"
  """str or unicode: assumed prefix for individual test case
  directories and files
  """

  def __init__(self):
    """Create harness resources.
    """
    super(HarnessResources, self).__init__()
    self._test_cases_dir = ""
    self._comparators = {}
    self._format_comparators = {}
    self._test_cases = []

  @property
  def test_cases_dir(self):
    """Get test cases directory.

    :returns: directory name
    :rtype: list of str or unicode
    """
    return self._test_cases_dir

  @property
  def test_cases(self):
    """Get test cases.

    :returns: list of tuple: zero or more test case tuples of form
      (test case index, ocument 1 format, full path to document 1,
      document 2 format, full path to document 2) where formats are
      assumed to be as in ``prov_interop.standards``
    :rtype: list of tuple of (int, str or unicode, str or unicode, str
      or unicode, str or unicode)
    """
    return self._test_cases

  @property
  def comparators(self):
    """Get dictionary of comparators, keyed by name.

    :returns: comparators
    :rtype: dict from str or unicode to instances of
      :class:`~prov_interop.comparator.Comparator`
    """
    return self._comparators

  @property
  def format_comparators(self):
    """Gets dictionary of comparators keyed by formats.
    Formats are as defined in ``prov_interop.standards``.

    :returns: comparators
    :rtype: dict from str or unicode to instances of 
      :class:`~prov_interop.comparator.Comparator`
    """
    return self._format_comparators

  def register_comparators(self, comparators):
    """Populate dictionaries mapping both comparator names and formats
    to instances of :class:`~prov_interop.comparator.Comparator`. 
    ``comparators`` must include entries:: 

        Comparator nick-name
          class: ... class name...
          ...comparator class-specific configuration...

    For example::

        ProvPyComparator: 
          class: prov_interop.provpy.comparator.ProvPyComparator
          executable: prov-compare
          arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
          formats: [provx, json]

    :param comparators: Mapping of comparator names to 
      class names and comparator-specific configuration
    :type config: dict
    :raises ConfigError: if ``comparators`` is empty,
      comparator-specific configuration is missing ``class``, or there
      is a problem loading, creating or configuring an instance of a 
      sub-class of :class:`~prov_interop.comparator.Comparator`.
    """
    if len(comparators) == 0:
      raise ConfigError("There must be at least one comparator defined")
    for comparator_name in comparators:
      config = comparators[comparator_name]
      if HarnessResources.CLASS not in config:
        raise ConfigError("Missing " + HarnessResources.CLASS + 
                          " for " + comparator_name)
      class_name = config[HarnessResources.CLASS]
      comparator = factory.get_instance(class_name)
      comparator.configure(config)
      self._comparators[comparator_name] = comparator
      for format in comparator.formats:
        self._format_comparators[format] = comparator

  def register_test_cases(self, test_cases_dir, format_filter):
    """Create and register list of test cases.
 
    - Initialise an empty list of test cases.
    - Get test cases directory from.
    - For each child directory, whose name is prefixed by "testcase":

      - Filter its files to get only those which have an extension 
        matching one of the formats in ``prov_interop.standards`` and 
        for which the format is recorded in ``format_filter``.
      - Calculate possible combinations of pairs of the filtered files 
        to get a set of (test-case-number, format1, file1, format2, 
        file2) tuples and add these to``test_cases``.

    :param test_cases_dir: Test cases directory
    :type config: str or unicode
    :param format_filter: List of formats such that only test cases
      within these formats will be considered
    :type format_filter: list of str or unicode
    :raises ConfigError: if the directory is not found
    """
    if not os.path.isdir(test_cases_dir):
      raise ConfigError("Directory not found: " + test_cases_dir)
    pattern = re.compile("^" + HarnessResources.TEST_CASE_PREFIX + "\d+$")
    index_pattern = re.compile("\d+$")
    self._test_cases = []
    for test_case in sorted(os.listdir(test_cases_dir)):
      test_case_dir = os.path.join(test_cases_dir, test_case)
      # Only consider directories of form testcaseNNNN.
      if pattern.match(test_case) is not None \
            and os.path.isdir(test_case_dir):
        index = int(index_pattern.search(test_case).group(0))
        files = []
        for test_file in sorted(os.listdir(test_case_dir)):
          format = os.path.splitext(test_file)[1][1:]
          # Only consider files with the supported extensions and which
          # are in format_filter.
          if format in standards.FORMATS and \
                format in format_filter:
            files.append((format, os.path.join(test_case_dir, test_file)))
        # Create all-pairs combination of the files,
        test_case_tests = [(index, format1, file1, format2, file2) \
                             for (format1, file1) in files \
                             for (format2, file2) in files]
        # Add to current list of all test cases
        self._test_cases.extend(test_case_tests)

  def configure(self, config):
    """Configure harness. ``config`` must hold entries::

        test-cases: ...test cases directory...
        comparators:
          Comparator nick-name
            class: ... class name...
            ...class-specific configuration...
        ...other configuration...

    For example::

        test-cases: /home/user/interop/test-cases
        comparators:
          ProvPyComparator: 
            class: prov_interop.provpy.comparator.ProvPyComparator
            executable: prov-compare
            arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
            formats: [provx, json]

    Other configuration is saved but not processed by this method.
    
    :func:`register_comparators` is called to create and populate
    available comparators.

    :func:`register_test_cases` is called to create applicable test
    cases based on directories in ``test-cases`` and formats 
    supported by available comparators.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above
      entries, or problems arise invoking :func:`configure`
    """
    super(HarnessResources, self).configure(config)
    self.check_configuration(
      [HarnessResources.TEST_CASES_DIR, HarnessResources.COMPARATORS])
    self._test_cases_dir = config[HarnessResources.TEST_CASES_DIR]
    self.register_comparators(config[HarnessResources.COMPARATORS])  
    self.register_test_cases(
      self.configuration[HarnessResources.TEST_CASES_DIR],
      list(self.format_comparators.keys()))      
