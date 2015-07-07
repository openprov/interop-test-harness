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

from prov.interop.comparator import Comparator
from prov.interop.component import ConfigError
from prov.interop.component import ConfigurableComponent
from prov.interop.factory import FactoryUtilities

class HarnessConfiguration(ConfigurableComponent):
  """Interoperability test harness configuration."""

  TEST_CASES = "test_cases"
  COMPARATORS = "comparators"
  CLASS_NAME = "class_name"

  def __init__(self):
    """Create harness configuration.
    Invokes super-class ``__init__``.
    """
    super(HarnessConfiguration, self).__init__()
    self._configuration = {}
    self._test_cases = ""
    self._comparators = {}
    self._format_comparators = {}

  @property
  def configuration(self):
    """Gets raw configuration.

    :returns: configuration
    :rtype: dict
    """
    return self._configuration

  @property
  def test_cases(self):
    """Gets test_cases directory

    :returns: directory name
    :rtype: list of str or unicode
    """
    return self._test_cases

  @property
  def comparators(self):
    """Gets dictionary of comparators.

    :returns: comparators
    :rtype: dict from str or unicode to Comparator
    """
    return self._comparators

  @property
  def format_comparators(self):
    """Gets dictionary of comparators keyed by formats (see
    ``standards``).

    :returns: comparators
    :rtype: dict from str or unicode to Comparator
    """
    return self._format_comparators

  def register_comparators(self, comparators):
    """Populate dictionary mapping comparator names to
    instances of Comparator sub-classes.

    :param comparators: Mapping of comparator names to 
    comparator-specific configuration.
    :type config: dict mapping str or unicode to dict
    :raises ConfigError: if there is a problem creating a
    Comparator (e.g. missing configuration), or there are no
    comparators
    """
    if len(comparators) == 0:
      raise ConfigError("There must be at least one comparator defined")
    for comparator_name in comparators:
      config = comparators[comparator_name]
      HarnessConfiguration.check_configuration(
        config, [HarnessConfiguration.CLASS_NAME])
      class_name = config[HarnessConfiguration.CLASS_NAME]
      comparator = FactoryUtilities.get_instance(class_name)
      comparator.configure(config)
      self._comparators[comparator_name] = comparator
      for format in comparator.formats:
        self._format_comparators[format] = comparator

  def configure(self, config):
    """Configure harness configuration.
    Invokes super-class ``configure``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if config does not contain ``test_cases``
    (str or unicode) and ``comparators`` (dict mapping str or unicode
    to Comparator configurations with additional ``class_name``
    key), or if there is a problem creating a Comparator.
    """
    super(HarnessConfiguration, self).configure(config)
    HarnessConfiguration.check_configuration(
      config,
      [HarnessConfiguration.TEST_CASES,
       HarnessConfiguration.COMPARATORS])
    self._configuration = config
    self._test_cases = config[HarnessConfiguration.TEST_CASES]
    self.register_comparators(config[HarnessConfiguration.COMPARATORS])
