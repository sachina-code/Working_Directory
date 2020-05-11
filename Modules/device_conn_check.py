import sys, stc_cred
from device_connect import device_connect


def device_conn_check(dev_name):
    # Function to read the devices.csv file and login to the RE and check connectivity and pass the Mgmt_ip as output
    with open("devices.csv", "r") as csv_file:
        lines = csv_file.readlines()

    for line in lines[1:]:
        if line.split(",")[0] == dev_name:
            try:
                device_connect(
                    line.split(",")[1], stc_cred.user_name, stc_cred.password
                )
            except:
                print(
                    "Unable to connect to "
                    + line.split(",")[0]
                    + " "
                    + line.split(",")[1]
                )
                try:
                    device_connect(
                        line.split(",")[2], stc_cred.user_name, stc_cred.password
                    )
                except:
                    print(
                        "Unable to connect to "
                        + line.split(",")[0]
                        + " "
                        + line.split(",")[2]
                    )
                else:
                    print(
                        "Connected to " + line.split(",")[0] + " " + line.split(",")[2]
                    )
                    return line.split(",")[2]
            else:
                print("Connected to " + line.split(",")[0] + " " + line.split(",")[1])
                return line.split(",")[1]
