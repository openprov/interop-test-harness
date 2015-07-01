"""Base class, and related classes, for configurable components.
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

class ConfigurableComponent(object):
  """Base class for configurable components."""

  def __init__(self):
    """Create component.
    Can be overriden by sub-classes.
    """
    pass

  def configure(self, config):
    """Configure component.
    Can be overriden by sub-classes.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config is not a dict
    """
    if not type(config) is dict:
      raise ConfigError("config must be a dictionary");

class ConfigError(Exception):
  """Configuration error."""

  def __init__(self, value):
    """Create configuration error.

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
