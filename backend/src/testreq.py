import requests

url = "http://127.0.0.1:5000"

s = requests.Session()

r = s.post(url + "/api/login", json = {"email": "fiocchi.1934851@studenti.uniroma1.it", "password": "f53db7021b3b60e052ee1b97b3dfbbcf"})


r = s.get(url + "/api/getAllUsers")

print(r.text)