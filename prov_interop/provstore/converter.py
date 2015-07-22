"""Manages invocation of ProvStore service.
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

import json
import os.path
import requests

from prov_interop import http
from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.component import RestComponent
from prov_interop.converter import ConversionError
from prov_interop.converter import Converter
from prov_interop.provstore import service

class ProvStoreConverter(Converter, RestComponent):
  """Manages invocation of ProvStore service."""

  AUTHORIZATION = "authorization"
  """str or unicode: configuration key for ProvStore Authorization 
  HTTP header value
  """

  def __init__(self):
    """Create converter.
    """
    super(ProvStoreConverter, self).__init__()
    self._authorization = ""

  @property
  def authorization(self):
    """Get authorization header value.
    
    :returns: authoriation header
    :rtype: str or unicode
    """
    return self._authorization

  def configure(self, config):
   """Configure converter. ``config`` must hold entries::


        url: ...endpoint URL...
        authorization: ... ProvStore authorixation header...
        input-formats: [...list of formats from prov_interop.standards...]
        output-formats: [...list of formats from prov_interop.standards...]

    For example::

        url: https://provenance.ecs.soton.ac.uk/validator/provapi/documents/
        authorization: ApiKey user:12345qwerty
        input-formats: [provn, ttl, trig, provx, json]
        output-formats: [provn, ttl, trig, provx, json]

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
   super(ProvStoreConverter, self).configure(config)
   self.check_configuration([ProvStoreConverter.AUTHORIZATION])
   self._authorization = config[ProvStoreConverter.AUTHORIZATION]

  def convert(self, in_file, out_file):
    """Convert input file into output file. Each file must have an
    extension matching a format in
    ``prov_interop.standards``. Conversion is done in three stages:

    - Issue a POST request to deposit ``in_file`` into ProvStore.
    - Issue a GET request to request the document in the desired
      output format. This is saved into ``out_file``.
    - Issue a POST request to remove the document from ProvStore.

    :param in_file: Input file name
    :type in_file: str or unicode
    :param out_file: Output file name
    :type out_file: str or unicode
    :raises ConversionError: if the input file is not found, or the
    HTTP response is not 200
    :raises requests.exceptions.ConnectionError: if there are problems
    executing any of the requests e.g. the URL cannot be found
    """
    super(ProvStoreConverter, self).convert(in_file, out_file)
    in_format = os.path.splitext(in_file)[1][1:]
    out_format = os.path.splitext(out_file)[1][1:]
    super(ProvStoreConverter, self).check_formats(in_format, out_format)
    # Store document
    with open(in_file, "r") as f:
      doc = f.read()
    (response_status, response_text) = service.store(self._url,
                                                     in_file,
                                                     in_format,
                                                     doc,
                                                     self._authorization)
    if (response_status != requests.codes.created): # 201 CREATED
      raise ConversionError(self._url + " POST returned " + 
                            str(response_status))
    # Get document in desired format
    doc_url = service.get_stored_url(self._url, response_text)
    (response_status, response_text) = service.get(doc_url,
                                                   out_format)
    if (response_status != requests.codes.ok): # 200 OK
      raise ConversionError(doc_url + " GET returned " + 
                            str(response_status))
    with open(out_file, "w") as f:
      f.write(response_text)
    # Delete document
    (response_status, response_text) = service.delete(doc_url,
                                                      self._authorization)
    if (response_status != requests.codes.no_content): # 204 NO CONTENT
      raise ConversionError(doc_url + " DELETE returned " + 
                            str(response_status))
