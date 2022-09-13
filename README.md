<a href="https://trifinite.org/stuff/tool_temparary-profiler/" target="_blank"><img align="right" src="/images/temparary-profiler_logo.png"/></a>

# temparary-profiler - Helper tool for temparary
This tool is part of Project TEMPA (https://trifinite.org/tempa/)

The temparary-profiler tool is used in order to generate vehicle profiles to be used with the temparary-tool.

Find out more about the temparary tool application on https://trifinite.org/stuff/tool_temparary/ 

## Installation
Install all the reqiuired python requiremets:
```
$> python3 -m pip install -r requirements.txt
```

## Usage
Since the used Bleak library (https://github.com/hbldh/bleak) depends on the bluez dbus-service, please make sure to start the bluetooth service (in case you stopped it beforehand).

This works for Ubuntu:
```
$> sudo systemctl start bluetooth
```

Within the Bluetooth range of the respective Tesla vehicle you want to impersonate using temparary run:
```
$> python3 temparary-profiler.py
```

In case, there is more than one Tesla vehicle in range, the script will generate one JSON-file per vehicle. It is also possible to filter the Tesla vehicles by VIN number. (The VIN number can be found in the lower section of the windshield on the left hand side of the vehicle)
```
$> python3 temparary-profiler.py --vin XP7YGCEE3MBR00112
```

## Disclaimer
Only use this tool on Tesla vehicles you own or have permission to do so!
