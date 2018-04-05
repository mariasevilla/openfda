import socket


IP = "192.168.1.58"
PORT = 8000
MAX_OPEN_REQUESTS = 10


def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024)

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
        id= drug['id']
        num += 1



        contenido = """
          <!doctype html>
          <html>
          <body style='background-color: lightblue'>
            <h1>Informacion sobre medicamentos</h2>
            <p></p>
          </body>
          </html>
        """



        linea_inicial = "HTTP/1.1 200 OK\n"
        cabecera = "Content-Type: text/html\n"
        cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))


        mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido+id)
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