"""Test classes for ``prov_interop.files``.
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

from prov_interop.files import load_yaml
from prov_interop.files import YamlError

class FilesTestCase(unittest.TestCase):

  def setUp(self):
    super(FilesTestCase, self).setUp()
    self.config={"counter": 12345}
    (_, self.yaml) = tempfile.mkstemp(suffix=".yaml")
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write(yaml.dump(self.config, default_flow_style=False))
    self.env_var = "PROV_LOAD_CONFIG"
    self.default_file = os.path.join(os.getcwd(), "test_component.yaml")

  def tearDown(self):
    super(FilesTestCase, self).tearDown()
    if self.yaml != None and os.path.isfile(self.yaml):
      os.remove(self.yaml)
      
  def test_load_yaml_from_file(self):
    config = load_yaml(self.env_var,
                       self.default_file,
                       self.yaml)
    self.assertEqual(12345, config["counter"])

  def test_load_yaml_from_env(self):
    os.environ[self.env_var] = self.yaml
    config = load_yaml(self.env_var,
                       self.default_file,
                       self.yaml)
    self.assertEqual(12345, config["counter"])

  def test_load_yaml_from_default(self):
    shutil.move(self.yaml, self.default_file)
    self.yaml = self.default_file
    config = load_yaml(self.env_var,
                       self.default_file)
    self.assertEqual(12345, config["counter"])

  def test_load_yaml_from_file_missing_file(self):
    with self.assertRaises(IOError):
      config = load_yaml(self.env_var,
                         self.default_file,
                         "nosuchfile.yaml")
      
  def test_load_yaml_from_file_non_yaml_file(self):
    with open(self.yaml, 'w') as yaml_file:
      yaml_file.write("This is an invalid YAML file")
      with self.assertRaises(YamlError):
        config = load_yaml(self.env_var,
                           self.default_file,
                           self.yaml)
