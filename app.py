import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('Mongo_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/enemy-list')
def enemy_index():
    enemyIndexMDB = mongo.db.enemyIndexMDB.find()
    return render_template('enemyIndex.html', enemyIndexMDB=enemyIndexMDB)


@app.route('/stage-list')
def stage_index():
    stageIndexMDB = mongo.db.stageIndexMDB.find()
    return render_template('stageIndex.html', stageIndexMDB=stageIndexMDB)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
