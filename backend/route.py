import sys
import os
IMPORT_PATH = os.path.realpath("../notebooks/")
sys.path.append(IMPORT_PATH)


import import_files as MrtRecommendationDependencies
from flask import Flask
from flask import request
from util import Util
from recommender import Recommender


app = Flask(__name__)

@app.route('/')
def hello_world():
    return MrtRecommendationDependencies.__name__

@app.route('/get_prediction')
def get_prediction():
    model = Recommender()
    station = request.args.get('station')
    datetime = Util.string_to_date(request.args.get('datetime'),"%Y-%m-%d %H:%M")
    return model.predict(station,datetime)
