"""Test classes for prov.interop.factory.
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

import inspect
import os
import shutil
import tempfile
import unittest
import yaml

import prov.interop.factory as factory

class Counter:
  """Dummy class for testing FactoryUtilities."""

  def __init__(self):
    """Set counter to 0."""
    self._counter = 0
    
  def increment(self):
    """Increment counter."""
    self._counter += 1

  def get_counter(self):
    """Gets counter value.

    :returns: counter value
    :rtype: int
    """
    return self._counter

  def configure(self, config):
    """Sets counter value.

    :param config: dict with ``counter`` entry with new value for counter.
    :type config: dict
    :raises KeyError: if no ``counter`` entry in dict.
    :raises TypeError: if ``config`` is not a dict
    """
    self._counter = int(config["counter"])


class Value:
  """Dummy class for testing FactoryUtilities."""

  def __init__(self, value):
    """Store value.

    :param value:
    :type name: int
    """
    self._value = value


class FactoryCreateTestCase(unittest.TestCase):

  def test_get_class(self):
    my_module = self.__module__
    clazz = factory.get_class(str(self.__module__) + ".Counter")
    self.assertEquals(Counter, clazz, msg="Expected Counter class")

  def test_get_class_no_prefix(self):
    with self.assertRaises(ValueError):
      factory.get_class("Counter")

  def test_get_class_no_such_module(self):
    with self.assertRaises(ImportError):
      factory.get_class("nosuchmodule.NoSuchClass")

  def test_get_class_no_such_class(self):
    with self.assertRaises(AttributeError):
      factory.get_class(str(self.__module__) + ".NoSuchClass")

  def test_get_instance(self):
    my_module = self.__module__
    obj = factory.get_instance(str(self.__module__) + ".Counter")
    self.assertIsInstance(obj, Counter, msg="Expected Counter object")
    obj.increment()
    obj.increment()
    self.assertEquals(2, obj.get_counter(), msg="Expected Counter object to have value 2")

  def test_get_instance_no_prefix(self):
    with self.assertRaises(ValueError):
      factory.get_instance("Factory")

  def test_get_instance_no_such_module(self):
    with self.assertRaises(ImportError):
      factory.get_instance("nosuchmodule.NoSuchClass")

  def test_get_instance_no_such_class(self):
    with self.assertRaises(AttributeError):
      factory.get_instance(str(self.__module__) + ".NoSuchClass")

  def test_get_instance_non_zero_arity_constructor(self):
    with self.assertRaises(TypeError):
      factory.get_instance(str(self.__module__) + ".Value")


class FactoryConfigureTestCase(unittest.TestCase):

  def setUp(self):
    self.counter = Counter()
    self.config={"counter": 12345}
    (_, self.yaml) = tempfile.mkstemp(suffix=".yaml")
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write(yaml.dump(self.config, default_flow_style=False))
    self.env_var = "PROV_COUNTER"
    self.default_file = os.path.join(os.getcwd(), "test_factory_default.yaml")

  def tearDown(self):
    if self.yaml != None and os.path.isfile(self.yaml):
      os.remove(self.yaml)

  def test_configure_object_from_file(self):
    factory.configure_object(self.counter, 
                             self.env_var,
                             self.default_file,
                             self.yaml)
    self.assertEqual(12345, self.counter.get_counter())

  def test_configure_object_from_env(self):
    os.environ[self.env_var] = self.yaml
    factory.configure_object(self.counter, 
                             self.env_var,
                             self.default_file,
                             self.yaml)
    self.assertEqual(12345, self.counter.get_counter())

  def test_configure_object_from_default(self):
    shutil.move(self.yaml, self.default_file)
    self.yaml = self.default_file
    factory.configure_object(self.counter, 
                             self.env_var,
                             self.default_file)
    self.assertEqual(12345, self.counter.get_counter())

  def test_configure_object_from_file_missing_file(self):
    with self.assertRaises(IOError):
      factory.configure_object(self.counter, 
                               self.env_var,
                               self.default_file,
                               "nosuchfile.yaml")

  def test_configure_object_from_file_non_yaml_file(self):
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write("This is an invalid YAML file")
    with self.assertRaises(TypeError):
      factory.configure_object(self.counter, 
                               self.env_var,
                               self.default_file,
                               self.yaml)
