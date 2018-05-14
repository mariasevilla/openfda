from flask import Flask
from flask import request
import socket
import http.client
import json
import socketserver
import socket
socketserver.TCPServer.allow_reuse_address = True
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
    return "<ul><li>{}</li></ul>".format(info)

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
    return "<ul><li>{}</li></ul>".format(info)


def jsontohtml(info):
    mensaje = """
          <!doctype html>
          <html>
          <body style='background-color: lightgreen'>
            <h1>Informacion sobre medicamentos</h2>
            <p></p>
        """

    mensaje += info #datos(datos sacados de la apirest)

    mensaje += """</br></body></html>"""

    return mensaje

@app.route("/")
def entrada():
    inicio= """<!DOCTYPE html>
    <html>
    <body>
    <body style='background-color: lightblue'>
    <h2><b>1. <u>Medicamento:</b></u></2>
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
        <h2><b>2. <u>Company</b></u></2>
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
        <h2><b>3. <u>Listado de Medicamentos</b></u></2>
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
       <h2><b>4. <u>Listado de Empresas</b></u></2>
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
    app.run(host="127.0.0.1",port=8013)
