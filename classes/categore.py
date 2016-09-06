from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Cat {0},{1},{2}>'.format(self.username, self.email, self.password )