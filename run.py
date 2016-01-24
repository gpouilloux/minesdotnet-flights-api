from flask import Flask
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# TODO flights with critera such as date, location (departure, arrival)

@app.route("/")
def hello():
    client = MongoClient('localhost', 27017)
    db = client.test

    post = {"author": "Mike",
            "text": "My first blog post!",
             "tags": ["mongodb", "python", "pymongo"],
             "date": datetime.datetime.utcnow()}

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)
    return "Hello World!"


if __name__ == "__main__":
    app.run()
