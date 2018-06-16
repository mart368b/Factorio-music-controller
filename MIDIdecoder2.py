import struct
import math
from constants import INDEXTOKEY

class MIDIDecoder2:
	def __init__(self, path):
		f = open(path, "rb")
		self.file = f.read()
		f.close()
		self.currentbyte = 0
		if (self.getNextBytes(4).decode("utf-8") != "MThd"):
			raise ImportError("Unknown file format")
		self.getNextBytes(6)
		self.chunkCount = self.getSum(self.getNextBytes(2))
		self.currentChunk = 0

		# STILL NEED TO BE FIXED maybe right shift by 2?
		self.ppqnStaus = self.getNextBytes(2)
		self.ppqn = 96

		self.BPM = 0
		self.timesignature = 24
		self.tracks = []
		self.runtime = 0

		self.tracks.append(Track(self.getNextBytes(4), self, 1, self.ppqn))
		self.tracks.append(Track(self.getNextBytes(4), self, 2, self.ppqn))

		#for i in range(1,self.chunkCount+1):
		#	self.tracks.append(Track(self.getNextBytes(4), self, i, self.ppqn))


	def getSum(self, byte):
		total = 0
		for i in range(len(byte)-1, -1, -1):
			total += byte[i]
		return total

	def getNextBytes(self, length):
		self.currentbyte += length
		temp = self.file[self.currentbyte - length: self.currentbyte]
		return temp

	def getCurrentByte(self):
		return self.file[self.currentbyte]

	def getVariableLengthQuantity(self):
		value = int.from_bytes(self.getNextBytes(1), byteorder='big')
		length = value
		i = 0
		while (value >> 7 != 0):
			value = int.from_bytes(self.getNextBytes(1), byteorder='big')
			length = length << 7
			length |= value 
			i += 1
			if (i >= 3):
				raise IndexError("no quantity could be found")
		return length
		
