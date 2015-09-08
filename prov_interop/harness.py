"""Managing test harness configuration.
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
  """Manages test harness configuration including the test cases."""

  TEST_CASES_DIR = "test-cases"
  """str or unicode: configuration key for test cases directory"""

  COMPARATORS = "comparators"
  """str or unicode: configuration key for comparators"""

  CLASS = "class"
  """str or unicode: configuration key for comparator class names"""

  TEST_CASE_PREFIX="test-"
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

  @property
  def test_cases_dir(self):
    """Get test cases directory.

    :return: directory name
    :rtype: list of str or unicode
    """
    return self._test_cases_dir

  @property
  def comparators(self):
    """Get dictionary of comparators, keyed by name, where names
    are those provided in the comparator configuration.

    :return: comparators
    :rtype: dict from str or unicode to 
      :class:`prov_interop.comparator.Comparator`
    """
    return self._comparators

  @property
  def format_comparators(self):
    """Gets dictionary of comparators keyed by formats.
    Formats are in :mod:`prov_interop.standards`.

    :return: comparators
    :rtype: dict from str or unicode to 
      :class:`prov_interop.comparator.Comparator`
    """
    return self._format_comparators

  def register_comparators(self, comparators):
    """Populate a dictionary of comparators, keyed by comparator name,
    and a dictionary of comparators, keyed by format. `comparators`
    must hold a list of comparator configurations keyed by name. Each
    configuration consists of:

    - ``class``: name of class that manages invocations of that comparator.
    - Configuration values required by the value of ``class``.

    A valid value for `comparators` is::

      {
        "ProvPyComparator": 
        {
          "class": "prov_interop.provpy.comparator.ProvPyComparator",
          "executable": "prov-compare",
          "arguments": "-f FORMAT1 -F FORMAT2 FILE1 FILE2",
          "formats": ["provx", "json"],
        }
      }

    This method populates `comparators`, a dictionary of
    :class:`prov_interop.comparator.Comparator` objects, keyed by
    comparator name. The `class` determines the comparator object to
    create and the associated configuration is used to configure it
    - this uses dynamic object creation (see
    :mod:`prov_interop.factory`). Using the above configuration
    there would be a mapping from ``ProvPyComparator`` to an instance
    of :class:`prov_interop.provpy.comparator.ProvPyComparator`. 
    
    It also populates `format_comparators`, a dictionary of
    :class:`prov_interop.comparator.Comparator` objects, keyed by
    formats in :mod:`prov_interop.standards`. Using the above
    configuration there would be mappings from both ``provx`` and
    ``json`` to an instance of
    :class:`prov_interop.provpy.comparator.ProvPyComparator`.  

    :param comparators: Mapping of comparator names to 
      class names and comparator-specific configuration
    :type config: dict
    """
    if (comparators == None) or (len(comparators) == 0):
      return
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

  def test_cases_generator(self):
    """Return a generator for test cases.

    This serves as a generator for test cases. Using a generator
    avoids the need to cache all the possible test cases in a list in
    memory. Each test case is a tuple of form::

      (test case index, format1, file1, format2, file2)

    where ``file1`` and ``file2`` have extension ``format1`` and
    ``format2`` respectively and both ``format1`` and ``format2`` are
    in :mod:`prov_interop.standards`. For example::

      (case1, "json", "/home/user/test-cases/test-case1/testcase1.json",
          "provx", "/home/user/test-cases/test-case1/testcase1.provx")
      (case1, "trig", "/home/user/test-cases/test-case1/testcase1.trig",
          "provx", "/home/user/test-cases/test-case1/testcase1.provx")

    The method traverses `test_cases_dir`, looking for
    sub-directories whose name matches the pattern
    ``test-([-\w]+)``. For each directory, it filters its files to
    get only those which have an extension in both
    :mod:`prov_interop.standards` and the formats for which a
    comparator has been registered). From the files left it calculates
    all possible combinations of pairs of files and creates tuples as
    above. So, if `test_cases_dir` contains::

      test-case1/
        README.md
        testcase1.json
        testcase1.provn
        testcase1.provx
        testcase1.trig
        testcase1.ttl
      test-case3/
        README.md
        primer.json
        primer.provn
        primer.trig
        primer.ttl
      example/
        example.json

    and comparators have been registered for ``["json", "provx"]``
    this would give the test case tuples::

      (case1, json, /home/user/test-cases/testcase1.json
              json, /home/user/test-cases/testcase1.json),
      (case1, json, /home/user/test-cases/testcase1.json
              provx, /home/user/test-cases/testcase1.provx),
      (case1, provx, /home/user/test-cases/testcase1.provx
              json, /home/user/test-cases/testcase1.json),
      (case1, provx, /home/user/test-cases/testcase1.provx
          provx, /home/user/test-cases/testcase1.provx),
      (case3, json, /home/user/test-cases/primer.json
          json, /home/user/test-cases/primer.json)

    :returns: test case tuple
    :rtype: tuple of (int, str or unicode, str or unicode, str or
      unicode, str or unicode) 
    :raises ConfigError: if the test cases directory is not found
    """
    if not os.path.isdir(self._test_cases_dir):
      raise ConfigError("Directory not found: " + self._test_cases_dir)
    pattern = re.compile("^" + HarnessResources.TEST_CASE_PREFIX + "([-\w]+)$")
    for test_case in sorted(os.listdir(self._test_cases_dir)):
      test_case_dir = os.path.join(self._test_cases_dir, test_case)
      # Only consider directories
      if not os.path.isdir(test_case_dir):
        continue
      match = pattern.match(test_case)
      if match:
        testcase_id = match.group(1)
        files = []
        for test_file in sorted(os.listdir(test_case_dir)):
          format = os.path.splitext(test_file)[1][1:]
          # Only consider files with the supported extensions and which
          # are in format_filter.
          if format in standards.FORMATS and \
                format in list(self.format_comparators.keys()):
            files.append((format, os.path.join(test_case_dir, test_file)))
        # Create all-pairs combination of the files.
        for (format1, file1) in files:
          for (format2, file2) in files:
            yield (testcase_id, format1, file1, format2, file2)

  def configure(self, config):
    """Configure harness. The configuration must hold:

    - ``test-cases``: location of test cases directory.
    - ``comparators``: a list of comparator configurations keyed by
       name. Each configuration consists of: 

      - ``class``: name of class that manages invocations of that comparator.
      - Configuration values required by the class named in ``class``.

    A valid configuration is::

      {
        "test-cases": "/home/user/test-cases",
        "comparators": 
        {
          "ProvPyComparator": 
          {
            "class": "prov_interop.provpy.comparator.ProvPyComparator",
            "executable": "prov-compare",
            "arguments": "-f FORMAT1 -F FORMAT2 FILE1 FILE2",
            "formats": ["provx", "json"],
          }
        }
      }

    This method invokes :func:`register_comparators` to
    create the comparators.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if `config` does not hold the above
      entries, or if there are any problems creating or configuring
      comparators.
    """
    super(HarnessResources, self).configure(config)
    self.check_configuration(
      [HarnessResources.TEST_CASES_DIR, HarnessResources.COMPARATORS])
    self._test_cases_dir = config[HarnessResources.TEST_CASES_DIR]
    self.register_comparators(config[HarnessResources.COMPARATORS])  
