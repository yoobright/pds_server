import datetime

import jsonschema
from flask import Flask, jsonify, make_response, abort
from flask.json import JSONEncoder
from db import DB_Obj
from flask_restful import Resource, Api
from flask_restful import reqparse
from flasgger import Swagger, swag_from
from flask_cors import CORS
from flask_migrate import Migrate

from webargs import fields
from webargs.flaskparser import use_args

from db import api as db_api
from db.books import Book
from defs import swagger_api


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if app.config['DEBUG']:
    app.config['SQLALCHEMY_ECHO'] = True
app.config['JSON_SORT_KEYS'] = False


DB_Obj.set_app(app)

with app.app_context():
    DB_Obj.db.create_all()

app_api = Api(app)
app.config['SWAGGER'] = {
    'title': 'OA3 API',
    'openapi': '3.0.2',
    # 'uiversion': 3,
}
swagger = Swagger(app)

migrate = Migrate(app, DB_Obj.db)


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
        self.user_add_parser.add_argument('uid', type=str, required=True)
        self.user_add_parser.add_argument('gender', type=str, required=True)
        self.user_add_parser.add_argument('age', type=int, required=True)
        self.user_add_parser.add_argument('height', type=float)
        self.user_add_parser.add_argument('weight', type=float)
        self.user_add_parser.add_argument('job', type=str)
        self.user_add_parser.add_argument('edu', type=str)
        self.user_add_parser.add_argument('special', type=str, default="???")
        self.user_add_parser.add_argument('tel', type=str)
        self.user_add_parser.add_argument('tumor', type=str, default="???")
        self.user_add_parser.add_argument('tumor_metastasis', type=str)
        self.user_add_parser.add_argument('tumor_treatment', type=str)
        self.user_add_parser.add_argument('illness', type=str)
        self.user_add_parser.add_argument('liver_function', type=str)
        self.user_add_parser.add_argument('kidney_function', type=str)
        self.user_add_parser.add_argument('cardiac_function', type=str)
        self.user_add_parser.add_argument('allergy', type=str)
        self.user_add_parser.add_argument('physical_q1', type=str)
        self.user_add_parser.add_argument('physical_q2', type=str)
        self.user_add_parser.add_argument('physical_q3', type=str)
        self.user_add_parser.add_argument('physical_q4', type=str)
        self.user_add_parser.add_argument('physical_q5', type=str)
        self.user_add_parser.add_argument('physical_score', type=str)

    @swag_from(swagger_api.patient_get_dict)
    def get(self):
        """
        get all patient list
        """
        args = self.user_get_parser.parse_args()

        users = db_api.get_all_patients(args)

        res = [dict(u.items()) for u in users]
        return jsonify(res)

    @swag_from(swagger_api.patient_post_dict)
    def post(self):
        """
        add a new patient
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

    @swag_from(swagger_api.patient_get_by_id_dict)
    def get(self, pid: int):
        user = db_api.get_patient_by_id(pid)

        if user is not None:
            return jsonify(dict(user.items()))
        return jsonify(None)

    @swag_from(swagger_api.patient_delete_by_id_dict)
    def delete(self, pid: int):
        res = db_api.delete_patient_by_id(pid)

        return make_response(jsonify(res), 204)

    def put(self, pid: int):
        args = self.user_put_parser.parse_args()
        user = db_api.update_patient_by_id(pid, args)

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


class DrugListResource(Resource):

    def __init__(self):
        super(DrugListResource, self).__init__()

    @swag_from(swagger_api.drug_get_dict)
    @use_args(
        {
            "drug_name": fields.Str(),
            "page": fields.Int(),
            "limit": fields.Int(),
        },
        location="query"
    )
    def get(self, args):
        drugs, total = db_api.get_all_drugs(args)

        res = [dict(d.items()) for d in drugs]
        return jsonify({
            "total": total,
            "data": res
        })


class DiagnosticListResource(Resource):

    def __init__(self):
        super(DiagnosticListResource, self).__init__()
        self.diagnostic_post_parser = reqparse.RequestParser()
        self.diagnostic_post_parser.add_argument(
            'uuid', type=str)
        self.diagnostic_post_parser.add_argument(
            'patient_basic_info_id', type=int, required=True)
        self.diagnostic_post_parser.add_argument(
            'pain_assessment_info_id', type=int)
        self.diagnostic_post_parser.add_argument(
            'prev_medication_info_id', type=int)
        self.diagnostic_post_parser.add_argument(
            'decision_info_id', type=int)
        self.diagnostic_post_parser.add_argument(
            'doctor_id', type=int)
        self.diagnostic_post_parser.add_argument(
            'previous_medication_issue', type=str)
        self.diagnostic_post_parser.add_argument(
            'recmd', type=str)

    @staticmethod
    def to_dict(diagnostics):
        res = []
        for d in diagnostics:
            data = dict(d.items())
            data["patient_basic_info"] = d.patient_basic_info.to_brief_info()
            res.append(data)

        return res

    # @swag_from(swagger_api.diagnostic_get_dict)
    @use_args(
        {
            "user_name": fields.Str(),
            "page": fields.Int(),
            "limit": fields.Int(),
        },
        location="query"
    )
    def get(self, args):
        diagnostics, total = db_api.get_all_diagnostics(args)
        res = self.to_dict(diagnostics)
        return jsonify({
            "total": total,
            "data": res
        })

    def post(self):
        args = self.diagnostic_post_parser.parse_args()
        print(args)
        diagnostic = db_api.add_diagnostic(args)

        if diagnostic is None:
            return make_response(
                jsonify({"id": -1}),
                422
            )

        return make_response(jsonify({
            "id": diagnostic.id,
            "uuid": diagnostic.uuid
        }), 201)


class DiagnosticResourceByUUID(Resource):

    def __init__(self):
        super(DiagnosticResourceByUUID, self).__init__()
        self.diagnostic_put_parser = reqparse.RequestParser()
        self.diagnostic_put_parser.add_argument(
            'previous_medication_issue',
            type=str)
        self.diagnostic_put_parser.add_argument(
            'recmd',
            type=str)
        self.diagnostic_put_parser.add_argument(
            'feedback_score',
            type=int)

    @staticmethod
    def to_dict(diagnostic):
        data = dict(diagnostic.items())
        data["patient_basic_info"] = dict(
            diagnostic.patient_basic_info.items())
        return data

    def get(self, uuid: str):
        diagnostic = db_api.get_diagnostic_by_uuid(uuid)
        # print(diagnostic)
        if diagnostic is not None:
            return jsonify(self.to_dict(diagnostic))
        return jsonify(None)

    def put(self, uuid: str):
        args = self.diagnostic_put_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        diagnostic = db_api.update_diagnostic_by_uuid(uuid, args)

        if diagnostic is not None:
            return make_response(
                jsonify({"uuid": diagnostic.uuid}), 200
            )

        return make_response(
            jsonify({"message": "resource not found"}), 400
        )


class PainAssessmentListResource(Resource):
    def __init__(self):
        super(PainAssessmentListResource, self).__init__()
        self.pain_assessment_post_parser = reqparse.RequestParser()
        self.pain_assessment_post_parser.add_argument(
            'diagnostic_uuid', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'causes', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'body_parts', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'pain_extra', type=str)
        self.pain_assessment_post_parser.add_argument(
            'character', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'level', type=int, required=True)
        self.pain_assessment_post_parser.add_argument(
            'aggravating_factors', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'relief_factors', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'breakout_type', type=str, required=True)
        self.pain_assessment_post_parser.add_argument(
            'breakout_freq', type=str, required=True)

    def post(self):
        args = self.pain_assessment_post_parser.parse_args()
        print(args)
        pain_assessment = db_api.add_pain_assessment(args)
        if pain_assessment is None:
            return make_response(
                jsonify({"id": -1}),
                422
            )

        return make_response(jsonify({
            "id": pain_assessment.id
        }), 201)


drug_table_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "drug_name": {"type": "string"},
            "spec": {"type": "string"},
            "dose": {"type": "number"},
            "dose_unit": {"type": "string"},
            "freq": {"type": "string"},
            "freq_unit": {"type": "string"},
            "duration": {"type": "string"}
        },
        "required": ["drug_name", "spec", "dose", "dose_unit",
                     "freq", "freq_unit", "duration"]
    }
}


class DiagnosticResourceByPatient(Resource):
    
    def __init__(self):
        super(DiagnosticResourceByPatient, self).__init__()
        self.diagnostic_get_parser = reqparse.RequestParser()
        self.diagnostic_get_parser.add_argument(
            'user_name', type=str, required=True)
        self.diagnostic_get_parser.add_argument(
            'uid', type=str, required=True)
        self.diagnostic_get_parser.add_argument(
            'latest', type=bool, default=False)
    
    @staticmethod
    def to_dict(diagnostic):
        data = dict(diagnostic.items())
        data["patient_basic_info"] = dict(
            diagnostic.patient_basic_info.items())
        return data

    def get(self):
        args = self.diagnostic_get_parser.parse_args()
        print(args)
        res = db_api.get_diagnostic_by_patient(args)
        if res is not None:
            if args.get("latest", False):
                return jsonify(self.to_dict(res))
            else:
                return jsonify([self.to_dict(d) for d in res])
        return jsonify(None)


class DecisionListResource(Resource):
    def __init__(self):
        super(DecisionListResource, self).__init__()
        self.decision_post_parser = reqparse.RequestParser()
        self.decision_post_parser.add_argument(
            'diagnostic_uuid', type=str, required=True)
        self.decision_post_parser.add_argument(
            'drug_table', type=dict, action='append')
        self.decision_post_parser.add_argument(
            'previous_medication_issue', type=str, required=True)
        self.decision_post_parser.add_argument(
            'recmd', type=str, required=True)
        self.decision_post_parser.add_argument(
            'recmd_constraint', type=bool, default=False)
        self.decision_post_parser.add_argument(
            'pcne_constraint', type=bool, default=False)

    def post(self):
        args = self.decision_post_parser.parse_args()
        print(args)
        if args.drug_table is not None:
            try:
                jsonschema.validate(args.drug_table, drug_table_schema)
            except Exception:
                return make_response(
                    jsonify({"message": "drug_table????????????"}),
                    400
                )

        decision = db_api.add_decision(args)
        if decision is None:
            return make_response(
                jsonify({"id": -1}),
                422
            )

        return make_response(jsonify({
            "id": decision.id
        }), 201)


class PreviousMedicationListResource(Resource):
    def __init__(self):
        super(PreviousMedicationListResource, self).__init__()
        self.previous_medication_post_parser = reqparse.RequestParser()
        self.previous_medication_post_parser.add_argument(
            'diagnostic_uuid', type=str, required=True)
        self.previous_medication_post_parser.add_argument(
            'drug_table', type=dict, action='append')
        self.previous_medication_post_parser.add_argument(
            'compliance_q1', type=str)
        self.previous_medication_post_parser.add_argument(
            'compliance_q2', type=str)
        self.previous_medication_post_parser.add_argument(
            'compliance_q3', type=str)
        self.previous_medication_post_parser.add_argument(
            'compliance_q4', type=str)
        self.previous_medication_post_parser.add_argument(
            'adverse_reaction', type=str)
        self.previous_medication_post_parser.add_argument(
            'adverse_reaction_drugs', type=str)

    def post(self):
        args = self.previous_medication_post_parser.parse_args()
        print(args)
        if args.drug_table is not None:
            try:
                jsonschema.validate(args.drug_table, drug_table_schema)
            except Exception:
                return make_response(
                    jsonify({"message": "drug_table????????????"}),
                    400
                )
        previous_medication = db_api.add_previous_medication(args)
        if previous_medication is None:
            return make_response(
                jsonify({"id": -1}),
                422
            )

        return make_response(jsonify({
            "id": previous_medication.id
        }), 201)


app_api.add_resource(PatientListResource, '/patients')
app_api.add_resource(PatientByIdResource, '/patients/<int:pid>')
app_api.add_resource(BookResource, '/books')
app_api.add_resource(DrugListResource, '/drugs')
app_api.add_resource(DiagnosticListResource, '/diagnostics')
app_api.add_resource(DiagnosticResourceByUUID,
                     '/diagnostics/uuid/<string:uuid>')
app_api.add_resource(DiagnosticResourceByPatient,
                     '/diagnostics/patient')
app_api.add_resource(PainAssessmentListResource, '/pain_assessments')
app_api.add_resource(DecisionListResource, '/decisions')
app_api.add_resource(PreviousMedicationListResource, '/previous_medications')


if __name__ == '__main__':
    ssl_context = ('/root/cert.cer', '/root/cert.key')
    app.run(host="0.0.0.0", port=8089, ssl_context=ssl_context)
