"""ProvTranslator service constants and functions.
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

import requests

from prov_interop import http
from prov_interop import standards

CONTENT_TYPES = {
  standards.PROVN: "text/provenance-notation",
  standards.TTL: "text/turtle",
  standards.TRIG: "application/trig",
  standards.PROVX: "application/provenance+xml",
  standards.JSON: "application/json"}
"""list of str or unicode: list of mapping from formats in
``prov_interop.standards`` to content types understood by the
service.
"""

def translate(url, in_format, out_format, document):
  """Use ProvTranslator to convert a document from one format
  to another. Each format must be as defined in
  ``prov_interop.standards``.
  
  :param url: ProvTranslate URL
  :type url: str or unicode
  :param in_format: Input format
  :type in_format: str or unicode
  :param out_format: Input format
  :type out_format: str or unicode
  :param document: Document
  :type document: str or unicode
  :returns: resoponse status code and response text
  :rtype: tuple (int, str or unicode)
  :raises requests.exceptions.ConnectionError: if there are
  problems executing the request e.g. the URL cannot be found
  """
  content_type = CONTENT_TYPES[in_format]
  accept_type = CONTENT_TYPES[out_format]
  headers = {http.CONTENT_TYPE: content_type, 
             http.ACCEPT: accept_type}
  response = requests.post(url, 
                           headers=headers, 
                           data=document)
  return (response.status_code, response.text)
