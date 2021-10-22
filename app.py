from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
from main import analitics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def send_data():
    node = request.form['node']
    days = request.form['days']

    return render_template('index.html', data = analitics(node, days))

if __name__ == '__main__':
    app.run(debug=True, port=4000)