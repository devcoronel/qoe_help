import mysql.connector
import datetime as dt
import json
import requests
from built_nodes import get_nodes
from constants import *
from xpertrak_login import get_cookie

mydb = mysql.connector.connect(
    host= mysql_host,
    user= mysql_user,
    password= mysql_password,
    database = mysql_database,
    auth_plugin= mysql_auth_plugin # Define la autenticación que tendrá con la base de datos. DEJAR COMENTADO EN LA PC DE OFICINA
    # Se puede verificar en la base de datos con SELECT HOST, USER, PLUGIN FROM MYSQL.USER;
    # Fuente: https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
)

def init():
    try:
    # if True:
        cookie = get_cookie()
        lima_nodes = get_nodes(cookie)

        for node in lima_nodes:
            query = "INSERT INTO NODES (PLANO, CMTS) VALUES ('{}', '{}');".format(node["name"], node["cmts"])
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            cursor.close()
        return print("======== ¡SUCCESS! ========")

    except:
    # else:
        return print("Error")

def complete():
    query = "SELECT ID FROM NODES"
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    
    for id in result:
        for x in ['MODULATION', 'STATUS_NODE', 'NEW_HOURS', 'NEW_QOE', 'PERIOD', 'AFECTED_DAYS']:
            query0 = "INSERT INTO {} (ID_NODE) VALUES ({})".format(x, id[0])
            cursor = mydb.cursor()
            cursor.execute(query0)
            mydb.commit()

def insert_value(tabla, fecha, valor, plano):
    cursor = mydb.cursor()
    if tabla == 'PERIOD':
        query = "UPDATE {} SET `{}` = '{}' WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');".format(tabla, fecha, valor, plano)
    else:    
        query = "UPDATE {} SET `{}` = {} WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = '{}');".format(tabla, fecha, valor, plano)
    cursor.execute(query)
    mydb.commit()
    cursor.close()

def get_values_in_dates(dates, tabla, id_node):
    query = "SELECT"
    for date in dates:
        query = query + "`"+ date + "`,"
    query = query[:-1]
    query = query + " FROM {} WHERE ID_NODE = {};".format(tabla, id_node)
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result = list(result[0])
    cursor.close()
    return result

def create_column(tabla, ytd, tipo, default):
    query = "ALTER TABLE {} ADD COLUMN `{}` {} DEFAULT {} AFTER ID_NODE;".format(tabla, ytd, tipo, default)
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()
    cursor.close()
    print("Column {} created in {}".format(ytd, tabla))

def delete_column(tabla, fecha):
    query = "ALTER TABLE {} DROP COLUMN `{}`;".format(tabla, fecha)
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()
    cursor.close()

def autocomplete_null(tabla, ytd, value):
    cursor = mydb.cursor()
    if tabla == 'PERIOD':
        query = "UPDATE {} SET `{}` = '{}' WHERE `{}` = Null;".format(tabla, ytd, value, ytd)
    else:
        query = "UPDATE {} SET `{}` = {} WHERE `{}` = Null;".format(tabla, ytd, value, ytd)
    cursor.execute(query)
    mydb.commit()
    cursor.close()

def get_period(dia, noche, madrugada, hours):
    
    if dia >= 24:
        if noche >= 12:
            value_period = "TODO EL DIA"
        else:
            value_period = "DIA"
    else:
        if dia >= 12:
            if noche >= 12:
                value_period = "TODO EL DIA"
            else:
                value_period = "DIA"
        else:
            if noche >= 12:
                value_period = "NOCHE"
            else:
                if madrugada >= 12:
                    value_period = "MADRUGADA"
                else:
                    if hours >= 3:
                        value_period = 'INTERMITENTE'
                    else:
                        value_period = "NO AFECTADO"

    return value_period

