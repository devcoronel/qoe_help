from datetime import date
from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import algorithm
from up import upload
import requests

app = Flask(__name__)

@app.route('/hours', methods = ['GET', 'POST'])
def hours():
    if request.method == 'GET':
        return render_template('sumary.html', title = "Horas con QoE bajo", x = 'NEW_HOURS')
    elif request.method == 'POST':
        node = request.form['node']
        days = request.form['days']
        data = algorithm(node, days, 'NEW_HOURS', False)
        return data

@app.route('/qoe', methods = ['GET', 'POST'])
def qoe():
    if request.method == 'GET':
        return render_template('sumary.html', title = "Estado diario QoE", x = 'NEW_QOE')
    elif request.method == 'POST':
        node = request.form['node']
        days = request.form['days']
        data = algorithm(node, days, 'NEW_QOE', False)
        return data

@app.route(r'/detail', methods = ['GET', 'POST'])
@app.route(r'/detail/<string:node>', methods = ['GET'])
def detail(node = None):
    if request.method == 'GET':
        if node:
            with_search = False
            days = 14

            data_hours = algorithm(node, days, 'NEW_HOURS', True)
            values_hours = (((data_hours["msg"])[0])[0])[node]

            data_qoe = algorithm(node, days, 'NEW_QOE', True)
            values_qoe = (((data_qoe["msg"])[0])[0])[node]

            return render_template('detail.html', node = node, data_values = [values_hours, values_qoe], dates = (data_hours["msg"])[1], with_search = with_search)

        else:
            with_search = True
            return render_template('detail.html', with_search = with_search)
    
    elif request.method == 'POST':

        node = request.form["node"].upper()
        days = request.form["days"]

        data_hours = algorithm(node, days, 'NEW_HOURS', True, True)
        data_qoe = algorithm(node, days, 'NEW_QOE', True, True)
        print(data_hours)


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

@app.route('/priority', methods=['POST', 'GET'])
def priority():
    if request.method == 'GET':
        # Se tiene que pasar los datos para GET
        return render_template('priority.html')
    elif request.method == 'POST':
        # Tener un botón de actualizar
        # Tener un div (antes de la tabla HTML) que tenga un id para construir una tabla por JS
        # Se necesita editar tabla
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
        
        result = upload(date, cookie)
        
        return result

@app.route('/info')
def indexe():
    return render_template('index.html')

# @app.route('/hours', methods=['POST'])
# def data_hours():
#     node = request.form['node']
#     days = request.form['days']
#     data = algorithm(node, days, 'NEW_HOURS', False)
#     return data

# @app.route('/qoe', methods=['POST'])
# def data_qoe():
#     node = request.form['node']
#     days = request.form['days']
#     data = algorithm(node, days, 'NEW_QOE', False)
#     return data

if __name__ == '__main__':
    app.run(debug=False, port=8080)

# OBENER COOKIES AUTOMÁTICAMENTE
# DAR DETALLE DE US, DS, T3
# CREAR PÁGINA PARA POWER BI

# QOE > 80 AND SHOW HOURS QOE