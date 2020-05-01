from netmiko import ConnectHandler
import time, sys
from datetime import datetime

start_time = datetime.now() 
jnpr = {'device_type': 'juniper', 'host': '10.85.88.25', 'username': 'stc', 'password': 'Password1'}
net_connect = ConnectHandler(**jnpr)
time.sleep(2)
output = net_connect.send_command("show isis adjacency")
#print(output)
    
#print(type(output))

with open('isis.txt', 'w+') as f:
    f.write(output)

with open('isis.txt', 'r') as f1:
    isis = f1.readlines()
    
for line in isis:
    a = line.split(' ')    
    if 'ae1.0' in a:
        if 'Up' in a:
            print(str(a[0]) + ' is Up')
        else:
            print(str(a[0]) + ' is Down')
