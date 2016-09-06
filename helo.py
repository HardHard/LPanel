# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for,  flash
from flask import session as flask_session, abort
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from functools import wraps
from flask.ext.login import login_user , logout_user , current_user , login_required, user_logged_in
import os
from classes.categore import *
import init.confdb
#ghg

from flask.ext.login import LoginManager
app = Flask(__name__)

#Config
app.config.from_object(init.confdb.DBcong)


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)




# Test
try:
    admins = Cat('4adffddf555', 'admdfhfhha7mple.co55','12ffhg556')

    # db.create_all() # In case user table doesn't exists already. Else remove it.

    db.session.add(admins)
    #
    db.session.flush() # This is needed to write the changes to database

except exc.IntegrityError, exc:

    if "Duplicate" in exc.message:
        print "Neme Cat Used"


#end Test


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)



    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0},{1},{2}>'.format(self.username, self.email, self.password )

#admin = User('admin', 'admin@example.com','123456')

#db.create_all() # In case user table doesn't exists already. Else remove it.    

#db.session.add(admin)

#db.session.commit() # This is needed to write the changes to database

# User.query.all()

# print User.query.filter_by(username='admin').first()



@login_manager.user_loader
def load_user(user_id):
    print user_id
    return User.query.get(user_id)

login_manager.login_view = 'login'

@app.route('/',methods=['GET','POST'])
def login():
    print current_user.is_authenticated

    # if current_user.is_authenticated == True:
    #     return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['pass']
    print password, "Pass"
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(url_for('index'))



@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    return render_template("index.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    print "Settinds"
    # if current_user.is_authenticated == False:
    #     return redirect(url_for('login'))
    print request.method
    if request.method == 'POST':
        useradd = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        print password, "Pass"
        try:
            newuser = User(useradd, email, password)
            db.session.add(newuser)
            db.session.commit() # This is needed to write the changes to database
        except:
            flash(u'User Not Add', 'User')
            return redirect(url_for('settings'))

        flash(u'User Add', 'User')
        return redirect(url_for('settings'))
    return render_template("settings.html")


@app.route('/cod')
@login_required
def cod():
    pass
    return render_template("cod.html", title='Cod', cod='cod')





@app.route('/links')
@login_required
def links():
    pass

    return render_template("cod.html", title='Cod', cod='cod')


@app.route('/categories/<int:cat>')
@login_required
def categories(cat):
    pass
    print cat

    return render_template("cod.html", title='Cod', cod='cod')



if __name__ == "__main__":
    app.run(debug=True,  port=8080)
