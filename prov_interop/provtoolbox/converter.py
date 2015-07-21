"""Manages invocation of ProvToolbox provconvert script.
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
from prov_interop.converter import ConversionError
from prov_interop.converter import Converter

class ProvToolboxConverter(Converter, CommandLineComponent):
  """Manages invocation of ProvToolbox provconvert script."""

  INPUT = "INPUT"
  """str or unicode: token for input file in command-line specification"""
  OUTPUT = "OUTPUT"
  """str or unicode: token for output file in command-line specification"""

  def __init__(self):
    """Create converter.
    """
    super(ProvToolboxConverter, self).__init__()

  def configure(self, config):
    """Configure converter.
    ``config`` is expected to hold configuration of form::

        executable: ...executable name...
        arguments: [...list of arguments including tokens INPUT, OUTPUT...]
        input-formats: [...list of formats...]
        output-formats: [...list of formats...]

    For example::

        executable: /home/user/ProvToolbox/bin/provconvert
        arguments: [-infile, INPUT, -outfile, OUTPUT]
        input-formats: [provn, ttl, trig, provx, json]
        output-formats: [provn, ttl, trig, provx, json]

    Input and output formats must be as defined in
    ``prov_interop.standards``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above
    entries
    """
    super(ProvToolboxConverter, self).configure(config)
    ProvToolboxConverter.check_configuration(
      self._arguments,
      [ProvToolboxConverter.INPUT, ProvToolboxConverter.OUTPUT])

  def convert(self, in_file, out_file):
    """Use provconvert to convert an input file into an output
    file. Each file must have an extension matching one of those
    in ``prov_interop.standards``.
    ``executable`` and ``arguments`` in the configuration are used to
    create a command to execute at the shell. `
    ``INPUT`` and ``OUTPUT`` tokens are populated using
    ``in_file``, ``out_file`` values, with mappings to local formats
    supported by provcconvert being done if needed.

    :param in_file: Input file name
    :type in_file: str or unicode
    :param out_file: Output file name
    :type out_file: str or unicode
    :raises ConversionError: if the input file is not found, the
    return code is non-zero, the return code is zero but the output
    file is not found, the input or output formats are invalid
    :raises OSError: if there are problems invoking the converter
    e.g. the script is not found
    """
    super(ProvToolboxConverter, self).convert(in_file, out_file)
    in_format = os.path.splitext(in_file)[1][1:]
    out_format = os.path.splitext(out_file)[1][1:]
    super(ProvToolboxConverter, self).check_formats(in_format, out_format)
    # Replace tokens in arguments
    command_line = [in_file if x==ProvToolboxConverter.INPUT else x 
                    for x in self._arguments]
    command_line = [out_file if x==ProvToolboxConverter.OUTPUT else x 
                    for x in command_line]
    command_line.insert(0, self.executable)
    # Execute
    print((" ".join(command_line)))
    return_code = subprocess.call(command_line)
    if return_code != 0:
      raise ConversionError(self._executable + " returned " + str(return_code))
    if not os.path.isfile(out_file):
      raise ConversionError("Output file not found: " + out_file)
