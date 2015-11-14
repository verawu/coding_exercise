"""The hailstorm runner.

Usage:
    runner.py [options]

Examples:
    runner.py --time=13:22
    runner.py --outfile=/var/log/mydata.log
    runner.py -t 13:22 -o /var/log/mydata.log
    runner.py (-h | --help)

Options:
    -d --debug              Enable debug output (stdout)
    -o --outfile=<p>        Specify an outfile [default: hailstorm.out]
    -t --time=<t>           Override the current time of day.
                            Note: please use HH:MM formatting.
    -h --help               Show this screen
"""


from __future__ import absolute_import, print_function
import os
import re
import sys
from datetime import datetime
# ---
from docopt import docopt



try:
    from hailstorm.data import datagen
    from hailstorm.data.driver import Driver
except ImportError:
    __root__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(__root__)
    from hailstorm.data import datagen
    from hailstorm.data.driver import Driver



def run():
    idx = (sys.argv.index('--') + 1) if '--' in sys.argv else 1
    arguments = docopt(__doc__, argv=sys.argv[idx:])
    debug = arguments.get('--debug')
    outfile = arguments.get('--outfile')
    when = arguments.get('--time')
    
    # populate 100 driver
    driverList = []
    for i in range(0, 100):
	dtmp = Driver(i,[50,50],0)
        driverList.append(dtmp)
        print(dtmp.did)
        print(dtmp.coords_current[0])
        print(dtmp.coords_current[1])
	

    if when and not isinstance(when, datetime) and re.match(r'\d{2}:\d{2}', when):
        try:
            when = datetime.strptime('{ymd} {t}'.format(ymd=datetime.now().strftime('%Y-%m-%d'), t=when), '%Y-%m-%d %H:%M')
        except ValueError as e:
            raise(e)

    with open(outfile, 'a+') as of:
        for hail in datagen.gen(ts=when):
            if debug:
                print(hail)
            print(hail, file=of)
	       # here goes the logic
	       # print(hail.coords_pickup[0]);
	       # print(hail.coords_pickup[1]);
            #The minimum distance a driver is willing to take a rider is 5 blocks,max 100 blocks;
            rideDistance = abs(hail.coords_pickup[0]-hail.coords_dropoff[0])+ abs(hail.coords_pickup[1]-hail.coords_dropoff[1])
            if rideDistance >=5 and rideDistance <=100:
	        for i in range(0, 100):
		    # status 0 is idle, 1 is busy
		    if driverList[i].checkStatus(hail) == 0:
			print("%d is an idle driver!", driverList[i].did)
            
	    '''
            minDistance = 101
            driverId = 0
            for i in range(0, 100):
                #true if idol
                if driverList[i].updateStatus(hail):
                    pickupDistance = abs(driverList[i].coords_current[0]-hail.coords_pickup[0])+ abs(driverList[i].coords_current[1]-hail.coords_pickup[1])
                    if pickupDistance < minDistance:
                        driverId = i
                        minDistance = pickupDistance
            if minDistance == 101:
                print("fail to pick up this hail")
                print(hail.coords_pickup[0]);
                print(hail.coords_pickup[1]);
            else:
                driverList[driverId].pickup(hail)
                #you can collect pickup est time here
	    '''

    for k, v in arguments.items():
        print('{k} = {v}'.format(k=k, v=v))


if __name__ == '__main__':
    run()
