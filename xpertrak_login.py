from constants import url_ext
import requests

def get_cookie():
    login_link = 'http://{}/pathtrak/api/auth/login'.format(url_ext)
    credentials = {
    "password": "calidad",
    "username": "calidad"
    }
    sesion = requests.post(login_link, json= credentials)
    cookie = sesion.cookies.get_dict()["JSESSIONID"]

    return cookie
