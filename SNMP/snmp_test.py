from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

system_up_time_oid = "1.3.6.1.2.1.25.1.1.0"
cisco_contact_info_oid = "1.3.6.1.2.1.1.5.0"

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData("DEVOPS"),
    cmdgen.UdpTransportTarget(("10.85.88.25", 161)),
    system_up_time_oid,
    cisco_contact_info_oid,
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
            print("%s = %s" % (name.prettyPrint(), str(val)))