def verify_upload(date, cookie):
    today = dt.datetime.utcnow() - dt.timedelta(hours=5)
    my_date = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
    if my_date > today:
        return {"msg":"No hay data para esta fecha"}
    elif my_date.strftime("%d/%m/20%y") == today.strftime("%d/%m/20%y"):
        return {"msg":"Todavía no hay data para esta fecha"}
    else:
        pass

    ytd = my_date.strftime("%d/%m/20%y")
    lima_nodes = get_nodes(cookie)
    if isinstance(lima_nodes, dict):
        return lima_nodes

    for bool in ['MODULATION', 'NEW_HOURS', 'NEW_QOE', 'PERIOD', 'AFECTED_DAYS']:

        query0 = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(bool, ytd)

        cursor = mydb.cursor()
        cursor.execute(query0)
        result = cursor.fetchall()
        cursor.close()
        
        if result[0][0] == 1:
            print("Column {} already exists in {} table".format(ytd, bool))
            return {"msg": "Ya existe data cargada en {}".format(ytd)}
        
    create_column('NEW_HOURS', ytd, 'FLOAT', -1)
    create_column('NEW_QOE', ytd, 'FLOAT', -1)
    create_column('PERIOD', ytd, 'VARCHAR(20)', "'NO DATA'")
    create_column('AFECTED_DAYS', ytd, 'INT(1)', 0)
    create_column('MODULATION', ytd, 'FLOAT', 0)
    my_date_plus = my_date + dt.timedelta(days=1)

    return [lima_nodes, ytd, my_date_plus]


def upload(lima_nodes, ytd, my_date_plus):
    contador = 0
    for node in lima_nodes:
    # if True:
        contador += 1
        link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,str(node["nodeId"]), my_date_plus.year, str(my_date_plus.month).zfill(2), str(my_date_plus.day).zfill(2))
        link_modul = 'http://{}/pathtrak/api/node/{}/capacity/channels/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,str(node["nodeId"]), my_date_plus.year, str(my_date_plus.month).zfill(2), str(my_date_plus.day).zfill(2))
        try:
        # if True:
            mydata = requests.get(link)

            value_qoe = -1
            value_hours = -1
            value_period = "NO DATA"
            value_afected = 0
            value_modulation = 0

            if mydata.status_code == 200:
                mydata = mydata.content
                mydata = json.loads(mydata)
                
                if mydata == []:
                    print(contador, node["name"], "200 - Without data")
                    print(link)

                    insert_value('NEW_HOURS', ytd, value_hours, node["name"])
                    insert_value('NEW_QOE', ytd, value_qoe, node["name"])
                    insert_value('PERIOD', ytd, value_period, node["name"])
                    insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])

                else:
                    print(contador, node["name"], "200 - OK")
                    print(link)

                    # QOE, HORAS QOE AFECTADO Y PERIODO DE AFECTACIÓN
                    counter = 0
                    period = []
                    scores = []

                    for i in mydata:
                        scores.append(i["qoeScore"])

                        if i["qoeScore"] < min_qoe:
                            counter = counter + 1
                            ts = i["timestamp"]
                            hour = int((dt.datetime(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13])) - dt.timedelta(hours=5)).strftime("%H"))
                            if hour > umbral_night:
                                period.append("NOCHE")
                            elif hour > umbral_morning_afternoon:
                                period.append("DIA")
                            else:
                                period.append("MADRUGADA")

                    value_qoe = round(sum(scores)/len(scores), 0)
                    value_hours = (counter*15)/60

                    noche = period.count("NOCHE")
                    dia = period.count("DIA")
                    madrugada = period.count("MADRUGADA")

                    value_period = get_period(dia, noche, madrugada, value_hours)

                    insert_value('NEW_HOURS', ytd, value_hours, node["name"])
                    insert_value('NEW_QOE', ytd, value_qoe, node["name"])
                    insert_value('PERIOD', ytd, value_period, node["name"])
                
            elif mydata.status_code == 500:
                print(contador, node["name"], "500 - Internal Server Error")
                print(link)

            mydata_modul = requests.get(link_modul)
			
            if mydata_modul.status_code == 200:
                print(contador, node["name"], "200 - OK")
                print(link_modul)
                mydata_modul = mydata_modul.content
                mydata_modul = json.loads(mydata_modul)

                change_modul_group = []
                modul_node_dayly = []
                modul_node_dayly.append(mydata_modul["upstreamTotalChannels"])
                modul_node_dayly.append(mydata_modul["upstreamChannelCapacityHistory"])

                for modul in modul_node_dayly[1]:
                    if modul["modChanged"] == True and modul["modType"] != "qam64":
                        change_modul_group.append(modul)
                value_modulation = len(change_modul_group)

                insert_value('MODULATION', ytd, value_modulation, node["name"])

            elif mydata_modul.status_code == 500:
                print(contador, node["name"], "500 - Internal Server Error")
                print(link_modul)

            # DIAS AFECTADO
            if (value_qoe < min_qoe and value_qoe >= 0) or (value_hours >= min_afected_hours):
                value_afected = 1

            insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])

        except:
        # else:
            print("Error connecting with Xpertrak")
            delete_column("NEW_HOURS", ytd)
            delete_column("NEW_QOE", ytd)
            delete_column("PERIOD", ytd)
            delete_column("AFECTED_DAYS", ytd)
            delete_column("MODULATION", ytd)
            return {"msg": "Error en la conexión con Xpertrak"}
    
    print("======== ¡SUCCESS! ========")
    return {"msg":"Carga subida con éxito"}


