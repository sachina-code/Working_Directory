from netmiko import ConnectHandler
import time, sys, re  

jnpr = {'device_type': 'juniper', 'host': '10.85.88.25', 'username': 'stc', 'password': 'Password1'}
net_connect = ConnectHandler(**jnpr)
time.sleep(2)
output = net_connect.send_command("set cli screen-length 0\n")
time.sleep(2)
output = net_connect.send_command("show configuration protocols isis")

with open('isis_conf.txt', 'w+') as f:
    f.write(output)

output = net_connect.send_command("show isis adjacency")

with open('isis.txt', 'w+') as f:
    f.write(output)
    
with open('isis_conf.txt', 'r') as f:
    isis_conf = f.readlines()
    
with open('isis.txt', 'r') as f:
    isis = f.readlines()    
    
interface_list = []    

    
for line in isis_conf:
    intf = re.match("interface (.*?) {", line)
    if intf:
        interface_list.append((intf.group(1)))
 
up_isis = 0
down_isis = 0

for item in interface_list:
    for line in isis:
        if item in line:
            if 'Up' in line.split(' '):  
                up_isis = up_isis + 1
            else:
                down_isis = down_isis + 1   
                           

print(str(up_isis) + " ISIS Neighbors Are Up")
print(str(down_isis) + " ISIS Neighbors Are Down")
    
            
