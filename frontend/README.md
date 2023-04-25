# Login request


```http request
POST /login

{
    "email": "email@example.com",
    "password": "passwordMd5"
}
```

Response if success (Sets cookie `sessionID`):
```json5
{
  status: "success",
  username: "username",
  email: "email@smt.com",
}
```
Response if error:
```json5
{
  status: "error",
  error: "error message",
}
```



# Sign up request

```http request
POST /signup

{
    "email": "email@example.com",
    "password": "passwordMd5",
    "username": "username",
    "birthday": "YYYY-MM-DD",
}
```

Response: same of Login request (sets cookie `sessionID`).