from printer import *
from entities.decider import *
from entities.combinator import *
from MIDIdecoder import *
class Main:
	def __init__(self):
		self.entityid = 0
		self.printer = Printer()
		self.musik = MIDIDecoder("sounds/mii.mid")

	def getEntityId(self):
		self.entityid += 1
		return self.entityid
m = Main()
#http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA1_