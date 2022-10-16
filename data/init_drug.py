import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import DB as db_cls

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db_cls.set_db(SQLAlchemy(app))

DB = db_cls.db
from db import api as db_api


if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
        # add durg data from json
        with open('data/drug_data.json', 'r', encoding='utf-8') as f:
            drug_data = json.load(f)
            for drug in drug_data:
                db_api.add_drug(drug)




