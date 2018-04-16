import http.server
import socketserver
import json
import http.client
socketserver.TCPServer.allow_reuse_address = True
# -- Puerto donde lanzar el servidor
PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):


    def do_GET(self):

        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y el recurso solicitado
        message = """<!DOCTYPE html>
            <html>
            <body>
            
            <h2>Medicamentos</h2>
            
            <form action="/action_page.php">
              Punto de entrada:<br>
              <input type="text" name="Punto de entrada" value="">
              <br>
              
              <input type="submit" value="Submit">
            </form> 
            
            <p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>
            
            </body>
            </html>"""

        # Enviar el mensaaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        # con esto nos conectamos a la pagina a la que deseamos acceder. Ponemos limit=1 pues solo queremos la informaciion de un medicamento

        conn.request("GET", "/drug/label.json?&limit=11", None, headers)

        info = conn.getresponse()

        print(info.status, info.reason)
        drugs_raw = info.read().decode("utf-8")
        conn.close()

        drugs = json.loads(drugs_raw)
        #if self.path == "/action_page.php?Punto+de+entrada=ListDrugs":
        def process_client(clientsocket):
        # Funcion que atiende al cliente. Lee su peticion y le envia un mensaje de respuesta en cuyo contenido hay texto
        # en HTML que se muestra en el navegador

        # Leemos a traves del socket el mensaje de solicitud del cliente

            mensaje_solicitud = clientsocket.recv(1024)

        # definimos el contenido del mensaje de respuesta
            contenido = """
                  <!doctype html>
                  <html>
                  <body style='background-color: lightblue'>
                    <h1>Informacion sobre medicamentos</h2>
                    <p></p>
                """

            # este bucle nos permite ir añadiendo al contenido la informacion deseada de los medicamentos (geeric_name)
            num = 0
            for drug in drugs['results']:

                num += 1
                if drug['openfda']:
                    contenido += drug['openfda']['generic_name'][0]
                    contenido += """</br></body></html>"""

            # Indicamos primero quetodo OK.

            linea_inicial = "HTTP/1.1 200 OK\n"
            cabecera = "Content-Type: text/html\n"
            cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

            # creamos el mensaje de respuesta uniendo todas sus partes
            mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
            clientsocket.send(mensaje_respuesta)
            clientsocket.close()
        #return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
httpd=socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
