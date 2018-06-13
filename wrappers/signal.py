class Signal:
	def __init__(self, name, count):
		self.name = name
		self.count = count
	
	def getJson(self, index):
		signal = '{"signal": { "type": "virtual", '
		signal += '"name": "' + self.name + '",'
		signal += "},"
		signal += '"count": ' + str(self.count) + ","
		signal += '"index": ' + str(index)
		signal += "},"
		return signal