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

import os
import yaml

class ConfigurableComponent(object):
  """Base class for configurable components."""

  def __init__(self):
    """Create component.
    """
    self._config = {}

  @property
  def configuration(self):
    """Get raw configuration.

    :returns: configuration
    :rtype: dict
    """
    return self._config

  def configure(self, config):
    """Configure component.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config is not a dict
    """
    if not type(config) is dict:
      raise ConfigError("config must be a dictionary")
    self._config = config

  @staticmethod
  def check_configuration(config, keys):
    """Check configuration contains keys.

    :param config: Configuration
    :type config: dict or list
    :param keys: Keys to check for
    :type keys: list of str or unicode
    :raises ConfigError: if config does not contain one of the keys
    """
    for key in keys:
      if not key in config:
        raise ConfigError("Missing " + key)


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


class CommandLineComponent(ConfigurableComponent):
  """Base class for configurable command-line components."""

  EXECUTABLE = "executable"
  """string or unicode: configuration key for component's executable"""
  ARGUMENTS = "arguments"
  """string or unicode: configuration key for component's arguments"""

  def __init__(self):
    """Create component.
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
    ``config`` is expected to hold configuration of form::

        executable: ...executable name...
        arguments: [...list of arguments ...]

    For example::

        executable: python
        arguments: [/home/user/prov/scripts/prov-convert, -f, FORMAT, INPUT, OUT
PUT]

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
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
  """string or unicode: configuration key for REST endpoint URL"""

  def __init__(self):
    """Create component.
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
    ``config`` is expected to hold configuration of form::

        url: ...REST endpoint URL...

    For example::

        url: https://provenance.ecs.soton.ac.uk/validator/provapi/documents/

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
    super(RestComponent, self).configure(config)
    RestComponent.check_configuration(config, [RestComponent.URL])
    self._url = config[RestComponent.URL]


def load_configuration(env_var, default_file_name, file_name = None):
  """Load configuration from a YAML file.
  - If ``file_name`` is provided then the contents of the file are
  loaded and returned.
  - Else, if an environment variable with name ``env_var`` is defined,
  then the contents of the file named in that variable are loaded.
  - Else, the contents of the default file, ``default_file_name``, 
  are loaded.
  
  :param env_var: Environment variable with configuration file name
  :type env_var: str or unicode
  :param default_file_name: Default configuration file name
  :type file_name: str or unicode
  :param file_name: Configuration file name (optional)
  :type file_name: str or unicode
  :returns: configuration
  :rtype: dict
  :raises IOError: if the file is not found
  :raises ConfigError: if the file does not parse into a dict
  """
  if (file_name is None):
    try:
      file_name = os.environ[env_var]
    except KeyError:
      file_name = default_file_name
  with open(file_name, 'r') as f:
    config = yaml.load(f)
    if not type(config) is dict:
      raise ConfigError(file_name + " does not contain a valid YAML document")
    return config
