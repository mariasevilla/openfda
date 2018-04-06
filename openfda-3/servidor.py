import socket
import http.client
import json


IP = "212.128.255.132"
PORT = 8086
MAX_OPEN_REQUESTS = 10

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=11", None, headers)

info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024)






    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: lightblue'>
        <h1>Informacion sobre medicamentos</h2>
        <p></p>
    """


    num = 0
    for drug in drugs['results']:

        num += 1
        if drug['openfda']:
            contenido += drug['openfda']['generic_name'][0]
            contenido += """</br></body></html>"""

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))


    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)


    while True:

        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto y verifica la IP")