import cancer
import random
import data
import math

class person(object):


	def __init__(self): 

		# initial parameters of person
		self.age = 0
		self.sex = 0
		self.isAlive = True
		self.ear = [0, 0, 0, 0, 0]
		self.info = data.data()          # data object, our data container
		self.cancers = []
		self.dose = []
		self.age = self.generateAge()    # generate age
		self.startAge = self.age         # save initial age

		self.ifRad = False               # NEW if is having radiation

		self.toDie = False

		self.ageGetCancer = []

		for i in xrange(0,self.startAge):
			self.dose.append(0)


	# def generateAge(self):  # generating age of person due to distribution
	# 	dice = random.random();
	# 	return 20
	# 	if dice < 0.1873 :
	# 		return int(0 + random.random()*14)
	# 	if dice < 0.32 :
	# 		return int(15 + random.random()*9)
	# 	if dice < 0.7145 :
	# 		return int(25 + random.random()*29)
	# 	if dice < 0.8436 :
	# 		return int(55 + random.random()*9)
	# 	else:
	# 		return int(65 + random.random()*15)

	def generateAge(self):
		return 1


	def increaseAge(self): #################################

		# if self.age < 20:                       # if younger then 20 - has no radiation
		# 	return
		self.ifRad = True                       # if elder - make a radiation flag true
		if self.age < 60 and self.age > 20:
			#newDose = 6.23 + self.dose[-1]	# add a dose
			 newDose = 59.2 + self.dose[-1]	# add a dose 
		else: 
			newDose = self.dose[-1]
		

		growRes = False

		self.dose.append(newDose)               # add dose to the list of all lifetime doses
		self.isGettingCancer()                  # check if he's getting cancer this year
		for i in self.cancers:
			i.age = self.age
			growRes = i.grow()

		self.toDie = growRes
		self.age += 1                           # increment age






	def diagnosis(self):
		dice = random.random()
		for i in self.cancers:
			if dice < i.probFind:
				i.isFound = True
				i.ageFound = self.age
				return True
		return False





	def isGettingCancer(self):
		if self.age < 20:            # no cancer under 20 
			return
		self.generateEAR()           # calculate ear for this person
		
		# for i in xrange(0,1):        # loop for all cancers
		dice = random.random()   # get random value
		if dice < self.ear[4]:   # check if it passes
			self.makeCancer(0)   # male a cancer to him if he sould have one


	def generateEAR(self):   # calculate ear
		L = 5                # latency for solid cancer 5 year
		# if len(self.dose)<5:
		# 	return 0
		if self.age < 30:    # no radiation before 30
			eStar = 0
		else:
			eStar = (self.age - L - 30)/10    # e star from formula
		# for i in xrange(0,5):    # calculate ear for each type of cancer
		i = 4
		self.ear[i] =  self.info.getBetaS(self.sex, i) * self.dose[self.age - L -1] * math.exp(self.info.getGamma(i) * eStar) * ( ((self.age - L - 0.5)/60)**self.info.getEta(i) )/10**7
		

	#def generateEAR(self):
	#	# if self.age < 20:
	#	# 	ear1 = 0
	#	if self.age < 30:
	#		ear1 = self.dose[-5]*10**(-3)*40./10**4
	#	if self.age < 45:
	#		ear1 = self.dose[-5]*10**(-3)*23./10**4
	#	if self.age < 60:
	#		ear1 = self.dose[-5]*10**(-3)*20./10**4
	#	else:
	#		ear1 = self.dose[-5]*10**(-3)*67./10**4
	#		# ear1 = 0
	#	for i in xrange(0,5):
	#		self.ear[i] = ear1


	def makeCancer(self, i):      # make a cancer
		newCancer = cancer.cancer(i,self.age)
		self.cancers.append(newCancer)
		self.ageGetCancer.append(self.age)






