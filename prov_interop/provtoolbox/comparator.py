"""Manages invocation of ProvToolbox `provconvert` script for comparison
of two PROV documents.
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

from prov_interop.component import CommandLineComponent
from prov_interop.component import ConfigError
from prov_interop.comparator import ComparisonError
from prov_interop.comparator import Comparator


class ProvToolboxComparator(Comparator, CommandLineComponent):
    """Manages invocation of ProvToolbox `provconvert` script for comparison of two PROV documents."""

    FORMAT1 = "FORMAT1"
    """str or unicode: token for file1's format in command-line specification"""

    FORMAT2 = "FORMAT2"
    """str or unicode: token for file2's format in command-line specification"""

    FILE1 = "FILE1"
    """str or unicode: token for file1 in command-line specification"""

    FILE2 = "FILE2"
    """str or unicode: token for file2 in command-line specification"""

    def __init__(self):
        """Create comparator.
        """
        super(ProvToolboxComparator, self).__init__()

    def configure(self, config):
        """Configure comparator. The configuration must hold:

        - :class:`prov_interop.comparator.Comparator` configuration
        - :class:`prov_interop.component.CommandLineComponent` configuration

        ``arguments`` must have tokens ``FORMAT1``, ``FORMAT2``,
        ``FILE1``, ``FILE2``, which are place-holders for the the files and
        their formats.

        A valid configuration is::

          {
            "executable": "provconvert"
            "arguments": "-infile FILE1 -compare FILE2"
            "formats": ["provx", "json"]
          }

        :param config: Configuration
        :type config: dict
        :raises ConfigError: if `config` does not hold the above entries
        """
        super(ProvToolboxComparator, self).configure(config)
        for token in [
            ProvToolboxComparator.FILE1,
            ProvToolboxComparator.FILE2
        ]:
            if token not in self._arguments:
                raise ConfigError("Missing token " + token)

    def compare(self, file1, file2):
        """Compare files.

        - File formats are derived from `file1` and `file1` file extensions.
        - A check is done to see that `file1` and `file2` exist and that
          their formats are in ``formats``.
        - ``executable`` and ``arguments`` are used to create a
          command-line invocation, with ``FORMAT1``, ``FORMAT2``,
          ``FILE1`` and ``FILE2`` being replaced with the file formats,
          `in_file`, and `out_file`
        - If either format is ``provx`` then ``xml`` is used (as
          ``prov-compare`` does not recognise ``provx``).

        An example command-line invocation is::

          prov-compare -f xml -F xml testcase1.provx converted.provx

        :param file1: File
        :type file1: str or unicode
        :param file2: File
        :type file2: str or unicode
        :return: ``True`` or ``False``
        :rtype: bool
        :raises ComparisonError: if either of the files cannot be found,
          or the exit code of ``prov-compare`` is neither 0 nor 1
        :raises OSError: if there are problems invoking the comparator
          e.g. the script is not found
        """
        super(ProvToolboxComparator, self).compare(file1, file2)
        format1 = os.path.splitext(file1)[1][1:]
        format2 = os.path.splitext(file2)[1][1:]
        self.check_format(format1)
        self.check_format(format2)

        command_line = list(self._executable)
        command_line.extend(self._arguments)
        command_line = [format1 if x == ProvToolboxComparator.FORMAT1 else x
                        for x in command_line]
        command_line = [format2 if x == ProvToolboxComparator.FORMAT2 else x
                        for x in command_line]
        command_line = [file1 if x == ProvToolboxComparator.FILE1 else x
                        for x in command_line]
        command_line = [file2 if x == ProvToolboxComparator.FILE2 else x
                        for x in command_line]
        print((" ".join(command_line)))
        return_code = subprocess.call(command_line)
        if return_code == 0:
            return True
        elif return_code == 6:
            return False
        else:
            raise ComparisonError(" ".join(command_line) +
                                  " returned " + str(return_code))
