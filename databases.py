import json
import cryptocode

class Database():
	def auth(self, name, key):
		Cryptedkey = json.load(open('users.json'))[name]['key']
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
					db[name][base] = {collection: []}
					db[name][base][collection].append(data)
				except:
					db[name] = {base: {}}
					db[name][base][collection] = []
					db[name][base][collection].append(data)
		json.dump(db, open('database.json', 'w'), indent=4)

	def find(self, name, base, collection, identity):
		db = json.load(open("database.json"))
		try:
			docs = db[name][base][collection]
			res = []
			for i in docs:
				a = [i for (key, value) in set(identity.items()) & set(i.items())]
				if len(a) == len(identity):
					res.append(i)
			if not res:
				return None
			return res
		except Exception as e:
			print(e)
			return None

	def update(self, name, base, collection, identity, change):
		items = self.find(name, base, collection, identity)
		if items is not None:
			db = json.load(open("database.json"))
			try:
				docs = db[name][base][collection]
				res = []
				for num, i in enumerate(docs):
					res.extend([i,num] for (key, value) in set(identity.items()) & set(i.items()))
				for i in res:
					i[0]={**i[0], **change}
					docs[i[1]] = i[0]
				print(res)
				print(docs)
				db[name][base][collection] = docs
				json.dump(db, open('database.json', 'w'), indent=4)
				return True
			except Exception as e:
				print(e)
				return None
		return False

	def updateOne(self, name, base, collection, identity, change):
		items = self.find(name, base, collection, identity)
		if items is not None:
			db = json.load(open("database.json"))
			try:
				e=0
				docs = db[name][base][collection]
				res = []
				for num, i in enumerate(docs):
					res.extend([i,num] for (key, value) in set(identity.items()) & set(i.items()))
				for i in res:
					if e==0:
						i[0]={**i[0], **change}
						docs[i[1]] = i[0]
						e=1
				print(res)
				print(docs)
				db[name][base][collection] = docs
				json.dump(db, open('database.json', 'w'), indent=4)
				return True
			except Exception as e:
				print(e)
				return None
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
			try:
				e=0
				docs = db[name][base][collection]
				res = []
				for num, i in enumerate(docs):
					res.extend([i,num] for (key, value) in set(identity.items()) & set(i.items()))
				print(docs)
				for i in res:
					if e==0:
						print(i)
						docs.pop(i[1])
						e=1
				print(res)
				print(docs)
				db[name][base][collection] = docs
				json.dump(db, open('database.json', 'w'), indent=4)
				return True
			except Exception as e:
				print(e)
				return None
		return False

	def createDB(self, name, base):
		db = json.load(open("database.json"))
		try:
			print(db[name][base])
			return False
		except:
			db[name][base] = {}
			json.dump(db, open('database.json', 'w'), indent=4)
			return True

	def createCollection(self, name, base, collection):
		db = json.load(open("database.json"))
		try:
			a = db[name][base][collection]
			return False
		except:
			db[name][base][collection] = []
			json.dump(db, open('database.json', 'w'), indent=4)
			return True
	def getUser(self, name):
		db = json.load(open("database.json"))
		try:
			return db[name]
		except:
			db[name] = {}
			json.dump(db, open('database.json', 'w'), indent=4)
			return db[name]