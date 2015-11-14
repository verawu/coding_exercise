from __future__ import absolute_import
import json
import random
import time
import uuid



RANGE_GRID = (0,99)

class Driver(object):
    did = 0
    coords_current = [0,0]
    status= 0
    hail_record = None
    ride_time_est = 0
    pick_time_est = 0
    prev_coords = [0,0]
    
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
	    if (new_hail.timestamp - self.hail_record.timestamp) > (self.absdist(self.hail_record.coords_dropoff, self.hail_record.coords_pickup)/60):
	        # update driver states
		states = 0
		return 0
	    else:
	        return 1
	else:
	    return 0
    
    # absolute distance
    def absdist(self, src, dst):
	return abs(src[0]-dst[0]) + abs(src[1]-dst[1])
	
'''
    def __updateStatus__(self, new_hail):
        waittime = (abs(self.coords_current[0]-new_hail.coords_pickup[0])+ abs(self.coords_current[1]-new_hail.coords_pickup[1]))/60
        if waittime > 0.5:
            return false
        
        if self.status = 0:            
            return true

        # driver is busy since last check
        # you can comment out updatePosition and leave only udpateStatusCode

        if !updateStatusCode(new_hail):
            # updatePosition(new_hail)
        
        # driver became available
        if self.status = 0:
            return true

        return false

    def __updateStatusCode__(self, new_hail):
        time_passed = new_hail.timpstamp-hail_record.timestamp
        if time_passed >=ride_time_est:
            self.status = 0
            self.coords_current = self.hail_record.coords_dropoff
            self.hail_record = None
            self.ride_time_est = 0
            self.pick_time_est = 0
            self.prev_coords = self.coords_current
            return true
        return false    

    def __updatePosition__(self, new_hail):
        time_passed = new_hail.timpstamp-hail_record.timestamp
        if time_passed = pick_time_est:
            self.coords_current = self.hail_record.coords_pickup
        else if time_passed < pick_time_est:
            time_est_x = abs(self.hail_record.coords_pickup[0]-self.prev_coords[0])/60
            time_est_y = abs(self.hail_record.coords_pickup[1]-self.prev_coords[1])/60

            if time_passed < time_est_x:
                relative_dis = (self.hail_record.coords_pickup[0]-self.prev_coords[0]) * (time_passed/time_est_x)
                self.coords_current[0] += relative_dis
            else:
                relative_dis = (self.hail_record.coords_pickup[0]-self.prev_coords[0]) * ((time_passed-time_est_x)/time_est_y)
                self.coords_current = self.hail_record.coords_pickup[0]
                self.coords_current[1] += relative_dis
        else:
            time_passed_after_pickup = ride_time_est - pick_time_est
            time_est_x = abs(self.hail_record.coords_dropoff[0]-self.hail_record.coords_pickup[0])/60
            time_est_y = abs(self.hail_record.coords_dropoff[1]-self.hail_record.coords_pickup[1])/60

            if time_passed < time_est_x:
                relative_dis = (self.hail_record.coords_dropoff[0]-self.hail_record.coords_pickup[0]) * (time_passed_after_pickup/time_est_x)
                self.coords_current[0] += relative_dis
            else:
                relative_dis = (self.hail_record.coords_dropoff[1]-self.hail_record.coords_pickup[1]) * ((time_passed_after_pickup-time_est_x)/time_est_y)
                self.coords_current = self.hail_record.coords_dropoff[0]
                self.coords_current[1] += relative_dis

    def __pickup__(self, hail):
        self.hail_record = hail
        self.status = 1
            
        self.pick_time_est = abs(self.hail_record.coords_pickup[0]-self.coords_current[0])/60 + abs(self.hail_record.coords_pickup[1]-self.coords_current[1])/60
        arrival_time_est =  abs(self.hail_record.coords_dropoff[0]-self.hail_record.coords_pickup[0])/60 +   abs(self.hail_record.coords_dropoff[1]-self.hail_record.coords_pickup[1])/60
        self.ride_time_est = arrival_time_est + self.pick_time_est
'''
