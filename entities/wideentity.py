from entities.entity import *

class WideEntity(Entity):
	"""docstring for WideEntity"""
	def __init__(self, id, name, x, y, direction):
		Entity.__init__(self, id, name, x, y)
		self.direction = direction
		if (direction == 2 or direction == 6):
			self.x -= 0.5
		if (direction == 4 or direction == 3):
			self.x -= 0.5

	def getEntityJson(self):
		id = '"entity_number": ' + str(self.id) + ','
		name = '"name": "' + self.name + '",'
		position = '"position": { "x": ' + str(self.x) + ', "y": ' + str(self.y) + "},"
		direction = '"direction": ' + str(self.direction) + ',' 
		return id + name + position + direction