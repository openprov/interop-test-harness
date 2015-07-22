"""Utilities for dynamic object creation.
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

import os
import importlib
import yaml

def get_class(name):
  """Load class given a module-prefixed class name. A valid
  module-prefixed class name is, for example,
  ``prov_interop.component.Component``. An invalid class name is
  ``Component``.
   
  :param name: Module-prefixed class name
  :type name: str or unicode
  :returns: Class specified in name
  :rtype: classobj
  :raises ValueError: if ``name`` is not module-prefixed
  :raises ImportError: if module cannot be loaded
  :raises AttributeError: if class cannot be found
  """
  module_class = name.rsplit(".",1)
  if len(module_class) != 2:
    raise ValueError(("Class name " + name + " must be module-prefixed"))
  (module_name, class_name) = module_class
  module = importlib.import_module(module_name)
  clazz = getattr(module, class_name)
  return clazz

def get_instance(name):
  """Return instance of class given a module-prefixed class name. A
  valid module-prefixed class name is, for example,
  ``prov_interop.component.Component``. An invalid class name is
  ``Component``. The class must have a 0-arity constructor.

  :param name: Module-prefixed class name
  :type name: str or unicode
  :returns: Instance of class specified in name
  :rtype: instance
  :raises ValueError: if ``name`` is not module-prefixed
  :raises ImportError: if module cannot be loaded
  :raises AttributeError: if class cannot be found
  :raises TypeError: if class constructor has non-0 arity constructor
  """
  return get_class(name)()
