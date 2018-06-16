from entities.decider import *
from entities.combinator import *
from entities.operator import *
from wrappers.signal import *
from wrappers.constant import *
from constants import *
class Memory:
	def __init__(self, main, x, y, target):
		self.eachSignal = Signal("signal-each", 1)
		self.greenSignal = Signal("signal-green", 1)
		self.iSignal = Signal("signal-I", 1)
		self.constant = Constant(target)
		self.e1 = Operator( main.getEntityId(), -1 + x, y, 6, self.eachSignal, self.greenSignal, "*", self.eachSignal)
		self.c1 = Combinator(main.getEntityId(), x, y, 4)
		self.d1 = Decider(main.getEntityId(), 2 + x, y, 6, self.iSignal, self.constant, "=", self.greenSignal, False)
			

		self.e1.connectTo(0, self.c1.id, 1, REDWIRE)
		self.e1.connectTo(0, self.d1.id, 2, GREENWIRE)

		self.c1.connectTo(0, self.e1.id, 1, REDWIRE)

		self.d1.connectTo(1, self.e1.id, 1, GREENWIRE)

		self.nameindex = 0
		self.index = 1

		#self.addFilter(Signal("signal-2", 5))
	
	def connectTo(self, target):
		self.d1.connectTo(0, target.d1.id, 1, GREENWIRE)
		target.d1.connectTo(0, self.d1.id, 1, GREENWIRE)

		self.e1.connectTo(1, target.e1.id, 2, GREENWIRE)
		target.e1.connectTo(1, self.e1.id, 2, GREENWIRE)

	def isFull(self):
		return self.index == 19

	def getJson(self):
		output = "{"
		output += self.e1.getJson()
		output += "},{"
		output += self.c1.getJson()
		output += "},{"
		output += self.d1.getJson()
		output += "}"
		#.replace(",", ",\n").replace("{","{\n").replace("}","\n}").replace("[","[\n").replace("]","\n]")
		return output

	def addEntry(self, data):
		for i in range(0, len(data)):
			signal = Signal("signal-" + SIGNALNAMES[self.nameindex], data[i])
			self.nameindex += 1
			self.c1.addFilter(signal)
			self.index += 1