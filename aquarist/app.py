from flask import Flask, render_template, request, redirect, url_for
from flask import flash, send_from_directory
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
# assign secret key to setup sessions
app.secret_key = os.environ.get('SECRET_KEY')

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'aquarist_resource'

# set up mongo client
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# favicon route


@app.route('/favicon.ico')
def get_favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# route to show the homepage


@app.route('/')
def index():
    return render_template('index.template.html')


# READ
# route to show all the fishes


@app.route('/fish')
def show_all_fish():
    fish = db.fish.find()
    return render_template('show_fish.template.html', fish=fish)

# CREATE
# route to show the form


@app.route('/fish/create')
def show_create_fish():
    return render_template('create_fish.template.html')

# route to process the form


@app.route('/fish/create', methods=["POST"])
def process_create_fish():
    print(request.form)
    name = request.form.get('name')
    scientific_name = request.form.get('scientific_name')
    higher_classification = request.form.get('higher_classification')
    full_grown_size_in_cm = float(request.form.get('full_grown_size_in_cm'))
    diet = request.form.get('diet')

    # insert only ONE new documernt
    db.fish.insert_one({
        "name": name,
        "scientific_name": scientific_name,
        "higher_classification": higher_classification,
        "full_grown_size_in_cm": full_grown_size_in_cm,
        "diet": diet
    })
    flash("A new fish has been created successfully!")
    return redirect(url_for('show_all_fish'))

# DELETE
# route to show the form for deletion


@app.route('/fish/<fish_id>/delete')
def delete_fish(fish_id):
    # find the fish that we want to delete
    fish = db.fish.find_one({
        '_id': ObjectId(fish_id)
    })

    return render_template('confirm_delete_fish.template.html',
                           fish_to_delete=fish)


# route to process the deletion
@app.route('/fish/<fish_id>/delete', methods=['POST'])
def process_delete_fish(fish_id):
    db.fish.delete_one({
        "_id": ObjectId(fish_id)
    })
    return redirect(url_for('show_all_fish'))


# UPDATE
# route to show the form for updating
@app.route('/fish/<fish_id>/update')
def show_update_fish(fish_id):
    fish_to_update = db.fish.find_one({
        '_id': ObjectId(fish_id)
    })
    return render_template('show_update_fish.template.html',
                           fish_to_update=fish_to_update)

# process the fish update


@app.route('/fish/<fish_id>/update', methods=['POST'])
def process_update_fish(fish_id):
    db.fish.update_one({
        "_id": ObjectId(fish_id)
    }, {
        "$set": {
            "name": request.form['name'],
            "scientific_name": request.form['scientific_name'],
            "higher_classification": request.form['higher_classification'],
            "full_grown_size_in_cm": request.form['full_grown_size_in_cm'],
            "diet": request.form['diet']
        }
    })
    return redirect(url_for('show_all_fish'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
