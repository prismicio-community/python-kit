# -*- coding: utf-8 -*-

"""
prismic.utils
~~~~~~~~~~~

This module is mostly for internal use.

"""

import sys


PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring
