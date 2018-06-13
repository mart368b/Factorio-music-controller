from entities.entity import *
from wrappers.circuit import *
from wrappers.signal import *
from constants import REDWIRE, GREENWIRE
class Combinator(Entity):
	"""docstring for Decider"""
	def __init__(self, id, x, y):
		Entity.__init__(self, id, "constant_combinator", x, y)

		self.filters = []

		self.circuits = [Circuit(id)]
		self.addFilter(Signal("signal-A", 1))
		self.addFilter(Signal("signal-2", 5))

	def connectTo(self, circuitIndex, id1, id2, connectionType):
		self.circuits[circuitIndex].connecTo(id1,id2,connectionType)

	def addFilter(self, signal):
		self.filters.append(signal)

	def getJson(self):
		filters = ""
		if (len(self.filters) > 0):
			filters = '"control_behavior":{"filters": ['
			for i in range(0, len(self.filters)):
				filters += self.filters[i].getJson(i)
			filters = filters[:-1] + "]"
		connections = "}"
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
			connections = connections[:-1]

		return self.getEntityJson() + filters + connections
		