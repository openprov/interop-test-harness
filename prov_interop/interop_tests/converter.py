"""Base class for converter interoperability tests.
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
  """``nose_parameterized`` callback function to create custom
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
  """str or unicode: configuration key for tests to skip"""

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
    """Raise a SkipTest error if this test case is to be skipped 
    for this converter.

    :param index: Test case index
    :type index: int
    :raises SkipTest:
    """
    print("Skipping as " + str(index) + " in skip-tests")
    raise SkipTest("Test case " + str(index) +
                   " in " + self.converter.__class__.__name__ + 
                   " skip-tests")

  def skip_unsupported_format(self, index, format, format_type):
    """Raise a SkipTest error if a specific conversion is to be
    skipped because the converter does not support one of the
    formats. 

    :param index: Test case index
    :type index: int
    :param format: one of the formats in ``prov_interop.standards``
    :type format: str or unicode
    :param format_type: Converter configuration key indicating 
    which format is not supported (e.g. "input-format" or
    "output-format"
    :type format_type: str or unicode
    :raises SkipTest:
    """
    print("Skipping as " + str(index) + " in skip-tests")
    print("Skipping as " + format + " not in converter's " + format_type)
    raise SkipTest("Format " + format +
                   " not in " + self.converter.__class__.__name__ + 
                   " " + format_type)

  @parameterized.expand(harness.harness_resources.test_cases, 
                        testcase_func_name=test_case_name)
  def test_case(self, index, ext_in, file_ext_in, ext_out, file_ext_out):
    """Test converter's conversion of a file in one format to another
    format. 

    The comparator registered for the output format is used to
    compare the file output by the converter to the given output file,
    which is assumed to be semantically equivalent to the input
    file. The test succeeds if the comparator deems the converter's
    output file to be semantially equivalent to the given output file.
    
    If the test case index is recorded as one of those to be skipped
    for the converter, or if the input or output formats are not
    supported by the converter, then the test is skipped.

    :param index: Test case index
    :type index: int
    :param ext_in: input format, one of the formats in
    ``prov_interop.standards``
    :type ext_in: str or unicode
    :param file_ext_in: input file path, assumed to be of format
    ``ext_in`` 
    :type file_ext_in: str or unicode
    :param ext_out: output format, one of the formats in
    ``prov_interop.standards`` 
    :type ext_out: str or unicode
    :param file_ext_out: output file path, assumed to be of format
    ``ext_out`` 
    :type file_ext_out: str or unicode
    :param format_type: Converter configuration key indicating 
    which format is not supported (e.g. "input-format" or
    "output-format"
    :type format_type: str or unicode
    :raises SkipTest: if the test case is to be skipped, or the input
    format or output format are not supported by the converter.
    """
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
    are_equivalent = comparator.compare(file_ext_out, self.converter_ext_out)
    msg = ""
    if not are_equivalent:
      with open(self.converter_ext_out) as f: 
        expected = f.read()
      with open(file_ext_out) as f: 
        actual = f.read()
      msg = "Comparison failure for converted file " + ext_out + \
          "\nCanonical file " + file_ext_out + ":\n" + expected + \
          "\nConverted file:\n:" + actual
    self.assertTrue(are_equivalent, msg=msg)
