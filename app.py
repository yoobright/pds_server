from flask import Flask, jsonify, make_response
from models import db
from flask_restful import Resource, Api
from flask_restful import reqparse

from models.users import User
from models.books import Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!!!'


user_add_parser = reqparse.RequestParser()
user_add_parser.add_argument('user_name', type=str, required=True)
user_add_parser.add_argument('email', type=str)


class UserResource(Resource):

    def get(self):
        users = db.session.query(User).all()
        res = [u.as_dict() for u in users]
        return jsonify(res)

    def post(self):
        args = user_add_parser.parse_args()
        print(args)

        user = User(
            user_name=args.user_name,
            email=args.email,
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})


book_add_parser = reqparse.RequestParser()
book_add_parser.add_argument('book_name', type=str, required=True)
book_add_parser.add_argument('author_id', type=int, required=True)


class BookResource(Resource):

    def get(self):
        books = db.session.query(User, Book)\
            .join(Book, Book.author_id == User.id).all()
        res = [[b[0].as_dict(), b[1].as_dict()] for b in books]
        return jsonify(res)

    def post(self):
        args = book_add_parser.parse_args()
        print(args)

        book = Book(
            book_name=args.book_name,
            author_id=args.author_id,
        )
        db.session.add(book)
        db.session.commit()

        return jsonify({"id": book.id})


api.add_resource(UserResource, '/users')
api.add_resource(BookResource, '/books')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8089')
