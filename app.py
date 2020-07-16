import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
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


@app.route('/enemy-list', methods=['POST'])
def search_enemyIndex():
    query = request.form['search']
    enemy_code = mongo.db.enemyIndexMDB.find({'enemy_code': True})
    enemy_name = mongo.db.enemyIndexMDB.find({'name': True})

    stat = mongo.db.enemyIndexMDB.find_one({'attack': 'b'})

    stat2 = mongo.db.enemyIndexMDB.find({ 'level' : { '$exists' : True } })

    if query == stat2['level']:
        return render_template('queryEnemy.html')
    else:
        return render_template('searchError.html')


@app.route('/enemy-list/<enemy_code>')
def more_info_enemy(enemy_code):
    the_enemy = mongo.db.enemyIndexMDB.find({'_id': ObjectId(enemy_code)})
    return render_template('moreInfoEnemy.html', enemy=the_enemy)


@app.route('/stage-list')
def stage_index():
    stageIndexMDB = mongo.db.stageIndexMDB.find()
    return render_template('stageIndex.html', stageIndexMDB=stageIndexMDB)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