def new_upload(node, ytd, my_date_plus):

    link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,str(node["nodeId"]), my_date_plus.year, str(my_date_plus.month).zfill(2), str(my_date_plus.day).zfill(2))
    link_modul = 'http://{}/pathtrak/api/node/{}/capacity/channels/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,str(node["nodeId"]), my_date_plus.year, str(my_date_plus.month).zfill(2), str(my_date_plus.day).zfill(2))
    try:
    # if True:
        mydata = requests.get(link)
        value_qoe = -1
        value_hours = -1
        value_period = "NO DATA"
        value_afected = 0
        value_modulation = 0

        if mydata.status_code == 200:
            mydata = mydata.content
            mydata = json.loads(mydata)
            
            if mydata == []:
                print(node["name"], "200 - Without data")
                print(link)
                insert_value('NEW_HOURS', ytd, value_hours, node["name"])
                insert_value('NEW_QOE', ytd, value_qoe, node["name"])
                insert_value('PERIOD', ytd, value_period, node["name"])
                insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])
            else:
                print(node["name"], "200 - OK")
                print(link)
                # QOE, HORAS QOE AFECTADO Y PERIODO DE AFECTACIÓN
                counter = 0
                period = []
                scores = []
                for i in mydata:
                    scores.append(i["qoeScore"])
                    if i["qoeScore"] < min_qoe:
                        counter = counter + 1
                        ts = i["timestamp"]
                        hour = int((dt.datetime(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13])) - dt.timedelta(hours=5)).strftime("%H"))
                        if hour > umbral_night:
                            period.append("NOCHE")
                        elif hour > umbral_morning_afternoon:
                            period.append("DIA")
                        else:
                            period.append("MADRUGADA")
                value_qoe = round(sum(scores)/len(scores), 0)
                value_hours = (counter*15)/60
                noche = period.count("NOCHE")
                dia = period.count("DIA")
                madrugada = period.count("MADRUGADA")
                value_period = get_period(dia, noche, madrugada, value_hours)
                insert_value('NEW_HOURS', ytd, value_hours, node["name"])
                insert_value('NEW_QOE', ytd, value_qoe, node["name"])
                insert_value('PERIOD', ytd, value_period, node["name"])
            
        elif mydata.status_code == 500:
            print(node["name"], "500 - Internal Server Error")
            print(link)

        mydata_modul = requests.get(link_modul)
		
        if mydata_modul.status_code == 200:
            print(node["name"], "200 - OK")
            print(link_modul)
            mydata_modul = mydata_modul.content
            mydata_modul = json.loads(mydata_modul)
            change_modul_group = []
            modul_node_dayly = []
            modul_node_dayly.append(mydata_modul["upstreamTotalChannels"])
            modul_node_dayly.append(mydata_modul["upstreamChannelCapacityHistory"])
            for modul in modul_node_dayly[1]:
                if modul["modChanged"] == True and modul["modType"] != "qam64":
                    change_modul_group.append(modul)
            value_modulation = len(change_modul_group)
            insert_value('MODULATION', ytd, value_modulation, node["name"])

        elif mydata_modul.status_code == 500:
            print(node["name"], "500 - Internal Server Error")
            print(link_modul)
        # DIAS AFECTADO
        if (value_qoe < min_qoe and value_qoe >= 0) or (value_hours >= min_afected_hours):
            value_afected = 1
        insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])

    except:
    # else:
        print("Error connecting with Xpertrak")
        delete_column("NEW_HOURS", ytd)
        delete_column("NEW_QOE", ytd)
        delete_column("PERIOD", ytd)
        delete_column("AFECTED_DAYS", ytd)
        delete_column("MODULATION", ytd)
        return {"msg": "Error en la conexión con Xpertrak"}
    
    print("======== ¡SUCCESS! ========")
    return {"msg":"Carga subida con éxito"}