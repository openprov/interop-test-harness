"""Base class, and related classes, for comparators.
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

class Comparator(ConfigurableComponent):
  """Base class for comparators."""

  FORMATS = "formats"
  """str or unicode: configuration key for supported formats
  """

  def __init__(self):
    """Create comparator.
    """
    super(Comparator, self).__init__()
    self._formats = []

  @property
  def formats(self):
    """Gets formats supported by the comparator. Formats are defined
    in ``prov_interop.standards``.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._formats

  def configure(self, config):
    """Configure comparator. ``config`` must hold entries::

        formats: [...list of formats from prov_interop.standards...]

    For example::

        formats: [provx, json]

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(Comparator, self).configure(config)
    self.check_configuration([Comparator.FORMATS])
    for format in config[Comparator.FORMATS]:
      if format not in standards.FORMATS:
        raise ConfigError("Unrecognised format in " + Comparator.FORMATS +
                          ":" + format)
    self._formats = config[Comparator.FORMATS]

  def check_format(self, format):
    """Check given format is supported.

    :param format: Format
    :type iormat: str or unicode
    :raises ComparisonError: if the format is not supported
    """
    if format not in self.formats:
      raise ComparisonError("Unsupported format: " + format)

  def compare(self, file1, file2):
    """Compare two files. Each file must have an extension matching a
    format in ``prov_interop.standards``.

    :param file1: File name
    :type file1: str or unicode
    :param file2: File name
    :type file2: str or unicode
    :returns: True (success) if files are equivalent, else False 
    (fail)
    :rtype: bool
    :raises ComparisonError: if either of the files are not found
    """
    for f in [file1, file2]:
      if not os.path.isfile(f):
        raise ComparisonError("File not found: " + f)


class ComparisonError(Exception):
  """Comparison error."""

  def __init__(self, value):
    """Create comparison error.

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
