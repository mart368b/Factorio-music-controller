import struct

class MIDIDecoder:
	def __init__(self, path):
		f = open(path, "rb")
		self.file = f.read()
		self.currentbyte = 0
		f.close()
		print(self.file)
		if (self.getNextBytes(4).decode("utf-8") != "MThd"):
			raise ImportError("Unknown file format")
		self.getNextBytes(6)
		self.chunkCount = self.getSum(self.getNextBytes(2))
		self.currentChunk = 0
		self.ppqn = self.getSum(self.getNextBytes(2))

		print("track 1")
		self.track1 = Track(self.getNextBytes(4), self)
		print("track 2")
		self.track2 = Track(self.getNextBytes(4), self)

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
	def __init__(self, MTrkID, decoder):
		if (MTrkID != b'MTrk'):
			raise KeyError("Expected MTrk, got: " + MTrkID)
		#print("byte = " + str(decoder.currentbyte))
		self.length = int.from_bytes(decoder.getNextBytes(4), byteorder='big')
		#print("length = " + str(self.length))
		self.searching = True
		self.timing = 0
		while self.searching:
			self.timing = decoder.getVariableLengthQuantity()
			#print("byte = " + str(decoder.currentbyte) + " Timing = " + str(self.timing))
			eventType = self.getEventType(decoder)
			if (eventType != None):
				self.useEvent(eventType, decoder, self.timing)
			else:
				decoder.getNextBytes(1)
			

	def getEventType(self, decoder):
		flag = decoder.getNextBytes(1)
		#print("flag value = " + str(flag[0]))
		# Chacks for meta events
		if (flag == b'\xff'):
			return decoder.getNextBytes(1)[0]
		elif (flag[0] <= 127):
			return None
		else:
			return flag[0] & 0xF0


	def useEvent(self, eventType, decoder, timing):
		event = switcher[eventType]
		event(self, decoder, timing)
	
#events
def sequenceNumber(track, decoder, time):
	decoder.getNextBytes(3)
	print("sequenceNumber")

def text(track, decoder, time):
	length = decoder.getVariableLengthQuantity()
	if (length != 0):
		decoder.getNextBytes(length)
	print("text")

def copyright(track, decoder, time):
	track.skipEvent(decoder)
	print("copyright")

def trackName(track, decoder, time):
	length = decoder.getVariableLengthQuantity()
	if (length != 0):
		decoder.getNextBytes(length)
	print("trackName")

def instrument(track, decoder, time):
	track.skipEvent(decoder)
	print("instrument")

def lyric(track, decoder, time):
	track.skipEvent(decoder)
	print("lyric")

def marker(track, decoder, time):
	length = decoder.getVariableLengthQuantity()
	if (length == 0):
		decoder.getNextBytes(1)
	else:
		decoder.getNextBytes(length)
	print("marker")

def cuePoint(track, decoder, time):
	track.skipEvent(decoder)
	print("cuePoint")

def MIDIChannel(track, decoder, time):
	decoder.getNextBytes(2)
	print("MIDIChannel")

def MIDIPort(track, decoder, time):
	decoder.getNextBytes(2)
	print("MIDIPort")

def endOfTrack(track, decoder, time):
	print("end")
	decoder.getNextBytes(1)
	track.searching = False

def tempo(track, decoder, time):
	decoder.getNextBytes(4)
	print("tempo")

def SMPTEOffset(track, decoder, time):
	track.skipEvent(decoder)
	print("SMPTEOffset")

def timeSignature(track, decoder, time):
	decoder.getNextBytes(5)
	print("timeSignature")

def keySignature(track, decoder, time):
	decoder.getNextBytes(3)
	print("keySignature")

def proprietaryEvent (track, decoder, time):
	track.skipEvent(decoder)
	print("proprietaryEvent")

def keyReleas(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	decoder.getNextBytes(2)
	print("keyReleas")

def keyPressed(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	value = decoder.getNextBytes(2)
	print("keyPressed at channel " + str(channel) + " key pressed " + str(value[0]) + " timing " +str(time))

def localPreassureChange(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	print(decoder.getNextBytes(2))
	print("localPreassureChange")

def pedalChange(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	decoder.getNextBytes(2)
	print("pedal")

def changeInstrument(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	decoder.getNextBytes(1)
	print("changeInstrument")

def globalPreasureChange(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	decoder.getNextBytes(1)
	print("globalPreasureChange")

def pitchBendChange(track, decoder, time):
	channel = decoder.getCurrentByte() & 0x0F
	decoder.getNextBytes(2)
	print("pitchBendChange")

def unknownCommand(track, decoder, time):
	decoder.getNextBytes(2)
	print("unknownCommand")

switcher = {
    0: sequenceNumber,
    1: text,
    2: copyright,
    3: trackName,
    4: instrument,
    5: lyric,
    6: marker,
    7: cuePoint,
    32: MIDIChannel,
    33: MIDIPort,
    47: endOfTrack,
    81: tempo,
    84: SMPTEOffset,
    88: timeSignature,
    89: keySignature,
    127: proprietaryEvent,
    128: keyReleas,
    144: keyPressed,
    160: localPreassureChange,
    176: pedalChange,
    192: changeInstrument,
    208: globalPreasureChange,
    224: pitchBendChange
}

		
		

		