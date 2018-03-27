import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=1", None, headers)

info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

drug = drugs['results'][0]
print("El id medicamento es", drug['id'])
print("El proposito del medicamento es", drug['purpose'])
print("El fabricante del medicamento es", drug['openfda']['manufacturer_name'])