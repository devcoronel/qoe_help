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

def init(x): # x puede ser 'HOURS', 'QOE'
    try:
        lima_nodes = get_nodes()
        for node in lima_nodes:
            print(node["name"])
            query = "INSERT INTO {} (PLANO) VALUES ('{}');".format(x, node["name"])
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
        return print("======== ¡SUCCESS! ========")
    except:
        return print("Error")

def upload(x):  # x puede ser 'HOURS', 'QOE' o 'BOTH'

    lima_nodes = get_nodes()

    today_utc = dt.datetime.utcnow()
    today_local = today_utc - dt.timedelta(hours= 5)
    yesterday_local = today_local - dt.timedelta(days=1)
    ytd = yesterday_local.strftime("%d/%m/20%y")
    # ytd = '12/11/2021'

    ytd_utc = today_local - dt.timedelta(hours=today_local.hour - 5, minutes=today_local.minute)

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
            return print("Column {} already exists".format(ytd))
        
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
                return print("Column {} already exists in {} table".format(ytd, bool))
            
            print("Creating column {}".format(ytd))
            query1 = "ALTER TABLE {} ADD COLUMN `{}` FLOAT AFTER PLANO;".format(bool, ytd)
            cursor = mydb.cursor()
            cursor.execute(query1)
            mydb.commit()
            print("¡Column created!")
            print("")
    else:
       return print("Error typing HOURS, QOE or BOTH")


    for node in lima_nodes:
        link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(str(node["nodeId"]), ytd_utc.year, str(ytd_utc.month).zfill(2), str(ytd_utc.day).zfill(2), str(ytd_utc.hour).zfill(2), str(ytd_utc.minute).zfill(2))
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
            return print("Error connecting with Xpertrak")

    return print("======== ¡SUCCESS! ========")
