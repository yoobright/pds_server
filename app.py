import datetime

from flask import Flask, jsonify, make_response
from flask.json import JSONEncoder
from db import DB_Obj
from flask_restful import Resource, Api
from flask_restful import reqparse
from flasgger import Swagger

from db import api as db_api
from db.books import Book


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False


DB_Obj.set_app(app)

with app.app_context():
    DB_Obj.db.create_all()

app_api = Api(app)
swagger = Swagger(app)


def get_datetime_from_str(s):
    try:
        return datetime.datetime.fromtimestamp(int(s))
    except ValueError:
        return datetime.datetime.fromisoformat(s)


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


class PatientListResource(Resource):

    def __init__(self):
        super(PatientListResource, self).__init__()
        self.user_get_parser = reqparse.RequestParser()
        self.user_get_parser.add_argument('user_name', type=str)

        self.user_add_parser = reqparse.RequestParser()
        self.user_add_parser.add_argument('user_name', type=str, required=True)
        self.user_add_parser.add_argument('uid', type=str)
        self.user_add_parser.add_argument('gender', type=str, required=True)
        self.user_add_parser.add_argument('age', type=int, required=True)
        self.user_add_parser.add_argument('height', type=float)
        self.user_add_parser.add_argument('weight', type=float)
        self.user_add_parser.add_argument('job', type=str)
        self.user_add_parser.add_argument('edu', type=str)
        self.user_add_parser.add_argument('special', type=str, default="无")
        self.user_add_parser.add_argument('tel', type=str)
        self.user_add_parser.add_argument('tumor', type=str, default="无")
        self.user_add_parser.add_argument('tumor_metastasis', type=str)
        self.user_add_parser.add_argument('tumor_treatment', type=str)
        self.user_add_parser.add_argument('illness', type=str)
        self.user_add_parser.add_argument('liver_function', type=str)
        self.user_add_parser.add_argument('kidney_function', type=str)
        self.user_add_parser.add_argument('cardiac_function', type=str)
        self.user_add_parser.add_argument('allergy', type=str)
        self.user_add_parser.add_argument('physical', type=str)

    def get(self):
        """
        get all patient list
        ---
        responses:
          200:
            description: patient list
            schema:
              type: array
              items:
                type: object
                properties:
                  user_name:
                    type: string
                  uid:
                    type: string
                  gender:
                    type: string
                  age:
                    type: integer
                  height:
                    type: number
                    format: float
                  weight:
                    type: number
                    format: float
                  job:
                    type: string
                  edu:
                    type: string
                  special:
                    type: string
                  tel:
                    type: string
                  tumor:
                    type: string
                  tumor_metastasis:
                    type: string
                  tumor_treatment:
                    type: string
                  illness:
                    type: string
                  liver_function:
                    type: string
                  kidney_function:
                    type: string
                  cardiac_function:
                    type: string
                  allergy:
                    type: string
                  physical:
                    type: string
        """
        args = self.user_get_parser.parse_args()

        users = db_api.get_all_patients(args)

        res = [dict(u.items()) for u in users]
        return jsonify(res)

    def post(self):
        """
        add a patient
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            required: true
            name: user_name
            schema:   
              type: string
          - in: body
            required: true
            name: gender
            schema:
              type: string
          - in: body
            required: true
            name: age
            schema:
              type: integer
          - in: body
            name: height
            schema:
              type: number
              format: float
          - in: body
            name: weight
            schema:
              type: number
              format: float
          - in: body
            name: job
            schema:
              type: string
          - in: body
            name: edu
            schema:
              type: string
          - in: body
            special:
              type: string
          - in: body
            name: tel
            schema:
              type: string
          - in: body
            name: tumor
            schema:
              type: string
          - in: body
            name: tumor_metastasis
            schema:
              type: string
          - in: body
            name: tumor_treatment
            schema:
              type: string
          - in: body
            name: illness
            schema:
              type: string
          - in: body
            name: liver_function
            schema:
              type: string
          - in: body
            kidney_function:
              type: string
          - in: body
            name: cardiac_function
            schema:
              type: string
          - in: body
            name: allergy
            schema:
              type: string
          - in: body
            name: physical
            schema:
              type: string
        responses:
          200:
            description: patient primary key
            schema:
              type: object
              properties:
                id:
                  type: integer
        """
        args = self.user_add_parser.parse_args()
        print(args)
        user = db_api.add_patient(args)

        return make_response(jsonify({"id": user.id}), 201)


class PatientByIdResource(Resource):
    def __init__(self):
        super(PatientByIdResource, self).__init__()
        self.user_put_parser = reqparse.RequestParser()
        self.user_put_parser.add_argument('user_name', type=str)

    def get(self, uid: int):
        user = db_api.get_patient_by_id(uid)

        if user is not None:
            return jsonify(user.as_dict())
        return jsonify(None)

    def delete(self, uid: int):
        res = db_api.delete_patient_by_id(uid)

        return make_response(jsonify(res), 204)

    def put(self, uid: int):
        args = self.user_put_parser.parse_args()
        user = db_api.update_patient_by_id(uid, args)

        if user is not None:
            return user.id
        return -1


class BookResource(Resource):
    def __init__(self):
        super(BookResource, self).__init__()
        self.book_add_parser = reqparse.RequestParser()
        self.book_add_parser.add_argument('book_name', type=str, required=True)
        self.book_add_parser.add_argument('author_id', type=int, required=True)

    def get(self):
        books = DB_Obj.db.session.query().all()
        res = [[b[0].as_dict(), b[1].as_dict()] for b in books]
        return jsonify(res)

    def post(self):
        args = self.book_add_parser.parse_args()
        print(args)

        book = Book(
            book_name=args.book_name,
            author_id=args.author_id,
        )
        DB_Obj.db.session.add(book)
        DB_Obj.db.session.commit()

        return jsonify({"id": book.id})


app_api.add_resource(PatientListResource, '/patients')
app_api.add_resource(PatientByIdResource, '/patients/<int:uid>')
app_api.add_resource(BookResource, '/books')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8089')
