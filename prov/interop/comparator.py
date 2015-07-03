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

from prov.interop import standards
from prov.interop.component import ConfigError
from prov.interop.component import ConfigurableComponent

class Comparator(ConfigurableComponent):
  """Base class for comparators."""

  FORMATS = "formats"

  def __init__(self):
    """Create comparator.
    Invokes super-class ``__init__``.
    """
    super(Comparator, self).__init__()
    self._formats = []

  @property
  def formats(self):
    """Gets list of canonical formats supported by the comparator.

    :returns: formats
    :rtype: list of str or unicode
    """
    return self._formats

  def configure(self, config):
    """Configure comparator.
    Invokes super-class ``configure``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config does not contain ``formats`` (list
    of str or unicode) or any format in ``formats`` is not a canonical
    format (see ``standards``)
    """
    super(Comparator, self).configure(config)
    Comparator.check_configuration(config, [Comparator.FORMATS])
    for format in config[Comparator.FORMATS]:
      if not format in standards.FORMATS:
        raise ConfigError("Unrecognised format in " + Comparator.FORMATS +
                          ":" + format)
    self._formats = config[Comparator.FORMATS]

  def compare(self, file1, file2):
    """Invoke comparison of files in canonical formats.
    Each file must have an extension matching one of the canonical
    file formats.
    Canonical formats are defined in ``standards``.

    :param file1: File name
    :type file1: str or unicode
    :param file2: File name
    :type file2: str or unicode
    :returns: True (success) if files are equivalent, else False (fail)
    :rtype: bool
    :raises ComparisonError: if there are problems invoking the comparator 
    """
    # TODO validate files exist
    # TODO validate file extensions
    pass

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
