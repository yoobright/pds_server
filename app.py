from flask import Flask, jsonify, make_response
from models import db
from flask_restful import Resource, Api
from flask_restful import reqparse

from models.users import User

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
    return 'Hello World!'


user_add_parser = reqparse.RequestParser()
user_add_parser.add_argument('username', type=str, required=True)
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
            username=args.username,
            email=args.email,
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"id": user.id})


api.add_resource(UserResource, '/users')

if __name__ == '__main__':
    app.run(port='8089')
