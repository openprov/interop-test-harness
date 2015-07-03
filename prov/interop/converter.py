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

import os

from prov.interop import standards
from prov.interop.component import ConfigError
from prov.interop.component import ConfigurableComponent

class Converter(ConfigurableComponent):
  """Base class for converters."""

  INPUT_FORMATS = "input_formats"
  OUTPUT_FORMATS = "output_formats"

  def __init__(self):
    """Create converter.
    Invokes super-class ``__init__``.
    """
    super(Converter, self).__init__()
    self._input_formats = []
    self._output_formats = []

  @property
  def input_formats(self):
    """Gets list of canonical input formats supported by the converter.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._input_formats

  @property
  def output_formats(self):
    """Gets list of canonical ouput formats supported by the converter.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._output_formats

  def configure(self, config):
    """Configure converter.
    Invokes super-class ``configure``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config does not contain ``input_formats``
    (list of str or unicode) and ``output_formats`` (list of str or
    unicode) or any format in ``input_formats`` or ``output_formats``
    is not a canonical format (see ``standards``)
    """
    super(Converter, self).configure(config)
    Converter.check_configuration(
      config, [Converter.INPUT_FORMATS, Converter.OUTPUT_FORMATS])
    for key in [Converter.INPUT_FORMATS, Converter.OUTPUT_FORMATS]:
      for format in config[key]:
        if not format in standards.FORMATS:
          raise ConfigError("Unrecognised format in " + key +
                            ":" + format)
    self._input_formats = config[Converter.INPUT_FORMATS]
    self._output_formats = config[Converter.OUTPUT_FORMATS]

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
    :raises ConversionError: if either file does not exist
    """
    if not os.path.isfile(in_file):
      raise ConversionError("Input file not found: " + in_file)

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
