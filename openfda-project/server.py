import http.server
import socketserver
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
        return


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
