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
from nose.tools import istest
from nose.tools import nottest

from prov_interop import standards
from prov_interop.component import load_configuration
from prov_interop.component import ConfigError
from prov_interop.converter import Converter
from prov_interop.interop_tests import harness

@nottest
def test_case_name(testcase_func, param_num, param):
  """
  ``nose_parameterized`` callback function to create custom
  test function names.

  :param testcase__func: test function
  :type testcase__func: function
  :param param_num: number of parameters in ``param``
  :type param_num: int
  :param param: tuple of arguments to test function
  :type param: tuple, assumed to be of form (int, str or unicode, _,
  str or unicode, )
  :returns: test functionname of form N_EXTIN_EXTOUT (e.g. 
  ``test_case_1_provx_json``)
  :rtype: str or unicode
  """
  (index, ext_in, _, ext_out, _) =  param.args
  return "%s_%s" %(
    testcase_func.__name__,
    parameterized.to_safe_name(str(index) + "_" + ext_in + "_" + ext_out))


@nottest
class ConverterTestCase(unittest.TestCase):

  SKIP_TESTS = "skip-tests"
  """string or unicode: configuration key for tests to skip"""

  def setUp(self):
    super(ConverterTestCase, self).setUp()
    self.converter = None
    self.skip_tests = []
    self.converter_ext_out = None

  def tearDown(self):
    super(ConverterTestCase, self).tearDown()
    if self.converter_ext_out != None and \
          os.path.isfile(self.converter_ext_out):
      os.remove(self.converter_ext_out)

  def configure(self, env_var, default_file_name):
    """Configure converter to be tested. 
    - This assumes :class:`~prov_interop.harness.HarnessResources` has
      been initialised by ``prov_interop.interop_tests.harness``.
    - This assumes ``self.converter`` has been assigned to a sub-class
      of ``:class:`~prov_interop.converter.Converter`.
      - If harness configuration has key matching the converter's
      class name, then its value is assumed to be a configuration
      file for the converter.
    - Else, if an environment variable with the name in
      ``env_var`` is defined, then this environment variable is assumed
       to hold a configuration file for the converter.
    - Else ``default_file_name`` is used as a configuration file.
    - The configuration file is assumed to be a YAML file, with 
      an entry keyed using the class name of the converter
      (e.g. ProvPyConverter) 
    - The configuration file is loaded and the values under the
      converter's key used to configure the converter.

    :param env_var: Environment variable with configuration file name
    :type env_var: str or unicode
    :param default_file_name: Default configuration file name
    :type file_name: str or unicode
    :raises IOError: if the file is not found
    :raises ConfigError: if the configuration file does not parse
    into a dict, if there is no entry with the converter's class
    name within the configuration, or if converter-specific
    configuration information is missing.
    """
    config_key = self.converter.__class__.__name__
    config_file_name = None
    if config_key in harness.harness_resources.configuration:
      config_file_name = harness.harness_resources.configuration[config_key]
    config = load_configuration( 
      env_var,
      default_file_name,
      config_file_name)
    if config_key not in config:
      raise ConfigError("Missing configuration for " + config_key)
    self.converter.configure(config[config_key])
    if ConverterTestCase.SKIP_TESTS in self.converter.configuration:
      self.skip_tests = self.converter.configuration[
        ConverterTestCase.SKIP_TESTS]

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
    if index in self.skip_tests:
      self.skip_member_of_skip_set(index)
    if (not ext_in in self.converter.input_formats):
      self.skip_unsupported_format(index, ext_in, Converter.INPUT_FORMATS)
    if (not ext_out in self.converter.output_formats):
      self.skip_unsupported_format(index, ext_out, Converter.OUTPUT_FORMATS)
    self.converter_ext_out = "out." + ext_out
    self.converter.convert(file_ext_in, self.converter_ext_out)
    comparator = harness.harness_resources.format_comparators[ext_out]
    self.assertTrue(comparator.compare(file_ext_out, self.converter_ext_out), 
                    msg=ext_out + 
                    " file produced by converter did not match " + 
                    file_ext_out)
