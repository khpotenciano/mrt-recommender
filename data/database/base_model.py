import database

class BaseModel():
    def save(self):
        try:
            database.DB_SESSION.add(self)
            database.DB_SESSION.commit()
        except:
            database.DB_SESSION.rollback()
            raise Exception("Error Saving!")

    def delete(self):
        try:
            database.DB_SESSION.delete(self)
            database.DB_SESSION.commit()
        except:
            database.DB_SESSION.rollback()
            raise Exception("Error Deleting!")

    @classmethod
    def filter(cls, conditionals):
        return database.DB_SESSION.query(cls).filter(conditionals)
