import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from up import mydb, get_period, cursor
from constants import *
import re

def insert_status(dependence, impediment, revision, problem_type, problem, state, detail, node):
    
    query = """
    UPDATE STATUS_NODE
    SET DEPENDENCIA = '{}', IMPEDIMENTO = '{}', REVISION = '{}', TIPO = '{}', PROBLEMA = '{}', ESTADO = '{}', DETALLE = '{}'
    WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');
    """.format(dependence, impediment, revision, problem_type, problem, state, detail, node)

    regex = r"^"+ node + r"$"
    for lima_node in lima_nodes:
        if re.search(regex, lima_node["name"], re.IGNORECASE):
            cursor.execute(query)
            mydb.commit()
            # cursor.close()
            return {'msg': '{}: Status actualizado con éxito'.format(node)}
    
    return {'msg': 'No se ha encontrado el plano en la base de datos'}


def if_column_exists(x, dates, new_dates):
    for date in dates:

        query = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(mysql_database, x, date)

        # cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()
        if result[0][0] == 1:
            new_dates.append(date)

    dates = new_dates
    return dates

def data_analysis(dates, table, regex, region):

    query_dates = ""
    for date in dates:
        query_dates += "`"+ date + "` , "
    query_dates =  query_dates[:-2]

    query = """
    SELECT REGION, CMTS, PLANO, {0} FROM NODES
    INNER JOIN {1} ON {1}.ID_NODE = NODES.ID
    WHERE PLANO REGEXP '^{2}' AND REGION = '{3}';
    """.format(query_dates, table, regex, region)
    # cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()
    if cursor.rowcount == 0:
        return "Plano(s) no encontrado(s)"
    else:
        return result
    

def analysis(regex, days, x, region):

    try:
        regex = str(regex).upper()
        days = int(days)
        if days == 0 or x not in ['SAMPLING', 'STRESSEDMODEMS', 'IMPACTEDMODEMS', 'NEW_QOE', 'NEW_HOURS', 'PERIOD', 'MODULATION']:
            return "Dato(s) incorrectos"
    except:
        return "Dato(s) incorrectos"

    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    new_dates = []

    try:
        dates = if_column_exists(x, dates, new_dates)

        if dates == []:
            return "No hay data en estos últimos {} días".format(days)
        
        else:
            analysis = data_analysis(dates, x, regex, region)
            if x == 'NEW_HOURS':
                id_table = 'hourstable'
            elif x == 'NEW_QOE':
                id_table = 'qoetable'
            elif x == 'PERIOD':
                id_table = 'periodtable'
            elif x == 'IMPACTEDMODEMS':
                id_table = 'impactedtable'
            elif x == 'STRESSEDMODEMS':
                id_table = 'stressedtable'
            elif x == 'SAMPLING':
                id_table = 'samplingtable'
            else:
                id_table = 'modulationtable'
            return [analysis, dates, id_table]
    
    except:
        return "Error en la conexión con la Base de Datos"
        

