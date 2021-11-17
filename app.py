from flask import Flask, render_template, request, jsonify, url_for, redirect
from maindb import algorithm
import requests

app = Flask(__name__)

@app.route('/hours')
def hours():
    return render_template('sumary.html', title = "Horas con QoE bajo", x = 'HOURS')

@app.route('/qoe')
def qoe():
    return render_template('sumary.html', title = "Estado diario QoE", x = 'QOE')

@app.route('/detail/<string:node>')
def detail(node):
    days = 1

    data_hours = algorithm(node, days, 'HOURS', True)
    values_hours = (((data_hours["data"])[0])[0])[node]

    data_qoe = algorithm(node, days, 'QOE', True)
    values_qoe = (((data_qoe["data"])[0])[0])[node]

    return render_template('detail.html', node = node, data_values = [values_hours, values_qoe], dates = (data_hours["data"])[1])

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', title = "Carga de data")
    elif request.method == 'POST':
        type = request.form["type"]
        date = request.form["date"]
        # FALTA LLAMAR A LA FUNCIÓN
        
        if date == "":
            return {"data": "no date"}
        return {"data": "Data subida exitosamente"}

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
    app.run(debug=True, port=8080)