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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.component import ConfigurableComponent

class Converter(ConfigurableComponent):
  """Base class for converters."""

  INPUT_FORMATS = "input-formats"
  """str or unicode: configuration key for converter's supported input formats"""
  OUTPUT_FORMATS = "output-formats"
  """str or unicode: configuration key for converter's supported output formats"""

  def __init__(self):
    """Create converter.
    """
    super(Converter, self).__init__()
    self._input_formats = []
    self._output_formats = []

  @property
  def input_formats(self):
    """Gets list of input formats supported by the converter.
   Formats are a subset of those in ``prov_interop.standards``.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._input_formats

  @property
  def output_formats(self):
    """Gets list of canonical ouput formats supported by the converter.
   Formats are a subset of those in ``prov_interop.standards``.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._output_formats

  def configure(self, config):
    """Configure converter.
    ``config`` is expected to hold configuration of form::

        input-formats: [...list of formats...]
        output-formats: [...list of formats...]

    For example::

        input-formats: [json]
        output-formats: [provn, provx, json]

    Formats must be as defined in ``prov_interop.standards``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(Converter, self).configure(config)
    Converter.check_configuration(
      config, [Converter.INPUT_FORMATS, Converter.OUTPUT_FORMATS])
    for key in [Converter.INPUT_FORMATS, Converter.OUTPUT_FORMATS]:
      for format in config[key]:
        if format not in standards.FORMATS:
          raise ConfigError("Unrecognised format in " + key +
                            ":" + format)
    self._input_formats = config[Converter.INPUT_FORMATS]
    self._output_formats = config[Converter.OUTPUT_FORMATS]

  def check_formats(self, in_format, out_format):
    """Check given formats are in the input and output formats
    supported by the converter.

    :param in_format: Input format
    :type in_format: str or unicode
    :param out_format: Output format
    :type out_format: str or unicode
    :raises ConversionError: if the input or output formats are
    not in those supported by the converter
    """
    if in_format not in self.input_formats:
      raise ConversionError("Unsupported input format: " + in_format)
    if out_format not in self.output_formats:
      raise ConversionError("Unsupported input format: " + out_format)

  def convert(self, in_file, out_file):
    """Use converter to convert an input file into an output
    file. Each file must have an extension matching one of those
    in ``prov_interop.standards``.

    :param in_file: Input file name
    :type in_file: str or unicode
    :param out_file: Output file name
    :type out_file: str or unicode
    :raises ConversionError: if the input file is not found
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
