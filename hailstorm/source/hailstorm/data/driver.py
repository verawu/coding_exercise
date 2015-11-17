from __future__ import absolute_import
import json
import random
import time
import uuid



RANGE_GRID = (0,99)

class Driver(object):
    did = 0
    coords_current = None
    status= 0
    hail_record = None
    pick_time_est = 0
    
    def __init__(self, did, current, status):
        self.did = did
        self.coords_current = current
        self.status = status

    def __str__(self):
        return '%(cls)s|%(did)s|%(locx)s,%(locy)s' % dict(
            cls=self.__class__.__name__,
            did=self.did,
            locx=self.coords_current[0],
            locy=self.coords_current[1]
        )
    
    def checkStatus(self, new_hail):
	# check if driver has a hail record
        if self.hail_record is not None:
            # check if previous hail is finished
            if (new_hail.timestamp - self.hail_record.timestamp) > self.absdist(self.hail_record.coords_dropoff, self.coords_current)/(60.0):
                self.status = 0
                self.coords_current = self.hail_record.coords_dropoff
                return 0
            else:
                return 1
        else:
            return 0
    
    # absolute distance
    def absdist(self, src, dst):
        return abs(src[0]-dst[0]) + abs(src[1]-dst[1])

    def pickup(self, new_hail):
        self.hail_record = new_hail
        self.status = 1
        self.pick_time_est = self.absdist(self.coords_current, new_hail.coords_pickup)/60.0