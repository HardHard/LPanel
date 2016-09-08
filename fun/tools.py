from flask.ext.sqlalchemy import SQLAlchemy
from classes.categore import Cat
db = SQLAlchemy()


def QCat():
    cohoselist = []
    query = db.session.query(Cat).all()
    for item in query:

        cohoselist.append((item.id, item.namecat))
    return cohoselist

class QQ():
    def QCat(self):
        cohoselist = []
        query = db.session.query(Cat).all()
        for item in query:
            cohoselist.append((item.id, item.namecat))
        return cohoselist