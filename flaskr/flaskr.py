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

#-----Database functions-----
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

@app.before_request
def before_request():
    g.db = connect_db()
    return

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#-----View Functions-----
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0],text=row[1])for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401) #Access Denied

    g.db.execute('insert into entries (title, text) values (?, ?)',
        [request.form['title'],request.form['text']])
    g.db.commit()

    flash('New entry was succesfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()