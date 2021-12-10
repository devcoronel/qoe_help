from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import algorithm, dayly, priority, modulation
from up import upload, verify_upload
from constants import days_detail, days_modulation
from xpertrak_login import get_cookie
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.errorhandler(429)
def error_429(error):
    return render_template('error.html', number = 429)

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', number = 404)

@app.errorhandler(500)
def error_500(error):
    return render_template('error.html', number = 500)


@app.route('/analysis', methods = ['GET', 'POST'])
@limiter.limit("2/second")
def qoe():
    if request.method == 'GET':
        return render_template('index.html', route = 0)

    elif request.method == 'POST':
        parameter = request.form['type']
        node = request.form['node']
        days = request.form['days']
        data = algorithm(node, days, parameter, False)
        return data


@app.route(r'/detail', methods = ['GET', 'POST'])
@app.route(r'/detail/<string:node>', methods = ['GET'])
@limiter.limit("2/second")
def detail(node = None):
    if request.method == 'GET':
        if node:
            with_search = False
            days = days_detail

            data_hours = algorithm(node, days, 'NEW_HOURS', True, True)
            values_hours = (((data_hours["msg"])[0])[0])[node]

            data_qoe = algorithm(node, days, 'NEW_QOE', True, True)
            values_qoe = (((data_qoe["msg"])[0])[0])[node]
            
            data_period = algorithm(node, days, 'PERIOD', True, True)
            values_period = (((data_period["msg"])[0])[0])[node]

            data_modul = algorithm(node, days, 'MODULATION', True, True)
            values_modul = (((data_modul["msg"])[0])[0])[node]

            return render_template('index.html', route = 1, node = node, data_values = [values_hours, values_qoe, values_period, values_modul], dates = (data_hours["msg"])[1], with_search = with_search)

        else:
            with_search = True
            return render_template('index.html', route = 1, with_search = with_search)
    
    elif request.method == 'POST':

        node = request.form["node"].upper()
        days = request.form["days"]

        data_hours = algorithm(node, days, 'NEW_HOURS', True, True)
        data_qoe = algorithm(node, days, 'NEW_QOE', True, True)
        data_period = algorithm(node, days, 'PERIOD', True, True)
        data_modul = algorithm(node, days, 'MODULATION', True, True)

        if isinstance(data_hours["msg"], str):
            return data_hours
        elif isinstance(data_hours["msg"], list):

            values_hours = (((data_hours["msg"])[0])[0])[node]
            values_qoe = (((data_qoe["msg"])[0])[0])[node]
            values_period = (((data_period["msg"])[0])[0])[node]
            values_modul = (((data_modul["msg"])[0])[0])[node]

            data_values = [values_hours, values_qoe, values_period, values_modul]
            dates = (data_hours["msg"])[1]
            
            return {"msg":[node, data_values, dates]}
        else:
            pass

@app.route('/priority', methods=['POST', 'GET'])
@limiter.limit("2/second")
def my_priority():
    if request.method == 'GET':
        data = priority()
        return render_template('index.html', route = 2, data = {'msg': data})
    
    elif request.method == 'POST':
        
        return 0

@app.route('/modulation')
@limiter.limit("2/second")
def my_modulation():
    data = modulation()
    return render_template('index.html', route = 3, data = {'msg': data})
    

@app.route('/upload', methods=['POST', 'GET'])
@limiter.limit("2/second")
def my_upload():
    if request.method == 'GET':
        return render_template('index.html', route = 4, title = "Carga de data")

    elif request.method == 'POST':
        action = request.form["action"]
        date = request.form["date"]

        if date == "":
            return {"msg": "Especifique la fecha para la carga"}

        if action == 'upload':
            cookie = get_cookie()
            result = verify_upload(date, cookie)

            if isinstance(result, list):
                process = upload(result[0], result[1], result[2])
                return process

            else:
                return result
        
        elif action == 'delete':
            pass

@app.route('/dayly', methods = ['GET', 'POST'])
@limiter.limit("1/2second")
def my_dayly():
    if request.method == 'GET':
        return render_template('index.html', route = 5)
    elif request.method == 'POST':
        date = request.form["date"]
        data = dayly(date)
        return {'msg': data}

@app.route('/info')
@limiter.limit("2/second")
def indexe():
    return render_template('index.html', route = 6)


if __name__ == '__main__':
    app.run(host= "0.0.0.0", port=8080, debug=False)

# CREAR PÁGINA PARA POWER BI