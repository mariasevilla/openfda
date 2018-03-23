import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "https://api.fda.gov/drug/label.json?search=openfda:spl_id", None, headers)

r1 = conn.getresponse()
print(r1)