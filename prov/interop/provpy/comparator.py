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
import re
import shutil
import subprocess

from prov.interop import standards
from prov.interop.component import CommandLineComponent
from prov.interop.component import ConfigError
from prov.interop.comparator import ComparisonError
from prov.interop.comparator import Comparator

class ProvPyComparator(Comparator, CommandLineComponent):
  """Manages invocation of ProvPy prov-compare script."""

  FORMAT1 = "FORMAT1"
  """string or unicode: token for file1's format in command-line specification"""
  FORMAT2 = "FORMAT2"
  """string or unicode: token for file2's format in command-line specification"""
  FILE1 = "FILE1"
  """string or unicode: token for file1 in command-line specification"""
  FILE2 = "FILE2"
  """string or unicode: token for file1 in command-line specification"""
  LOCAL_FORMATS = {standards.PROVX: "xml"}
  """list of string or unicode: list of mapping from formats in
  ``prov.interop.standards`` to formats understood by prov-compare
` """

  def __init__(self):
    """Create comparator.
    """
    super(ProvPyComparator, self).__init__()

  def configure(self, config):
    """Configure comparator.
    ``config`` is expected to hold configuration of form::

        executable: ...executable name...
        arguments: [...list of arguments including tokens FORMAT1, FORMAT2, FILE1, FILE2...]
        formats: [...list of formats...]

    For example::

        class: prov.interop.provpy.comparator.ProvPyComparator
        executable: python
        arguments: [/home/user/prov/scripts/prov-compare, -f, FORMAT1, -F, FORMAT2, FILE1, FILE2]
        formats: [provx, json]

    Formats must be as defined in ``prov.interop.standards``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(ProvPyComparator, self).configure(config)
    ProvPyComparator.check_configuration(
      self._arguments,
      [ProvPyComparator.FORMAT1, ProvPyComparator.FORMAT2,
       ProvPyComparator.FILE1, ProvPyComparator.FILE2])

  def compare(self, file1, file2):
    """Use prov-compare to compare two files. Each file must have an
    extension matching one of those in ``prov.interop.standards``.
    ``executable`` and ``arguments`` in the configuration are used to
    create a command to execute at the shell. ``FORMAT1``,
    ``FORMAT2``, ``FILE1`` and ``FILE2`` tokens are populated using
    ``file1``, ``file2`` values, with mappings to local formats
    supported by prov-compare being done if needed.

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
      if not format in self.formats:
        raise ComparisonError("Unsupported format: " + format)
    # Map prov.interop.standards formats to formats supported by prov-compare
    local_file1 = file1
    local_format1 = format1
    if (format1 in ProvPyComparator.LOCAL_FORMATS):
      local_format1 = ProvPyComparator.LOCAL_FORMATS[format1]
      local_file1 = re.sub(format1 + "$", local_format1, file1)
      shutil.copy(file1, local_file1)
    local_file2 = file2
    local_format2 = format2
    if (format2 in ProvPyComparator.LOCAL_FORMATS):
      local_format2 = ProvPyComparator.LOCAL_FORMATS[format2]
      local_file2 = re.sub(format2 + "$", local_format2, file2)
      shutil.copy(file2, local_file2)
    # Replace tokens in arguments
    command_line = [local_format1 if x==ProvPyComparator.FORMAT1 else x 
                    for x in self._arguments]
    command_line = [local_format2 if x==ProvPyComparator.FORMAT2 else x 
                    for x in command_line]
    command_line = [local_file1 if x==ProvPyComparator.FILE1 else x 
                    for x in command_line]
    command_line = [local_file2 if x==ProvPyComparator.FILE2 else x 
                    for x in command_line]
    command_line.insert(0, self.executable)
    # Execute
    try:
      print(" ".join(command_line))
      return_code = subprocess.call(command_line)
      print return_code
      if return_code == 0:
        return True
      elif return_code == 1:
        return False
      else:
        raise ComparisonError(self._executable + " returned " + str(return_code))
    finally:
      if (local_file1 != file1) and os.path.isfile(local_file1):
        os.remove(local_file1)
      if (local_file2 != file2) and os.path.isfile(local_file2):
        os.remove(local_file2)
