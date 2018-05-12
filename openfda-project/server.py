from flask import Flask
from flask import request
import socket
import http.client
import json
import socket

app = Flask(__name__)


@app.route("/listDrug")
def get_listdrug():

    limit = request.args.get('limit')
    resultado = datos1("/drug/label.json?&limit="+limit)
    mi_html = jsontohtml(resultado)
    return mi_html

@app.route("/listCompanies")
def get_listcomp():
    limit = request.args.get('limit')
    resultado = datos2("/drug/label.json?&limit=" + limit)
    mi_html = jsontohtml(resultado)
    return mi_html


@app.route("/searchDrugs")
def search_drug():
    limit = request.args.get('limit')
    ingrediente = request.args.get('active_ingredient').replace(" ","%20")
    resultado =  datos1("/drug/label.json?search=active_ingredient:"+ingrediente+"&limit="+limit)
    mi_html= jsontohtml(resultado)
    return mi_html

@app.route("/searchCompany")
def search_company():
    limit = request.args.get('limit')
    nombre = request.args.get('manufacturer_name').replace(" ","%20")
    resultado = datos2("/drug/label.json?search=manufacturer_name:"+nombre+"&limit="+limit)
    mi_html = jsontohtml(resultado)
    return mi_html

#@app.route("/secret")
#def secret(clientsocket):
    #linea_inicial = "HTTP/1.1 401 Unauthorized"
    #cabecera = "Content-Type: text/html\n"
    #cabecera += "WWW-Authenticate: Basic realm=Access to staging site"

    #mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n")
    #clientsocket.send(mensaje_respuesta)
    #clientsocket.close()
#@app.route("/redirect")



def datos1(resultado):

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
                info+="Desconocida"
                info += "</br>"
    return info

def datos2(resultado):

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
            if 'manufacturer_name' in drug['openfda']:
                info += str(drug['openfda']['manufacturer_name'])
                info += "</br>"
            else:
                info+="Desconocida"
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
    <h2><b><u>Medicamento:</b></u></2>
    <form action="/searchDrugs"
    <br>
    <small>Ingrediente activo:</small>
    <input type="text" name="active_ingredient" value="">
    <br>
    <small>Limite:</small>
    <input type="text" name="limit" value="">
    <br>
    <input type="submit" value="Submit">
    </form>
    </body>
    </html>"""

    inicio += """<!DOCTYPE html>
        <html>
        <body>
        <h2><b><u>Company</b></u></2>
        <form action="/searchCompany"
        Medicamento:<br>
        <small>Nombre:</small>
        <input type="text" name="manufacturer_name" value="">
        <br>
        <small>Limite:</small>
        <input type="text" name="limit" value="">
        <br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""

    inicio += """<!DOCTYPE html>
        <html>
        <body>
        <h2><b><u>Listado de Medicamentos</b></u></2>
        <form action="/listDrug"
        Medicamento:<br>
        <small>Limite:</small>
        <input type="text" name="limit" value="">
        <br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    inicio += """<!DOCTYPE html>
       <html>
       <body>
       <h2><b><u>Listado de Empresas</b></u></2>
       <form action="/listCompanies"
       Medicamento:<br>
       <small>Limite:</small>
       <input type="text" name="limit" value="">
       <br>
       <input type="submit" value="Submit">
       </form>
       </body>
       </html>"""
    return inicio


if __name__ == "__main__":
    app.run(port=8000)