def detail(my_node, my_days, x):
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

        regex = r"^"+ my_node+ r"$"
        for node in lima_nodes:
            if re.search(regex, node["name"], re.IGNORECASE):
                match.append(node)

        if match == []:
            return {"msg": "Plano(s) no encontrado(s)"}
        elif len(match) > 1:
            return {"msg": "Se necesita especificar solo un plano"}
        
    except:
        return {"msg": "Dato(s) incorrectos"}
    
    def create_link(nodeid, duration, date, x = True):
        if x:
            # link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(url_ext, nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
            link = 'http://{}/pathtrak/api/qoesummary?duration={}&limit=96&nodeId={}&nodeLimit=1&startTime={}-{}-{}T{}:{}:59Z'.format(url_ext, duration, nodeid, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
            return link
        else:
            link_modul = 'http://{}/pathtrak/api/node/{}/capacity/channels/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:59.000Z'.format(url_ext ,nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
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
                    counter = 0
                    for j in data:
                        if j["qoeScore"] < min_qoe:
                            counter = counter + 1
                            ts = j["timestamp"]
                            hour = int((dt.datetime(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13])) - dt.timedelta(hours=5)).strftime("%H"))
                            if hour > umbral_night:
                                period.append("NOCHE")
                            elif hour > umbral_morning_afternoon:
                                period.append("DIA")
                            else:
                                period.append("MADRUGADA")
                    hours = (counter*15)/60
                    noche = period.count("NOCHE")
                    dia = period.count("DIA")
                    madrugada = period.count("MADRUGADA")

                    value_period = get_period(dia, noche, madrugada, hours)
                    value_node.append(value_period)
                
                elif x == 'IMPACTEDMODEMS':
                    impacted_modems = []
                    for j in data:
                        impacted_modems.append(j["impactedModems"])
                    value_impacted_modems = max(impacted_modems)
                    value_node.append(value_impacted_modems)
                
                elif x == 'STRESSEDMODEMS':
                    impacted_modems = []
                    stressed_modems = []
                    for j in data:
                        impacted_modems.append(j["impactedModems"])
                        stressed_modems.append(j["stressedModems"])
                    value_impacted_modems = max(impacted_modems)
                    value_stressed_modems = stressed_modems[impacted_modems.index(value_impacted_modems)]
                    value_node.append(value_stressed_modems)

                elif x == 'SAMPLING':
                    counter = 0
                    for j in data:
                        counter += 1
                    value_node.append(counter)
            
            else:
                value_node.append("NO DATA")

        query1 = "SELECT "
        for date in dates:
            query1 = query1 + "`"+ date + "`,"
        query1 = query1[:-1]
        query1 = query1 + " FROM {} WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');".format(x, node["name"])

        # cursor = mydb.cursor()
        cursor.execute(query1)
        result = cursor.fetchall()
        # cursor.close()

        for value in result[0]:
            value_node.append(value)

        value_nodes.append({node["name"] : value_node})
        dates.insert(0, today.strftime("%d/%m/20%y"))

    return {"msg": [value_nodes, dates, x]}

def data_status_node(node, dates):

    sum_dates_general = ""
    sum_dates_afected = ""
    for date in dates:
        sum_dates_general += "`"+ date + "` + "
        sum_dates_afected += "AFECTED_DAYS.`"+ date + "` + "
    sum_dates_general =  sum_dates_general[:-2]
    sum_dates_afected =  sum_dates_afected[:-2]

    query = """SELECT REGION, CMTS, PLANO, DEPENDENCIA, IMPEDIMENTO, DATE_FORMAT(REVISION, '%Y-%m-%d') AS REVISION, TIPO, SUM({0}) AS DAYS, PROBLEMA, ESTADO, DETALLE FROM STATUS_NODE
    INNER JOIN NODES ON NODES.ID = STATUS_NODE.ID_NODE
    INNER JOIN AFECTED_DAYS ON NODES.ID = AFECTED_DAYS.ID_NODE
    WHERE STATUS_NODE.ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{1}')
    GROUP BY STATUS_NODE.ID_NODE
    ORDER BY DAYS DESC, ID DESC;""".format(sum_dates_general, node)
    # cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()
    return result

def status_node(node):

    days = days_priority
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []

    try:
        dates = if_column_exists('AFECTED_DAYS', dates, new_dates)

        if dates == []:
            return "No hay data en estos últimos {} días".format(days)
        
        else:
            status = data_status_node(node, dates)
            return status

    except:
        return "Error en la conexión con la Base de Datos"

