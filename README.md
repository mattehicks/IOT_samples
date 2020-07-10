# IOT_samples
* The IOTmicrocloud platform uses a custom designed AWS pipeline.  
* The platform accepts web input, as well as requests made from the free IOTmicrocloud Android app. 
* Requests are stored with your DeviceID, and a unique identifierID and a timestamp.
* When you run the python script on your device - it asks for requests from the IOTMC backend and answers back with "OK" once its done processing the command. (It loops indefinitely, waiting for more commands).
* You can customize the script to do anything and send any data back that you like.
* The response data is then shown in the web UI, or on the Android display.
-Super easy!
<br/><br/><br/>


## Pi/Arduino INSTRUCTIONS
<br/>
  ## Step 1: Download and run the python app on your device.
  1. Use the button at the bottom of the page to create a unique device ID for your device.  
  2. Download and run "iot_device.py" on your internet connected RaspberryPi or Arduino.
  3. Be sure to replace the default deviceID in the script with  your unique deviceID.
  4. The script will now respond to commands sent to it from the IOTwebsite Demo.

## Step 2: Send commands from the IOTMC-Demo platform.
1. Enter your device ID into the Device ID box  (leave ClientID empty).
2. Send one of the default commands, or send your own command string using the dropdowns + text box.
3. Use the IOT demo at http://demo.iotmicrocloud.com/ to send commands to your device.


## Optional: Use the totally configurable Android IOT app (developed by me!)
* Just enter your DeviceID at the top of the app, and start sending commands.
* The app has default commands like "get temp" and "reset device" but can also be configured to send your own customized commands.
* Just edit the config.txt file and load it in-app. 

## Link to the app:
https://play.google.com/store/apps/details?id=com.iotmicrocloud

-Thanks for trying it out!


![Demo](platform_working.JPG)
