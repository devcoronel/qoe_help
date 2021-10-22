import requests, json

txt = open('NODES.txt', 'r')
b = json.loads(txt.read())
txt.close()

nodes = []
for n in b:
    n.pop("modems")
    n.pop("cmts")
    n.pop("cmtsNodeId")
    n.pop("cmtsNode")
    n.pop("rphyMac")
    n.pop("macDomain")
    n.pop("serviceGroup")
    n.pop("billingNodeId")
    n.pop("billingNode")
    n.pop("hcu")
    n.pop("rpmPortId")
    n.pop("rpmPort")
    n.pop("rpmPortMapTyp")
    n.pop("cmtsUsPortId")
    n.pop("cmtsUsPortName")
    n.pop("upstreamServiceGroup")
    n.pop("downstreamServiceGroup")
    n.pop("qoeLicensed")
    n.pop("rphy")
    n.pop("pnmLicensed")
    n.pop("modemHealthLicensed")
    n.pop("topologyOutageLicensed")
    n.pop("modemLiveAnalyzerLicensed")
    n.pop("modemHistoryLicensed")
    n.pop("modemAnalyserLicensed")
    n.pop("topologyAlarmLicensed")
    
    nodes.append(n)

print(nodes)
# En la consola ejecutar el programa
# Luego validar en https://jsonformatter.curiousconcept.com/#
# Copiar el clipboard y pegar en nodes.py