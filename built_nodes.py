import requests, json, re
from iteration_utilities import duplicates, unique_everseen
from constants import url_ext, url_int

def normalize(node):
    node.pop("modems")
    node.pop("cmtsNodeId")
    node.pop("cmtsNode")
    node.pop("rphyMac")
    node.pop("macDomain")
    node.pop("serviceGroup")
    node.pop("billingNodeId")
    node.pop("billingNode")
    node.pop("hcu")
    node.pop("rpmPortId")
    node.pop("rpmPort")
    node.pop("rpmPortMapTyp")
    node.pop("cmtsUsPortId")
    node.pop("cmtsUsPortName")
    node.pop("upstreamServiceGroup")
    node.pop("downstreamServiceGroup")
    node.pop("qoeLicensed")
    node.pop("rphy")
    node.pop("pnmLicensed")
    node.pop("modemHealthLicensed")
    node.pop("topologyOutageLicensed")
    node.pop("modemLiveAnalyzerLicensed")
    node.pop("modemHistoryLicensed")
    node.pop("modemAnalyserLicensed")
    node.pop("topologyAlarmLicensed")

def get_nodes(cookie):
    lima_nodes = []
    try:
        print("Getting data's nodes from Xpertrak")
        url_nodes = 'http://{}/pathtrak/api/node'.format(url_ext)
        data_nodes = requests.get(url_nodes, cookies={'JSESSIONID': '{}'.format(cookie)})

        if data_nodes.status_code == 200:
            print("Data Obtained")
            data_nodes = data_nodes.content
            data_nodes = json.loads(data_nodes)

            for node in data_nodes:

                if re.search("^RPM", node["name"], re.IGNORECASE):
                    pass
                
                else:
                    normalize(node)
                    if node["cmts"] == None:
                        node["cmts"] = "-"
                    lima_nodes.append(node)
            
            name_nodes = []
            for node in lima_nodes:
                name_nodes.append(node["name"])
            redundant_nodes = list(unique_everseen(duplicates(name_nodes)))

            complete_redundant_nodes = []
            for node in lima_nodes:
                if node["name"] in redundant_nodes:
                    complete_redundant_nodes.append(node)
            
            for node in complete_redundant_nodes:
                link = 'http://{}/pathtrak/api/node/{}/summary/metric?sampleResponse=false'.format(url_ext, node["nodeId"])
                get_link = requests.get(link)
                if get_link.status_code == 500:
                    index = lima_nodes.index(node)
                    lima_nodes.pop(index)

                elif get_link.status_code == 200:
                    pass
                else:
                    index = lima_nodes.index(node)
                    lima_nodes.pop(index)

            file_nodes = open('lima_nodes.py', 'w')
            file_nodes.write('lima_nodes = [')
            for i in lima_nodes:
                file_nodes.write(json.dumps(i))
                file_nodes.write(',\n')
            file_nodes.write(']')
            file_nodes.close()

            return lima_nodes 
        
        elif data_nodes.status_code == 500:
            return {"msg":"Cookie incorrecta"}
        
        else:
            return {"msg":"Cookie incorrecta"}

    except:
        return {"msg":"Verifique su conexión a Internet o se ha excedido el límite de conexiones con Xpertrak"}
