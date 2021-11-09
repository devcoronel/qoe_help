from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import get_urls, sumary, details
import requests

app = Flask(__name__)

@app.route('/sumario')
def index():
    return render_template('sumary.html')

@app.route('/detalle/<string:node>/<int:days>')
def detail(node, days):
    return render_template('detail.html', node = node)

@app.route('/info')
def indexe():
    return render_template('index.html')

@app.route('/sumario', methods=['POST'])
def send_data():
    node = request.form['node']
    days = request.form['days']
    data = sumary(get_urls(node, days))

    return data

if __name__ == '__main__':
    app.run(debug=True, port=8080)