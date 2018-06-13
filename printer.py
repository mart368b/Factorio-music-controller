import zlib
import base64

class Printer:
	def __init__(self):
		pass

	def decode(self, txt):
		data = txt[1:]
		b64 = base64.b64decode(data)
		return zlib.decompress(b64)
		
	def encode(self, txt):
	    output = ""
	    i = 0

	    return base64.b64encode(txt)