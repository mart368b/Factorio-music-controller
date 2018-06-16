class Constant:
	def __init__(self, value):
		self.value = value
	
	def getJson(self):
		return '"constant":' +  str(self.value)