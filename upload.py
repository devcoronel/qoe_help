import mysql.connector
import datetime as dt
import json
import requests
from requests.exceptions import RetryError
from built_nodes import get_nodes

mydb = mysql.connector.connect(
    host="192.168.0.32",
    user="diego_remote",
    password="Mysqldiego10",
    database = "qoehelp",
    auth_plugin='mysql_native_password' # Define la autenticación que tendrá con la base de datos
    # Se puede verificar en la base de datos con SELECT HOST, USER, PLUGIN FROM MYSQL.USER;
    # Fuente: https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
)
# commmit para ejecutar cambios
# fetchall para obtener la salida del comando
min_qoe = 80

def init(x, cookie): # x puede ser 'HOURS', 'QOE' o 'BOTH'
    try:
        lima_nodes = get_nodes(cookie)
        if x == 'HOURS' or x == 'QOE':
            for node in lima_nodes:
                print(node["name"])
                query = "INSERT INTO {} (PLANO) VALUES ('{}');".format(x, node["name"])
                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
            return print("======== ¡SUCCESS! ========")

        elif x == 'BOTH':
            for node in lima_nodes:
                print(node["name"])

                for i in ['HOURS', 'QOE']:
                    query = "INSERT INTO {} (PLANO) VALUES ('{}');".format(i, node["name"])
                    cursor = mydb.cursor()
                    cursor.execute(query)
                    mydb.commit()
            return print("======== ¡SUCCESS! ========")
            
        else:
            return print("Error typing HOURS, QOE or BOTH")

    except:
        return print("Error")

def upload(x, date, cookie):  # x puede ser 'HOURS', 'QOE' o 'BOTH'

    today = dt.datetime.utcnow() - dt.timedelta(hours=5)
    my_date = dt.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
    if my_date > today:
        return {"msg":"No hay data para esta fecha"}
    elif my_date.strftime("%d/%m/20%y") == today.strftime("%d/%m/20%y"):
        return {"msg":"Todavía no hay data para esta fecha"}
    else:
        pass

    ytd = my_date.strftime("%d/%m/20%y")

    if x == 'HOURS' or x == 'QOE':

        query0 = """
        SELECT IF ( EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'),1,0);
        """.format(x, ytd)

        cursor = mydb.cursor()
        cursor.execute(query0)
        result = cursor.fetchall()

        if result[0][0] == 1:
            print("Column {} already exists".format(ytd))
            return {"msg": "Ya existe una data cargada en {}".format(ytd)}
        
        print("Creating column {}".format(ytd))
        query1 = "ALTER TABLE {} ADD COLUMN `{}` FLOAT AFTER PLANO;".format(x, ytd)
        cursor = mydb.cursor()
        cursor.execute(query1)
        mydb.commit()
        print("¡Column created!")
        print("")
    
    elif x == 'BOTH':

        for bool in ['HOURS', 'QOE']:

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
                return {"msg": "Ya existe una data cargada en {} en la tabla {}".format(ytd, bool)}
            
            print("Creating column {}".format(ytd))
            query1 = "ALTER TABLE {} ADD COLUMN `{}` FLOAT AFTER PLANO;".format(bool, ytd)
            cursor = mydb.cursor()
            cursor.execute(query1)
            mydb.commit()
            print("¡Column created!")
            print("")
    else:
       return print("Error typing HOURS, QOE or BOTH")

    lima_nodes = get_nodes(cookie)
    if isinstance(lima_nodes, dict):
        return lima_nodes

    for node in lima_nodes:
        link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T05:00:00.000Z'.format(str(node["nodeId"]), my_date.year, str(my_date.month).zfill(2), str(my_date.day + 1).zfill(2))
        mydata = requests.get(link)

        if mydata.status_code == 200:
            mydata = mydata.content
            mydata = json.loads(mydata)
            
            if mydata == []:
                print(node["name"], "200 - Without data")
                print(link)
                value = -1

                if x == 'QOE' or x == 'HOURS':

                    cursor = mydb.cursor()
                    query2 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(x, ytd, value, node["name"])
                    cursor.execute(query2)
                    mydb.commit()

                elif x == 'BOTH':

                    for i in ['HOURS', 'QOE']:
                        cursor = mydb.cursor()
                        query2 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(i, ytd, value, node["name"])
                        cursor.execute(query2)
                        mydb.commit()
                
                else:
                    return print("Error typing HOURS, QOE or BOTH")

            elif x == 'HOURS':
                counter = 0
                for i in mydata:
                    if i["qoeScore"] < min_qoe:
                        counter = counter + 1
                print(node["name"], "200 - OK")
                print(link)             
                value = (counter*15)/60

                cursor = mydb.cursor()
                query2 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(x, ytd, value, node["name"])
                cursor.execute(query2)
                mydb.commit()
            
            elif x == 'QOE':
                scores = []
                for i in mydata:
                    scores.append(i["qoeScore"])
                print(node["name"], "200 - OK")
                print(link)
                value = round(sum(scores)/len(scores), 0)

                cursor = mydb.cursor()
                query2 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(x, ytd, value, node["name"])
                cursor.execute(query2)
                mydb.commit()

            elif x == 'BOTH':
                print(node["name"], "200 - OK")
                print(link)

                counter = 0
                for i in mydata:
                    if i["qoeScore"] < min_qoe:
                        counter = counter + 1            
                hours = (counter*15)/60

                scores = []
                for j in mydata:
                    scores.append(j["qoeScore"])
                qoe = round(sum(scores)/len(scores), 0)

                cursor = mydb.cursor()
                query3 = "UPDATE HOURS SET `{}` = {} WHERE PLANO = '{}';".format(ytd, hours, node["name"])
                cursor.execute(query3)
                mydb.commit()

                cursor = mydb.cursor()
                query4 = "UPDATE QOE SET `{}` = {} WHERE PLANO = '{}';".format(ytd, qoe, node["name"])
                cursor.execute(query4)
                mydb.commit()

            else:
                return print("Error typing HOURS, QOE or BOTH")
            
        elif mydata.status_code == 500:

            if x == 'HOURS' or x == 'QOE':
                print(node["name"], "500 - Internal Error Server")
                print(link)
                value = -1

                cursor = mydb.cursor()
                query5 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(x, ytd, value, node["name"])
                cursor.execute(query5)
                mydb.commit()

            elif x == 'BOTH':
                print(node["name"], "500 - Internal Error Server")
                print(link)
                value = -1

                for i in ['HOURS', 'QOE']:
                    cursor = mydb.cursor()
                    query6 = "UPDATE {} SET `{}` = {} WHERE PLANO = '{}';".format(i, ytd, value, node["name"])
                    cursor.execute(query6)
                    mydb.commit()
            
            else:
                return print("Error typing HOURS, QOE or BOTH")

        else:
            print("Error connecting with Xpertrak")
            return {"msg": "Error en la conexión con Xpertrak"}

    print("======== ¡SUCCESS! ========")
    return {"msg":"Carga subida con éxito"}
