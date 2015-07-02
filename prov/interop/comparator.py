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

from prov.interop.component import ConfigError
from prov.interop.component import ConfigurableComponent

class Comparator(ConfigurableComponent):
  """Base class for comparators."""

  def __init__(self):
    """Create comparator.
    Invokes super-class ``__init__``.
    """
    super(Comparator, self).__init__()
    self._formats = []

  @property
  def formats(self):
    """Gets list of formats supported by the comparator.

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
    of str or unicode)
    """
    super(Comparator, self).configure(config)
    if not "formats" in config:
      raise ConfigError("Missing 'formats'");
    self._formats = config["formats"]

  def compare(self, expected_file, expected_format, actual_file, actual_format):
    """Invoke comparison of expected file in given format to actual
    file in given format.

    :param expected_file: Expected file name
    :type expected_file: str or unicode
    :param expected_format: Expected format
    :type expected_format: str or unicode
    :param actual_file: Actual file name
    :type actual_file: str or unicode
    :param actual_format: Actual format
    :type actual_format: str or unicode
    :returns: True (success) if files are equivalent, else False (fail)
    :rtype: bool
    :raises ComparisonError: if there are problems invoking the comparator 
    """
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
