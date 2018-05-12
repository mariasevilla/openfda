from flask import Flask
from flask import request
import socket
import http.client
import json

app = Flask(__name__)


@app.route("/listDrug")
def get_listdrug():

    #limite= request.args.get('limit')
    return jsontohtml()


@app.route("/listCompanies")
def get_listcomp():
    return "listcompanies"

@app.route("/searchDrugs")
def search_drug():

    ingrediente = request.args.get('active_ingredient').replace(" ","%20")
    resultado =  datos("/drug/label.json?search=active_ingredient:"+ingrediente+"&limit=10")
    mi_html= jsontohtml(resultado)
    return mi_html

@app.route("/searchCompany")
def search_company():
    nombre = request.args.get('manufacturer_name').replace(" ","%20")
    resultado = datos("/drug/label.json?search=manufacturer_name:"+nombre+"&limit=10")
    mi_html = jsontohtml(resultado)
    return mi_html




def datos(resultado):

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    #conn.request("GET", "/drug/label.json?&limit="+limite, None, headers)
    conn.request("GET",resultado, None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    drugs_raw = info.read().decode("utf-8")
    conn.close()

    drugs = json.loads(drugs_raw)

    num = 0
    info=""
    if "results" in drugs:
        for drug in drugs['results']:
            num +=1
            if 'generic_name' in drug['openfda']:
                info += str(drug['openfda']['generic_name'])
                info += "</br>"
            else:
                info+="No tenemos información"
                info += "</br>"
    return info



def jsontohtml(info):
    mensaje = """
          <!doctype html>
          <html>
          <body style='background-color: lightblue'>
            <h1>Informacion sobre medicamentos</h2>
            <p></p>
        """
    for med in info:
        """<ul>
        <li>"""
        mensaje += med #datos(datos sacados de la apirest)
        """</li></ul>"""
    mensaje += """</br></body></html>"""

    return mensaje

@app.route("/")
def entrada():
    inicio= """<!DOCTYPE html>
    <html>
    <body>
    <h2>Medicamento</2>
    <form action="/searchDrugs"
    Medicamento:<br>
    <input type="text" name="active_ingredient" value="">
    <br>
    <input type="submit" value="Submit">
    </form>
    </body>
    </html>"""

    inicio += """<!DOCTYPE html>
        <html>
        <body>
        <h2>Company</2>
        <form action="/searchCompany"
        Medicamento:<br>
        <input type="text" name="manufacturer_name" value="">
        <br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""

    inicio += """<!DOCTYPE html>
        <html>
        <body>
        <h2>Listado de Medicamentos</2>
        <form action="/listDrug"
        Medicamento:<br>
        <input type="text" name="limite" value="">
        <br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    inicio += """<!DOCTYPE html>
       <html>
       <body>
       <h2>Listado de Empresas</2>
       <form action="/listCompanies"
       Medicamento:<br>
       <input type="text" name="limite" value="">
       <br>
       <input type="submit" value="Submit">
       </form>
       </body>
       </html>"""
    return inicio


if __name__ == "__main__":
    app.run(port=8000)
