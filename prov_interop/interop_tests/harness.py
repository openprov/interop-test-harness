"""Interoperability test harness initialisation.
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

from prov_interop.harness import HarnessResources
from prov_interop import component
from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.files import load_yaml

CONFIGURATION_FILE_ENV = "PROV_HARNESS_CONFIGURATION"
"""str or unicode: environment variable holding interoperability test
harness configuration file name
"""

DEFAULT_CONFIGURATION_FILE="harness.yaml"
"""str or unicode: default interoperability test harness configuration
file name
"""

harness_resources = None
""":class:`prov_interop.harness.HarnessResources`:
interoperability test harness resources
"""

def initialise_harness_from_file(file_name = None):
  """Initialise interoperability test harness.

  This function creates an instance of
  :class:`prov_interop.harness.HarnessResources` and then configures
  it using configuration loaded from a YAML file (using
  :func:`prov_interop.files.load_yaml`). The file loaded is: 

  - `file_name` if this argument is provided (when called from within
    this module itself, no value is provided). 
  - Else, the file named in an environment variable with name
    ``PROV_HARNESS_CONFIGURATION``, if such an environment variable has
    been defined. 
  - Else, ``harness.yaml``, co-located with the Python file.

  The function will not reinitialise the
  :class:`prov_interop.harness.HarnessResources` instance once it has 
  been created and initialised. 

  A valid YAML configuration file, which, when loaded, yields a Python
  dictionary holding the configuration required by
  :class:`prov_interop.harness.HarnessResources` is::

    ---
    test-cases: /home/user/test-cases
    comparators:
      ProvPyComparator: 
        class: prov_interop.provpy.comparator.ProvPyComparator
        executable: prov-compare
        arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
        formats: [provx, json]

  :param file_name: Configuration file name (optional)
  :type file_name: str or unicode
  :raises IOError: if the file is not found.
  :raises ConfigError: if the configuration in the file does not
    contain the configuration properties expected by
    :class:`prov_interop.harness.HarnessResources`
  :raises YamlError: if the file is an invalid YAML file
  """
  global harness_resources
  global CONFIGURATION_FILE_ENV
  global DEFAULT_CONFIGURATION_FILE
  if harness_resources is None:
    default_config_file = os.path.join(
      os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe()))), DEFAULT_CONFIGURATION_FILE)
    harness_resources = HarnessResources()
    config = load_yaml(CONFIGURATION_FILE_ENV,
                       default_config_file,
                       file_name)
    harness_resources.configure(config)
    print("Comparators available:")
    for format in harness_resources.format_comparators:
      print((" " + format + ":" + 
            harness_resources.format_comparators[format].__class__.__name__))
    print("Test cases directory:")
    print((harness_resources.test_cases_dir))
    print("Test cases available:")
    num_test_cases = 0
    for (index, format1, _, format2, _) in harness_resources.test_cases_generator():
      num_test_cases += 1
      print((str(index) + ":" + format1 + "->" + format2))
    print("Total: " + str(num_test_cases))
