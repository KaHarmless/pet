import data

class cancer(object):



	def __init__(self, i, start):
		self.info = None
		self.cancerType = i
		self.startAge = start
		self.ownerAge = start

		self.cancerName = ""
		self.stage = 0
		self.isFound = 0
		self.ageFound = 0
		self.stageFound = 0

		self.isCured = False
		
		self.probablyDead = False
		

	def grow(self):
		# probFindArray = self.info[self.cancerType]
		self.stage += 1


