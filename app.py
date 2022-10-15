import datetime

from flask import Flask, jsonify, make_response
from flask.json import JSONEncoder
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


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


@app.route('/')
def hello_world():
    return 'Hello World!!!'


class UserListResource(Resource):
    def __init__(self):
        super(UserListResource, self).__init__()
        self.user_get_parser = reqparse.RequestParser()
        self.user_get_parser.add_argument('user_name', type=str)

        self.user_add_parser = reqparse.RequestParser()
        self.user_add_parser.add_argument('user_name', type=str, required=True)
        self.user_add_parser.add_argument('email', type=str)
        self.user_add_parser.add_argument(
            'submit_time',
            type=datetime.datetime.fromisoformat,
            required=True
        )

    def get(self):
        args = self.user_get_parser.parse_args()

        query = db.session.query(User)
        if args.user_name:
            query = query.filter(User.user_name == args.user_name)

        users = query.all()
        res = [u.as_dict() for u in users]
        return jsonify(res)

    def post(self):
        args = self.user_add_parser.parse_args()
        print(args)

        user = User(
            user_name=args.user_name,
            email=args.email,
            submit_time=args.submit_time
        )
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({"id": user.id}), 201)


class UserByIdResource(Resource):
    def __init__(self):
        super(UserByIdResource, self).__init__()
        self.user_put_parser = reqparse.RequestParser()
        self.user_put_parser.add_argument('user_name', type=str)

    def get(self, uid: int):
        user = db.session.query(User).filter(User.id == uid).one_or_none()
        if user is not None:
            return jsonify(user.as_dict())
        return jsonify(None)

    def delete(self, uid: int):
        res = db.session.query(User).filter(User.id == uid).delete()
        db.session.commit()
        return make_response(jsonify(res), 204)

    def put(self, uid: int):
        args = self.user_put_parser.parse_args()
        user = db.session.query(User).filter(User.id == uid).one_or_none()
        user_name = args.user_name
        if user and user_name:
            user.user_name = user_name
            db.session.commit()
            return user.id
        return 0


class BookResource(Resource):
    def __init__(self):
        super(BookResource, self).__init__()
        self.book_add_parser = reqparse.RequestParser()
        self.book_add_parser.add_argument('book_name', type=str, required=True)
        self.book_add_parser.add_argument('author_id', type=int, required=True)

    def get(self):
        books = db.session.query(User, Book) \
            .join(Book, Book.author_id == User.id).all()
        res = [[b[0].as_dict(), b[1].as_dict()] for b in books]
        return jsonify(res)

    def post(self):
        args = self.book_add_parser.parse_args()
        print(args)

        book = Book(
            book_name=args.book_name,
            author_id=args.author_id,
        )
        db.session.add(book)
        db.session.commit()

        return jsonify({"id": book.id})


api.add_resource(UserListResource, '/users')
api.add_resource(UserByIdResource, '/users/<int:uid>')
api.add_resource(BookResource, '/books')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8089')
