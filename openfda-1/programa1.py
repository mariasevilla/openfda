import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=1", None, headers)

info = conn.getresponse()
counter= 0
#for i in info["results"]["0"]:
    #counter +=1
    #print("El id es:", i["results"]["id"])
    #print(i)

print(info["results"]["0"])
#print("El medicamento", informacion['results']['0']['id'])
conn.close()