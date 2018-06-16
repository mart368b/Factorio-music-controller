from entities.entity import *
from wrappers.circuit import *
from wrappers.signal import *
from wrappers.constant import *
from constants import REDWIRE, GREENWIRE
class Combinator(Entity):
	"""docstring for Decider"""
	def __init__(self, id, x, y, direction):
		Entity.__init__(self, id, "constant-combinator", x, y)

		self.filters = []

		self.direction = direction

		self.circuits = [Circuit(id)]

	def connectTo(self, circuitIndex, id1, id2, connectionType):
		self.circuits[circuitIndex].connecTo(id1,id2,connectionType)

	def addFilter(self, signal):
		self.filters.append(signal)

	def getSignal(self, name, signal):
		if (type(signal) is Constant):
			return signal.getJson() + ","
		else:
			return '"' + name + '": {' + signal.getJson() + "},"

	def getJson(self):
		direction = '"direction": ' + str(self.direction)
		filters = ""
		if (len(self.filters) > 0):
			filters = ',"control_behavior":{"filters": ['
			for i in range(0, len(self.filters)):
				filters += "{" + self.getSignal("signal", self.filters[i])
				filters += '"count": ' + str(self.filters[i].count) + ","
				filters += '"index": ' + str(i+1)
				filters += "},"
			filters = filters[:-1] + "]}"
		connections = ""
		connected = False
		for c in self.circuits:
			if (c.connected):
				connected = True
		if (connected):
			connections += ',"connections": {'
			for i in range(0,len(self.circuits)):
				if (self.circuits[i].connected):
					connections += '"' + str(i+1) + '": {'
					connections += self.circuits[i].getJson()
					connections += "},"
			connections = connections[:-1] + "}"

		return self.getEntityJson() + direction + filters + connections
		