from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisascreet'

def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    

@app.route('/')
def index():
    return '<h1>You are in index</h1>'

@app.route('/<name>')
def hello_world(name):
    return '<h1>Hello {name}!</h1>'.format(name=name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select * from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=False, \
        mylist=[1,2,3,4], listsomething = [{'name': 'Zack'}, {'name': 'Zoey'}], results=results)

@app.route('/json')
def json():
    name = session['name']
    return jsonify({'key_1': 'value', 'key_aja': [1,2,3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are in Query Page</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        # name = request.form['name']
        # location = request.form['location']
        # return '<h1>Hello {}. You are from {}. You submit this shit successfully.'
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        return redirect(url_for('home', name=name, location=location))

# @app.route('/process', methods=['POST'])
# def process():
#     name = request.form['name']
#     location = request.form['location']

#     return '<h1>Hello {}. You are from {}. You have submitted form successfully</h1>'.format(name, location)

@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result': 'success', 'name': name, 'location': location, 'randomlist': randomlist})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return 'The ID is {}. The name is {}. The location is {}'.format(results[1]['id'], results[1]['name'], results[1]['location'])

if __name__ == '__main__':
    app.run(debug=True)