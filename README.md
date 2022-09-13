<a href="https://trifinite.org/stuff/tool_temparary-profiler/" target="_blank"><img align="right" src="/images/temparary-profiler_logo.png"/></a>

# temparary-profiler - Helper tool for temparary
This tool is part of Project TEMPA (https://trifinite.org/tempa/)

The temparary-profiler tool is used in order to generate vehicle profiles to be used with the temparary-tool.

Find out more about the temparary tool application on https://trifinite.org/stuff/tool_temparary/ 

## About
Modern Tesla vehicles (Model 3, Model Y, Model S (2021+) and Model X (2021+)) have a feature where the owner's smartphone can be used as car key. In order to make this work, each Tesla vehicle is exposing a Bluetooth LE interface that is used for passing messages to the phone and to receive messages from the connected phone.

The Tesla research conducted by trifinite.org has shown, that the trust model of the Tesla "Phone-as-a-key" is very unbalanced. Where the smartphone has to cryptographically prove its identity to the vehicle for most of the security-relevant functions, the vehicle itself does not have to do so. Therefore, attackers are able to emulate a Tesla vehicle's Bluetooth interface and communicate to smartphones that connect to the emulated vehicle.

The temparary tool can impersonate/emulate a Tesla car. For the tool to impersonate a specific vehicle in question, the temparary tool requires information that is recognized by the smartphone.

The required information consist of:
* an Extended Inquiry Response dataset, that encodes properties of an iBeacon
* a Scan Response thar encodes the Vehicle ID (S<8 bytes that are hex-encoded>C)
* the vehicles public key

The temparary-profiler tool is able to retrieve this information from the actual vehicle.

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

After a successful profiling, there should be a JSON-file (e.g. S0f7885c2af1a6ef9C.json), that has to be copied to the temparary tool directory.

## Disclaimer
Only use this tool on Tesla vehicles you own or have permission to do so!
