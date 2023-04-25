# Login request


```http request
POST /login

{
    "email": "email@example.com",
    "password": "passwordMd5"
}
```

Response:
```ts
{
  status: "success" | "error";
  username: string;
  email: string;
}
```
Sets cookie `sessionID`.
