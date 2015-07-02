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

from prov.interop.component import CommandLineComponent
from prov.interop.component import ConfigError
from prov.interop.converter import Converter

class ProvToolboxConverter(Converter, CommandLineComponent):
  """Manages invocation of ProvToolbox provconvert script."""

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
    tokens ``PROV_INPUT``, ``PROV_OUTPUT``
    """
    super(ProvToolboxConverter, self).configure(config)
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
    :returns: True (success) or False (fail)
    :rtype: bool
    :raises ConversionError: if there are problems invoking the converter 
    """
    # TODO
    print("Execute " + self._directory + "/" + self._executable + " " +
        str(self._arguments))
    # Replace tokens
    # Execute prov-convert.
    # Capture return code, standard output, standard error.
    # Check both return code and existence of output file.
    # ProvToolbox's provconvert returns an exit code of 1 if there is no input file, the input file is not a valid PROV document or the input file format is not supported. It returns an exit code of 0 if successful or, problematically, if the output file format is not supported. However, it does not create any output files if any file or file format is invalid, so that allows for conversion failures to be detected.
    # Sub-classes can replace the tokens with the output format, input and output file names when constructing the command to invoke. 

