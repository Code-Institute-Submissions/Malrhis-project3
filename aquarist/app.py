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

# favicon GET route


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

    name = request.form.get('name')
    scientific_name = request.form.get('scientific_name')
    higher_classification = request.form.get('higher_classification')
    fish_picture = request.form.get('fish_picture')
    full_grown_size_in_cm = request.form.get('full_grown_size_in_cm')
    reproduction = request.form.get('reproduction')
    diet = request.form.get('diet')
    water_temp_in_degc = request.form.get('water_temp_in_degc')
    pH = request.form.get('pH')
    tank_setup_text = request.form.get('tank_setup_text')

    # Validate Form Entry in Backend app.py
    errors = {}

    if len(name) == 0:
        errors['name_is_blank'] = "Fish name cannot be blank"

    if len(scientific_name) == 0:
        errors['scientific_name_is_blank'] = "Scientific name cannot be blank"

    if len(fish_picture) == 0:
        errors['fish_picture_is_blank'] = "No fish pic URL was found"

    if len(full_grown_size_in_cm) == 0:
        errors['full_grown_size_is_blank'] = "No fish size was entered"
    elif int(full_grown_size_in_cm) < 0:
        errors['full_grown_size_is_negative'] = "Fish Size cannot be negative"

    if len(reproduction) == 0:
        errors['reproduction_is_blank'] = "No reproduction method was entered"

    if len(water_temp_in_degc) == 0:
        errors['water_temp_is_blank'] = "No water temperature was entered"
    elif int(water_temp_in_degc) < 0:
        errors['water_temp_is_negative'] = "Water Temp cannot be negative"

    if len(pH) == 0:
        errors['pH_is_blank'] = "pH cannot be blank"
    elif int(pH) < 0:
        errors['pH_is_negative'] = "pH cannot be negative"

    if len(pH) == 0:
        errors['tank_setup_text_is_blank'] = "No tank setup text was entered"

    # insert only ONE new documernt
    if len(errors) == 0:
        db.fish.insert_one({
            "name": name,
            "scientific_name": scientific_name,
            "higher_classification": higher_classification,
            "fish_picture": fish_picture,
            "full_grown_size_in_cm": float(full_grown_size_in_cm),
            "reproduction": reproduction,
            "diet": diet,
            "water_temp_in_degc": float(water_temp_in_degc),
            "pH": float(pH),
            "tank_setup_text": tank_setup_text
        })
        flash("A new fish has been created successfully!")
        return redirect(url_for('show_all_fish'))
    else:
        return render_template('create_fish.template.html', errors=errors)

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
