# Simple Flask/PyMongo API

Simple Flask API to manage CRUD operations on blog posts using MongoDB.
Simple API de Flask para gestionar operaciones CRUD en las publicaciones de un blog usando MongoDB.

Endpoints:
- \[ GET \] localhost:5000/posts/ --> Return Posts List
- \[ POST \] localhost:5000/posts/ --> Return New Post Id
    - 'title' __required__
    - 'author' __required__
    - 'content' __required__
- \[ GET \] localhost:5000/posts/\<post_id\> --> Return Post with Id == post_id
- \[ PUT \] localhost:5000/posts/\<post_id\> --> Return Edited Post Id
    - 'title' __required__
    - 'author' __required__
    - 'content' __required__
- \[ PATCH \] localhost:5000/posts/\<post_id\> --> Return Edited Post Id
    - 'title' __optional__
    - 'author' __optional__
    - 'content' __optional__
