import sys
import os

SCRAPER_PATH = os.path.realpath("../data/scraper/")
CLEANER_PATH = os.path.realpath("../data/cleaner/")
UTIL_PATH = os.path.realpath("../util/")
DATASET_PATH = os.path.realpath("../data/datasets/")
DATABASE_PATH = os.path.realpath("../data/database/")
MODEL_PATH = os.path.realpath("../ml_model/")
sys.path.append(SCRAPER_PATH)
sys.path.append(CLEANER_PATH)
sys.path.append(UTIL_PATH)
sys.path.append(DATABASE_PATH)
sys.path.append(MODEL_PATH)



def get_dataset_path(file):
    return os.path.join(DATASET_PATH, file)

def get_model_path(file):
    return os.path.join(MODEL_PATH, file)

def model_exists(model_name):
    return os.path.isfile(get_model_path(model_name))
