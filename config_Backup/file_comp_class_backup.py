import json, time, filecmp, smtplib
from netmiko import ConnectHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import empty_line


class fileCompare:
    "Takes the output of some command and compares it with the same output of the previous run. Takes actions if not same"

    def __init__(self, device_name, device_ip):
        self.device_name = device_name
        self.device_ip = device_ip

    def compare_files(self):
        masterFileName = (
            "/root/Working_Directory/config_Backup/"
            + self.device_name
            + "_config_Master.txt"
        )
        tmpFileName = (
            "/root/Working_Directory/config_Backup/"
            + self.device_name
            + "_config_tmp.txt"
        )
        tmpFileName1 = (
            "/root/Working_Directory/config_Backup/"
            + self.device_name
            + "_config_tmp1.txt"
        )
        jnpr = {
            "device_type": "juniper",
            "host": self.device_ip,
            "username": "xxx",
            "password": "xxx",
        }
        net_connect = ConnectHandler(**jnpr)
        time.sleep(5)
        output = net_connect.send_command("set cli screen-length 0\n")
        with open(tmpFileName, "w+") as f1:
            output = net_connect.send_command("show configuration")
            time.sleep(5)
            f1.write(output)

        # To remove empty lines from tmpFile
        with open(tmpFileName, "r") as f4:
            with open(tmpFileName1, "w+") as f5:
                for line in f4.readlines():
                    if not empty_line.isLineEmpty(line):
                        f5.write(line)

        # Compares the tmp file to the Master output to check if there are any new coredump
        if not filecmp.cmp(tmpFileName1, masterFileName):
            with open(tmpFileName1, "r") as f2:
                with open(masterFileName, "w+") as f3:
                    for line in f2.readlines():
                        if not empty_line.isLineEmpty(line):
                            f3.write(line)

    def save_config(self):
        if not filecmp.cmp(tmpFileName1, masterFileName):
            date = (
                str(localtime.tm_year)
                + "-"
                + str(localtime.tm_mon)
                + "-"
                + str(localtime.tm_mday)
            )
            dir = os.path.join("/root/STC_Config_Backup/", date)
            if not os.path.exists(dir):
                os.mkdir(dir)

            backupFile = (
                "/root/STC_Config_Backup/"
                + date
                + "/"
                + self.device_name
                + "_Config_"
                + date
                + ".cfg"
            )
            with open(masterFileName, "r") as f6:
                with open(backupFile, "w+") as f7:
                    for line in f6.readlines():
                        f7.write(line)
