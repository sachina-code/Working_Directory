from pysnmp.entity.rfc3413.oneliner import cmdgen

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime

cmdGen = cmdgen.CommandGenerator()

host = "10.85.88.25"
community = "DEVOPS"

# Hostname OID
system_name = "1.3.6.1.2.1.1.5.0"


# Interface OID
interface_in_oct = "1.3.6.1.2.1.2.2.1.10.794"
interface_in_uPackets = "1.3.6.1.2.1.2.2.1.11.794"
interface_out_oct = "1.3.6.1.2.1.2.2.1.16.794"
interface_out_uPackets = "1.3.6.1.2.1.2.2.1.17.794"


def snmp_query(host, community, oid):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community), cmdgen.UdpTransportTarget((host, 161)), oid
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1] or "?",
                )
            )
        else:
            for name, val in varBinds:
                return str(val)


result = {}
result["Time"] = datetime.datetime.utcnow().isoformat()
result["hostname"] = snmp_query(host, community, system_name)
result["Interface_In_Octet"] = snmp_query(host, community, interface_in_oct)
result["Interface_In_uPackets"] = snmp_query(host, community, interface_in_uPackets)
result["Interface_Out_Octet"] = snmp_query(host, community, interface_out_oct)
result["Interface_Out_uPackets"] = snmp_query(host, community, interface_out_uPackets)

with open("/root/Working_Directory/SNMP/results_for_graph.txt", "a") as f:
    f.write(str(result))
    f.write("\n")


x_time = []
y_value = []


with open("/root/Working_Directory/SNMP/results_for_graph.txt", "r") as f:
    for line in f.readlines():
        # eval(line) reads in each line as dictionary instead of string
        line = eval(line)
        # convert to internal float
        x_time.append(dates.datestr2num(line["Time"]))
        y_value.append(line["Interface_Out_uPackets"])

plt.subplots_adjust(bottom=0.3)
plt.xticks(rotation=80)

# Use plot_date to display x-axis back in date format
plt.plot_date(x_time, y_value)
plt.title("Mx2020 et-2/1/0")
plt.xlabel("Time in UTC")
plt.ylabel("Output Unicast Packets")
plt.savefig("/root/Working_Directory/SNMP/matplotlib_1_result.png")
