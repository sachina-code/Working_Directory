# Module to send Coredump alert as mail

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to send Coredump alert as mail when from address, to address and device name is passed as args
# MasterFile name should be provided in the code


def send_mail(fromaddr, toaddr, dev, file):

    # MIMEMultipart
    msg = MIMEMultipart()

    # senders email address
    msg["From"] = fromaddr

    # receivers email address
    msg["To"] = toaddr

    # the subject of mail
    msg["Subject"] = f"Coredump Alert {dev}"

    # the body of the mail
    body = "There is a new coredump"

    msg.attach(MIMEText(body, "plain"))

    # open the file to be sent
    # rb is a flag for readonly
    filename = file
    attachment = open(file, "rb")

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