def data_priority(general_or_especific, table, dates, region):

    sum_dates_general = ""
    sum_dates_afected = ""
    sum_dates_especific = ""
    for date in dates:
        sum_dates_general += "`"+ date + "` + "
        sum_dates_afected += "AFECTED_DAYS.`"+ date + "` + "
        sum_dates_especific += "{}.`".format(table) + date + "` , "
    sum_dates_general =  sum_dates_general[:-2]
    sum_dates_afected =  sum_dates_afected[:-2]
    sum_dates_especific =  sum_dates_especific[:-2]

    if general_or_especific == 'G':

        query = """SELECT CMTS, PLANO, DEPENDENCIA, IMPEDIMENTO, DATE_FORMAT(REVISION, '%Y-%m-%d') AS REVISION, TIPO, SUM({0}) AS DAYS, PROBLEMA, ESTADO, DETALLE FROM STATUS_NODE
        INNER JOIN NODES ON NODES.ID = STATUS_NODE.ID_NODE
        INNER JOIN AFECTED_DAYS ON NODES.ID = AFECTED_DAYS.ID_NODE
        WHERE STATUS_NODE.ID_NODE IN (
        SELECT ID_NODE FROM AFECTED_DAYS
        WHERE {0} >= 2) AND REGION = '{1}'
        GROUP BY STATUS_NODE.ID_NODE
        ORDER BY DAYS DESC, ID DESC;""".format(sum_dates_general, region)

        # cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()

        return result

    if general_or_especific == 'E':

        query = """SELECT CMTS, PLANO, TIPO, SUM({0}) AS DAYS, PROBLEMA, ESTADO, {1} FROM {2}
        INNER JOIN NODES ON NODES.ID = {2}.ID_NODE
        INNER JOIN STATUS_NODE ON NODES.ID = STATUS_NODE.ID_NODE
        INNER JOIN AFECTED_DAYS ON NODES.ID = AFECTED_DAYS.ID_NODE
        WHERE {2}.ID_NODE IN (
        SELECT ID_NODE FROM AFECTED_DAYS
        WHERE {3} >= 2) AND REGION = '{4}'
        GROUP BY STATUS_NODE.ID_NODE
        ORDER BY DAYS DESC, ID DESC;""".format(sum_dates_afected, sum_dates_especific, table, sum_dates_general, region)

        # cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()

        return result


# def priority(region = 'LIMA'):
def priority(region = "-"):
    days = days_priority
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []

    try:
        dates = if_column_exists('AFECTED_DAYS', dates, new_dates)

        if dates == []:
            return "No hay data en estos últimos {} días".format(days)
        
        else:
            general_priority = data_priority('G', '', dates, region)
            especific_priority_qoe =data_priority('E', 'NEW_QOE', dates, region) 
            especific_priority_hours =data_priority('E', 'NEW_HOURS', dates, region) 
            especific_priority_period =data_priority('E', 'PERIOD', dates, region) 
            especific_priority_modulation =data_priority('E', 'MODULATION', dates, region)
            especific_priority_impacted =data_priority('E', 'IMPACTEDMODEMS', dates, region)
            especific_priority_stressed =data_priority('E', 'STRESSEDMODEMS', dates, region)
            especific_priority_sampling =data_priority('E', 'SAMPLING', dates, region)

            return [general_priority, especific_priority_qoe, especific_priority_hours, especific_priority_period, especific_priority_modulation, especific_priority_impacted, especific_priority_stressed, especific_priority_sampling, dates]

    except:
        return "Error en la conexión con la Base de Datos"

def data_modulation(dates):

    query_dates = ""
    for date in dates:
        query_dates += "`"+ date + "` , "
    query_dates =  query_dates[:-2]

    try:
        query = """
        SELECT CMTS, PLANO, {0} FROM MODULATION
        INNER JOIN NODES ON NODES.ID = MODULATION.ID_NODE
        WHERE ID_NODE IN (
        SELECT ID_NODE FROM MODULATION
        WHERE `{1}` >= 2 AND `{2}` >= 2)
        ORDER BY `{1}` DESC;
        """.format(query_dates, dates[0], dates[1])

        # cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # cursor.close()

        return result
    
    except:
        return "Error en la conexión con la Base de Datos"


def modulation():
    days = days_modulation
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []

    try:
        dates = if_column_exists('MODULATION', dates, new_dates)

        if dates == []:
            return "No hay data en estos últimos {} días".format(days)
        
        else:
            values_modulation = data_modulation(dates)
            return [values_modulation, dates]

    except:
        return "Error en la conexión con la Base de Datos"


