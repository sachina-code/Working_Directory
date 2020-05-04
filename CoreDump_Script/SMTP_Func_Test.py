import json, time, filecmp, smtplib
from netmiko import ConnectHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail(device):

    fromaddr = "sachina@juniper.net"
    toaddr = "sachina@juniper.net"
    masterFileName = device + "_coredump_output_Master.txt"

    # MIMEMultipart
    msg = MIMEMultipart()

    # senders email address
    msg["From"] = fromaddr

    # receivers email address
    msg["To"] = toaddr

    # the subject of mail
    msg["Subject"] = f"Fake Coredump Alert {device}"

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


send_mail("Mx960-1")
