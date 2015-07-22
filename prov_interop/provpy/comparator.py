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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path
import subprocess

from prov_interop import standards
from prov_interop.component import CommandLineComponent
from prov_interop.component import ConfigError
from prov_interop.comparator import ComparisonError
from prov_interop.comparator import Comparator

class ProvPyComparator(Comparator, CommandLineComponent):
  """Manages invocation of ProvPy prov-compare script."""

  FORMAT1 = "FORMAT1"
  """str or unicode: token for file1's format in command-line specification"""
  FORMAT2 = "FORMAT2"
  """str or unicode: token for file2's format in command-line specification"""
  FILE1 = "FILE1"
  """str or unicode: token for file1 in command-line specification"""
  FILE2 = "FILE2"
  """str or unicode: token for file1 in command-line specification"""
  LOCAL_FORMATS = {standards.PROVX: "xml"}
  """dict: mapping from formats in ``prov_interop.standards`` to
  formats understood by prov-compare
` """

  def __init__(self):
    """Create comparator.
    """
    super(ProvPyComparator, self).__init__()

  def configure(self, config):
    """Configure comparator. ``config`` must hold entries::

        executable: ...executable name...
        arguments: [...list of arguments including tokens INPUT, OUTPUT...]
        formats: [...list of formats from prov_interop.standards...]

    For example::

        class: prov_interop.provpy.comparator.ProvPyComparator
        executable: python
        arguments: [/home/user/prov/scripts/prov-compare, -f, FORMAT1, -F, FORMAT2, FILE1, FILE2]
        formats: [provx, json]

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(ProvPyComparator, self).configure(config)
    for token in [ProvPyComparator.FORMAT1,
                  ProvPyComparator.FORMAT2, 
                  ProvPyComparator.FILE1, 
                  ProvPyComparator.FILE2]:
      if token not in self._arguments:
        raise ConfigError("Missing token " + token)

  def compare(self, file1, file2):
    """Compare two files. Each file must have an extension matching a
    format in ``prov_interop.standards``.

    ``FORMAT1``, ``FORMAT2``, ``FILE1`` and ``FILE2`` tokens from
    configuration ``arguments`` value are replaced with ``file1`` and
    ``file2`` formats and ``file1`` and ``file2`` values and output
    format, then prepended with ``executable`` value to create
    command-line invocation.

    :param file1: File name
    :type file1: str or unicode
    :param file2: File name
    :type file2: str or unicode
    :returns: True (success) if files are equivalent, else False
    (fail)
    :rtype: bool
    :raises ComparisonError: if either of the files are not found,
    or the files or formats are invalid, or the return code is neither
    0 nor 1
    :raises OSError: if there are problems invoking the comparator
    e.g. the script is not found
    """
    super(ProvPyComparator, self).compare(file1, file2)
    format1 = os.path.splitext(file1)[1][1:]
    format2 = os.path.splitext(file2)[1][1:]
    for format in [format1, format2]:
      super(ProvPyComparator, self).check_format(format)
    local_format1 = format1
    if (format1 in ProvPyComparator.LOCAL_FORMATS):
      local_format1 = ProvPyComparator.LOCAL_FORMATS[format1]
    local_format2 = format2
    if (format2 in ProvPyComparator.LOCAL_FORMATS):
      local_format2 = ProvPyComparator.LOCAL_FORMATS[format2]
    command_line = [local_format1 if x==ProvPyComparator.FORMAT1 else x 
                    for x in self._arguments]
    command_line = [local_format2 if x==ProvPyComparator.FORMAT2 else x 
                    for x in command_line]
    command_line = [file1 if x==ProvPyComparator.FILE1 else x 
                    for x in command_line]
    command_line = [file2 if x==ProvPyComparator.FILE2 else x 
                    for x in command_line]
    command_line.insert(0, self.executable)
    print((" ".join(command_line)))
    return_code = subprocess.call(command_line)
    if return_code == 0:
      return True
    elif return_code == 1:
      return False
    else:
      raise ComparisonError(self._executable + " returned " + str(return_code))
