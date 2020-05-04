# Script to check each device for any newly generated coredump and if present, send a mail alert

import json, time, filecmp, smtplib
from netmiko import ConnectHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


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
    jnpr = {
        "device_type": "juniper",
        "host": devices[device]["ip"],
        "username": "stc",
        "password": "Password1",
    }
    net_connect = ConnectHandler(**jnpr)
    time.sleep(5)
    output = net_connect.send_command("set cli screen-length 0\n")
    with open(tmpFileName, "w+") as f1:
        for command in commands:
            output = net_connect.send_command(command)
            time.sleep(5)
            f1.write(output)

    # Compares the tmp file to the Master output to check if there are any new coredump
    if not filecmp.cmp(tmpFileName, masterFileName):
        with open(tmpFileName, "r") as f2:
            with open(masterFileName, "w+") as f3:
                for line in f2.readlines():
                    f3.write(line)

        # Code to send mail

        fromaddr = "sachina@juniper.net"
        toaddr = "sachina@juniper.net"

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
