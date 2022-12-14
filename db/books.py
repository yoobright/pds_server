from db import DB_Obj

DB = DB_Obj.db


class Book(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    book_name = DB.Column(DB.String, nullable=False)
    author_id = DB.Column(DB.String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
