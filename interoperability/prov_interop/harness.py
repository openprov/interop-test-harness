"""Interoperability test harness configuration.
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
import re

from prov_interop.harness import HarnessResources
from prov_interop import component
from prov_interop import standards
from prov_interop.component import ConfigError

CONFIGURATION_FILE = "PROV_HARNESS_CONFIGURATION_FILE"
"""str or unicode: environment variable holding interoperability test
harness configuration file name
"""

DEFAULT_CONFIGURATION_FILE="harness-configuration.yaml"
"""str or unicode: default interoperability test harness configuration
file name
"""

TEST_CASE_PREFIX="testcase"
"""
str or unicode: assumed prefix for individual test case directories
and files
"""

harness_resources = None
""":class:`~prov_interop.harness.HarnessResources`:
interoperability test harness resources
"""

test_cases = None
"""
:list of tuple: zero or more test case tuples of form (int - test case
index, str or unicode, document 1 format, full path to document 1,
document 2 format, full path to document 2) where formats are assumed
to be as in ``prov_interop.standards``
"""

def initialise_harness_from_file(file_name = None):
  """Initialise interoperability test harness.
  Create :class:`~prov_interop.harness.HarnessResources` 
  and assigns to module variable ``harness``. 
  - If ``file_name`` is provided then the contents of the file are
    loaded and used as configuration.
  - Else, if an environment variable with name
    ``PROV_HARNESS_CONFIGURATION_FILE`` is defined, then the contents
    of the file named in that variable are loaded and used.
  - Else, the contents of the default file,
    ``harness-configuration.yaml``,  are loaded and used.
  If ``harness`` has already been created and initialised, this
  function does nothing.

  :param file_name: Configuration file name (optional)
  :type file_name: str or unicode
  :raises IOError: if the file is not found.
  :raises ConfigError: if the configuration in the file does not
  contain the configuration properties expected by
  :class:`~prov_interop.harness.HarnessResources`, or is an invalud
  YAML file
  """
  global harness_resources
  global CONFIGURATION_FILE
  global DEFAULT_CONFIGURATION_FILE
  if harness_resources is None:
    harness_resources = HarnessResources()
    config = component.load_configuration(CONFIGURATION_FILE,
                                          DEFAULT_CONFIGURATION_FILE, 
                                          file_name)
    harness_resources.configure(config)
    print("Comparators available:")
    for format in harness_resources.format_comparators:
      print(" " + format + ":" + 
            harness_resources.format_comparators[format].__class__.__name__)

def initialise_test_cases():
  global TEST_CASE_PREFIX
  global harness_resources
  global test_cases
  pattern = re.compile("^" + TEST_CASE_PREFIX + "\d+$")
  index_pattern = re.compile("\d+$")
  test_cases_dir = harness_resources.configuration[HarnessResources.TEST_CASES]
  print("Registering test cases in " + test_cases_dir)
  test_cases = []
  for test_case in sorted(os.listdir(test_cases_dir)):
    test_case_dir = os.path.join(test_cases_dir, test_case)
    # Only consider directories of form testcaseNNNN.
    if not pattern.match(test_case) is None and os.path.isdir(test_case_dir):
      index = int(index_pattern.search(test_case).group(0))
      files = []
      for test_file in sorted(os.listdir(test_case_dir)):
        format = os.path.splitext(test_file)[1][1:]
        # Only consider files with the supported extensions and for
        # which a comparator exists.
        if format in standards.FORMATS and \
              format in harness_resources.format_comparators:
          files.append((format, os.path.join(test_case_dir, test_file)))
      # Create all-pairs combination of the files,
      test_case_tests = [(index, format1, file1, format2, file2) \
          for (format1, file1) in files for (format2, file2) in files]
      for (_, format1, _, format2, _) in test_case_tests:
        print(test_case + ":" + format1 + "->" + format2)
      # Add to current list of all test cases
      test_cases.extend(test_case_tests)
  print(str(len(test_cases)) + " test cases registered")

os.environ[CONFIGURATION_FILE] = "localconfig/harness-configuration.yaml"
initialise_harness_from_file()
initialise_test_cases()
