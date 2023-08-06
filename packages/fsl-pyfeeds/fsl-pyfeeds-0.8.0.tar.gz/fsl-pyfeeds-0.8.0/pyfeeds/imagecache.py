#!/usr/bin/env python
#
# imagecache.py - A cache for NIFTI images
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provide the :class:`ImageCache` class, a simple in-memory
cache for nibabel-loaded files.
"""


import nibabel as nib


class ImageCache(object):
    """The ``ImageCache`` is just a cache for loading ``nibabel`` images (and
    other data types).  Its purpose is to avoid re-loading the same image
    multiple times - once an image has been loaded through the cache, it will
    be kept in the cache for subsequent access.

    An image can be loaded by accessing the ``ImageCache`` as a ``dict``::

        cache = ImageCache()

        # the image is loaded on first access
        img = cache['myiamge.nii.gz']

        # on subsequent accesses, the image
        # is returned from the cache
        img = cache['myiamge.nii.gz']


    TODO Make smarter - discard old images
         when a memory limit is reached.
    """

    def __init__(self):
        """Create the cache. """
        self.__cache = {}


    def __getitem__(self, imagefile):
        """Return the ``nibabel`` image corresponding to the given
        ``imagefile``, loading it if necessary.
        """

        if imagefile in self.__cache:
            return self.__cache[imagefile]

        image = nib.load(imagefile)

        self.__cache[imagefile] = image

        return image


    def __setitem__(self, key, value):
        """Add something to the cache. This is intended to be used for
        storing derived, in-memory-only images.
        """
        self.__cache[key] = value
