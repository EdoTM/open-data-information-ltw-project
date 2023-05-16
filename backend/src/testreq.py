import requests

url = "http://localhost:5000"

s = requests.Session()

r = s.post(url + "/login", json = {"email": "bianchi.1942637@studenti.uniroma1.it", "password": "d41d8cd98f00b204e9800998ecf8427e"})

r = s.post(url + "/createPost", json = {"title": "titolo", "content": "contenuto", "postImage": "immagine"})

r = s.get(url + "/getPosts")

body = {
  "postID": 34,
  "starred": True
}

r = s.post(url + "/starPost", json = body)
print(r.text)