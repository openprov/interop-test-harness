"""Interoperability tests for ProvTranslator.
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

from nose.tools import istest

from prov_interop.provtranslator.converter import ProvTranslatorConverter
from prov_interop.interop_tests.test_converter import ConverterTestCase

@istest
class ProvTranslatorTestCase(ConverterTestCase):
  """Interoperability tests for ProvTranslator.
  
  Its configuration, loaded via
  :meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.configure`,
  is expected to be in a YAML file: 
  
  - Either provided as the value of a ``ProvTranslator`` key in the
    :class:`prov_interop.harness.HarnessResource` configuration. 
  - Or, named in an environment variable, 
    ``PROVTRANSLATOR_TEST_CONFIGURATION``.
  - Or in ``localconfig/provtranslator.yaml``.

  The configuration itself, within this file, is expected to have the
  key `ProvTranslator``. 

  A valid YAML configuration file is::

    ---
    ProvTranslator:
      url: https://provenance.ecs.soton.ac.uk/validator/provapi/documents/
      input-formats: [provn, ttl, trig, provx, json]
      output-formats: [provn, ttl, trig, provx, json]
      skip-tests: []
  """

  CONFIGURATION_FILE_ENV = "PROVTRANSLATOR_TEST_CONFIGURATION"
  """str or unicode: environment variable holding configuration file name  
  """

  DEFAULT_CONFIGURATION_FILE="localconfig/provtranslator.yaml"
  """str or unicode: default configuration file name
  """

  CONFIGURATION_KEY="ProvTranslator"
  """str or unicode: key for ProvTranslator configuration in configuration
  file"""

  def setUp(self):
    super(ProvTranslatorTestCase, self).setUp()
    self.converter = ProvTranslatorConverter()
    super(ProvTranslatorTestCase, self).configure(
      ProvTranslatorTestCase.CONFIGURATION_KEY,
      ProvTranslatorTestCase.CONFIGURATION_FILE_ENV,
      ProvTranslatorTestCase.DEFAULT_CONFIGURATION_FILE)

  def tearDown(self):
    super(ProvTranslatorTestCase, self).tearDown()
