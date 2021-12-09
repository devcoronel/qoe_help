import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from up import mydb, get_values_in_dates
from constants import *
import re

def if_column_exists(x, dates, new_dates):
    for date in dates:

        query = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(x, date)

        cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if result[0][0] == 1:
            new_dates.append(date)

    dates = new_dates
    return dates

def algorithm(my_node, my_days, x, also_today, only_one = False): # x only can be 'HOURS' or 'QOE'
    match = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    duration_today = (today.hour)*60 + today.minute
    dates = []
    value_nodes = []

    try:
        my_node = str(my_node).upper()
        my_days = int(my_days)
        days = my_days
        if my_days == 0:
            return {"msg": "Dato(s) incorrectos"}

        regex = re.escape(my_node) + r"\w*"
        for node in lima_nodes:
            if re.search(regex, node["name"], re.IGNORECASE):
                match.append(node)

        if match == []:
            return {"msg": "Plano(s) no encontrado(s)"}
        
    except:
        return {"msg": "Dato(s) incorrectos"}

    if only_one == True and len(match) > 1:
        for only_node in match:
            if my_node == only_node["name"]:
                match = [only_node]
        # Mejorar aqui, corre 3 veces
        if len(match) > 1:
            return {"msg": "Se necesita especificar solo un plano"}
    
    def create_link(nodeid, duration, date, x = True):
        if x:
            link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(url_ext, nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
            return link
        else:
            link_modul = 'http://{}/pathtrak/api/node/{}/capacity/channels/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
            return link_modul
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)

    new_dates = []
    dates = if_column_exists(x, dates, new_dates)

    if dates == []:
        return {"msg": "No se tiene data en estos últimos {} dias".format(days)}
    
    for node in match:
        value_node = []
        if also_today:

            if x == 'MODULATION':
                link = create_link(node["nodeId"],duration_today, today_utc, False)
                data = requests.get(link)
                if data.status_code == 200:
                    data = data.content
                    mydata_modul = json.loads(data)

                    change_modul_group = []
                    modul_node_dayly = []
                    modul_node_dayly.append(mydata_modul["upstreamTotalChannels"])
                    modul_node_dayly.append(mydata_modul["upstreamChannelCapacityHistory"])

                    for modul in modul_node_dayly[1]:
                        if modul["modChanged"] == True and modul["modType"] != "qam64":
                            change_modul_group.append(modul)
                    
                    value_node.append(len(change_modul_group))
                
                else:
                    value_node.append("NO DATA")

            else:

                link = create_link(node["nodeId"], duration_today, today_utc)
                data = requests.get(link)
                if data.status_code == 200:
                    data = data.content
                    data = json.loads(data)

                    if data == []:
                        value_node.append("NO DATA")
                    
                    elif x == 'NEW_HOURS':
                        counter = 0
                        for j in data:
                            if j["qoeScore"] < min_qoe:
                                counter = counter + 1
                        hours = (counter*15)/60
                        value_node.append(hours)
                    
                    elif x == 'NEW_QOE':
                        scores = []
                        for j in data:
                            scores.append(j["qoeScore"])
                        qoe = round(sum(scores)/len(scores), 0)
                        value_node.append(qoe)
                    
                    elif x == 'PERIOD':
                        period = []
                        for j in data:
                            if j["qoeScore"] < min_qoe:
                                ts = j["timestamp"]
                                hour = int((dt.datetime(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13])) - dt.timedelta(hours=5)).strftime("%H"))
                                if hour > umbral_night:
                                    period.append("NOCHE")
                                elif hour > umbral_morning_afternoon:
                                    period.append("DIA")
                        total_noche = period.count("NOCHE")
                        total_dia = period.count("DIA")

                        if total_dia > 24 and total_noche > 12:
                            value_period = "TODO EL DIA"
                        elif total_dia > 24 and total_noche <= 12:
                            value_period = "DIA"
                        elif total_dia > 12 and total_noche > 12:
                            if total_dia >= total_noche:
                                value_period = "DIA"
                            else:
                                value_period = "NOCHE"
                        elif total_dia > 12 and total_noche <= 12:
                            value_period = "DIA"
                        elif total_dia <= 12 and total_noche > 12:
                            value_period = "NOCHE"
                        elif total_dia <= 12 and total_noche <= 12:
                            if total_dia > 8 and total_noche > 8:
                                value_period = "DIA"
                            elif total_dia > 8:
                                value_period = "DIA"
                            elif total_noche > 8:
                                value_period = "NOCHE"
                            else:
                                value_period = "NO AFECTADO"
                        
                        value_node.append(value_period)
                    
                    else:
                        pass
                
                else:
                    value_node.append("NO DATA")

        query1 = "SELECT "
        for date in dates:
            query1 = query1 + "`"+ date + "`,"
        query1 = query1[:-1]
        query1 = query1 + " FROM {} WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');".format(x, node["name"])

        cursor = mydb.cursor()
        cursor.execute(query1)
        result = cursor.fetchall()

        # MOMENTANEO
        if result != []:
            for value in result[0]:
                value_node.append(value)

            value_nodes.append({node["name"] : value_node})

            if also_today:    
                dates.insert(0, today.strftime("%d/%m/20%y"))

    return {"msg": [value_nodes, dates]}

