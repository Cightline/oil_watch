import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from sql.price_schema import *
from sql import initialize_sql



class CreateDB():
    def __init__(self, db_path):
        self.db_path = db_path
        self.base    = automap_base()
        self.engine  = create_engine(db_path, echo=True)



    def create(self):
        initialize_sql(self.engine)



if __name__ == '__main__':
    with open('config.json') as c:
        cfg = json.load(c)
        cdb = CreateDB(cfg['SQLALCHEMY_DATABASE_URI'])
        cdb.create()

