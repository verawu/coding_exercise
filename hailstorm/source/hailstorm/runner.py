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
    -n --num-records=<n>    num of items to be read
    -s --source=<p>         path to a continuously-appended file
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
    numRows = arguments.get('--num-records')
    if numRows is None:
        numRows = 0
    #print(numRows)
    source = arguments.get('--source')
    #limited
    # metric variables
    hail_last_hour = []
    fail_pickup_count = 0    
    # populate 100 driver

    driverList = []
    for i in range(0, 100):
        dtmp = Driver(i,[50,50],0)
        driverList.append(dtmp)

    if when and not isinstance(when, datetime) and re.match(r'\d{2}:\d{2}', when):
        try:
            when = datetime.strptime('{ymd} {t}'.format(ymd=datetime.now().strftime('%Y-%m-%d'), t=when), '%Y-%m-%d %H:%M')
        except ValueError as e:
            raise(e)
    

    with open(outfile, 'a+') as of:
        print("hail_req_count in last hour,"+"hail_pickup_count in last hour,"+"hail_complete_count in last hour,"+"avg pick up time in last hour,"+"fail_pickup_count in total", file=of)
        for hail in datagen.gen(ts=when):
            
            hail_last_hour.append(hail)
            if int(numRows) >0:
                if len(hail_last_hour)-1 == int(numRows):
                    print("reach --num-records, use Ctrl+D to exit")
                    break
            #The minimum distance a driver is willing to take a rider is 5 blocks,max 100 blocks;
            minDistance = 201
            driverId = 0
            rideDistance = abs(hail.coords_pickup[0]-hail.coords_dropoff[0])+ abs(hail.coords_pickup[1]-hail.coords_dropoff[1])
            if rideDistance >=5 and rideDistance <=100:
                for i in range(0, 100):
                    # status 0 is idle, 1 is busy
                    if driverList[i].checkStatus(hail)==0:
                        #print("%d is an idle driver!", driverList[i].did)
                        pickupDistance = driverList[i].absdist(driverList[i].coords_current, hail.coords_pickup)
                        waittime = pickupDistance/(60*1.0)
                        if waittime <=0.5:
                            if pickupDistance < minDistance:
                                driverId = i
                                minDistance = pickupDistance
                if minDistance == 201:
                    hail.pickup_tag = 0
                    fail_pickup_count += 1
                    if debug:
                        print("fail to pick up this hail due to waittime too long")
                        print(hail)
                else:
                    hail.pickup_tag = 1
                    driverList[driverId].pickup(hail)
                    minDistance = 201
                    hail.pick_time_est = driverList[driverId].pick_time_est
                    if debug:
                        print("success in pick up hail")
                        print(hail)
                        print(driverList[driverId])
            
            hail_req_count = 0
            hail_complete_count = 0
            hail_pickup_count = 0
            total_pick_up_time = 0
            # search all hail in last hour
            
            for ihail in hail_last_hour:
                if (hail.timestamp - ihail.timestamp) <= 1.0:
                    hail_req_count += 1
                    if ihail.pickup_tag == 1:
                        if (hail.timestamp - ihail.timestamp) <= hail.pick_time_est:
                            hail_complete_count += 1
                        total_pick_up_time += ihail.pick_time_est
                        hail_pickup_count += 1 
            avg_pickup_time = 0
            if hail_pickup_count > 0:
                avg_pickup_time = 1.0*total_pick_up_time/hail_pickup_count
            if debug:
                print(hail_req_count)
                print("hail_pickup_count in last hour")
                print(hail_pickup_count)
                print("hail_complete_count in last hour")
                print(hail_complete_count)
                print("avg pick up time in last hour")
                print(avg_pickup_time)
                print("fail_pickup_count in total")
                print(fail_pickup_count)
            print(str(hail_req_count)+","+str(hail_pickup_count)+","+str(hail_complete_count)+","+str(avg_pickup_time)+","+str(fail_pickup_count),file=of)

    for k, v in arguments.items():
        print('{k} = {v}'.format(k=k, v=v))


if __name__ == '__main__':
    run()
