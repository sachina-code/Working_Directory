import json, time, filecmp, smtplib, time, os
from netmiko import ConnectHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import empty_line



class fileCompare:
    'Takes the output of some command and compares it with the same output of the previous run. Takes actions if not same'
    localtime = time.localtime(time.time())

    def __init__(self, device_name, device_ip):
        self.device_name = device_name
        self.device_ip = device_ip
        self.compare = True
        self.masterFileName = '/root/Working_Directory/config_Backup/' + self.device_name + '_config_Master.txt'
        self.tmpFileName = '/root/Working_Directory/config_Backup/' + self.device_name + '_config_tmp.txt'
        self.tmpFileName1 = '/root/Working_Directory/config_Backup/' + self.device_name + '_config_tmp1.txt'
        self.date = str(fileCompare.localtime.tm_year) + '-' + str(fileCompare.localtime.tm_mon) + '-' + str(fileCompare.localtime.tm_mday)


    def compare_files(self):
        jnpr = {'device_type': 'juniper', 'host': self.device_ip, 'username': 'stc', 'password': 'Password1'}
        net_connect = ConnectHandler(**jnpr)
        time.sleep(5)
        output = net_connect.send_command("set cli screen-length 0\n")
        with open(self.tmpFileName, 'w+') as f1:
            output = net_connect.send_command("show configuration")
            time.sleep(5)
            f1.write(output)

        # To remove empty lines from tmpFile
        with open(self.tmpFileName, 'r') as f4:
            with open(self.tmpFileName1, 'w+') as f5:
                for line in f4.readlines():
                    if not empty_line.isLineEmpty(line):
                        f5.write(line)

        # Compares the tmp file to the Master output to check if there are any new coredump
        if not filecmp.cmp(self.tmpFileName1, self.masterFileName):
            self.compare = False
            with open(self.tmpFileName1, 'r') as f2:
                with open(self.masterFileName, 'w+') as f3:
                    for line in f2.readlines():
                        if not empty_line.isLineEmpty(line):
                            f3.write(line)

    # Method to save create directory and save config in it
    def save_config(self):
        if not self.compare:
            dir = os.path.join("/root/STC_Config_Backup/", self.date)
            if not os.path.exists(dir):
                os.mkdir(dir)

            backupFile = '/root/STC_Config_Backup/' + self.date + '/' + self.device_name + '_Config_' + self.date + '.cfg'
            with open(self.masterFileName, 'r') as f6:
                with open(backupFile, 'w+') as f7:
                    for line in f6.readlines():
                        f7.write(line)



    def send_mail(self):

        fromaddr = "sachina@juniper.net"
        toaddr = "sachina@juniper.net"

        # MIMEMultipart
        msg = MIMEMultipart()

        # senders email address
        msg['From'] = fromaddr

        # receivers email address
        msg['To'] = toaddr

        # the subject of mail
        msg['Subject'] = f'Config Backup Alert {self.device_name}'

        # the body of the mail
        body = " Issue with config backup script"

        msg.attach(MIMEText(body, 'plain'))

        message = msg.as_string()
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(fromaddr, toaddr, message)
