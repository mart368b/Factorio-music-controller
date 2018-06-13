class Entity:
	def __init__(self, id, name, x, y):
		self.id = id
		self.name = name
		self.x = x
		self.y = y

	def getEntityJson(self):
		id = '"entity_number": ' + str(self.id) + ','
		name = '"name": "' + self.name + '",'
		position = '"position": { "x": ' + str(self.x) + ', "y": ' + str(self.y) + "},"
		return id + name + position
	
	def getJson(self):
		print("I believe something went wrong")
		return ""