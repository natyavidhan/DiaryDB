import cryptocode
from flask import Flask, request, jsonify, abort, render_template
import json
from databases import Database

app = Flask(__name__)

database = Database()

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return render_template('index.html')	
	key = json.load(open('keys.json'))[request.form['name']]
	if str(cryptocode.decrypt(key, request.form['key'])) == request.form['key']:
		return jsonify({'SUCCESS': 'Key Accepted'})
	return jsonify({'ERROR': 'Wrong Key'})




#-----------------------------------------------------API Routes---------------------------------------------------------------

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
			database.insert(data['name'], data['base'], data['collection'], str(data['data']))
			return jsonify({'SUCCESS': 'Data Inserted'})
		except Exception as e:
			return jsonify({"ERROR": f"{e}"})
	return jsonify({'ERROR': 'Wrong Key'})

@app.route('/find', methods=['POST'])
def findRoute():
	data = request.get_json()
	if database.auth(data['name'], data['key']):
		try:
			result = database.find(data['name'], data['base'], data['collection'], list(data['identity']))
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
				result = database.updateOne(data['name'], data['base'], data['collection'], list(data['identity']), list(data['change']))
				return jsonify({'SUCCESS': result})
			result = database.update(data['name'], data['base'], data['collection'], list(data['identity']), list(data['change']))
			return jsonify({'SUCCESS': result})
		except Exception as e:
			return jsonify({"ERROR": f"{e}"})
	return jsonify({'ERROR': 'Wrong Key'})

@app.route('/delete', methods=['POST'])
def deleteRoute():
	data = request.get_json()
	if database.auth(data['name'], data['key']):
		try:
			if data['one'] == "true":
				result = database.deleteOne(data['name'], data['base'], data['collection'], list(data['identity']))
				return jsonify({'SUCCESS': result})
			result = database.delete(data['name'], data['base'], data['collection'], list(data['identity']))
			return jsonify({'SUCCESS': result})
		except Exception as e:
			return jsonify({"ERROR": f"{e}"})
	return jsonify({'ERROR': 'Wrong Key'})

if __name__ == '__main__':
	app.run(debug=True)