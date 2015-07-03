"""Test classes for prov.interop.component classes.
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

from prov.interop.component import CommandLineComponent
from prov.interop.component import ConfigurableComponent
from prov.interop.component import ConfigError
from prov.interop.component import RestComponent

class ConfigurableComponentTestCase(unittest.TestCase):

  def test_configure(self):
    comp = ConfigurableComponent()
    comp.configure({})
    self.assertTrue(True)

  def test_configure_non_dict_error(self):
    comp = ConfigurableComponent()
    with self.assertRaises(ConfigError):
      comp.configure(123)


class CommandLineComponentTestCase(unittest.TestCase):

  def test_init(self):
    command_line = CommandLineComponent()
    self.assertEquals("", command_line.executable)
    self.assertEquals([], command_line.arguments)

  def test_configure(self):
    command_line = CommandLineComponent()
    command_line.configure(
      {CommandLineComponent.EXECUTABLE: "b", 
       CommandLineComponent.ARGUMENTS: ["c", 1]})
    self.assertEquals("b", command_line.executable)
    self.assertEquals(["c", 1], command_line.arguments)

  def test_configure_non_dict_error(self):
    command_line = CommandLineComponent()
    with self.assertRaises(ConfigError):
      command_line.configure(123)

  def test_configure_no_executable(self):
    command_line = CommandLineComponent()
    with self.assertRaises(ConfigError):
      command_line.configure({CommandLineComponent.ARGUMENTS: ["c", 1]})

  def test_configure_no_arguments(self):
    command_line = CommandLineComponent()
    with self.assertRaises(ConfigError):
      command_line.configure({CommandLineComponent.EXECUTABLE: "b"})


class RestComponentTestCase(unittest.TestCase):

  def test_init(self):
    rest = RestComponent()
    self.assertEquals("", rest.url)

  def test_configure(self):
    rest = RestComponent()
    rest.configure({RestComponent.URL: "a"})
    self.assertEquals("a", rest.url)

  def test_configure_non_dict_error(self):
    rest = RestComponent()
    with self.assertRaises(ConfigError):
      rest.configure(123)

  def test_configure_no_url(self):
    rest = RestComponent()
    with self.assertRaises(ConfigError):
      rest.configure({})
