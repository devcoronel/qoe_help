from concurrent import futures
import concurrent
from datetime import date
import re
from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import detail, dayly, insert_status, priority, modulation, analysis, status_node, sampling
from up import upload, verify_upload
from constants import days_detail, days_modulation
from xpertrak_login import get_cookie
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from decorator import when_upload_runs

import threading

from multiprocessing.dummy import Pool
from multiprocessing.pool import ThreadPool
import concurrent.futures

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


@app.route('/analysis', methods = ['POST'])
@limiter.limit("1/2second")
@when_upload_runs
def my_post_qoe():
    region = request.form['region']
    parameter = request.form['type']
    node = request.form['node']
    days = request.form['days']
    data = analysis(node, days, parameter, region)
    return {'msg': data}


@app.route('/analysis', methods = ['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_qoe():
    return render_template('index.html', route = 0)


@app.route(r'/detail', methods = ['POST'])
@limiter.limit("1/2second")
@when_upload_runs
def my_post_detail():
    node = request.form["node"].upper()
    days = request.form["days"]

    data_hours = detail(node, days, 'NEW_HOURS')
    data_qoe = detail(node, days, 'NEW_QOE')
    data_period = detail(node, days, 'PERIOD')
    data_modul = detail(node, days, 'MODULATION')
    data_impacted = detail(node, days, 'IMPACTEDMODEMS')
    data_stressed = detail(node, days, 'STRESSEDMODEMS')
    data_sampling = detail(node, days, 'SAMPLING')

    if isinstance(data_hours["msg"], str):
        return data_hours
    elif isinstance(data_hours["msg"], list):

        values_hours = (((data_hours["msg"])[0])[0])[node]
        values_qoe = (((data_qoe["msg"])[0])[0])[node]
        values_period = (((data_period["msg"])[0])[0])[node]
        values_modul = (((data_modul["msg"])[0])[0])[node]
        values_impacted = (((data_impacted["msg"])[0])[0])[node]
        values_stressed = (((data_stressed["msg"])[0])[0])[node]
        values_sampling = (((data_sampling["msg"])[0])[0])[node]

        data_values = [values_hours, values_qoe, values_period, values_modul, values_impacted, values_stressed, values_sampling]
        dates = (data_hours["msg"])[1]

        status = status_node(node)
        
        return {"msg":[node, data_values, dates, status]}


@app.route(r'/detail', methods = ['GET'])
@app.route(r'/detail/<string:node>', methods = ['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_detail(node = None):
    if node:
        with_search = False
        days = days_detail

        data_hours = detail(node, days, 'NEW_HOURS')
        values_hours = (((data_hours["msg"])[0])[0])[node]

        data_qoe = detail(node, days, 'NEW_QOE')
        values_qoe = (((data_qoe["msg"])[0])[0])[node]
            
        data_period = detail(node, days, 'PERIOD')
        values_period = (((data_period["msg"])[0])[0])[node]

        data_modul = detail(node, days, 'MODULATION')
        values_modul = (((data_modul["msg"])[0])[0])[node]

        data_impacted = detail(node, days, 'IMPACTEDMODEMS')
        values_impacted = (((data_impacted["msg"])[0])[0])[node]

        data_stressed = detail(node, days, 'STRESSEDMODEMS')
        values_stressed = (((data_stressed["msg"])[0])[0])[node]

        data_sampling = detail(node, days, 'SAMPLING')
        values_sampling = (((data_sampling["msg"])[0])[0])[node]

        status = status_node(node)

        return render_template('index.html', route = 1, node = node, data_values = [values_hours, values_qoe, values_period, values_modul, values_impacted, values_stressed, values_sampling], dates = (data_hours["msg"])[1], status = status, with_search = with_search)

    else:
        with_search = True
        return render_template('index.html', route = 1, with_search = with_search)
    

@app.route('/priority', methods=['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_priority():
    data = priority("LIMA")
    return render_template('index.html', route = 2, data = {'msg': data})


@app.route('/priority', methods=['POST'])
@limiter.limit("1/second")
@when_upload_runs
def my_post_priority():
    region = request.data
    region = (str(region, 'UTF-8'))[1:-1]
    data = priority(region)
    return {'msg': data}
    

@app.route('/modulation', methods=['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_modulation():
    data = modulation("LIMA")
    return render_template('index.html', route = 3, data = {'msg': data})


@app.route('/modulation', methods=['POST'])
@limiter.limit("1/second")
@when_upload_runs
def my_post_modulation():
    region = request.data
    region = (str(region, 'UTF-8'))[1:-1]
    data = modulation(region)
    return {'msg': data}
    

@app.route('/upload', methods=['POST', 'GET'])
@limiter.limit("2/second")
@when_upload_runs
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
            verify_result = verify_upload(date, cookie)

            if isinstance(verify_result, list):
                
                try:
                    process = upload(verify_result[0], verify_result[1], verify_result[2])
                    return process
                except:
                    return {"msg": "Error en la Conexión con Xpertrak"}

            else:
                return verify_result
        
        elif action == 'delete':
            pass


@app.route('/dayly', methods = ['POST'])
@limiter.limit("1/2second")
@when_upload_runs
def my_post_dayly():
    region = request.form["region"]
    date = request.form["dayly_date"]
    
    if date == '':
        return {'msg': 'No se ha especificado ninguna fecha'}
    else:
        data = dayly(date, region)
        return {'msg': data}


@app.route('/dayly', methods = ['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_dayly():
    return render_template('index.html', route = 5)


@app.route('/sampling', methods = ['GET'])
@limiter.limit("2/second")
@when_upload_runs
def my_sampling():
    data_sampling = sampling("LIMA")
    return render_template('index.html', route = 8, data = {'msg': data_sampling})


@app.route('/sampling', methods = ['POST'])
@limiter.limit("1/second")
@when_upload_runs
def my_post_sampling():
    region = request.data
    region = (str(region, 'UTF-8'))[1:-1]
    data = sampling(region)
    return {'msg': data}


@app.route('/info')
@limiter.limit("2/second")
@when_upload_runs
def my_info():
    return render_template('index.html', route = 6)


@app.route('/status', methods=['POST'])
@limiter.limit("1/2second")
@when_upload_runs
def status():
    node = request.form["pla"].upper()
    dependence = request.form["dep"]
    impediment = request.form["imp"]
    problem_type = request.form["tip"]
    problem = request.form["pro"]
    state = request.form["est"]
    revision = request.form["rev"]
    detail = request.form["det"]

    if node == '' or revision == '':
        return {'msg': 'Faltan datos por completar'}
    else:
        try:
            result = insert_status(dependence, impediment, revision, problem_type, problem, state, detail, node)
            return result
        except:
            return {'msg': 'Error en la conexión con la base de datos'}


if __name__ == '__main__':
    # app.run(port=8080, debug=False)
    app.run(host= "0.0.0.0", port=8080, debug=False)