# -*- coding: utf-8 -*-
import os
class DBcong(object):
    DEBUG = True
    SECRET_KEY = os.urandom(25)
    SQLALCHEMY_DATABASE_URI = 'mysql://userlp:123456@localhost/lpdb'
