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

  FORMAT1 = "FORMAT1"
  FORMAT2 = "FORMAT2"
  FILE1 = "FILE1"
  FILE2 = "FILE2"

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
    tokens ``FORMAT1``, ``FORMAT2``, ``FILE1``, ``FILE2``.
    """
    super(ProvPyComparator, self).configure(config)
    ProvPyComparator.check_configuration(
      self._arguments,
      [ProvPyComparator.FORMAT1, ProvPyComparator.FORMAT2,
       ProvPyComparator.FILE1, ProvPyComparator.FILE2])

  def compare(self, file1, file2):
    """Invoke comparison of files in canonical formats.
    Each file must have an extension matching one of the canonical
    file formats.
    Canonical formats are defined in ``standards``.

    :param file1: File name
    :type file1: str or unicode
    :param file2: File name
    :type file2: str or unicode
    :returns: True (success) if files are equivalent, else False (fail)
    :rtype: bool
    :raises ComparisonError: if either of the files are not found,
    or the files or formats are invalid.
    :raises OSError: if there are problems invoking the comparator
    e.g. the script is not found at the specified location.
    """
    if not os.path.isfile(file1):
      raise ComparisonError("File not found: " + file1)
    if not os.path.isfile(file2):
      raise ComparisonError("File not found: " + file2)
    format1 = os.path.splitext(file1)[1][1:]
    format2 = os.path.splitext(file2)[1][1:]
    # TODO check formats in input/output formats
    # TODO map to local format
    # Replace tokens in arguments
    command_line = [format1 if x==ProvPyComparator.FORMAT1 else x 
                    for x in self._arguments]
    command_line = [format2 if x==ProvPyComparator.FORMAT2 else x 
                    for x in command_line]
    command_line = [file1 if x==ProvPyComparator.FILE1 else x 
                    for x in command_line]
    command_line = [file2 if x==ProvPyComparator.FILE2 else x 
                    for x in command_line]
    command_line.insert(0, self.executable)
    # Execute
    return_code = subprocess.call(command_line)
    if return_code == 0:
      return True
    elif return_code == 1:
      return False
    else:
      raise ComparisonError(self._executable + " returned " + str(return_code))
