import json
import cryptocode

class Database():
	def auth(self, name, key):
		Cryptedkey = json.load(open('keys.json'))[name]
		if str(cryptocode.decrypt(Cryptedkey, key)) == key:
			return True
		return False

	def insert(self, name, base, collection, data:dict):
		data = str(data).replace("'", '"')
		data = json.loads(data)
		db = json.load(open("database.json"))
		try:
			db[name][base][collection].append(data)
		except:
			try:
				db[name][base][collection] = []
				db[name][base][collection].append(data)
			except:
				try:
					db[name][base] = {}
					db[name][base][collection] = []
					db[name][base][collection].append(data)
				except:
					db[name] = {}
					db[name][base] = {}
					db[name][base][collection] = []
					db[name][base][collection].append(data)
		json.dump(db, open('database.json', 'w'), indent=4)

	def find(self, name, base, collection, identity):
		db = json.load(open("database.json"))
		try:
			docs = db[name][base][collection]
			res = []
			for i in docs:
				try:
					if i[identity[0]] == identity[1]:
						res.append(i)
				except:
					pass
			if len(res) == 0:
				return None
			return res
		except Exception as e:
			print(e)
			return None

	def update(self, name, base, collection, identity, change):
		items = self.find(name, base, collection, identity)
		if items is not None:
			for i in items:
				i[change[0]] = change[1]
			db = json.load(open("database.json"))
			docs = db[name][base][collection]
			res = []
			for i in docs:
				try:
					if i[identity[0]] == identity[1]:
						i[change[0]] = change[1]
					res.append(i)
				except:
					pass
			db[name][base][collection] = res
			json.dump(db, open('database.json', 'w'), indent=4)
			return True
		return False

	def updateOne(self, name, base, collection, identity, change):
		items = self.find(name, base, collection, identity)
		if items is not None:
			for i in items:
				i[change[0]] = change[1]
			db = json.load(open("database.json"))
			docs = db[name][base][collection]
			res = []
			e=0
			for i in docs:
				try:
					if i[identity[0]] == identity[1] and e == 0:
						i[change[0]] = change[1]
						e+=1
					res.append(i)
				except:
					pass
			db[name][base][collection] = res
			json.dump(db, open('database.json', 'w'), indent=4)
			return True
		return False

	def delete(self, name, base, collection, identity):
		items = self.find(name, base, collection, identity)
		if items is not None:
			db = json.load(open("database.json"))
			docs = db[name][base][collection]
			for i in items:
				docs.remove(i)
			db[name][base][collection] = docs
			json.dump(db, open('database.json', 'w'), indent=4)
			return True
		return False

	def deleteOne(self, name, base, collection, identity):
		items = self.find(name, base, collection, identity)
		if items is not None:
			db = json.load(open("database.json"))
			docs = db[name][base][collection]
			e=0
			for i in docs:
				try:
					if i[identity[0]] == identity[1] and e==0:
						docs.remove(i)
						e=1
				except:
					pass
			db[name][base][collection] = docs
			json.dump(db, open('database.json', 'w'), indent=4)
			return True
		return False

	def createDB(self, name, base):
		db = json.load(open("database.json"))
		try:
			db[name][base]
			return False
		except:
			db[name][base] = {}
			json.dump(db, open('database.json', 'w'), indent=4)
			return True

	def createCollection(self, name, base, collection):
		db = json.load(open("database.json"))
		try:
			db[name][base][collection]
			return False
		except:
			db[name][base][collection] = []
			json.dump(db, open('database.json', 'w'), indent=4)
			return True