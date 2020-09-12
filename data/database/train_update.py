from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

import database
import re
from base_model import BaseModel

class TrainUpdate(database.DB_BASE,BaseModel):
    __tablename__ = 'train_updates'
    datetime = Column(DateTime, primary_key = True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    num_train_running = Column(Integer)
    num_train_operational = Column(Integer)
    num_dalian_train_running = Column(Integer)
    num_dalian_train_operational = Column(Integer)
    headway = Column(Float)
    tweet = relationship("Tweet", back_populates = "train_update")
