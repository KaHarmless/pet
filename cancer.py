import data

class cancer(object):



	def __init__(self, i, start):
		self.info = None
		self.cancerType = i
		self.startAge = start
		self.ownerAge = start

		self.cancerName = ""
		self.stage = 1
		self.isFound = False

		
		self.probablyDead = False
		

	def grow(self):
		# probFindArray = self.info[self.cancerType]
		self.stage += 1


