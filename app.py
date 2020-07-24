import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_paginate import Pagination, get_page_args
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', selected_home="selected")


@app.route('/enemy-list')
def enemy_index():

    query = []
    query_item = {}
    has_filter = False
    search = ''
    attack = ''
    level = ''

    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if 'search' in request.args:
        search = request.args.get('search').lower()
        query_item["name"] = { "$regex": search, "$options": "i" }
        query.append(query_item)
        has_filter = True

    if 'attack-type' in request.args:
        attack = request.args.get('attack-type')
        query_item["attack_type"] = attack
        query.append(query_item)
        has_filter = True

    if 'level-type' in request.args:
        level = request.args.get('level-type')
        query_item["level"] = level
        query.append(query_item)
        has_filter = True

    if has_filter == True:
        if len(query) > 0:
            result = mongo.db.enemyIndexMDB.find({"$and": query})
            paginate_results = get_records(offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=result.count())
            return render_template('enemyIndex.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, page=page, per_page=per_page, attack=attack, level=level)
        else:
            flash('No search results or no filters selected.')
            return redirect(url_for('enemy_index'))
    else:
        result = mongo.db.enemyIndexMDB.find()
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('enemyIndex.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, page=page, per_page=per_page)

# @app.route('/enemy-list')
# def enemy_index():
#     if 'search' in request.args:
#         search = request.args.get('search')

#         if search == '':
#             flash('A keyword is required!')
#             return redirect(url_for('enemy_index'))


#         search = search.lower()
#         result = mongo.db.enemyIndexMDB.find({'name': { "$regex": search, "$options": "i" }})

#         if result.count() > 0:
#             return render_template('enemyIndex.html', enemyIndexMDB=result)
#         else:
#             flash('No results found.')
#             return redirect(url_for('enemy_index'))

#     else:
#         enemyIndexMDB = mongo.db.enemyIndexMDB.find()
#         return render_template('enemyIndex.html', enemyIndexMDB=enemyIndexMDB)


# @app.route('/enemy-list', methods=['GET', 'POST'])
# def filter_enemyIndex():

#     query = []
#     query_item = {}
#     queryValue = {}

#     if 'attack-type' in request.form:
#         items = request.form.get('attack-type')
#         query_item["attack_type"] = items
#         query.append(query_item)

#     if 'level-type' in request.form:
#         queryLevel = request.form.get('level-type')
#         query_item["level"] = queryLevel
#         query.append(query_item)

#     if len(query) > 0:
#         result = mongo.db.enemyIndexMDB.find({"$and": query})
#         return render_template('enemyIndex.html', enemyIndexMDB=result)
#     else:
#         flash('No filters selected.')
#         return redirect(url_for('enemy_index'))


@app.route('/enemy-list/<enemy_code>')
def more_info_enemy(enemy_code):
    the_enemy = mongo.db.enemyIndexMDB.find({'_id': ObjectId(enemy_code)})
    return render_template('moreInfoEnemy.html', enemy=the_enemy)


@app.route('/stage-list')
def stage_index():
    result = mongo.db.stageIndexMDB.find()
    return render_template('stageIndex.html', selected_stage="selected", stageIndexMDB=result)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
