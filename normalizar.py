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


# SOLO NODOS DE LIMA
# from nodes import nodes
# import re

# regex_1 = re.escape("LM") + r"\w*"
# regex_2 = re.escape("LAMO") + r"\w*"
# regex_3 =re.escape("50") + r"\w*"
# regex_4 =re.escape("51") + r"\w*"
# regex_5 =re.escape("52") + r"\w*"
# regex_6 =re.escape("53") + r"\w*"
# regex_7 =re.escape("54") + r"\w*"
# regex_8 =re.escape("55") + r"\w*"

# lima_nodes = []

# for element in nodes:
#     if re.search(regex_1, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_2, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_3, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_4, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_5, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_6, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_7, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     elif re.search(regex_8, element["name"], re.IGNORECASE):
#         lima_nodes.append(element)
#     else:
#         pass

# print(lima_nodes)