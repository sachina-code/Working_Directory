from netmiko import ConnectHandler
import time, sys, re  

jnpr = {'device_type': 'juniper', 'host': '10.85.88.25', 'username': 'stc', 'password': 'Password1'}
net_connect = ConnectHandler(**jnpr)
time.sleep(2)
output = net_connect.send_command("set cli screen-length 0\n")
time.sleep(2)
output = net_connect.send_command("show configuration protocols isis\n")

with open('isis_conf.txt', 'w+') as f:
    f.write(output)

output = net_connect.send_command("show isis adjacency\n")

with open('isis.txt', 'w+') as f1:
    f1.write(output)
    
with open('isis_conf.txt', 'r') as f2:
    isis_conf = f2.readlines()
    
    
with open('isis.txt', 'r') as f3:
    isis = f3.readlines()    
    


interface_list = []    

    
for line in isis_conf:
    intf = re.match("interface (.*?) {", line)
    if intf:
        interface_list.append((intf.group(1)))
 
up_isis = 0
down_isis = 0
l2_isis = 0

b = []

for item in interface_list:
    for line in isis:
        if item in line: 
            b.append(item)   
            a = line.split(' ')
            while("" in a): 
                a.remove("") 
            if ((a[2] == '2') and ('Up' in a)):
                up_isis = up_isis + 1
                l2_isis = l2_isis + 1
            elif 'Up' in a:  
                up_isis = up_isis + 1
 

for item in interface_list:
    if item not in b:
        print("ISIS Neighbor " + item + " is not Up")
             
                    

                   
down_isis = len(interface_list) - up_isis                           

print(str(up_isis) + " ISIS Neighbors Are Up")
print(str(l2_isis) + " ISIS Neighbors Are Level 2")
print(str(down_isis) + " ISIS Neighbors Are Down")
    
           
