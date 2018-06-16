from printer import *
from segments.memory import *
from segments.packethandler import *
from MIDIdecoder import *
from MIDIdecoder2 import *
from constants import *
class Main:
	def __init__(self):
		self.entityid = 0
		self.printer = Printer()

		#self.m1 = Memory(self, 0, 0)
		#self.m2 = Memory(self, 0, 2)
		#self.m3 = Memory(self, 0, 4)

		#self.m1.connectTo(self.m2)
		#self.m2.connectTo(self.m3)
		
		#output = '{"blueprint": {"icons": [{"signal": {"type": "item","name": "constant-combinator"},"index": 1}],"entities": ['
		#output += self.m1.getJson() + ","
		#output += self.m2.getJson() + ","
		#output += self.m3.getJson()
		#output += '],"item": "blueprint","version": 68721836034}}'

		#print(self.printer.encode(output))

		self.packethandler = PacketHandler(self)
		
		self.music = MIDIDecoder2("sounds/base/mii.mid")
		self.channellock = [0,0,0,0,0,0]
		self.keys = []
		self.ids = []
		for i in range(0,len(self.music.tracks)):
			keyarray = self.music.tracks[i].getPressedKeys()
			if (len(keyarray) > 0):
				self.id = self.music.tracks[i].id
				self.getNewChannel()
				self.keys.append(keyarray)
				self.ids.append(self.music.tracks[i].id)

		self.currentkeys = []
		for keyarray in self.keys:
			self.currentkeys.append(keyarray.pop(0))

		self.values = [[],[],[],[],[],[]]
		#format [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]
		self.packeddata = []
		difference = math.floor((self.music.runtime/4 - math.floor(self.music.runtime/4))*4)
		print(self.music.runtime)
		for t in range(0, self.music.runtime + difference):
			#handle getting data in
			for i in range(0, len(self.values)):
				self.values[i].append(0)
			for i in range(0,len(self.currentkeys)):
				self.id = self.ids[i]
				while self.currentkeys[i][0] == t:
					for c in range(0, len(self.channellock)):
						if (self.id == self.channellock[i]):
							placed = self.placeKey(i)
							if (not placed):
								self.getNewChannel()
								break
							else:
								break
				#print("current key " + str(self.currentkeys[i]) + " time " + str(t))
			#handle getting data out
			if (len(self.values[i]) == 4):
				channelvalues = [0,0,0,0,0,0]
				for c in range(0,len(channelvalues)):
					value = self.values[c]
					channelvalues[c] = value[0] << 18 | value[1] << 12 | value[2] << 6 | value[3]
					self.values[c] = []
				self.packethandler.saveData(channelvalues)
								

						

		self.getJson()

	def placeKey(self, i):
		placed = False
		for c in range(0,len(self.channellock)):
			channel = self.channellock[c]
			if (channel == self.id and self.values[c][len(self.values[c])-1] == 0):
				self.values[c][len(self.values[c])-1] = self.currentkeys[i][1] + 1
				if (len(self.keys[i]) <= 0):
					self.currentkeys[i][0] = 2
					return True
				self.currentkeys[i] = self.keys[i].pop(0)
				return True
		return False
		
			


		#self.saveEvents()

	def getNewChannel(self):
		print(self.channellock)
		for i in range(0,len(self.channellock)):
			markedchannel = self.channellock[i]
			if (markedchannel == 0):
				self.channellock[i] = self.id
				return True
		print("Failed to find unused channel")
		return False

	def getJson(self):
		output = '{"blueprint": {"icons": [{"signal": {"type": "item","name": "constant-combinator"},"index": 1}],"entities": ['
		output += self.packethandler.getJson()
		output += '],"item": "blueprint","version": 68721836034}}'
		#print(output.replace(",", ",\n").replace("{","{\n").replace("}","\n}").replace("[","[\n").replace("]","\n]"))
		print(self.printer.encode(output))

	def getEntityId(self):
		self.entityid += 1
		return self.entityid
m = Main()
#http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA1_


#NOTES

# one storage = 4 * 0x3F hukommelse
#eks 110000 110000 110000 110000
# dette dækker over 4 oktaver eller 48 toner

#0  = 000000
#01 = 000001
#02 = 000010
#03 = 000011
#0000 0000 0001 0000 1000 0011
#4227 eller 1083
#000001000010000011000100
#‭000001000010000011000100‬