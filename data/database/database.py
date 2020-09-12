from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import pandas as pd
import import_files as MrtRecommendationDependencies
from sqlalchemy.orm import sessionmaker, relationship


def get_query_string():
    creds = pd.read_json(f'{MrtRecommendationDependencies.DATABASE_PATH}/mysql.json', typ='series')
    dialect = 'mysql'
    driver = 'pymysql'
    username = creds.username
    password = creds.password
    host = creds.host
    port = creds.port
    database = creds.database
    path = dialect + "+" + driver + "://" + username + ":" + password + '@' + host + ":" + port + "/" + database
    return path


DB_ENGINE = create_engine(get_query_string())
DB_BASE = declarative_base()

### Database Table to Class Mapping
from tweet import Tweet
from train_update import TrainUpdate


DB_BASE.metadata.create_all(DB_ENGINE)
Session = sessionmaker(bind = DB_ENGINE)
DB_SESSION = Session()
