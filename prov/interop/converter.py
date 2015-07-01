"""Base class, and related classes, for converters.
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

from prov.interop.component import ConfigurableComponent

class Converter(ConfigurableComponent):
  """Base class for converters."""

  def __init__(self):
    """Create converter.
    Can be overriden by sub-classes.
    """
    super(ConfigurableComponent, self).__init__()

  def get_input_formats(self):
    """Gets list of input formats supported by the converter.

    :returns: formats
    :rtype: list of str or unicode
    """
    pass

  def get_output_formats(self):
    """Gets list of output formats supported by the converter.

    :returns: formats
    :rtype: list of str or unicode
    """
    pass

  def configure(self, config):
    """Configure converter.
    Can be overriden by sub-classes.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config is not a dict.
    """
    super(Converter, self).configure(config)

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
    pass

class ConversionError(Exception):
  """Conversion error."""

  def __init__(self, value):
    """Create conversion error.

    :param value: Value holding information about error
    :type value: str or unicode or list of str or unicode
    """
    self._value = value

  def __str__(self):
    """Get error as formatted string.

    :returns: formatted string
    :rtype: str or unicode
    """
    return repr(self._value)
