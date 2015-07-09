"""Interoperability tests for ProvPy prov-convert.
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
import re
import tempfile
import unittest

from nose_parameterized import parameterized
from nose.plugins.skip import Skip, SkipTest
from nose.tools import nottest
from nose.tools import istest

from prov.interop import standards
from prov.interop import component
from prov.interop.provpy.converter import ProvPyConverter
from prov.interop.provtoolbox.converter import ProvToolboxConverter
from interoperability.prov.interop import harness

@nottest
class InteroperabilityTestBase(unittest.TestCase):

  def setUp(self):
    super(InteroperabilityTestBase, self).setUp()
    print(self.__class__.__name__)
    self.converter = None

  def configure(self, converter, config_file_key, converter_key, 
                env_var, default_file_name):
    config_file_name = harness.harness_resources.configuration[config_file_key]
    # TODO check and raise error if missing
    config = component.load_configuration( 
      env_var,
      default_file_name,
      config_file_name)
    # TODO check and raise error if missing
    converter.configure(config[converter_key])

  @parameterized.expand(harness.get_test_cases())
  def test_case(self, test_case_index, test_case_name, dir_name):
    print("Test case name: " + test_case_name)
    if test_case_index in self.converter.configuration["skip-tests"]:
      print("Skipping")
      raise SkipTest("Test case " + str(test_case_index) +
                     " in " + self.converter.__class__.__name__ + 
                     " skip-tests")
    # Enumerate set of (ext_in, ext_out) pairs based on test_case formats.
    # Enumerate set of (ext_in, ext_out) pairs based on converter input and output formats.
    # FOR EACH (ext_in, ext_out) pair IN intersection of sets:
    ext_in = standards.JSON
    ext_out = standards.PROVX
    test_case_ext_in = os.path.join(dir_name, test_case_name + "." + ext_in)
    converters_ext_out = "out." + ext_out
    self.converter.convert(test_case_ext_in, converters_ext_out)
    comparator = harness.harness_resources.format_comparators[ext_out]
    test_case_ext_out = os.path.join(dir_name, test_case_name + "." + ext_out)
    # Record comparator result.
    self.assertTrue(comparator.compare(test_case_ext_out, converters_ext_out))

@istest
class ProvPyInteroperabilityTestCase(InteroperabilityTestBase):

  def setUp(self):
    # TODO initialise converter only once?
    super(ProvPyInteroperabilityTestCase, self).setUp()
    self.provpy = ProvPyConverter()
    super(ProvPyInteroperabilityTestCase, self).configure(
      self.provpy, 
      "ProvPy",
      "ProvPyConverter",
      "PROV_PROVPY_CONFIGURATION_FILE",
      "provpy-configuration.yaml")
    self.converter = self.provpy

  def tearDown(self):
    super(ProvPyInteroperabilityTestCase, self).tearDown()

@istest
class ProvToolboxInteroperabilityTestCase(InteroperabilityTestBase):

  def setUp(self):
    # TODO initialise converter only once?
    super(ProvToolboxInteroperabilityTestCase, self).setUp()
    self.provtoolbox = ProvToolboxConverter()
    super(ProvToolboxInteroperabilityTestCase, self).configure(
      self.provtoolbox, 
      "ProvToolbox",
      "ProvToolboxConverter",
      "PROV_PROVTOOLBOX_CONFIGURATION_FILE",
      "provtoolbox-configuration.yaml")
    self.converter = self.provtoolbox

  def tearDown(self):
    super(ProvToolboxInteroperabilityTestCase, self).tearDown()