class Track:
	def __init__(self, MTrkID, decoder, id, ppqn):
		if (MTrkID != b'MTrk'):
			temp = decoder.getNextBytes(5)
			raise KeyError("Failed to locate track " + str(temp))
		self.id = id
		length = decoder.getNextBytes(4)
		self.offset = decoder.currentbyte
		self.length = length[0]<< 24 | length[1]<<16 | length[2]<<8 | length[3]
		self.chunk = decoder.getNextBytes(self.length)
		self.searching = True
		self.timing = 0
		self.ppqn = ppqn
		self.currentbyte = 0
		self.events = []
		self.pressednotes = 0
		self.releasednotes = 0
		self.lowestnote = 0xff
		self.highestnote = 0
		self.name = "Track " + str(id)
		self.instrument = "Unknown"
		self.log = ""
		while self.currentbyte < self.length-1:
			newtime = math.floor(self.getVariableLengthQuantity()/self.ppqn)
			if (newtime != 0):
				self.timing += newtime
			self.currentstatus = self.getNextBytes(1)[0]
			if (self.currentstatus < 0x80):
				pass
				#self.getNextBytes(1)
			elif (self.currentstatus == 0xFF):
				self.readMetaEvent(decoder)
			elif(self.currentstatus == 0xF0 or self.currentstatus == 0xF7):
				self.readSYSEXEvent()
			else:
				self.readMIDIEvent()
		print("-"*40)
		print(self.name)
		print("-"*40 + "\n" + " "*10 + " Reading log")
		print(self.log[:-1])
		print("-"*40)
		print("Total notes pressed: " + str(self.pressednotes) + " and released " + str(self.releasednotes))
		if (self.pressednotes > 0):
			print("lowest note " + self.getKey(self.lowestnote) + "(" + str(self.lowestnote) + ") highest note " + self.getKey(self.highestnote)+ "(" + str(self.highestnote) + ")" + " totalspan " + str(self.highestnote-self.lowestnote))
		print("\n")
		if (self.timing > decoder.runtime):
			decoder.runtime = self.timing
		#print(self.events)

	def readSYSEXEvent(self):
		length = self.getVariableLengthQuantity()
		data = self.getNextBytes(length)
		self.logEvent("System event", self.currentstatus, data)

	def readMetaEvent(self, decoder):
		status = self.getNextBytes(1)
		length = self.getVariableLengthQuantity()
		data = self.getNextBytes(length)
		if (status[0] == 0x03):
			self.name = str(data)[2:-1]
			self.log += str(self.timing) + ": Set track name to " + self.name + "\n"
		if (status[0] == 0x51):
			milliseconds = data[0]<<16 | data[1]<<8 | data[2]
			decoder.BPM = 60000000/ milliseconds
			self.log += str(self.timing) + ": Set tempo to " + str(milliseconds) + "\n"
		elif(status[0] == 0x58):
			self.timesignature = data[0]/2**data[1]
			self.log += str(self.timing) + ": Set time signature to " + str(self.timesignature) + "\n"
		elif (status[0] == 47):
			self.log += "End of track\n\n"
		else:
			self.logEvent("Meta event", status[0], data)

	def getKey (self, number):
		n = number % 12
		o = math.floor(number/11)-1
		#INDEXTOKEY[n] + " " + str(o) + "  " + str(n + 12*o)
		return INDEXTOKEY[n] + str(o)
	
	def pressKey (self, channel, key):
		self.events.append([self.timing, key])
		self.pressednotes += 1
		if (key < self.lowestnote):
			self.lowestnote = key
		if (key > self.highestnote):
			self.highestnote = key
		#print(str(self.timing) + ": Key pressed " + self.getKey(key))

	def releaseKey (self, channel, key):
		self.releasednotes += 1

	def readMIDIEvent(self):
		status = self.currentstatus >> 4
		if (status == 0x8):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(2)
			self.releaseKey(channel, data[0])
			return
		if (status == 0x9):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(2)
			self.pressKey(channel, data[0])
			return
		if (status == 0xA):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(2)
			return
		if (status == 0xB):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(2)
			self.logEvent("Control mode", channel, data)
			return
		if (status == 0xC):
			channel = self.currentstatus & 0x0F
			rawdata = self.getNextBytes(1)
			data = rawdata[0]
			currentinstrument = self.instrument
			if (data >= 0 and data <= 8):
				self.instrument = "Piano"
			if (data >= 9 and data <= 16):
				self.instrument = "Chromatic Percussion"
			if (data >= 17 and data <= 24):
				self.instrument = "Organ"
			if (data >= 25 and data <= 32):
				self.instrument = "Guitar"
			if (data >= 33 and data <= 40):
				self.instrument = "Bass"
			if (data >= 41 and data <= 48):
				self.instrument = "Strings"
			if (data >= 49 and data <= 56):
				self.instrument = "Ensemble"
			if (data >= 57 and data <= 64):
				self.instrument = "Brass"
			if (currentinstrument != self.instrument):
				self.log += str(self.timing) + ": Changed instrument to " + self.instrument + "\n"
			else:
				self.logEvent("Program change", channel, rawdata)
			return
		if (status == 0xD):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(1)
			return
		if (status == 0xE):
			channel = self.currentstatus & 0x0F
			data = self.getNextBytes(1)
			return
		if (status == 0xF):
			status = searchinge.currentstatus & 0x0F
			if (status == 0x0):
				data = self.getNextBytes(2)
				return
			if (status == 0x2):
				data = self.getNextBytes(2)
				return
			if (status == 0x3):
				data = self.getNextBytes(1)
				return
			return

	def logEvent(self,msg ,status , data):
		self.log += str(self.timing) + ": " + str(msg) + " - " + str(status) + " With data: " + str(data) + " - " + str(len(data)) + "\n"

	def getNextBytes(self, length):
		self.currentbyte += length
		temp = self.chunk[self.currentbyte - length: self.currentbyte]
		return temp

	def getVariableLengthQuantity(self):
		value = int.from_bytes(self.getNextBytes(1), byteorder='big')
		length = value & 0x7F
		i = 0
		while (value >> 7 != 0):
			value = int.from_bytes(self.getNextBytes(1), byteorder='big')
			length = length << 7
			length |= value 
			i += 1
			if (i >= 3):
				raise IndexError("no quantity could be found")
		return length

	def getPressedKeys(self):
		if (self.instrument == "Piano"):
			for i in range(0,len(self.events)):
				self.events[i][1] = self.events[i][1] - self.lowestnote
		for i in range(0,len(self.events)):
			self.events[i][0] = self.events[i][0]
		return self.events

#‭1000 0000 0101 0001 1000 0111‬
#‭100000 00 0101 0001 1000 0111‬

#F3 #E7
#54 - 100
