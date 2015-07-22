"""ProvStore service constants and functions.
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
import requests

from prov_interop import http
from prov_interop import standards

CONTENT_TYPES = {
  standards.PROVN: "text/provenance-notation",
  standards.TTL: "text/turtle",
  standards.TRIG: "application/trig",
  standards.PROVX: "application/xml",
  standards.JSON: "application/json"}
"""list of str or unicode: list of mapping from formats in
``prov_interop.standards`` to content types understood by the
service.
"""

CONTENT = "content"
"""str or unicode: key for ProvStore request document content"""
PUBLIC = "public"
"""str or unicode: key for ProvStore request public flag"""
REC_ID = "rec_id"
"""str or unicode: key for ProvStore request document name"""
ID = "id"
"""str or unicode: key for ProvStore response document ID"""

def create_store_request(name, document, is_public=True):
  """Create a ProvStore-compliant request, wrapping up a PROV document.
  
  :param name: Name or ID for the document
  :type name: str or unicode
  :param document: Document
  :type document: str or unicode
  :param is_public: Is document to be publicly visible?
  :type is_public: bool
  :returns: store request document
  :rtype: JSON-compliant dict
  """
  return {CONTENT: document, PUBLIC: is_public, REC_ID: name}

def store(url, name, format, document, authorization, is_public=True):
  """Store a document of the given format in ProvStore. The format
  must be as defined in ``prov_interop.standards``. The "Accept" type
  is set to JSON.
  
  :param url: ProvStore URL
  :type url: str or unicode
  :param name: Name or ID for the document
  :type name: str or unicode
  :param format: Document format
  :type format: str or unicode
  :param document: Document
  :type document: str or unicode
  :param authorization: Authorization token (API key)
  :type authorization: str or unicode
  :param is_public: Is document to be publicly visible?
  :type is_public: bool
  :returns: response status code and response text
  :rtype: tuple (int, str or unicode)
  :raises requests.exceptions.ConnectionError: if there are
  problems executing the request e.g. the URL cannot be found
  """
  content_type = CONTENT_TYPES[format]
  accept_type = CONTENT_TYPES[standards.JSON]
  headers = {http.CONTENT_TYPE: content_type, 
             http.ACCEPT: accept_type,
             http.AUTHORIZATION: authorization}
  store_request = create_store_request(name, document, is_public)
  response = requests.post(url, 
                           headers=headers, 
                           data=json.dumps(store_request))
  return (response.status_code, response.text)

def get_stored_url(url, response):
  """Given the response text from a successful call to ``store``,
  extract the document ID and create the document URL.

  :param url: ProvStore URL
  :type url: str or unicode
  :param response: ProvStore response to a successful storing 
  of a document, assumed to be parsable into JSON
  :type response: str or unicode
  :returns: document URL
  :rtype: str or unicode
  """
  response_json = json.loads(response)
  document_id = response_json[ID]
  document_url = url + str(document_id)
  return document_url

def get(url, format, authorization=""):
  """Get a document in the given format from ProvStore. The format
  must be as defined in ``prov_interop.standards``.
  
  :param url: ProvStore document URL
  :type url: str or unicode
  :param format: Document format
  :type format: str or unicode
  :param authorization: Authorization token (API key)
  :type autoorization: str or unicode

  :returns: response status code and response text
  :rtype: tuple (int, str or unicode)
  :raises requests.exceptions.ConnectionError: if there are
  problems executing the request e.g. the URL cannot be found
  """
  accept_type = CONTENT_TYPES[format]
  headers = {http.ACCEPT: accept_type,
             http.AUTHORIZATION: authorization}
  response = requests.get(url + "." + format, 
                          headers=headers, 
                          allow_redirects=True)
  return (response.status_code, response.text)

def delete(url, authorization):
  """Delete a document from ProvStore.
  
  :param url: ProvStore document URL
  :type url: str or unicode
  :param authorization: Authorization token (API key)
  :type authorization: str or unicode
  :returns: response status code and response text
  :rtype: tuple (int, str or unicode)
  :raises requests.exceptions.ConnectionError: if there are
  problems executing the request e.g. the URL cannot be found
  """
  headers = {http.AUTHORIZATION: authorization}
  response = requests.delete(url, headers=headers)
  return (response.status_code, response.text)
