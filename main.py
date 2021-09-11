import cryptocode
from flask import Flask, request, jsonify, abort, render_template, session, redirect, url_for
import json
from databases import Database
import random
import string

app = Flask(__name__)

database = Database()

app.secret_key = ''.join(random.choice(
    string.ascii_uppercase + string.digits) for _ in range(32))


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'], data=database.getUser(session['user']['name']))
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    users = json.load(open('users.json'))
    data = request.form
    try:
        user = users[data['name']]
        password = cryptocode.decrypt(user['password'], data['password'])
        key = cryptocode.decrypt(user['key'], data['key'])
        if password == data['password'] and key == data['key']:
            session['user'] = {'name': data['name'], 'key': key}
            return redirect(url_for('home'))
        return jsonify({'RESULT': 'Wrong Password or Key'})
    except:
        return jsonify({'RESULT': 'User Not Found'})


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    users = json.load(open('users.json'))
    res = ''.join(random.choices(string.ascii_letters+string.digits, k=30))
    try:
        users[request.form['name']]
        return jsonify({'RESULT': 'User Already Exists'})
    except:
        users[request.form['name']] = {"password": cryptocode.encrypt(request.form['password'], request.form['password']),
                                       "key": cryptocode.encrypt(res, res)}
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        session['user'] = {'name': request.form['name'], 'key': res}
        return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# -----------------------------------------------------API Routes---------------------------------------------------------------


@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    key = json.load(open('keys.json'))[data['name']]
    if str(cryptocode.decrypt(key, data['key'])) == data['key']:
        return jsonify({'SUCCESS': 'Key Accepted'})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/insert', methods=['POST'])
def insertRoute():
    data = request.get_json()
    if database.auth(data['name'], data['key']):
        try:
            database.insert(data['name'], data['base'],
                            data['collection'], str(data['data']))
            return jsonify({'SUCCESS': 'Data Inserted'})
        except Exception as e:
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/find', methods=['POST'])
def findRoute():
    data = request.get_json()
    if database.auth(data['name'], data['key']):
        try:
            result = database.find(
                data['name'], data['base'], data['collection'], dict(data['identity']))
            return jsonify({'SUCCESS': result})
        except Exception as e:
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/update', methods=['POST'])
def updateRoute():
    data = request.get_json()
    if database.auth(data['name'], data['key']):
        try:
            if data['one'] == "true":
                result = database.updateOne(data['name'], data['base'], data['collection'], dict(data['identity']), dict(data['change']))
                return jsonify({'SUCCESS': result})
            result = database.update(data['name'], data['base'], data['collection'], data['identity'], data['change'])
            return jsonify({'SUCCESS': result})
        except Exception as e:
            print(e)
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/delete', methods=['POST'])
def deleteRoute():
    data = request.get_json()
    if database.auth(data['name'], data['key']):
        try:
            if data['one'] == "true":
                result = database.deleteOne(
                    data['name'], data['base'], data['collection'], data['identity'])
                return jsonify({'SUCCESS': result})
            result = database.delete(
                data['name'], data['base'], data['collection'], data['identity'])
            return jsonify({'SUCCESS': result})
        except Exception as e:
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/createDB', methods=['POST'])
def createDB():
    data = request.get_json()
    if database.auth(data['name'], data['key']) and data['base'] != "":
        try:
            res = database.createDB(data['name'], data['base'])
            print(res)
            return jsonify({'SUCCESS': 'Database Created'})
        except Exception as e:
            print(e)
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


@app.route('/createCollection', methods=['POST'])
def createCollection():
    data = request.get_json()
    if database.auth(data['name'], data['key']) and data['base'] != "" and data['collection'] != "":
        try:
            res = database.createCollection(
                data['name'], data['base'], data['collection'])
            print(res)
            return jsonify({'SUCCESS': 'Database Created'})
        except Exception as e:
            print(e)
            return jsonify({"ERROR": f"{e}"})
    return jsonify({'ERROR': 'Wrong Key'})


if __name__ == '__main__':
    app.run(debug=True)
