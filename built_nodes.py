import requests, json, re
from iteration_utilities import duplicates, unique_everseen

def normalize(node):
    node.pop("modems")
    node.pop("cmts")
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

def get_nodes():
    lima_nodes = []
    # url_login = 'http://190.117.108.84:1380/pathtrak/login/view.html#/login'
    # url_page = 'http://190.117.108.84:1380/pathtrak/main/dashboard'

    # COOKIES VÁLIDOS
    # {'JSESSIONID': '798F94186575CBEF86C7D879964B2218'}
    # {'JSESSIONID': '904583CCA4AC3CFB48FDE7BB30B540F7'}
    # 1BE5D32027F07BBA071FCA7F0D789FCD
    print("Getting data's nodes from Xpertrak ...")
    url_nodes = 'http://190.117.108.84:1380/pathtrak/api/node'
    data_nodes = requests.get(url_nodes, cookies={'JSESSIONID': '1BE5D32027F07BBA071FCA7F0D789FCD'})

    if data_nodes.status_code == 200:
        print("Data Obtained")
        data_nodes = data_nodes.content
        data_nodes = json.loads(data_nodes)

        for node in data_nodes:

            if re.search("^LM", node["name"], re.IGNORECASE):
                normalize(node)
                lima_nodes.append(node)
            
            elif re.search("^LAMO", node["name"], re.IGNORECASE):
                normalize(node)
                lima_nodes.append(node)

            elif re.search("^5", node["name"], re.IGNORECASE):
                normalize(node)
                lima_nodes.append(node)
            
            else:
                pass
        
        name_nodes = []
        for node in lima_nodes:
            name_nodes.append(node["name"])
        redundant_nodes = list(unique_everseen(duplicates(name_nodes)))

        complete_redundant_nodes = []
        for node in lima_nodes:
            if node["name"] in redundant_nodes:
                complete_redundant_nodes.append(node)
        
        for node in complete_redundant_nodes:
            link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/summary/metric?sampleResponse=false'.format(node["nodeId"])
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
        return print("Error 500 - Iniciar Sesión")
    
    else:
        return print("Error")
