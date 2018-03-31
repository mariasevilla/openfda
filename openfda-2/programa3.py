import http.client
import json
#el principio activo de las aspirinas es el acido acetilsalicilico (acetylsalicylic acid)
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?search=active_ingredient:%22acetylsalicylic+acid%22&limit=100&skip", None, headers)

info = conn.getresponse()

print(info.status, info.reason)
drugs_raw = info.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

for drug in drugs['results']:
    print (drug['openfda']['manufacturer_name'])

