import requests
import json
import time
from threading import Event
# from datetime import datetime
import RPi.GPIO as GPIO
import sys
import os
import glob
import itertools, sys
import threading
import subprocess
import math
import html 


debug = False
my_device_id = "GA1875"
blinkerIO = 17  #pinouts
tempIO = 26     #pinouts
DEBUG = False   #pinouts
TEMP = True
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

BASE_URL = 'https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT'
apiUrl = 'https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT/device'

fetch_url = apiUrl+'/commands/{}'.format(my_device_id)
status_url = apiUrl+'/status/{}'.format(my_device_id)

#TEMP = true
if TEMP is True:
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    temp_sensor = "/sys/bus/w1/devices/28-02131e0b69aa/w1_slave"

events = ['reboot', 'toggle_led', 'status', 'temp', 'geolocate', 'custom_command' ]

print("Running...... Device_id:{}".format(my_device_id))

def setupServices():
    #create auto-run service
    print("service created")


class event(object):
    #request_id
    #timestamp
    #event_type
    #data
    #request_id

    pass

def get_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_f = "{:.2f}".format(temp_f)

        if debug == True:
            print("temp_f: " + str(temp_f))
        return temp_f

def get_system_metrics():
    result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
    return str(result)
    if debug == True:
        print( "RESULT: " + result)

def setupIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(blinkerIO,GPIO.OUT)
    GPIO.setup(tempIO,GPIO.OUT)
    
def blinker():
    GPIO.output(blinkerIO,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(blinkerIO,GPIO.LOW)
    
def handle_toggle_led(requestID,timestamp):
    #handle_toggle_led
    #print("TOGGLING LED...")
    if DEBUG:
        pass
    else:
        GPIO.output(tempIO,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(tempIO,GPIO.LOW)
        post_status(requestID,"OK",timestamp)
        
def handle_reboot(requestID,timestamp):
    #print("REBOOTING DEVICE...")
    post_status(requestID,"rebooting",timestamp)
    
def handle_read_temperature(requestID,timestamp):
    #print("READING TEMPERATURE...")
    post_status(requestID,get_temp(),timestamp)

def handle_custom( requestID,timestamp, command):
    #print("READING TEMPERATURE...")

    print("Terminal command: " + command)
    # result = subprocess.check_output([command])
    result = os.popen(command).read()
    output = html.escape(result, quote=True)
    
    print("result")
    print(output)
    print()
    print(result)
    post_status(requestID, output ,timestamp, "custom")
        

def post_status(requestID, msg_data, timestamp, eventType='status'):

    event_type = eventType
    data = {'request_id' : requestID, 'timestamp': timestamp, 'event_type': event_type, 'data': msg_data }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', "httpMethod": "POST"}
    requests.method = "POST"
    requests.httpBody = data

    print("posting status: ")
    print(data)
    try:
        response = requests.post(status_url, data=data_json, headers=headers)
        print("response: {}".format(response))
        return response
    except:
        print("Unexpected error 1:", sys.exc_info()[0])
        

def handle_status(request_id, timestamp):
    msg_data = {}
    timestamp = math.floor(time.time());
        
    #simulated systems data
    volt = {"voltage":5.0}
    loc =  {"geolocation":"100x100"}
    version = {"version":"v3.10"}
    subsys = {"subsystems":"Ax100"}
    network = {"network":"network55OC"}

    if TEMP:
        t = get_temp()
        temp = {"temp":t}
        msg_data['temp'] = t

    #msg_data['request_id'] = request_id
    print("Outgoing: ")
    print(msg_data)
    
    if DEBUG:
        print(msg_data)
    
    post_status(request_id, msg_data, timestamp)
    
def handle_commands(commands):
    if not commands:
        return
        #commands is all database columns

    for cmd in commands:
        
        try:
            request_id = cmd['request_id']
            timestamp = math.floor(time.time());
            command = cmd['command']
            event_type = cmd['event_type']
        except:
            print("Unexpected error 6:", sys.exc_info()[0])

        print("Handling command:  " + command)
        # if event_type == 'command':
        #     print("{} :: {}".format(request_id,command))
        if command =='get_ip':
            handle_custom(request_id, timestamp, "hostname -I | awk '{print $1}'")

        if command =='toggle_led':
            handle_toggle_led(request_id,timestamp)

        elif command =='reboot':
            handle_reboot(request_id,timestamp)

        elif command =='read_temp':
            handle_read_temperature(request_id,timestamp)

        elif command =='status':
            handle_status(request_id, timestamp)
        
        elif event_type == 'custom':
            print ("{} :: {} ".format(request_id, command))
            handle_custom(request_id, timestamp, command)
        else:
            print("No handler for command: " + command)
        print("")
         

def fetch_commands():
    try:
        # print(".")
        url = BASE_URL+'/device/commands/{}'.format(my_device_id)

#        print(url)
        response = requests.get(url) 
        data = response.json()
 #       print(data)

        if data['Items']:
            if len(data['Items']):
                print('found')
                print(data['Items'])
                #print("#: {}").format(str(len(data['Items'])))
                return data['Items']

    except:
        print("Fetch commands: ", sys.exc_info()[0])
        print(data)
        pass


setupIO()

# #run once
# commands = fetch_commands()
# handle_commands(commands)



while True:
    Event().wait(5) 
    commands = fetch_commands()
    handle_commands(commands)






