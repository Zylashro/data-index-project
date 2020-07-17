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
    queryAll = request.form.get['show-all']
    queryAttack = request.form.get['attack-type']
    queryLevel = request.form.get['level-type']

    enemyAttackMelee = mongo.db.enemyIndexMDB.find({'attack_type': 'melee'})
    enemyAttackRanged = mongo.db.enemyIndexMDB.find({'attack_type': 'ranged'})
    enemyAttackArts = mongo.db.enemyIndexMDB.find({'attack_type': 'arts'})
    enemyAttackMeleeAndRanged = mongo.db.enemyIndexMDB.find({'attack_type': 'melee / ranged'})
    enemyAttackMeleeAndArts = mongo.db.enemyIndexMDB.find({'attack_type': 'melee / arts'})
    enemyAttackRangedAndArts = mongo.db.enemyIndexMDB.find({'attack_type': 'ranged / arts'})

    enemyLevelNormal = mongo.db.enemyIndexMDB.find({'level': 'normal'})
    enemyLevelElite = mongo.db.enemyIndexMDB.find({'level': 'elite'})
    enemyLevelBoss = mongo.db.enemyIndexMDB.find({'level': 'boss'})

    if queryAll:
        return redirect(url_for('enemy_index'))
    elif queryAttack == enemyAttackMelee['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackMelee)
    elif queryAttack == enemyAttackRanged['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackRanged)
    elif queryAttack == enemyAttackArts['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackArts)
    elif queryAttack == enemyAttackMeleeAndRanged['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackMeleeAndRanged)
    elif queryAttack == enemyAttackMeleeAndArts['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackMeleeAndArts)
    elif queryAttack == enemyAttackRangedAndArts['attack_type']:
        return render_template('queryEnemy.html', queryEnemy=enemyAttackRangedAndArts)
    elif queryLevel == enemyLevelNormal['level']:
        return render_template('queryEnemy.html', queryEnemy=enemyLevelNormal)
    elif queryLevel == enemyLevelElite['level']:
        return render_template('queryEnemy.html', queryEnemy=enemyLevelElite)
    elif queryLevel == enemyLevelBoss['level']:
        return render_template('queryEnemy.html', queryEnemy=enemyLevelBoss)
    else:
        return render_template('searchError.html')
    '''
    query = request.form['search']
    stat = mongo.db.enemyIndexMDB.find({'level': true})
    
    if query == stat['level']:
        return render_template('queryEnemy.html')
    else:
        return render_template('searchError.html')
    '''


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
