from datetime import date
from flask import Flask, render_template, request, jsonify, url_for, redirect
from maindb import algorithm
from upload import upload
import requests

app = Flask(__name__)

@app.route('/hours')
def hours():
    return render_template('sumary.html', title = "Horas con QoE bajo", x = 'HOURS')

@app.route('/qoe')
def qoe():
    return render_template('sumary.html', title = "Estado diario QoE", x = 'QOE')

@app.route(r'/detail', methods = ['GET', 'POST'])
@app.route(r'/detail/<string:node>', methods = ['GET'])
def detail(node = None):
    if request.method == 'GET':
        if node:
            with_search = False
            days = 14

            data_hours = algorithm(node, days, 'HOURS', True)
            values_hours = (((data_hours["msg"])[0])[0])[node]

            data_qoe = algorithm(node, days, 'QOE', True)
            values_qoe = (((data_qoe["msg"])[0])[0])[node]

            return render_template('detail.html', node = node, data_values = [values_hours, values_qoe], dates = (data_hours["msg"])[1], with_search = with_search)

        else:
            with_search = True
            return render_template('detail.html', with_search = with_search)
    
    elif request.method == 'POST':

        node = request.form["node"].upper()
        days = request.form["days"]

        data_hours = algorithm(node, days, 'HOURS', True, True)
        data_qoe = algorithm(node, days, 'QOE', True, True)

        if isinstance(data_hours["msg"], str):
            return data_hours
        elif isinstance(data_hours["msg"], list):

            values_hours = (((data_hours["msg"])[0])[0])[node]
            values_qoe = (((data_qoe["msg"])[0])[0])[node]

            data_values = [values_hours, values_qoe]
            dates = (data_hours["msg"])[1]
            
            return {"msg":[node, data_values, dates]}
        else:
            pass

@app.route('/upload', methods=['POST', 'GET'])
def my_upload():
    if request.method == 'GET':
        return render_template('upload.html', title = "Carga de data")
    elif request.method == 'POST':
        election = request.form["type"]
        date = request.form["date"]
        cookie = request.form["cookie"]
        
        if date == "":
            return {"msg": "Especifique la fecha para la carga"}
        
        result = upload(election, date, cookie)
        
        return result

@app.route('/info')
def indexe():
    return render_template('index.html')

@app.route('/hours', methods=['POST'])
def data_hours():
    node = request.form['node']
    days = request.form['days']
    data = algorithm(node, days, 'HOURS', False)
    return data

@app.route('/qoe', methods=['POST'])
def data_qoe():
    node = request.form['node']
    days = request.form['days']
    data = algorithm(node, days, 'QOE', False)
    return data

if __name__ == '__main__':
    app.run(debug=False, port=8080)

# OBENER COOKIES AUTOMÁTICAMENTE
# DAR DETALLE DE US, DS, T3
# CREAR PÁGINA PARA POWER BI