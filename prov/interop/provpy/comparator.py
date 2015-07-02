"""Manages invocation of ProvPy prov-compare script.
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

import os.path
import subprocess

from prov.interop.component import CommandLineComponent
from prov.interop.component import ConfigError
from prov.interop.comparator import ComparisonError
from prov.interop.comparator import Comparator

class ProvPyComparator(Comparator, CommandLineComponent):
  """Manages invocation of ProvPy prov-compare script."""

  def __init__(self):
    """Create comparator.
    Invokes super-classes ``__init__``.
    """
    super(ProvPyComparator, self).__init__()

  def configure(self, config):
    """Configure comparator.
    Invokes super-classes ``__configure__``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config ``arguments`` does not contain the
    tokens ``PROV_EXPECTED_FORMAT``, ``PROV_ACTUAL_FORMAT``, 
    ``PROV_EXPECTED_FILE``, ``PROV_ACTUAL_FILE``
    """
    super(ProvPyComparator, self).configure(config)
    if not "PROV_EXPECTED_FORMAT" in self._arguments:
      raise ConfigError("Missing PROV_EXPECTED_FORMAT token in 'arguments'")
    if not "PROV_ACTUAL_FORMAT" in self._arguments:
      raise ConfigError("Missing PROV_FORMAT token in 'arguments'")
    if not "PROV_EXPECTED_FILE" in self._arguments:
      raise ConfigError("Missing PROV_EXPECTED_FILE token in 'arguments'")
    if not "PROV_ACTUAL_FILE" in self._arguments:
      raise ConfigError("Missing PROV_ACTUAL_FILE token in 'arguments'")

  def compare(self, expected_file, expected_format, actual_file, actual_format
):
    """Invoke comparison of expected file in given format to actual
    file in given format.

    :param expected_file: Expected file name
    :type expected_file: str or unicode
    :param expected_format: Expected format
    :type expected_format: str or unicode
    :param actual_file: Actual file name
    :type actual_file: str or unicode
    :param actual_format: Actual format
    :type actual_format: str or unicode
    :returns: True (success) if files are equivalent, else False
    (fail) if files are not equivalent.
    :rtype: bool
    :raises ComparisonError: if either of the files are not found,
    or the input files or formats are invalid.
    :raises OSError: if there are problems invoking the comparator
    e.g. the script is not found at the specified location.
    """
    if not os.path.isfile(expect4ed_file):
      raise ComparisonError("Expected file not found: " + expected_file)
    if not os.path.isfile(actual_file):
      raise ComparisonError("Actual file not found: " + actual_file)
    # Replace tokens in arguments
    command_line = [expected_format if x=="PROV_EXPECTED_FORMAT" 
                    else x for x in self._arguments]
    command_line = [actual_format if x=="PROV_ACTUAL_FORMAT" 
                    else x for x in self._arguments]
    command_line = [expected_file if x=="PROV_EXPECTED_FILE" 
                    else x for x in self._arguments]
    command_line = [actual_file if x=="PROV_ACTUAL_FILE" 
                    else x for x in self._arguments]
    command_line.insert(0, self.executable)
    # Execute
    return_code = subprocess.call(command_line)
    if return_code == 0:
      return True
    else if return_code == 1:
      return False
    else:
      raise ComparisonError(self._executable + " returned " + str(return_code))
