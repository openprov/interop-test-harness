"""Manages invocation of ProvPy prov-convert script.
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

class ProvPyConverter(Converter, CommandLineComponent):
  """Manages invocation of ProvPy prov-convert script."""

  def __init__(self):
    """Create converter.
    Invokes super-classes ``__init__``.
    """
    super(ProvPyConverter, self).__init__()

  def configure(self, config):
    """Configure converter.
    Invokes super-classes ``__configure__``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config ``arguments`` does not contain the
    tokens ``PROV_FORMAT``, ``PROV_INPUT``, ``PROV_OUTPUT``
    """
    super(ProvPyConverter, self).configure(config)
    if not "PROV_FORMAT" in self._arguments:
      raise ConfigError("Missing PROV_FORMAT token in 'arguments'")
    if not "PROV_INPUT" in self._arguments:
      raise ConfigError("Missing PROV_INPUT token in 'arguments'")
    if not "PROV_OUTPUT" in self._arguments:
      raise ConfigError("Missing PROV_OUTPUT token in 'arguments'")

  def convert(self, in_file, in_format, out_file, out_format):
    """Invoke conversion of input file in given format to output
    file in given format.

    :param in_file: Input file name
    :type in_file: str or unicode
    :param in_format: Input format
    :type in_format: str or unicode
    :param out_file: Output file name
    :type out_file: str or unicode
    :param out_format: Output format
    :type out_format: str or unicode
    :raises ConversionError: if the input file is not found, the
    return code is non-zero, or the return code is zero but the output
    file is not found.
    :raises OSError: if there are problems invoking the converter
    e.g. the script is not found at the specified location.
    """
    if not os.path.isfile(in_file):
      raise ConversionError("Input file not found: " + in_file)
    # Replace tokens in arguments
    command_line = [in_file if x=="PROV_INPUT" else x for x in self._arguments]
    command_line = [out_file if x=="PROV_OUTPUT" else x for x in command_line]
    command_line = [in_format if x=="PROV_FORMAT" else x for x in command_line]
    command_line.insert(0, self.executable)
    return_code = subprocess.call(command_line)
    if return_code != 0:
      raise ConversionError(self._executable + " returned " + str(return_code))
    if not os.path.isfile(out_file):
      raise ConversionError("Output file not found: " + out_file)
