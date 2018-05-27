import data

class cancer(object):

	def grow(self):
		if self.age - self.startAge == 1:
			stage = 1
			probFind = 0.10
			return False
		if self.age - self.startAge == 2:
			stage = 2
			probFind = 0.50
			return False
		if self.age - self.startAge == 3:
			stage = 3
			probFind = 0.95
			return False
		if self.age - self.startAge == 4:
			stage = 4
			return True
		return True




	def __init__(self, i, start):
		self.age = 0
		self.cancerType = i
		self.startAge = start

		self.cancerName = ""
		self.stage = 0
		self.isFound = 0
		self.ageFound = 0
		self.stageFound = 0

		self.probFind = 0
		
		