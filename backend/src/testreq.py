import requests

url = "http://127.0.0.1:5000"

s = requests.Session()

r = s.post(url + "/api/login", json = {"email": "fiocchi.1934851@studenti.uniroma1.it", "password": "f53db7021b3b60e052ee1b97b3dfbbcf"})



# body = {
#     "elements": [
#         {
#             "name": "3GPP",
#             "color": "#ff0000",
#             "currentCategory": "3GPP",
#             "tdocFilter": "all",
#         }
#     ],
#     "index": "nation"
               
# }

# r = s.post(url + "/api/plot/tdocs", json = body)

# /api/votePost
# r = s.post(url + "/api/hidePost", json = {"postID": 1, "hidden": 1})

# /api/getComments
r = s.get(url + "/api/getComments/39")

print(r.text)