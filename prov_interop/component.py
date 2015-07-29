"""Base class, related classes, and helpers for configurable components.
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

class ConfigurableComponent(object):
  """Base class for configurable components."""

  def __init__(self):
    """Create component.
    """
    self._config = {}

  @property
  def configuration(self):
    """Get configuration.

    :return: configuration
    :rtype: dict
    """
    return self._config

  def check_configuration(self, keys):
    """Check configuration contains keys.

    :param config: Configuration
    :type config: dict or list
    :param keys: Keys to check for
    :type keys: dict or list
    :raises ConfigError: if config does not contain one of the keys
    """
    for key in keys:
      if key not in self._config:
        raise ConfigError("Missing " + key)

  def configure(self, config):
    """Configure component. Any configuration not specific to a
    component is ignored.

    :param config: Component-specific configuration
    :type config: dict
    :raises ConfigError: if config is not a dict
    """
    if type(config) is not dict:
      raise ConfigError("config must be a dictionary")
    self._config = config


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

    :return: formatted string
    :rtype: str or unicode
    """
    return repr(self._value)


class CommandLineComponent(ConfigurableComponent):
  """Base class for command-line components."""

  EXECUTABLE = "executable"
  """str or unicode: configuration key for executable"""
  ARGUMENTS = "arguments"
  """str or unicode: configuration key for arguments"""

  def __init__(self):
    """Create component.
    """
    super(CommandLineComponent, self).__init__()
    self._executable = ""
    self._arguments = []

  @property
  def executable(self):
    """Get the executable as a list of strings. The ``executable``
    value provided during configuration is split upon spaces and
    returned.
   
    :return: executable
    :rtype: list of str or unicode
    """
    return self._executable

  @property
  def arguments(self):
    """Get the arguments as a list. The ``arguments`` value provided
  during configuration is split upon spaces and returned.
    
    :return: arguments
    :rtype: list of str or unicode
    """
    return self._arguments

  def configure(self, config):
    """Configure component. The configuration must hold:

    - ``executable``: the name of the executable. This may be a single
      executable file name or an executable name and a script
      name. Executables may be prefixed with their absolute path
      depending on whether or not they are on the system path. 
    - ``arguments``: arguments for the executable.

    Valid configurations include::

      {
        "executable": "/home/user/ProvToolbox/bin/provconvert",
        "arguments": "-infile INPUT -outfile OUTPUT"
      }
      {
        "executable": "prov-convert",
        "arguments": "-f FORMAT INPUT OUTPUT"
      }
      {
        "executable": "python /home/user/ProvPy/scripts/prov-convert",
        "arguments": "-f FORMAT INPUT OUTPUT"
      }

    Both values may include tokens that can be replaced at run time
    with actual values. This is the responsibility of sub-classes. For
    example, `INPUT` and `OUTPUT` would be replaced with input and
    output file names. 

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(CommandLineComponent, self).configure(config)
    self.check_configuration([CommandLineComponent.EXECUTABLE, 
                              CommandLineComponent.ARGUMENTS])
    self._executable = config[CommandLineComponent.EXECUTABLE].split()
    self._arguments = config[CommandLineComponent.ARGUMENTS].split()


class RestComponent(ConfigurableComponent):
  """Base class for REST-ful components."""

  URL = "url"
  """str or unicode: configuration key for REST endpoint URL"""

  def __init__(self):
    """Create component.
    """
    super(RestComponent, self).__init__()
    self._url = ""

  @property
  def url(self):
    """Get the URL.
    
    :return: URL
    :rtype: str or unicode
    """
    return self._url

  def configure(self, config):
    """Configure component. The configuration must hold:

    - ``url``: REST endpoint for POST requests.

    A valid configuration is::

      {
        "url": "https://provenance.ecs.soton.ac.uk/validator/provapi/documents/"
      }

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(RestComponent, self).configure(config)
    self.check_configuration([RestComponent.URL])
    self._url = config[RestComponent.URL]
