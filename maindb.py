import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from upload import mydb, min_qoe
import re

# AGREGAR VARIABLE ONLY_ONE PARA QUE EN EL MATCH ACEPTE SOLO 1 O VARIOS
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
    
    if only_one == True and len(match) != 1:
        return {"msg": "Se necesita especificar solo un plano"}
    
    def create_link(nodeid, duration, date):
        link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
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
    
    for node in match:
        value_node = []
        if also_today:
            link = create_link(node["nodeId"], duration_today, today_utc)
            
            data = requests.get(link)
            if data.status_code == 200:
                data = data.content
                data = json.loads(data)

                if data == []:
                    value_node.append("Null")
                
                if x == 'HOURS':
                    counter = 0
                    for j in data:
                        if j["qoeScore"] < min_qoe:
                            counter = counter + 1
                    hours = (counter*15)/60
                    value_node.append(hours)
                
                elif x == 'QOE':
                    scores = []
                    for j in data:
                        scores.append(j["qoeScore"])
                    qoe = round(sum(scores)/len(scores), 0)
                    value_node.append(qoe)
                
                else:
                    return print("Error typing HOURS or QOE")
            
            else:
                value_node.append("Null")

        query1 = "SELECT "
        for date in dates:
            query1 = query1 + "`"+ date + "`,"
        query1 = query1[:-1]
        query1 = query1 + " FROM {} WHERE PLANO = '{}';".format(x, node["name"])

        cursor = mydb.cursor()
        cursor.execute(query1)
        result = cursor.fetchall()
        for value in result[0]:
            value_node.append(value)

        value_nodes.append({node["name"] : value_node})

        if also_today:    
            dates.insert(0, today.strftime("%d/%m/20%y"))

    
    return {"msg": [value_nodes, dates]}