def data_priority(table, afected_id_nodes, dates):
    query = "SELECT "
    for date in dates:
        query += "`"+ date + "`,"
    query = query[:-1]
    query += " FROM {} WHERE ID_NODE IN {};".format(table, afected_id_nodes)

    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # FALTA


def new_priority():
    days = days_priority
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []
    dates = if_column_exists('AFECTED_DAYS', dates, new_dates)

    query = "SELECT ID_NODE FROM AFECTED_DAYS WHERE "
    for date in dates:
        query += "`"+ date + "`+"
    query = query[:-1]
    query += ">= 2;"

    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    afected_id_nodes = []
    for id_node in result:
        afected_id_nodes.append(id_node[0])
    afected_id_nodes = str(tuple(afected_id_nodes))
    # OPTIMIZAR PRIORITY



new_priority()

def priority():

    try:
        days = days_priority
        dates = []
        today_utc = dt.datetime.utcnow()
        today = today_utc - dt.timedelta(hours=5)
        
        for day in range(days+1):
            dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
        dates.pop(0)
        
        new_dates = []
        dates = if_column_exists('AFECTED_DAYS', dates, new_dates)
        
        general_values = []
        especific_values = []
        total_especific_qoe = []
        total_especific_hours = []
        total_especific_period = []
        total_especific_modulation = []
        # Iterar planos
        query = "SELECT * FROM NODES;"
        cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        for node in result:
            general_value = []
            especific_value = []

            result_1 = get_values_in_dates(dates, "AFECTED_DAYS", int(node[0]))
            suma = sum(result_1)

            if suma > 1:
                general_value.append(node[1])
                especific_value.append(node[1])
                
                query2 = "SELECT DEPENDENCIA, IMPEDIMENTO, REVISION, TIPO, PROBLEMA, ESTADO FROM STATUS_NODE WHERE ID_NODE = {}".format(node[0])
                cursor = mydb.cursor()
                cursor.execute(query2)
                result_2 = cursor.fetchall()
                result_2 = list(result_2[0])

                for item in result_2:
                    general_value.append(item)
                    especific_value.append(item)
                especific_value.pop(1)
                especific_value.pop(1)
                especific_value.pop(1)
                
                general_value.insert(5, suma)
                especific_value.insert(2, suma)

                general_values.append(general_value)
                especific_values.append(especific_value)

                total_especific_qoe.append(get_values_in_dates(dates, "NEW_QOE", int(node[0])))
                total_especific_hours.append(get_values_in_dates(dates, "NEW_HOURS", int(node[0])))
                total_especific_period.append(get_values_in_dates(dates, "PERIOD", int(node[0])))
                total_especific_modulation.append(get_values_in_dates(dates, "MODULATION", int(node[0])))


        # general_values = [[[LMLO066, DEPENDENCIA, IMPEDIMENTO, REVISION, TIPO, DIAS, PROBLEMA, ESTADO, V_FECHA1, V_FECHA3], []], [FECHA1, FECHA2, FECHA3]]
        # especific_values = [[[LMLO066, TIPO, DIAS, PROBLEMA, ESTADO, V_FECHA1, V_FECHA3], []], [FECHA1, FECHA2, FECHA3]]
        return [general_values, especific_values , total_especific_qoe, total_especific_hours, total_especific_period, total_especific_modulation, dates]

    except:
        return "Error en la conexión con la Base de Datos"

def modulation(for_modulation):
    # for_modulation = True # La función se usa para el ranking de modulación
    # for_modulation = False # La función se usa para el detalle de un plano
    try:
        days = days_modulation
        dates = []
        today_utc = dt.datetime.utcnow()
        today = today_utc - dt.timedelta(hours=5)
        
        for day in range(days+1):
            dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
        dates.pop(0)
        
        new_dates = []
        dates = if_column_exists('MODULATION', dates, new_dates)

        values = []
        # Iterar planos
        query = "SELECT * FROM NODES;"
        cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        for node in result:
            value = []
            query1 = "SELECT"
            for date in dates:
                query1 = query1 + "`"+ date + "`,"
            query1 = query1[:-1]
            query1 = query1 + " FROM MODULATION WHERE ID_NODE = {};".format(int(node[0]))
            cursor = mydb.cursor()
            cursor.execute(query1)
            result_1 = cursor.fetchall()

            if for_modulation == True:
                suma = sum(result_1[0])

                if suma >= umbral_ch_mod:
                    value.append(node[1])
                    for nmod in result_1[0]:
                        value.append(nmod)
                    values.append(value)
        return [values, dates]
    
    except:
        return "Error en la conexión con la Base de Datos"

def dayly(date):
    today = dt.datetime.utcnow() - dt.timedelta(hours=5)
    my_date = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
    if my_date > today:
        return {"msg":"No hay data para esta fecha"}
    elif my_date.strftime("%d/%m/20%y") == today.strftime("%d/%m/20%y"):
        return {"msg":"Todavía no hay data para esta fecha"}
    else:
        pass

    ytd = my_date.strftime("%d/%m/20%y")
    return {'msg': [[], [ytd]]}