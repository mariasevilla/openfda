import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#con esto nos conectamos a la pagina a la que deseamos acceder. Ponemos limit=10 pues queremos la informaciion de diez medicamentos
conn.request("GET", "/drug/label.json?&limit=10", None, headers)
#Guardamos en una variable toda la informacion que el servidor web nos manda al acceder a esa direccion URL
info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)
#Decodificamos la informacion y la leemos para guardarla en una nueva variable (drugs)
#Creamos un bucle que vaya accediendo e imprima el id de los 10 primeros medicamentos
num=0
while num < 10:
    drug = drugs['results'][num]#para acceder al id hay que entrar primero en results
    print("El id medicamento es", drug['id'])
    num +=1

