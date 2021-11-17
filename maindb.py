import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from upload import mydb, min_qoe
import re

def algorithm(my_node, my_days, x, also_today): # x only can be 'HOURS' or 'QOE'
    match = []

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
    
    today_utc = dt.datetime.utcnow()
    today = today_utc - dt.timedelta(hours=5)
    duration_today = (today.hour)*60 + today.minute
    dates = []
    value_nodes = []

    def create_link(nodeid, duration, date):
        link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
        return link
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)

    for node in match:
        value_node = []
        if also_today:
            link = create_link(node["nodeId"], duration_today, today_utc)
            
            data = requests.get(link)
            if data.status_code == 200:
                data = data.content
                data = json.loads(data)
                
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

        string = "SELECT "
        for date in dates:
            string = string + "`"+ date + "`,"
        string = string[:-1]
        string = string + " FROM {} WHERE PLANO = '{}';".format(x, node["name"])

        cursor = mydb.cursor()
        cursor.execute(string)
        result = cursor.fetchall()
        for value in result[0]:
            value_node.append(value)

        value_nodes.append({node["name"] : value_node})

        if also_today:    
            dates.insert(0, today.strftime("%d/%m/20%y"))

    
    return {"data": [value_nodes, dates]}
