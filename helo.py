# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for,  flash
from flask import session as flask_session, abort
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from functools import wraps
from flask.ext.login import login_user , logout_user , current_user , login_required, user_logged_in
import os
from classes.categore import Cat
from fun.tools import  QQ
import init.confdb
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, StringField, PasswordField, validators,  TextAreaField, SelectMultipleField, SelectField
import os
#test Coment

from flask.ext.login import LoginManager
app = Flask(__name__)

#Config
app.config.from_object(init.confdb.DBcong)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Links(db.Model):
    idlink = db.Column(db.Integer, primary_key=True)
    idurlcat = db.Column(db.String(25))
    link = db.Column(db.String(900))
    delimiter = db.Column(db.String(900))
    encoding = db.Column(db.String(200))

    def __init__(self, idurlcat,  link, delimiter, encoding ):

        self.idurlcat = idurlcat
        self.link = link
        self.delimiter = delimiter
        self.encoding = encoding

    def create(self):
        db.create_all()


    def __repr__(self):
        return '<Links {0},{1},{2},{3},{4}>'.format(self.idlink, self.idurlcat, self.link, self.delimiter, self.encoding )


l = Links(1,1,1,1)
l.create()


class UrlCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcat = db.Column(db.String(25), unique=True)
    url = db.Column(db.String(500))
    pr = db.Column(db.String(10))
    tc = db.Column(db.String(10))
    spam = db.Column(db.String(50))
    indexgo = db.Column(db.String(10))
    indexya = db.Column(db.String(10))
    datareg = db.Column(db.String(10))
    ags = db.Column(db.String(10))

    def __init__(self, idcat, url, pr, tc, spam, indexgo, indexya, datareg, ags):
        self.idcat = idcat
        self.url = url
        self.pr = pr
        self.tc = tc
        self.spam = spam
        self.indexgo = indexgo
        self.indexya = indexya
        self.datareg = datareg
        self.ags = ags

    def create(self):
        db.create_all()

    def __repr__(self):
        return '<UrlCat {0},'.format(self.id, self.idcat, self.url, self.pr, self.tc, self.spam , self.indexgo ,
                                                                    self.indexya, self.datareg, self.ags)

u = UrlCat(1,2,3,4,5,6,7,8,9)
u.create()



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameproject = db.Column(db.String(25))
    listkey = db.Column(db.String(500))
    listcontext = db.Column(db.Text() )
    status = db.Column(db.String(500))

    def __init__(self, nameproject, listkey, listcontext, status):
        self.nameproject = nameproject
        self.listkey = listkey
        self.listcontext = listcontext
        self.status = status


    def create(self):
        db.create_all()


    def __repr__(self):
        return '<Project {0},{1},{2},{3},{4}>'.format(self.id, self.nameproject , self.listkey, self.listcontext, self.status)


p = Project(1,2,3,4)
p.create()


class AddCats(Form):
    namecats = StringField("namecats", [validators.Length(min=1, max=25)])
    comentcats = TextAreaField("comentcats", [validators.Length(min=1, max=220)])

class CatPrintForm(Form):
    Cat = SelectMultipleField(choices=[])

class CatPrintFormSelect(Form):
    Cat = SelectField(choices=[])
    Encoding = SelectField(choices=[])
    Url = StringField("Url", [validators.Length(min=1, max=250)])
    Delimiter = TextAreaField("Delimiter", [validators.Length(min=1, max=900)])

class CatEditForm(Form):
    idcats = StringField("idcats", [validators.Length(min=1, max=25)])
    namecats = StringField("namecats", [validators.Length(min=1, max=250)])
    commcats = StringField("commcats", [validators.Length(min=1, max=250)])

# Test
# try:
#
#     #admins = Cat('4adffddf555', 'admdfhfhha7mple.co55')
#
#     #db.create_all() # In case user table doesn't exists already. Else remove it.
#
#     # db.session.add(admins)
#     # #
#     # db.session.commit()
#     #db.session.flush() # This is needed to write the changes to database
#
# except exc.IntegrityError, exc:
#
#     if "Duplicate" in exc.message:
#         print "Neme Cat Used"


#end Test

def QCat():
    cohoselist = []
    query = db.session.query(Cat).all()
    for item in query:

        cohoselist.append((item.id, item.namecat))
    return cohoselist


def EditCat():
    cohoselist = []
    query = db.session.query(Cat).all()
    for item in query:

        cohoselist.append((item.id, item.namecat, item.comcat))
    return cohoselist


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
def sumcatnum(id):
    AllCat = Links.query.filter(Links.idurlcat == id).all()
    return AllCat
