"""Base class for converter interoperability tests.

The test harness is initialised by a call to
:func:`prov_interop.interop_tests.harness.initialise_harness_from_file`. This 
is done within
:meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.initialise_test_harness`
which provides tuples to :mod:`nose_parameterized` when it
dynamically creates the test methods (see
:meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.test_case`).
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

import inspect
import os
import re
import sys
import tempfile
import unittest

from nose_parameterized import parameterized
from nose.plugins.skip import SkipTest
from nose.tools import istest
from nose.tools import nottest

from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.converter import Converter
from prov_interop.files import load_yaml
from prov_interop.harness import HarnessResources
from prov_interop.interop_tests import harness

@nottest
def test_case_name(testcase_func, param_num, param):
  """:mod:`nose_parameterized` callback function to create custom 
  test function names.

  This overrides the default method names created by
  :mod:`nose_parameterized`.

  :param testcase_func: test function
  :type testcase_func: function
  :param param_num: number of parameters in `param`
  :type param_num: int
  :param param: tuple of arguments to test function
  :type param: tuple of form (int, str or unicode, _, str or unicode,
    _) 
  :return: test function name of form ``N_EXTIN_EXTOUT`` (e.g. 
    ``test_case_1_provx_json``)
  :rtype: str or unicode
  """
  (index, ext_in, _, ext_out, _) =  param.args
  return str("%s_%s" %(
    testcase_func.__name__,
    parameterized.to_safe_name(str(index) + "_" + ext_in + "_" + ext_out)))

@nottest
class ConverterTestCase(unittest.TestCase):
  """Base class for converter interoperability tests.

  This class implements the procedure for testing a converter using a
  test case and a comparator: 
  
  - A converter translates ``testcaseNNNN/file.<ext_in>`` to 
    ``converted.<ext_out>``.
  - A comparator compares ``testcaseNNNN/file.<ext_out>`` to 
    ``converted.<ext_out>`` for equivalence, which results in either
    success or failure. 

  This class is sub-classed by test classes for each converter.
  """

  SKIP_TESTS = "skip-tests"
  """str or unicode: configuration key for tests to skip"""

  _multiprocess_can_split_ = True

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

  def shortDescription(self):
    """Suppress use of docstring by nose when printing tests being run"""
    return None

  def configure_converter(self, config):
    """Configure a converter using the given configuration.

    The method assumes the converter has been created and stored in an
    instance variable.

    The given configuration is used to configure the converter via its
    :meth:`prov_interop.converter.Converter.configure` method.

    In addition to converter-specific configuration, this
    configuration can also hold:

    - ``skip-tests``: a list of the indices of zero or more tests that
      are to be skipped for this converter. 

    If so, then this list is cached in an instance variable.

    An example configuration, in the form of a Python dictionary, and
    for ProvPy ``prov-convert``, is::

    {
        "executable": "prov-convert"
        "arguments": "-f FORMAT INPUT OUTPUT"
        "input-formats": ["json"]
        "output-formats": ["provn", "provx", "json"]
        "skip-tests": [2, 3, 5]
    }

    :param config: Converter-specific configuration
    :type config_key: dict
    :raises ConfigError: if there is no entry with value `config_key`
      within the configuration, or if converter-specific
      configuration information is missing
    """
    self.converter.configure(config)
    if ConverterTestCase.SKIP_TESTS in self.converter.configuration:
      self.skip_tests = self.converter.configuration[
        ConverterTestCase.SKIP_TESTS]

  def configure(self, config_key, env_var, default_file_name):
    """Get the configuration for the converter to be tested within a
    sub-class. 

    The method assumes the converter has been created and stored in an
    instance variable. It loads the contents of a YAML file (using
    :func:`prov_interop.files.load_yaml`) into a Python
    dictionary. The file loaded is: 

    - The value of an entry in
      :class:`prov_interop.harness.HarnessResources` configuration with
      name `config_key`, if any. 
    - Else, the file named in the environment variable named in
      `env_var`, if such an environment variable has been defined. 
    - Else, `default_file_name`.

    Once loaded, a dictionary entry with whose key is the value of
    `config_key` is extracted and used to configure the converter via
    :meth:`configure_converter`.

    An example configuration, in the form of a Python dictionary, and
    for ProvPy ``prov-convert``, is::

      {
        "ProvPy": {
          "executable": "prov-convert"
          "arguments": "-f FORMAT INPUT OUTPUT"
          "input-formats": ["json"]
          "output-formats": ["provn", "provx", "json"]
          skip-tests: [2, 3, 5]
        }
      }

    The corresponding YAML configuration file is::

      ---
      ProvPy: 
        executable: prov-convert
        arguments: -f FORMAT INPUT OUTPUT
        input-formats: [json]
        output-formats: [provn, provx, json]
        skip-tests: [2, 3, 5]

    :param config_key: Key to access converter-specific configuration
    :type config_key: str or unicode
    :param env_var: Environment variable with configuration file name
    :type env_var: str or unicode
    :param default_file_name: Default configuration file name
    :type file_name: str or unicode
    :raises IOError: if the file is not found
    :raises ConfigError: if there is no entry with value `config_key`
      within the configuration, or if converter-specific
      configuration information is missing
    :raises YamlError: if the file is an invalid YAML file
    """
    config_file_name = None
    if config_key in harness.harness_resources.configuration:
      config_file_name = harness.harness_resources.configuration[config_key]
    config = load_yaml(env_var,
                       default_file_name,
                       config_file_name)
    if config_key not in config:
      raise ConfigError("Missing configuration for " + config_key)
    self.configure_converter(config[config_key])

  def skip_member_of_skip_set(self, index):
    """Raise a :class:`nose.plugins.skip.SkipTest` if this test
    case is marked as to be skipped for the converter. Tests to be
    skipped are recorded in the optional ``skip-tests``
    configuration. 

    :param index: Test case index
    :type index: int
    :raises nose.plugins.skip.SkipTest: always
    """
    print(("Skipping as " + str(index) + " in skip-tests"))
    raise SkipTest(("Test case " + str(index) +
                    " in " + self.converter.__class__.__name__ + 
                    " skip-tests"))

  def skip_unsupported_format(self, index, format, format_type):
    """Raise a :class:`nose.plugins.skip.SkipTest` if a specific
    conversion is to be skipped because the converter does not support
    one of the formats. 

    :param index: Test case index
    :type index: int
    :param format: one of the formats in :mod:`prov_interop.standards`
    :type format: str or unicode
    :param format_type: Converter configuration key indicating 
      which format is not supported (e.g. ``input-format`` or
      ``output-format``
    :type format_type: str or unicode
    :raises nose.plugins.skip.SkipTest: always
    """
    print(("Skipping as " + str(index) + " in skip-tests"))
    print(("Skipping as " + format + " not in converter's " + format_type))
    raise SkipTest(("Format " + format +
                    " not in " + self.converter.__class__.__name__ + 
                    " " + format_type))

  @nottest
  def initialise_test_harness():
    """Initialises the test harness and provide the test cases as a
    generator. 

    The test harness is bootstrapped by a call to
    :func:`prov_interop.interop_tests.harness.initialise_harness_from_file`. 
    This method provides test case tuples by returning the generator,
    :meth:`prov_interop.harness.HarnessResources.test_cases_generator`,
    so that :mod:`nose_parameterized` can dynamically creates the test
    methods (see
    :meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.test_case`).

    If running Sphinx to create API documentation then the test
    harness initialisation is not done and, instead, a generator 
    that contains zero test cases is returned. This is a hack to
    workaround Sphinx's execution of the Python it parses.

    :returns: test case tuple
    :rtype: tuple of (int, str or unicode, str or unicode, str or
      unicode, str or unicode) 
    :raises ConfigError: if the test cases directory is not found
    """
    if "sphinx-build" in sys.argv[0]:
      return (nothing for nothing in ())
    else:
      harness.initialise_harness_from_file()
      return harness.harness_resources.test_cases_generator()

  @parameterized.expand(initialise_test_harness(), 
                        testcase_func_name=test_case_name)
  def test_case(self, index, ext_in, file_ext_in, ext_out, file_ext_out):
    """Test a converter's conversion of a file in one format to
    another format. 

    This generic test method implements the following test procedure: 

    - If the test case `index` is in the optional ``skip-tests``
      configuration for the converter then the test is skipped, by
      raising :class:`nose.plugins.skip.SkipTest`. 
    - If `ext_in` or `ext_out` are not in the ``input-formats`` or
      ``output-formats`` for the converter then the test is skipped,
      again by raising :class:`nose.plugins.skip.SkipTest`. 
    - The converter translates ``testcaseNNNN/file_ext_in`` to 
      ``out.ext_out``.
    - The comparator for `ext_out` registered with
      :class:`prov_interop.harness.HarnessResources` is retrieved. 
    - The comparator compares ``testcaseNNNN/file.ext_out`` to 
      ``out.ext_out`` for equivalence, which results in either success
      or failure. 

    :mod:`nose_parameterized`, in conjunction with the test case
    tuples provided via the generator,
    :meth:`prov_interop.harness.HarnessResources.test_cases_generator`,
    is used to dynamically create test methods for each test case
    tuple. When this class is loaded, :mod:`nose_parameterized`
    will iterate through each of the test cases and create
    corresponding test methods::

      test_case_1_json_json
      test_case_1_provx_json
      test_case_1_json_provx
      test_case_1_provx_provx
      ...

    The arguments passed into each test method, `(index, ext_in,
    file_ext_in, ext_out, file_ext_out)` are those from the tuple that
    was used to create that method.  

    :param index: Test case index
    :type index: int
    :param ext_in: input format, one of the formats in
      :mod:`prov_interop.standards`
    :type ext_in: str or unicode
    :param file_ext_in: input file, assumed to have extension `ext_in`
    :type file_ext_in: str or unicode
    :param ext_out: output format, one of the formats in
      :mod:`prov_interop.standards`
    :type ext_out: str or unicode
    :param file_ext_out: output file, assumed to have extension `ext_out`
    :type file_ext_out: str or unicode
    :raises nose.plugins.skip.SkipTest: if the test case is to be
      skipped, or the input format or output format are not supported
      by the converter
    """
    print(("Test case: " + str(index) + 
          " from " + ext_in + 
          " to " + ext_out + " Process: " + str(os.getpid())))
    if index in self.skip_tests:
      self.skip_member_of_skip_set(index)
    if (not ext_in in self.converter.input_formats):
      self.skip_unsupported_format(index, ext_in, Converter.INPUT_FORMATS)
    if (not ext_out in self.converter.output_formats):
      self.skip_unsupported_format(index, ext_out, Converter.OUTPUT_FORMATS)
    self.converter_ext_out = "out." + str(os.getpid()) + "." + ext_out
    self.converter.convert(file_ext_in, self.converter_ext_out)
    comparator = harness.harness_resources.format_comparators[ext_out]
    are_equivalent = comparator.compare(file_ext_out, self.converter_ext_out)
    self.assertTrue(are_equivalent, \
      msg="Test failed: " + file_ext_out + 
          " does not match " + self.converter_ext_out + 
	  " converted from " + file_ext_in)
