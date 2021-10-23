from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
from main import get_urls, sumary, details

app = Flask(__name__)

@app.route('/sumario')
def index():
    return render_template('sumary.html')

@app.route('/detalle')
def indexa():
    return render_template('contactme.html')

@app.route('/info')
def indexe():
    return render_template('contactme.html')

@app.route('/sumario', methods=['POST'])
def send_data():
    node = request.form['node']
    days = request.form['days']
    print(node)
    print(days)

    return {"msg": sumary(get_urls(node, days))}

if __name__ == '__main__':
    app.run(debug=True, port=8080)