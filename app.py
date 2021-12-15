from concurrent import futures
import concurrent
from flask import Flask, render_template, request, jsonify, url_for, redirect
from main import detail, dayly, priority, modulation, analysis
from up import prueba, upload, verify_upload, new_upload
from constants import days_detail, days_modulation
from xpertrak_login import get_cookie
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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


@app.route('/analysis', methods = ['GET', 'POST'])
@limiter.limit("2/second")
def my_qoe():
    if request.method == 'GET':
        return render_template('index.html', route = 0)

    elif request.method == 'POST':
        parameter = request.form['type']
        node = request.form['node']
        days = request.form['days']
        data = analysis(node, days, parameter)
        return {'msg': data}


@app.route(r'/detail', methods = ['POST'])
@limiter.limit("1/2second")
def my_post_detail():
    print("post")
    node = request.form["node"].upper()
    days = request.form["days"]

    data_hours = detail(node, days, 'NEW_HOURS')
    data_qoe = detail(node, days, 'NEW_QOE')
    data_period = detail(node, days, 'PERIOD')
    data_modul = detail(node, days, 'MODULATION')

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


@app.route(r'/detail', methods = ['GET'])
@app.route(r'/detail/<string:node>', methods = ['GET'])
@limiter.limit("2/second")
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

        return render_template('index.html', route = 1, node = node, data_values = [values_hours, values_qoe, values_period, values_modul], dates = (data_hours["msg"])[1], with_search = with_search)

    else:
        with_search = True
        return render_template('index.html', route = 1, with_search = with_search)
    

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
            verify_result = verify_upload(date, cookie)

            if isinstance(verify_result, list):
                # process = upload(verify_result[0], verify_result[1], verify_result[2])
                # return process

                try:
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(upload, (verify_result[0], verify_result[1], verify_result[2], ))
                    return_val = async_result.get()
    
                    return return_val
                except:
                    return {"msg": "Error en la Conexión con Xpertrak app"}
                # executor = concurrent.futures.ThreadPoolExecutor()
                # executor.submit(prueba)
                # print(executor.result())

                # try:
                #     with concurrent.futures.ThreadPoolExecutor() as executor:
                #         future = executor.submit(upload, verify_result[0], verify_result[1], verify_result[2])
                #         return_value = future.result()
                #     return return_value

                # except:
                #     return {"msg": "Error en la conexión con Xpertrak"}
                # thread = threading.Thread(target=upload, args=(result[0], result[1], result[2], ))
                # thread.start()
                # try:
                #     thread = threading.Thread(target=prueba)
                #     thread.start()
                #     print(thread)
                #     print(thread.get())
                #     return {"msg": "Correcto app"}

                # except:
                #     return {"msg": "Incorrecto app"}
                # process = upload(result[0], result[1], result[2])
                # return process

                # with ThreadPool(len(result[0])) as pool:
                #     res = pool.starmap(upload, zip(result[0], repeat(result[1]), repeat(result[2])))

                # SE PUEDE NAVEGAR SIN CRASHEAR EL PROGRAMA
                # pool = Pool()
                # pool.map([new_upload(node, result[1], result[2]) for node in result[0]])
                # pool.join()

                # SE PUEDE NAVEGAR SIN CRASHEAR EL PROGRAMA
                # with Pool() as pool:
                #     res = pool.map([new_upload(node, result[1], result[2]) for node in result[0]])

                # NO ACEPTA NAVEGAR LATERALMENTE
                # with Pool(len(result[0])) as pool:
                #     res = pool.starmap([new_upload(node, result[1], result[2]) for node in result[0]])

                # SE PUEDE NAVEGAR SIN CRASHEAR EL PROGRAMA
                # with ThreadPoolExecutor(max_workers=len(result[0])) as executor:
                #     future = executor.map([new_upload(node, result[1], result[2]) for node in result[0]])
                #     future.join()

                # SE PUEDE NAVEGAR SIN CRASHEAR EL PROGRAMA
                # executor = ThreadPoolExecutor(max_workers=10)
                # executor.submit([new_upload(node, result[1], result[2]) for node in result[0]])

                # NO FUNCIONA
                # executor = ThreadPoolExecutor(max_workers=len(result[0]))
                # for node in result[0]:
                #     executor.submit(new_upload, node, result[1], result[2])   


            else:
                return verify_result
        
        elif action == 'delete':
            pass

@app.route('/dayly', methods = ['GET', 'POST'])
@limiter.limit("1/2second")
def my_dayly():
    if request.method == 'GET':
        return render_template('index.html', route = 5)

    elif request.method == 'POST':
        date = request.form["date"]
        
        if date == '':
            return {'msg': 'No se ha especificado ninguna fecha'}

        else:
            data = dayly(date)
            return {'msg': data}

@app.route('/info')
@limiter.limit("2/second")
def indexe():
    return render_template('index.html', route = 6)


if __name__ == '__main__':
    app.run(host= "0.0.0.0", port=8080, debug=False)