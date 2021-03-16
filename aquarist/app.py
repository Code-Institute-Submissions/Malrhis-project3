from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'aquarist_resource'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# READ
# route to show all the fishes
@app.route('/fish')
def show_all_fish():
    fish = db.fish.find()
    return render_template('show_fish.template.html', fish=fish)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)