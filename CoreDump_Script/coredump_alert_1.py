# Script to check each device for any newly generated coredump and if present, send a mail alert

import sendmail
import json, time, filecmp, smtplib
from netmiko import ConnectHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to remove empty lines
def isLineEmpty(line):
    return len(line.strip()) < 1


# Loads the devices file
with open("/root/Working_Directory/CoreDump_Script/Core_Dump_devices.json", "r") as f:
    devices = json.load(f)


# Loads the text file which contains the commands to enter
with open("/root/Working_Directory/CoreDump_Script/commands.txt", "r") as f:
    commands = f.readlines()


# Starts the loop for devices and writes the show_sys_coredump output into a tmp file
for device in devices.keys():
    masterFileName = (
        "/root/Working_Directory/CoreDump_Script/"
        + device
        + "_coredump_output_Master.txt"
    )
    tmpFileName = (
        "/root/Working_Directory/CoreDump_Script/" + device + "_coredump_output_tmp.txt"
    )
    tmpFileName1 = (
        "/root/Working_Directory/CoreDump_Script/"
        + device
        + "_coredump_output_tmp1.txt"
    )
    jnpr = {
        "device_type": "juniper",
        "host": devices[device]["ip"],
        "username": "xxx",
        "password": "xxx",
    }
    net_connect = ConnectHandler(**jnpr)
    time.sleep(5)
    output = net_connect.send_command("set cli screen-length 0\n")
    with open(tmpFileName, "w+") as f1:
        for command in commands:
            output = net_connect.send_command(command)
            time.sleep(5)
            f1.write(output)

    # To remove empty lines from tmpFile
    with open(tmpFileName, "r") as f4:
        with open(tmpFileName1, "w+") as f5:
            for line in f4.readlines():
                if not isLineEmpty(line):
                    f5.write(line)

    # Compares the tmp file to the Master output to check if there are any new coredump
    if not filecmp.cmp(tmpFileName1, masterFileName):
        with open(tmpFileName1, "r") as f2:
            with open(masterFileName, "w+") as f3:
                for line in f2.readlines():
                    if not isLineEmpty(line):
                        f3.write(line)

        # Code to send mail
        # Code to call the send_mail function from sendmail Module
        sendmail.send_mail(
            "xxx@juniper.net", "xxx@juniper.net", device, masterFileName
        )
