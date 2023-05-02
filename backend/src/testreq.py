import requests

url = "http://localhost:5000"

s = requests.Session()

r = s.post(url + "/login", json = {"email": "gino@gino.com", "password": "0fe4f43e1dd173abc07ce508a74800e2"})

r = s.post(url + "/createPost", json = {"title": "titolo", "content": "contenuto", "postImage": "immagine"})

r = s.get(url + "/getPosts")
print(r.text)