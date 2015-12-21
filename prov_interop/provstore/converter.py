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
import os
import os.path
import requests

from prov_interop import http
from prov_interop import standards
from prov_interop.component import ConfigError
from prov_interop.component import RestComponent
from prov_interop.converter import ConversionError
from prov_interop.converter import Converter

class ProvStoreConverter(Converter, RestComponent):
  """Manages invocation of ProvStore service."""

  CONTENT_TYPES = {
    standards.PROVN: "text/provenance-notation",
    standards.TTL: "text/turtle",
    standards.TRIG: "application/trig",
    standards.PROVX: "application/xml",
    standards.JSON: "application/json"
  }
  """dict: mapping from :mod:`prov_service_tests.standards` formats to
  content types understood by ProvStore
  """

  CONTENT = "content"
  """str or unicode: key for request document content"""
  PUBLIC = "public"
  """str or unicode: key for request public flag"""
  REC_ID = "rec_id"
  """str or unicode: key for request document name"""
  ID = "id"
  """str or unicode: key for response document ID"""

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
    
    :return: authoriation header
    :rtype: str or unicode
    """
    return self._authorization

  def configure(self, config):
    """Configure converter. The configuration must hold:

    - :class:`prov_interop.converter.Converter` configuration
    - :class:`prov_interop.component.RestComponent` configuration
    - ``authorization``: value for ``Authorization`` HTTP header. For
      ProvStore, this is of form ``ApiKey USER:APIKEY`` where ``USER``
      is a ProvStore user name, and ``APIKEY`` is the user's ProvStore
      API key. 

    A valid configuration is::

      {
        "url": "https://provenance.ecs.soton.ac.uk/store/api/v0/documents/"
        "authorization": "ApiKey user:12345qwerty"
        "input-formats": ["provn", "ttl", "trig", "provx", "json"]
        "output-formats": ["provn", "ttl", "trig", "provx", "json"]
      }

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if `config` does not hold the above entries
    """
    super(ProvStoreConverter, self).configure(config)
    self.check_configuration([ProvStoreConverter.AUTHORIZATION])
    self._authorization = config[ProvStoreConverter.AUTHORIZATION]

  def convert(self, in_file, out_file):
    """Convert input file into output file. 

    - Input and output formats are derived from `in_file` and
      `out_file` file extensions. 
    - A check is done to see that `in_file` exists and that the input
      and output format are in `input-formats` and `output-formats`
      respectively. 
    - The input and output formats and ``authorization`` are used to
      set HTTP ``Content-type``, ``Accept`` and ``Authorization``
      header values, respectively.  
    - The contents of `in_file` are loaded and used to create a
      ProvStore compliant HTTP POST request which is submitted to
      ``url``, to store the document. 
    - The HTTP status is checked to be 201 CREATED.
    - The HTTP response is parsed to get the URL of the newly-stored
      document. 
    - The output format is used to set the HTTP ``Accept`` header
      value. 
    - An HTTP GET request is submitted to the URL of the new document
      to get it in the desired output format. 
    - The HTTP status is checked to to be 200 OK.
    - The HTTP response is parsed to get the converted document, and
      this is saved to `out_file`. 
    - An HTTP DELETE request is submitted to the URL of the
      newly-stored document to remove it. 
    - The HTTP status is checked to to be 204 NO CONTENT.


    :param in_file: Input file
    :type in_file: str or unicode
    :param out_file: Output file
    :type out_file: str or unicode
    :raises ConversionError: if the input file cannot be found, or the
      HTTP response is not 200
    :raises requests.exceptions.ConnectionError: if there are
      problems executing the request e.g. the URL cannot be found
    """
    super(ProvStoreConverter, self).convert(in_file, out_file)
    in_format = os.path.splitext(in_file)[1][1:]
    out_format = os.path.splitext(out_file)[1][1:]
    super(ProvStoreConverter, self).check_formats(in_format, out_format)
    # Store document
    with open(in_file, "r") as f:
      doc = f.read()
    content_type = ProvStoreConverter.CONTENT_TYPES[in_format]
    accept_type = ProvStoreConverter.CONTENT_TYPES[standards.JSON]
    headers = {http.CONTENT_TYPE: content_type, 
               http.ACCEPT: accept_type,
               http.AUTHORIZATION: self._authorization}
    store_request = {ProvStoreConverter.CONTENT: doc, 
                     ProvStoreConverter.PUBLIC: False,
                     ProvStoreConverter.REC_ID: str(os.getpid()) + "." + in_format}
    response = requests.post(self._url, 
                             headers=headers, 
                             data=json.dumps(store_request))
    if (response.status_code != requests.codes.created): # 201 CREATED
      raise ConversionError(self._url + " POST returned " + 
                            str(response.status_code))
    # Get document in desired format
    response_json = json.loads(response.text)
    document_id = response_json[ProvStoreConverter.ID]
    doc_url = self._url + str(document_id)
    accept_type = ProvStoreConverter.CONTENT_TYPES[out_format]
    headers = {http.ACCEPT: accept_type,
               http.AUTHORIZATION: self._authorization}
    response = requests.get(doc_url + "." + out_format, 
                            headers=headers, 
                            allow_redirects=True)
    if (response.status_code != requests.codes.ok): # 200 OK
      raise ConversionError(doc_url + " GET returned " + 
                            str(response.status_code))
    with open(out_file, "w") as f:
      f.write(response.text)
    # Delete document
    headers = {http.AUTHORIZATION: self._authorization}
    response = requests.delete(doc_url, headers=headers)
    if (response.status_code != requests.codes.no_content): # 204 NO CONTENT
      raise ConversionError(doc_url + " DELETE returned " + 
                            str(response.status_code))

