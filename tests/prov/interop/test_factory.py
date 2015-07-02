"""Test classes for prov.interop.converter classes.
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

import unittest

from prov.interop.factory import FactoryUtilities

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


class Value:
  """Dummy class for testing FactoryUtilities."""

  def __init__(self, value):
    """Store value.

    :param value:
    :type name: int
    """
    self._value = value


class FactoryUtilitiesTestCase(unittest.TestCase):

  def test_get_class(self):
    my_module = self.__module__
    clazz = FactoryUtilities.get_class(str(self.__module__) + ".Counter")
    self.assertEquals(Counter, clazz, msg="Expected Counter class")

  def test_get_class_no_prefix(self):
    with self.assertRaises(ValueError):
      FactoryUtilities.get_class("Counter")

  def test_get_class_no_such_module(self):
    with self.assertRaises(ImportError):
      FactoryUtilities.get_class("nosuchmodule.NoSuchClass")

  def test_get_class_no_such_class(self):
    with self.assertRaises(AttributeError):
      FactoryUtilities.get_class(str(self.__module__) + ".NoSuchClass")

  def test_get_instance(self):
    my_module = self.__module__
    obj = FactoryUtilities.get_instance(str(self.__module__) + ".Counter")
    self.assertIsInstance(obj, Counter, msg="Expected Counter object")
    obj.increment()
    obj.increment()
    self.assertEquals(2, obj.get_counter(), msg="Expected Counter object to have value 2")

  def test_get_instance_no_prefix(self):
    with self.assertRaises(ValueError):
      FactoryUtilities.get_instance("Factory")

  def test_get_instance_no_such_module(self):
    with self.assertRaises(ImportError):
      FactoryUtilities.get_instance("nosuchmodule.NoSuchClass")

  def test_get_instance_no_such_class(self):
    with self.assertRaises(AttributeError):
      FactoryUtilities.get_instance(str(self.__module__) + ".NoSuchClass")

  def test_get_instance_non_zero_arity_constructor(self):
    with self.assertRaises(TypeError):
      FactoryUtilities.get_instance(str(self.__module__) + ".Value")
