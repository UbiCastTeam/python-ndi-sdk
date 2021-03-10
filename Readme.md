# Magewell Capture SDK python wrapper

## Description
python-ndi-sdk provides a python wrapper allowing to use the library 
libMWCapturemade available by the Magewell Capture SDK (http://www.magewell.com/files/sdk/Magewell_Capture_SDK_Linux_3.3.1.1313.tar.gz).  
python-ndi-sdk provides all the definitions of the
cast C ++ -> Python structures.  
python-ndi-sdk provides access to these resources through a D-Bus service.

## Installation
### Prerequisites
You must first generate the dynamic libraries from the 
static libraries provided by the Magewell Capture SDK.
You will find in the archive a script doing this (Magewell_Capture_SDK_Linux_3.3.1.1313/Lib/gen_shared.sh).
Copy the generated dynamic libraries to your lib folder (usually 
/usr/lib) and run the ldconfig command.
### Procedure
Perform the following commands:
```
git clone https://github.com/UbiCastTeam/python-ndi-sdk.git
cd python-ndi-sdk/
sed -i 's/\/bin/\/local\/bin/g' dbus-1/system-services/com.magewell.MWCapture.service
sudo ./setup.py install
```

## Use
After installation carry out the following command:
```
mc-magewell-signal 
A209180830030 HDMI 1920x1080p 60.00 Hz RGB
```
This is a D-Bus client that displays the characteristics of thedevices
videoconnected to the Capture Magewell.


