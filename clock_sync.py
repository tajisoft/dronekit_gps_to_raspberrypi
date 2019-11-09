# encoding: utf-8

import subprocess
import datetime
import time

from dronekit import connect

NEED_GPS_COUNT = 3

gps_count = 0
timesynced = False

vehicle = connect('127.0.0.1:14550', wait_ready=True)


@vehicle.on_message('GPS_RAW_INT')
def on_gps_raw_int(self, name, message):
    global gps_count
    gps_count = message.satellites_visible


@vehicle.on_message('SYSTEM_TIME')
def on_system_time(self, name, message):
    global gps_count, timesynced, NEED_GPS_COUNT
    if gps_count > NEED_GPS_COUNT and not timesynced:
        sec = message.time_unix_usec / 1e6
        ds = datetime.datetime.fromtimestamp(sec)
        # Sync time
        subprocess.call(
            ['sudo', 'date', '-s', '{:}'.format(ds.strftime('%Y/%m/%d %H:%M:%S'))])
        timesynced = True


while not timesynced:
    time.sleep(0.5)

print('System time is synced! {}'.format(datetime.datetime.now()))
