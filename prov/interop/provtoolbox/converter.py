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

import os.path
import subprocess

from prov.interop.component import CommandLineComponent
from prov.interop.component import ConfigError
from prov.interop.converter import ConversionError
from prov.interop.converter import Converter

class ProvToolboxConverter(Converter, CommandLineComponent):
  """Manages invocation of ProvToolbox provconvert script."""

  INPUT = "INPUT"
  OUTPUT = "OUTPUT"

  def __init__(self):
    """Create converter.
    Invokes super-classes ``__init__``.
    """
    super(ProvToolboxConverter, self).__init__()

  def configure(self, config):
    """Configure converter.
    Invokes super-classes ``__configure__``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config ``arguments`` does not contain the
    tokens ``INPUT``, ``OUTPUT``
    """
    super(ProvToolboxConverter, self).configure(config)
    ProvToolboxConverter.check_configuration(
      self._arguments,
      [ProvToolboxConverter.INPUT, ProvToolboxConverter.OUTPUT])

  def convert(self, in_file, out_file):
    """Invoke conversion of input file in a canonical format to output
    file in a canonical format. 
    Each file must have an extension matching one of the canonical
    file formats.
    Canonical formats are defined in ``standards``.

    :param in_file: Input file name
    :type in_file: str or unicode
    :param out_file: Output file name
    :type out_file: str or unicode
    :raises ConversionError: if the input file is not found, the
    return code is non-zero, the return code is zero but the output
    file is not found, the input or output formats are invalid.
    :raises OSError: if there are problems invoking the converter
    e.g. the script is not found at the specified location.
    """
    if not os.path.isfile(in_file):
      raise ConversionError("Input file not found: " + in_file)
    in_format = os.path.splitext(in_file)[1][1:]
    out_format = os.path.splitext(out_file)[1][1:]
    # TODO check formats in input/output formats
    # TODO map to local format
    # Replace tokens in arguments
    command_line = [in_file if x==ProvToolboxConverter.INPUT else x 
                    for x in self._arguments]
    command_line = [out_file if x==ProvToolboxConverter.OUTPUT else x 
                    for x in command_line]
    command_line.insert(0, self.executable)
    # Execute
    return_code = subprocess.call(command_line)
    if return_code != 0:
      raise ConversionError(self._executable + " returned " + str(return_code))
    if not os.path.isfile(out_file):
      raise ConversionError("Output file not found: " + out_file)
