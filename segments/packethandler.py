from segments.memory import *
class PacketHandler:
	def __init__(self, main):
		self.y = 0
		self.main = main
		self.memorie = [Memory(self.main, 0, self.y, 1)]
		self.height = 1
		self.direction = 1
		self.lastdirection = 1
		
	def addNewMemory(self):
		self.y += 1
		newmemory =  Memory(self.main, 0, self.y, len(self.memorie)+1)
		newmemory.connectTo(self.memorie[len(self.memorie)-1])
		self.memorie.append(newmemory)

	def saveData(self, data):
		currentmemory = self.memorie[len(self.memorie)-1]
		if (currentmemory.isFull()):
			self.addNewMemory()
			self.saveData(data)
		else:
			currentmemory.addEntry(data)

	def getJson(self):
		output = ""
		for m in self.memorie:
			output += m.getJson() + ","
		return output[:-1]

