#Basic imports
from ctypes import *
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, PositionChangeEventArgs

from Phidgets.Devices.AdvancedServo import AdvancedServo
from Phidgets.Devices.Servo import ServoTypes
#import restbroker
try:
	import json
except ImportError:
	import simplejson as json 
import urllib
import urllib2
import base64
import httplib
import signal


#TODO: ADD YOUR SENSOR NAME AND CREDENTIALS
SENSOR_NAME = 'sensetecnic.demo-servos'
KEY = ''
KEYSECRET = ''
HOST = 'wotkit.sensetecnic.com'

def main():

    def signal_handler(signal, frame):
        print 'You pressed Ctrl+C! Closing Phidgets.'
        try:
            servo.closePhidget()
        except PhidgetException, e:
            PhidgetError(e)

        print("Done.")
        sys.exit(0)

    def PhidgetError(e):
        print("Phidget Exception %i: %s, Exiting." % (e.code, e.details))
	exit(1)

    #Create an servo object
    try:
        servo = AdvancedServo()
    except RuntimeError, e:
        PhidgetError(e)

    def DisplayDeviceInfo():
        print("Servos Attached: %8s | Device Name: %30s" % (servo.isAttached(), servo.getDeviceName()))
        
    #Event Handler Callback Functions
    def ServoAttached(e):
        print("Servo %i Attached!" % (e.device.getSerialNum()))
    def ServoDetached(e):
        print("Servo %i Detached!" % (e.device.getSerialNum()))
    def ServoError(e):
	print("Servo %i: Phidget Error %i: %s" % (e.device.getSerialNum(), e.eCode, e.description))

    #Main Program Code
    try:
        servo.setOnAttachHandler(ServoAttached)
        servo.setOnDetachHandler(ServoDetached)
        servo.setOnErrorhandler(ServoError)
    except PhidgetException, e:
        PhidgetError(e)

    print("Waiting for attach....")
    try:
        servo.openPhidget()
        servo.waitForAttach(10000)
    except PhidgetException, e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        try:
            servo.closePhidget()
        except PhidgetException, e:
            PhidgetError(e)
	print("Exiting....")
	exit(1)
    else:
        DisplayDeviceInfo()

    try:
        #set servos types and accelerations, set engaged so we can use them.
        servo.setServoType(0, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
        servo.setAcceleration(0, servo.getAccelerationMax(0)/2)
        servo.setVelocityLimit(0, servo.getVelocityMax(0)/2)
        servo.setEngaged(0, True)
        servo.setServoType(1, ServoTypes.PHIDGET_SERVO_HITEC_HS322HD)
        servo.setAcceleration(1, servo.getAccelerationMax(1)/2)
        servo.setVelocityLimit(1, servo.getVelocityMax(1)/2)
        servo.setEngaged(1, True)

        # authentication setup
        conn = httplib.HTTPConnection(HOST)
        base64string = base64.encodestring('%s:%s' % (KEY, KEYSECRET))[:-1]
        authheader =  "Basic %s" % base64string
        headers = {'Authorization': authheader}
        
        #subscribe first and get the subscribe ID
        conn.request("POST", "/wotkit/api/control/sub/" + SENSOR_NAME, headers=headers)
        data = conn.getresponse().read()
        json_object = json.loads(data)
        subId = json_object['subscription']

        # set Ctrl+C handler to quit and close phidgets properly
        signal.signal(signal.SIGINT, signal_handler)

        # get data
        print "Getting Control data..."
        while 1:
	    #print "request started for subId: " + str(subId)
            conn.request("GET", "/wotkit/api/control/sub/" + str(subId) + "?wait=10",headers=headers)
            response = conn.getresponse()
            data = response.read()
            json_object = json.loads(data)
            
            #print data;
            #print json_object
		
            for item in json_object:
                if item.has_key('slider'):
                    servo.setPosition(0, (float) (item['slider']))
                if item.has_key('button'):
                    if item['button'] == 'on':
                        servo.setPosition(1, 50)
                    elif item['button'] == 'off':
                        servo.setPosition(1, 110)
  
    except PhidgetException, e:
        PhidgetError(e)

if __name__ == "__main__":
    main()

