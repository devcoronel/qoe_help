import mysql.connector
import datetime as dt
import json
import requests
from lima_nodes import lima_nodes

mydb = mysql.connector.connect(
  host="192.168.0.32",
  user="diego_remote",
  password="",
  database = "qoehelp",
  auth_plugin='mysql_native_password' # Define la autenticación que tendrá con la base de datos
  # Se puede verificar en la base de datos con SELECT HOST, USER, PLUGIN FROM MYSQL.USER;
  # Fuente: https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported
)
# commmit para ejecutar cambios
# fetchall para obtener la salida del comando
min_qoe = 80

def init():
    for node in lima_nodes:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO HOURS (PLANO) VALUES (%s);", [node["name"]])
        mydb.commit()

def data():
    today_utc = dt.datetime.utcnow()
    ytd_utc = today_utc - dt.timedelta(days = 1, hours= today_utc.hour-5, minutes= today_utc.minute)
    ytd = (today_utc - dt.timedelta(days=1, hours= 5)).strftime("%d/%m/20%y")
    lima_data = []

    cursor = mydb.cursor()
    cursor.execute("""
    ALTER TABLE HOURS
    ADD COLUMN `%s` FLOAT
    AFTER PLANO;
    """, [ytd])

    for node in lima_nodes:
        link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration=1440&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(str(node["nodeId"]), ytd_utc.year, str(ytd_utc.month).zfill(2), str(ytd_utc.day).zfill(2), str(ytd_utc.hour).zfill(2), str(ytd_utc.minute).zfill(2))
        mydata = requests.get(link)

        if mydata.status_code == 200:
            mydata = mydata.content
            mydata = json.loads(mydata)
            counter = 0

            for i in mydata:
                if i["qoeScore"] < min_qoe:
                    counter = counter + 1
                
            hours = (counter*15)/60
            lima_data.append({node["name"]:hours})
        
        cursor = mydb.cursor()
        cursor.execute("""
        UPDATE HOURS
        SET `%s` = %s
        WHERE PLANO = %s;
        """, [ytd, hours, node["name"]])
        mydb.commit()

    #print(lima_data)
            

def upload():
    today_utc = dt.datetime.utcnow()
    today = (today_utc - dt.timedelta(hours=5)).strftime("%d/%m/20%y")

    cursor = mydb.cursor()
    cursor.execute(""" 
    SELECT * FROM HOURS;
    """)
    result = cursor.fetchall()
    print(result)

#init()  
data()
# upload()