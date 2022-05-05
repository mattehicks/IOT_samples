# IOT_samples 
The backend system handles user input from the Demo Website or the Android app. 
Requests are stored with your DeviceID and a timestamp.

The python "IOT" script listens for commands sent from the website, and will answer back with "OK" once its done processing the command, as well as send any information that was requested, like "temperature" or "status" info.  

# Customize the mobile interface to suit your needs.
You can  enter custom commands and in the web text box and on the mobile app, by using the config file provided.
The config file allows you to create a your own custom button layout for sending the commands you provide. 
Device response/data is shown in the app text area.


# Running python samples in the background and exit (on Rpi/Linux):  
 nohup python iot.py &  
 

## Using the IOT Control Web Platform.  
1. Click the 'Create ID' button, then the 'Add Device' button.   
    This will create a new unique id that you can use in your raspberry pi code.
    
2. The "Client ID" box can be empty, but is useful for securing your commands - which would require both boxes to be populated. 
     Note: You will have to validate these values in your Rpi or device code.
     
3. There is a default device already populated called GA1875.  This is a Raspberry Pi device running the included Python sample code (with a temp sensor attached).     

4. Install the python IOT.py sample code on your Raspberry, and run it on your internet connected device. The python instructions are listed above.
 
5. Click on 'SEND' or type your own command string using the dropdowns + text box.

6. After the Rpi device receives the command, it should send a response back - which will be shown in the message table.

7. Optional: Use the IOT Android app to send commands to your devices.

 ![FireShot Capture 002 - IOT Demo - demo iotmicrocloud com](https://user-images.githubusercontent.com/859222/161656646-5c974f0a-5691-4fef-ab67-ea53fd38f9fa.png)


## Using the Mobile app  
* Just enter your DeviceID at the top of the app, and start sending commands.
* The app has default commands like "get temp" and "reset device" but can also be configured to send your own customized commands.
* Just edit the config.txt file and load it in-app. 

## Customizing the mobile app buttons
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
  
    

