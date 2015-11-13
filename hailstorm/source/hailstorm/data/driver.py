from __future__ import absolute_import
import json
import random
import time
import uuid



RANGE_GRID = (0,99)

class Driver(object):
    did = 0
    coords_current = [0,0]

    def __init__(self, did, current):
        self.did = did
        self.coords_current = current

    def __str__(self):
        return '%(cls)s|%(did)s|%(locx)s,%(locy)s' % dict(
            cls=self.__class__.__name__,
            did=self.did,
            locx=self.coords_current[0],
            locy=self.coords_current[1]
        )
