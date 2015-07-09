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

from prov_interop import standards
from prov_interop import component
from prov_interop.converter import Converter
from prov_interop.provpy.converter import ProvPyConverter
from prov_interop.provtoolbox.converter import ProvToolboxConverter
from interoperability.prov_interop import harness

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

  def skip_member_of_skip_set(self, index):
    print("Skipping as " + str(index) + " in skip-tests")
    raise SkipTest("Test case " + str(index) +
                   " in " + self.converter.__class__.__name__ + 
                   " skip-tests")

  def skip_unsupported_format(self, index, format, format_type):
      print("Skipping as " + format + " not in converter's " + format_type)
      raise SkipTest("Format " + format +
                     " not in " + self.converter.__class__.__name__ + 
                     " " + format_type)

  @parameterized.expand(harness.test_cases)
  def test_case(self, index, ext_in, file_ext_in, ext_out, file_ext_out):
    print("Test case: " + str(index))
    if index in self.converter.configuration["skip-tests"]:
      self.skip_member_of_skip_set(index)
    if (not ext_in in self.converter.input_formats):
      self.skip_unsupported_format(index, ext_in, Converter.INPUT_FORMATS)
    if (not ext_out in self.converter.output_formats):
      self.skip_unsupported_format(index, ext_out, Converter.OUTPUT_FORMATS)
    converter_ext_out = "out." + ext_out
    self.converter.convert(file_ext_in, converter_ext_out)
    comparator = harness.harness_resources.format_comparators[ext_out]
    self.assertTrue(comparator.compare(file_ext_out, converter_ext_out), msg="Did not match")

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
