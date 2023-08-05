__author__ = 'dstogsdill'
_name_ = 'pypalo'
"""A Python library for interacting with Palo Alto devices"""

#: Version info (major, minor, maintenance, status)
VERSION = (0, 0, 3)
__version__ = '%d.%d.%d' % VERSION[0:3]

from pypalo.pan import Panorama
