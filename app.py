from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import get_urls, sumary, details
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
    return render_template('detail.html', node = node)

@app.route('/info')
def indexe():
    return render_template('index.html')

@app.route('/hours', methods=['POST'])
def data_hours():
    node = request.form['node']
    days = request.form['days']
    data = algorithm(node, days, 'HOURS')
    return data

@app.route('/qoe', methods=['POST'])
def data_qoe():
    node = request.form['node']
    days = request.form['days']
    data = algorithm(node, days, 'QOE')
    return data

if __name__ == '__main__':
    app.run(debug=True, port=8080)