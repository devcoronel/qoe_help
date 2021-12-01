import mysql.connector
import datetime as dt
import json
import requests
from requests.exceptions import RetryError
from built_nodes import get_nodes
from constants import *

mydb = mysql.connector.connect(
    host= mysql_host,
    user= mysql_user,
    password= mysql_password,
    database = mysql_database,
    auth_plugin= mysql_auth_plugin # Define la autenticación que tendrá con la base de datos. DEJAR COMENTADO EN LA PC DE OFICINA
    # Se puede verificar en la base de datos con SELECT HOST, USER, PLUGIN FROM MYSQL.USER;
    # Fuente: https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
)

def init(cookie):
    try:
        lima_nodes = get_nodes(cookie)

        for node in lima_nodes:
            print(node["name"])
            query = "INSERT INTO NODES (PLANO) VALUES ('{}');".format(node["name"])
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
        return print("======== ¡SUCCESS! ========")

    except:
        return print("Error")

def complete():
    query = "SELECT ID FROM NODES"
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    for id in result:
        for x in ['STATUS_NODE', 'NEW_HOURS', 'NEW_QOE', 'PERIOD', 'AFECTED_DAYS']:
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

def create_column(tabla, ytd, tipo, default):
    print("Creating column {}".format(ytd))
    query = "ALTER TABLE {} ADD COLUMN `{}` {} DEFAULT {} AFTER ID_NODE;".format(tabla, ytd, tipo, default)
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()
    print("¡Column created!")
    print("")

def delete_column(tabla, fecha):
    query = "ALTER TABLE {} DROP COLUMN `{}`;".format(tabla, fecha)
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()

def autocomplete_null(tabla, ytd, value):
    cursor = mydb.cursor()
    if tabla == 'PERIOD':
        query = "UPDATE {} SET `{}` = '{}' WHERE `{}` = Null;".format(tabla, ytd, value, ytd)
    else:
        query = "UPDATE {} SET `{}` = {} WHERE `{}` = Null;".format(tabla, ytd, value, ytd)
    cursor.execute(query)
    mydb.commit()

def upload(date, cookie):

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

    for bool in ['NEW_HOURS', 'NEW_QOE', 'PERIOD', 'AFECTED_DAYS']:

        query0 = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(bool, ytd)

        cursor = mydb.cursor()
        cursor.execute(query0)
        result = cursor.fetchall()
        
        if result[0][0] == 1:
            print("Column {} already exists in {} table".format(ytd, bool))
            return {"msg": "Ya existe data cargada en {}".format(ytd)}
        
    create_column('NEW_HOURS', ytd, 'FLOAT', -1)
    create_column('NEW_QOE', ytd, 'FLOAT', -1)
    create_column('PERIOD', ytd, 'VARCHAR(20)', "'NO AFECTADO'")
    create_column('AFECTED_DAYS', ytd, 'INT(1)', 0)


    for node in lima_nodes:
        link = 'http://{}/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(url_ext ,str(node["nodeId"]), my_date.year, str(my_date.month).zfill(2), str(my_date.day + 1).zfill(2))
        try:
        #if True:
            mydata = requests.get(link)

            if mydata.status_code == 200:
                mydata = mydata.content
                mydata = json.loads(mydata)
                
                if mydata == []:
                    print(node["name"], "200 - Without data")
                    print(link)
                    value = -1
                    value_period = "NO DATA"
                    value_afected = 0

                    insert_value('NEW_HOURS', ytd, value, node["name"])
                    insert_value('NEW_QOE', ytd, value, node["name"])
                    insert_value('PERIOD', ytd, value_period, node["name"])
                    insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])

                else:
                    print(node["name"], "200 - OK")
                    print(link)

                    # HORAS QOE AFECTADO Y PERIODO DE AFECTACIÓN
                    counter = 0
                    period = []
                    for i in mydata:
                        if i["qoeScore"] < min_qoe:
                            counter = counter + 1
                            ts = i["timestamp"]
                            hour = int((dt.datetime(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13])) - dt.timedelta(hours=5)).strftime("%H"))
                            if hour > 17:
                                period.append("NOCHE")
                            elif hour > 8:
                                period.append("DIA")

                    hours = (counter*15)/60
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

                    # QOE PROMEDIO
                    scores = []
                    for j in mydata:
                        scores.append(j["qoeScore"])
                    qoe = round(sum(scores)/len(scores), 0)

                    # DIAS AFECTADO
                    value_afected = 0
                    if (qoe < min_qoe and qoe >= 0) or hours > min_afected_hours:
                        value_afected = 1
                    
                    insert_value('NEW_HOURS', ytd, hours, node["name"])
                    insert_value('NEW_QOE', ytd, qoe, node["name"])
                    insert_value('PERIOD', ytd, value_period, node["name"])
                    insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])
                
            elif mydata.status_code == 500:
                print(node["name"], "500 - Internal Error Server")
                print(link)
                value = -1
                value_period = "NO DATA"
                value_afected = 0

                insert_value('NEW_HOURS', ytd, value, node["name"])
                insert_value('NEW_QOE', ytd, value, node["name"])
                insert_value('PERIOD', ytd, value_period, node["name"])
                insert_value('AFECTED_DAYS', ytd, value_afected, node["name"])

        except:
        #else:
            print("Error connecting with Xpertrak")
            delete_column("NEW_HOURS", ytd)
            delete_column("NEW_QOE", ytd)
            delete_column("PERIOD", ytd)
            delete_column("AFECTED_DAYS", ytd)
            return {"msg": "Error en la conexión con Xpertrak"}

    


    print("======== ¡SUCCESS! ========")
    return {"msg":"Carga subida con éxito"}