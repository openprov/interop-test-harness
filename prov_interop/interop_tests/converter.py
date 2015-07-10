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
from prov_interop.component import load_configuration
from prov_interop.converter import Converter
from prov_interop.interop_tests import harness

@nottest
def test_case_name(testcase_func, param_num, param):
  (index, ext_in, _, ext_out, _) =  param.args
  return "%s_%s" %(
    testcase_func.__name__,
    parameterized.to_safe_name(str(index) + "_" + ext_in + "_" + ext_out))

@nottest
class ConverterTestCase(unittest.TestCase):

  def setUp(self):
    super(ConverterTestCase, self).setUp()
    print(self.__class__.__name__)
    self.converter = None

  def configure(self, env_var, default_file_name):
    config_key = self.converter.__class__.__name__
    config_file_name = harness.harness_resources.configuration[config_key]
    # TODO check and raise error if missing
    config = load_configuration( 
      env_var,
      default_file_name,
      config_file_name)
    # TODO check and raise error if missing
    print(config)
    self.converter.configure(config[config_key])

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

  @parameterized.expand(harness.test_cases, testcase_func_name=test_case_name)
  def test_case(self, index, ext_in, file_ext_in, ext_out, file_ext_out):
    print("Test case: " + str(index) + " from " + ext_in + " to " + ext_out)
    if index in self.converter.configuration["skip-tests"]:
      self.skip_member_of_skip_set(index)
    if (not ext_in in self.converter.input_formats):
      self.skip_unsupported_format(index, ext_in, Converter.INPUT_FORMATS)
    if (not ext_out in self.converter.output_formats):
      self.skip_unsupported_format(index, ext_out, Converter.OUTPUT_FORMATS)
    converter_ext_out = "out." + ext_out
    self.converter.convert(file_ext_in, converter_ext_out)
    comparator = harness.harness_resources.format_comparators[ext_out]
    self.assertTrue(comparator.compare(file_ext_out, converter_ext_out), 
                    msg=ext_out + " file produced by converter did not match canonical " + file_ext_out)
