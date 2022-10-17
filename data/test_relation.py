import json
import os
import sys
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask
from db import DB_Obj
from db import api as db_api
from db import models

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
DB_Obj.set_app(app)
DB = DB_Obj.db


if __name__ == '__main__':
    with app.app_context():
        DB_Obj.db.create_all()
        values = {
            "user_name": "test",
            "gender": 1,
            "age": 22
        }

        user = models.Patient()
        user.update(values)
        DB.session.add(user)
        DB.session.commit()

        diagnostic1 = models.Diagnostic()
        d1_uuid = str(uuid.uuid4())
        diagnostic1.update({"uuid": d1_uuid})
        diagnostic1.patient_basic_info = user

        diagnostic2 = models.Diagnostic()
        d2_uuid = str(uuid.uuid4())
        diagnostic2.update({"uuid": d2_uuid})
        diagnostic2.patient_basic_info = user
        DB.session.commit()

        print(dict(diagnostic1.items()))
        print(dict(diagnostic2.items()))
        print(db_api.get_all_patients())
        print(user.diagnostics)

