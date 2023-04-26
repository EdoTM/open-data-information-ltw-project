import requests

url = "http://127.0.0.1:5000"

r = requests.post(url + "/login", json={"email": "gino@hello.com", "password": "erkadjaiewfflwal"})
print(r.cookies)
print(r.json())
