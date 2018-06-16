from entities.wideentity import *
from wrappers.circuit import *
from wrappers.constant import *
from constants import REDWIRE, GREENWIRE
class Operator(WideEntity):
	def __init__(self, id, x, y, direction, first_signal, second_signal, action, output_signal):
		WideEntity.__init__(self, id, "arithmetic-combinator", x, y, direction)
		self.first_signal = first_signal
		self.second_signal = second_signal
		#output
		self.action = action
		self.output_signal = output_signal
		self.circuits = [Circuit(id), Circuit(id)]

	def connectTo(self, circuitIndex, id1, id2, connectionType):
		self.circuits[circuitIndex].connecTo(id1,id2,connectionType)

	def getSignal(self, name, signal):
		if (type(signal) is Constant):
			return signal.getJson() + ","
		else:
			return '"' + name + '": {' + signal.getJson() + "},"
	def getJson(self):
		
		first_signal = self.getSignal("first_signal", self.first_signal)
		second_signal = self.getSignal("second_signal", self.second_signal)
		operator = '"operation": "' + self.action + '",'
		output_signal = self.getSignal("output_signal", self.output_signal)
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

		return self.getEntityJson() + '"control_behavior":{' + '"arithmetic_conditions": {' + first_signal + second_signal + operator + output_signal[:-1] + "} }" + connections
		