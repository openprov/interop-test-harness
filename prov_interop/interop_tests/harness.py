"""Interoperability test harness boot-strapping.
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

from prov_interop.harness import HarnessResources
from prov_interop import component
from prov_interop import standards
from prov_interop.component import ConfigError

CONFIGURATION_FILE_ENV = "PROV_HARNESS_CONFIGURATION"
"""str or unicode: environment variable holding interoperability test
harness configuration file name
"""

DEFAULT_CONFIGURATION_FILE="localconfig/harness.yaml"
"""str or unicode: default interoperability test harness configuration
file name
"""

harness_resources = None
""":class:`~prov_interop.harness.HarnessResources`:
interoperability test harness resources
"""

def initialise_harness_from_file(file_name = None):
  """Initialise interoperability test harness.
  Create :class:`~prov_interop.harness.HarnessResources` 
  and assigns to module variable ``harness``. 
  - If ``file_name`` is provided then the contents of the file are
    loaded and used as configuration.
  - Else, if an environment variable with name
    ``PROV_HARNESS_CONFIGURATION`` is defined, then the contents
    of the file named in that variable are loaded and used.
  - Else, the contents of the default file, ``harness.yaml``, 
    are loaded and used.
  If ``harness`` has already been created and initialised, this
  function does nothing.

  :param file_name: Configuration file name (optional)
  :type file_name: str or unicode
  :raises IOError: if the file is not found.
  :raises ConfigError: if the configuration in the file does not
  contain the configuration properties expected by
  :class:`~prov_interop.harness.HarnessResources`, or is an invalid
  YAML file
  """
  global harness_resources
  global CONFIGURATION_FILE_ENV
  global DEFAULT_CONFIGURATION_FILE
  if harness_resources is None:
    harness_resources = HarnessResources()
    config = component.load_configuration(CONFIGURATION_FILE_ENV,
                                          DEFAULT_CONFIGURATION_FILE, 
                                          file_name)
    harness_resources.configure(config)
    print("Comparators available:")
    for format in harness_resources.format_comparators:
      print((" " + format + ":" + 
            harness_resources.format_comparators[format].__class__.__name__))
    print((harness_resources.test_cases_dir))
    print((str(len(harness_resources.test_cases)) + " test cases registered:"))
    for (index, format1, _, format2, _) in harness_resources.test_cases:
      print((str(index) + ":" + format1 + "->" + format2))

initialise_harness_from_file()
