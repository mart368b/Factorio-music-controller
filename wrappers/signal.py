class Signal:
	def __init__(self, name, count):
		self.name = name
		self.count = count
	
	def getJson(self):
		signal = '"type": "virtual", '
		signal += '"name": "' + self.name + '"'
		return signal