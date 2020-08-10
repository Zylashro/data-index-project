import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_paginate import Pagination, get_page_args
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env

# Environment variables
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = os.urandom(24)


mongo = PyMongo(app)

# Get the list of episodes from the database for the select menus.
def episode_lists():
    episode_names = {}
    episodes = []
    episode_list = mongo.db.episodes.find().sort("sort-index")
    for item in episode_list:
        episodes.append({'id': str(item['_id']), 'name': item['name']})
        episode_names[item['_id']] = item['name']
    
    return { 'episode_names': episode_names, 'episodes': episodes }


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', selected_home="selected", title='Home | Reunion Movement Index')


@app.route('/enemy-index')
def enemy_index():

    # Set up all necessary objects, lists, and strings in order to query the database.
    query_result = []
    has_filter = False
    search = ''
    attack = ''
    level = ''
    radio = {
        'attackType': ['melee', 'ranged', 'melee / ranged', 'melee / arts', 'ranged / arts', 'none'],
        'levelType': ['normal', 'elite', 'boss']
    }

    # Set up the pagination for the page.
    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Append the input from the search bar form to a list that will serve as the query request to the database.
    if 'search' in request.args:
        query = []
        search = request.args.get('search').lower()
        if len(search) > 0:
            query.append({'name': { "$regex": search, "$options": "i" }})
            query.append({'enemy_code': { "$regex": search, "$options": "i" }})
            query_search = {"$or": query}
            query_result.append(query_search)
            has_filter = True

    # Append the selected radio button from field to a list that will serve as the query request to the database.
    if 'attack-type' in request.args:
        attack = request.args.get('attack-type')
        query_result.append({'attack_type': attack})
        has_filter = True

    # Append the selected radio button from field to a list that will serve as the query request to the database.
    if 'level-type' in request.args:
        level = request.args.get('level-type')
        query_result.append({'level': level})
        has_filter = True

    # If any filter were selected, query the database with said filters.
    if has_filter == True:
        result = mongo.db.enemyIndexMDB.find({"$and": query_result})
        if result.count() < 1:
            flash('No search results found.')
        
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('enemy.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, attack=attack, level=level, search=search, radio=radio, title='Enemy Index | Reunion Movement Index')

    # If no filters were selected, get entire collection from database.
    else:
        result = mongo.db.enemyIndexMDB.find()
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('enemy.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, radio=radio, title='Enemy Index | Reunion Movement Index')


@app.route('/enemy-index/<enemy_code>')
def more_info_enemy(enemy_code):
    # Attempting an SQL Injection, or inputing an invalid id in the search bar, return an 404 page.
    if not ObjectId.is_valid(enemy_code):
        return render_template('404.html', title='404: Page not found')

    the_enemy = mongo.db.enemyIndexMDB.find_one({'_id': ObjectId(enemy_code)})

    stage_ids = []
    episode_ids = []
    occurrence = {}
    episode_names = {}
    episode_card = {}

    # Find enemy from the relation collection, append the ids of stages it appears in.
    connected_stages = mongo.db.stageEnemyRelation.find({'enemy': ObjectId(enemy_code)})
    for item in connected_stages:
        stage_ids.append(item['stage'])
        occurrence[item['stage']] = item['occurrence']

    # Find stages in which specific enemy appears in, append the id of episode the stages appear in.
    stages = mongo.db.stageIndexMDB.find({ '_id' : { "$in" : stage_ids } })
    for stg in stages:
        if stg['episode'] not in episode_ids:
            episode_ids.append(stg['episode'])
    stages.rewind()

    # Find episodes in which specific enemy appears in.
    episodes = mongo.db.episodes.find({ '_id' : { "$in" : episode_ids } })
    for episode in episodes:
        episode_names[episode['_id']] = episode['name']

    # For loop for creating list of episode and stages.
    for stg in stages:
        e_id = stg['episode']
        stg_list = []
        if e_id not in episode_card:
            stg_list.append({
                '_id': stg['_id'],
                'name': stg['name'],
                'occurrence': occurrence[stg['_id']]
            })
            episode_card[e_id] = {
                'name': episode_names[e_id],
                'stages': stg_list
            }
        else:
            stg_list = episode_card[e_id]['stages']
            stg_list.append({
                '_id': stg['_id'],
                'name': stg['name'],
                'occurrence': occurrence[stg['_id']]
            })
            episode_card[e_id]['stages'] = stg_list

    return render_template('moreInfoEnemy.html', enemy=the_enemy, episodes=episode_card, title='More Info Enemy | Reunion Movement Index')


@app.route('/stage-index')
def stage_index():

    # Set up all necessary objects, lists, and string in order to query the database.
    query_result = []
    has_filter = False
    search = ''
    episode = ''

    # Set up the pagination for the page.
    def get_records(result, offset=0, per_page=10):
        return result[offset: offset + per_page]
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    episode_list = episode_lists()
    episode_names = episode_list['episode_names']
    episodes = episode_list['episodes']

    # Append the input from the search bar form to a list that will serve as the query request to the database.
    if 'search' in request.args:
        query = []
        search = request.args.get('search').lower()
        if len(search) > 0:
            query.append({'name': { "$regex": search, "$options": "i" }})
            query.append({'stage_code': { "$regex": search, "$options": "i" }})
            query_search = {"$or": query}
            query_result.append(query_search)
            has_filter = True
    
    # Append selected form option to a list that will serve as the query request to the database.
    if 'episode' in request.args:
        episode = request.args.get('episode')
        if len(episode) > 0:
            query_result.append({'episode': ObjectId(episode)})
            has_filter = True

    # If any filter were selected, query the database with said filters.
    if has_filter == True:
        result = mongo.db.stageIndexMDB.find({"$and": query_result})
        if result.count() < 1:
            flash('No search results found.')

        paginate_results = get_records(result=result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('stage.html', episode_names=episode_names, episodes=episodes, selected_stage="selected", stages=result, pagination=pagination, episode=episode, search=search, title='Stage Index | Reunion Movement Index')

    # If no filters were selected, get entire collection from database.
    else:
        result = mongo.db.stageIndexMDB.find()
        paginate_results = get_records(result=result, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('stage.html', episode_names=episode_names, episodes=episodes, selected_stage="selected", stages=result, pagination=pagination, title='Stage Index | Reunion Movement Index')


@app.route('/stage-index/<stage_code>')
def more_info_stage(stage_code):
    if not ObjectId.is_valid(stage_code):
        return render_template('404.html', title='404: Page not found')

    the_stage = mongo.db.stageIndexMDB.find_one({'_id': ObjectId(stage_code)})

    enemy_ids = []
    occurrence = {}

    # Find stage from the relation collection, append the ids of enemies that appear in it.
    connected_enemies = mongo.db.stageEnemyRelation.find({'stage': ObjectId(stage_code)})
    for item in connected_enemies:
        enemy_ids.append(item['enemy'])
        occurrence[item['enemy']] = item['occurrence']

    enemies = mongo.db.enemyIndexMDB.find({ '_id' : { "$in" : enemy_ids } })

    episode_list = episode_lists()
    episode_names = episode_list['episode_names']
    
    return render_template('moreInfoStage.html', episode_names=episode_names, stage=the_stage, enemies=enemies, occurrence=occurrence, title='More Info Stage | Reunion Movement Index')


@app.route('/statistics')
def statistics():
    has_filter = False
    episode = ''
    enemy_numbers = {}

    episode_list = episode_lists()
    episodes = episode_list['episodes']

    # Append selected form option to a list that will serve as the query request to the database.
    if 'episode' in request.args:
        episode = request.args.get('episode')
        if len(episode) > 0:
            episode_result = mongo.db.stageIndexMDB.find({'episode': ObjectId(episode) })

            # Find id of stages in episode.
            stages = []
            for stage in episode_result:
                stages.append(stage['_id'])

            # Find enemies that appear in stage.
            enemies = []
            enemy_ids = mongo.db.stageEnemyRelation.find({'stage': { "$in": stages }})
            # For loop to create list of how many of each enemy appear in a stage.
            for enemy in enemy_ids:
                enemy_names = mongo.db.enemyIndexMDB.find_one({'_id': ObjectId(enemy['enemy'])})
                if enemy['enemy'] not in enemies:
                    enemies.append(enemy['enemy'])
                    enemy_numbers[enemy_names['name']] = enemy['occurrence']
                else:
                    enemy_numbers[enemy_names['name']] += enemy['occurrence']
            
            if len(enemies) > 0:
                has_filter = True

    if has_filter == True:
        # Find and calculate every enemy with a specific attack type.
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

        # Find and calculate every enemy with a specific level type.
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
    
    # Find and calculate all attack and level types respectively.
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

    # Set up lists for appending results.
    results_attack_type = []
    pie_attack_type_labels = []
    
    results_level_type = []
    pie_level_type_labels = []

    results_enemy_number = []
    pie_enemy_number_labels = []

    # For loops to append values from the above calculation to lists.
    for item in results_attack:
        results_attack_type.append(item["count"])
        pie_attack_type_labels.append(item["_id"].title())

    for item in results_level:
        results_level_type.append(item["count"])
        pie_level_type_labels.append(item["_id"].upper())

    for key, value in enemy_numbers.items():
        results_enemy_number.append(value)
        pie_enemy_number_labels.append(key.title())

    pie_data = {
        'pie_attack_type_values': results_attack_type, 
        'pie_attack_type_labels': pie_attack_type_labels, 
        'pie_level_type_values': results_level_type, 
        'pie_level_type_labels': pie_level_type_labels,
        'pie_enemy_number_values': results_enemy_number, 
        'pie_enemy_number_labels': pie_enemy_number_labels
    }
    
    return render_template('statistics.html', selected=episode, selected_statistics="selected", pie_data=pie_data, episodes=episodes, title='Statistics | Reunion Movement Index')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
