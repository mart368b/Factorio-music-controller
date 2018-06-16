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
		compressed = zlib.compress(txt.encode())
		return "0" + str(base64.b64encode(compressed) ) [2:-1]