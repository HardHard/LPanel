from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namecat = db.Column(db.String(25), unique=True)
    comcat = db.Column(db.String(220))



    def __init__(self, namecat, comcat):
        self.namecat = namecat
        self.comcat = comcat
    def create(self):
        db.create_all()


    def __repr__(self):
        return '<Cat {0},{1},{2}>'.format(self.id, self.namecat, self.comcat)


