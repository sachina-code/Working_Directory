from netmiko import ConnectHandler


def device_connect(dev_ip, uname, pwd):
    jnpr = {
        "device_type": "juniper",
        "host": dev_ip,
        "username": uname,
        "password": pwd,
    }
    return ConnectHandler(**jnpr)
