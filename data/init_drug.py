import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask
from db import DB_Obj
from db import api as db_api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
DB_Obj.set_app(app)


if __name__ == '__main__':
    with app.app_context():
        DB_Obj.db.create_all()
        # rebuild drug table
        db_api.rebuild_drug_table()
        # add drug data from json
        with open('data/drug_data.json', 'r', encoding='utf-8') as f:
            drug_data = json.load(f)
            for drug in drug_data:
                db_api.add_drug(drug)




