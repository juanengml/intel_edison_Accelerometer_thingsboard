from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_mma7660 as upmMMA7660
import os
import time
import sys
#import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json


THINGSBOARD_HOST = 'delrey.td.utfpr.edu.br'
ACCESS_TOKEN = 'u6xiinYt45q8SqOL4G56'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'x': 0, 'y': 0,'z':0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()


import time,os # importa biblioteca de tempo e os para sistema operacional



def main():
    myDigitalAccelerometer = upmMMA7660.MMA7660(
                                            upmMMA7660.MMA7660_DEFAULT_I2C_BUS,
                                            upmMMA7660.MMA7660_DEFAULT_I2C_ADDR);

    def SIGINTHandler(signum, frame):
        raise SystemExit

    def exitHandler():
        print("Exiting")
        sys.exit(0)

    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)
    myDigitalAccelerometer.setModeStandby()
    myDigitalAccelerometer.setSampleRate(upmMMA7660.MMA7660_AUTOSLEEP_64)
    myDigitalAccelerometer.setModeActive()
    ax = upmMMA7660.new_floatp()
    ay = upmMMA7660.new_floatp()
    az = upmMMA7660.new_floatp()

    while (1):
        myDigitalAccelerometer.getAcceleration(ax, ay, az)
        sensor_data['x'] = upmMMA7660.floatp_value(ax)
        sensor_data['y'] = upmMMA7660.floatp_value(ay)
        sensor_data['z'] = upmMMA7660.floatp_value(az)
        
        outputStr = ("'Acceleration',{0},"
                     "{1},"
                     "{2}").format(upmMMA7660.floatp_value(ax),
        upmMMA7660.floatp_value(ay),
        upmMMA7660.floatp_value(az))
        print(outputStr)
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        time.sleep(.5)

if __name__ == '__main__':
    main()
    
client.loop_stop()
client.disconnect()    