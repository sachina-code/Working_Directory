from netmiko import ConnectHandler
import time, sys, re, os
from prettytable import PrettyTable


def isis_check_with_conf(device_ip):
    # Func to check ISIS neighbours based on ISIS Config 
    jnpr = {'device_type': 'juniper', 'host': device_ip, 'username': 'stc', 'password': 'Password1'}
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
        
    
    #List of interfaces from Protocol ISIS Config
    interface_list = []    
    
        
    for line in isis_conf:
        intf = re.match("interface (.*?) {", line)
        if intf:
            interface_list.append((intf.group(1)))
     
    #Counters to have the number of Up, Down neighbours and L2 Neighbours 
    up_isis = 0
    down_isis = 0
    l2_isis = 0
    
    b = []
        
    # Code For Final Result Display
    t = PrettyTable(['Interface', 'ISIS_State'])
    
    #Code to loop over each interface in config and check whether they are Up & Level2
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
                    t.add_row([item, 'Up'])
                elif 'Up' in a:  
                    up_isis = up_isis + 1
                    t.add_row([item, 'Up'])
                break    
     
    #Code to loop over each interface in config and check whether they are present in the ISIS Adj list
    for item in interface_list:
        if item not in b:
            t.add_row([item, 'Down or Not Configured'])
                 
                        
    print('------------------------------------------------------')
    print('------------------------------------------------------')
    print(t)             
    print('------------------------------------------------------')
    print('------------------------------------------------------')   
                       
    down_isis = len(interface_list) - up_isis                           
    
    print(str(up_isis) + " ISIS Neighbors Are Up")
    print(str(l2_isis) + " ISIS Neighbors Are Level 2")
    print(str(down_isis) + " ISIS Neighbors Are Down")
    
    # Code to remove the .txt files are script run
    if os.path.exists("isis.txt"):
        os.remove("isis.txt")

    
    if os.path.exists("isis_conf.txt"):
        os.remove("isis_conf.txt")        
        
        

def isis_check_db(device_ip):
    # Func to check ISIS neighbours based on Interfaces in CSV File 
    jnpr = {'device_type': 'juniper', 'host': device_ip, 'username': 'stc', 'password': 'Password1'}
    net_connect = ConnectHandler(**jnpr)
    time.sleep(2)
    output = net_connect.send_command("set cli screen-length 0\n")
    time.sleep(2)
    output = net_connect.send_command("show isis adjacency\n")
    
    with open('isis.txt', 'w+') as f1:
        f1.write(output)
        
    with open('isis.txt', 'r') as f3:
        isis = f3.readlines()    
        
    #Code to read the interfaces from the csv file 
    with open('isis.csv','r') as csv_file:
        lines = csv_file.readlines()
    
    interface_list = []
    for line in lines:
        data = line.rstrip().split(',')
        interface_list.append(data[0])

    interface_list.pop(0)       
     
    #Counters to have the number of Up, Down neighbours and L2 Neighbours  
    up_isis = 0
    down_isis = 0
    l2_isis = 0
    
    b = []
    
    # Code For Final Result Display
    t = PrettyTable(['Interface', 'ISIS_State'])
    
    #Code to loop over each interface in config and check whether they are Up & Level2
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
                    t.add_row([item, 'Up'])
                elif 'Up' in a:  
                    up_isis = up_isis + 1   
                    t.add_row([item, 'Up'])
                break    
     
    #Code to loop over each interface in config and check whether they are present in the ISIS Adj list
    for item in interface_list:
        if item not in b:
            t.add_row([item, 'Down or Not Configured'])
            
            
    print('------------------------------------------------------')
    print('------------------------------------------------------')
    print(t)             
    print('------------------------------------------------------')
    print('------------------------------------------------------')                    
    
                       
    down_isis = len(interface_list) - up_isis   
                            
    print(str(len(interface_list)) + " ISIS Neighbors Were Queried")
    print(str(up_isis) + " ISIS Neighbors Are Up")
    print(str(l2_isis) + " ISIS Neighbors Are Level 2")
    print(str(down_isis) + " ISIS Neighbors Are Down")
   
    # Code to remove the .txt files are script run
    if os.path.exists("isis.txt"):
        os.remove("isis.txt")
