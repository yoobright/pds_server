class DB(object):
    db = None
    
    @classmethod
    def set_db(cls, db):
        DB.db = db


