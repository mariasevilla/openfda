import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#con esto nos conectamos a la pagina a la que deseamos acceder. Ponemos limit=1 pues solo queremos la informaciion de un medicamento
conn.request("GET", "/drug/label.json?&limit=1", None, headers)
#Guardamos en una variable toda la informacion que el servidor web nos manda al acceder a esa direccion URL
info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)
#Una vez decodificada la informacion vamos al lugar a que queremos llegar, primero entramos en results en el primer medicamento
drug = drugs['results'][0]
print("El id medicamento es", drug['id'])#una vez alli buscamos el id
print("El proposito del medicamento es", drug['purpose'])# y el purpose
print("El fabricante del medicamento es", drug['openfda']['manufacturer_name'])#y por ultimo entramos en openfda para poder acceder
#al manufacturr_name