def data_dayly(dates, mydate):

    sum_dates_general = ""
    sum_dates_afected = ""
    for date in dates:
        sum_dates_general += "`"+ date + "` + "
        sum_dates_afected += "AFECTED_DAYS.`"+ date + "` + "
    sum_dates_general =  sum_dates_general[:-2]
    sum_dates_afected =  sum_dates_afected[:-2]

    query = """
    SELECT CMTS, PLANO,
    NEW_QOE.`{0}` AS QOE,
    IMPACTEDMODEMS.`{0}` AS IMPACTED,
    STRESSEDMODEMS.`{0}` AS STRESSED,
    NEW_HOURS.`{0}` AS HOURS,
    PERIOD.`{0}` AS PERIOD,
    MODULATION.`{0}` AS MODULATION,
    SUM({1}) AS DAYS
    FROM NODES
    INNER JOIN NEW_QOE ON NEW_QOE.ID_NODE = NODES.ID
    INNER JOIN IMPACTEDMODEMS ON IMPACTEDMODEMS.ID_NODE = NODES.ID
    INNER JOIN STRESSEDMODEMS ON STRESSEDMODEMS.ID_NODE = NODES.ID
    INNER JOIN NEW_HOURS ON NEW_HOURS.ID_NODE = NODES.ID
    INNER JOIN PERIOD ON PERIOD.ID_NODE = NODES.ID
    INNER JOIN MODULATION ON MODULATION.ID_NODE = NODES.ID
    INNER JOIN AFECTED_DAYS ON NODES.ID = AFECTED_DAYS.ID_NODE
    WHERE AFECTED_DAYS.ID_NODE IN (
    SELECT ID_NODE FROM AFECTED_DAYS
    WHERE {2} >= 2)
    OR AFECTED_DAYS.ID_NODE IN (
    SELECT ID_NODE FROM MODULATION
    WHERE `{3}` >= 2 AND `{4}` >= 2)
    GROUP BY AFECTED_DAYS.ID_NODE
    ORDER BY DAYS DESC;
    """.format(mydate, sum_dates_afected, sum_dates_general, dates[0], dates[1])

    # cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()

    return result


def dayly(date):
    days = days_modulation
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []
    my_date = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))

    if my_date > today:
        return "No hay data para esta fecha"

    elif my_date.strftime("%d/%m/20%y") == today.strftime("%d/%m/20%y"):
        return "Todavía no hay data para esta fecha"

    else:

        try:
        # if True:
            dates = if_column_exists('MODULATION', dates, new_dates)

            if dates == [] or (my_date.strftime("%d/%m/20%y") not in dates):
                return "No hay data para la fecha {}".format(my_date.strftime("%d/%m/20%y"))
            
            else:
                values_dayly = data_dayly(dates, my_date.strftime("%d/%m/20%y"))
                return [values_dayly]

        except:
        # else:
            return "Error en la conexión con la Base de Datos"

def data_sampling(dates):

    sum_dates_general = ""
    for date in dates:
        sum_dates_general += "`"+ date + "` , "
    sum_dates_general =  sum_dates_general[:-2]

    query = """"
    SELECT CMTS, PLANO, {} FROM SAMPLING
    INNER JOIN NODES ON NODES.ID = SAMPLING.ID_NODE
    WHERE  `{}` < 90 OR  `{}` < 90;
    """.format(sum_dates_general, dates[0], dates[1])

    # cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()

    return result

def sampling():

    days = days_sampling
    dates = []
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)
    
    new_dates = []

    try:
        dates = if_column_exists('SAMPLING', dates, new_dates)
        if dates == [] or len(dates) == 1:
            return "Asegurarse cargar data los últimos {} días".format(days_sampling)
        
        else:
            values_sampling = data_sampling(dates)
            return [values_sampling]
    except:
        return "Error en la conexión con la Base de Datos"