"""Test classes for ``prov_interop.component``.
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
import shutil
import tempfile
import unittest
import yaml

from prov_interop.component import CommandLineComponent
from prov_interop.component import ConfigurableComponent
from prov_interop.component import ConfigError
from prov_interop.component import load_configuration
from prov_interop.component import RestComponent

class ConfigurableComponentTestCase(unittest.TestCase):

  def setUp(self):
    super(ConfigurableComponentTestCase, self).setUp()
    self.config = {"a":"b", "c":"d", "e":["f", "g", 123]}
    self.component = ConfigurableComponent()

  def test_configure_empty(self):
    self.component.configure({})
    self.assertEqual({}, self.component.configuration)

  def test_configure_non_empty(self):
    self.component.configure(self.config)
    self.assertEqual(self.config, self.component.configuration)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.component.configure(123)

  def test_check_configuration(self):
    self.component.configure(self.config)
    self.component.check_configuration(["a", "c", "e"])
    self.assertTrue(True)

  def test_check_configuration_error(self):
    self.component.configure(self.config)
    with self.assertRaises(ConfigError):
      self.component.check_configuration(["a", "c", "expectfail"])


class CommandLineComponentTestCase(unittest.TestCase):

  def setUp(self):
    super(CommandLineComponentTestCase, self).setUp()
    self.command_line = CommandLineComponent()

  def test_init(self):
    self.assertEqual("", self.command_line.executable)
    self.assertEqual([], self.command_line.arguments)
    self.assertEqual({}, self.command_line.configuration)

  def test_configure(self):
    config = {CommandLineComponent.EXECUTABLE: "a", 
              CommandLineComponent.ARGUMENTS: ["b", 1]}
    self.command_line.configure(config)
    self.assertEqual(config, self.command_line.configuration)
    self.assertEqual("a", self.command_line.executable)
    self.assertEqual(["b", 1], self.command_line.arguments)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.command_line.configure(123)

  def test_configure_no_executable(self):
    with self.assertRaises(ConfigError):
      self.command_line.configure({CommandLineComponent.ARGUMENTS: ["b", 1]})

  def test_configure_no_arguments(self):
    with self.assertRaises(ConfigError):
      self.command_line.configure({CommandLineComponent.EXECUTABLE: "a"})


class RestComponentTestCase(unittest.TestCase):

  def setUp(self):
    super(RestComponentTestCase, self).setUp()
    self.rest = RestComponent()

  def test_init(self):
    self.assertEqual("", self.rest.url)
    self.assertEqual({}, self.rest.configuration)

  def test_configure(self):
    config = {RestComponent.URL: "a"}
    self.rest.configure(config)
    self.assertEqual(config, self.rest.configuration)
    self.assertEqual("a", self.rest.url)

  def test_configure_non_dict_error(self):
    with self.assertRaises(ConfigError):
      self.rest.configure(123)

  def test_configure_no_url(self):
    with self.assertRaises(ConfigError):
      self.rest.configure({})


class LoadConfigurationTestCase(unittest.TestCase):

  def setUp(self):
    super(LoadConfigurationTestCase, self).setUp()
    self.config={"counter": 12345}
    (_, self.yaml) = tempfile.mkstemp(suffix=".yaml")
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write(yaml.dump(self.config, default_flow_style=False))
    self.env_var = "PROV_LOAD_CONFIG"
    self.default_file = os.path.join(os.getcwd(), "test_component.yaml")

  def tearDown(self):
    super(LoadConfigurationTestCase, self).tearDown()
    if self.yaml != None and os.path.isfile(self.yaml):
      os.remove(self.yaml)
      
  def test_load_configuration_from_file(self):
    config = load_configuration(self.env_var,
                                self.default_file,
                                self.yaml)
    self.assertEqual(12345, config["counter"])

  def test_load_configuration_from_env(self):
    os.environ[self.env_var] = self.yaml
    config = load_configuration(self.env_var,
                                self.default_file,
                                self.yaml)
    self.assertEqual(12345, config["counter"])

  def test_load_configuration_from_default(self):
    shutil.move(self.yaml, self.default_file)
    self.yaml = self.default_file
    config = load_configuration(self.env_var,
                                self.default_file)
    self.assertEqual(12345, config["counter"])

  def test_load_configuration_from_file_missing_file(self):
    with self.assertRaises(IOError):
      config = load_configuration(self.env_var,
                                  self.default_file,
                                  "nosuchfile.yaml")
      
  def test_load_configuration_from_file_non_yaml_file(self):
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write("This is an invalid YAML file")
      with self.assertRaises(ConfigError):
        config = load_configuration(self.env_var,
                                    self.default_file,
                                    self.yaml)
