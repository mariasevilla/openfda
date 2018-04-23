from flask import Flask
from flask import request

app = Flask(__name__)

def jsontohtml():
    contenido = """
          <!doctype html>
          <html>
          <body style='background-color: lightblue'>
            <h1>Informacion sobre medicamentos</h2>
            <p></p>
        """
    contenido += "HOLA" #datos(datos sacados de la apirest)
    contenido += """</br></body></html>"""

    return contenido


@app.route("/listDrug")
def get_listdrug():

    #limite= request.args.get('limit')
    return jsontohtml(contenido)


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
    app.run(host='0.0.0.0',port=8081)