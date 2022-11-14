from weakref import ReferenceType
from flask import Flask
# import pymongo
from pymongo import MongoClient
from mongoengine import connect, disconnect, DynamicDocument, IntField, StringField, ReferenceField
import hashlib
from simpleflake import simpleflake
from bson.json_util import dumps
import json

app = Flask(__name__)
# mongo = pymongo.MongoClient("mongodb+srv://dat:duongtuandat123@cluster0.vqmrfwo.mongodb.net/?retryWrites=true&w=majority")
# db = pymongo.database.Database(mongo, 'mydatabase')
# col = pymongo.collection.Collection(db, 'user')



def get_uuid():
    return str(simpleflake())

def md5(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()


connect(db="mydatabase", host='mongodb+srv://dat:duongtuandat123@cluster0.vqmrfwo.mongodb.net/?retryWrites=true&w=majority')

class User(DynamicDocument):
    meta = {"collection": "user"}
    id = StringField(primary_key=True, default = get_uuid)
    name = StringField()

class Project(DynamicDocument):
    meta = {"collection": "project"}
    id = StringField(primary_key=True, default = get_uuid)
    projectName = StringField()

class Post(DynamicDocument):
    meta = {"collection":"post"}
    id = StringField(primary_key=True, default= get_uuid)
    content = StringField()
    author = ReferenceField(User)

@app.route("/")
def default():
    return f"welcome"


@app.route("/insert=<name1>")
def something(name1):
    user = User(name=name1)
    user.save()
    return f"OK!"

@app.route("/createproject=<name>")
def createProject(name):
    project = Project(projectName=name)
    project.save()
    return f"OK"

@app.route("/listname")
def listUsername():
    result = User.objects()
    arr = []
    for i in result:
        arr.append(i.name)
    x = json.loads(dumps(arr))
    
    return f"{x}"

@app.route("/find=<name1>")
def findUser(name1):
    result = User.objects(name=name1)
    arr = []
    for i in result:
        arr.append(i.name)
        print(i.name)
    x = json.loads(dumps(arr))
    return f"{x}"


@app.route("/post/<content>/<author>")
def postNew(content, author):
    post = Post(content = content)
    dat = User.objects(name = author)
    aDat = dat[0]

    post.author = aDat
    post.save()
    return f"success"

@app.route("/userpost=<name>")
def userPost(name):
    user_result = User.objects(name=name)
    post_result =Post.objects(author = user_result[0].id)

    arr = []
    for i in post_result:
        
        arr.append(i.content)

    return f"{arr}"

if __name__ == '__main__':
    app.run(debug=True)