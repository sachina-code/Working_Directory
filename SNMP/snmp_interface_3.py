# Script captures the stat of each interface and appends it in the result.txt file


from pysnmp.entity.rfc3413.oneliner import cmdgen
import datetime

cmdGen = cmdgen.CommandGenerator()

host = "10.85.88.25"
community = "DEVOPS"

# Hostname OID
system_name = "1.3.6.1.2.1.1.5.0"


# Interface OID
# interface_name = '1.3.6.1.2.1.2.2.1.2.' + str(x)
# in_oct = '1.3.6.1.2.1.2.2.1.10.' + str(x)
# in_uPackets = '1.3.6.1.2.1.2.2.1.11.' + str(x)
# out_oct = '1.3.6.1.2.1.2.2.1.16.' + str(x)
# out_uPackets = '1.3.6.1.2.1.2.2.1.17.' + str(x)
int_number = "1.3.6.1.2.1.2.1.0"


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


interface_number = snmp_query(host, community, int_number)

int_numb = int(interface_number)

unit = range(int_numb)

result = {}

for x in unit:
    interface_name = "1.3.6.1.2.1.2.2.1.2." + str(x)
    in_oct = "1.3.6.1.2.1.2.2.1.10." + str(x)
    in_uPackets = "1.3.6.1.2.1.2.2.1.11." + str(x)
    out_oct = "1.3.6.1.2.1.2.2.1.16." + str(x)
    out_uPackets = "1.3.6.1.2.1.2.2.1.17." + str(x)

    result["interface_name"] = snmp_query(host, community, interface_name)
    result["Time"] = datetime.datetime.utcnow().isoformat()
    result["hostname"] = snmp_query(host, community, system_name)
    result["Interface_In_Octet"] = snmp_query(host, community, in_oct)
    result["Interface_In_uPackets"] = snmp_query(host, community, in_uPackets)
    result["Interface_Out_Octet"] = snmp_query(host, community, out_oct)
    result["Interface_Out_uPackets"] = snmp_query(host, community, out_uPackets)

    with open("results.txt", "a") as f:
        f.write(str(result))
        f.write("\n")
