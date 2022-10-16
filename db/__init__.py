from flask_sqlalchemy import SQLAlchemy


class DB_Obj(object):
    db = SQLAlchemy()
    
    @staticmethod
    def set_app(app):
        DB_Obj.db.init_app(app)


