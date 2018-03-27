import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=10", None, headers)

info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

num=0
while num < 10:
    drug = drugs['results'][num]
    print("El id medicamento es", drug['id'])
    num +=1
