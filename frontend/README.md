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
  profilePic: "https://www.image.com/image.png",
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


# Posts

Get posts 

  ```http request
  GET /getPosts
  ```
    ```http request
  GET /getFavoritePosts
  ```
    ```http request
  GET /getHiddenPosts
  ```

  ```json5
  [
    {
      "id": 213,
      "title": "title",
      "content": "content",
      "score": 0,
      "authorUsername": "username",
      "authorProfilePic": "https://www.gravatar.com/avatar/f9879d71855b5ff21e4963273a886bfc?d=retro",
      "postImage": "iVBORw0KGgoAAAANSUhEUgAAAeAAAAEOCAYA...",
      "commentCount": 0,
      "userVote": 1,
      "starred": true,
      "hidden": false,
      "timestamp": "2020-12-12 12:12:12"
    },
    {
      // ...
    }
  ]
  ```

Create a post

  ```http request
  POST /createPost
  ```

  ```json
  {
    "title": "title",
    "content": "content",
    "postImage": "iVBORw0KGgoAAAANSUhEUgAAAeAAAAEOCAYA..."
  }
  ```

Get comments for a post

```http request
GET /getComments/:postID
```

```json5
[
  {
    "content": "CHE BELLO commento TOP",
    "timestamp": "2001-09-11 08:46:00",
    "username": "edoardo-fiocchi"
  },
  {
    // ...
  }
]
```


Vote a post

  ```http request
  POST /votePost
  ```

  ```json
  {
    "postID": 213,
    "vote": 1
  }
  ```

Star a post

  ```http request
  POST /starPost
  ```

  ```json
  {
    "postID": 213,
    "starred": true
  }
  ```

Hide a post
  
  ```http request
  POST /hidePost
  ```
  
  ```json
  {
    "postID": 213,
    "hidden": true
  }
  ```

Comment a post

  ```http request
  POST /newComment
  ```

  ```json
  {
    "postID": 213,
    "content": "CHE BELLO commento TOP"
  }
  ```

# Plot Data

## Meetings

### Request

```http request
POST /plot/meetings
```

```json5
{
  "index" : "nation",
  "elements": [
    {
      "name": "Element 6",
      "color": "#fffc23",
      "currentCategory": "All",
    },
    {
      // ...
    }
  ]
}
```

### Response

```json5
{
  "xAxisValues": [
    "Samsung",
    "Apple",
    "Google"
  ],
  "elements": [
    {
      "name": "Element 1",
      "data": [
        5,
        10,
        15
      ],
      "color": "#fffc23",
    },
    {
      "name": "Element 2",
      "data": [
        10,
        15,
        5
      ],
      "color": "#2abcab",
    },
    // ...
  ]
}
```
