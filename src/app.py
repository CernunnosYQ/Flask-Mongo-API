from bson.objectid import ObjectId
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile("config.py")
mongo = PyMongo(app)

@app.route('/')
def index():
    return {"message": "Welcome to my api"}

# <--- Create --->
@app.route('/posts/', methods=['POST'])
def createPost():
    try:
        title = request.json['title']
        author = request.json['author']
        content = request.json['content']
        date = datetime.now()
    except (KeyError):
        return handle_400_error('Some key / value pair is missing')

    if title and author and content:
        id = mongo.db.blog.insert({
            'title': title,
            'author': author,
            'content': content,
            'last_mod': date.ctime()
        })

        resp = {
            'id': str(id)
        }

        return resp, 201
    else:
        return handle_400_error('Required values can not be empty')

# <--- Read --->
@app.route('/posts/', methods=['GET'])
def getPostsList():
    data = mongo.db.blog.find()
    resp = json_util.dumps(data)

    return Response(resp, mimetype='application/json', content_type='application/json', status=200)

@app.route('/posts/<post_id>', methods=['GET'])
def getPost(post_id):
    data = mongo.db.blog.find_one({'_id': ObjectId(post_id)})
    if not data: return handle_404_error('Resource not found')

    resp = json_util.dumps(data)

    return Response(resp, mimetype='application/json', content_type='application/json', status=200)

# <--- Update --->
@app.route('/posts/<post_id>', methods=['PUT'])
def replacePost(post_id):
    try:
        title = request.json['title']
        author = request.json['author']
        content = request.json['content']
        date = datetime.now()
    except (KeyError):
        return handle_400_error('Some key / value pair is missing')

    if title and author and content:
        mongo.db.blog.update_one({'_id': ObjectId(post_id)}, {'$set': {
            'title': title,
            'author': author,
            'content': content,
            'last_mod': date.ctime()
        }})

        return jsonify(message=f'Post {post_id} was replaced successfully'), 200
    else:
        return handle_400_error('Required values can not be empty')

@app.route('/posts/<post_id>', methods=['PATCH'])
def updatePost(post_id):
    data = request.json
    date = datetime.now()

    delta = {'last_mod': date.ctime()}

    if 'title' in data:
        delta['title'] = data['title']
    if 'author' in  data:
        delta['author'] = data['author']
    if 'content' in data:
        delta['content'] = data['content']

    mongo.db.blog.update_one({'_id': ObjectId(post_id)}, {'$set': delta})
    
    return jsonify(message=f'Post {post_id} was updated successfully'), 200

# <--- Delete --->
@app.route('/posts/<post_id>', methods=['DELETE'])
def deletePost(post_id):
    mongo.db.blog.delete_one({'_id': ObjectId(post_id)})

    return jsonify(message=f'Post {post_id} was deleted successfully'), 200


# <--- Error handling --->
@app.errorhandler(Exception)
def handle_exception_error(e):
    return jsonify(message='An error ocurred, please try again later'), 500

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify(message=f'Resource Not Found {request.url}'), 404

@app.errorhandler(400)
def handle_400_error(msg):
    return jsonify(message=msg), 400


# <--- 
if __name__ == '__main__':
    app.run(debug=True)