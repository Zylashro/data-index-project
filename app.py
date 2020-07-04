import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'MS3DB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost/MS3DB')

mongo = PyMongo(app)

if __name__ == '__main__':
    app.run(host=environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
