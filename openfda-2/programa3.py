import http.client
import json
#el principio activo de las aspirinas es el acido acetilsalicilico (acetylsalicylic acid)
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#con esto nos conectamos a la pagina a la que deseamos acceder. Ponemos limit=100 para que busque en esos 100 primeros medicamentos

conn.request("GET", "/drug/label.json?search=active_ingredient:%22acetylsalicylic+acid%22&limit=100&skip", None, headers)
#Guardamos en una variable toda la informacion que el servidor web nos manda al acceder a esa direccion URL
info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)
#Decodificamos la informacion y la leemos para guardarla en una nueva variable (drugs)

#creamos un bucle para buscar el id y el nobre del fabricante de todos los medicamentos relacionados con las aspirinas.
#dentro del bucle usamos if y else para que no de error si algun  medicamento de esos no tiene dicha información
for drug in drugs['results']:
    print ("El id del medicamento es:", drug['id'])
    if drug['openfda']:
        print("Y el nombre de su fablicante es",drug['openfda']['manufacturer_name'])#para buscar el manufacturer_name hay que
        #entrar primero en openfda
    else:
        print("Pero no tenemos información sobre su fabricante")


