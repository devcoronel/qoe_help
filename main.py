import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from up import mydb
from constants import *
import re

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
                print("cae aqui")
                match = [only_node]
        # Mejorar aqui, corre 3 veces
        print(match)
        if len(match) > 1:
            return {"msg": "Se necesita especificar solo un plano"}
    
    def create_link(nodeid, duration, date):
        link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(url_ext, nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
        return link
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)

    new_dates = []
    for date in dates:

        query0 = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(x, date)

        cursor = mydb.cursor()
        cursor.execute(query0)
        result = cursor.fetchall()
        if result[0][0] == 1:
            new_dates.append(date)

    dates = new_dates
    if dates == []:
        return {"msg": "No se tiene data en estos últimos {} dias".format(days)}
    
    for node in match:
        value_node = []
        if also_today:
            link = create_link(node["nodeId"], duration_today, today_utc)
            print(link)
            data = requests.get(link)
            if data.status_code == 200:
                data = data.content
                data = json.loads(data)

                if data == []:
                    value_node.append("Null")
                
                if x == 'NEW_HOURS':
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
                            if hour > 17:
                                period.append("NOCHE")
                            elif hour > 8:
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
                    return print("Error typing HOURS or QOE")
            
            else:
                value_node.append("Null")

        query1 = "SELECT "
        for date in dates:
            query1 = query1 + "`"+ date + "`,"
        query1 = query1[:-1]
        query1 = query1 + " FROM {} WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');".format(x, node["name"])

        cursor = mydb.cursor()
        cursor.execute(query1)
        result = cursor.fetchall()
        for value in result[0]:
            value_node.append(value)

        value_nodes.append({node["name"] : value_node})

        if also_today:    
            dates.insert(0, today.strftime("%d/%m/20%y"))

    return {"msg": [value_nodes, dates]}

def priority():
    days = days_priority
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []
    for date in dates:

        query0 = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = 'AFECTED_DAYS' AND COLUMN_NAME = '{}'),1,0);
        """.format(date)

        cursor = mydb.cursor()
        cursor.execute(query0)
        result = cursor.fetchall()
        if result[0][0] == 1:
            new_dates.append(date)

    dates = new_dates
    
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
        query1 = query1 + " FROM AFECTED_DAYS WHERE ID_NODE = {};".format(int(node[0]))
        cursor = mydb.cursor()
        cursor.execute(query1)
        result_1 = cursor.fetchall()
        suma = sum(result_1[0])

        if suma > 1 and suma < days +1:
            value.append(node[1])
            
            query2 = "SELECT DEPENDENCIA, IMPEDIMENTO, TIPO, PROBLEMA, ESTADO , DETALLE FROM STATUS_NODE WHERE ID_NODE = {}".format(node[0])
            cursor = mydb.cursor()
            cursor.execute(query2)
            result_2 = cursor.fetchall()
            for data in result_2[0]:
                value.append(data)
            
            value.insert(4, suma)
            # print(value)

            values.append(value)
    
    # print(values)
    #print(result)
    # Hacer una sumatoria de las 8 últimas fechas cargadas de la tabla AFECTED_DAYS
    
    # Si la sumatoria sale en el rango de 1 a 8, adjuntarla en una lista
    
    #
    # values = [[[LMLO066, DEPENDENCIA, IMPEDIMENTO, TIPO, DIAS, PERIODO, PROBLEMA, ESTADO , DETALLE, V_FECHA1, V_FECHA3], []], [FECHA1, FECHA2, FECHA3]]
    return values
