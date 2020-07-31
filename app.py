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


def episode_lists():
    episode_names = {}
    episodes = []
    episode_list = mongo.db.episodes.find()
    for item in episode_list:
        episodes.append({'id': str(item['_id']), 'name': item['name']})
        episode_names[item['_id']] = item['name']
    
    return { 'episode_names': episode_names, 'episodes': episodes }


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', selected_home="selected")


@app.route('/enemy-list')
def enemy_index():

    query_result = []
    has_filter = False
    search = ''
    attack = ''
    level = ''

    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if 'search' in request.args:
        query = []
        search = request.args.get('search').lower()
        query.append({'name': { "$regex": search, "$options": "i" }})
        query.append({'enemy_code': { "$regex": search, "$options": "i" }})
        query_search = {"$or": query}
        query_result.append(query_search)
        has_filter = True

    if 'attack-type' in request.args:
        attack = request.args.get('attack-type')
        query_result.append({'attack_type': attack})
        has_filter = True

    if 'level-type' in request.args:
        level = request.args.get('level-type')
        query_result.append({'level': level})
        has_filter = True

    if has_filter == True:
        if len(query) > 0:
            result = mongo.db.enemyIndexMDB.find({"$and": query_result})
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


@app.route('/enemy-list/<enemy_code>')
def more_info_enemy(enemy_code):
    the_enemy = mongo.db.enemyIndexMDB.find({'_id': ObjectId(enemy_code)})
    return render_template('moreInfoEnemy.html', enemy=the_enemy)


@app.route('/stage-list')
def stage_index():

    query_result = []
    has_filter = False
    search = ''
    episode = ''

    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    episode_list = episode_lists()
    episode_names = episode_list['episode_names']
    episodes = episode_list['episodes']

    if 'search' in request.args:
        query = []
        search = request.args.get('search').lower()
        query.append({'name': { "$regex": search, "$options": "i" }})
        query.append({'stage_code': { "$regex": search, "$options": "i" }})
        query_search = {"$or": query}
        query_result.append(query_search)
        has_filter = True
    
    if 'episode' in request.args:
        episode = request.args.get('episode')
        query_result.append({'episode': ObjectId(episode)})
        has_filter = True

    if has_filter == True:
        if len(query) > 0:
            result = mongo.db.stageIndexMDB.find({"$and": query_result})
            paginate_results = get_records(offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=result.count())
            return render_template('stageIndex.html', episode_names=episode_names, episodes=episodes, selected_stage="selected", stages=result, pagination=pagination, page=page, per_page=per_page, episode=episode)
        else:
            flash('No search results or no filters selected.')
            return redirect(url_for('stage_index'))
    else:
        result = mongo.db.stageIndexMDB.find()
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('stageIndex.html', episode_names=episode_names, episodes=episodes, selected_stage="selected", stages=result, pagination=pagination, page=page, per_page=per_page)

    result = mongo.db.stageIndexMDB.find()
    return render_template('stageIndex.html', episode_names=episode_names, episodes=episodes, selected_stage="selected", stages=result)


@app.route('/stage-list/<stage_code>')
def more_info_stage(stage_code):
    the_stage = mongo.db.stageIndexMDB.find_one({'_id': ObjectId(stage_code)})

    eids = []
    enemy_ids = mongo.db.stageEnemyRelation.find({'stage': ObjectId(stage_code)})
    for item in enemy_ids:
        eids.append(item['enemy'])

    enemy = mongo.db.enemyIndexMDB.find({ '_id' : { "$in" : eids } })

    episode_list = episode_lists()
    episode_names = episode_list['episode_names']
    
    return render_template('moreInfoStage.html', episode_names=episode_names, stage=the_stage, enemy=enemy)


@app.route('/statistics')
def statistics():
    query = []
    query_item = {}
    has_filter = False
    episode = ''

    episode_list = episode_lists()
    episodes = episode_list['episodes']

    if 'episode' in request.args:
        episode = request.args.get('episode')
        if len(episode) > 0:
            episode_result = mongo.db.stageIndexMDB.find({'episode': ObjectId(episode) })

            stages = []
            for stage in episode_result:
                stages.append(stage['_id'])

            enemies = []
            enemy_ids = mongo.db.stageEnemyRelation.find({'stage': { "$in": stages }})
            for enemy in enemy_ids:
                if enemy['enemy'] not in enemies:
                    enemies.append(enemy['enemy'])
            
            if len(enemies) > 0:
                has_filter = True
        
    results_attack_type = []
    results_level_type = []

    if has_filter == True:
        results_attack = mongo.db.enemyIndexMDB.aggregate([
            { 
                "$match": { '_id' : { "$in" : enemies } }
            },
            {
                "$group": {
                    "_id": "$attack_type",
                    "count": { "$sum": 1 } 
                }
            }
        ])

        results_level = mongo.db.enemyIndexMDB.aggregate([
            { 
                "$match": { '_id' : { "$in" : enemies } }
            },
            { 
                "$group": {
                    "_id": "$level",
                    "count": { "$sum": 1 } 
                }
            }
        ])
        
    else:
        results_attack = mongo.db.enemyIndexMDB.aggregate([
            { "$group": {
                "_id": "$attack_type",
                "count": { "$sum": 1 } 
            }}
        ])

        results_level = mongo.db.enemyIndexMDB.aggregate([
            { "$group": {
                "_id": "$level",
                "count": { "$sum": 1 } 
            }}
        ])

    results_attack_type = []
    pie_attack_type_labels = []
    
    results_level_type = []
    pie_level_type_labels = []

    for item in results_attack:
        results_attack_type.append(item["count"])
        pie_attack_type_labels.append(item["_id"].title())

    for item in results_level:
        results_level_type.append(item["count"])
        pie_level_type_labels.append(item["_id"].upper())

    pie_data = {
        'pie_attack_type_values': results_attack_type, 
        'pie_attack_type_labels': pie_attack_type_labels, 
        'pie_level_type_values': results_level_type, 
        'pie_level_type_labels': pie_level_type_labels
    }
    
    return render_template('statistics.html', selected=episode, selected_statistics="selected", pie_data=pie_data, episodes=episodes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
