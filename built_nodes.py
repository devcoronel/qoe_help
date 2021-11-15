import requests, json, re
from iteration_utilities import duplicates, unique_everseen

def redundant(listNums):
	return list(unique_everseen(duplicates(listNums)))

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
    print("Getting data's nodes from Xpertrak ...")
    url_nodes = 'http://190.117.108.84:1380/pathtrak/api/node'
    data_nodes = requests.get(url_nodes, cookies={'JSESSIONID': '904583CCA4AC3CFB48FDE7BB30B540F7'})
    print("Data Obtained")

    if data_nodes.status_code == 200:
        print("200 - OK")
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
        
        # name_nodes = []
        # for node in lima_nodes:
        #     name_nodes.append(node["name"])
        # redundant_nodes = redundant(name_nodes)
        # print(redundant_nodes)


        # ENCONTRAR UN MECANISMO PARA QUEDARSE CON EL MEJOR NODO QUE SÍ ARROJE DATA
        # UN MÉTODO PARA ESO SERÍA ANALIZAR EL MÉTODO GET PARA VER SI ARROJA CODIGO 200 O 500
        # YA QUE EN LA BASE DE DATOS SE BUSCA QUE HAYA UN VALOR ÚNICO EN LA COLUMNA PLANO

        # TAMBIEN DURANTE UN PERIODO DE TIEMPO CREAR UNA LISTA ESTÁTICA QUE PUEDA SER CONSULTADA
        # POR LA INTERFAZ WEB. PARA QUE NO SE EXRAIGA DATA CADA VEZ QUE SE HAGA UNA CONSULA

        return lima_nodes
    
    elif data_nodes.status_code == 500:
        return print("Error 500 - Iniciar Sesión")
    
    else:
        return print("Error")
get_nodes()
# ['LMLV050', 'LMAT055', 'LAMO022', 'LMSB051', 'LMPL036']