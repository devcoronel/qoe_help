import json, requests
import datetime as dt
from lima_nodes import lima_nodes
from upload import mydb, min_qoe
import re

def algorithm(my_node, my_days, x):
    match = []

    try:
        my_node = str(my_node).upper()
        my_days = int(my_days)
        days = my_days
        if my_days == 0: #or my_node == '':
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
    dates = []
    value_nodes = []
    
    for day in range(days+1):
        dates.append((today - dt.timedelta(days = day)).strftime("%d/%m/20%y"))
    dates.pop(0)

    for node in match:
        value_node = []

        string = "SELECT "
        for date in dates:
            string = string + "`"+ date + "`,"
        string = string[:-1]
        string = string + " FROM {} WHERE PLANO = '{}';".format(x, node["name"])

        cursor = mydb.cursor()
        print(string)
        cursor.execute(string)
        result = cursor.fetchall()
        for value in result[0]:
            value_node.append(value)

        value_nodes.append({node["name"] : value_node})
    
    return {"data": [value_nodes, dates]}

    # today_utc = dt.datetime.utcnow()
    # today = today_utc - dt.timedelta(hours=5)
    # duration_today = (today.hour)*60 + today.minute

    # def create_link(nodeid, duration, date):
    #     link = 'http://190.117.108.84:1380/pathtrak/api/node/{}/qoe/metric/history?duration={}&sampleResponse=false&startdatetime={}-{}-{}T{}:{}:00.000Z'.format(nodeid, duration, date.year, str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2), str(date.minute).zfill(2))
    #     return link

    # link = create_link(node["nodeId"], duration_today, today_utc)

    # data = requests.get(link)
    # if data.status_code == 200:
    #     data = data.content
    #     data = json.loads(data)
    #     counter = 0

    #     for j in data:
    #         if j["qoeScore"] < min_qoe:
    #             counter = counter + 1
  
    #     hours_day = (counter*15)/60
    #     hours_node.append(hours_day)
    # hours_nodes.append({node["name"] : hours_node})