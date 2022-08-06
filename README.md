# Overview

## Python sample script:
The python "IOT" script will run on RaspberyPi devices. It has 2 main functions:
1. Listen for commands sent from the website, and will answer back with "OK" once its done processing the command.
2. Send back any status, sensor data, or messages. 

INSTRUCTIONS: Download the script using this command on your Pi:  
wget https://github.com/mattehicks/IOT_samples/edit/master/iot_device.py

## Running python samples in the background and exit (on Rpi/Linux):  
 nohup python iot.py &  
  
  
  
  ---
    
    
## Using the Web Platform.  
1. Click the 'Create ID' button, then the 'Add Device' button.   
    This will create a new unique id that you can use in your raspberry pi code.
    
2. The "Client ID" box can be empty, but is useful for securing your commands - which would require both boxes to be populated. 
     Note: You will have to validate these values in your Rpi or device code.
     
3. There is a default device already populated called GA1875.  This is a Raspberry Pi device running the included Python sample code (with a temp sensor attached).     

4. Install the python IOT.py sample code on your Raspberry, and run it on your internet connected device. The python instructions are listed above.
 
5. Click on 'SEND' or type your own command string using the dropdowns + text box.

6. After the Rpi device receives the command, it should send a response back - which will be shown in the message table.
   BE SURE TO DISABLE ADBLOCK.

7. Optional: Use the IOT Android app to send commands to your devices.

 ![FireShot Capture 002 - IOT Demo - demo iotmicrocloud com](https://user-images.githubusercontent.com/859222/161656646-5c974f0a-5691-4fef-ab67-ea53fd38f9fa.png)


## Using the Mobile app  
* Just enter your DeviceID at the top of the app, and start sending commands.
* The app has default commands like "get temp" and "reset device" but can also be configured to send your own customized commands.
* Just edit the config.txt file and load it in-app. 

! You will need to load a button layout  
The default config file can be downloaded here:  
https://drive.google.com/file/d/1GOUrb33zQEIU4QfK6yqLE7qN93EL857Y/view?usp=sharing  

The config file allows you to create a your own custom button layout for sending the commands you provide. 
* Open the config.txt file from this repo  
* Substitute your custom "Name" and "Json" string. (Leave the default endpoint + endpoint type).  
  
  Example: 
```
{
    "api_name": "MY_CUSTOM_BUTTON",
    "endpoint_type": "POST",
    "endpoint": "https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT/app/commands/{device_id}",
    "json":  "{'eventType':'custom', 'data':'ANY_DATA_YOU_WANT_TO_SEND'}"
}
```
  
![PHONE1](https://user-images.githubusercontent.com/859222/160740720-c6f107bd-f294-4319-ae56-8142b18f7e91.jpg)  ![PHONE2](https://user-images.githubusercontent.com/859222/160740895-403f833d-5269-4e26-a88d-05c0d0ad26b5.jpg)


## Link to the app:  
https://play.google.com/store/apps/details?id=com.iotmicrocloud

-Thanks for trying it out!  
  
  
## Mobile phone users
  The website works well on mobile also!
  
![Screenshot_20220505-103116](https://user-images.githubusercontent.com/859222/166980451-e7ff6aea-443a-4e25-b6d2-c7967eb514b2.png)

