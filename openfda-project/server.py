from flask import Flask
from flask import request
import socket
import http.client
import json

app = Flask(__name__)

def jsontohtml():
    contenido = """
          <!doctype html>
          <html>
          <body style='background-color: lightblue'>
            <h1>Informacion sobre medicamentos</h2>
            <p></p>
        """
    contenido += datos() #datos(datos sacados de la apirest)
    contenido += """</br></body></html>"""

    return contenido

def datos():

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")

    conn.request("GET", "/drug/label.json?&limit=10", None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    drugs_raw = info.read().decode("utf-8")
    conn.close()

    drugs = json.loads(drugs_raw)

    num = 0
    while num < 10:
        drug = drugs['results'][num]
        datos = drug['id']
        num += 1







@app.route("/listDrug")
def get_listdrug():

    #limite= request.args.get('limit')
    return jsontohtml()


@app.route("/listCompanies")
def get_listcomp():
    return "listcompanies"

@app.route("/searchDrugs")
def search_drug():
    ingrediente = request.args.get('active_ingredient')
    return "search_drug" + ingrediente

@app.route("/searchCompany")
def search_company():
    nombre = request.args.get('company')
    return "searchcompany" + nombre





if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8008)
