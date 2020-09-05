import sys
import os

MODEL_PATH = os.path.realpath("../model/")
SCRAPER_PATH = os.path.realpath("../data/scraper/")
CLEANER_PATH = os.path.realpath("../data/cleaner/")
UTIL_PATH = os.path.realpath("../util/")
DATASET_PATH = os.path.realpath("../data/datasets/")
DATABASE_PATH = os.path.realpath("../data/database/")
sys.path.append(MODEL_PATH)
sys.path.append(SCRAPER_PATH)
sys.path.append(CLEANER_PATH)
sys.path.append(UTIL_PATH)
sys.path.append(DATABASE_PATH)



def get_dataset_path(file):
    return os.path.join(DATASET_PATH, file)
