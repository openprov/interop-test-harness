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

import json
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
    standards.JSON: "application/json"}
  """list of string or unicode: list of mapping from formats in
  ``prov_interop.standards`` to content types understood by the
  service.
  """

  AUTHORIZATION = "authorization"
  """string or unicode: configuration key for ProvStore Authorization 
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
   """Configure converter.
    ``config`` is expected to hold configuration of form::

        url: ...endpoint URL...
        authorization: ... ProvStore authorixation header...
        input-formats: [...list of formats...]
        output-formats: [...list of formats...]

    For example::

        url: https://provenance.ecs.soton.ac.uk/validator/provapi/documents/
        authorization: ApiKey user:12345qwerty
        input-formats: [provn, ttl, trig, provx, json]
        output-formats: [provn, ttl, trig, provx, json]

    Input and output formats must be as defined in
    ``prov_interop.standards``.

    :param config: Configuration
    :type config: dict
    :raises ConfigError: if ``config`` does not hold the above entries
    """
   super(ProvStoreConverter, self).configure(config)
   ProvStoreConverter.check_configuration(config,
                                          [ProvStoreConverter.AUTHORIZATION])
   self._authorization = config[ProvStoreConverter.AUTHORIZATION]

  def convert(self, in_file, out_file):
    """Use ProvStore to convert an input file into an output
    file. Each file must have an extension matching one of those
    in ``prov_interop.standards``. This consists of 3 stages:

    - Issue a POST request to deposit ``in_file`` into ProvStore.
    - Issue a GET request to request the document in the desired
      output format. This is saved into ``out_file``.
    - Issue a POST request to remove the document from ProvStore.

    ``in_file`` and ``out_file`` file extensions are mapped to 
    content and accept types using ``CONTENT_TYPES``.

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
    with open(in_file, "r") as f:
      doc = f.read()
    # Prepare ProvStore request, including doc.
    store_request={"content": doc,
                   "public": True,
                   "rec_id": in_file} # Use file name as ID.
    # Map prov_interop.standards formats to Content-Type supported by 
    # ProvStore. 
    content_type = ProvStoreConverter.CONTENT_TYPES[in_format]
    # Request ProvStore response be JSON from which auto-generated
    # document identifier will be extracted
    accept_type = ProvStoreConverter.CONTENT_TYPES[standards.JSON]
    headers = {http.CONTENT_TYPE: content_type, 
               http.ACCEPT: accept_type,
               http.AUTHORIZATION: self._authorization}
    response = requests.post(self._url, 
                             headers=headers, 
                             data=json.dumps(store_request))
    if (response.status_code != requests.codes.created): # 201 CREATED
      raise ConversionError(self._url + " POST returned " + 
                            str(response.status_code))
    store_meta_data = json.loads(response.text)
    doc_id = store_meta_data["id"]
    doc_url = self._url + str(doc_id)
    # Map prov_interop.standards formats to Accept-Type supported by 
    # ProvStore. 
    accept_type = ProvStoreConverter.CONTENT_TYPES[out_format]
    headers = {http.ACCEPT: accept_type}
    response = requests.get(doc_url + "." + out_format, 
                            headers=headers, 
                            allow_redirects=True)
    if (response.status_code != requests.codes.ok): # 200 OK
      raise ConversionError(self._url + " GET returned " + 
                            str(response.status_code))
    with open(out_file, "w") as f:
      f.write(response.text)
    headers = {http.AUTHORIZATION: self._authorization}
    response = requests.delete(doc_url, headers=headers)
    if (response.status_code != requests.codes.no_content): # 204 NO CONTENT
      raise ConversionError(doc_url + " DELETE returned " + 
                            str(response.status_code))
