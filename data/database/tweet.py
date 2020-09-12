from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

import database
import re
from train_update import TrainUpdate 
from datetime import datetime
from base_model import BaseModel

class Tweet(database.DB_BASE,BaseModel):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key = True)
    link = Column(String)
    text = Column(String)
    datetime = Column(DateTime)
    datequery = Column(String)
    is_update_tweet = Column(Boolean)
    is_passenger_queue_tweet = Column(Boolean)
    train_update = relationship("TrainUpdate", back_populates="tweet")

    @classmethod
    def get_blank_tweets(cls):
        return database.DB_SESSION.query(Tweet).filter(Tweet.text == None)

    @classmethod
    def classify_update_tweets(cls):
        print("Classify Started")
        for tweet in database.DB_SESSION.query(Tweet).filter(Tweet.is_update_tweet == None):
            pattern = r"(MRT-3 update) | (MRT3 update) | (MRT-3, update) | (MRT3, update)"
            regex_obj = re.compile(pattern, re.IGNORECASE)
            if len(regex_obj.findall(tweet.text)) > 0:
                tweet.is_update_tweet = True
            else:
                tweet.is_update_tweet = False
            tweet.save()
        print("Classify Finished")


    @classmethod
    def create_train_updates(cls):
        for tweet in database.DB_SESSION.query(Tweet).outerjoin(Tweet.train_update).filter(TrainUpdate.datetime == None).filter(Tweet.is_update_tweet == True):
            try:
                train_object = cls.create_train_update_object(tweet)
                train_object.save()
                print(f"Tweet: {tweet.id} DONE")
            except:
                print(f"Tweet: {tweet.id} FAILED")


    @classmethod
    def create_train_update_object(cls,tweet):
        num_train_running = re.compile(r"\d+ trains running",re.IGNORECASE).findall(tweet.text)
        num_train_operational = re.compile(r"\d+ trains operational",re.IGNORECASE).findall(tweet.text)
        num_dalian_train_running = re.compile(r"\d+ Dalian train",re.IGNORECASE).findall(tweet.text)
        headway = re.compile(r"(\d)+(.\d+)*(\s)*mins",re.IGNORECASE).findall(tweet.text)

        if len(num_train_running) > 0:
            num_train_running = int(num_train_running[0].split(" ")[0])
        else:
            num_train_running = None
        if len(num_train_operational) > 0:
            num_train_operational = int(num_train_operational[0].split(" ")[0])
        else:
            num_train_operational = None
        if len(num_dalian_train_running) > 0:
            num_dalian_train_running = int(num_dalian_train_running[0].split(" ")[0])
        else:
            num_dalian_train_running = None
        if len(headway) > 0:
            headway = float(''.join(headway[0]))
        else:
            headway = None
        datekey = datetime(tweet.datetime.year, tweet.datetime.month, tweet.datetime.day, tweet.datetime.hour,0)
        return TrainUpdate(num_train_running=num_train_running,num_train_operational=num_train_operational,num_dalian_train_running=num_dalian_train_running,headway=headway,tweet_id=tweet.id,datetime=datekey)
