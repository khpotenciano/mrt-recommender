from sqlalchemy import Column, Integer, String, DateTime
import database

class Tweet(database.DB_BASE):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key = True)
    link = Column(String)
    text = Column(String)
    datetime = Column(DateTime)
    datequery = Column(String)

    def save(self):
        try:
            database.DB_SESSION.add(self)
            database.DB_SESSION.commit()
        except:
            database.DB_SESSION.rollback()

    def delete(self):
        try:
            database.DB_SESSION.delete(self)
            database.DB_SESSION.commit()
        except:
            database.DB_SESSION.rollback()

    @classmethod
    def get_blank_tweets(cls):
        return database.DB_SESSION.query(Tweet).filter(Tweet.text == None)
