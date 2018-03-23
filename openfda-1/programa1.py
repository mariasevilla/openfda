import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=1", None, headers)

info = conn.getresponse()

for i in info:
    print(i)
print(info)
#print("El medicamento", informacion['results']['0']['id'])
conn.close()