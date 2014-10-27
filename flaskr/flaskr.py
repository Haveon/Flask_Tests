import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
    abort, render_template, flash
from contextlib import closing

#config
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create application
app = Flask(__name__)
app.config.from_object(__name__) #looks at uppercase vars in file, sets env

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """
    Makes our sql database
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read()) #exec db intrucs at schema.sql
        db.commit() #Commit changes

if __name__ == '__main__':
    app.run()