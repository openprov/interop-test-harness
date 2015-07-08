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

import prov.interop.standards
import prov.interop.component as component
import interoperability.prov.interop.harness as harness

from prov.interop.provpy.converter import ProvPyConverter
from prov.interop.harness import HarnessResources


from prov.interop.provtoolbox.converter import ProvToolboxConverter

class InteroperabilityTestCase(unittest.TestCase):

  def setUp(self):
    super(InteroperabilityTestCase, self).setUp()
    os.environ[harness.CONFIGURATION_FILE] = "localconfig/harness-configuration.yaml"
    harness.initialise_harness_from_file()

  def configure(self, obj, file_key, config_key, env_var, default_file_name):
    config_file = harness.harness_resources.configuration[file_key]
    # TODO check and raise error if missing
    config = component.load_configuration( 
      env_var,
      default_file_name,
      config_file)
    # TODO check and raise error if missing
    obj.configure(config[config_key])

  def run_case1(self, converter):
    test_cases = harness.harness_resources.configuration["test-cases"]
    test_case = os.path.join(test_cases, "testcase1")
    test_case_json = os.path.join(test_case, "testcase1.json")
    converter.convert(test_case_json, "outyyy.provx")
    comparator = harness.harness_resources.format_comparators["provx"]
    test_case_provx = os.path.join(test_case, "testcase1.provx")
    self.assertTrue(comparator.compare(test_case_provx, "outyyy.provx"))

  def run_interoperability(self, specification, comparators):
    pass
#    specification is a converter specification.
#    comparators is a dictionary of Comparators indexed by format.
#    Use specification to create and configure the Converter.
#    FOR EACH test_case NOT IN skip-tests:
#      Enumerate set of (ext_in, ext_out) pairs based on test_case formats.
#      Enumerate set of (ext_in, ext_out) pairs based on converter input and output formats.
#      FOR EACH (ext_in, ext_out) pair IN intersection of sets:
#        convertor.convert(test_case.ext_in, ext_in, converted.ext_out, ext_out).
#        Get comparator for ext_out from comparators
#        comparator.compare(test_case.ext_out, ext_out, converted.ext_out, ext_out)
#        Record comparator result.

class ProvPyInteroperabilityTestCase(InteroperabilityTestCase):

  def setUp(self):
    # Initialize only once too!
    super(ProvPyInteroperabilityTestCase, self).setUp()
    self.provpy = ProvPyConverter()
    super(ProvPyInteroperabilityTestCase, self).configure(
      self.provpy, 
      "ProvPy",
      "ProvPyConverter",
      "PROV_PROVPY_CONFIGURATION_FILE",
      "provpy-configuration.yaml")

  def tearDown(self):
    super(ProvPyInteroperabilityTestCase, self).tearDown()

  def test_case1(self):
    super(ProvPyInteroperabilityTestCase, self).run_case1(self.provpy)
#    test_cases = harness.harness_resources.configuration["test-cases"]
#    test_case = os.path.join(test_cases, "testcase1")
#    test_case_json = os.path.join(test_case, "testcase1.json")
#    self.provpy.convert(test_case_json, "out.provx")
#    comparator = harness.harness_resources.format_comparators["provx"]
#    test_case_provx = os.path.join(test_case, "testcase1.provx")
#    self.assertTrue(comparator.compare(test_case_provx, "out.provx"))

class ProvToolboxInteroperabilityTestCase(InteroperabilityTestCase):

  def setUp(self):
    super(ProvToolboxInteroperabilityTestCase, self).setUp()
    self.provtoolbox = ProvToolboxConverter()
    super(ProvToolboxInteroperabilityTestCase, self).configure(
      self.provtoolbox, 
      "ProvToolbox",
      "ProvToolboxConverter",
      "PROV_PROVTOOLBOX_CONFIGURATION_FILE",
      "provtoolbox-configuration.yaml")

  def tearDown(self):
    super(ProvToolboxInteroperabilityTestCase, self).tearDown()

  def test_case1(self):
    super(ProvToolboxInteroperabilityTestCase, self).run_case1(self.provtoolbox)
#    test_cases = harness.harness_resources.configuration["test-cases"]
#    test_case = os.path.join(test_cases, "testcase1")
#    test_case_json = os.path.join(test_case, "testcase1.json")
#    self.provtoolbox.convert(test_case_json, "outyyy.provx")
#    comparator = harness.harness_resources.format_comparators["provx"]
#    test_case_provx = os.path.join(test_case, "testcase1.provx")
#    self.assertTrue(comparator.compare(test_case_provx, "outyyy.provx"))
