from netmiko import ConnectHandler
import time, sys, re

jnpr = {
    "device_type": "juniper",
    "host": "10.85.88.25",
    "username": "xxx",
    "password": "xxx",
}
net_connect = ConnectHandler(**jnpr)
time.sleep(2)
output = net_connect.send_command("show configuration protocols isis")

with open("isis_conf.txt", "w+") as f:
    f.write(output)

output = net_connect.send_command("show isis adjacency")

with open("isis.txt", "w+") as f:
    f.write(output)

with open("isis_conf.txt", "r") as f:
    isis_conf = f.readlines()

interface_list = []


for line in isis_conf:
    intf = re.match("interface (.*?) {", line)
    if intf:
        interface_list.append((intf.group(1)))

print(interface_list)