def sumsitecat(data):
    Temp = []
    body = []

    id = 0
    for item in data:
        print item
        id = id + 1
        num =len(sumcatnum(item[0]))

        body.append(id)

        for ritem in item:

            print ritem

            body.append(ritem)
            # body.append(ritem[1])
            # body.append(ritem[1])
        body.append(num)
        Temp.append(tuple(body))
        del body[:]
    return Temp

@app.route('/index')
@login_required
def index():
    # Delete Register
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    result = EditCat()
    obr =     sumsitecat(result)

    return render_template("index.html", formcat=obr)

@app.route('/cat<id>')
@login_required
def cat(id):
    print id, "ffff"
    sumcatnum(id)
    return render_template("catview.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/project')
@login_required
def project():
    pass

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
# @login_required
def cod():


    dir_path = os.path.dirname(os.path.realpath(__file__))
    cod = open( dir_path + "\\simple-code\\simple.php").read()
    return render_template("cod.html", title='Cod', cod=cod)





@app.route('/links',methods=['GET','POST'])
#@login_required
def links():

    formcatdel = CatPrintFormSelect(request.form)
    if request.method == 'POST' :
        ## self.idlink, self.idurlcat, self.link, self.delimiter, self.encoding  ##
        print formcatdel.Cat.data, "Cat"
        print formcatdel.Url.data
        print formcatdel.Delimiter.data
        print formcatdel.Encoding.data
        chekdubl =  Links.query.filter(Links.link == formcatdel.Url.data).all()
        print chekdubl, "Dub"
        if len(chekdubl) != 0:
            flash(u'Duplicate Url', 'Links')
            return redirect(url_for('links'))


        cname = Links(formcatdel.Cat.data, formcatdel.Url.data, formcatdel.Delimiter.data, formcatdel.Encoding.data)
        # cname.create()
        # db.create_all() # In case user table doesn't exists already. Else remove it.
        db.session.add(cname)
        #
        db.session.commit()
    formcatdel.Cat.choices = QCat()
    formcatdel.Encoding.choices  = [("utf-8", "utf-8"), ("windows-1251", "windows-1251")]


    return render_template("makelinks.html", title='Cod', formcat=formcatdel)


@app.route('/categories/<int:cat>')
@login_required
def categories(cat):
    pass
    print cat

    return render_template("cod.html", title='Cod', cod='cod')




@app.route('/addcats',methods=['GET','POST'])
# @login_required # Login

def addcats():




    forms = AddCats(request.form)
    if request.method == 'POST' and forms.validate():
        print forms.namecats.data
        print forms.comentcats.data
        cname = Cat(forms.namecats.data, forms.comentcats.data)
        # cname.create()
        # db.create_all() # In case user table doesn't exists already. Else remove it.
        db.session.add(cname)
        #
        db.session.commit()
        flash('Cat Add',"Cat")
        return redirect(url_for('addcats'))

    return render_template("addcats.html", form = forms)




@app.route('/deletecat',methods=['GET','POST'])
# @login_required # Login

def deletecat():
    print QCat()
    formcatdel = CatPrintForm(request.form)
    print request.method
    if request.method == 'POST' :
        print formcatdel.Cat.data
        db.session.query(Cat).filter(Cat.id == formcatdel.Cat.data[0]).delete(synchronize_session=False)
        # db.session.add(admin)

        db.session.commit() # This is needed to write the changes to database

        flash('Cat Del',"Cat")
        return redirect(url_for('deletecat'))

    elif request.method == 'GET':

        formcatdel.Cat.choices = QCat()
        return render_template("delcats.html",  formcat=formcatdel)






@app.route('/editcat',methods=['GET','POST'])
# @login_required # Login

def editcat():
    # for c in db.session.query(Cat).all():
    #     print c
    #     c.comcat = c.comcat + "ff"

    # db.session.commit()
    if request.method == 'POST':
        form = CatEditForm(request.form)
        print form.idcats.data
        print form.namecats.data
        print form.commcats.data

        db.session.query(Cat).filter(Cat.id == form.idcats.data).update({'namecat': form.namecats.data,'comcat': form.commcats.data})
        db.session.commit()
        flash('Cat Edit', "Cat")
        return redirect(url_for('editcat'))

    result = EditCat()
    print result
    return render_template("editcats.html", result =  result)



if __name__ == "__main__":
    app.run(debug=True,  port=8080)
