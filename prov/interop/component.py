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
    """
    pass

  def configure(self, config):
    """Configure component.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config is not a dict
    """
    if not type(config) is dict:
      raise ConfigError("config must be a dictionary")

  @staticmethod
  def check_configuration(config, values):
    """Check configuration contains values.

    :param config: Configuration
    :type config: dict or list
    :param values: Values to check for
    :type values: list of str or unicode
    :raises ConfigError: if config does not contain any of the values
    """
    for value in values:
      if not value in config:
        raise ConfigError("Missing " + value)


class CommandLineComponent(ConfigurableComponent):
  """Base class for configurable command-line components."""

  EXECUTABLE = "executable"
  ARGUMENTS = "arguments"

  def __init__(self):
    """Create component.
    Invokes super-class ``__init__``.
    """
    super(CommandLineComponent, self).__init__()
    self._executable = ""
    self._arguments = []

  @property
  def executable(self):
    """Get the executable.
    
    :returns: executable
    :rtype: str or unicode
    """
    return self._executable

  @property
  def arguments(self):
    """Get the arguments.
    
    :returns: arguments
    :rtype: list of str or unicode or int or float
    """
    return self._arguments

  def configure(self, config):
    """Configure component.
    Invokes super-class ``configure``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config does not contain ``executable``
    (str or unicode) and ``arguments`` (list of str or unicode or int
    or float) 
    """
    super(CommandLineComponent, self).configure(config)
    CommandLineComponent.check_configuration(
      config, [CommandLineComponent.EXECUTABLE, 
               CommandLineComponent.ARGUMENTS])
    self._executable = config[CommandLineComponent.EXECUTABLE]
    self._arguments = config[CommandLineComponent.ARGUMENTS]


class RestComponent(ConfigurableComponent):
  """Base class for configurable REST-ful components."""

  URL = "url"

  def __init__(self):
    """Create component.
    Invokes super-class ``__init__``.
    """
    super(RestComponent, self).__init__()
    self._url = ""

  @property
  def url(self):
    """Get the URL.
    
    :returns: URL
    :rtype: str or unicode
    """
    return self._url

  def configure(self, config):
    """Configure component.
    Invokes super-class ``configure``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config does not contain ``url`` (str or 
    unicode)
    """
    super(RestComponent, self).configure(config)
    RestComponent.check_configuration(config, [RestComponent.URL])
    self._url = config[RestComponent.URL]


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
