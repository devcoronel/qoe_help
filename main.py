import json, requests
import datetime as dt
from datetime import datetime, timedelta
from nodes import nodes
import re

def get_urls(my_node, my_days):
  urls_for_all_nodes = []
  urls_for_each_node = []
  match = []

  try:
    my_node = str(my_node).upper()
    my_days = int(my_days)
    days = my_days
    if my_node == '' or my_days == 0:
        return "Dato(s) incorrectos"
    regex = re.escape(my_node) + r"\w*"
    for node in nodes:
      if re.search(regex, node["name"], re.IGNORECASE):
        match.append(node)    
    if match == []:
      return "Plano(s) no encontrado(s)"
  except:
    return "Dato(s) incorrectos"
  
  today_utc = dt.datetime.utcnow()
  today = today_utc - dt.timedelta(hours=5)

  duration_day = 1440 #minutes: máximo 1440 (24 horas)
  duration_today = (today.hour)*60 + today.minute

  def url_built(node, built_day, duration):
    urls_for_each_node.append('http://190.117.108.84:1380/pathtrak/api/node/'+str(node["nodeId"])+'/qoe/metric/history?duration='+ str(duration) + '&sampleResponse=false&startdatetime=' + str(built_day.year)+'-'+str(built_day.month).zfill(2)+'-'+str(built_day.day).zfill(2)+'T'+str(built_day.hour).zfill(2) +':'+ str(built_day.minute).zfill(2)+':'+'00.000Z')

  for node in match:
    for day in range(days):
      if day == 0:
        url_built(node, today_utc, duration_today)
      else:
        url_built(node, today_utc-dt.timedelta(days=day-1, hours=today.hour, minutes= today_utc.minute), duration_day)
    urls_for_all_nodes.append({node['name']:urls_for_each_node})
    urls_for_each_node = []
  
  return [urls_for_all_nodes, (today).strftime("%d/%m/%y")]

# ONE OR MORE NODES ANALITIC
def sumary(urls):
  if isinstance(urls, str):
    return urls

  urls_for_all_nodes = urls[0]
  today = urls[1]
  hours_nodes = []
  min_qoe = 80

  for node in urls_for_all_nodes:
    name_node = list(node.keys())[0]
    url_node = node[name_node]
    hours_node = []

    for i in url_node:
      data = requests.get(i)

      if data.status_code == 200:
        data = data.content
        data = json.loads(data)
        counter = 0

        for j in data:
          if j["qoeScore"] < min_qoe:
            counter = counter + 1
        
        hours_day = (counter*15)/60
        hours_node.append(hours_day)

    hours_nodes.append({name_node : hours_node})  
  return [hours_nodes, today]

# ONE NODE ANALITIC
def details(urls):
  if isinstance(urls, str):
    return urls

  urls_node = urls[0]
  today = urls[1]

  name_node = list(urls_node[0].keys())[0]
  urls_node = (urls_node[0])[name_node]
  days_report = []
  min_qoe = 80

  for i in urls_node:
    data = requests.get(i)

    if data.status_code == 200:
      data = data.content
      data = json.loads(data)
      counter = 0
      qoe_consecutives = []
      day_report = []

      # Dia por iteración
      #print((today - dt.timedelta(days = urls_node.index(i))).strftime("%d/%m/%y"))

      for j in data:

        if j["qoeScore"] < min_qoe:
          counter = counter + 1
          qoe_consecutives.append(j["qoeScore"])

          if data.index(j) == len(data) - 1:
            time = (counter * 15)/60
            start = datetime.strptime(j["timestamp"], '%Y-%m-%dT%H:%M:%SZ') - dt.timedelta(hours=5, minutes=-15)
            end = start + dt.timedelta(minutes = counter * 15)
            average = round(sum(qoe_consecutives)/len(qoe_consecutives))
            day_report.append([time, average, start.strftime("%H:%M"), end.strftime("%H:%M")])

            counter = 0
            qoe_consecutives = []

        else:
          if counter != 0:
            time = (counter * 15)/60
            start = datetime.strptime(j["timestamp"], '%Y-%m-%dT%H:%M:%SZ') - dt.timedelta(hours=5, minutes=-15)
            end = start + dt.timedelta(minutes = counter * 15)
            average = round(sum(qoe_consecutives)/len(qoe_consecutives))
            day_report.append([time, average, start.strftime("%H:%M"), end.strftime("%H:%M")])

            counter = 0
            qoe_consecutives = []
      
      days_report.append(day_report)
  return [days_report, today]

#print(sumary(get_urls('lamo015', 3)))
#print(details(get_urls('lamo015', 3)))
#print(get_urls('lmlo00', 1)[1])