from constants import REDWIRE, GREENWIRE

class Circuit:
	def __init__(self, id):
		self.ownerid = id
		self.connections = [[], []]
		self.connected = False
	
	def connecTo(self, entid, circuitid, type):
		self.connected = True
		self.connections[type].append([entid, circuitid])

	def getJson(self):
		output = ""
		red = False
		if (len(self.connections[REDWIRE]) > 0):
			red = True
			output += '"red": ['
			
			for c in self.connections[REDWIRE]:
				output += "{"
				output += '"entity_id": ' + str(c[0]) + ","
				output += '"circuit_id": ' + str(c[1])
				output += "},"

			output = output[:-1] +  "]"
		if (red):
			output += ","
		if (len(self.connections[GREENWIRE]) > 0):
			output += '"red": ['
			
			for c in self.connections[GREENWIRE]:
				output += "{"
				output += '"entity_id": ' + str(c[0])
				output += '"circuit_id": '
				output += "},"

			output = output[:-1] +  "]"
		elif (red):
			output = output[:-1]
		return output