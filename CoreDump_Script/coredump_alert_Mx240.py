# Script to check each device for any newly generated coredump and if present, send a mail alert

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
with open(
    "/root/Working_Directory/CoreDump_Script/Core_Dump_devices_Mx240.json", "r"
) as f:
    devices = json.load(f)


# Loads the text file which contains the commands to enter
with open("/root/Working_Directory/CoreDump_Script/commands.txt", "r") as f:
    commands = f.readlines()


# Function which takes the device name as argument and sends mail when new coredump is found
def send_mail(device):

    fromaddr = "xxx@juniper.net"
    toaddr = "xxx@juniper.net"

    # MIMEMultipart
    msg = MIMEMultipart()

    # senders email address
    msg["From"] = fromaddr

    # receivers email address
    msg["To"] = toaddr

    # the subject of mail
    msg["Subject"] = f"Coredump Alert {device}"

    # the body of the mail
    body = "There is a new coredump"

    msg.attach(MIMEText(body, "plain"))

    # open the file to be sent
    # rb is a flag for readonly
    filename = masterFileName
    attachment = open(masterFileName, "rb")

    # MIMEBase
    attc = MIMEBase("application", "octet-stream")

    # To change the payload into encoded form
    attc.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(attc)

    attc.add_header("Content-Disposition", "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(attc)

    message = msg.as_string()
    smtpObj = smtplib.SMTP("localhost")
    smtpObj.sendmail(fromaddr, toaddr, message)


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
        output = net_connect.send_command("show system core-dumps\n")
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

        send_mail(device)
