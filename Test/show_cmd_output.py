#!/usr/bin/env python

import json, datetime, time, sys
from netmiko import ConnectHandler

# Used to calculate the total script runtime at the end
start_time = datetime.datetime.now()


# Loads the devices file from devices.json

with open("/root/Working_Directory/Test/devices.json", "r") as f:
    devices = json.load(f)

# Code to pop the script file name from sys.argv
sys.argv.pop(0)


# Starts the loop for devices and prints the command output on the terminal
for device in devices.keys():
    jnpr = {
        "device_type": "juniper",
        "host": devices[device]["ip"],
        "username": "stc",
        "password": "Password1",
    }
    net_connect = ConnectHandler(**jnpr)
    time.sleep(2)
    print("\n\n\n")
    print(device)
    print("------------------------------------------------------")
    print("------------------------------------------------------")
    output = net_connect.send_command("set cli timestamp\n")
    time.sleep(2)
    net_connect.clear_buffer()
    output = net_connect.send_command("set cli screen-length 0\n")
    time.sleep(2)
    net_connect.clear_buffer()
    for arg in sys.argv:
        output = net_connect.send_command(arg)
        time.sleep(2)
        print("\n")
        print(arg)
        print("-----------------------------------")
        print(output)
        print("------------------------------------------------------")
        net_connect.clear_buffer()


# Used to calculate the total script runtime
end_time = datetime.datetime.now()
total_time = end_time - start_time
print("Total time taken to run the script is " + str(total_time))
