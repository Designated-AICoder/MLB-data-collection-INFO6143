import json
import requests

response = requests.get("https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1")
# response = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=search&prop=info&inprop=url&utf8=&format=json&origin=*&srlimit=20&srsearch=fanshawe")
mlb_json = json.loads(response.text)
json_str = json.dumps(mlb_json)
pyObject = json.loads(json_str)

print(json_str)
print()
print(pyObject)