"""Interoperability tests for ProvScala ``provmanagement``.
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

from prov_interop.provman.converter import ProvManConverter
from prov_interop.interop_tests.test_converter import ConverterTestCase


@istest
class ProvManTestCase(ConverterTestCase):
    """Interoperability tests for ProvToolbox ``provmanagement``.

    Its configuration, loaded via
    :meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.configure`,
    is expected to be in a YAML file:

    - Either provided as the value of a ``ProvMan`` key in the
      :class:`prov_interop.harness.HarnessResource` configuration.
    - Or, named in an environment variable,
      ``PROVMAN_TEST_CONFIGURATION``.
    - Or in ``localconfig/provman.yaml``.

    The configuration itself, within this file, is expected to have the
    key `ProvMan``.

    A valid YAML configuration file is::

      ---
      ProvMan:
        executable: provmanagement
        arguments: translate --infile INPUT --outfile OUTPUT --inputFormat INFORMAT --outformat OUTFORMAT
        input-formats: [provn, ttl, trig, provx, json]
        output-formats: [provn, ttl, trig, provx, json]
        skip-tests: []
    """

    CONFIGURATION_FILE_ENV = "PROVMAN_TEST_CONFIGURATION"
    """str or unicode: environment variable holding configuration file name
    """

    DEFAULT_CONFIGURATION_FILE = "localconfig/provman.yaml"
    """str or unicode: default configuration file name
    """

    CONFIGURATION_KEY = "ProvMan"
    """str or unicode: key for ProvToolbox configuration in configuration
    file"""

    def setUp(self):
        super(ProvManTestCase, self).setUp()
        self.converter = ProvManConverter()
        super(ProvManTestCase, self).configure(
                ProvManTestCase.CONFIGURATION_KEY,
                ProvManTestCase.CONFIGURATION_FILE_ENV,
                ProvManTestCase.DEFAULT_CONFIGURATION_FILE)

    def tearDown(self):
        super(ProvManTestCase, self).tearDown()
