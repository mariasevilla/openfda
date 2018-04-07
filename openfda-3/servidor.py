import socket
import http.client
import json


IP = "192.168.1.58"
PORT = 8086
MAX_OPEN_REQUESTS = 10

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#con esto nos conectamos a la pagina a la que deseamos acceder. Ponemos limit=1 pues solo queremos la informaciion de un medicamento

conn.request("GET", "/drug/label.json?&limit=11", None, headers)

info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)
#Decodificamos la informacion y la leemos para guardarla en una nueva variable (drugs)

def process_client(clientsocket):
#Funcion que atiende al cliente. Lee su peticion y le envia un mensaje de respuesta en cuyo contenido hay texto
#en HTML que se muestra en el navegador

    # Leemos a traves del socket el mensaje de solicitud del cliente

    mensaje_solicitud = clientsocket.recv(1024)

#definimos el contenido del mensaje de respuesta
    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: lightblue'>
        <h1>Informacion sobre medicamentos</h2>
        <p></p>
    """

#este bucle nos permite ir añadiendo al contenido la informacion deseada de los medicamentos (geeric_name)
    num = 0
    for drug in drugs['results']:

        num += 1
        if drug['openfda']:
            contenido += drug['openfda']['generic_name'][0]
            contenido += """</br></body></html>"""

#Indicamos primero quetodo OK.

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

#creamos el mensaje de respuesta uniendo todas sus partes
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


# Creamos un socket para el servidor. Es por el que llegan las peticiones de los clientes.
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
# Asociar el socket a la direccion IP y puertos del servidor
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)


    while True:
# Esperar a que lleguen conexiones del exterior. Cuando llega una conexion nueva, se obtiene un nuevo socket para
# comunicarnos con el cliente. Este sockets contiene la IP y Puerto del cliente
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()
# Procesamos la peticion del cliente, pasandole el socket como argumento
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
#en caso de error conectandose al socket se lanzan los siguientes mensajes
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto y verifica la IP")