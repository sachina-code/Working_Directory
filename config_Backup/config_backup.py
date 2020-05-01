import file_comp_class
import json, time, filecmp, smtplib, sys

# Loads the devices file
with open('/root/Working_Directory/config_Backup/devices.json', 'r') as f:
    devices = json.load(f)



# Starts the loop for devices and writes the show_sys_coredump output into a tmp file
# Sends email alert if the below action fails

for device in devices.keys():
    try:
        dev = file_comp_class.fileCompare(device, devices[device]['ip'])
        dev.compare_files()
        dev.save_config()
    except:
        dev.send_mail()
